# Linear combination
A linear combination is defined using a set of vectors and a 'vector of scalars' and applying this operation:

$$
\sum_{i=1}^{n} \alpha_i \vec{v}_i
$$
# Span
Is the set of all linear combinations of a given set of [[Vector|Vectors]].

# Linear Independence (LI)
Considering $V$ as a [[Vector Spaces|Vector Space]] and the set of vectors $\vec{v}_1 \ldots \vec{v}_n$ we say there is linear independence if the their linear combination is equal to 0. Which implies that:

$$
\alpha_1 = \alpha_2 = \ldots = \alpha_n = 0
$$

If any $\alpha_i \neq 0$  the set is **Linear dependent (LD)**. But that can be divided into two cases:

$$
\begin{cases}
\alpha_i \neq 0 & \quad \text{then} \quad \vec{v}_i = 0 \\
\alpha_i \neq 0 \text{ and } \alpha_j \neq 0 \text{ and } i \neq j & \quad \text{then} \quad \alpha_i \vec{v}_i = \alpha_j \vec{v}_j
\end{cases}
$$

Therefore $\vec{v}_i$ can be expressed as a scalar multiplication of $\vec{v}_j$ and vice-versa.

# Base
A set of vectors ($beta$) is a base of a [[Vector Spaces|Vector Space]] $V$ if:

$$
\begin{aligned}
(1) \quad &\text{Span}(\beta) = V \\
(2) \quad &\beta \text{ is LI}
\end{aligned}
$$

A base change operation is 
# Dimension
A dimension of a Vector Space is defined as the number of vectors in a Base of a [[Vector Spaces]]. That is highly related to [[Matrix#Rank|Rank of Matrices]].