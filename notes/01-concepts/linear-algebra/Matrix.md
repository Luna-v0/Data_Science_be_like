# Definition
A matrix can be defined as a list/array of [[Vector]], there is two main views for that, as seeing them as vectors as lines or vectors as columns

Matrix are also [[Linearity|Linear]] Functions, that map from a [[Vector Spaces#Vector Subspace|Subspace]] to another Subspace. 
# Intuition
You can reduce [[Linearity|Linear]] operations as a single big Matrix using the [[Linearity#Linear composition|Linear Composition]].

# Mathematical Formulation
A matrix has two dimension, $i$ and $j$, where lines are $i$. 

$$
M(n,m) = \begin{pmatrix}
x_{11} & x_{12} & \ldots & x_{1m} \\
x_{21} & x_{22} & \ldots & x_{2m} \\
\ldots & \ldots & \ldots & \ldots \\
x_{n1} & x_{n2} & \ldots & x_{nm} 
\end{pmatrix}
$$

or as
$$
\begin{align*}
& M(n,m) = \begin{pmatrix} \vec{x}_1 & \vec{x}_2 & \ldots & \vec{x}_n \end{pmatrix} \\ \\
& M(n,m) = \begin{pmatrix} \vec{y}_1 \\ \vec{y}_2 \\ \ldots \\ \vec{y}_n \end{pmatrix}
\end{align*}
$$

where $\vec{x}_i$ are column vectors and $\vec{y}_i$ are line vectors.

## Linear Transformation View
Applying the matrix $M(n,m)$ using a [[Matrix#Matrix multiplication|Matrix Multiplication]] is equivalent to view it as applying a function with $n$ inputs and returning $m$ inputs, that's an intuition why the second term of the input must be of size $n$ when applied to this Transformation $M$.

# Properties
Notice that almost all the properties of matrices are derived from [[Vector|Vectors]]
## Sum
Can only be done using matrix of the same dimensions

$$
A(n,m) + B(n,m) = \begin{pmatrix} \vec{a}_1 + \vec{b}_1 & \vec{a}_2 + \vec{b}_2 & \ldots & \vec{a}_m + \vec{b}_m \end{pmatrix}
$$

## Multiply by scalar

$$
\alpha A(n,m) = \begin{pmatrix} \alpha \vec{a}_1 & \alpha \vec{a}_2 & \ldots & \alpha \vec{a}_m \end{pmatrix}
$$

## Matrix multiplication
For the matrix multiplication of $A(x,n) \cdot B(n,y) = C(x,y)$ each cell of the matrix is defined as:

$$
c_{ij} = \vec{a}_i \cdot \vec{b}_j
$$

Where $\vec{a}_i$ is defined as the line vector of index $i$ and $\vec{b}_j$ is defined as the column vector of index $j$

It can also be computed as:
$$
A \cdot B = \sum_{k=1}^{n} a_k \cdot b_k^T
$$
## Determinant
The determinant is a [[Linearity#Bi-linearity or N-linearity|N-linearity Function]] on each column.

To compute using column vectors use:
$$
det(A) = \sum_{k=1}^n(-1)^{k+j}a_{kj} \;det(A_{k,j})
$$
To compute using row vectors use:
$$
det(A) = \sum_{k=1}^n(-1)^{k+j}a_{jk} \;det(A_{j,k})
$$
It has two important Geometric reasoning. 
1. $|det(A)|$ computes the area (for $\mathbb{R}²$) or the volume (for $\mathbb{R}³$) of the square/cube created by the vectors. It is related to [[Integral|Integrals]] in that sense.
2. $sign(det(A))$ Computes the orientation of the underlying points of the vectors.

## Transposing
A matrix ( $B(m,n)$ ) is transposed from another matrix ( $A(n,m)$ ) if $b_{ij} = a_{ji}$. Normally written as:

$$
A^T = B
$$
It has a few properties:
$$
\begin{gather*}
& (A^T)^T = A \\ \\
& (A+C)^T = A^T + C^T \\ \\
& (A \cdot C)^T = C^T \cdot A^T
\end{gather*}

$$

# Rank
The Rank of a matrix is the number of columns that are [[Linear definitions#Linear Independence (LI)|LI]].