It is a metric to compute the ideal sample size with a margin of error $e$ and a confidence interval $z$ where $z$ is the [[Z-Score]].

## For unknown population size

$$
n_0 = \frac{z^2 \cdot p \ \cdot (1- p)}{e^2}
$$

## For known population size (N)

$$
n = \frac{n_0}{1+\frac{n_0-1}{N}}
$$

# A simpler estimation 

$$
n = \frac{N}{1+ N \cdot e^2}
$$
