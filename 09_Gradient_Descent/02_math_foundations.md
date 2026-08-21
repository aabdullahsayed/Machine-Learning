# 02 — Math Foundations

## 1. The setup: what are we optimizing?

In supervised ML we have:
- Data: features `x`, true labels `y`
- A model with parameters `θ` that produces predictions `ŷ = f(x; θ)`
- A **cost function** `J(θ)` measuring how wrong those predictions are

For linear regression:

```
ŷ_i = θ0 + θ1·x_i                       (prediction for example i)

J(θ0, θ1) = (1/2m) · Σ_{i=1}^{m} (ŷ_i − y_i)²      (Mean Squared Error, /2 for clean derivative)
```

Our goal:

```
θ* = argmin_θ  J(θ)
```

Find the parameter values that minimize the cost.

## 2. Why calculus? The gradient

The **gradient** `∇J(θ)` is the vector of partial derivatives of `J` with
respect to every parameter. It always points in the direction of **steepest
ascent** (fastest increase) of `J`.

```
∇J(θ) = [ ∂J/∂θ0 ,  ∂J/∂θ1 ,  ... ,  ∂J/∂θn ]ᵀ
```

For our simple linear regression cost:

```
∂J/∂θ0 = (1/m) Σ (ŷ_i − y_i)
∂J/∂θ1 = (1/m) Σ (ŷ_i − y_i)·x_i
```

### Deriving ∂J/∂θ1 step by step (chain rule)

```
J(θ) = (1/2m) Σ (θ0 + θ1·x_i − y_i)²

Let e_i = (θ0 + θ1·x_i − y_i)          "error" for example i

∂J/∂θ1 = (1/2m) Σ 2·e_i · ∂e_i/∂θ1
       = (1/2m) Σ 2·e_i · x_i
       = (1/m)  Σ e_i · x_i
```

That's just the chain rule: derivative of the outer square, times the
derivative of the inner linear term.

## 3. The update rule

```
                    ┌────────────────────────────┐
                    │  θ_j := θ_j − α · ∂J/∂θ_j   │   for every parameter j
                    └────────────────────────────┘
```

All parameters are updated **simultaneously** using gradients computed from
the *same* `θ` (don't use an already-updated `θ0` to compute `θ1`'s gradient
in the same step).

| Symbol | Meaning |
|---|---|
| `θ_j` | j-th parameter (weight or bias) |
| `α` (alpha) | learning rate — step size, typically 0.001 – 0.1 |
| `∂J/∂θ_j` | partial derivative of cost w.r.t. that parameter |
| `:=` | "is updated to" (assignment, not equality) |

## 4. Worked numeric example

Tiny dataset: `x = [1, 2, 3]`, `y = [2, 4, 6]` (perfectly `y = 2x`).
Start with `θ0 = 0`, `θ1 = 0`, learning rate `α = 0.1`.

**Step 1 — forward pass (predictions with current θ):**

```
ŷ = [0, 0, 0]        (since θ0=0, θ1=0 → ŷ = 0 + 0·x)
errors e = ŷ − y = [-2, -4, -6]
```

**Step 2 — compute gradients:**

```
∂J/∂θ0 = (1/3)(-2 -4 -6)        = -4.0
∂J/∂θ1 = (1/3)(-2·1 -4·2 -6·3)  = (1/3)(-2-8-18) = -9.333
```

**Step 3 — update:**

```
θ0 := 0 − 0.1·(-4.0)     = 0.4
θ1 := 0 − 0.1·(-9.333)   = 0.933
```

After just **one step**, θ1 already jumped from 0 toward the true value 2.
Repeat this loop hundreds of times and θ0 → 0, θ1 → 2.

| Iteration | θ0 | θ1 | J(θ) |
|---|---|---|---|
| 0 | 0.000 | 0.000 | 9.33 |
| 1 | 0.400 | 0.933 | 1.51 |
| 2 | 0.499 | 1.276 | 0.34 |
| 5 | 0.487 | 1.647 | 0.06 |
| 20 | 0.145 | 1.921 | 0.006 |
| 100 | 0.006 | 1.997 | ~0.00003 |

(Values approximate — reproduce them yourself in `06_python_implementation.py`.)

## 5. Visualizing the loss surface (bowl shape)

For linear regression with MSE, `J(θ0, θ1)` is a **convex paraboloid** —
a perfect bowl with exactly one minimum. This is why simple gradient
descent works so reliably for linear/logistic regression: no matter where
you start, you'll always reach the bottom.

```
J(θ)
 │        ..                          ..
 │          ..                      ..
 │            ..                  ..
 │              ..              ..
 │                ..          ..
 │                  ..      ..
 │                    ..  ..
 │                      ..            <- global minimum (unique bottom)
 └───────────────────────────────────  θ1
```

For deep neural networks, `J(θ)` is **non-convex** — a bumpy, high-dimensional
landscape with many local dips, saddle points, and plateaus (see file 04).

## 6. The full batch gradient descent algorithm (pseudocode)

```
initialize θ (often randomly, or all zeros)
repeat until convergence (or max_iterations):
    compute predictions ŷ = f(X; θ)     for ALL m examples
    compute gradient g = ∇J(θ)          using ALL m examples
    θ := θ − α · g
return θ
```

Next file (`03`) explores what happens when we *don't* use all m examples
every step.
