# 002 - Hierarchical Clustering

## Concept
Hierarchical clustering builds a tree (dendrogram) of nested clusters, either bottom-up (agglomerative: start with each point as its own cluster, merge closest pairs) or top-down (divisive). Unlike K-Means, it doesn't require pre-specifying `k` — you cut the dendrogram at any level.

## Why It Matters
The dendrogram gives a rich, multi-resolution view of cluster structure and doesn't assume spherical clusters the way K-Means does — useful for exploratory analysis when the "right" number of clusters isn't obvious.

## Hands-On

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from sklearn.preprocessing import StandardScaler

X, y_true = make_blobs(n_samples=50, centers=3, cluster_std=0.7, random_state=42)
X_scaled = StandardScaler().fit_transform(X)

# 1. Build and visualize a dendrogram using scipy - shows the FULL merge history
linkage_matrix = linkage(X_scaled, method="ward")  # ward minimizes within-cluster variance
plt.figure(figsize=(12, 6))
dendrogram(linkage_matrix)
plt.title("Hierarchical Clustering Dendrogram (Ward linkage)")
plt.xlabel("Sample index")
plt.ylabel("Distance")
plt.axhline(y=6, color="red", linestyle="--", label="Cut point -> 3 clusters")
plt.legend()
plt.savefig("dendrogram.png")
plt.close()

# 2. Different linkage methods change how "distance between clusters" is defined
linkage_methods = ["single", "complete", "average", "ward"]
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
for ax, method in zip(axes.ravel(), linkage_methods):
    Z = linkage(X_scaled, method=method)
    dendrogram(Z, ax=ax, no_labels=True)
    ax.set_title(f"Linkage: {method}")
plt.tight_layout()
plt.savefig("linkage_methods_comparison.png")
plt.close()
print("""
Linkage methods explained:
  single   -> distance between CLOSEST points in two clusters (can create long chains)
  complete -> distance between FARTHEST points (tends toward compact clusters)
  average  -> mean distance between all point pairs
  ward     -> minimizes increase in within-cluster variance (most common default)
""")

# 3. Cut the dendrogram at a specific number of clusters
cluster_labels_3 = fcluster(linkage_matrix, t=3, criterion="maxclust")
print("Cluster assignments (3 clusters):", cluster_labels_3)

# 4. sklearn's AgglomerativeClustering - fits directly into sklearn pipelines
agg_cluster = AgglomerativeClustering(n_clusters=3, linkage="ward")
agg_labels = agg_cluster.fit_predict(X_scaled)

plt.figure(figsize=(7, 6))
plt.scatter(X_scaled[:, 0], X_scaled[:, 1], c=agg_labels, cmap="viridis", alpha=0.7)
plt.title("Agglomerative Clustering Result")
plt.savefig("agglomerative_clustering_result.png")
plt.close()

# 5. Compare against K-Means on the same data
from sklearn.cluster import KMeans
kmeans_labels = KMeans(n_clusters=3, random_state=42, n_init=10).fit_predict(X_scaled)
from sklearn.metrics import adjusted_rand_score
agreement = adjusted_rand_score(agg_labels, kmeans_labels)
print(f"\nAgreement between Hierarchical and K-Means (Adjusted Rand Index): {agreement:.4f}")
print("(1.0 = perfect agreement, 0.0 = random-level agreement)")
```

## Exercise
1. Cut the same dendrogram at 2, 3, and 5 clusters using `fcluster` and visualize each result as a scatter plot.
2. Compare `linkage="single"` vs `linkage="ward"` on a dataset with elongated (non-spherical) clusters — which handles it better, and why?
3. Use `AgglomerativeClustering` on a small real dataset (10-20 rows) and manually verify the first few merges match your intuition about which points are "closest."

## Key Takeaways
- Hierarchical clustering doesn't require choosing `k` in advance — you decide the cut-point after seeing the full dendrogram.
- Ward linkage (minimizing variance increase) is the most common default and tends to produce K-Means-like compact clusters.
- Hierarchical clustering scales poorly to large datasets (O(n²) or worse) compared to K-Means — use it for exploratory work on small-to-medium data.
