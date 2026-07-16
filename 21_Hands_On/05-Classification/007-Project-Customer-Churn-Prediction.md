# 007 - Project: Customer Churn Prediction

## Concept
A full binary-classification project on mixed numeric/categorical business data: predicting whether a customer will churn (cancel their subscription). Covers encoding categorical variables (previewed here, formalized in module 07), handling class imbalance, and choosing the right evaluation metric.

## Why It Matters
Churn prediction is one of the most common applied ML problems in industry. It combines everything from modules 02, 04-06: cleaning, splitting, encoding, model comparison, and business-aware evaluation (the cost of missing a churner vs. a false alarm are rarely equal).

## Hands-On

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score, RocCurveDisplay
import matplotlib.pyplot as plt

# 1. Simulate a realistic churn dataset
np.random.seed(42)
n = 1000
df = pd.DataFrame({
    "tenure_months": np.random.randint(1, 72, n),
    "monthly_charges": np.random.normal(65, 20, n).clip(20, 150),
    "contract_type": np.random.choice(["Month-to-month", "One year", "Two year"], n, p=[0.5, 0.3, 0.2]),
    "support_calls": np.random.poisson(2, n),
    "payment_method": np.random.choice(["Credit card", "Bank transfer", "Electronic check"], n),
})
# churn probability driven by tenure, contract type, and support calls (realistic pattern)
churn_logit = (
    -0.05 * df["tenure_months"]
    + 0.02 * df["monthly_charges"]
    + 0.3 * df["support_calls"]
    + df["contract_type"].map({"Month-to-month": 1.5, "One year": 0.2, "Two year": -1.0})
)
churn_prob = 1 / (1 + np.exp(-(churn_logit - churn_logit.mean())))
df["churned"] = (np.random.uniform(0, 1, n) < churn_prob).astype(int)

print(df.head())
print("\nChurn rate:", df["churned"].mean())

# 2. Split
X = df.drop(columns=["churned"])
y = df["churned"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, stratify=y, random_state=42
)

# 3. Preprocessing pipeline - numeric scaling + categorical one-hot encoding
numeric_features = ["tenure_months", "monthly_charges", "support_calls"]
categorical_features = ["contract_type", "payment_method"]

preprocessor = ColumnTransformer([
    ("num", StandardScaler(), numeric_features),
    ("cat", OneHotEncoder(drop="first"), categorical_features),
])

# 4. Compare models using a consistent leakage-safe pipeline
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000, class_weight="balanced"),
    "Decision Tree": DecisionTreeClassifier(max_depth=5, class_weight="balanced", random_state=42),
    "Random Forest": RandomForestClassifier(n_estimators=200, class_weight="balanced", random_state=42),
}

print("\n--- 5-fold CV comparison (ROC-AUC) ---")
results = {}
for name, model in models.items():
    pipe = Pipeline([("prep", preprocessor), ("model", model)])
    scores = cross_val_score(pipe, X_train, y_train, cv=5, scoring="roc_auc")
    results[name] = scores.mean()
    print(f"{name:20s} -> {scores.mean():.4f} (+/- {scores.std():.4f})")

best_name = max(results, key=results.get)
print(f"\nBest model: {best_name}")

# 5. Fit final pipeline, evaluate on held-out test set
final_pipe = Pipeline([("prep", preprocessor), ("model", models[best_name])])
final_pipe.fit(X_train, y_train)
y_pred = final_pipe.predict(X_test)
y_proba = final_pipe.predict_proba(X_test)[:, 1]

print("\n", classification_report(y_test, y_pred, target_names=["stayed", "churned"]))
print("Test ROC-AUC:", roc_auc_score(y_test, y_proba))

# 6. ROC curve
RocCurveDisplay.from_predictions(y_test, y_proba)
plt.title("Churn Prediction ROC Curve")
plt.savefig("churn_roc_curve.png")
plt.close()

# 7. Feature importance (business insight, not just a metric)
if best_name == "Random Forest":
    feature_names = (numeric_features +
                      list(final_pipe.named_steps["prep"]
                           .named_transformers_["cat"].get_feature_names_out(categorical_features)))
    importances = final_pipe.named_steps["model"].feature_importances_
    importance_df = pd.DataFrame({"feature": feature_names, "importance": importances})
    print("\nTop drivers of churn:\n", importance_df.sort_values("importance", ascending=False).head())
```

## Exercise
1. Change `class_weight="balanced"` to `None` on the best model and compare recall for the churned class — explain the difference.
2. Add a business cost analysis: assume a false negative (missed churner) costs $200 and a false positive (unnecessary retention offer) costs $20 — compute total cost at different classification thresholds and find the cost-minimizing threshold.
3. Engineer one new feature (e.g., `charges_per_tenure_month = monthly_charges / tenure_months`) and check if it improves the best model's CV ROC-AUC.

## Key Takeaways
- `class_weight="balanced"` is a simple, effective first step for imbalanced classification, adjusting the loss to penalize minority-class errors more.
- `ColumnTransformer` + `Pipeline` is the standard sklearn pattern for cleanly combining different preprocessing per column type without leakage.
- For business problems, the "best" model isn't necessarily the one with highest accuracy — it's the one that minimizes real-world cost at the chosen decision threshold.
