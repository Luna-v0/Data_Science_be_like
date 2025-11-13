A projection of  $\vec{v}$ in the $\vec{u}$ is defined as 

$$\cal P_{\vec{u}} (\vec{v}) = \frac{\vec{v} \cdot \vec{u}}{\|\vec{u}\|} \vec{u}$$
Is it important to note that:

$$
\cal P_{\vec{u}} (P_{\vec{u}}(\vec{v})) = P_{\vec{u}}(\vec{v})
$$

## Orthogonal Projection
It is a projection that minimises the distance between the point of the vector and the projected [[Vector Spaces|Hyperplane]]. Given the subspace [[Linear definitions|spanned]] by a [[Matrix]] composed of [[Orthonormal and Orthogonal#Orthonormal Base|Orthonormal Vectors]] $Q = \begin{pmatrix} \vec{q}_1 & \vec{q}_2 & \ldots & \vec{q}_n \end{pmatrix}$

$$
\mathcal{P(\vec{v})} = Q \cdot Q^T \cdot \vec{v}
$$
If the subspace is defined as non-orthonormal vectors, (but defined as Matrix $A$) then:

$$
\mathcal{P(\vec{v})} = A \cdot (A^T \cdot A)^{-1} \cdot A^T \cdot \vec{v}
$$