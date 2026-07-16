# 003 - Bias-Variance Tradeoff

## Concept
A model's prediction error decomposes into three parts: **bias** (error from overly simplistic assumptions), **variance** (error from sensitivity to the specific training set), and **irreducible noise**. Simple models tend to have high bias/low variance (underfit); complex models tend to have low bias/high variance (overfit).

## Why It Matters
Nearly every modeling decision — model complexity, regularization strength (module 04), tree depth (module 05), number of boosting rounds (module 09) — is really a bias-variance tradeoff decision in disguise.

## Hands-On

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

np.random.seed(42)

# True underlying function (unknown to the model in real life)
def true_function(x):
    return np.sin(x) * 2

def generate_dataset(n=30, noise=0.5):
    x = np.sort(np.random.uniform(0, 2 * np.pi, n))
    y = true_function(x) + np.random.normal(0, noise, n)
    return x.reshape(-1, 1), y

x_test = np.linspace(0, 2 * np.pi, 200).reshape(-1, 1)
y_test_true = true_function(x_test.ravel())

degrees = [1, 4, 15]  # underfit, good fit, overfit
n_trials = 20
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

for ax, degree in zip(axes, degrees):
    predictions = []
    for trial in range(n_trials):
        x_train, y_train = generate_dataset()
        model = make_pipeline(PolynomialFeatures(degree), LinearRegression())
        model.fit(x_train, y_train)
        preds = model.predict(x_test)
        predictions.append(preds)
        ax.plot(x_test, preds, alpha=0.15, color="blue")
    predictions = np.array(predictions)

    mean_prediction = predictions.mean(axis=0)
    bias_sq = np.mean((mean_prediction - y_test_true) ** 2)
    variance = np.mean(predictions.var(axis=0))

    ax.plot(x_test, y_test_true, color="black", linewidth=2, label="True function")
    ax.plot(x_test, mean_prediction, color="red", linewidth=2, label="Avg prediction")
    ax.set_title(f"Degree {degree}\nBias²≈{bias_sq:.3f}, Var≈{variance:.3f}")
    ax.legend(fontsize=8)

plt.tight_layout()
plt.savefig("bias_variance_tradeoff.png")
plt.close()

print("Degree 1 (underfit): high bias, low variance -> consistently wrong in the same way")
print("Degree 4 (good fit): balanced bias and variance")
print("Degree 15 (overfit): low bias, high variance -> wildly different predictions per training set")
```

## Exercise
1. Re-run the experiment with `n=10` (fewer training points) instead of 30 — how does variance change for the degree-15 model?
2. Add a degree-2 model to the comparison and report its bias²/variance — where does it fall relative to the other three?
3. In your own words, explain why adding more training data typically reduces variance but does NOT reduce bias.

## Key Takeaways
- Underfitting = high bias (model too simple to capture the pattern).
- Overfitting = high variance (model too sensitive to the specific training sample, including its noise).
- The "sweet spot" model minimizes total error (bias² + variance + irreducible noise) — this is exactly what cross-validation (module 06) helps you find in practice.
