It is a iteration over the [[Policy Optimization (PG)#Vanilla Policy Gradient (VPG)|REINFORCE]], it uses the concept of [[Local Approximation]] (known as the surrogate objective) for optimizing the policy. 

To hold this local approximation we keep two separated version of the policy one old and one updated, and to check if that locality holds between the two policies and optimize base on the newer policy for that we need [[Kullback–Leibler Divergence (KL)|KL divergence]].

We define the loss of TRPO we take:

$$
L(\theta) = \mathbb{E} [e^{(\log \pi_\theta (a_t|s_t) - \log \pi_{old} (a_t|s_t))} A_t] = \mathbb{E} [\frac{ \pi_\theta (a_t|s_t)}{\pi_{old} (a_t|s_t)} A_t]
$$

Constrained by:

$$
D_{KL} (\pi_{old}||\pi_\theta) \le \delta
$$
Where $\delta$ is a hyperparameter (the locality).

## Improvement of the update using [[Hessian]]

There is a better way to optimize TRPO, meaning a smart way to take the step. Which is the by taking the Hessian of KL. Basically KL is the way of comparing two policies and checking the way the policies change, meaning the way the KL [[Vector Spaces]] work, you can measure how different the policies were modified in the correct direction. Since Hessian for this case is intractable to compute we use a [[Fisher Information Matrix]]. That basically computes:
$$
H = \nabla^2 D_{KL}
$$

Because:

$$
\mathbb{E}[\nabla\log\pi\nabla\log\pi^T] = \nabla^2 D_{KL}
$$
And
$$
H x= \nabla_\theta L
$$

Another noticeable improvement that can be done is using [[Generalized Advantage Estimator (GAE)]]. 