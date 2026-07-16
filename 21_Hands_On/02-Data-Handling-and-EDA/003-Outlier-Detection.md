# 003 - Outlier Detection

## Concept
Outliers are data points that deviate significantly from the rest. They can be genuine rare events, data-entry errors, or measurement issues. This lesson covers statistical (Z-score, IQR) and model-based (Isolation Forest) detection methods.

## Why It Matters
Outliers can dominate loss functions (especially MSE-based ones — see module 04), distort feature scaling, and mislead distance-based algorithms like KNN (module 05) and K-Means (module 08).

## Hands-On

```python
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

np.random.seed(0)
normal_data = np.random.normal(50, 10, 200)
outliers = np.array([150, -30, 200, 5, -50])  # injected anomalies
data = np.concatenate([normal_data, outliers])
df = pd.DataFrame({"value": data})

# 1. Z-score method - flags points > N standard deviations from the mean
mean, std = df["value"].mean(), df["value"].std()
df["z_score"] = (df["value"] - mean) / std
z_outliers = df[df["z_score"].abs() > 3]
print("Z-score outliers:\n", z_outliers)

# 2. IQR (Interquartile Range) method - robust to extreme values since it
# uses quartiles instead of mean/std
Q1 = df["value"].quantile(0.25)
Q3 = df["value"].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
iqr_outliers = df[(df["value"] < lower_bound) | (df["value"] > upper_bound)]
print(f"\nIQR bounds: [{lower_bound:.2f}, {upper_bound:.2f}]")
print("IQR outliers:\n", iqr_outliers)

# 3. Isolation Forest - a model-based approach that isolates anomalies via
# random partitioning; works well in higher dimensions where IQR/Z-score
# per-column checks miss multivariate outliers
iso_forest = IsolationForest(contamination=0.05, random_state=42)
df["anomaly"] = iso_forest.fit_predict(df[["value"]])  # -1 = outlier, 1 = normal
print("\nIsolation Forest flagged:\n", df[df["anomaly"] == -1])

# 4. Handling detected outliers - three common strategies
# (a) Remove them
df_removed = df[df["z_score"].abs() <= 3]

# (b) Cap them (Winsorization)
df["value_capped"] = df["value"].clip(lower=lower_bound, upper=upper_bound)

# (c) Log-transform to reduce the influence of extreme values
df["value_log"] = np.log1p(df["value"] - df["value"].min() + 1)

print("\nOriginal std:", df["value"].std())
print("Capped std:", df["value_capped"].std())
```

## Exercise
1. Apply the Z-score and IQR methods to a real column (e.g., `income` from module 02's file 002) and compare how many outliers each method flags.
2. Run `IsolationForest` on a 2D dataset (two numeric columns) and visualize flagged points with a scatter plot colored by `anomaly`.
3. For a skewed distribution (e.g., `np.random.exponential`), compare Z-score outlier detection results before and after a log transform.

## Key Takeaways
- Z-score assumes roughly normal data; it performs poorly on skewed distributions.
- IQR is more robust and is the standard method behind box plots (module 01, file 004).
- Isolation Forest generalizes to multivariate outliers that univariate methods can't catch — useful before clustering (module 08) or fraud detection tasks.
