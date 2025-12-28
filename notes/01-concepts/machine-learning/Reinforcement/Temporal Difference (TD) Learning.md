Is one of the [[Markov Decision Process (MDP)#Value Based|Value Based]] approaches, it relies on bootstrapping and learn by sampling the environment. To estimate a new [[Markov Decision Process (MDP)#Value Function|Value Function]] it uses the following recursion:

$$
\begin{gather}
\delta_t = r_{t+1} + \gamma V(s_{t+1}) - V(s_t)
\\ \\
V(s_t) = V(s_t) + \alpha \; \delta_t
\end{gather}
$$

Where the $\delta$ is often called the Temporal Difference Error. The idea is that it computes a better estimation for $V$ then the previous. 

This method is the bases of other RL Algorithms like [[Q-Learning]] and [[Sarsa]].

