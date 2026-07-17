# Expectation & Variance

## Math Explanation

### Expectation (Expected Value)
The **expectation** `E[X]` is the long-run average value of a random variable — a weighted average of all possible outcomes, weighted by their probability.
```
Discrete:    E[X] = Σ x · P(X=x)
Continuous:  E[X] = ∫ x · f(x) dx
```

### Key properties (linearity of expectation — extremely useful)
```
E[X + Y] = E[X] + E[Y]        (always true, even if X, Y are dependent!)
E[cX] = c·E[X]                  (scaling)
```

### Variance
**Variance** measures how spread out a random variable's values are around its mean:
```
Var(X) = E[(X - E[X])²] = E[X²] - (E[X])²
```
**Standard deviation** `σ = √Var(X)` — same units as `X` itself, often more interpretable than variance.

### Covariance
Measures how two random variables vary *together*:
```
Cov(X, Y) = E[(X - E[X])(Y - E[Y])]
```
Positive → tend to increase together. Negative → one increases as the other decreases. Zero → no linear relationship (though not necessarily independent!).

## In ML/DL

- **Loss functions are expectations.** The "true" loss we ultimately want to minimize is `E[Loss(model(x), y)]` over the entire true data distribution — but since we can't access the true distribution, we approximate it using the average loss over a finite training set (or mini-batch), which is a **sample estimate** of this expectation. This is the formal justification for why training on a large, representative dataset works.
- **Bias-Variance tradeoff** (see `04-Statistics/Bias-Variance.md`) is built entirely on these definitions — decomposing a model's expected prediction error into bias (systematic error) and variance (sensitivity to the specific training set) components.
- **Batch Normalization** explicitly computes and uses the mean and variance of activations within each mini-batch to normalize them, stabilizing and speeding up training.
```python
# Conceptually, batch norm does:
mean = activations.mean()
var = activations.var()
normalized = (activations - mean) / np.sqrt(var + epsilon)
```
- **The covariance matrix** of your features is exactly what PCA operates on (see `01-Linear-Algebra/Eigenvalues-Eigenvectors.md` and `07-ML-Applications/PCA.md`) — it captures how every pair of features varies together, which PCA uses to find the directions of maximum variance.
- **Reward in reinforcement learning** is fundamentally about maximizing an *expected* cumulative reward `E[Σ rewards]` — nearly all of RL theory is built around estimating and optimizing this expectation under uncertainty.
