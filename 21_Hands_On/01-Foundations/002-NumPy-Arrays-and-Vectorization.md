# 002 - NumPy Arrays and Vectorization

## Concept
NumPy's `ndarray` is a fixed-type, contiguous block of memory that supports vectorized (element-wise, loop-free) operations. Vectorization is the single biggest speed and readability upgrade you'll make going from plain Python to ML code.

## Why It Matters
Every ML library (Pandas, scikit-learn, PyTorch, TensorFlow) is built on array semantics inherited from NumPy. Thinking in arrays instead of loops is a prerequisite for reading model internals like gradient descent (module 03) and backpropagation (module 10).

## Hands-On

```python
import numpy as np

# 1. Creating arrays
a = np.array([1, 2, 3, 4, 5])
zeros = np.zeros((3, 4))
ones = np.ones((2, 2))
rand = np.random.randn(3, 3)   # standard normal samples
identity = np.eye(3)

# 2. Vectorized arithmetic - no Python for-loops needed
x = np.array([1, 2, 3])
y = np.array([10, 20, 30])
print(x + y)      # [11 22 33]
print(x * y)      # [10 40 90]
print(x ** 2)     # [1 4 9]

# 3. Broadcasting - operate on arrays of different shapes
matrix = np.array([[1, 2, 3], [4, 5, 6]])
row_vector = np.array([10, 20, 30])
print(matrix + row_vector)
# [[11 22 33]
#  [14 25 36]]

# 4. Indexing and boolean masks (used constantly for filtering datasets)
data = np.array([5, -3, 8, -1, 0, 12])
positive_only = data[data > 0]
print(positive_only)  # [5 8 12]

# 5. Aggregations along axes
matrix = np.array([[1, 2, 3], [4, 5, 6]])
print(matrix.sum(axis=0))   # column sums -> [5 7 9]
print(matrix.mean(axis=1))  # row means   -> [2. 5.]

# 6. Speed comparison: loop vs vectorized
import time
big = np.random.randn(1_000_000)

start = time.time()
total = 0
for v in big:
    total += v ** 2
loop_time = time.time() - start

start = time.time()
total_vec = np.sum(big ** 2)
vec_time = time.time() - start

print(f"Loop: {loop_time:.4f}s, Vectorized: {vec_time:.4f}s")
```

## Exercise
1. Create a 5x5 matrix of random integers between 0 and 100. Replace every value greater than 50 with 0 using a boolean mask (no loops).
2. Given `weights = np.array([0.2, 0.5, 0.3])` and `features = np.array([[1,2,3],[4,5,6]])`, compute the weighted sum per row using broadcasting and `@` (matrix multiply).
3. Time a manual Python loop that normalizes a 100,000-element array `(x - mean) / std` against the vectorized NumPy version.

## Key Takeaways
- Vectorized operations are typically 10-100x faster than pure Python loops.
- Broadcasting lets you combine arrays of different shapes without manual reshaping in most cases.
- Boolean masking is the idiomatic way to filter arrays — you'll use this pattern in outlier detection (module 02).
