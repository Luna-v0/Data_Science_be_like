from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Protocol, Sequence, Tuple

import gymnasium as gym
import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
from torch import Tensor
from torch.distributions import Categorical

EnvFn = Callable[[], gym.Env]

@dataclass
class StepRecord:
    """One transition collected during an episode rollout."""
    obs: np.ndarray
    action: int
    reward: float
    log_prob: Tensor


@dataclass
class EpisodeBatch:
    """All data collected from a single full episode."""
    observations: List[np.ndarray]
    actions: List[int]
    rewards: List[float]
    log_probs: List[Tensor]

    @property
    def episode_return(self) -> float:
        return float(sum(self.rewards))

    @property
    def episode_length(self) -> int:
        return len(self.rewards)


@dataclass
class TrainingHistory:
    """Tracks scalar metrics across training."""
    episode_returns: List[float] = field(default_factory=list)
    episode_lengths: List[int] = field(default_factory=list)
    policy_losses: List[float] = field(default_factory=list)
    eval_checkpoints: List[int] = field(default_factory=list)
    eval_mean_returns: List[float] = field(default_factory=list)
    stopped_early: bool = False
    stop_reason: Optional[str] = None
    stop_episode: Optional[int] = None


@dataclass
class EarlyStoppingConfig:
    """
    Stop training when evaluation returns plateau or a target is reached.
    """
    patience_evals: int = 5
    min_delta: float = 0.0
    target_return: Optional[float] = None


class DiscretePolicyAgent(Protocol):
    """
    Minimal interface for a discrete-action policy-gradient agent.

    The trainer only needs:
    - sample_action: for training rollouts
    - update_from_episode: for REINFORCE update
    - predict_action: for evaluation/demo
    """
    def sample_action(self, obs: np.ndarray) -> Tuple[int, Tensor]:
        ...

    def predict_action(self, obs: np.ndarray) -> int:
        ...

    def update_from_episode(self, episode: EpisodeBatch) -> float:
        ...

def set_seed(seed: int) -> None:
    """Set NumPy and PyTorch seeds for more reproducible experiments."""
    np.random.seed(seed)
    torch.manual_seed(seed)


def to_tensor(obs: np.ndarray, device: torch.device) -> Tensor:
    """
    Convert a single observation to a float32 torch tensor with batch dimension.
    """
    return torch.as_tensor(obs, dtype=torch.float32, device=device).unsqueeze(0)


def compute_discounted_returns(rewards: Sequence[float], gamma: float) -> Tensor:
    """
    Compute rewards-to-go:
        G_t = r_t + gamma * r_{t+1} + gamma^2 * r_{t+2} + ...

    Returns a 1D float32 tensor of shape [T].
    """
    returns: List[float] = []
    running_return = 0.0

    for reward in reversed(rewards):
        running_return = reward + gamma * running_return
        returns.append(running_return)

    returns.reverse()
    out = torch.tensor(returns, dtype=torch.float32)

    # Normalization is not mathematically required, but often helps reduce variance.
    if len(out) > 1:
        out = (out - out.mean()) / (out.std() + 1e-8)

    return out

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

