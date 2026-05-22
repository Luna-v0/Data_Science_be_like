
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Protocol, Sequence

import gymnasium as gym
import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
from torch import Tensor


EnvFn = Callable[[], gym.Env]


# ============================================================================
# Generic rollout data containers
# ============================================================================

@dataclass
class ActionSample:
    """
    Output returned by an agent during environment interaction.

    The environment API only cares about `action`.
    Everything else is stored so the algorithm can later decide how to use it.

    Examples:
    - REINFORCE: store `log_prob`
    - Baseline actor-critic: store `log_prob`, `value`
    - PPO/TRPO: store `log_prob`, `value`, `policy_stats`
    - Future LLM-style methods: store arbitrary metadata in `extras`
    """
    action: int
    log_prob: Optional[Tensor] = None
    value: Optional[Tensor] = None
    extras: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StepRecord:
    """
    One transition collected during a rollout.
    """
    obs: np.ndarray
    action: int
    reward: float
    next_obs: np.ndarray
    terminated: bool
    truncated: bool
    done: bool
    log_prob: Optional[Tensor] = None
    value: Optional[Tensor] = None
    extras: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EpisodeBatch:
    """
    All data collected from a single full episode.

    This is intentionally raw data.
    Returns, advantages, normalization, KL targets, clipping targets, etc.
    should be computed inside the algorithm, not here.
    """
    observations: List[np.ndarray]
    actions: List[int]
    rewards: List[float]
    next_observations: List[np.ndarray]
    terminateds: List[bool]
    truncateds: List[bool]
    dones: List[bool]
    log_probs: List[Optional[Tensor]]
    values: List[Optional[Tensor]]
    extras: List[Dict[str, Any]]

    @property
    def episode_return(self) -> float:
        return float(sum(self.rewards))

    @property
    def episode_length(self) -> int:
        return len(self.rewards)


@dataclass
class RolloutBatch:
    """
    A flattened on-policy batch collected across one or more episodes.
    """
    observations: List[np.ndarray]
    actions: List[int]
    rewards: List[float]
    next_observations: List[np.ndarray]
    terminateds: List[bool]
    truncateds: List[bool]
    dones: List[bool]
    log_probs: List[Optional[Tensor]]
    values: List[Optional[Tensor]]
    extras: List[Dict[str, Any]]
    episode_returns: List[float]
    episode_lengths: List[int]

    @property
    def num_steps(self) -> int:
        return len(self.rewards)

    @property
    def num_episodes(self) -> int:
        return len(self.episode_returns)

    @property
    def mean_episode_return(self) -> float:
        if not self.episode_returns:
            return 0.0
        return float(np.mean(self.episode_returns))

    @property
    def mean_episode_length(self) -> float:
        if not self.episode_lengths:
            return 0.0
        return float(np.mean(self.episode_lengths))


@dataclass
class TrainingHistory:
    """
    Tracks scalar metrics across training.
    """
    episode_returns: List[float] = field(default_factory=list)
    episode_lengths: List[int] = field(default_factory=list)
    policy_losses: List[float] = field(default_factory=list)
    metric_history: Dict[str, List[float]] = field(default_factory=dict)
    eval_checkpoints: List[int] = field(default_factory=list)
    eval_mean_returns: List[float] = field(default_factory=list)
    stopped_early: bool = False
    stop_reason: Optional[str] = None
    stop_iteration: Optional[int] = None


@dataclass
class EarlyStoppingConfig:
    """
    Stop training when evaluation returns plateau or a target is reached.
    """
    patience_evals: int = 5
    min_delta: float = 0.0
    target_return: Optional[float] = None


# ============================================================================
# Agent interfaces
# ============================================================================

class RolloutAgent(Protocol):
    """
    Smallest agent interface needed by the environment utilities.

    sample_action:
        Used during training rollouts. Returns an ActionSample object so the
        agent can attach algorithm-specific metadata without modifying pg_env.py.

    predict_action:
        Used during evaluation and demos. Usually greedy or deterministic.
    """
    def sample_action(self, obs: np.ndarray) -> ActionSample:
        ...

    def predict_action(self, obs: np.ndarray) -> int:
        ...


class EpisodeUpdateAgent(RolloutAgent, Protocol):
    """
    Agent that learns from one full episode at a time.
    Suitable for REINFORCE-style algorithms.
    """
    def update_from_episode(self, episode: EpisodeBatch) -> Dict[str, float] | float:
        ...


