# 005 - Data Splitting: Train / Validation / Test

## Concept
To estimate how a model will perform on unseen data, you split your dataset into three parts: **train** (fit the model), **validation** (tune hyperparameters), and **test** (final, untouched evaluation). This lesson also covers stratified splitting and time-based splitting.

## Why It Matters
Every metric you report later (module 06) is only trustworthy if the split was done correctly. This is the single most common source of overly optimistic ("too good to be true") results in beginner ML projects.

## Hands-On

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

np.random.seed(0)
n = 1000
df = pd.DataFrame({
    "feature1": np.random.randn(n),
    "feature2": np.random.randn(n),
    "target": np.random.choice([0, 1], n, p=[0.9, 0.1]),  # imbalanced
    "date": pd.date_range("2023-01-01", periods=n, freq="D"),
})

X = df[["feature1", "feature2"]]
y = df["target"]

# 1. Basic random split (70% train, 30% test)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)
print("Train:", X_train.shape, "Test:", X_test.shape)

# 2. Three-way split: train / validation / test
X_train, X_temp, y_train, y_temp = train_test_split(
    X, y, test_size=0.3, random_state=42
)
X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size=0.5, random_state=42
)
print(f"Train: {X_train.shape[0]}, Val: {X_val.shape[0]}, Test: {X_test.shape[0]}")

# 3. Stratified split - preserves class proportions, crucial for imbalanced data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, stratify=y, random_state=42
)
print("\nOriginal class balance:\n", y.value_counts(normalize=True))
print("Train class balance:\n", y_train.value_counts(normalize=True))
print("Test class balance:\n", y_test.value_counts(normalize=True))

# 4. Time-based split - required when data has a temporal order (e.g., time
# series, module 12), since randomly shuffling would leak future info into
# the training set
df_sorted = df.sort_values("date")
split_idx = int(len(df_sorted) * 0.8)
train_time = df_sorted.iloc[:split_idx]
test_time = df_sorted.iloc[split_idx:]
print(f"\nTime split -> Train ends: {train_time['date'].max()}, "
      f"Test starts: {test_time['date'].min()}")

# 5. Why the test set must stay untouched - a demonstration of the danger
# of "peeking": fitting a scaler on the FULL dataset before splitting leaks
# information from test into train
from sklearn.preprocessing import StandardScaler

# WRONG: fit on all data, then split
scaler_wrong = StandardScaler()
X_scaled_wrong = scaler_wrong.fit_transform(X)  # sees test set statistics!

# RIGHT: split first, fit scaler only on train, then transform both
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
scaler_right = StandardScaler()
X_train_scaled = scaler_right.fit_transform(X_train)   # fit only on train
X_test_scaled = scaler_right.transform(X_test)          # transform test using train stats
print("\nCorrect scaling: scaler fit only on training data.")
```

## Exercise
1. Split a dataset three ways (train/val/test) with a 60/20/20 ratio and confirm the sizes add up correctly.
2. Take a heavily imbalanced dataset (95/5 split) and compare class proportions with and without `stratify=y`.
3. Simulate a time-series dataset and show, with a concrete example, why a random split would leak future information (hint: think about what a lag feature would contain).

## Key Takeaways
- Always fit preprocessing objects (scalers, encoders, imputers) on the training set only, then apply (`.transform()`) to validation/test — this prevents data leakage (module 02, file 006).
- Use `stratify=y` for classification tasks with imbalance, always.
- Time-ordered data needs a time-based split, never a random shuffle.