def evaluate_agent(
    env_fn: EnvFn,
    agent: DiscretePolicyAgent,
    num_episodes: int = 5,
    max_steps: Optional[int] = None,
    greedy: bool = True,
) -> Dict[str, float]:
    """
    Evaluate the agent on fresh environments.

    By default, uses greedy actions for a cleaner measure of current behavior.
    """
    returns: List[float] = []
    lengths: List[int] = []

    for _ in range(num_episodes):
        env = env_fn()
        obs, info = env.reset()

        terminated = False
        truncated = False
        total_reward = 0.0
        steps = 0

        while not (terminated or truncated):
            if greedy:
                action = agent.predict_action(obs)
            else:
                action, _ = agent.sample_action(obs)

            obs, reward, terminated, truncated, info = env.step(action)
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
    Plot return and policy loss curves.
    """
    plt.figure(figsize=(10, 4))
    plt.plot(history.episode_returns, alpha=0.35, label="episode return")
    smoothed_returns = moving_average(history.episode_returns, smoothing_window)
    if len(smoothed_returns) > 0:
        offset = smoothing_window - 1 if len(history.episode_returns) >= smoothing_window else 0
        plt.plot(range(offset, offset + len(smoothed_returns)), smoothed_returns, label="smoothed return")
    plt.xlabel("Episode")
    plt.ylabel("Return")
    plt.title("Training Returns")
    plt.legend()
    plt.show()

    plt.figure(figsize=(10, 4))
    plt.plot(history.policy_losses, alpha=0.8)
    plt.xlabel("Episode")
    plt.ylabel("Policy Loss")
    plt.title("Policy Loss")
    plt.show()

    if history.eval_checkpoints:
        plt.figure(figsize=(10, 4))
        plt.plot(history.eval_checkpoints, history.eval_mean_returns, marker="o")
        plt.xlabel("Episode")
        plt.ylabel("Eval Mean Return")
        plt.title("Evaluation Returns")
        plt.show()

def train_on_policy_agent(
    env_fn: EnvFn,
    agent: DiscretePolicyAgent,
    num_episodes: int = 500,
    max_steps_per_episode: Optional[int] = None,
    eval_every: int = 50,
    eval_episodes: int = 5,
    early_stopping: Optional[EarlyStoppingConfig] = None,
    verbose: bool = True,
) -> TrainingHistory:
    """
    Generic on-policy training loop for episode-based agents like REINFORCE.

    The only assumptions are:
    - agent can sample actions during training
    - agent knows how to update itself from one episode
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

        policy_loss = agent.update_from_episode(episode)

        history.episode_returns.append(episode.episode_return)
        history.episode_lengths.append(episode.episode_length)
        history.policy_losses.append(policy_loss)

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
                print(
                    f"[episode {episode_idx:4d}] "
                    f"train_return={episode.episode_return:7.2f} | "
                    f"loss={policy_loss:9.4f} | "
                    f"eval_mean_return={eval_stats['mean_return']:7.2f}"
                )

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
                    history.stop_episode = episode_idx
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

def make_cartpole_env(render_mode: Optional[str] = None) -> gym.Env:
    """
    Factory for CartPole-v1.

    Keep env creation in a function so the trainer can request fresh envs
    whenever needed.
    """
    return gym.make("CartPole-v1", render_mode=render_mode)

def run_demo_episode(
    env_fn: EnvFn,
    agent: DiscretePolicyAgent,
    greedy: bool = True,
    max_steps: Optional[int] = None,
) -> float:
    """
    Run one episode and print total return.

    For notebook video rendering later, this is a clean place to extend.
    """
    env = env_fn()
    obs, info = env.reset()

    total_reward = 0.0
    steps = 0
    terminated = False
    truncated = False

    while not (terminated or truncated):
        if greedy:
            action = agent.predict_action(obs)
        else:
            action, _ = agent.sample_action(obs)

        obs, reward, terminated, truncated, info = env.step(action)
        total_reward += float(reward)
        steps += 1

        if max_steps is not None and steps >= max_steps:
            break

    env.close()
    print(f"Demo return: {total_reward:.2f}")
    return total_reward



def rollout_episode(
    env: gym.Env,
    agent: DiscretePolicyAgent,
    max_steps: Optional[int] = None,
) -> EpisodeBatch:
    """
    Collect one full training episode using the agent's stochastic policy.
    """
    obs, info = env.reset()

    observations: List[np.ndarray] = []
    actions: List[int] = []
    rewards: List[float] = []
    log_probs: List[Tensor] = []

    steps = 0
    terminated = False
    truncated = False

    while not (terminated or truncated):
        action, log_prob = agent.sample_action(obs)

        next_obs, reward, terminated, truncated, info = env.step(action)

        observations.append(np.asarray(obs, dtype=np.float32))
        actions.append(int(action))
        rewards.append(float(reward))
        log_probs.append(log_prob.view(1))

        obs = next_obs
        steps += 1

        if max_steps is not None and steps >= max_steps:
            break

    return EpisodeBatch(
        observations=observations,
        actions=actions,
        rewards=rewards,
        log_probs=log_probs,
    )
