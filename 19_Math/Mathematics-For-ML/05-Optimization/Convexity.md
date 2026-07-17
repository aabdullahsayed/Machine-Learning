# Convexity

## Math Explanation

A function `f` is **convex** if the line segment connecting any two points on its graph lies entirely **above or on** the graph itself:
```
f(λx + (1-λ)y) ≤ λf(x) + (1-λ)f(y)     for all λ ∈ [0,1]
```
Intuitively: a convex function is "bowl-shaped" — no local dips that aren't also the global minimum.

### Why convexity matters mathematically
**A convex function has, at most, ONE global minimum region (no separate local minima to get trapped in).** This means gradient descent, run on a convex function, is *guaranteed* to converge to the global minimum (given a suitable learning rate) — no risk of getting stuck.

### Checking convexity
- **Single variable**: `f''(x) ≥ 0` everywhere (non-negative curvature — always curving upward or flat).
- **Multivariable**: the Hessian matrix `H(x)` is **positive semi-definite** everywhere (see `01-Linear-Algebra/Eigenvalues-Eigenvectors.md`).

### Examples
- **Convex**: `f(x) = x²`, `f(x) = eˣ`, Mean Squared Error loss (as a function of the model's linear parameters), Support Vector Machine's hinge loss objective.
- **Non-convex**: `f(x) = x⁴ - x²` (has multiple local minima), and critically — **the loss surface of any nontrivial neural network** (due to the nonlinear activation functions and the many ways to permute/rescale weights while producing identical outputs).

## In ML/DL

- **Classical ML models with convex loss functions (linear regression, logistic regression, linear SVMs) have a mathematically guaranteed unique optimal solution** — this is why these models are so reliable and well-understood; there's no "bad luck" from initialization or optimizer choice affecting the final result (given enough training).
- **Neural network loss surfaces are NOT convex** — this was historically considered a major theoretical concern ("how can gradient descent possibly work well on a non-convex surface with potentially many bad local minima?"). In practice, deep learning research has found that for large, overparameterized networks, most local minima found by SGD tend to have similar, good loss values — the non-convexity turns out to be far less of a practical obstacle than early theory feared, though it remains an active research topic.
- **Convex optimization is still hugely important as a subroutine**: many parts of ML pipelines (e.g., fitting the final linear layer on frozen features, certain regularized regression formulations, SVM training) rely on genuinely convex sub-problems with strong theoretical guarantees, solved via specialized, highly efficient convex optimization algorithms.
- **Understanding convexity helps you interpret training curves**: a smooth, monotonically decreasing loss curve on a genuinely convex problem is expected and reliable; the "bumpier," less predictable loss curves typical of deep learning training are a natural consequence of optimizing a non-convex surface with a stochastic, noisy gradient estimate (mini-batch SGD).
