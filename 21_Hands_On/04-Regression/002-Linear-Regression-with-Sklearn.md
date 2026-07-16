# 002 - Linear Regression with Scikit-Learn

## Concept
Scikit-learn provides a production-grade, optimized `LinearRegression` estimator following the consistent `fit`/`predict` API used across the entire library. This lesson focuses on the practical workflow: preprocessing, fitting, evaluating, and interpreting coefficients.

## Why It Matters
This `fit`/`predict`/`score` pattern is identical across every sklearn model you'll use in modules 04-09 — learning it once here pays off for the rest of the course.

## Hands-On

```python
import numpy as np
import pandas as pd
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

# 1. Load a real dataset
housing = fetch_california_housing(as_frame=True)
df = housing.frame
print(df.head())
print(df.describe())

X = df.drop(columns=["MedHouseVal"])
y = df["MedHouseVal"]

# 2. Split (module 02, file 005)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Scale features (important for interpreting coefficient magnitudes fairly)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 4. Fit
model = LinearRegression()
model.fit(X_train_scaled, y_train)

# 5. Predict & evaluate
y_pred = model.predict(X_test_scaled)
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"\nMSE: {mse:.4f}, MAE: {mae:.4f}, R²: {r2:.4f}")

# 6. Interpret coefficients (only meaningful because features were scaled)
coef_df = pd.DataFrame({
    "feature": X.columns,
    "coefficient": model.coef_
}).sort_values("coefficient", key=abs, ascending=False)
print("\nFeature importance (by coefficient magnitude):\n", coef_df)

# 7. Residual analysis - errors should look like random noise, not a pattern
residuals = y_test - y_pred
import matplotlib.pyplot as plt
plt.figure(figsize=(6, 4))
plt.scatter(y_pred, residuals, alpha=0.3)
plt.axhline(0, color="red", linestyle="--")
plt.xlabel("Predicted values")
plt.ylabel("Residuals")
plt.title("Residual Plot")
plt.savefig("residual_plot.png")
plt.close()

# A funnel/curve shape in residuals suggests the linear model is misspecified
# (missing nonlinearity, module 003) or needs a variance-stabilizing transform.
```

## Exercise
1. Add polynomial features of degree 2 for just the `MedInc` column and re-fit — does R² improve? (Preview of file 003.)
2. Compare `LinearRegression`'s test R² against a naive "always predict the mean" baseline (`DummyRegressor`) to confirm the model is adding real value.
3. Plot predicted vs. actual values as a scatter plot with a diagonal reference line (`y=x`) — a perfect model would place all points exactly on that line.

## Key Takeaways
- Scaling features before fitting makes coefficients comparable in magnitude — critical for interpretation, though not required for `LinearRegression`'s predictions themselves.
- R² measures the proportion of variance explained; it's not the whole story — always pair it with a residual plot.
- The `fit → predict → score` pattern here is identical for every sklearn regressor and classifier in this course.
