# Principal Component Analysis (PCA)

## Math Explanation

**PCA** is a dimensionality reduction technique that finds new axes (directions) along which the data varies the most, and re-expresses the data using only the top few of these directions — capturing most of the information (variance) with far fewer dimensions.

### The full derivation, tying together earlier chapters
1. **Center the data**: subtract the mean from every feature (`04-Statistics/Descriptive-Stats.md`).
2. **Compute the covariance matrix** of the centered data (`03-Probability/Expectation-Variance.md`):
```
Σ = (1/n) XᵀX     (X is the centered data matrix)
```
3. **Find the eigenvectors and eigenvalues of Σ** (`01-Linear-Algebra/Eigenvalues-Eigenvectors.md`):
```
Σ v = λ v
```
Each eigenvector `v` is a **principal component** — a direction in feature space. Its corresponding eigenvalue `λ` tells you how much variance the data has along that direction.
4. **Sort eigenvectors by eigenvalue, descending.** The top eigenvector is the direction of maximum variance in the data; the second (orthogonal to the first) captures the next-most variance, and so on.
5. **Project the data onto the top `k` eigenvectors** to get a `k`-dimensional representation that preserves as much of the original variance as possible for that number of dimensions.

### Why this is the "best possible" linear dimensionality reduction
It can be proven (via the Eckart-Young theorem, connected to `01-Linear-Algebra/SVD.md`) that projecting onto the top-`k` principal components gives the best possible rank-`k` approximation of the data, in terms of minimizing reconstruction error — no other linear projection to `k` dimensions preserves more of the original data's variance/structure.

## In ML/DL

### From-scratch implementation
```python
import numpy as np

def pca(X, k):
    X_centered = X - X.mean(axis=0)               # step 1
    cov_matrix = np.cov(X_centered.T)                # step 2
    eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)  # step 3
    idx = np.argsort(eigenvalues)[::-1]                 # step 4: sort descending
    top_k_vectors = eigenvectors[:, idx[:k]]
    return X_centered @ top_k_vectors                     # step 5: project

# vs. the library version:
from sklearn.decomposition import PCA
reduced = PCA(n_components=2).fit_transform(X)
```

### Real-world uses
- **Visualization**: reduce high-dimensional data (e.g., 50-dimensional embeddings) down to 2D/3D for plotting and human inspection.
- **Preprocessing**: reduce feature count before feeding into a downstream model, speeding up training and sometimes reducing overfitting (fewer, less-correlated input dimensions).
- **Noise reduction**: dropping low-variance components can remove noise while preserving the meaningful structure/signal in the data.
- **Compression**: PCA is directly used in some image/data compression pipelines (keep top-k components, discard the rest, reconstruct approximately).
- **Explained variance ratio** (`eigenvalue_i / Σ all eigenvalues`) tells you exactly how much information you're keeping vs discarding when you choose a value of `k` — a direct, quantitative way to choose how aggressively to reduce dimensions.

### Relationship to autoencoders
A linear autoencoder (encoder and decoder are both simple linear layers, trained to reconstruct its own input) with a bottleneck layer of size `k` learns, remarkably, a representation that spans the exact same subspace as PCA's top-`k` components — a deep learning model can be shown to converge to the classical linear-algebra solution in this special case, a nice concrete link between "classical ML math" and "deep learning."
