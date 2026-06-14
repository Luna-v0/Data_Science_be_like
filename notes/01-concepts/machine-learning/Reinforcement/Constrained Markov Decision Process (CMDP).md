It is a extension of [[Markov Decision Process (MDP)]], but with a cost function $c(s,a)$ and a threshold $d$, with the following optimization problem:

$$
\max_\pi \;\mathbb{​E}_\pi​[\sum_t​\gamma^t r(s_t​,a_t​)] \quad s.t. \quad \mathbb{​E}_\pi​[\sum_t ​\gamma^t c(s_t​,a_t​)]≤d
$$
This modeling is used in Safe Reinforcement Learning, where you define the cost function as a separated signal 