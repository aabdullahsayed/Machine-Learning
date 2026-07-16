# 002 - Encoding Categorical Variables

## Concept
Most ML algorithms require numeric input, so categorical (text-label) features must be encoded. **One-Hot Encoding** creates a binary column per category; **Label Encoding** assigns an integer per category (implies ordering — use carefully); **Target/Mean Encoding** replaces a category with the mean target value for that category (powerful but leakage-prone).

## Why It Matters
Choosing the wrong encoding can either explode dimensionality (too many one-hot columns), imply false ordinal relationships, or leak target information — this expands on the `OneHotEncoder` used in module 05, file 007.

## Hands-On

```python
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, OrdinalEncoder
from sklearn.model_selection import train_test_split, KFold

df = pd.DataFrame({
    "color": ["red", "blue", "green", "blue", "red", "green", "red"],
    "size": ["S", "M", "L", "M", "S", "L", "XL"],  # has a natural order!
    "city": ["NYC", "LA", "Chicago", "NYC", "LA", "NYC", "Chicago"],
    "target": [10, 20, 15, 22, 12, 18, 25],
})

# 1. One-Hot Encoding - no false ordering, but adds one column per category
ohe = OneHotEncoder(sparse_output=False, drop="first")  # drop first to avoid redundancy
color_encoded = ohe.fit_transform(df[["color"]])
color_cols = ohe.get_feature_names_out(["color"])
print("One-hot encoded 'color':\n", pd.DataFrame(color_encoded, columns=color_cols))
print("\nUse for: NOMINAL categories with no inherent order (color, city).")

# 2. Ordinal Encoding - preserves a MEANINGFUL order (only use when order exists!)
size_order = [["S", "M", "L", "XL"]]
ordinal = OrdinalEncoder(categories=size_order)
size_encoded = ordinal.fit_transform(df[["size"]])
print("\nOrdinal encoded 'size' (S=0, M=1, L=2, XL=3):\n", size_encoded.ravel())
print("Use for: ORDINAL categories with true order (size, education level, ratings).")

# 3. Plain LabelEncoder - DANGEROUS for nominal features fed to linear/distance
# models, since it implies a false numeric order; fine for tree-based models
# or for encoding the TARGET variable in classification
le = LabelEncoder()
city_labels = le.fit_transform(df["city"])
print("\nLabelEncoder on 'city' (WARNING - implies false ordering: "
      f"{dict(zip(le.classes_, range(len(le.classes_))))})")
print("A linear model would now (wrongly) treat 'NYC' > 'LA' numerically.")

# 4. Target (mean) encoding - replaces category with its mean target value;
# very powerful for high-cardinality features, but HIGH leakage risk if
# computed on the full dataset (module 02, file 006)
X_train, X_test, y_train, y_test = train_test_split(
    df[["city"]], df["target"], test_size=0.3, random_state=42
)
train_df = X_train.copy()
train_df["target"] = y_train
city_means = train_df.groupby("city")["target"].mean()
print("\nTarget means computed from TRAINING data only:\n", city_means)

X_train_encoded = X_train["city"].map(city_means)
# for test data, unseen categories need a fallback (global mean)
global_mean = y_train.mean()
X_test_encoded = X_test["city"].map(city_means).fillna(global_mean)
print("Encoded test set 'city' values:\n", X_test_encoded)

# 5. SAFER target encoding via K-Fold to avoid leakage within the training set
def kfold_target_encode(df, col, target_col, n_splits=5):
    df = df.copy()
    df["encoded"] = np.nan
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)
    for train_idx, val_idx in kf.split(df):
        fold_means = df.iloc[train_idx].groupby(col)[target_col].mean()
        df.loc[df.index[val_idx], "encoded"] = df.iloc[val_idx][col].map(fold_means)
    df["encoded"] = df["encoded"].fillna(df[target_col].mean())
    return df["encoded"]

df["city_target_encoded_safe"] = kfold_target_encode(df, "city", "target")
print("\nLeakage-safe K-Fold target encoding:\n", df[["city", "target", "city_target_encoded_safe"]])

# 6. High-cardinality categorical - when one-hot creates too many columns
high_card = pd.Series([f"user_{i}" for i in range(1000)])
print(f"\nOne-hot encoding {high_card.nunique()} unique users would create "
      f"{high_card.nunique()} columns - consider target encoding or hashing instead.")
```

## Exercise
1. One-hot encode the `city` column and compare model performance (using a simple `LinearRegression` on `target`) against the leakage-safe target-encoded version.
2. Explain, for a `day_of_week` feature, whether One-Hot or Ordinal encoding is more appropriate, and why.
3. Implement `OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)` to gracefully handle a category seen at test time but not at train time.

## Key Takeaways
- Use One-Hot for nominal (unordered) categories, Ordinal for genuinely ordered categories, and be very cautious with plain LabelEncoder outside of tree models.
- Target encoding is powerful for high-cardinality features but must be computed with proper cross-fold isolation to avoid leakage.
- Always plan for unseen categories at prediction time — they will happen in production.
