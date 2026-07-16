# 004 - ROC Curve and AUC

## Concept
The ROC (Receiver Operating Characteristic) curve plots the True Positive Rate (recall) against the False Positive Rate at every possible classification threshold. AUC (Area Under the Curve) summarizes this into a single number: the probability a randomly chosen positive example is ranked higher than a randomly chosen negative one.

## Why It Matters
ROC-AUC is threshold-independent, making it ideal for comparing models before you've committed to a specific operating threshold — it's the standard metric reported in the churn project (module 05, file 007) and used heavily throughout module 09.

## Hands-On

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import roc_curve, roc_auc_score, RocCurveDisplay

X, y = make_classification(n_samples=1000, n_features=10, weights=[0.7, 0.3],
                            flip_y=0.05, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y, random_state=42)

# 1. Compare a strong model vs a weak model vs a random-guess model
strong_model = LogisticRegression(max_iter=1000).fit(X_train, y_train)
weak_model = DecisionTreeClassifier(max_depth=1, random_state=42).fit(X_train, y_train)

strong_proba = strong_model.predict_proba(X_test)[:, 1]
weak_proba = weak_model.predict_proba(X_test)[:, 1]
random_proba = np.random.uniform(0, 1, len(y_test))  # a "model" that just guesses

for name, proba in [("Strong (LogReg)", strong_proba),
                     ("Weak (stump)", weak_proba),
                     ("Random guessing", random_proba)]:
    auc = roc_auc_score(y_test, proba)
    print(f"{name:20s} -> AUC: {auc:.4f}")

# 2. Manually compute TPR/FPR at a few thresholds to understand the curve
fpr, tpr, thresholds = roc_curve(y_test, strong_proba)
print("\nSample points along the ROC curve:")
for i in range(0, len(thresholds), max(1, len(thresholds) // 5)):
    print(f"  threshold={thresholds[i]:.3f} -> FPR={fpr[i]:.3f}, TPR={tpr[i]:.3f}")

# 3. Plot ROC curves for comparison
plt.figure(figsize=(7, 6))
for name, proba in [("Strong (LogReg)", strong_proba), ("Weak (stump)", weak_proba)]:
    fpr_i, tpr_i, _ = roc_curve(y_test, proba)
    auc_i = roc_auc_score(y_test, proba)
    plt.plot(fpr_i, tpr_i, label=f"{name} (AUC={auc_i:.3f})")
plt.plot([0, 1], [0, 1], "k--", label="Random guessing (AUC=0.5)")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve Comparison")
plt.legend()
plt.savefig("roc_curve_comparison.png")
plt.close()

# 4. AUC interpretation - the ranking probability
print("""
AUC interpretation: an AUC of 0.85 means that if you randomly pick one
positive example and one negative example, the model assigns a higher
predicted probability to the positive one 85% of the time.
AUC = 0.5  -> no better than random guessing
AUC = 1.0  -> perfect separation
AUC < 0.5  -> worse than random (predictions are inverted!)
""")

# 5. When ROC-AUC can be misleading: severe class imbalance
X_imb, y_imb = make_classification(n_samples=1000, weights=[0.99, 0.01], random_state=42)
X_tr, X_te, y_tr, y_te = train_test_split(X_imb, y_imb, test_size=0.3, stratify=y_imb, random_state=42)
model_imb = LogisticRegression(max_iter=1000).fit(X_tr, y_tr)
proba_imb = model_imb.predict_proba(X_te)[:, 1]
print(f"Highly imbalanced data (1% positive) -> ROC-AUC: {roc_auc_score(y_te, proba_imb):.4f}")
print("On extreme imbalance, ROC-AUC can look deceptively good; "
      "Precision-Recall AUC (file 003) is often more informative in that regime.")
```

## Exercise
1. Compute both ROC-AUC and Precision-Recall AUC (`average_precision_score`) on the extremely imbalanced dataset (1% positive) — which metric better reflects the model's practical usefulness?
2. Plot ROC curves for 3 different `max_depth` values of a `DecisionTreeClassifier` — how does AUC change with tree complexity?
3. Explain in one sentence why AUC is "threshold-independent" while precision/recall/F1 (file 003) are threshold-dependent.

## Key Takeaways
- ROC-AUC summarizes a model's ranking ability across ALL thresholds — useful for model comparison before choosing an operating point.
- For severely imbalanced datasets, Precision-Recall AUC is often more informative than ROC-AUC, which can look artificially high.
- An AUC near 0.5 means the model isn't learning useful signal; check your features and target before assuming a bug.
