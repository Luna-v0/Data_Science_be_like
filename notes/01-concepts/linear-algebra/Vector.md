---
type: concept
topic: {{topic}}
difficulty: beginner/intermediate/advanced
related_concepts: []
related_code: []
tags: []
created: {{date}}
---
# Definition
Is defined as a ordered list of numbers or an array. Geometrically can be interpreted as an arrow in space that has magnitude, direction and orientation.

# Mathematical Formulation
Normally expressed as $arrow(x)$ or as tuples like:


$$
vec(x_1,x_2,x_3)
$$

They also have a Dimension also known as size in the above example its of size 3
# Properties
The [[Vector#Sum]] and the [[Vector#Scalar Multiplication]] are part of the [[Linearity]]

## Sum
Sum is only defined for vectors of the same size

$$arrow(x)+arrow(y) = vec(x_1+y_1, x_2 + y_2,\ ,...,\ ,x_n+y_n)$$
## Scalar Multiplication

$$alpha. arrow(x) = vec(alpha x_1,alpha x_2,\ , ...,\ ,alpha x_n)$$

## Inner product
Is any operation that takes two vectors of the same size and returns a single scalar the most famous being the dot product
### Dot product
Notice that operation is highly scalable in GPU level. That operation also is also used for comparing two vectors and returning the distance of them ($theta$ being the angle between the two arrows in space)

$$
arrow(x) dot arrow(y) = sum_(i=1)^n x_i y_i
\ \ \
arrow(x) dot arrow(y) = ||arrow(x)|| ||arrow(y)|| cos(theta) 
$$

## Magnitude
The magnitude can be expressed as simple Pythagoras theorem like:

$$||arrow(x)|| = sqrt(arrow(x) dot arrow(x)) $$




## Implementation Notes
[[code/notebooks/ja]]

## References
- Source 1
- Source 2
