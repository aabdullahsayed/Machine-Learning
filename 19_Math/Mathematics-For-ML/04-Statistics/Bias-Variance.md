# Bias-Variance Tradeoff

## Math Explanation

For a model trying to predict `y` from `x`, the **expected prediction error** on new data can be mathematically decomposed into three parts:
```
Expected Error = Bias² + Variance + Irreducible Error
```
- **Bias**: error from overly simplistic assumptions in the model — how far off the model's average prediction is from the true value, if you could retrain on many different datasets. High bias = **underfitting**.
- **Variance**: how much the model's predictions would change if trained on a *different* training set — sensitivity to the specific data sampled. High variance = **overfitting**.
- **Irreducible error**: noise inherent in the data itself — no model can eliminate this (e.g., measurement noise).

### The tradeoff
- **Simple models** (e.g., linear regression on complex data): high bias, low variance — consistently wrong in the same way, but stable/predictable.
- **Complex models** (e.g., a very deep decision tree, or an overparameterized neural network with no regularization): low bias, high variance — can fit training data very well, but predictions swing wildly depending on the exact training set, and generalize poorly.

```
       High Bias                    High Variance
    (underfitting)                 (overfitting)
  Simple model -----------------------> Complex model
       ↓                                    ↓
  Misses patterns                  Memorizes noise in
  in the data                       training data
```

## In ML/DL

- **This is THE central conceptual framework for diagnosing model performance problems.** Training accuracy low AND validation accuracy low → high bias (underfitting) → try a more complex model, more features, less regularization. Training accuracy high but validation accuracy much lower → high variance (overfitting) → try more data, regularization, simpler model, dropout, early stopping.
- **Regularization (L1/L2, dropout)** deliberately **increases bias slightly to reduce variance substantially** — this trade is usually worth it because it improves generalization (performance on new, unseen data), which is what actually matters in production.
- **Ensemble methods** attack each side differently:
  - **Bagging** (e.g., Random Forests): trains many high-variance models (deep decision trees) on different bootstrapped samples and averages them — averaging reduces variance while keeping bias low.
  - **Boosting** (e.g., XGBoost, AdaBoost): trains a sequence of simple, high-bias models, each correcting the previous one's errors — reduces bias while controlling variance carefully.
- **Deep learning's "double descent" phenomenon** (a modern nuance to classic bias-variance theory): very large, heavily overparameterized models can sometimes have LOW variance despite huge capacity, contradicting naive intuition — an active area of ML research showing the classic bias-variance curve isn't the complete picture for today's massive models.
- **Learning curves** (plotting training vs. validation error as a function of training set size or model complexity) are the standard practical diagnostic tool for visualizing exactly where you sit on this tradeoff.
