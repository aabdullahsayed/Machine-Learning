# 001 - What is Machine Learning

## Concept
Machine Learning is the practice of building systems that improve their performance on a task by learning patterns from data, rather than following explicitly programmed rules. Formally (Tom Mitchell's definition): a program learns from experience E with respect to task T and performance measure P, if its performance at T, measured by P, improves with E.

## Why It Matters
This framing — task, experience, performance measure — is exactly how you should scope every ML project: define what you're predicting (T), what data you have (E), and how you'll know if it worked (P, covered fully in module 06).

## Hands-On

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

# Demonstration: "traditional programming" vs "machine learning"

# --- Traditional programming: rules are hand-written ---
def traditional_shipping_cost(weight_kg):
    if weight_kg <= 1:
        return 5.0
    elif weight_kg <= 5:
        return 5.0 + (weight_kg - 1) * 1.5
    else:
        return 5.0 + 4 * 1.5 + (weight_kg - 5) * 1.0

weights = [0.5, 2, 4, 8, 10]
print("Traditional rule-based costs:", [traditional_shipping_cost(w) for w in weights])

# --- Machine learning: rules are LEARNED from examples (experience E) ---
# We only give the model (weight, actual_cost) pairs; it discovers the pattern.
np.random.seed(0)
train_weights = np.random.uniform(0.1, 15, 200).reshape(-1, 1)
# Ground truth follows a roughly linear relationship + noise
train_costs = 5 + 1.2 * train_weights.ravel() + np.random.normal(0, 1, 200)

model = LinearRegression()
model.fit(train_weights, train_costs)  # this is "learning from experience"

# The model was never told the rule - it discovered slope & intercept itself
print(f"\nLearned relationship: cost ≈ {model.intercept_:.2f} + {model.coef_[0]:.2f} * weight")

predicted_costs = model.predict(np.array(weights).reshape(-1, 1))
print("ML-predicted costs:", predicted_costs.round(2))

# Task (T): predict shipping cost from weight
# Experience (E): 200 historical (weight, cost) examples
# Performance measure (P): how close predictions are to actual costs (module 06)
```

## Exercise
1. For three real-world problems of your choice (e.g., email spam filtering, house price estimation, medical diagnosis), write out T, E, and P explicitly.
2. Modify the shipping-cost example so the true relationship is nonlinear (e.g., quadratic) and observe how a `LinearRegression` model underfits it — you'll fix this in module 04 with polynomial regression.
3. In one paragraph, explain why "traditional programming" would struggle with a task like image classification (module 11), where the "rules" for what makes a picture a "cat" are nearly impossible to hand-write.

## Key Takeaways
- ML shines when patterns are too complex or numerous to hand-code, but there's enough representative data to learn from.
- Every ML problem should be scoped with a clear Task, Experience (data), and Performance measure before you write any modeling code.
- A model's "knowledge" is entirely a function of the data it was shown — biased or incomplete data yields a biased or incomplete model.
