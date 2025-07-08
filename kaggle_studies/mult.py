
import numpy as np



# Example usage:
if __name__ == "__main__":
    a = np.random.rand(5000, 5000)
    b = np.random.rand(5000, 5000)
    for i in range(1000):
        result = np.matmul(a, b)