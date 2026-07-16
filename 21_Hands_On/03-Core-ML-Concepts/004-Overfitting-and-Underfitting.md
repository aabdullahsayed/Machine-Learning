# 004 - Overfitting and Underfitting

## Concept
Overfitting: a model learns the training data too well, including its noise, and fails to generalize. Underfitting: a model is too simple to capture the underlying pattern, performing poorly on both train and test data. This lesson focuses on *detecting* and *diagnosing* these via learning curves.

## Why It Matters
Diagnosing over/underfitting correctly tells you what to do next: get more data, reduce model complexity, add regularization, or the opposite. Misdiagnosing wastes enormous amounts of time.

## Hands-On

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import learning_curve, train_test_split
from sklearn.metrics import mean_squared_error

np.random.seed(0)
X = np.random.uniform(0, 10, 300).reshape(-1, 1)
y = np.sin(X).ravel() + np.random.normal(0, 0.3, 300)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 1. Underfitting example - a tree that's too shallow
underfit_model = DecisionTreeRegressor(max_depth=1, random_state=42)
underfit_model.fit(X_train, y_train)
train_mse_under = mean_squared_error(y_train, underfit_model.predict(X_train))
test_mse_under = mean_squared_error(y_test, underfit_model.predict(X_test))
print(f"Underfit  -> Train MSE: {train_mse_under:.4f}, Test MSE: {test_mse_under:.4f}")
print("  Both errors are HIGH and similar -> classic underfitting signature.")

# 2. Overfitting example - a tree with no depth limit
overfit_model = DecisionTreeRegressor(max_depth=None, random_state=42)
overfit_model.fit(X_train, y_train)
train_mse_over = mean_squared_error(y_train, overfit_model.predict(X_train))
test_mse_over = mean_squared_error(y_test, overfit_model.predict(X_test))
print(f"\nOverfit   -> Train MSE: {train_mse_over:.4f}, Test MSE: {test_mse_over:.4f}")
print("  Train error is near-zero but test error is much higher -> classic overfitting signature.")

# 3. Good fit example - a reasonably constrained tree
good_model = DecisionTreeRegressor(max_depth=4, random_state=42)
good_model.fit(X_train, y_train)
train_mse_good = mean_squared_error(y_train, good_model.predict(X_train))
test_mse_good = mean_squared_error(y_test, good_model.predict(X_test))
print(f"\nGood fit  -> Train MSE: {train_mse_good:.4f}, Test MSE: {test_mse_good:.4f}")
print("  Both errors are low and close together -> good generalization.")

# 4. Learning curves - the definitive diagnostic tool: plot error vs
# training-set size to see whether more data would help
train_sizes, train_scores, val_scores = learning_curve(
    DecisionTreeRegressor(max_depth=None, random_state=42),
    X, y, cv=5, scoring="neg_mean_squared_error",
    train_sizes=np.linspace(0.1, 1.0, 10)
)
train_errors = -train_scores.mean(axis=1)
val_errors = -val_scores.mean(axis=1)

plt.figure(figsize=(7, 5))
plt.plot(train_sizes, train_errors, "o-", label="Training error")
plt.plot(train_sizes, val_errors, "o-", label="Validation error")
plt.xlabel("Training set size")
plt.ylabel("MSE")
plt.title("Learning Curve (unconstrained tree -> overfitting pattern)")
plt.legend()
plt.savefig("learning_curve.png")
plt.close()
print("\nLearning curve saved. A large, non-shrinking GAP between train/val "
      "error as data grows confirms overfitting.")
```

## Exercise
1. Generate a learning curve for the `max_depth=1` (underfit) model and describe how its shape differs from the overfit model's curve.
2. Sweep `max_depth` from 1 to 15 and plot train/test MSE vs depth — identify the depth where test error starts increasing again (the overfitting "elbow").
3. Explain, using the learning curve concept, why "just collect more data" fixes high variance problems but does NOT fix high bias problems.

## Key Takeaways
- Underfitting signature: high error on both train and test, close together.
- Overfitting signature: near-zero train error, much higher test error — a large gap.
- Learning curves that converge to a low, shared error as data grows indicate a well-specified model; curves with a persistent gap indicate you need regularization (module 04) or a simpler model.
