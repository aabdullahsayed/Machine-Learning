# 005 - Handling Imbalanced Data

## Concept
Class imbalance (e.g., 95% "normal", 5% "fraud") biases most models toward the majority class. This lesson covers resampling techniques: **Random Oversampling**, **SMOTE** (Synthetic Minority Oversampling), **Random Undersampling**, and algorithm-level fixes like `class_weight`.

## Why It Matters
This is the deep-dive companion to the imbalance issues seen in module 05 (churn/spam) and module 06 (precision/recall/ROC-AUC) — this lesson gives you concrete tools to actually fix the imbalance, not just measure around it.

## Hands-On

```python
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, f1_score
from collections import Counter

X, y = make_classification(n_samples=2000, n_features=10, weights=[0.95, 0.05],
                            flip_y=0.01, random_state=42)
print("Original class distribution:", Counter(y))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y, random_state=42)

# 1. Baseline: no handling of imbalance at all
baseline = LogisticRegression(max_iter=1000).fit(X_train, y_train)
print("\n--- Baseline (no imbalance handling) ---")
print(classification_report(y_test, baseline.predict(X_test)))

# 2. class_weight="balanced" - reweights the loss function, no data changes
weighted = LogisticRegression(max_iter=1000, class_weight="balanced").fit(X_train, y_train)
print("--- class_weight='balanced' ---")
print(classification_report(y_test, weighted.predict(X_test)))

# 3. Random oversampling - duplicate minority class examples
try:
    from imblearn.over_sampling import RandomOverSampler, SMOTE
    from imblearn.under_sampling import RandomUnderSampler
    HAS_IMBLEARN = True
except ImportError:
    HAS_IMBLEARN = False
    print("\n(imbalanced-learn not installed - showing manual implementation instead)")

if HAS_IMBLEARN:
    ros = RandomOverSampler(random_state=42)
    X_ros, y_ros = ros.fit_resample(X_train, y_train)
    print(f"\nAfter Random Oversampling: {Counter(y_ros)}")
    model_ros = LogisticRegression(max_iter=1000).fit(X_ros, y_ros)
    print("--- Random Oversampling ---")
    print(classification_report(y_test, model_ros.predict(X_test)))

    # 4. SMOTE - generates SYNTHETIC minority examples by interpolating
    # between real minority neighbors, rather than exact duplicates
    smote = SMOTE(random_state=42)
    X_smote, y_smote = smote.fit_resample(X_train, y_train)
    print(f"\nAfter SMOTE: {Counter(y_smote)}")
    model_smote = LogisticRegression(max_iter=1000).fit(X_smote, y_smote)
    print("--- SMOTE ---")
    print(classification_report(y_test, model_smote.predict(X_test)))

    # 5. Random undersampling - discard majority class examples
    rus = RandomUnderSampler(random_state=42)
    X_rus, y_rus = rus.fit_resample(X_train, y_train)
    print(f"\nAfter Random Undersampling: {Counter(y_rus)}")
    model_rus = LogisticRegression(max_iter=1000).fit(X_rus, y_rus)
    print("--- Random Undersampling ---")
    print(classification_report(y_test, model_rus.predict(X_test)))
else:
    # Manual oversampling as a fallback
    minority_idx = np.where(y_train == 1)[0]
    majority_idx = np.where(y_train == 0)[0]
    oversample_idx = np.random.choice(minority_idx, size=len(majority_idx), replace=True)
    balanced_idx = np.concatenate([majority_idx, oversample_idx])
    np.random.shuffle(balanced_idx)
    X_manual, y_manual = X_train[balanced_idx], y_train[balanced_idx]
    print(f"\nManual oversampling result: {Counter(y_manual)}")
    model_manual = LogisticRegression(max_iter=1000).fit(X_manual, y_manual)
    print(classification_report(y_test, model_manual.predict(X_test)))

# 6. CRITICAL: resample ONLY the training set, never the test set!
print("""
IMPORTANT: Resampling must happen AFTER the train/test split, and only on
the training data (module 02, file 006). Resampling before splitting, or
resampling the test set, leaks synthetic/duplicated information across the
split and gives an artificially inflated (and wrong) performance estimate.
""")
```

## Exercise
1. Compare F1 score (module 06, file 003) for the minority class across all methods tried above — which one wins on this dataset?
2. If `imbalanced-learn` is available, try `SMOTETomek` (SMOTE + cleaning overlapping points) and compare against plain SMOTE.
3. Explain, for a fraud-detection use case with 0.1% fraud rate, why undersampling alone (throwing away 99.9% of legitimate transactions) might be a bad idea, and propose a hybrid approach.

## Key Takeaways
- `class_weight="balanced"` is the simplest fix and requires no changes to the data itself — try it first.
- SMOTE generally outperforms naive duplication (Random Oversampling) because it creates diverse synthetic examples rather than exact copies.
- Resampling must be applied only to the training set, inside the cross-validation loop if used — never to validation/test data.
