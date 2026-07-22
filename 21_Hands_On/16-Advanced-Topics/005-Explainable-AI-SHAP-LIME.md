# 005 - Explainable AI: SHAP & LIME

## Concept
Explainable AI (XAI) techniques explain *why* a model made a specific prediction. SHAP (SHapley Additive exPlanations) uses game theory to fairly attribute a prediction to each feature; LIME (Local Interpretable Model-agnostic Explanations) approximates the model locally with a simple, interpretable model around one prediction.

## Why It Matters
"The model said no" isn't good enough for high-stakes decisions (loans, medical diagnoses, hiring) — regulators, users, and even model developers often need to understand which features drove a specific prediction, and whether that reasoning is sound.

## Hands-On

```python
# pip install shap lime --break-system-packages
import numpy as np
import pandas as pd
import shap
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

data = load_breast_cancer()
X = pd.DataFrame(data.data, columns=data.feature_names)
y = data.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)
print("Test accuracy:", model.score(X_test, y_test))

# ============================================
# 1. SHAP - global and local explanations
# ============================================
explainer = shap.TreeExplainer(model)          # optimized explainer for tree-based models
shap_values = explainer.shap_values(X_test)

# Global feature importance - which features matter most across ALL predictions
shap.summary_plot(shap_values[:, :, 1], X_test, show=False)  # class 1 = malignant
import matplotlib.pyplot as plt
plt.tight_layout()
plt.savefig("shap_summary.png")
plt.close()

# Local explanation - why did the model predict THIS specific sample the way it did?
sample_idx = 0
sample = X_test.iloc[[sample_idx]]
prediction = model.predict(sample)[0]
print(f"\nSample {sample_idx} predicted class: {prediction} ({'malignant' if prediction==0 else 'benign'})")

sample_shap_values = shap_values[sample_idx, :, prediction]
feature_contributions = pd.Series(sample_shap_values, index=X_test.columns).sort_values(key=abs, ascending=False)
print("Top 5 features driving this prediction:")
print(feature_contributions.head(5))

# ============================================
# 2. LIME - model-agnostic local explanations
# ============================================
from lime.lime_tabular import LimeTabularExplainer

lime_explainer = LimeTabularExplainer(
    training_data=X_train.values,
    feature_names=X_train.columns.tolist(),
    class_names=["malignant", "benign"],
    mode="classification",
)

lime_explanation = lime_explainer.explain_instance(
    X_test.iloc[sample_idx].values,
    model.predict_proba,
    num_features=5,
)
print("\nLIME explanation for the same sample:")
for feature, weight in lime_explanation.as_list():
    print(f"  {feature}: {weight:.4f}")

# ============================================
# 3. Comparing SHAP vs LIME agreement
# ============================================
# Both should broadly agree on the MOST important features, even though their
# underlying methods differ (SHAP: game-theoretic exact attribution;
# LIME: local linear approximation).

# ============================================
# 4. Permutation importance - a simpler, model-agnostic global importance measure
# ============================================
from sklearn.inspection import permutation_importance

perm_result = permutation_importance(model, X_test, y_test, n_repeats=10, random_state=42)
perm_importances = pd.Series(perm_result.importances_mean, index=X_test.columns).sort_values(ascending=False)
print("\nTop 5 features by permutation importance:")
print(perm_importances.head(5))
```

## Exercise
1. Compare the top-5 features from SHAP, LIME, and permutation importance on the same sample — how much overlap is there?
2. Find a sample the model gets *wrong* and use SHAP to investigate which features misled the model.
3. Try SHAP's `dependence_plot` for the single most important feature — does the relationship between feature value and SHAP value look linear, or more complex?

## Key Takeaways
- SHAP values are additive and theoretically grounded (based on Shapley values from cooperative game theory) — they sum up to exactly explain the difference between a prediction and the average prediction.
- LIME is model-agnostic (works with any black-box model, not just trees) but its explanations are local approximations and can be less stable across repeated runs on the same instance.
- Feature importance (module 09) tells you what matters on average across the whole dataset; SHAP/LIME tell you what mattered for one specific prediction — both views are useful and answer different questions.
