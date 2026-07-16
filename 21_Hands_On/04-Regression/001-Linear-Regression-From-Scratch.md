# 001 - Linear Regression From Scratch

## Concept
Linear regression models the relationship `y = w1*x1 + w2*x2 + ... + b` between features and a continuous target. This lesson implements it two ways: the closed-form Normal Equation, and gradient descent — connecting directly to modules 01 (linear algebra) and 03 (gradient descent).

## Why It Matters
Linear regression is the simplest, most interpretable model and a baseline you should always compare against before reaching for anything fancier.

## Hands-On

```python
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)
n = 100
X = np.random.uniform(0, 10, n)
true_w, true_b = 2.5, 4.0
y = true_w * X + true_b + np.random.normal(0, 2, n)

# --- Method 1: Closed-form Normal Equation: w = (X^T X)^-1 X^T y ---
X_design = np.column_stack([np.ones(n), X])  # add bias column of 1s
w_closed_form = np.linalg.inv(X_design.T @ X_design) @ X_design.T @ y
b_cf, w_cf = w_closed_form
print(f"Closed-form solution -> w={w_cf:.3f}, b={b_cf:.3f}")

# --- Method 2: From-scratch gradient descent (see module 03, file 006) ---
class LinearRegressionScratch:
    def __init__(self, lr=0.01, epochs=1000):
        self.lr = lr
        self.epochs = epochs
        self.w = None
        self.b = None
        self.loss_history = []

    def fit(self, X, y):
        n = len(X)
        self.w, self.b = 0.0, 0.0
        for _ in range(self.epochs):
            y_pred = self.w * X + self.b
            error = y_pred - y
            dw = (2 / n) * np.sum(error * X)
            db = (2 / n) * np.sum(error)
            self.w -= self.lr * dw
            self.b -= self.lr * db
            self.loss_history.append(np.mean(error ** 2))
        return self

    def predict(self, X):
        return self.w * X + self.b

model = LinearRegressionScratch(lr=0.01, epochs=1000)
model.fit(X, y)
print(f"Gradient descent solution -> w={model.w:.3f}, b={model.b:.3f}")

# --- Compare against sklearn to validate correctness ---
from sklearn.linear_model import LinearRegression
sk_model = LinearRegression()
sk_model.fit(X.reshape(-1, 1), y)
print(f"sklearn solution -> w={sk_model.coef_[0]:.3f}, b={sk_model.intercept_:.3f}")

# Visualize fit
plt.figure(figsize=(7, 5))
plt.scatter(X, y, alpha=0.5, label="Data")
x_line = np.linspace(0, 10, 100)
plt.plot(x_line, model.predict(x_line), color="red", label="Learned fit (scratch)")
plt.legend()
plt.title("Linear Regression From Scratch")
plt.savefig("linear_regression_scratch.png")
plt.close()

# Plot loss curve to confirm convergence
plt.figure(figsize=(6, 4))
plt.plot(model.loss_history)
plt.xlabel("Epoch")
plt.ylabel("MSE Loss")
plt.title("Training Loss")
plt.savefig("linear_regression_loss.png")
plt.close()
```

## Exercise
1. Extend `LinearRegressionScratch` to handle multiple features (multivariate regression) using matrix operations (`X @ w`) instead of scalar `w * X`.
2. Compare the closed-form solution's speed vs. gradient descent's speed on a dataset with 100,000 rows — when does the closed-form approach become impractical (hint: matrix inversion is O(n³))?
3. Add L2 regularization (Ridge) to the from-scratch gradient descent loss and gradient — you'll formalize this fully in file 004.

## Key Takeaways
- The closed-form Normal Equation gives an exact solution but doesn't scale well to many features (matrix inversion cost) or huge datasets.
- Gradient descent scales better and generalizes to models with no closed-form solution (like neural networks).
- Always sanity-check a from-scratch implementation against a trusted library (sklearn) before trusting it on real data.
