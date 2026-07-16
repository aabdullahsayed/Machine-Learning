# 001 - Feature Scaling

## Concept
Feature scaling transforms numeric features to a common range or distribution. **StandardScaler** (zero mean, unit variance), **MinMaxScaler** (scales to [0,1]), and **RobustScaler** (uses median/IQR, resistant to outliers) are the three most common approaches.

## Why It Matters
Distance-based (KNN, SVM, K-Means) and gradient-based (linear/logistic regression, neural networks) algorithms are all sensitive to feature scale — this directly extends the KNN scaling demo from module 05, file 002.

## Hands-On

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

np.random.seed(0)
df = pd.DataFrame({
    "age": np.random.normal(40, 12, 200),
    "income": np.random.lognormal(mean=10.5, sigma=0.6, size=200),  # skewed, has outliers
    "credit_score": np.random.normal(650, 80, 200),
})
df.loc[0, "income"] = 5_000_000  # inject an extreme outlier

# 1. StandardScaler - (x - mean) / std, assumes roughly normal-ish data
standard_scaler = StandardScaler()
df_standard = pd.DataFrame(standard_scaler.fit_transform(df), columns=df.columns)
print("StandardScaler stats:\n", df_standard.describe().loc[["mean", "std"]])

# 2. MinMaxScaler - (x - min) / (max - min), squashes to [0, 1]
minmax_scaler = MinMaxScaler()
df_minmax = pd.DataFrame(minmax_scaler.fit_transform(df), columns=df.columns)
print("\nMinMaxScaler stats:\n", df_minmax.describe().loc[["min", "max"]])
print("WARNING: the outlier in 'income' compresses ALL other values toward 0!")
print(df_minmax["income"].describe())

# 3. RobustScaler - (x - median) / IQR, resistant to the outlier
robust_scaler = RobustScaler()
df_robust = pd.DataFrame(robust_scaler.fit_transform(df), columns=df.columns)
print("\nRobustScaler stats (median, IQR-based):\n", df_robust.describe().loc[["50%"]])

# 4. Visual comparison
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
axes[0].hist(df["income"], bins=30)
axes[0].set_title("Original income (with outlier)")
axes[1].hist(df_minmax["income"], bins=30)
axes[1].set_title("MinMax scaled\n(outlier compresses everything else)")
axes[2].hist(df_robust["income"], bins=30)
axes[2].set_title("Robust scaled\n(outlier isolated, rest preserved)")
plt.tight_layout()
plt.savefig("scaling_comparison.png")
plt.close()

# 5. CRITICAL: fit scaler on train only, apply to test (module 02, file 006)
from sklearn.model_selection import train_test_split
X = df.drop(columns=[])
X_train, X_test = train_test_split(X, test_size=0.3, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)  # learns mean/std from train ONLY
X_test_scaled = scaler.transform(X_test)         # applies train's mean/std to test
print(f"\nScaler learned mean: {scaler.mean_}")
print("Applying the SAME mean/std to test data (never re-fitting) avoids leakage.")

# 6. Which algorithms need scaling vs which don't
print("""
NEEDS scaling: KNN, SVM, Logistic/Linear Regression (for regularization to be
  fair across features), Neural Networks, K-Means, PCA.
Does NOT strictly need scaling: Decision Trees, Random Forests, Gradient
  Boosting - tree-based splits are scale-invariant (a split at x > 5 works
  the same whether x is in dollars or thousands of dollars).
""")
```

## Exercise
1. Apply all three scalers to a feature with a single extreme outlier and compare the resulting range/distribution for the 99% "normal" data points.
2. Confirm empirically that a `DecisionTreeClassifier`'s accuracy is identical whether trained on scaled or unscaled features (unlike `KNeighborsClassifier` from module 05).
3. Write a `ColumnTransformer` (module 05, file 007 pattern) that applies `RobustScaler` to skewed columns and `StandardScaler` to normally distributed columns.

## Key Takeaways
- MinMaxScaler is very sensitive to outliers since it uses min/max directly; RobustScaler is the safer default when outliers are present.
- Always fit scalers on training data only, then `.transform()` (never re-`.fit()`) on validation/test data.
- Tree-based models (module 05, file 003; module 09) generally don't need feature scaling at all.
