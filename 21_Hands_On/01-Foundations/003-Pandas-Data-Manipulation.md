# 003 - Pandas Data Manipulation

## Concept
Pandas provides the `DataFrame`, a labeled, 2D table built on top of NumPy arrays. It's the standard tool for loading, cleaning, filtering, grouping, and reshaping tabular data before feeding it into a model.

## Why It Matters
Almost every real-world ML project (module 02 onward) starts with a messy CSV. Pandas fluency directly determines how fast you can go from raw data to a model-ready feature matrix.

## Hands-On

```python
import pandas as pd
import numpy as np

# 1. Creating a DataFrame
df = pd.DataFrame({
    "name": ["Alice", "Bob", "Carol", "Dave"],
    "age": [25, 32, 45, 29],
    "salary": [50000, 62000, 58000, np.nan],
    "department": ["Sales", "Eng", "Eng", "Sales"]
})
print(df.head())
print(df.info())
print(df.describe())

# 2. Selecting and filtering
print(df["age"])                      # single column -> Series
print(df[["name", "age"]])            # multiple columns
print(df[df["age"] > 28])             # boolean filter (rows)
print(df.loc[df["department"] == "Eng", "salary"])  # label-based selection

# 3. Adding / transforming columns
df["age_in_5_years"] = df["age"] + 5
df["salary_k"] = df["salary"] / 1000
df["name_upper"] = df["name"].str.upper()

# 4. Handling missing data (deep dive in module 02)
print(df["salary"].isna().sum())
df["salary_filled"] = df["salary"].fillna(df["salary"].mean())

# 5. Group-by aggregation - core for feature engineering
dept_stats = df.groupby("department")["salary"].agg(["mean", "count"])
print(dept_stats)

# 6. Merging datasets (like a SQL join)
bonuses = pd.DataFrame({
    "department": ["Sales", "Eng"],
    "bonus_pct": [0.05, 0.08]
})
merged = df.merge(bonuses, on="department", how="left")
print(merged)

# 7. Sorting and reshaping
print(df.sort_values("age", ascending=False))
pivot = df.pivot_table(values="salary", index="department", aggfunc="mean")
print(pivot)
```

## Exercise
1. Load any CSV of your choice with `pd.read_csv()` and print `.shape`, `.dtypes`, and `.isna().sum()`.
2. Create a new column that buckets `age` into `"young"` (< 30) and `"senior"` (>= 30) using `np.where` or `pd.cut`.
3. Group by `department` and compute both the mean and standard deviation of `salary` in one `.agg()` call.

## Key Takeaways
- `.loc` is label-based, `.iloc` is position-based — mixing them up is the #1 Pandas bug.
- `groupby` + `agg` is the pattern behind most engineered features (rolling averages, category stats).
- Always check `.isna().sum()` and `.dtypes` immediately after loading data — this feeds directly into module 02.
