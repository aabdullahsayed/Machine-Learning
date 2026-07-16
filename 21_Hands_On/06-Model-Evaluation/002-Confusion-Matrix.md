# 002 - Confusion Matrix

## Concept
A confusion matrix tabulates predictions vs. actual labels: True Positives (TP), True Negatives (TN), False Positives (FP), and False Negatives (FN). Nearly every classification metric (accuracy, precision, recall, F1) is derived from these four numbers.

## Why It Matters
Understanding the confusion matrix deeply lets you reason about the *type* of error your model makes, which is often more important than a single scalar accuracy number — especially in asymmetric-cost problems like the churn (module 05, file 007) and spam (module 05, file 006) projects.

## Hands-On

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

X, y = make_classification(n_samples=500, n_features=5, weights=[0.85, 0.15], random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y, random_state=42)

model = LogisticRegression(max_iter=1000).fit(X_train, y_train)
y_pred = model.predict(X_test)

# 1. Build the confusion matrix manually to understand its structure
cm = confusion_matrix(y_test, y_pred)
tn, fp, fn, tp = cm.ravel()
print("Confusion Matrix:\n", cm)
print(f"\nTrue Negatives (TN):  {tn}  -> correctly predicted class 0")
print(f"False Positives (FP): {fp}  -> predicted class 1, actually class 0 (Type I error)")
print(f"False Negatives (FN): {fn}  -> predicted class 0, actually class 1 (Type II error)")
print(f"True Positives (TP):  {tp}  -> correctly predicted class 1")

# 2. Visualize
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Class 0", "Class 1"])
disp.plot(cmap="Blues")
plt.title("Confusion Matrix")
plt.savefig("confusion_matrix_example.png")
plt.close()

# 3. Manually derive metrics from the confusion matrix (previews file 003)
accuracy = (tp + tn) / (tp + tn + fp + fn)
precision = tp / (tp + fp) if (tp + fp) > 0 else 0
recall = tp / (tp + fn) if (tp + fn) > 0 else 0
print(f"\nAccuracy:  {accuracy:.4f}")
print(f"Precision: {precision:.4f}  (of predicted positives, how many were correct)")
print(f"Recall:    {recall:.4f}  (of actual positives, how many were caught)")

# 4. Concrete example of why FP and FN have different real-world costs
print("""
Example - Medical diagnosis for a serious disease:
  FN (missed a sick patient)    -> potentially life-threatening, VERY costly
  FP (flagged a healthy patient)-> extra test, inconvenient but low-risk

Example - Email spam filter:
  FN (spam reaches inbox)       -> mildly annoying
  FP (real email marked spam)   -> could mean a missed job offer, VERY costly

The confusion matrix forces you to look at BOTH error types separately,
instead of collapsing them into one accuracy number.
""")

# 5. Multi-class confusion matrix
from sklearn.datasets import load_iris
iris = load_iris()
X_train_i, X_test_i, y_train_i, y_test_i = train_test_split(
    iris.data, iris.target, test_size=0.3, random_state=42
)
model_iris = LogisticRegression(max_iter=1000).fit(X_train_i, y_train_i)
cm_multi = confusion_matrix(y_test_i, model_iris.predict(X_test_i))
disp_multi = ConfusionMatrixDisplay(cm_multi, display_labels=iris.target_names)
disp_multi.plot(cmap="Greens")
plt.title("Multi-Class Confusion Matrix (Iris)")
plt.savefig("confusion_matrix_multiclass.png")
plt.close()
```

## Exercise
1. Build a confusion matrix for a model with `class_weight="balanced"` vs `class_weight=None` on the same imbalanced dataset — how does the TP/FN balance shift?
2. For the multi-class Iris confusion matrix, identify which two classes are most often confused with each other, and hypothesize why (hint: look at the original feature distributions).
3. Write a function `cost_from_confusion_matrix(cm, fp_cost, fn_cost)` that computes total business cost from a confusion matrix and two cost values.

## Key Takeaways
- Every classification metric is a different way of summarizing TP, TN, FP, FN — understanding the matrix means understanding all downstream metrics.
- Which error type (FP vs FN) matters more is a business/domain decision, not a statistical one.
- For multi-class problems, off-diagonal entries reveal exactly which classes the model confuses.
