# Square matrix
Is a [[Matrix]] with the same size of lines and columns. I will use $M(n)$ to define a square matrix of size $n$

# Diagonal Matrix
Is a [[Types of Matrices#Square matrix|square matrix]] with $\vec{v}_i$:

$$
\begin{cases}
x_{ij} = \vec{v}_i & \text{if} & i = j \\
x_{ij} = 0 & \text{if} & i \neq j
\end{cases}
$$

> [!tip] All [[Base vectors#Identity Matrix|Identity Matrices]] are Diagonal Matrices
# Triangular Matrix
There is two types of triangular matrices, [[Types of Matrices#Diagonal Matrix|Diagonal Matrices]] are both types of Triangular Matrices. Triangular Matrices are always [[Types of Matrices#Square matrix|square matrices]].

I'm using $\alpha$ as any number
## Upper 
$$
\begin{cases}
x_{ij} = \alpha & \text{if} & j \geq i \\
x_{ij} = 0 & \text{if} & j < i
\end{cases}
$$
## Lower
$$
\begin{cases}
x_{ij} = \alpha & \text{if} & i \geq j \\
x_{ij} = 0 & \text{if} & i < j
\end{cases}
$$

# Echelon Row Matrix
What is important is that is not limited to [[Types of Matrices#Square matrix|square matrices]]

$$
x_{ij} = 0 \quad \text{if} \quad j < i 
$$

# Inverse Matrix
An inverse matrix $W$ is a matrix such:
$$
W \cdot M = I
$$

Often written as $M^(-1)$
# Orthogonal Matrix

# Orthonormal Matrix