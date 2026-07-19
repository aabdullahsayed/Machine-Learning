# 001 - K-Means Clustering

## Concept
K-Means partitions data into `k` clusters by iteratively: (1) assigning each point to its nearest centroid, (2) recomputing centroids as the mean of assigned points, until convergence. It's the most widely used unsupervised clustering algorithm.

## Why It Matters
K-Means is fast, simple, and a great entry point into unsupervised learning (module 03, file 002) — but it makes strong assumptions (spherical, similarly-sized clusters) that later lessons (DBSCAN, file 003) address.

## Hands-On

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

# 1. Generate synthetic clustered data
X, y_true = make_blobs(n_samples=300, centers=4, cluster_std=0.8, random_state=42)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 2. Fit K-Means with the correct k
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
cluster_labels = kmeans.fit_predict(X_scaled)

plt.figure(figsize=(7, 6))
plt.scatter(X_scaled[:, 0], X_scaled[:, 1], c=cluster_labels, cmap="viridis", alpha=0.6)
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1],
            c="red", marker="X", s=200, label="Centroids")
plt.legend()
plt.title("K-Means Clustering (k=4)")
plt.savefig("kmeans_clusters.png")
plt.close()

# 3. The Elbow Method - find a good k by plotting inertia (within-cluster
# sum of squares) vs k, looking for a diminishing-returns "elbow"
inertias = []
k_range = range(1, 11)
for k in k_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X_scaled)
    inertias.append(km.inertia_)

plt.figure(figsize=(7, 5))
plt.plot(k_range, inertias, marker="o")
plt.xlabel("k")
plt.ylabel("Inertia (within-cluster sum of squares)")
plt.title("Elbow Method for Choosing k")
plt.savefig("kmeans_elbow.png")
plt.close()
print("Look for the 'elbow' where adding more clusters stops giving big inertia drops.")

# 4. Silhouette Score - a more principled metric, measures how similar a
# point is to its own cluster vs other clusters (range: -1 to 1, higher better)
silhouette_scores = []
for k in range(2, 11):
    km = KMeans(n_clusters=k, random_state=42, n_init=10).fit(X_scaled)
    score = silhouette_score(X_scaled, km.labels_)
    silhouette_scores.append(score)
    print(f"k={k}: silhouette score = {score:.4f}")

best_k = list(range(2, 11))[np.argmax(silhouette_scores)]
print(f"\nBest k by silhouette score: {best_k}")

# 5. K-Means' key limitation: assumes spherical, equal-variance clusters
X_uneven, _ = make_blobs(n_samples=300, centers=[[0, 0], [0, 5]],
                          cluster_std=[0.3, 2.5], random_state=42)
km_uneven = KMeans(n_clusters=2, random_state=42, n_init=10).fit(X_uneven)
plt.figure(figsize=(7, 6))
plt.scatter(X_uneven[:, 0], X_uneven[:, 1], c=km_uneven.labels_, cmap="viridis", alpha=0.6)
plt.title("K-Means Struggles with Unequal Variance Clusters")
plt.savefig("kmeans_limitation.png")
plt.close()
print("\nNotice: K-Means tends to split the high-variance cluster unfairly "
      "because it assumes roughly equal-sized, spherical clusters.")

# 6. Random initialization sensitivity - why n_init matters
inertias_single_init = []
for seed in range(5):
    km = KMeans(n_clusters=4, random_state=seed, n_init=1)  # single random init
    km.fit(X_scaled)
    inertias_single_init.append(km.inertia_)
print(f"\nInertia with n_init=1 across 5 seeds: {np.round(inertias_single_init, 2)}")
print("-> results vary by starting point; n_init=10 (default) runs multiple "
      "inits and keeps the best result, avoiding bad local optima.")
```

## Exercise
1. Apply K-Means to a dataset where you know the "true" number of clusters and compare the elbow method's suggestion vs the silhouette method's suggestion.
2. Use `KMeans(init="k-means++")` (the default) vs `init="random"` and compare stability across different `random_state` values.
3. Cluster a real dataset (e.g., customer data with `income` and `spending_score`) and write 2-3 sentences interpreting what each discovered cluster might represent as a customer segment.

## Key Takeaways
- K-Means requires you to choose `k` upfront — use the elbow method or silhouette score to guide that choice, not a guess.
- K-Means assumes clusters are roughly spherical and similarly sized; it performs poorly on elongated or unevenly-sized clusters (DBSCAN, file 003, handles this better).
- Always run with multiple random initializations (`n_init > 1`) since K-Means can converge to different local optima depending on starting centroids.
