# Singular Value Decomposition (SVD)

## Math Explanation

SVD generalizes eigendecomposition to **any** matrix (not just square ones). Any matrix `A` (shape `m×n`) can be decomposed as:
```
A = U Σ Vᵀ
```
- `U` (`m×m`): orthogonal matrix — left singular vectors
- `Σ` (`m×n`): diagonal matrix of **singular values** (always ≥ 0, sorted largest to smallest)
- `Vᵀ` (`n×n`): orthogonal matrix — right singular vectors

### Intuition
SVD tells you: any linear transformation can be broken into a **rotation** (`Vᵀ`), a **scaling** along orthogonal axes (`Σ`), and another **rotation** (`U`). It's the most numerically stable and general way to understand a matrix's structure.

### Low-rank approximation
Keeping only the top `k` singular values/vectors gives the **best possible rank-k approximation** of `A` (in terms of minimizing reconstruction error) — this is the mathematical foundation of compression and dimensionality reduction.

## In ML/DL

- **PCA can be computed via SVD** directly on the data matrix (more numerically stable than eigendecomposition of the covariance matrix):
```python
import numpy as np
U, S, Vt = np.linalg.svd(data_centered, full_matrices=False)
principal_components = Vt[:k]   # top k directions of variance
```
- **Recommender systems** (collaborative filtering): decompose a sparse user-item rating matrix via SVD to find latent factors (this was the core idea behind the Netflix Prize-winning approaches).
- **Image compression**: keeping only the top-k singular values of an image matrix approximates the image with far less data.
- **LoRA (Low-Rank Adaptation)** for fine-tuning large language models is directly built on the idea that weight updates can be well-approximated by a low-rank (few singular values) matrix — dramatically reducing the number of trainable parameters.
- **Pseudo-inverse** (`np.linalg.pinv`), used to solve least-squares problems even when a matrix isn't invertible, is computed via SVD internally.
