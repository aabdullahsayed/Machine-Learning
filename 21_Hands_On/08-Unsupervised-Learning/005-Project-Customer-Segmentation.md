# 005 - Project: Customer Segmentation

## Concept
This project ties together K-Means, hierarchical clustering, and PCA into a real workflow: segmenting customers by purchasing behavior so a business can target each group differently (e.g., "high spenders," "bargain hunters," "at-risk churners").

## Why It Matters
Segmentation is one of the most common real-world unsupervised learning applications — used in marketing, retail, and banking. It's a great capstone for the clustering module because it forces you to combine scaling, dimensionality reduction, cluster count selection, and business interpretation.

## Hands-On

```python
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# 1. Simulate a customer dataset (annual income, spending score, purchase frequency)
np.random.seed(42)
n = 300
data = pd.DataFrame({
    "annual_income_k": np.concatenate([
        np.random.normal(25, 5, n // 3),
        np.random.normal(60, 8, n // 3),
        np.random.normal(90, 10, n // 3),
    ]),
    "spending_score": np.concatenate([
        np.random.normal(20, 10, n // 3),
        np.random.normal(55, 12, n // 3),
        np.random.normal(85, 8, n // 3),
    ]),
    "purchase_frequency": np.concatenate([
        np.random.normal(2, 1, n // 3),
        np.random.normal(8, 2, n // 3),
        np.random.normal(15, 3, n // 3),
    ]),
})

# 2. Scale features - critical since K-Means uses Euclidean distance
scaler = StandardScaler()
X_scaled = scaler.fit_transform(data)

# 3. Find k with the elbow method
inertias = []
k_range = range(1, 8)
for k in k_range:
    km = KMeans(n_clusters=k, n_init=10, random_state=42)
    km.fit(X_scaled)
    inertias.append(km.inertia_)

plt.plot(k_range, inertias, marker="o")
plt.xlabel("k")
plt.ylabel("Inertia")
plt.title("Elbow Method")
plt.savefig("elbow.png")
plt.close()

# 4. Fit final model with chosen k
k_final = 3
kmeans = KMeans(n_clusters=k_final, n_init=10, random_state=42)
data["segment"] = kmeans.fit_predict(X_scaled)

# 5. Profile each segment - the business-facing output
profile = data.groupby("segment").mean().round(1)
print(profile)

# 6. Visualize with PCA (reduce 3 features to 2D for plotting)
pca = PCA(n_components=2)
coords = pca.fit_transform(X_scaled)
plt.scatter(coords[:, 0], coords[:, 1], c=data["segment"], cmap="viridis")
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.title("Customer Segments (PCA projection)")
plt.savefig("segments.png")
plt.close()

# 7. Name the segments based on the profile table
segment_names = {0: "Budget Shoppers", 1: "Regular Customers", 2: "VIP High Spenders"}
data["segment_name"] = data["segment"].map(segment_names)
print(data["segment_name"].value_counts())
```

## Exercise
1. Add a fourth feature (e.g., `days_since_last_purchase`) and re-run the pipeline — does the optimal k change?
2. Replace K-Means with `AgglomerativeClustering` and compare the resulting segments using a crosstab.
3. Write a short paragraph translating each segment's stats into a marketing action (e.g., "VIP High Spenders → offer early access to new products").

## Key Takeaways
- Real clustering projects are 80% preprocessing/interpretation, 20% calling `.fit()`.
- The elbow method gives a candidate k, but business context should confirm the final choice.
- PCA is used here purely for visualization, not for the clustering itself — don't cluster on PCA output unless dimensionality is actually a problem.
