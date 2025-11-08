---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.17.2
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

# Jax basics

This is a specific notebook for me to learn [JAX](https://docs.jax.dev/en/latest/notebooks/thinking_in_jax.html)

```python
import jax.numpy as jnp
import matplotlib.pyplot as plt
import numpy as np
```

```python
from jax import make_jaxpr, jit, grad, jacobian, jacfwd, jacrev, hessian, random

from functools import partial
```

Jax cannot set items from array directly, must use `at[num].set`

```python
# In numpy
x = np.arange(10)
x[0] = 10
x
```

```python
# In Jax
y = jnp.arange(10)
y.at[0].set(10)
```

```python
y.devices(), y.sharding
```

Jax performance against numpy

```python
def norm(X):
    X = X - X.mean(0)
    return X / X.std(0)

acc_norm = jit(norm)
np.random.seed(42)

X = jnp.array(np.random.rand(10000,10))
```

```python
%%time
res_np = norm(X)
```

```python
%%time 
res_jax = acc_norm(X)
```

```python
np.allclose(res_np,res_jax,atol=1E-6)
```

```python
%timeit norm(X).block_until_ready()
%timeit acc_norm(X).block_until_ready()
```

First time the function is called it trigger the compilation of the function, and it only compiles JAX code, so prints are not compiled to JAX and therefore not showned the second time the function runs. `make_jaxpr` shows the underlying code of the function

Note that you cannot create conditional functions or with changing size. Only using partial you can make it, but results on re-compilation.

```python
@jit
def f(x, y):
  print("Running f():")
  print(f"  {x = }")
  print(f"  {y = }")
  result = jnp.dot(x + 1, y + 1)
  print(f"  {result = }")
  return result

x = np.random.randn(3, 4)
y = np.random.randn(4)
f(x, y)
```

```python
x2 = np.random.randn(3, 4)
y2 = np.random.randn(4)
f(x2, y2)
```

```python
make_jaxpr(f)(x,y)
```

```python
@partial(jit, static_argnums=(1,))
def f(x, neg):
  return -x if neg else x

f(1, True)
```

# Jax auto gradient

```python
def sum_logistic(x):
  return jnp.sum(1.0 / (1.0 + jnp.exp(-x)))

x_small = jnp.arange(3.)
derivative_fn = grad(sum_logistic)
print(derivative_fn(x_small))
```

You can mix and match `grad` with `jit`, the `grad` works similarly to [autograd](https://github.com/HIPS/autograd)

```python
print(grad(jit(grad(jit(grad(sum_logistic)))))(1.0))
```

Jax has multiple variation of the jacobian, like `jacobian`, `jacrev`, `jacfwd`, etc. You can also use the `hessian`

```python
jacobian(jnp.exp)(x_small)
```

```python
def hessian_m(fun):
    return jit(jacfwd(jacrev(fun)))

np.allclose(hessian_m(sum_logistic)(x_small),hessian(sum_logistic)(x_small), atol=1E-6)
```

Just like 

```python
key = random.key(1701)
key1, key2 = random.split(key)
mat = random.normal(key1, (150,100))
batched_x = random.normal(key2, (10,100))

def apply_matrix(x):
    return jnp.dot(mat,x)
```

```python
def v1_batch_apply(v_batched):
    return jnp.stack([[apply_matrix(v) for v in v_batched]])

def v2_batch_apply(v_batched):
    return 

```
