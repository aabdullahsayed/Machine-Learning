# Matrices

## Math Explanation

A **matrix** is a 2D grid of numbers — rows × columns.
```
      [1  2  3]
A =   [4  5  6]     (a 2×3 matrix: 2 rows, 3 columns)
```

### Key operations
- **Addition**: element-wise, same-shape matrices only.
- **Scalar multiplication**: multiply every element.
- **Matrix multiplication** `A @ B`: valid only if `A` is `(m×n)` and `B` is `(n×p)` → result is `(m×p)`. Each output element is a **dot product** of a row of A with a column of B.
- **Transpose** `Aᵀ`: flip rows and columns.
- **Identity matrix** `I`: diagonal of 1s, everything else 0 — `A @ I = A` (like multiplying by 1 in scalar algebra).
- **Inverse** `A⁻¹`: `A @ A⁻¹ = I` (like dividing — only exists for square, non-singular matrices).

### Worked example: matrix multiplication
```
A = [1 2]      B = [5 6]
    [3 4]          [7 8]

A @ B = [1*5+2*7   1*6+2*8]   = [19 22]
        [3*5+4*7   3*6+4*8]     [43 50]
```

## In ML/DL

- **A dataset is a matrix**: rows = samples, columns = features. Shape `(N, D)`.
- **A neural network layer is matrix multiplication**: `output = X @ W + b`, where `X` is your batch of inputs `(batch_size, input_dim)`, `W` is the weight matrix `(input_dim, output_dim)`.
```python
import numpy as np
X = np.random.randn(32, 784)   # batch of 32 images, 784 pixels each (flattened 28x28)
W = np.random.randn(784, 128)   # weight matrix: 784 inputs -> 128 hidden units
b = np.random.randn(128)
output = X @ W + b              # shape: (32, 128)
```
- **GPUs are built for matrix multiplication** — this exact operation (`X @ W`) is why training deep learning models needs GPUs: thousands of parallel multiply-accumulate operations.
- **Image data** is naturally a matrix (height × width, or a 3D tensor with color channels): `(H, W, C)`.
- **Convolution operations** (CNNs) are structured matrix multiplications (via `im2col` tricks) under the hood.
- **Attention mechanism (Transformers)**: `Attention(Q,K,V) = softmax(QKᵀ/√d) V` — pure matrix multiplication between Query, Key, Value matrices.
