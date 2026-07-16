# 004 - Regularization: Ridge and Lasso

## Concept
Regularization adds a penalty term to the loss function that discourages large coefficients, reducing overfitting. **Ridge (L2)** penalizes the sum of squared coefficients; **Lasso (L1)** penalizes the sum of absolute coefficients and can shrink some coefficients to exactly zero (automatic feature selection). **Elastic Net** blends both.

## Why It Matters
Regularization is the standard tool for controlling model complexity, directly addressing the high-variance side of the bias-variance tradeoff (module 03, file 003), and connects back to the L1/L2 norms from module 01, file 005.

## Hands-On

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

np.random.seed(0)
n, n_features = 50, 20  # more features than ideal -> prone to overfitting
X = np.random.randn(n, n_features)
# only the first 3 features actually matter
true_coefs = np.array([5, -3, 2] + [0] * (n_features - 3))
y = X @ true_coefs + np.random.normal(0, 1, n)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)

# 1. Plain linear regression - likely overfits with 20 features, 35 samples
lr = LinearRegression().fit(X_train_s, y_train)
print("Linear -> Test MSE:", mean_squared_error(y_test, lr.predict(X_test_s)))
print("  # near-zero coefs:", np.sum(np.abs(lr.coef_) < 0.1))

# 2. Ridge (L2) - shrinks all coefficients smoothly toward zero, rarely exactly zero
ridge = Ridge(alpha=1.0).fit(X_train_s, y_train)
print("\nRidge  -> Test MSE:", mean_squared_error(y_test, ridge.predict(X_test_s)))
print("  # near-zero coefs:", np.sum(np.abs(ridge.coef_) < 0.1))

# 3. Lasso (L1) - can zero out irrelevant features entirely -> built-in feature selection
lasso = Lasso(alpha=0.1).fit(X_train_s, y_train)
print("\nLasso  -> Test MSE:", mean_squared_error(y_test, lasso.predict(X_test_s)))
print("  # exactly-zero coefs:", np.sum(lasso.coef_ == 0), "out of", n_features)
print("  Nonzero coef indices:", np.nonzero(lasso.coef_)[0], "(true relevant: [0, 1, 2])")

# 4. Elastic Net - combination of L1 and L2
elastic = ElasticNet(alpha=0.1, l1_ratio=0.5).fit(X_train_s, y_train)
print("\nElasticNet -> Test MSE:", mean_squared_error(y_test, elastic.predict(X_test_s)))

# 5. Effect of alpha (regularization strength) - the key hyperparameter
alphas = np.logspace(-3, 2, 30)
ridge_coefs, lasso_coefs = [], []
for alpha in alphas:
    ridge_coefs.append(Ridge(alpha=alpha).fit(X_train_s, y_train).coef_)
    lasso_coefs.append(Lasso(alpha=alpha, max_iter=5000).fit(X_train_s, y_train).coef_)

ridge_coefs, lasso_coefs = np.array(ridge_coefs), np.array(lasso_coefs)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].plot(alphas, ridge_coefs)
axes[0].set_xscale("log")
axes[0].set_title("Ridge: Coefficients shrink smoothly")
axes[0].set_xlabel("alpha")
axes[1].plot(alphas, lasso_coefs)
axes[1].set_xscale("log")
axes[1].set_title("Lasso: Coefficients hit exactly zero")
axes[1].set_xlabel("alpha")
plt.tight_layout()
plt.savefig("ridge_lasso_paths.png")
plt.close()
```

## Exercise
1. Use `RidgeCV` and `LassoCV` (built-in cross-validated alpha selection) to automatically find the best `alpha` for this dataset.
2. Increase `n_features` to 100 with the same 3 relevant features — how does Lasso's feature-selection behavior change?
3. Explain geometrically (in your own words, referencing L1 vs L2 norm shapes from module 01) why Lasso produces exact zeros while Ridge does not.

## Key Takeaways
- Ridge is the default choice when you believe most features are somewhat relevant; it stabilizes coefficients without eliminating features.
- Lasso is preferred when you suspect many features are irrelevant, since it performs automatic feature selection.
- The regularization strength (`alpha`) should always be chosen via cross-validation (module 06), never guessed.