class BatchUpdateAgent(RolloutAgent, Protocol):
    """
    Agent that learns from flattened on-policy rollout batches.
    Suitable for baseline actor-critic, TRPO-style experiments, PPO, etc.
    """
    def update_from_batch(self, batch: RolloutBatch) -> Dict[str, float] | float:
        ...


# ============================================================================
# Utility helpers
# ============================================================================

def iter_minibatches(size: int, batch_size: int, shuffle: bool = True):
    indices = np.arange(size)
    if shuffle:
        np.random.shuffle(indices)
    for start in range(0, size, batch_size):
        yield indices[start:start + batch_size]


def set_seed(seed: int) -> None:
    """Set NumPy and PyTorch seeds for more reproducible experiments."""
    np.random.seed(seed)
    torch.manual_seed(seed)


def to_tensor(obs: np.ndarray, device: torch.device) -> Tensor:
    """
    Convert a single observation to a float32 torch tensor with batch dimension.
    """
    return torch.as_tensor(obs, dtype=torch.float32, device=device).unsqueeze(0)


class MLPPolicy(nn.Module):
    """
    Simple MLP that maps observations to action logits.
    Suitable for small discrete-control environments like CartPole.
    """
    def __init__(
        self,
        obs_dim: int,
        act_dim: int,
        hidden_sizes: Sequence[int] = (64, 64),
    ) -> None:
        super().__init__()

        layers: List[nn.Module] = []
        last_dim = obs_dim

        for hidden_dim in hidden_sizes:
            layers.append(nn.Linear(last_dim, hidden_dim))
            layers.append(nn.ReLU())
            last_dim = hidden_dim

        layers.append(nn.Linear(last_dim, act_dim))
        self.net = nn.Sequential(*layers)

    def forward(self, obs: Tensor) -> Tensor:
        """
        Return action logits of shape [batch_size, act_dim].
        """
        return self.net(obs)


class MLPValue(nn.Module):
    """
    Simple MLP that maps observations to scalar state-values.
    """
    def __init__(
        self,
        obs_dim: int,
        hidden_sizes: Sequence[int] = (64, 64),
    ) -> None:
        super().__init__()

        layers: List[nn.Module] = []
        last_dim = obs_dim

        for hidden_dim in hidden_sizes:
            layers.append(nn.Linear(last_dim, hidden_dim))
            layers.append(nn.ReLU())
            last_dim = hidden_dim

        layers.append(nn.Linear(last_dim, 1))
        self.net = nn.Sequential(*layers)

    def forward(self, obs: Tensor) -> Tensor:
        return self.net(obs).squeeze(-1)


# ============================================================================
# Rollout collection
# ============================================================================

def rollout_episode(
    env: gym.Env,
    agent: RolloutAgent,
    max_steps: Optional[int] = None,
) -> EpisodeBatch:
    """
    Collect one full training episode using the agent's stochastic policy.
    """
    obs, _ = env.reset()

    observations: List[np.ndarray] = []
    actions: List[int] = []
    rewards: List[float] = []
    next_observations: List[np.ndarray] = []
    terminateds: List[bool] = []
    truncateds: List[bool] = []
    dones: List[bool] = []
    log_probs: List[Optional[Tensor]] = []
    values: List[Optional[Tensor]] = []
    extras: List[Dict[str, Any]] = []

    steps = 0
    terminated = False
    truncated = False

    while not (terminated or truncated):
        action_sample = agent.sample_action(obs)
        next_obs, reward, terminated, truncated, _ = env.step(action_sample.action)
        done = bool(terminated or truncated)

        observations.append(np.asarray(obs, dtype=np.float32))
        actions.append(int(action_sample.action))
        rewards.append(float(reward))
        next_observations.append(np.asarray(next_obs, dtype=np.float32))
        terminateds.append(bool(terminated))
        truncateds.append(bool(truncated))
        dones.append(done)
        log_probs.append(action_sample.log_prob)
        values.append(action_sample.value)
        extras.append(dict(action_sample.extras))

        obs = next_obs
        steps += 1

        if max_steps is not None and steps >= max_steps:
            break

    return EpisodeBatch(
        observations=observations,
        actions=actions,
        rewards=rewards,
        next_observations=next_observations,
        terminateds=terminateds,
        truncateds=truncateds,
        dones=dones,
        log_probs=log_probs,
        values=values,
        extras=extras,
    )


