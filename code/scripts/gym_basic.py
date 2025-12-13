import gymnasium as gym
import numpy as np


env = gym.make('FrozenLake-v1', map_name="4x4", is_slippery=False)
env2 = gym.make('FrozenLake-v1', map_name="4x4", is_slippery=False, render_mode="human")


obs, info = env.reset()

dp_mem = - 1*np.ones((env.observation_space.n, env.action_space.n), dtype=np.int32)

ep_over = False
acc_reward = 0

def observe(current_state,last_state,last_action,reward):
    s = current_state
    if current_state == last_state:
        dp_mem[last_state,last_action] = -100
    else:
        dp_mem[last_state,last_action] = reward 
    missing_actions = np.where(dp_mem[s] == -1)[0]
    if len(missing_actions) > 1:
        return np.random.choice(missing_actions)
    elif len(missing_actions) == 0:
        return np.random.choice(range(env.action_space.n))
    else:
        return missing_actions[0]

last_state = 0


action = env.action_space.sample()

while np.any(dp_mem[dp_mem==-1]):
    
    obs, reward, terminated, truncated, info = env.step(action)
    action = observe(obs, last_state, action, reward)
    last_state = obs

    ep_over = truncated or terminated
    
    if ep_over:
        obs,info = env.reset()
        dp_mem[last_state] = -100
        last_state = 0

env.close()
print(dp_mem)
print("Reward ",acc_reward)
obs, info = env2.reset()

ep_over = False

policy = - np.ones(env.observation_space.n, dtype=np.int32)

i = 0
for state in dp_mem:
    policy[i] = np.argmax(state)
    i += 1 
print(policy)
while not ep_over:

    obs, reward, terminated, truncated, info = env2.step(policy[obs])

    ep_over = truncated or terminated

env2.close()

