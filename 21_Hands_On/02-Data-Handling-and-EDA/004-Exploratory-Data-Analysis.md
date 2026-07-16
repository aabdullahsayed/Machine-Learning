# 004 - Exploratory Data Analysis (EDA)

## Concept
EDA is the systematic process of summarizing a dataset's main characteristics, often visually, before modeling. It answers: What does each feature look like? How do features relate to each other and to the target? Are there red flags (leakage, imbalance, skew)?

## Why It Matters
A good EDA pass often reveals more actionable insight than the first several models you'll train. It also determines your feature engineering plan (module 07) and preprocessing choices (module 02).

## Hands-On

```python
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

np.random.seed(1)
n = 500
df = pd.DataFrame({
    "age": np.random.normal(40, 12, n).clip(18, 75).round(),
    "income": np.random.lognormal(mean=10.5, sigma=0.5, size=n),
    "credit_score": np.random.normal(650, 80, n).clip(300, 850),
    "region": np.random.choice(["North", "South", "East", "West"], n),
    "defaulted": np.random.choice([0, 1], n, p=[0.85, 0.15]),
})

# 1. Structural overview - always start here
print(df.shape)
print(df.dtypes)
print(df.describe(include="all"))

# 2. Target variable distribution - check for class imbalance early
print("\nTarget distribution:\n", df["defaulted"].value_counts(normalize=True))
sns.countplot(x="defaulted", data=df)
plt.title("Target Class Balance")
plt.savefig("target_balance.png")
plt.close()

# 3. Univariate analysis - distribution of each numeric feature
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
for ax, col in zip(axes, ["age", "income", "credit_score"]):
    sns.histplot(df[col], kde=True, ax=ax)
    ax.set_title(col)
plt.tight_layout()
plt.savefig("univariate_distributions.png")
plt.close()

# 4. Bivariate analysis - feature vs target
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
for ax, col in zip(axes, ["age", "income", "credit_score"]):
    sns.boxplot(x="defaulted", y=col, data=df, ax=ax)
    ax.set_title(f"{col} vs defaulted")
plt.tight_layout()
plt.savefig("bivariate_analysis.png")
plt.close()

# 5. Categorical feature vs target
cross_tab = pd.crosstab(df["region"], df["defaulted"], normalize="index")
print("\nDefault rate by region:\n", cross_tab)

# 6. Correlation analysis
corr = df.select_dtypes(include=np.number).corr()
sns.heatmap(corr, annot=True, cmap="coolwarm")
plt.title("Correlation Matrix")
plt.savefig("eda_correlation.png")
plt.close()

# 7. Summary of findings (this should always be written up, not just plotted)
print("""
EDA Summary:
- Target is imbalanced (~15% positive class) -> consider stratified splits (005) and
  resampling techniques (module 07, file 005).
- income is log-normal, heavily right-skewed -> consider log-transforming.
- Check region-level default rate differences -> could be a useful categorical feature.
""")
```

## Exercise
1. For a dataset of your choice, write a 5-bullet EDA summary covering: target balance, most skewed feature, strongest correlation, any suspicious "too-good-to-be-true" feature (leakage check!), and one bivariate insight.
2. Create a pairplot colored by the target variable to visually inspect class separability.
3. Identify one feature that looks like it might leak target information (i.e., only known *after* the target event happens) — this connects to module 02's next lesson.

## Key Takeaways
- Always check target balance before choosing metrics (module 06) — accuracy is misleading on imbalanced data.
- Bivariate plots against the target are more informative for modeling decisions than univariate plots alone.
- EDA should always end with a short written summary of hypotheses to test, not just a folder of plots.
