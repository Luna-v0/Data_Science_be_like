It is basically a simpler version of [[Trust Region Policy Optimization (TRPO)]] which borrows a lot of its design. Given the same loss of the TRPO:
$$
L(\theta) = \mathbb{E}[r_t(\theta) A_t]
$$
The objective is simply:
$$
L(\theta) = \mathbb{E}[\min({
r_t(\theta) A_t, clip(r_t(\theta),1- \epsilon, 1+ \epsilon ) A_t 
})]
$$
Which is simply a constraint so that the loss do not explode. But we compute this differently then TRPO. Here the clip is doing the [[Kullback–Leibler Divergence (KL)]] function by limiting the locality. 

A big difference between TRPO and PPO is that TRPO tries to compute a second order derivative, which explode quadratically meaning is not much tractable to compute. 