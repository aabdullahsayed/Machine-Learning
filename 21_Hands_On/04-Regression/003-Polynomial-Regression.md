# 003 - Polynomial Regression

## Concept
Polynomial regression extends linear regression by adding polynomial terms (x², x³, ...) as new features, allowing a "linear" model (linear in its coefficients) to fit nonlinear relationships.

## Why It Matters
It's the simplest bridge from linear models to nonlinear pattern-fitting, and a direct, concrete illustration of the bias-variance tradeoff (module 03, file 003) via the `degree` hyperparameter.

## Hands-On

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

np.random.seed(0)
X = np.random.uniform(-3, 3, 100)
y = 0.5 * X**3 - X**2 + 2 * X + np.random.normal(0, 3, 100)  # true cubic relationship
X = X.reshape(-1, 1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 1. Plain linear regression (degree 1) - will underfit this cubic pattern
linear_model = LinearRegression()
linear_model.fit(X_train, y_train)
linear_test_mse = mean_squared_error(y_test, linear_model.predict(X_test))

# 2. Polynomial features - manually inspect what gets created
poly = PolynomialFeatures(degree=3, include_bias=False)
X_poly_sample = poly.fit_transform(X_train[:3])
print("Original feature:\n", X_train[:3])
print("Polynomial features (x, x^2, x^3):\n", X_poly_sample)

# 3. Fit polynomial models of increasing degree, compare fit quality
degrees = [1, 2, 3, 6, 15]
results = []
x_plot = np.linspace(-3, 3, 200).reshape(-1, 1)

plt.figure(figsize=(8, 6))
plt.scatter(X_train, y_train, alpha=0.4, label="Train data", color="gray")

for degree in degrees:
    model = make_pipeline(PolynomialFeatures(degree), LinearRegression())
    model.fit(X_train, y_train)
    train_mse = mean_squared_error(y_train, model.predict(X_train))
    test_mse = mean_squared_error(y_test, model.predict(X_test))
    results.append((degree, train_mse, test_mse))
    plt.plot(x_plot, model.predict(x_plot), label=f"Degree {degree}")

plt.ylim(y.min() - 5, y.max() + 5)
plt.legend()
plt.title("Polynomial Regression - Varying Degree")
plt.savefig("polynomial_regression_degrees.png")
plt.close()

print("\nDegree | Train MSE | Test MSE")
for degree, train_mse, test_mse in results:
    print(f"{degree:6d} | {train_mse:9.2f} | {test_mse:8.2f}")
print("\nNotice: as degree increases, train MSE keeps dropping, but test MSE "
      "eventually rises again -> classic overfitting (module 03, file 004).")
```

## Exercise
1. Find the degree that minimizes test MSE for this dataset using a simple loop over `degrees = range(1, 16)`.
2. Repeat the experiment with a smaller training set (`n=20`) — at what degree does overfitting become severe now compared to `n=100`?
3. Combine `PolynomialFeatures(degree=3)` with `Ridge` regression (file 004) and observe whether regularization tames the degree-15 model's overfitting.

## Key Takeaways
- Polynomial regression is still a *linear* model — linear in the transformed feature space — which is why `LinearRegression` still works after `PolynomialFeatures`.
- Higher polynomial degree = higher model capacity = more prone to overfitting, especially with limited data.
- Always pick the polynomial degree using validation performance, never training performance alone.
