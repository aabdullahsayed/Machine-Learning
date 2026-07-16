# 003 - Precision, Recall, and F1 Score

## Concept
**Precision** = TP / (TP + FP): of all predicted positives, how many were correct. **Recall** = TP / (TP + FN): of all actual positives, how many did we catch. **F1** = harmonic mean of precision and recall, balancing both. This lesson also covers the precision-recall tradeoff via threshold tuning.

## Why It Matters
Accuracy is misleading on imbalanced datasets (a 95%-accurate model can be useless if it just predicts the majority class always). Precision/recall/F1 give a much more honest picture for problems like fraud detection, medical diagnosis, or the churn/spam projects (module 05).

## Hands-On

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    precision_score, recall_score, f1_score, classification_report,
    precision_recall_curve, PrecisionRecallDisplay
)
from sklearn.dummy import DummyClassifier

# 1. The accuracy trap - a lazy "always predict majority class" model
X, y = make_classification(n_samples=1000, n_features=10, weights=[0.95, 0.05], random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y, random_state=42)

dummy = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
dummy_acc = dummy.score(X_test, y_test)
print(f"Dummy classifier accuracy (always predicts majority): {dummy_acc:.4f}")
print("-> Looks great, but this model NEVER catches a single positive case!")
print(f"   Dummy recall for class 1: {recall_score(y_test, dummy.predict(X_test)):.4f}")

# 2. A real model, evaluated properly
model = LogisticRegression(max_iter=1000, class_weight="balanced").fit(X_train, y_train)
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

print(f"\nReal model accuracy:  {model.score(X_test, y_test):.4f}")
print(f"Real model precision: {precision_score(y_test, y_pred):.4f}")
print(f"Real model recall:    {recall_score(y_test, y_pred):.4f}")
print(f"Real model F1:        {f1_score(y_test, y_pred):.4f}")
print("\n", classification_report(y_test, y_pred))

# 3. The precision-recall tradeoff - controlled by the decision threshold
precisions, recalls, thresholds = precision_recall_curve(y_test, y_proba)

plt.figure(figsize=(7, 5))
plt.plot(thresholds, precisions[:-1], label="Precision")
plt.plot(thresholds, recalls[:-1], label="Recall")
plt.xlabel("Decision Threshold")
plt.ylabel("Score")
plt.legend()
plt.title("Precision-Recall Tradeoff vs Threshold")
plt.savefig("precision_recall_tradeoff.png")
plt.close()

# 4. Precision-Recall curve (threshold-independent view)
PrecisionRecallDisplay.from_predictions(y_test, y_proba)
plt.title("Precision-Recall Curve")
plt.savefig("precision_recall_curve.png")
plt.close()

# 5. Choosing a threshold based on business needs
# Scenario: we want recall >= 0.9 (catch 90%+ of positives), find the
# highest precision achievable at that recall level
valid_indices = np.where(recalls >= 0.9)[0]
if len(valid_indices) > 0:
    best_idx = valid_indices[np.argmax(precisions[valid_indices])]
    chosen_threshold = thresholds[min(best_idx, len(thresholds) - 1)]
    print(f"\nTo guarantee recall >= 0.9, use threshold ≈ {chosen_threshold:.3f}, "
          f"achieving precision ≈ {precisions[best_idx]:.3f}")

# 6. F-beta score - weight recall more (beta>1) or precision more (beta<1)
from sklearn.metrics import fbeta_score
f2 = fbeta_score(y_test, y_pred, beta=2)  # recall weighted 2x more than precision
f0_5 = fbeta_score(y_test, y_pred, beta=0.5)  # precision weighted 2x more than recall
print(f"\nF2 score (recall-focused):    {f2:.4f}")
print(f"F0.5 score (precision-focused): {f0_5:.4f}")
```

## Exercise
1. Explain why the dummy classifier's accuracy is high but useless — connect this to the churn project (module 05, file 007) and why `class_weight="balanced"` was used there.
2. Find the threshold that maximizes F1 score by sweeping over `thresholds` and computing F1 at each — compare it to the default (0.5) threshold's F1.
3. For a hypothetical cancer-screening model, argue (in 2-3 sentences) whether you'd optimize for precision or recall, and pick an appropriate F-beta value.

## Key Takeaways
- Never trust accuracy alone on imbalanced data — always check precision, recall, and F1 (or better, the full classification report).
- Precision and recall trade off against each other as you move the decision threshold — there's no free lunch, only business-driven choices.
- F-beta scores let you formally encode "recall matters more" (beta>1) or "precision matters more" (beta<1) into a single number.
