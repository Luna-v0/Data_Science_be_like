import cupy as cp

def matrix_multiplication_chunked(a, b, chunk_size):
    # Convert input matrices to Cupy arrays
    #a_cupy = cp.array(a)
    #b_cupy = cp.array(b)
    a_cupy = a
    b_cupy = b

    # Determine the shape of the matrices
    m, n, p = a_cupy.shape[0], a_cupy.shape[1], b_cupy.shape[1]

    # Initialize the result matrix with zeros
    result_cupy = cp.zeros((m, p), dtype=cp.float32)

    # Perform matrix multiplication using chunking
    for i in range(0, m, chunk_size):
        for j in range(0, p, chunk_size):
            for k in range(0, n, chunk_size):
                a_chunk = a_cupy[i:i+chunk_size, k:k+chunk_size]
                b_chunk = b_cupy[k:k+chunk_size, j:j+chunk_size]
                result_chunk = cp.matmul(a_chunk, b_chunk)
                result_cupy[i:i+chunk_size, j:j+chunk_size] += result_chunk

    return result_cupy

# Example usage:
if __name__ == "__main__":
    a = cp.random.randn(10000, 10000).astype(cp.float32)
    b = cp.random.randn(10000, 10000).astype(cp.float32)
    chunk_size = 5000  # Adjust the chunk size as needed based on available GPU memory
    for i in range(1000):
        result = matrix_multiplication_chunked(a, b, chunk_size)