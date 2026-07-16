# 004 - Capstone: Kaggle Competition Walkthrough

## Concept
A simplified, beginner-friendly walkthrough of how to approach any Kaggle competition, using the classic Titanic dataset as the running example: understand the problem → explore the data → engineer a few features → train and validate → submit.

## Why It Matters
Kaggle competitions are how most people practice applied ML after finishing a course. Knowing the standard workflow removes the "where do I even start" paralysis.

## Hands-On

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score, KFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# --- Step 1: Load train/test (simulated Titanic-style structure) ---
# In a real competition you'd do: train = pd.read_csv("train.csv")
np.random.seed(42)
n = 400
train = pd.DataFrame({
    "PassengerId": range(1, n + 1),
    "Pclass": np.random.choice([1, 2, 3], n, p=[0.2, 0.3, 0.5]),
    "Sex": np.random.choice(["male", "female"], n),
    "Age": np.random.normal(30, 12, n).clip(1, 80),
    "Fare": np.random.exponential(30, n),
    "SibSp": np.random.choice([0, 1, 2, 3], n, p=[0.6, 0.25, 0.1, 0.05]),
})
# Simulate a survival pattern: women and 1st class more likely to survive
survive_prob = 0.2 + 0.4*(train["Sex"]=="female") + 0.2*(train["Pclass"]==1)
train["Survived"] = (np.random.rand(n) < survive_prob).astype(int)

# --- Step 2: Quick EDA - the first thing to do in any competition ---
print(train.isnull().sum())          # check missing values
print(train["Survived"].value_counts(normalize=True))  # check class balance
print(train.groupby("Sex")["Survived"].mean())          # obvious signal check

# --- Step 3: Feature engineering ---
train["FamilySize"] = train["SibSp"] + 1
train["IsAlone"] = (train["FamilySize"] == 1).astype(int)
train["AgeBucket"] = pd.cut(train["Age"], bins=[0, 12, 18, 35, 60, 100],
                             labels=["child", "teen", "adult", "middle_age", "senior"])

# --- Step 4: Encode categoricals ---
le_sex = LabelEncoder()
train["Sex_enc"] = le_sex.fit_transform(train["Sex"])
train["AgeBucket_enc"] = LabelEncoder().fit_transform(train["AgeBucket"])

features = ["Pclass", "Sex_enc", "Age", "Fare", "FamilySize", "IsAlone", "AgeBucket_enc"]
X = train[features]
y = train["Survived"]

# --- Step 5: Cross-validate with a solid baseline model ---
model = RandomForestClassifier(n_estimators=300, max_depth=6, random_state=42, n_jobs=-1)
kf = KFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model, X, y, cv=kf, scoring="accuracy")
print(f"CV accuracy: {scores.mean():.4f} (+/- {scores.std():.4f})")

# --- Step 6: Fit on all training data and generate a submission ---
model.fit(X, y)

# Simulated test set - in real Kaggle this comes from test.csv
test = train.sample(50, random_state=1).drop(columns=["Survived"]).reset_index(drop=True)
test_preds = model.predict(test[features])

submission = pd.DataFrame({
    "PassengerId": test["PassengerId"],
    "Survived": test_preds,
})
submission.to_csv("submission.csv", index=False)
print(submission.head())

# --- Step 7: Feature importance check - useful for the next iteration ---
importances = pd.Series(model.feature_importances_, index=features).sort_values(ascending=False)
print(importances)
```

## Exercise
1. Download the real Titanic dataset from Kaggle and rerun this exact pipeline — compare CV score to the simulated version.
2. Add a `Title` feature extracted from a `Name` column (e.g., "Mr", "Mrs", "Master") — historically one of the strongest Titanic features.
3. Submit two different models (Random Forest vs. XGBoost) and note which one Kaggle's leaderboard scores higher.

## Key Takeaways
- Every competition starts the same way: check missing values, check class balance, check obvious signal (like `groupby("Sex")`) before touching any model.
- Cross-validation score should track your leaderboard score reasonably closely — if it doesn't, you likely have data leakage or a distribution mismatch between train/test.
- Feature engineering ideas usually come from domain understanding (e.g., "families might survive/sink together") more than from clever algorithms.