def collect_rollout_batch(
    env_fn: EnvFn,
    agent: RolloutAgent,
    batch_size: int,
    max_steps_per_episode: Optional[int] = None,
) -> RolloutBatch:
    """
    Collect at least `batch_size` timesteps across as many fresh episodes as
    needed, then flatten them into one rollout batch.

    This stays intentionally algorithm-agnostic. The agent decides later how to
    compute returns, advantages, KL diagnostics, clipping targets, and so on.
    """
    observations: List[np.ndarray] = []
    actions: List[int] = []
    rewards: List[float] = []
    next_observations: List[np.ndarray] = []
    terminateds: List[bool] = []
    truncateds: List[bool] = []
    dones: List[bool] = []
    log_probs: List[Optional[Tensor]] = []
    values: List[Optional[Tensor]] = []
    extras: List[Dict[str, Any]] = []
    episode_returns: List[float] = []
    episode_lengths: List[int] = []

    total_steps = 0

    while total_steps < batch_size:
        env = env_fn()
        episode = rollout_episode(
            env=env,
            agent=agent,
            max_steps=max_steps_per_episode,
        )
        env.close()

        observations.extend(episode.observations)
        actions.extend(episode.actions)
        rewards.extend(episode.rewards)
        next_observations.extend(episode.next_observations)
        terminateds.extend(episode.terminateds)
        truncateds.extend(episode.truncateds)
        dones.extend(episode.dones)
        log_probs.extend(episode.log_probs)
        values.extend(episode.values)
        extras.extend(episode.extras)

        episode_returns.append(episode.episode_return)
        episode_lengths.append(episode.episode_length)
        total_steps += episode.episode_length

    return RolloutBatch(
        observations=observations,
        actions=actions,
        rewards=rewards,
        next_observations=next_observations,
        terminateds=terminateds,
        truncateds=truncateds,
        dones=dones,
        log_probs=log_probs,
        values=values,
        extras=extras,
        episode_returns=episode_returns,
        episode_lengths=episode_lengths,
    )


# ============================================================================
# Evaluation and visualization
# ============================================================================

def evaluate_agent(
    env_fn: EnvFn,
    agent: RolloutAgent,
    num_episodes: int = 5,
    max_steps: Optional[int] = None,
    greedy: bool = True,
) -> Dict[str, float]:
    """
    Evaluate the agent on fresh environments.
    """
    returns: List[float] = []
    lengths: List[int] = []

    for _ in range(num_episodes):
        env = env_fn()
        obs, _ = env.reset()

        terminated = False
        truncated = False
        total_reward = 0.0
        steps = 0

        while not (terminated or truncated):
            if greedy:
                action = agent.predict_action(obs)
            else:
                action = agent.sample_action(obs).action

            obs, reward, terminated, truncated, _ = env.step(action)
            total_reward += float(reward)
            steps += 1

            if max_steps is not None and steps >= max_steps:
                break

        env.close()
        returns.append(total_reward)
        lengths.append(steps)

    return {
        "mean_return": float(np.mean(returns)),
        "std_return": float(np.std(returns)),
        "mean_length": float(np.mean(lengths)),
    }


def moving_average(values: Sequence[float], window: int) -> np.ndarray:
    """
    Simple moving average for smoother plots.
    """
    arr = np.asarray(values, dtype=np.float32)
    if len(arr) < window:
        return arr
    kernel = np.ones(window, dtype=np.float32) / window
    return np.convolve(arr, kernel, mode="valid")


