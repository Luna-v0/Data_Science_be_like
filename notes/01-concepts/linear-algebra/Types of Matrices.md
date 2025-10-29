# Square matrix
Is a [[Matrix]] with the same size of lines and columns. I will use $M(n)$ to define a square matrix of size $n$

# Diagonal Matrix
Is a [[Types of Matrices#Square matrix|square matrix]] with $arrow(v)_i$:

$$
cases(x_(i j) = arrow(v)_i && "if" && i = j, x_(i j) = 0 && "if" && i!= j)
$$

> [!tip] All [[Base vectors#Identity Matrix|Identity Matrices]] are Diagonal Matrices
# Triangular Matrix
There is two types of triangular matrices, [[Types of Matrices#Diagonal Matrix|Diagonal Matrices]] are both types of Triangular Matrices. Triangular Matrices are always [[Types of Matrices#Square matrix|square matrices]].

I'm using $alpha$ as any number
## Upper 
$$
cases(x_(i j) = alpha && "if" && j >= i, x_(i j) = 0 && "if" &&j<i)
$$
## Lower
$$
cases(x_(i j) = alpha && "if" && i >= j, x_(i j) = 0 && "if" && i<j)
$$

# Echelon Row Matrix
What is important is that is not limited to [[Types of Matrices#Square matrix|square matrices]]

$$
x_(i j) = 0 "if" j < i 
$$

# Inverse Matrix
An inverse matrix $W$ is a matrix such:
$$
W dot M = I
$$

Often written as $M^(-1)$
