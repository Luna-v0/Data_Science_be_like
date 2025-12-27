They are based on the fact that you can re-write the optimal [[Markov Decision Process (MDP)#Q-value function|Q Function]] and the [[Markov Decision Process (MDP)#Value Function|Value Function]] as a recursion like this, where the `*` means optimal:

$$
\begin{align}
V^*(s) &= \max_{a \in Actions}[R(s,a) + \gamma \sum_{s' \in States} P(s'|s,a) V^*(s')]
\\ \\
Q^*(s,a) &= R(s,a) + \gamma \sum_{s' \in States} P(s'|s,a) \max_{a' \in Actions}Q^*(s',a')
 
\end{align}
$$


## Value Iteration
This simple algorithm computes the optimal policy by computing the [[Markov Decision Process (MDP)#Value Function|Value Function]] together with the [[Markov Decision Process (MDP)#Q-value function|Q function]] iterationally in pairs (Computes Q, then V, then Q, etc...). 

$$
\begin{gather}
Q(s,a) = R(s,a) + \gamma \sum_{s' \in States} P(s'|s,a) V(s') \\ \\
\forall a \in Actions \; \land \; \forall s \in States
\\ \\ 
V(s) = \max_{a} Q(s,a)

\\ \\ \forall s \in States
\end{gather}

$$

This approach may take less computational time, but it takes more iterations to converge.
## Policy Iteration
Policy Iteration in the other hand takes it by computing the [[Markov Decision Process (MDP)#Value Function|Value Function]] using the following definition of policy evaluation using [[Matrix]] notation:
$$
V^\pi = (I - \gamma P_\pi^{-1})R_\pi
$$
Where $V^\pi$ is the value following the policy $\pi$ and the $P_\pi$ is the [[Markov Decision Process (MDP)#Enviroment|Probability Tensor]] by always taking the policy actions (therefore $P_\pi$ is a Matrix)

Then you take the value of $V^\pi$ and pass it though this steps:
$$
Q(s,a) = R(s,a)+ \gamma \sum_{s' \in States} P(s'|s,a) V^\pi(s') 
$$
$$
\pi(s) = \operatorname*{argmax}_{a \in Actions}Q(s,a) 
$$
Since this approach uses inverse, it takes more computational time, but it takes less iterations to converge.