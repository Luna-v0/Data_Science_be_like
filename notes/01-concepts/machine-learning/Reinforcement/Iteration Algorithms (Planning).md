They are based on the fact that you can re-write the optimal [[Markov Decision Process (MDP)#Q-value function|Q Function]] and the [[Markov Decision Process (MDP)#Value Function|Value Function]] as a recursion like this, where the `*` means optimal:

$$
\begin{gather}
V^*(s) &= \max_{a \in Actions}[R(s,a) + \gamma \sum_{s' \in States} P(s'|s,a) V^*(s')]
\\ \\
Q^*(s,a) &= R(s,a) = \gamma \sum_{s' \in States} P(s'|s,a) \max_{a' \in Actions}Q*(s',a')
 
\end{gather}
$$


## Value Iteration
This simple algorithm computes the optimal policy by computing the [[Markov Decision Process (MDP)#Value Function|Value Function]] together with the [[Markov Decision Process (MDP)#Q-value function|Q function]]. 