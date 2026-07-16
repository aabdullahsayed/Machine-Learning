# 005 - Linear Algebra Essentials

## Concept
ML models are fundamentally linear algebra: data is a matrix, weights are vectors, and predictions come from matrix-vector products. This lesson covers vectors, matrices, dot products, matrix multiplication, and norms — the minimum toolkit needed to understand regression (module 04) and neural networks (module 10).

## Why It Matters
`y = Xw + b` (linear regression), attention scores in transformers (module 13), and convolution operations (module 11) are all matrix operations. Reading model math without linear algebra is like reading code without knowing variables.

## Hands-On

```python
import numpy as np

# 1. Vectors and dot product - the core operation behind every neuron
w = np.array([0.5, -0.2, 0.1])   # weights
x = np.array([2.0, 3.0, 1.0])    # features
dot_product = np.dot(w, x)        # equivalent to w @ x
print("Dot product:", dot_product)  # 0.5*2 + -0.2*3 + 0.1*1 = 0.5

# 2. Matrix-vector product - this IS linear regression's forward pass
X = np.array([
    [2.0, 3.0, 1.0],
    [1.0, 0.5, 4.0],
    [3.0, 2.0, 2.0]
])  # 3 samples, 3 features
w = np.array([0.5, -0.2, 0.1])
predictions = X @ w
print("Predictions:", predictions)

# 3. Matrix-matrix multiplication - used in neural network layers
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])
print(A @ B)

# 4. Transpose - reorients data, essential for shape-matching in NN layers
print(X.T)  # 3x3 -> transposed 3x3

# 5. Norms - measure vector "length", used in regularization (module 04)
v = np.array([3, 4])
l2_norm = np.linalg.norm(v)          # sqrt(3^2 + 4^2) = 5.0
l1_norm = np.linalg.norm(v, ord=1)   # |3| + |4| = 7
print("L2 norm:", l2_norm, "| L1 norm:", l1_norm)

# 6. Identity matrix and matrix inverse - used in the closed-form solution
# to linear regression: w = (X^T X)^-1 X^T y
X_square = np.array([[2.0, 1.0], [1.0, 3.0]])
X_inv = np.linalg.inv(X_square)
print("Inverse:\n", X_inv)
print("Check (should be identity):\n", np.round(X_square @ X_inv, 5))

# 7. Eigenvalues/eigenvectors - the math behind PCA (module 07)
cov_matrix = np.array([[4, 2], [2, 3]])
eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)
print("Eigenvalues:", eigenvalues)
print("Eigenvectors:\n", eigenvectors)
```

## Exercise
1. Given `X` (5 samples x 4 features) and `w` (length 4), manually compute predictions with `X @ w`, then verify against a loop-based dot-product implementation.
2. Compute the L2 norm of the weight vector `w = [0.5, -0.2, 0.1, 0.8]` — this is exactly what Ridge regression penalizes (module 04).
3. Use `np.linalg.eig` on a 3x3 covariance matrix and confirm the eigenvectors are orthogonal (`eig_vec1 @ eig_vec2 ≈ 0`).

## Key Takeaways
- `X @ w` is literally the forward pass of linear regression and the building block of every neural network layer.
- L1 vs L2 norms directly correspond to Lasso vs Ridge regularization.
- Eigen-decomposition of the covariance matrix is exactly how PCA finds its principal components.
