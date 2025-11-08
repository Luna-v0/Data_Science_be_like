# Definition
A base vector is defined as a vector that follows a axis expressed as 1. Some examples are:
Base vectors are always [[Linear definitions#Linear Dependency|Linear Independent]] in relation to each other.

$$
\hat{i} = \begin{pmatrix} 1 \\ 0 \\ 0 \\ 0 \end{pmatrix} \quad \hat{j} = \begin{pmatrix} 0 \\ 1 \\ 0 \\ 0 \end{pmatrix} \quad \hat{k} = \begin{pmatrix} 0 \\ 0 \\ 1 \\ 0 \end{pmatrix} \quad \hat{w} = \begin{pmatrix} 0 \\ 0 \\ 0 \\ 1 \end{pmatrix}
$$

# Identity Matrix
A identity matrix is a squared matrix that has each column (or row) as the column number base vector like this:

$$
I(4) = M(4,4) = \begin{pmatrix} \hat{i} & \hat{j} & \hat{k} & \hat{w} \end{pmatrix}
$$

The Identity matrix has a special property of [[Matrix#Matrix multiplication|Matrix Multiplication]] and [[Types of Matrices#Inverse Matrix|Inverse Matrices]] that are:


$$
M(n,n)^{-1} \cdot M(n,n) = I(n) \\
M(n,n) \cdot I(n) = M(n,n)
$$