# Definition
Any function that follows this rules, $V$ is a [[Vector Spaces|Vector Space]]:

$$
\begin{gather*}
\text{Given a function } f \quad V \times V \to \mathbb{R} \\ \\
\forall x,y,z \in V \quad \land \quad \alpha \in \mathbb{R} 
\end{gather*}
$$

$$
\begin{aligned}
(1) \quad & f(x + \alpha y, z) = f(x,z) + \alpha f(x,y) \\ \\
(2) \quad & f(x, y + \alpha z) = f(x,y) + \alpha f(x,z) \\ \\
(3) \quad & f(x,y) = f(y,x) \\ \\
(4) \quad & f(x,x) > 0 \quad \text{if } x \neq 0
\end{aligned}
$$

Definitions, 1 and 2, are based on [[Linearity|Linear functions]].

# Cauchy-Schwarz
Any internal product $f$ should follow:

$$
\forall u,v \in V \to |f(u,v)|² \leq f(u,v)f(u,v)
$$
