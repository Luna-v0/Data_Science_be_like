---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.19.1
  kernelspec:
    display_name: .venv
    language: python
    name: python3
---


# Vanilla Policy Gradient (REINFORCE)



As discussed in the [[Policy Optimization (PG)]] the core objective is:

$$
\mathbb{E}\left[\log \pi_\theta(a_t\mid s_t) \cdot G_t\right]
$$
This implementation does not use baseline.

```python
from typing import Optional, Sequence, Tuple

import gymnasium as gym
import numpy as np
import torch
from torch import Tensor
from torch.distributions import Categorical

from pg_env import (
    EarlyStoppingConfig,
    EnvFn,
    EpisodeBatch,
    MLPPolicy,
    make_cartpole_env,
    plot_training_history,
    run_demo_episode,
    set_seed,
    to_tensor,
    train_on_policy_agent,
)

```

This is what basically works as the Advantage function.

```python
def compute_discounted_returns(rewards: Sequence[float], gamma: float) -> Tensor:
    """
    Compute rewards-to-go:
        G_t = r_t + gamma * r_{t+1} + gamma^2 * r_{t+2} + ...

    Returns a 1D float32 tensor of shape [T].
    """
    returns = []
    running_return = 0.0

    for reward in reversed(rewards):
        running_return = reward + gamma * running_return
        returns.append(running_return)

    returns.reverse()
    return torch.tensor(returns, dtype=torch.float32)
```

This simply normalize the returns. 

```python
def normalized_returns(rewards: Sequence[float], gamma: float) -> Tensor:
    """
    Compute discounted rewards-to-go and normalize them.
    """
    returns = compute_discounted_returns(rewards=rewards, gamma=gamma)

    if returns.numel() > 1:
        returns = (returns - returns.mean()) / (returns.std() + 1e-8)

    return returns

```

Here we implement the Reinforce Agent. 

```python
class ReinforceAgent:
    """
    Minimal REINFORCE agent for discrete action spaces.

    This class owns:
    - the policy network
    - the optimizer
    - the single-episode REINFORCE update

    It does not own the environment or the training loop.
    """

    def __init__(
        self,
        obs_dim: int,
        act_dim: int,
        hidden_sizes: Sequence[int] = (64, 64),
        learning_rate: float = 1e-2,
        gamma: float = 0.99,
        device: Optional[torch.device] = None,
    ) -> None:
        self.device = device or torch.device("cpu")
        self.gamma = gamma

        self.policy = MLPPolicy(
            obs_dim=obs_dim,
            act_dim=act_dim,
            hidden_sizes=hidden_sizes,
        ).to(self.device)

        self.optimizer = torch.optim.Adam(self.policy.parameters(), lr=learning_rate)

    def distribution(self, obs: np.ndarray) -> Categorical:
        """Build the current policy distribution for one observation."""
        obs_tensor = to_tensor(obs, self.device)
        logits = self.policy(obs_tensor)
        return Categorical(logits=logits)

    def sample_action(self, obs: np.ndarray) -> Tuple[int, Tensor]:
        """
        Sample an action during training and return:
        - the sampled action
        - the log-probability of that exact sampled action
        """
        dist = self.distribution(obs)
        action = dist.sample()
        log_prob = dist.log_prob(action)
        return int(action.item()), log_prob

    def predict_action(self, obs: np.ndarray) -> int:
        """Greedy action selection used during evaluation or demos."""
        with torch.no_grad():
            obs_tensor = to_tensor(obs, self.device)
            logits = self.policy(obs_tensor)
            action = torch.argmax(logits, dim=-1)
            return int(action.item())

    def update_from_episode(self, episode: EpisodeBatch) -> float:
        """
        Apply one REINFORCE update from a single complete episode.

        Objective:
            maximize sum_t log pi(a_t | s_t) * G_t

        Because PyTorch optimizers do gradient descent, we minimize the negative
        of that objective.
        """
        returns = normalized_returns(episode.rewards, gamma=self.gamma).to(self.device)
        log_probs = torch.cat(episode.log_probs, dim=0)

        loss = -(log_probs * returns).sum()

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        return float(loss.item())

```

## Environment-facing helper

The notebook only needs a small builder that inspects the environment and creates a compatible agent.


## Return signal used by this notebook

For this first REINFORCE version, the learning signal is the **normalized discounted return**. Later, we will replace this with a baseline-derived advantage.

```python
def build_reinforce_agent_from_env(
    env_fn: EnvFn,
    hidden_sizes: Sequence[int] = (64, 64),
    learning_rate: float = 1e-2,
    gamma: float = 0.99,
    device: Optional[torch.device] = None,
) -> ReinforceAgent:
    """
    Inspect one environment instance to infer observation and action sizes,
    then construct a compatible REINFORCE agent.
    """
    env = env_fn()

    assert isinstance(env.observation_space, gym.spaces.Box), "Expected Box observation space."
    assert isinstance(env.action_space, gym.spaces.Discrete), "Expected Discrete action space."

    obs_dim = int(np.prod(env.observation_space.shape))
    act_dim = int(env.action_space.n)

    env.close()

    return ReinforceAgent(
        obs_dim=obs_dim,
        act_dim=act_dim,
        hidden_sizes=hidden_sizes,
        learning_rate=learning_rate,
        gamma=gamma,
        device=device,
    )

```

```python
set_seed(42)

env_fn: EnvFn = lambda: make_cartpole_env(render_mode=None)

agent = build_reinforce_agent_from_env(
    env_fn=env_fn,
    hidden_sizes=(32, 32),
    learning_rate=3e-4,
    gamma=0.99,
)

history = train_on_policy_agent(
    env_fn=env_fn,
    agent=agent,
    num_episodes=10_000,
    eval_every=25,
    eval_episodes=10,
    early_stopping=EarlyStoppingConfig(
        patience_evals=15,
        min_delta=5.0,
    ),
    verbose=True,
)

plot_training_history(history)

if history.stopped_early:
    print(f"Stopped at iteration {history.stop_iteration}: {history.stop_reason}")

```

```python
visual_env: EnvFn = lambda: make_cartpole_env(render_mode="human")

run_demo_episode(visual_env, agent, greedy=True)

```
