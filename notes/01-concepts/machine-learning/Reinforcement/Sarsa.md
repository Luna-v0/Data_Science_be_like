Is a [[Markov Decision Process (MDP)#Learning a MDP|on policy]] algorithm based on [[Temporal Difference (TD) Learning|TD Control]], it uses the following variation:

$$
\begin{gather}
\delta_t = r_{t+1} + \gamma \; Q(s_{t+1},a_{t+1}) - Q(s_t,a_t) \\ \\ 
Q(s_t,a_t) = Q(s_t,a_t) + \alpha \; \delta_t
\end{gather}
$$

The overall algorithm does as following:
1. Start with a zeroed Q matrix.
2. Initialize current state and action using a [[Exploration vs Exploitation#Heuristics|EE heuristics]].
3. For each step:
	1. Take a observation  $a_t \to (s_t,r_t)$
	2. Choose some action (using the EE heuristics)
	3. $Q(s,a) = Q(s,a) + \alpha \; \delta_t$
	4. $a_{t+1}, s_{t+1} = a_t,s_t$
	