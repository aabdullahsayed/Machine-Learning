# 004 - Dimensionality Reduction: PCA

## Concept
Principal Component Analysis (PCA) transforms correlated features into a smaller set of uncorrelated "principal components" that capture the maximum variance in the data. It's an unsupervised technique — it doesn't look at the target at all. It builds directly on the eigenvector/eigenvalue math from module 01, file 005.

## Why It Matters
PCA reduces dimensionality for visualization (compressing to 2D/3D), speeds up downstream models, and can reduce noise/multicollinearity — while feature selection (file 003) keeps original features, PCA creates entirely new ones.

## Hands-On

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# 1. Load a high-dimensional dataset (8x8 pixel handwritten digits = 64 features)
digits = load_digits()
X, y = digits.data, digits.target
print("Original shape:", X.shape)

# 2. ALWAYS scale before PCA - it's sensitive to feature variance scale
# (a feature with a huge range would dominate the "variance" PCA chases)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 3. Fit PCA and inspect explained variance
pca_full = PCA()
pca_full.fit(X_scaled)
explained_var = pca_full.explained_variance_ratio_
cumulative_var = np.cumsum(explained_var)

plt.figure(figsize=(7, 5))
plt.plot(cumulative_var, marker=".")
plt.axhline(0.95, color="red", linestyle="--", label="95% variance threshold")
plt.xlabel("Number of components")
plt.ylabel("Cumulative explained variance")
plt.title("PCA - Explained Variance vs Number of Components")
plt.legend()
plt.savefig("pca_explained_variance.png")
plt.close()

n_components_95 = np.argmax(cumulative_var >= 0.95) + 1
print(f"\nComponents needed for 95% variance: {n_components_95} (down from {X.shape[1]})")

# 4. Reduce to 2 components for visualization
pca_2d = PCA(n_components=2)
X_pca_2d = pca_2d.fit_transform(X_scaled)

plt.figure(figsize=(8, 6))
scatter = plt.scatter(X_pca_2d[:, 0], X_pca_2d[:, 1], c=y, cmap="tab10", alpha=0.6)
plt.colorbar(scatter, label="Digit")
plt.xlabel(f"PC1 ({pca_2d.explained_variance_ratio_[0]*100:.1f}% variance)")
plt.ylabel(f"PC2 ({pca_2d.explained_variance_ratio_[1]*100:.1f}% variance)")
plt.title("Digits Dataset Compressed to 2D via PCA")
plt.savefig("pca_2d_visualization.png")
plt.close()
print("Even just 2 components show visible clustering by digit class "
      "(despite PCA never seeing the labels!).")

# 5. Does reducing dimensions hurt downstream model performance?
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)

for n_comp in [None, 30, 10, 2]:
    if n_comp is None:
        X_tr, X_te = X_train, X_test
        label = "No PCA (64 features)"
    else:
        pca = PCA(n_components=n_comp)
        X_tr = pca.fit_transform(X_train)
        X_te = pca.transform(X_test)  # transform only, never re-fit on test!
        label = f"PCA n_components={n_comp}"
    model = LogisticRegression(max_iter=2000).fit(X_tr, y_train)
    acc = model.score(X_te, y_test)
    print(f"{label:25s} -> Test accuracy: {acc:.4f}")

# 6. Reconstruction - PCA is lossy compression; show reconstruction error
pca_reconstruct = PCA(n_components=10)
X_reduced = pca_reconstruct.fit_transform(X_scaled)
X_reconstructed = pca_reconstruct.inverse_transform(X_reduced)
reconstruction_error = np.mean((X_scaled - X_reconstructed) ** 2)
print(f"\nReconstruction MSE with 10 components: {reconstruction_error:.4f}")
```

## Exercise
1. Find the minimum number of components needed to retain 90% of variance, and compare downstream model accuracy at that number vs. using all 64 features.
2. Visualize the first two principal components' loadings (`pca_2d.components_`) to see which original pixels contribute most to each component.
3. Compare PCA (unsupervised) against a supervised feature selection method (file 003) on the same dataset and discuss when you'd prefer one over the other.

## Key Takeaways
- Always standardize features before PCA — otherwise high-variance features dominate the components purely due to scale, not true importance.
- PCA components are linear combinations of ALL original features, so they're much less interpretable than raw features or a feature-selection subset.
- Fit PCA only on training data and `.transform()` (not `.fit_transform()`) on test/validation data, exactly like scalers (file 001).
