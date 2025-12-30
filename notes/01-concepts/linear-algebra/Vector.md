Is defined as a ordered list of numbers or an array. Geometrically can be interpreted as an arrow in space that has magnitude, direction and orientation.

# Mathematical Formulation
Normally expressed as $\vec{x}$ or as tuples like:

$$
\vec{x} = \begin{pmatrix} x_1 \\ x_2 \\ x_3 \end{pmatrix}
$$

They also have a Dimension also known as size in the above example its of size 3
# Properties
The [[Vector#Sum]] and the [[Vector#Scalar Multiplication]] are part of the [[Linearity]]

## Sum
Sum is only defined for vectors of the same size

$$\vec{x}+\vec{y} = \begin{pmatrix} x_1+y_1 \\ x_2 + y_2 \\ \ldots \\ x_n+y_n \end{pmatrix}$$
## Scalar Multiplication

$$\alpha \cdot \vec{x} = \begin{pmatrix} \alpha x_1 \\ \alpha x_2 \\ \ldots \\ \alpha x_n \end{pmatrix}$$

## Inner product
Is any operation that takes two vectors of the same size and returns a single scalar the most famous being the dot product
### Dot product
That operation also is also used for comparing two vectors and returning the distance of them ($\theta$ being the angle between the two arrows in space)

$$
\begin{gather*}
\vec{x} \cdot \vec{y} = \sum_{i=1}^{n} x_i y_i \\ \\
\vec{x} \cdot \vec{y} = \|\vec{x}\| \|\vec{y}\| \cos(\theta) 
\end{gather*}
$$

Using dot product you can compare two distinct vectors, this is often used in [[Embeddings]] to compare two vectors.

> [!tip] Notice this is highly optimizable using GPU
> There for any weighted sum can be scaled by libs like [[jax]]

## Magnitude
The magnitude can be expressed as simple Pythagoras theorem like:

$$\|\vec{x}\| = \sqrt{\vec{x} \cdot \vec{x}} $$

It is also the [[Nomal|Norm]] and a [[Internal Product]].
## Cross Product
The cross product of two vectors is a new vector orthogonal to all the other vectors, you compute it using the [[Matrix#Determinant]] and the [[Base vectors]]

$$
\vec{a} \times \vec{b} = \det\begin{pmatrix} \hat{i} & \hat{j} & \hat{k} \\ a_1 & a_2 & a_3 \\ b_1 & b_2 & b_3 \end{pmatrix}  
$$

When doing it on more dimensions you must do:

$$
\vec{a} \times \vec{b} \times \vec{c} = \det\begin{pmatrix} \hat{i} & \hat{j} & \hat{k} & \hat{w} \\ a_1 & a_2 & a_3 & a_4 \\ b_1 & b_2 & b_3 & b_4 \\ c_1 & c_2 & c_3 & c_4 \end{pmatrix}  
$$

# Code reference

1. [[jax]] 