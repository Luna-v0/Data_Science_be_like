To change between 'coordinate systems' is the same of changing from a matrix which represents the first coordinate system ($A$) and another matrix that represents the second coordinate systems ($B$). To turn a vector from the coordinate system $A \to B$ is:
$$
f(\vec{x}) = B^{-1}A\vec{x}
$$
Where $f$ is a function which has its underlying [[Matrix#Linear Transformation View|Linear Transformation]] as $B^{-1} \cdot A$

And if you want to turn from $B \to A$ you can use:

$$
g(\vec{x}) = A^{-1}B\vec{x}
$$

Notice that if you want to turn from the [[Base vectors]] to any matrix you would do:

$$
\begin{align}
h(\vec{x}) &= M^{-1}I\vec{x} 
\\ &= M^{-1}\vec{x}
\end{align}
$$

That totally makes sense since you could imagine that $\vec{x}$ is "[[Linear Systems#Definition|Encoded]]" in a specific [[Vector Spaces]]. Which also builds intuition for the fact that, to turn from the $I$ vector space to any vector space $M$, you would simply do $M \cdot x$.