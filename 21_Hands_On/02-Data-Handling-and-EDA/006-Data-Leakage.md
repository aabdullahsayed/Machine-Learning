# 006 - Data Leakage

## Concept
Data leakage happens when information from outside the training dataset — often information that wouldn't be available at prediction time — is used to build the model. It's the single most common cause of models that look great in validation but fail in production.

## Why It Matters
Leakage silently inflates every metric in module 06. Catching it requires understanding not just the code, but the *business/temporal logic* of when each feature would actually be known.

## Hands-On

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

np.random.seed(0)
n = 1000

# Simulate a loan default dataset
df = pd.DataFrame({
    "income": np.random.normal(55000, 15000, n),
    "credit_score": np.random.normal(650, 80, n),
    "loan_amount": np.random.normal(20000, 5000, n),
})
# True underlying relationship
risk_score = (-0.00002 * df["income"] - 0.01 * df["credit_score"]
              + 0.00005 * df["loan_amount"])
df["defaulted"] = (risk_score + np.random.normal(0, 1, n) > risk_score.mean()).astype(int)

# LEAKY FEATURE EXAMPLE: "collections_flag" is only set AFTER a customer
# defaults, so it perfectly encodes the target - a classic leakage bug
df["collections_flag"] = df["defaulted"]  # (in real life this bug is much subtler!)

X_leaky = df[["income", "credit_score", "loan_amount", "collections_flag"]]
X_clean = df[["income", "credit_score", "loan_amount"]]
y = df["defaulted"]

def evaluate(X, y, label):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )
    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)
    model = LogisticRegression()
    model.fit(X_train_s, y_train)
    preds = model.predict(X_test_s)
    acc = accuracy_score(y_test, preds)
    print(f"{label} accuracy: {acc:.4f}")
    return acc

print("--- Leakage demonstration ---")
evaluate(X_leaky, y, "WITH leaky feature (collections_flag)")
evaluate(X_clean, y, "WITHOUT leaky feature")

# ANOTHER COMMON LEAKAGE PATTERN: scaling/imputing on the full dataset
# before splitting (covered in file 005) - repeated here for emphasis
scaler = StandardScaler()
X_all_scaled = scaler.fit_transform(X_clean)  # WRONG: sees test data statistics
print("\nWARNING: fitting scaler before split leaks test-set distribution info "
      "into training, subtly inflating validation performance.")

# A THIRD PATTERN: target leakage via aggregated features computed using
# the whole dataset (e.g., "average default rate per region" computed
# BEFORE the split, using test-set rows too)
df["region"] = np.random.choice(["A", "B", "C"], n)
leaky_region_avg = df.groupby("region")["defaulted"].transform("mean")  # WRONG
print("\nLeaky groupby-based feature (computed on full data) example created.")
print("Fix: compute group statistics using ONLY the training fold, "
      "then map them onto validation/test.")
```

## Exercise
1. Identify which of these features would be leaky for a "will this customer churn next month" model, and explain why: `days_since_last_login`, `cancellation_request_submitted`, `total_lifetime_purchases`, `support_ticket_closed_reason`.
2. Rewrite the `leaky_region_avg` example correctly: compute the mean target-per-region using only `X_train`/`y_train`, then map those means onto both train and test sets.
3. Build a small `sklearn.pipeline.Pipeline` combining `StandardScaler` and `LogisticRegression`, and explain (in a comment) why using a `Pipeline` with cross-validation automatically avoids leakage that manual scaling doesn't.

## Key Takeaways
- Ask of every feature: "Would I know this value at the moment I need to make the prediction?" If not, it's leakage.
- Fit ALL preprocessing (scalers, encoders, target-encoders, imputers) only on the training fold — every time, including inside cross-validation loops.
- `sklearn.pipeline.Pipeline` + `cross_val_score` is the safest way to guarantee no leakage across folds.
