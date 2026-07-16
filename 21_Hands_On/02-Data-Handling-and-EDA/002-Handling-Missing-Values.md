# 002 - Handling Missing Values

## Concept
Missing data isn't just an annoyance — the *pattern* of missingness matters. Data can be Missing Completely At Random (MCAR), Missing At Random (MAR), or Missing Not At Random (MNAR), and the right strategy (drop, impute, or flag) depends on which applies.

## Why It Matters
Naively dropping or filling missing values can introduce bias or destroy signal. This directly affects model performance and is a frequent hidden cause of poor results.

## Hands-On

```python
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer, KNNImputer

df = pd.DataFrame({
    "age": [25, np.nan, 45, 29, np.nan, 38],
    "income": [50000, 62000, np.nan, 48000, 71000, np.nan],
    "department": ["Sales", "Eng", "Eng", np.nan, "Sales", "Eng"],
})

# 1. Quantify missingness
print(df.isna().sum())
print(df.isna().mean() * 100, "% missing per column")

# 2. Visual pattern check (via a simple heatmap-style print)
print(df.isna())

# 3. Strategy A: Drop rows with any missing value (only safe if missingness is rare)
df_dropped = df.dropna()
print("\nDropped shape:", df_dropped.shape, "vs original:", df.shape)

# 4. Strategy B: Drop columns with too much missingness (e.g., > 50%)
threshold = 0.5
df_col_dropped = df.loc[:, df.isna().mean() < threshold]

# 5. Strategy C: Simple imputation (mean/median/mode)
num_imputer = SimpleImputer(strategy="median")
df["age_imputed"] = num_imputer.fit_transform(df[["age"]])

cat_imputer = SimpleImputer(strategy="most_frequent")
df["department_imputed"] = cat_imputer.fit_transform(df[["department"]]).ravel()

# 6. Strategy D: KNN imputation - uses similar rows to fill gaps, often better
# than simple mean/median because it preserves relationships between features
knn_imputer = KNNImputer(n_neighbors=2)
numeric_cols = ["age", "income"]
df_knn = pd.DataFrame(knn_imputer.fit_transform(df[numeric_cols]), columns=numeric_cols)
print("\nKNN-imputed numeric columns:\n", df_knn)

# 7. Strategy E: Add a "missingness flag" - sometimes the fact that data is
# missing is itself predictive (e.g., income missing might correlate with unemployment)
df["income_was_missing"] = df["income"].isna().astype(int)

print("\nFinal DataFrame:\n", df)
```

## Exercise
1. Create a dataset with 20% missing values in one column. Compare the resulting mean before and after mean-imputation — does it change? Why does mean imputation preserve the overall mean but distort variance?
2. Use `KNNImputer` with `n_neighbors=3` vs `n_neighbors=1` on the same data. How different are the results?
3. Build a small pipeline where you add missingness flags for every column with any missing value, then verify the flag columns correctly match `.isna()`.

## Key Takeaways
- Mean/median imputation is simple but shrinks variance and can dilute signal — use with caution on features that matter a lot.
- KNN or model-based imputation generally preserves relationships between features better than simple imputation.
- A "missingness flag" column can capture predictive signal that a filled-in value would otherwise hide — always consider adding one before dropping the missing info entirely.
