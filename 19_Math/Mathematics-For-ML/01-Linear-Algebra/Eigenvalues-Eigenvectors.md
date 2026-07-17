# Eigenvalues & Eigenvectors

## Math Explanation

For a square matrix `A`, an **eigenvector** `v` is a vector whose direction doesn't change when `A` is applied to it — it only gets scaled by a factor `λ` (the **eigenvalue**):
```
A v = λ v
```
`A` stretches/shrinks `v` by `λ`, but doesn't rotate it off its own line.

### How to find them (conceptually)
Solve `det(A - λI) = 0` for `λ` (the "characteristic equation"), then for each `λ`, solve `(A - λI)v = 0` for `v`.

### Worked example
```
A = [2 0]
    [0 3]
```
This is diagonal, so eigenvalues are just the diagonal entries: `λ1 = 2` (eigenvector `[1,0]`), `λ2 = 3` (eigenvector `[0,1]`). Makes sense: `A` stretches the x-axis by 2 and the y-axis by 3.

### Eigendecomposition
Any diagonalizable matrix can be written as `A = V Λ V⁻¹`, where `V`'s columns are eigenvectors and `Λ` is a diagonal matrix of eigenvalues. This is a fundamental tool for understanding what a linear transformation "really does."

## In ML/DL

- **PCA (Principal Component Analysis)** is literally eigendecomposition of the data's covariance matrix — eigenvectors = principal components (directions of maximum variance), eigenvalues = how much variance each direction explains. See `07-ML-Applications/PCA.md`.
```python
import numpy as np
cov_matrix = np.cov(data.T)
eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)
# sort by eigenvalue descending -> top eigenvectors = principal components
```
- **Spectral clustering** uses eigenvectors of a graph's Laplacian matrix to find natural clusters.
- **PageRank** (Google's original algorithm) finds the dominant eigenvector of a web-link matrix.
- **Convergence of gradient descent** relates to the eigenvalues of the Hessian matrix — a poorly-conditioned Hessian (eigenvalues very different in magnitude) causes slow, zig-zagging convergence, which is exactly why techniques like Adam/momentum help (see `05-Optimization/SGD-Variants.md`).
- **Stability analysis of RNNs**: eigenvalues of the recurrent weight matrix determine whether gradients explode (`|λ| > 1`) or vanish (`|λ| < 1`) over many timesteps.
