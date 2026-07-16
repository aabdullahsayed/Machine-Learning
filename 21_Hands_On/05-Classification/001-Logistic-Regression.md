# 001 - Logistic Regression

## Concept
Despite the name, logistic regression is a classification algorithm. It applies the sigmoid function to a linear combination of features, squashing output into a (0,1) probability, then thresholds it into a class.

## Why It Matters
It's the simplest, most interpretable classifier and the natural bridge from linear regression (module 04). It's also literally a single-layer neural network with a sigmoid activation (module 10).

## Hands-On

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report

# 1. The sigmoid function - core to logistic regression
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

z_values = np.linspace(-10, 10, 100)
plt.figure(figsize=(6, 4))
plt.plot(z_values, sigmoid(z_values))
plt.axhline(0.5, color="gray", linestyle="--")
plt.axvline(0, color="gray", linestyle="--")
plt.title("Sigmoid Function")
plt.xlabel("z (linear combination of features)")
plt.ylabel("P(class = 1)")
plt.savefig("sigmoid_function.png")
plt.close()

# 2. Generate a binary classification dataset
X, y = make_classification(n_samples=500, n_features=2, n_redundant=0,
                            n_clusters_per_class=1, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)

# 3. Fit logistic regression
model = LogisticRegression()
model.fit(X_train_s, y_train)

# 4. Predict classes AND probabilities
y_pred = model.predict(X_test_s)
y_proba = model.predict_proba(X_test_s)  # [:, 1] = P(class=1)
print("First 5 predictions:", y_pred[:5])
print("First 5 probabilities (class 0, class 1):\n", y_proba[:5])

print(f"\nAccuracy: {accuracy_score(y_test, y_pred):.4f}")
print("\n", classification_report(y_test, y_pred))

# 5. Decision boundary visualization - the line where P(class=1) = 0.5
xx, yy = np.meshgrid(
    np.linspace(X_train_s[:, 0].min() - 1, X_train_s[:, 0].max() + 1, 200),
    np.linspace(X_train_s[:, 1].min() - 1, X_train_s[:, 1].max() + 1, 200)
)
grid_proba = model.predict_proba(np.c_[xx.ravel(), yy.ravel()])[:, 1].reshape(xx.shape)

plt.figure(figsize=(7, 6))
plt.contourf(xx, yy, grid_proba, levels=20, cmap="RdBu", alpha=0.6)
plt.colorbar(label="P(class=1)")
plt.scatter(X_train_s[:, 0], X_train_s[:, 1], c=y_train, edgecolor="k", cmap="RdBu")
plt.title("Logistic Regression Decision Boundary")
plt.savefig("logistic_regression_boundary.png")
plt.close()

# 6. Coefficients interpretation
print("\nCoefficients:", model.coef_, "Intercept:", model.intercept_)
print("A positive coefficient increases the log-odds of class 1 as the feature increases.")

# 7. Changing the decision threshold (default 0.5) - useful for imbalanced
# problems, connects to module 06 (Precision-Recall)
custom_threshold = 0.3
y_pred_custom = (y_proba[:, 1] >= custom_threshold).astype(int)
print(f"\nAt threshold=0.5: {accuracy_score(y_test, y_pred):.4f} accuracy")
print(f"At threshold={custom_threshold}: {accuracy_score(y_test, y_pred_custom):.4f} accuracy")
```

## Exercise
1. Derive (in comments) why the sigmoid function maps any real number to (0,1) — check `sigmoid(0)`, `sigmoid(100)`, `sigmoid(-100)`.
2. Sweep the decision threshold from 0.1 to 0.9 in steps of 0.1 and plot how accuracy changes.
3. Fit logistic regression on a dataset with 3 classes using `multi_class="multinomial"` and inspect `model.coef_.shape` — how many weight vectors are learned?

## Key Takeaways
- Logistic regression outputs probabilities, not raw classes — `predict()` just thresholds `predict_proba()` at 0.5 by default.
- The decision boundary of logistic regression is always linear (a straight line/plane) in the original feature space.
- Threshold choice matters a lot for imbalanced classification and should be tuned using precision/recall tradeoffs (module 06), not left at the default 0.5.
