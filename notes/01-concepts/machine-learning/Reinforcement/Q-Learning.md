Is a [[Markov Decision Process (MDP)#Learning a MDP|off policy]] algorithm based on [[Temporal Difference (TD) Learning|TD Control]], it uses the same variation as [[Sarsa]] except that it uses the following TD error:

$$
\delta_t = r_{t+1} + \max_{a'}Q(s_{t+1},a') - Q(s_t,a_t)
$$

Its algorithm is almost the same as [[Sarsa]], except it does not need to update the $a_{t+1}$ in the end of the loop since it doesn't have it. 

>[!tip] Q-Learning is important because it has a proof of convergence for optimal value
