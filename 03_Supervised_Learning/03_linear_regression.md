# 03 — Linear Regression

*(For the deep-dive on the optimization side — gradient descent, learning
rate, convergence — see the companion "Gradient Descent" notes pack. This
file focuses on linear regression itself as a model.)*

## Analogy: the "rule of thumb" line through a scatter of dots

Imagine a real-estate agent who's sold houses for years. Ask them "roughly
how much is a 2,000 sq ft house worth around here?" and they can eyeball an
answer instantly, because in their head they've drawn a mental **straight
line** through all the sales they remember: bigger house → roughly
proportionally higher price. Linear regression formalizes exactly this
mental "rule of thumb" line — it finds the *single straight line* (or flat
plane, in higher dimensions) that best threads through a cloud of data
points.

```
 price ($)
   │                                    ×
   │                              ×  ╱
   │                         ×  ╱
   │                    ×   ╱ ×
   │               ×    ╱
   │          ×    ╱ ×
   │      ×    ╱
   │   ×    ╱               "best fit" line:
   │    ╱  ×                 price = θ0 + θ1·sqft
   │  ╱
   └──────────────────────────────────────── sq ft
```

## The model

```
ŷ = θ0 + θ1·x1 + θ2·x2 + ... + θn·xn
```

| Symbol | Meaning |
|---|---|
| `ŷ` | predicted value |
| `θ0` | intercept / bias (value of ŷ when all x = 0) |
| `θ1...θn` | coefficients (weights) — how much ŷ changes per unit change in each feature |
| `x1...xn` | input features |

In matrix form (with `x0 = 1` folded in for the intercept):

```
ŷ = θᵀx = Xθ
```

## The cost function: Mean Squared Error

```
J(θ) = (1/2m) Σ_{i=1}^{m} (ŷ_i − y_i)²
```

We want the θ that minimizes this — i.e., the line with the smallest total
squared distance between predictions and actual points.

```
        │           ×
        │          ╱│  ← "residual" (error): vertical distance
        │         ╱ │     from point to the line
        │        ╱  │
        │   ×   ╱   
        │      ╱
        │─────╱───×──────── the fitted line
        │    ╱
        │   ╱   ×
        └──────────────────
```

## Two ways to solve for θ

### 1. Closed-form: the Normal Equation

```
θ = (XᵀX)⁻¹ Xᵀy
```

- ✅ Exact solution in one shot, no learning rate needed
- ❌ Computing a matrix inverse is `O(n³)` — slow/impractical when the
  number of features `n` is large (thousands+)

### 2. Iterative: Gradient Descent

```
θ := θ − α · (1/m) Xᵀ(Xθ − y)
```

- ✅ Scales to huge datasets and many features
- ❌ Requires tuning learning rate `α`, iterating until convergence

| | Normal Equation | Gradient Descent |
|---|---|---|
| Speed (small n) | fast | slower to converge |
| Speed (large n, e.g. n > 10,000) | slow (matrix inversion) | fast per step |
| Needs feature scaling? | no | yes (helps convergence) |
| Needs learning rate? | no | yes |
| Exact vs. approximate | exact | approximate (converges toward exact) |

## Assumptions of linear regression

| Assumption | What it means | If violated... |
|---|---|---|
| Linearity | relationship between x and y is (approximately) linear | model systematically under/over-predicts in regions |
| Independence | observations are independent of each other | standard errors become unreliable |
| Homoscedasticity | error variance is roughly constant across all x | predictions less reliable at certain x ranges |
| Normality of residuals | errors are roughly normally distributed | affects confidence intervals, not point predictions much |
| No severe multicollinearity | features aren't highly correlated with each other | unstable, hard-to-interpret coefficients |

## Multiple linear regression — adding more features

```
price = θ0 + θ1·sqft + θ2·bedrooms + θ3·age + θ4·distance_to_city
```

Each `θ_j` represents the effect of feature `j` **holding all other
features constant** — e.g. "each additional bedroom adds $θ2, all else
equal."

## Polynomial regression — still "linear" in the parameters!

Linear regression can fit *curves*, not just straight lines, by adding
polynomial features — it's still linear in θ, just not linear in x:

```
ŷ = θ0 + θ1·x + θ2·x² + θ3·x³
```

```
  y                                y (with x² term added)
  │  ×                             │  ×
  │ ×    ×          straight       │ ×    ×      curved fit
  │×  ─────── ×      line          │×   ╱‾‾╲ ×    captures the
  │      ───    ×    misses        │   ╱    ╲     bend in the data
  │×  ×     ─── ×    the curve     │× ╱   ×  ╲  ×
  └──────────────── x              └──────────────── x
```

⚠️ Careful: higher-degree polynomials fit training data increasingly well
but risk **overfitting** (see file `02`) — always validate on held-out data.

## Regularized variants: Ridge & Lasso

Add a penalty term to discourage large coefficients (reduces overfitting):

```
Ridge (L2):  J(θ) = MSE(θ) + λ Σ θ_j²
Lasso (L1):  J(θ) = MSE(θ) + λ Σ |θ_j|
```

| | Ridge (L2) | Lasso (L1) |
|---|---|---|
| Effect | shrinks coefficients toward zero | can shrink coefficients to *exactly* zero |
| Feature selection? | no | yes (sparse solutions) |
| Use case | many small/medium correlated features | want automatic feature selection |

## Evaluation metrics

| Metric | Formula | Interpretation |
|---|---|---|
| MSE | `(1/m)Σ(ŷ−y)²` | average squared error (penalizes large errors more) |
| RMSE | `√MSE` | same units as `y`, easier to interpret |
| MAE | `(1/m)Σ|ŷ−y|` | average absolute error, less sensitive to outliers |
| R² | `1 − SS_res/SS_tot` | fraction of variance in `y` explained by the model (1.0 = perfect) |

## When to use linear regression

✅ Good for: predicting continuous values, when the relationship is
roughly linear, when interpretability matters (coefficients have clear
meaning), as a fast baseline model.

❌ Not ideal for: strongly non-linear relationships (without engineered
features), classification tasks (use Logistic Regression instead — file `04`).
