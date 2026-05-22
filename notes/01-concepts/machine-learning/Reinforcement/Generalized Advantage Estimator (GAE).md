It is a simple estimator for the [[Policy Optimization (PG)#Vanilla Policy Gradient (VPG)|Advantage Function]] that uses the concept of [[Temporal Difference (TD) Learning]] to estimate a better Advantage. Which is computed by:
$$
A_t = \delta_t + \gamma \lambda\delta_{t+1} + \gamma^2\lambda^2\delta_{t+1} + ...
$$

Where $\lambda = 0$ makes (low variance, high bias):

$$
A_t = \delta_t
$$

And $\lambda = 1$ makes (high variance, low bias):
$$
A_t = \delta_t + \gamma \delta_{t+1} + \gamma^2\delta_{t+1} + ...
$$
Which is the same of no Advantage (See [[Policy Optimization (PG)#Vanilla Policy Gradient (VPG)]])