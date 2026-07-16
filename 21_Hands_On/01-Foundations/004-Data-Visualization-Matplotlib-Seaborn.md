# 004 - Data Visualization with Matplotlib & Seaborn

## Concept
Matplotlib is the low-level plotting engine; Seaborn is a higher-level wrapper with better statistical defaults (histograms, box plots, heatmaps). Visualization is how you build intuition about a dataset before modeling it.

## Why It Matters
Every EDA workflow (module 02) and every model-evaluation report (module 06) leans on these plots: distributions, correlations, confusion matrices, ROC curves.

## Hands-On

```python
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

# Sample dataset
np.random.seed(42)
df = pd.DataFrame({
    "age": np.random.normal(35, 10, 200).clip(18, 70),
    "income": np.random.normal(55000, 15000, 200),
    "purchased": np.random.choice([0, 1], 200, p=[0.6, 0.4])
})

# 1. Histogram - understand a single variable's distribution
plt.figure(figsize=(6, 4))
plt.hist(df["age"], bins=20, edgecolor="black")
plt.title("Age Distribution")
plt.xlabel("Age")
plt.ylabel("Count")
plt.savefig("age_hist.png")
plt.close()

# 2. Scatter plot - relationship between two continuous variables
plt.figure(figsize=(6, 4))
plt.scatter(df["age"], df["income"], alpha=0.6)
plt.xlabel("Age")
plt.ylabel("Income")
plt.title("Age vs Income")
plt.savefig("age_income_scatter.png")
plt.close()

# 3. Seaborn box plot - compare a numeric var across categories
plt.figure(figsize=(6, 4))
sns.boxplot(x="purchased", y="income", data=df)
plt.title("Income by Purchase Decision")
plt.savefig("income_boxplot.png")
plt.close()

# 4. Correlation heatmap - a staple of every EDA notebook
plt.figure(figsize=(5, 4))
corr = df.corr(numeric_only=True)
sns.heatmap(corr, annot=True, cmap="coolwarm", center=0)
plt.title("Correlation Matrix")
plt.savefig("correlation_heatmap.png")
plt.close()

# 5. Pairplot - quick overview of all pairwise relationships
sns.pairplot(df, hue="purchased")
plt.savefig("pairplot.png")
plt.close()

print("All plots saved.")
```

## Exercise
1. Plot a histogram of `income` split by `purchased` using `sns.histplot(..., hue="purchased")`.
2. Create a bar chart showing the count of purchases (0 vs 1) using `sns.countplot`.
3. Build a 2x2 grid of subplots (`plt.subplots(2, 2)`) showing four different views of the same dataset.

## Key Takeaways
- Histograms and box plots reveal skew and outliers before you touch a model.
- Correlation heatmaps are the fastest way to spot multicollinearity (relevant in module 04's regularization lesson).
- Save figures with `plt.savefig()` in scripts; use inline display in notebooks.
