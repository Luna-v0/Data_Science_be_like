The idea of Policy Optimization is to skip the whole process for learning the optimal [[Markov Decision Process (MDP)#Q-value function|state-action pairs]] learned by [[Markov Decision Process (MDP)#Value Based|Value Based Algorithms]] like by [[Deep Q-Learning (DQN)|DQN]] and learn directly the optimal [[Markov Decision Process (MDP)#Policy|Policy]] and learn the model of the world and the reward implicitly. Since we learn directly the policy the model is represented as $\pi_\theta$ where $\pi$ is the policy and $\theta$ is the parameters of this model. Since we want to approximate a function usually the model is a [[Neural Networks (NN)]], but since the goal is to maximize [[Markov Decision Process (MDP)#Reward Function|reward]] it is used the negative of the [[Neural Networks (NN)#Loss function|Loss]]. A key advantaged of using PG is that since we are simply approximating a function the action and state space can be continuous. 

## Vanilla Policy Gradient (VPG)
The most basic Policy Gradient Algorithm is the VPG, it learns the policy via Gradient Ascend and it is a on-policy algorithm that can be used in either discrete or continuous action spaces. The VPG gradient is formalized as:

$$
\begin{gather*}
\tau = (s_0,a_0,s_1,a_1,s_2, ...,s_n)\\\\
\nabla_\theta J(\pi_\theta) = \mathbb{E}_{\tau \;\sim \; \pi_\theta} [\sum_{t=0}^T \nabla_\theta\log\pi_{\theta}(a_t|s_t)A^{\pi_\theta}(s_t,a_t)]
\end{gather*}
$$
Where $\tau$ is the trajectory, the $J$ function is the expected finite-horizon undiscounted return of the policy and the function $A$ is a advantage function for the current policy. The most simple Advantage function is the following:
$$

A^\pi(s,a)= Q^\pi(s,a) - V^\pi(s)  
$$

But since we skip the Q function and Value function entirely in this process the Advantage function must be approximated rather then computed. Therefore in the most simple implementation of VPG called REINFORCED, the Advantage function is estimated via the following definition:  

$$
G_t = \sum_{k=t}^{T} \gamma^{k-t}r_k
$$
The main problem with this implementation is that the [[Variance]] of $G$ is proportional to the variance of the reward, meaning that a sparse reward generates a sparse 