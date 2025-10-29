# Definition
A matrix can be defined as a list/array of [[Vector]], there is two main views for that, as seeing them as vectors as lines or vectors as columns

Matrix are also [[Linearity|Linear]] Functions
# Intuition
You can reduce [[Linearity|Linear]] operations as a single big Matrix using the [[Linearity#Linear composition|Linear Composition]].

# Mathematical Formulation
A matrix has two dimension, $i & j$, where lines are $i$. 

$$
M(n,m) = mat(
x_11, x_12, ... , x_(1m);
x_21, x_22, ... , x_(2m);
..., , ...;
x_(n 1), x_(n 2), ... , x_(n m) 
)
$$

or as
$$
M(n,m) = mat(arrow(x_1), arrow(x_2), ... , arrow(x)_n)
\
\
M(n,m) = vec(arrow(y_1), arrow(y_2), ... , arrow(y)_n)

$$

where $arrow(x_i)$ are column vectors and $arrow(y_i)$ are line vectors.

# Properties
Notice that almost all the properties of matrices are derived from [[Vector|Vectors]]
## Sum
Can only be done using matrix of the same dimensions

$$
A(n,m) + B(n,m) = mat(arrow(a_1) + arrow(b_1), arrow(a_2) + arrow(b_2), ..., arrow(a)_m + arrow(b)_m )
$$

## Multiply by scalar

$$
alpha A(n,m) = mat(alpha arrow(a_1), alpha arrow(a_2), ..., alpha arrow(a)_m )
$$

## Matrix multiplication
For the matrix multiplication of $A(x,n) dot B(n,y) = C(x,y)$ each cell of the matrix is defined as:

$$
c_(i j) = arrow(a)_i dot arrow(b)_j
$$

Where $arrow(a)_i$ is defined as the line vector of index $i$ and $arrow(b)_j$ is defined as the column vector of index $j$

It can also be computed as:
$$
A dot B = sum_(k=1)^n a_k dot b_k^T
$$
## Determinant
The determinant is a [[Linearity#Bi-linearity or N-linearity|N-linearity Function]] on each 

## Transposing
A matrix ( $B(m,n)$ ) is transposed from another matrix ( $A(n,m)$ ) if $b_(i j) = a_(j i)$. Normally written as:

$$
A^T = B
$$
It has a few properties:
$$
(A^T)^T = A
\
(A+C)^T = A^T + C^T
\
(A dot C)^T = C^T dot A^T
$$

# Rank
The Rank of a matrix is the number of columns that are [[Linear definitions#Linear Independence (LI)|LI]].