def plot_training_history(
    history: TrainingHistory,
    smoothing_window: int = 20,
) -> None:
    """
    Plot return and tracked metric curves.
    """
    if history.episode_returns:
        plt.figure(figsize=(10, 4))
        plt.plot(history.episode_returns, alpha=0.35, label="episode return")
        smoothed_returns = moving_average(history.episode_returns, smoothing_window)
        if len(smoothed_returns) > 0:
            offset = smoothing_window - 1 if len(history.episode_returns) >= smoothing_window else 0
            plt.plot(
                range(offset, offset + len(smoothed_returns)),
                smoothed_returns,
                label="smoothed return",
            )
        plt.xlabel("Iteration")
        plt.ylabel("Return")
        plt.title("Training Returns")
        plt.legend()
        plt.show()

    if history.policy_losses:
        plt.figure(figsize=(10, 4))
        plt.plot(history.policy_losses, alpha=0.8, label="policy_loss")
        plt.xlabel("Iteration")
        plt.ylabel("Loss")
        plt.title("Policy Loss")
        plt.legend()
        plt.show()

    for metric_name, values in history.metric_history.items():
        if not values:
            continue
        plt.figure(figsize=(10, 4))
        plt.plot(values, alpha=0.8, label=metric_name)
        plt.xlabel("Iteration")
        plt.ylabel(metric_name)
        plt.title(metric_name)
        plt.legend()
        plt.show()

    if history.eval_checkpoints:
        plt.figure(figsize=(10, 4))
        plt.plot(history.eval_checkpoints, history.eval_mean_returns, marker="o")
        plt.xlabel("Iteration")
        plt.ylabel("Eval Mean Return")
        plt.title("Evaluation Returns")
        plt.show()


# ============================================================================
# Training loops
# ============================================================================

def _coerce_metrics(update_output: Dict[str, float] | float) -> Dict[str, float]:
    if isinstance(update_output, dict):
        return {str(k): float(v) for k, v in update_output.items()}
    return {"policy_loss": float(update_output)}


def _update_history_from_metrics(history: TrainingHistory, metrics: Dict[str, float]) -> None:
    if "policy_loss" in metrics:
        history.policy_losses.append(float(metrics["policy_loss"]))

    for key, value in metrics.items():
        if key == "policy_loss":
            continue
        history.metric_history.setdefault(key, []).append(float(value))


def train_on_policy_agent(
    env_fn: EnvFn,
    agent: EpisodeUpdateAgent,
    num_episodes: int = 500,
    max_steps_per_episode: Optional[int] = None,
    eval_every: int = 50,
    eval_episodes: int = 5,
    early_stopping: Optional[EarlyStoppingConfig] = None,
    verbose: bool = True,
) -> TrainingHistory:
    """
    Generic on-policy training loop for episode-based agents like REINFORCE.
    """
    history = TrainingHistory()
    best_eval_return = float("-inf")
    evals_without_improvement = 0

    env = env_fn()

    for episode_idx in range(1, num_episodes + 1):
        episode = rollout_episode(
            env=env,
            agent=agent,
            max_steps=max_steps_per_episode,
        )

        metrics = _coerce_metrics(agent.update_from_episode(episode))

        history.episode_returns.append(episode.episode_return)
        history.episode_lengths.append(episode.episode_length)
        _update_history_from_metrics(history, metrics)

        should_evaluate = episode_idx % eval_every == 0 or episode_idx == 1
        if should_evaluate and (verbose or early_stopping is not None):
            eval_stats = evaluate_agent(
                env_fn=env_fn,
                agent=agent,
                num_episodes=eval_episodes,
                max_steps=max_steps_per_episode,
                greedy=True,
            )
            history.eval_checkpoints.append(episode_idx)
            history.eval_mean_returns.append(eval_stats["mean_return"])

            if verbose:
                msg = (
                    f"[episode {episode_idx:4d}] "
                    f"train_return={episode.episode_return:7.2f} | "
                    f"eval_mean_return={eval_stats['mean_return']:7.2f}"
                )
                if "policy_loss" in metrics:
                    msg += f" | policy_loss={metrics['policy_loss']:9.4f}"
                print(msg)

            if early_stopping is not None:
                current_eval_return = eval_stats["mean_return"]
                improved = current_eval_return > (best_eval_return + early_stopping.min_delta)

                if improved:
                    best_eval_return = current_eval_return
                    evals_without_improvement = 0
                else:
                    evals_without_improvement += 1

                target_reached = (
                    early_stopping.target_return is not None
                    and current_eval_return >= early_stopping.target_return
                )
                patience_exhausted = evals_without_improvement >= early_stopping.patience_evals

                if target_reached or patience_exhausted:
                    history.stopped_early = True
                    history.stop_iteration = episode_idx
                    history.stop_reason = (
                        f"target_return_reached ({current_eval_return:.2f} >= "
                        f"{early_stopping.target_return:.2f})"
                        if target_reached
                        else (
                            f"no eval improvement greater than {early_stopping.min_delta:.2f} "
                            f"for {early_stopping.patience_evals} evals"
                        )
                    )
                    if verbose:
                        print(f"Early stopping at episode {episode_idx}: {history.stop_reason}")
                    break

    env.close()
    return history


