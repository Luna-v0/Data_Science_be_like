# Kernel
Given a [[Matrix#Linear Transformation View|Linear Transformation]] ($Phi$), the set of input values ($V$) that the transformation maps to the zero [[Vector]] in the output ($W$) is the Kernel (or the null space). Mathematically expressed as:

$$
\begin{gather*}
 \Phi: V \to W \\

\text{Kernel}(\Phi) = \{v \in V \text{ then } \Phi(v) = \vec{0}\}
\end{gather*}


$$

> [!error] This is not the same Kernel as the [[Support Vector Machine|SVM]]
# Image
Is the same definition of functions, for the definition above the Image is all the outputs of the transformation $Phi$. The image of a transformation is also a [[Linear definitions#Span|Span]] of the underlying [[Matrix]] transformation.

> [!note] The Kernel and Image of $V$ and $W$ are [[Vector Spaces#Vector Subspace|Subspace]] of $V$ and $W$
# Kernel & Image Theorem

$$
\begin{gather*}
\Phi: V \to W \\ \\
\dim(V) = \dim(\text{Kernel}(\Phi)) + \dim(\text{Image}(\Phi))
\end{gather*}


$$

The definition of $\dim$ can be found in [[Linear definitions#Dimension]].