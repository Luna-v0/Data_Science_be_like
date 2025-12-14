---
jupyter:
  jupytext:
    cell_metadata_filter: -all
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.18.1
  kernelspec:
    display_name: .venv
    language: python
    name: python3
---

# Experiment
In this notebook the simple Frozen Lake environment of Gymnasium will be study.
## Imports

```python
import gymnasium as gym
import numpy as np
```

## Setting up the Environments
I created one for training to go faster and another for visualising

```python
training_env = gym.make('FrozenLake-v1', map_name="8x8", is_slippery=True)
testing_env = gym.make('FrozenLake-v1', map_name="8x8", is_slippery=True, render_mode="human")
```

This are the states and actions

```python
states = training_env.observation_space
actions = training_env.action_space
```

## Collection the Data Points

```python
STEPS = 500000
current_state, _ = training_env.reset()
num_actions = actions.n
num_states = states.n
gamma = 0.99

data_points = np.zeros((STEPS, 4))


for i in range(STEPS):
    action = np.random.choice(range(num_actions))
    next_state, reward, terminated, truncated, info = training_env.step(action)
    data_points[i] = [current_state, action, reward, next_state]
    current_state = next_state
    if terminated or truncated:
        current_state, info = training_env.reset()
```

## Building the Reward Matrix and Transition Tensor

```python
transition_tensor = np.zeros((states.n, actions.n, states.n), dtype=np.float32)

state_action_counter = np.zeros((states.n, actions.n), dtype=np.int32)
# for each action states x states
state_action_tensor = np.zeros((states.n, actions.n,states.n), dtype=np.float32)

reward_matrix = np.zeros((states.n, actions.n), dtype=np.float32)

for i in range(STEPS):
    current_state, action, reward, next_state = data_points[i]
    current_state = int(current_state)
    action = int(action)
    next_state = int(next_state)
    state_action_counter[current_state, action] += 1
    state_action_tensor[current_state, action, next_state] += 1
    reward_matrix[current_state, action] += reward

# Normalize transition_tensor over next states (axis=2), not over actions!
# transition_tensor[state, action, next_state] = P(next_state | state, action)
transition_tensor = state_action_tensor / np.sum(state_action_tensor, axis=2, keepdims=True)
# Normalize reward_matrix by the count of (state, action) visits
reward_matrix = reward_matrix / np.maximum(state_action_counter, 1)  # Avoid division by zero
```

Just filtering some NaNs

```python
# turn all the nans into 0
reward_matrix = np.nan_to_num(reward_matrix, -1)

transition_tensor = np.nan_to_num(transition_tensor)
```

## The core Value Iteration algorithm

```python
err = 1
i = 0

V = np.ones(states.n)

while err > 1e-8:
  Q = np.zeros((states.n, num_actions))

  for action in range(num_actions):
    Q[:,action] = reward_matrix[:,action] + gamma * transition_tensor[:,action] @ V

  Vnew = np.max(Q, axis=1)
  err = np.linalg.norm(V - Vnew)
  V = Vnew
  i+=1

np.argmax(Q, axis=1)
```

## Testing

```python
import time

obs, info = testing_env.reset()

while True:
    action = np.argmax(Q[obs])
    obs, reward, terminated, truncated, info = testing_env.step(action)
    # sleep for 0.1 seconds
    time.sleep(0.1)
    if terminated or truncated:
        break
```

Note that sometimes it will fall into the whole since it has a probability of falling on it. 

```python
testing_env.close()
```