def train_on_policy_batches(
    env_fn: EnvFn,
    agent: BatchUpdateAgent,
    num_iterations: int = 100,
    batch_size: int = 2048,
    max_steps_per_episode: Optional[int] = None,
    eval_every: int = 10,
    eval_episodes: int = 5,
    early_stopping: Optional[EarlyStoppingConfig] = None,
    verbose: bool = True,
) -> TrainingHistory:
    """
    Generic on-policy training loop for batch-based agents.

    This is the loop you will likely keep for:
    - actor-critic with baseline
    - TRPO-style experiments
    - PPO
    - custom policy-gradient research variants
    """
    history = TrainingHistory()
    best_eval_return = float("-inf")
    evals_without_improvement = 0

    for iteration_idx in range(1, num_iterations + 1):
        batch = collect_rollout_batch(
            env_fn=env_fn,
            agent=agent,
            batch_size=batch_size,
            max_steps_per_episode=max_steps_per_episode,
        )

        metrics = _coerce_metrics(agent.update_from_batch(batch))

        history.episode_returns.extend(batch.episode_returns)
        history.episode_lengths.extend(batch.episode_lengths)
        _update_history_from_metrics(history, metrics)

        should_evaluate = iteration_idx % eval_every == 0 or iteration_idx == 1
        if should_evaluate and (verbose or early_stopping is not None):
            eval_stats = evaluate_agent(
                env_fn=env_fn,
                agent=agent,
                num_episodes=eval_episodes,
                max_steps=max_steps_per_episode,
                greedy=True,
            )
            history.eval_checkpoints.append(iteration_idx)
            history.eval_mean_returns.append(eval_stats["mean_return"])

            if verbose:
                msg = (
                    f"[iter {iteration_idx:4d}] "
                    f"batch_mean_return={batch.mean_episode_return:7.2f} | "
                    f"steps={batch.num_steps:5d} | "
                    f"episodes={batch.num_episodes:3d} | "
                    f"eval_mean_return={eval_stats['mean_return']:7.2f}"
                )
                if "policy_loss" in metrics:
                    msg += f" | policy_loss={metrics['policy_loss']:9.4f}"
                print(msg)

            if early_stopping is not None:
                current_eval_return = eval_stats["mean_return"]
                improved = current_eval_return > (best_eval_return + early_stopping.min_delta)

                if improved:
                    best_eval_return = current_eval_return
                    evals_without_improvement = 0
                else:
                    evals_without_improvement += 1

                target_reached = (
                    early_stopping.target_return is not None
                    and current_eval_return >= early_stopping.target_return
                )
                patience_exhausted = evals_without_improvement >= early_stopping.patience_evals

                if target_reached or patience_exhausted:
                    history.stopped_early = True
                    history.stop_iteration = iteration_idx
                    history.stop_reason = (
                        f"target_return_reached ({current_eval_return:.2f} >= "
                        f"{early_stopping.target_return:.2f})"
                        if target_reached
                        else (
                            f"no eval improvement greater than {early_stopping.min_delta:.2f} "
                            f"for {early_stopping.patience_evals} evals"
                        )
                    )
                    if verbose:
                        print(f"Early stopping at iteration {iteration_idx}: {history.stop_reason}")
                    break

    return history


# ============================================================================
# Environment factories and demos
# ============================================================================

def make_cartpole_env(render_mode: Optional[str] = None) -> gym.Env:
    """Factory for CartPole-v1."""
    return gym.make("CartPole-v1", render_mode=render_mode)


def run_demo_episode(
    env_fn: EnvFn,
    agent: RolloutAgent,
    greedy: bool = True,
    max_steps: Optional[int] = None,
) -> float:
    """
    Run one episode and print total return.
    """
    env = env_fn()
    obs, _ = env.reset()

    total_reward = 0.0
    steps = 0
    terminated = False
    truncated = False

    while not (terminated or truncated):
        if greedy:
            action = agent.predict_action(obs)
        else:
            action = agent.sample_action(obs).action

        obs, reward, terminated, truncated, _ = env.step(action)
        total_reward += float(reward)
        steps += 1

        if max_steps is not None and steps >= max_steps:
            break

    env.close()
    print(f"Demo return: {total_reward:.2f}")
    return total_reward
