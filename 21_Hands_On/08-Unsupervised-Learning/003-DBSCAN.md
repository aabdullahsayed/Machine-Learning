# 003 - DBSCAN

## Concept
DBSCAN (Density-Based Spatial Clustering of Applications with Noise) groups points that are closely packed together (dense regions), marking points in low-density regions as noise/outliers. Unlike K-Means, it doesn't require specifying `k` and can find arbitrarily-shaped clusters.

## Why It Matters
It elegantly solves two of K-Means' weaknesses seen in file 001: non-spherical cluster shapes and sensitivity to outliers (it explicitly labels outliers as noise instead of forcing them into a cluster).

## Hands-On

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons, make_blobs
from sklearn.cluster import DBSCAN, KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors

# 1. DBSCAN shines on non-spherical shapes where K-Means fails
X_moons, _ = make_moons(n_samples=300, noise=0.08, random_state=42)
X_moons_scaled = StandardScaler().fit_transform(X_moons)

kmeans_moons = KMeans(n_clusters=2, random_state=42, n_init=10).fit_predict(X_moons_scaled)
dbscan_moons = DBSCAN(eps=0.3, min_samples=5).fit_predict(X_moons_scaled)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
axes[0].scatter(X_moons_scaled[:, 0], X_moons_scaled[:, 1], c=kmeans_moons, cmap="viridis")
axes[0].set_title("K-Means (fails on crescent shapes)")
axes[1].scatter(X_moons_scaled[:, 0], X_moons_scaled[:, 1], c=dbscan_moons, cmap="viridis")
axes[1].set_title("DBSCAN (correctly finds crescents)")
plt.savefig("dbscan_vs_kmeans_moons.png")
plt.close()

# 2. Understanding DBSCAN's two key hyperparameters
# eps: max distance for two points to be considered neighbors
# min_samples: min points needed to form a dense region (a "core point")
print("""
DBSCAN point types:
  Core point   -> has >= min_samples neighbors within eps distance
  Border point -> within eps of a core point, but doesn't have enough neighbors itself
  Noise point  -> neither core nor border -> labeled -1 (outlier)
""")

# 3. DBSCAN naturally detects outliers as noise (label = -1)
X_blobs, _ = make_blobs(n_samples=200, centers=3, cluster_std=0.6, random_state=42)
outliers = np.random.uniform(-10, 10, (10, 2))  # scattered noise points
X_with_outliers = np.vstack([X_blobs, outliers])
X_scaled = StandardScaler().fit_transform(X_with_outliers)

dbscan = DBSCAN(eps=0.3, min_samples=5).fit(X_scaled)
n_noise = np.sum(dbscan.labels_ == -1)
n_clusters = len(set(dbscan.labels_)) - (1 if -1 in dbscan.labels_ else 0)
print(f"DBSCAN found {n_clusters} clusters and flagged {n_noise} points as noise/outliers")

plt.figure(figsize=(7, 6))
colors = dbscan.labels_
plt.scatter(X_scaled[:, 0], X_scaled[:, 1], c=colors, cmap="viridis")
plt.scatter(X_scaled[colors == -1, 0], X_scaled[colors == -1, 1],
            c="red", marker="x", s=100, label="Noise (outliers)")
plt.legend()
plt.title("DBSCAN Outlier Detection")
plt.savefig("dbscan_outliers.png")
plt.close()

# 4. Choosing eps - the k-distance plot method
neighbors = NearestNeighbors(n_neighbors=5)
neighbors.fit(X_scaled)
distances, _ = neighbors.kneighbors(X_scaled)
k_distances = np.sort(distances[:, -1])

plt.figure(figsize=(7, 5))
plt.plot(k_distances)
plt.xlabel("Points sorted by distance")
plt.ylabel("5th nearest neighbor distance")
plt.title("K-Distance Plot for Choosing eps")
plt.savefig("dbscan_eps_selection.png")
plt.close()
print("Look for the 'knee' in this plot - that distance value is a good eps choice.")

# 5. Sensitivity to hyperparameters
for eps in [0.1, 0.3, 0.5, 1.0]:
    labels = DBSCAN(eps=eps, min_samples=5).fit_predict(X_scaled)
    n_clust = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise_i = np.sum(labels == -1)
    print(f"eps={eps}: {n_clust} clusters, {n_noise_i} noise points")
```

## Exercise
1. Use the k-distance plot method to select `eps` for a new synthetic dataset, then verify DBSCAN's resulting cluster count matches the true generative number of clusters.
2. Compare DBSCAN and K-Means on a dataset with clusters of very different densities — where does DBSCAN also start to struggle?
3. Explain, using the core/border/noise point definitions, why DBSCAN can find clusters of arbitrary shape while K-Means cannot.

## Key Takeaways
- DBSCAN doesn't require specifying the number of clusters, and naturally handles outliers by labeling them as noise (-1) rather than forcing them into a cluster.
- It excels at non-spherical, arbitrarily-shaped clusters where K-Means fundamentally fails.
- Its main weakness: a single global `eps`/`min_samples` struggles when clusters have very different densities — a scenario where K-Means or Gaussian Mixture Models may do better.
