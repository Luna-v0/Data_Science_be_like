# Linear combination
A linear combination is defined using a set of vectors and a 'vector of scalars' and applying this operation:

$$
sum_(i=1)^n alpha_i arrow(v)_i
$$
# Span
Is the set of all linear combinations of a given set of [[Vector|Vectors]].

# Linear Independence (LI)
Considering $V$ as a [[Vector Spaces|Vector Space]] and the set of vectors $arrow(v)_1 ...  arrow(v)_n$ we say there is linear independence if the their linear combination is equal to 0. Which implies that:

$$
alpha_1 = alpha_2 = ... = alpha_n = 0
$$

If any $alpha_i != 0$  the set is **Linear dependent (LD)**. But that can be divided into two cases:

$$
cases(alpha_i!=0 & quad"then" arrow(v)_i = 0, alpha_i!=0 and alpha_j !=0 and i !=j & quad "then" alpha_i arrow(v)_i = alpha_j arrow(v)_j)
$$

Therefore $arrow(v)_i$ can be expressed as a scalar multiplication of $arrow(v)_j$ and vice-versa.

# Base
A set of vectors ($beta$) is a base of a [[Vector Spaces|Vector Space]] $V$ if:

$$
(1) & quad "Span"(beta) = V
\
(2) & quad beta "is" "LI"
$$

A base change operation is 
# Dimension
A dimension of a Vector Space is defined as the number of vectors in a Base of a Vector space. That is highly related to [[Matrix#Rank]]