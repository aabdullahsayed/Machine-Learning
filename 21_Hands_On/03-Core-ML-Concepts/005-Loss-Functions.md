# 005 - Loss Functions

## Concept
A loss function quantifies how wrong a model's prediction is for a single example; a cost function averages this over the dataset. Different tasks need different losses: MSE/MAE for regression, cross-entropy for classification, hinge loss for SVMs.

## Why It Matters
The loss function IS what gradient descent (module 03, file 006) optimizes. Choosing the wrong loss (e.g., MSE for classification) leads to poorly calibrated, slow-to-train models.

## Hands-On

```python
import numpy as np
import matplotlib.pyplot as plt

# --- Regression losses ---
y_true_reg = np.array([3.0, -0.5, 2.0, 7.0])
y_pred_reg = np.array([2.5, 0.0, 2.0, 8.0])

def mse(y_true, y_pred):
    return np.mean((y_true - y_pred) ** 2)

def mae(y_true, y_pred):
    return np.mean(np.abs(y_true - y_pred))

def huber_loss(y_true, y_pred, delta=1.0):
    error = y_true - y_pred
    is_small = np.abs(error) <= delta
    squared_loss = 0.5 * error ** 2
    linear_loss = delta * (np.abs(error) - 0.5 * delta)
    return np.mean(np.where(is_small, squared_loss, linear_loss))

print("MSE:", mse(y_true_reg, y_pred_reg))
print("MAE:", mae(y_true_reg, y_pred_reg))
print("Huber:", huber_loss(y_true_reg, y_pred_reg))

# Why it matters: MSE penalizes large errors quadratically -> sensitive to outliers
y_true_outlier = np.array([3.0, -0.5, 2.0, 100.0])  # one big outlier
y_pred_outlier = np.array([2.5, 0.0, 2.0, 8.0])
print("\nWith an outlier:")
print("MSE:", mse(y_true_outlier, y_pred_outlier), "(dominated by the outlier)")
print("MAE:", mae(y_true_outlier, y_pred_outlier), "(more robust to the outlier)")

# --- Classification losses ---
# Binary cross-entropy (log loss)
def binary_cross_entropy(y_true, y_pred_proba, eps=1e-15):
    y_pred_proba = np.clip(y_pred_proba, eps, 1 - eps)  # avoid log(0)
    return -np.mean(
        y_true * np.log(y_pred_proba) + (1 - y_true) * np.log(1 - y_pred_proba)
    )

y_true_clf = np.array([1, 0, 1, 1])
y_pred_confident_correct = np.array([0.9, 0.1, 0.8, 0.95])
y_pred_wrong_confident = np.array([0.1, 0.9, 0.2, 0.05])

print("\nBCE (confident & correct):", binary_cross_entropy(y_true_clf, y_pred_confident_correct))
print("BCE (confident & WRONG):", binary_cross_entropy(y_true_clf, y_pred_wrong_confident))
print("  -> cross-entropy punishes confident wrong predictions MUCH more than MSE would.")

# Visualize how loss changes as predicted probability moves for a true label of 1
p_values = np.linspace(0.01, 0.99, 100)
bce_curve = [-np.log(p) for p in p_values]  # loss when true label = 1
plt.figure(figsize=(6, 4))
plt.plot(p_values, bce_curve)
plt.xlabel("Predicted probability of class 1")
plt.ylabel("Cross-entropy loss (true label = 1)")
plt.title("Cross-Entropy Loss Curve")
plt.savefig("cross_entropy_curve.png")
plt.close()

# Multi-class: categorical cross-entropy
def categorical_cross_entropy(y_true_onehot, y_pred_proba, eps=1e-15):
    y_pred_proba = np.clip(y_pred_proba, eps, 1 - eps)
    return -np.mean(np.sum(y_true_onehot * np.log(y_pred_proba), axis=1))

y_true_multi = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])  # one-hot
y_pred_multi = np.array([[0.7, 0.2, 0.1], [0.1, 0.8, 0.1], [0.2, 0.2, 0.6]])
print("\nCategorical cross-entropy:", categorical_cross_entropy(y_true_multi, y_pred_multi))
```

## Exercise
1. Compute MSE, MAE, and Huber loss for a dataset with two outliers and compare how much each metric is affected.
2. Plot the binary cross-entropy loss curve for a true label of 0 (instead of 1) — how does the curve's shape change?
3. Implement hinge loss (`max(0, 1 - y_true * y_pred)`, with `y_true` in {-1, 1}) and compute it for a small set of predictions — this is the loss used by SVMs (module 05).

## Key Takeaways
- MSE is sensitive to outliers (squared penalty); MAE and Huber loss are more robust.
- Cross-entropy is the standard loss for classification because it heavily penalizes confident, wrong predictions — exactly what you want a classifier to avoid.
- The loss function you choose shapes what "good" means to your optimizer — always match it to your actual business objective, not just habit.
