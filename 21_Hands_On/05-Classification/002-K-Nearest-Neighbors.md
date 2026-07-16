# 002 - K-Nearest Neighbors (KNN)

## Concept
KNN is a non-parametric, instance-based algorithm: to classify a new point, find its `k` closest neighbors (by some distance metric) in the training data and take a majority vote. There's no explicit "training" — all computation happens at prediction time ("lazy learning").

## Why It Matters
KNN is a great illustration of distance-based learning and directly motivates the need for feature scaling (module 07) — distances are meaningless if features are on wildly different scales.

## Hands-On

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

# 1. Implement Euclidean distance and a basic KNN from scratch to build intuition
def euclidean_distance(a, b):
    return np.sqrt(np.sum((a - b) ** 2))

class KNNScratch:
    def __init__(self, k=3):
        self.k = k

    def fit(self, X, y):
        self.X_train = X
        self.y_train = y
        return self

    def predict_one(self, x):
        distances = [euclidean_distance(x, x_train) for x_train in self.X_train]
        k_indices = np.argsort(distances)[:self.k]
        k_nearest_labels = self.y_train[k_indices]
        values, counts = np.unique(k_nearest_labels, return_counts=True)
        return values[np.argmax(counts)]

    def predict(self, X):
        return np.array([self.predict_one(x) for x in X])

X, y = make_classification(n_samples=300, n_features=2, n_redundant=0,
                            n_clusters_per_class=1, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

scratch_knn = KNNScratch(k=5).fit(X_train, y_train)
scratch_preds = scratch_knn.predict(X_test)
print("From-scratch KNN accuracy:", accuracy_score(y_test, scratch_preds))

# 2. Compare with sklearn's optimized implementation
sk_knn = KNeighborsClassifier(n_neighbors=5)
sk_knn.fit(X_train, y_train)
sk_preds = sk_knn.predict(X_test)
print("sklearn KNN accuracy:", accuracy_score(y_test, sk_preds))

# 3. Why scaling matters - demonstrate with mismatched feature scales
X_unscaled = np.column_stack([X[:, 0] * 1000, X[:, 1]])  # feature 0 is 1000x bigger
X_train_u, X_test_u, y_train_u, y_test_u = train_test_split(
    X_unscaled, y, test_size=0.3, random_state=42
)

knn_no_scaling = KNeighborsClassifier(n_neighbors=5).fit(X_train_u, y_train_u)
acc_no_scaling = accuracy_score(y_test_u, knn_no_scaling.predict(X_test_u))

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_u)
X_test_scaled = scaler.transform(X_test_u)
knn_scaled = KNeighborsClassifier(n_neighbors=5).fit(X_train_scaled, y_train_u)
acc_scaled = accuracy_score(y_test_u, knn_scaled.predict(X_test_scaled))

print(f"\nWithout scaling: {acc_no_scaling:.4f}")
print(f"With scaling:    {acc_scaled:.4f}")
print("-> Feature 0 (1000x larger) dominates distance calculations without scaling.")

# 4. Choosing k - the key hyperparameter, controls bias-variance tradeoff
k_values = range(1, 30, 2)
accuracies = []
for k in k_values:
    knn = KNeighborsClassifier(n_neighbors=k).fit(X_train, y_train)
    accuracies.append(accuracy_score(y_test, knn.predict(X_test)))

plt.figure(figsize=(7, 4))
plt.plot(k_values, accuracies, marker="o")
plt.xlabel("k (number of neighbors)")
plt.ylabel("Test Accuracy")
plt.title("KNN: Effect of k")
plt.savefig("knn_k_selection.png")
plt.close()
print(f"\nBest k: {k_values[np.argmax(accuracies)]}")
```

## Exercise
1. Modify `KNNScratch` to support a `weighted` voting mode where closer neighbors count more (weight = 1/distance).
2. Explain why very small `k` (like k=1) leads to high variance (overfitting) and very large `k` leads to high bias (underfitting) — connect this to module 03, file 003.
3. Try `KNeighborsClassifier(metric="manhattan")` vs the default `"minkowski"` (Euclidean) — does it change accuracy on this dataset?

## Key Takeaways
- KNN has no training phase — it's "lazy" — but prediction is expensive since it computes distances to every training point.
- Feature scaling is not optional for KNN; unscaled features with large ranges will dominate the distance metric.
- `k` directly controls the bias-variance tradeoff: small k = flexible/high variance, large k = smooth/high bias.
