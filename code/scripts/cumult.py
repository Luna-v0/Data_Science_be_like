import cupy as cp
import numpy as np

# Example usage:
if __name__ == "__main__":
    # check if GPU is available
    # use two very large matrices for a 8GB GPU

    a = cp.random.rand(5000, 5000)
    b = cp.random.rand(5000, 5000)
    result = cp.matmul(a, b)