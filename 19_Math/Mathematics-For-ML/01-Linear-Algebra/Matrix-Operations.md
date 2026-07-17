# Matrix Operations Deep Dive

## Math Explanation

### Rank
The **rank** of a matrix is the number of linearly independent rows (or columns) — intuitively, how much "real" information the matrix contains, ignoring redundancy.

### Determinant
A scalar value computed from a square matrix, telling you:
- Whether the matrix is invertible (`det = 0` → NOT invertible, called "singular")
- How much the matrix scales area/volume when used as a linear transformation

For a 2×2 matrix: `det([a b; c d]) = ad - bc`

### Trace
Sum of the diagonal elements: `trace(A) = a11 + a22 + ... + ann`. Used in many ML formulas (e.g., some regularization terms, some loss function derivations).

### Orthogonal matrices
A matrix `Q` where `Qᵀ Q = I` (its transpose is its inverse). Rows/columns are unit vectors, mutually perpendicular. Represent pure **rotations/reflections** — they don't stretch or shrink space.

### Positive definite matrices
A symmetric matrix `A` is **positive definite** if `xᵀAx > 0` for all nonzero vectors `x`. Important because it guarantees a unique minimum in optimization (relevant to `05-Optimization/Convexity.md`).

## In ML/DL

- **Rank deficiency** in your feature matrix means redundant/correlated features — this is exactly why linear regression can become unstable with highly correlated features (multicollinearity).
- **Singular (non-invertible) matrices** show up when solving `w = (XᵀX)⁻¹Xᵀy` (the closed-form solution to linear regression, the "normal equation") — if `XᵀX` is singular, you need regularization (Ridge regression adds `λI` specifically to guarantee invertibility).
```python
import numpy as np
# Ridge regression normal equation
X = np.random.randn(100, 10)
y = np.random.randn(100)
lam = 0.1
w = np.linalg.inv(X.T @ X + lam * np.eye(10)) @ X.T @ y
```
- **The Hessian matrix** (second derivatives, see `02-Calculus/Jacobian-Hessian.md`) being positive definite at a point confirms you're at a true local minimum of your loss function, not a saddle point.
- **Orthogonal weight initialization** in deep networks helps preserve gradient magnitudes through many layers, reducing vanishing/exploding gradients.
