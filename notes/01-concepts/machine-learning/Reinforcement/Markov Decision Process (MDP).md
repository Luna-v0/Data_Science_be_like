MDP is a generic framework for modelling decision problem. It models the environment as Probabilistic Finite Automaton (PFA), where actions are model as transitions, but with a caveat, this transitions has probabilities, so the leading state changes. 

There are other important notions to MDP which will be discussed through out this document. 

Considering:
$$
\; s \in States \; \wedge \; a \in Actions
$$
# Policy
Defines the way the agent should behave at a given state. Mathematically it can be:

$$
\pi(s) \to a \\ \\
$$

Notice a important property, that for a finite number of states this could also be defined as a [[Vector]] which maps the state to its expected summed reward. Like this:
# Reward Function
It's a function that defined maximation objective of the agent. It's often analogous to pain and pleasure in biology or to profit in finance, and so on. Mathematically:
$$
R(s_t,a_t,s_{t+1}) \to \mathbb{R}
$$
>[!obs] $t$ refers to current and $t+1$ refers to next interations.
# Value Function
Also known as the state-value function. It's a function that given a **fixed policy** $\pi$ , it computes the [[Expected Value|expected]] summed reward of starting in a state $s$ and following the policy.
$$

V^{\pi} ( s )=\mathbb{E} \left[ \sum_{t=0}^{\infty} \gamma^{t} R ( s_{t} , a_{t} ) | s_{0}=s , a_{t}=\pi( s_{t} ) \right]
$$
Notice a important property, that for a finite number of states this could also be defined as a [[Vector]] which maps the state to its expected summed reward. Like this:
$$
\vec{V}^\pi = \begin{pmatrix} v_1 \\ v_2 \\ v_3 \\ ... \end{pmatrix}
$$

# Q-value function
Also know as the action-value function. It's a function that given a **fixed policy** $\pi$, it computes the [[Expected Value|expected]] summed reward of starting in a state $s$ and taking the action $a$ and following the policy.

$$
Q^{\pi} ( s , a )=\mathbb{E} \left[ \sum_{t=0}^{\infty} \gamma^{t} R ( s_{t} \, , a_{t} ) | s_{0}=s , a_{0}=a , a_{t > 0}=\pi( s_{t} ) \right]
$$

Notice a important property, that for a finite number of states this could also be defined as a [[Matrix]],  where each column is a action and each state is a line. Like this:

$$
Q^\pi = \begin{pmatrix}
v_{11} & v_{12} & \ldots & v_{1m} \\
v_{21} & v_{22} & \ldots & v_{2m} \\
\ldots & \ldots & \ldots & \ldots \\
v_{n1} & v_{n2} & \ldots & v_{nm} 
\end{pmatrix}
$$

Also notice that you can extract the optimal policy for this Q matrix simply by taking the following operation:
$$
\pi(s) = argmax \;Q^\pi
$$

# Learning a MDP
There are 3 main types of things you can learn in a MDP

## Model Based
Basically the idea is to learn everything, from the model of the world, to the reward function and then you can use one of the [[Iteration Algorithms (Planning)]] to extract the policy. Its by far the most sample efficient.

## Value Based
You skip the model and the reward function and computes directly the [[Markov Decision Process (MDP)#Q-value function|Value Function]] directly and then extract the policy. Its not as sample efficient as the Model Based approaches, but its iteration efficient. Since it doesn't learn directly a model of the world, it's considered **Model Free**. 

## Policy Based
You skip the problem completely and the model you are learning is the policy. The great advantage of this is that you can have continuous outputs since you are not extracting a policy matrix, but its the least sample efficient, and the most unstable. Since it doesn't learn directly a model of the world, it's considered **Model Free**. 