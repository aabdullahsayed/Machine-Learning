# 004 - Anomaly Detection

## Concept
Anomaly (outlier) detection identifies rare items that differ significantly from the majority of data. This lesson expands module 02's outlier detection (file 003) into full unsupervised anomaly-detection algorithms: Isolation Forest, One-Class SVM, and Local Outlier Factor (LOF) — each with a different notion of "normal."

## Why It Matters
Anomaly detection powers fraud detection, network intrusion detection, and manufacturing defect detection — problems where "abnormal" examples are too rare or novel to train a standard supervised classifier (module 05) on.

## Hands-On

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import StandardScaler

np.random.seed(42)
# Normal data: a dense cluster
X_normal = np.random.normal(0, 1, (300, 2))
# Anomalies: sparse points elsewhere
X_anomalies = np.random.uniform(-6, 6, (20, 2))
X = np.vstack([X_normal, X_anomalies])
true_labels = np.array([1] * 300 + [-1] * 20)  # 1 = normal, -1 = anomaly

X_scaled = StandardScaler().fit_transform(X)

# 1. Isolation Forest - isolates anomalies via random recursive partitioning;
# anomalies require FEWER splits to isolate since they're "sparse"
iso_forest = IsolationForest(contamination=0.06, random_state=42)
iso_pred = iso_forest.fit_predict(X_scaled)  # 1 = normal, -1 = anomaly
iso_scores = iso_forest.decision_function(X_scaled)  # higher = more normal

# 2. One-Class SVM - learns a boundary around the "normal" region, flagging
# anything outside it; sensitive to kernel/gamma choice
oc_svm = OneClassSVM(nu=0.06, kernel="rbf", gamma="scale")
svm_pred = oc_svm.fit_predict(X_scaled)

# 3. Local Outlier Factor - compares a point's local density to its
# neighbors' local density; great for anomalies that are only "local" outliers
lof = LocalOutlierFactor(n_neighbors=20, contamination=0.06)
lof_pred = lof.fit_predict(X_scaled)

# 4. Visualize all three side-by-side
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
for ax, pred, name in zip(axes, [iso_pred, svm_pred, lof_pred],
                            ["Isolation Forest", "One-Class SVM", "LOF"]):
    ax.scatter(X_scaled[pred == 1, 0], X_scaled[pred == 1, 1],
               c="blue", alpha=0.5, label="Normal")
    ax.scatter(X_scaled[pred == -1, 0], X_scaled[pred == -1, 1],
               c="red", marker="x", s=100, label="Anomaly")
    ax.set_title(name)
    ax.legend()
plt.savefig("anomaly_detection_comparison.png")
plt.close()

# 5. Evaluate against ground truth (only possible here because we SIMULATED
# the anomalies - in real applications you often don't have this luxury)
from sklearn.metrics import classification_report
for pred, name in zip([iso_pred, svm_pred, lof_pred],
                       ["Isolation Forest", "One-Class SVM", "LOF"]):
    print(f"\n--- {name} ---")
    print(classification_report(true_labels, pred, target_names=["anomaly", "normal"]))

# 6. Anomaly SCORES, not just binary labels - useful for ranking/prioritizing
# which anomalies to investigate first
top_anomalies_idx = np.argsort(iso_scores)[:5]  # 5 most anomalous points
print("\nTop 5 most anomalous points (Isolation Forest scores):")
for idx in top_anomalies_idx:
    print(f"  Point {idx}: score={iso_scores[idx]:.4f}, coords={X_scaled[idx]}")
```

## Exercise
1. Tune the `contamination` parameter (expected proportion of anomalies) for Isolation Forest and observe how the number of flagged points changes.
2. Apply LOF to a dataset with two clusters of very different densities — does it correctly find local outliers in the sparser cluster too (unlike a single global density threshold would)?
3. Combine anomaly detection with a supervised model: use Isolation Forest to flag likely-anomalous training points, remove them, and check if a downstream regression/classification model (modules 04-05) improves.

## Key Takeaways
- Isolation Forest is fast, scales well, and works well in higher dimensions — often a solid default.
- One-Class SVM defines a boundary around "normal" data and can be sensitive to hyperparameter choice, similar to regular SVMs (module 05, file 005).
- LOF detects *local* anomalies relative to their neighborhood density, which global methods can miss when data has clusters of varying density.
