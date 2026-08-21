# 08 — Generalized Linear Models (GLMs)

## Analogy: one universal recipe, different "toppings" per dish

Think of GLMs as a **base pizza dough recipe** that can be topped
differently to make very different dishes — Margherita, pepperoni, veggie
— but they all start from the exact same dough-making process. Similarly,
Linear Regression, Logistic Regression, and Poisson Regression all share
the *same underlying skeleton* (a linear combination of features), but each
adds a different "topping" (a **link function** and a **noise
distribution**) suited to a different type of output.

```
                    ┌─────────────────────────────┐
                    │   Same base "dough":          │
                    │   linear predictor            │
                    │   η = θ0 + θ1x1 + θ2x2 + ...  │
                    └───────────────┬───────────────┘
                                     │
              ┌──────────────────────┼──────────────────────┐
              ▼                      ▼                       ▼
     "Identity topping"      "Sigmoid topping"        "Exponential topping"
      (no transform)          (squash to 0-1)          (force positive)
              │                      │                       │
              ▼                      ▼                       ▼
     LINEAR REGRESSION      LOGISTIC REGRESSION        POISSON REGRESSION
     predicts real numbers   predicts probabilities      predicts counts
     (e.g. price, temp)      (e.g. spam/not spam)        (e.g. # of calls/day)
```

## The 3 components of every GLM

| Component | Role | Example (linear regression) | Example (logistic regression) |
|---|---|---|---|
| **1. Linear predictor** `η` | combines features linearly | `η = θ0 + θ1x1 + ...` | `η = θ0 + θ1x1 + ...` |
| **2. Link function** `g` | maps `η` to the mean of `y`'s distribution | identity: `g(μ) = μ` | logit: `g(μ) = log(μ/(1−μ))` |
| **3. Distribution family** | describes the noise/randomness in `y` | Gaussian (Normal) | Bernoulli |

```
η (linear predictor)  ──▶  g⁻¹ (inverse link)  ──▶  μ (predicted mean of y)  ──▶  y ~ Distribution(μ)
     θᵀx                    "un-squash" step         e.g. probability             actual noisy outcome
```

## Why bother generalizing at all?

Plain linear regression assumes `y` is a continuous, unbounded,
normally-distributed number. But real-world targets often violate this:

| Target `y` type | Problem with plain linear regression | GLM solution |
|---|---|---|
| Binary (0/1) | predictions can go outside [0,1], nonsensical | Logistic Regression (Bernoulli + logit link) |
| Counts (0,1,2,3,...) | predictions can be negative or non-integer | Poisson Regression (Poisson + log link) |
| Strictly positive, skewed (e.g. insurance claims) | Gaussian noise assumption poorly fits skewed data | Gamma Regression (Gamma + log link) |
| Proportions/rates | bounded [0,1], often not normally distributed | Beta Regression / Logistic with weights |

## The GLM family table

| Model | Distribution | Link function | Link formula | Typical use case |
|---|---|---|---|---|
| Linear Regression | Gaussian (Normal) | Identity | `g(μ) = μ` | house prices, temperature |
| Logistic Regression | Bernoulli | Logit | `g(μ) = log(μ/(1−μ))` | spam detection, churn prediction |
| Poisson Regression | Poisson | Log | `g(μ) = log(μ)` | # website visits, # accidents |
| Gamma Regression | Gamma | Log (typically) | `g(μ) = log(μ)` | insurance claim amounts, rainfall |
| Multinomial (Softmax) Regression | Multinomial | Softmax/generalized logit | — | multi-class classification |

## Worked example: Poisson Regression (predicting counts)

Suppose we want to predict the number of customer support calls per day
based on `marketing_spend`. Counts must be non-negative integers — a plain
linear model could nonsensically predict "-3.2 calls." Poisson regression
fixes this with a **log link**:

```
η = θ0 + θ1·marketing_spend
μ = e^η                          (exponentiate → always positive!)
y ~ Poisson(μ)                   (actual call count varies randomly around μ)
```

```
Linear regression on counts            Poisson regression on counts
(BAD — can predict negative!)          (GOOD — always non-negative)

 calls                                  calls
   │                                      │                    ___──
   │      ×  ×                            │      ×  ×      __──
   │   ×        ×                         │   ×        __──
   │ ×    line dips                       │ ×      __──
   │        below zero! ✗                 │    __──  (curved, exponential
  0│───────────────                      0│──────  shape — naturally
   │ ╲                                    │           stays ≥ 0)
   │  ╲ (nonsensical                      └──────────────── spend
   │   ╲  negative predictions)
   └──────────────── spend
```

## Why the "link function" matters mathematically

The link function `g` connects the unrestricted linear predictor `η`
(which can be any real number) to `μ`, the mean of `y`'s distribution
(which may be restricted, e.g. to (0,1) or (0,∞)):

```
g(μ) = η   ⟺   μ = g⁻¹(η)

Logistic regression:  g(μ) = log(μ/(1-μ))   ⟺   μ = 1/(1+e^(-η))   (sigmoid!)
Poisson regression:   g(μ) = log(μ)          ⟺   μ = e^η            (exponential!)
Linear regression:    g(μ) = μ               ⟺   μ = η              (no transform needed)
```

This is exactly why logistic regression's sigmoid isn't an arbitrary
choice — it's the **inverse logit link function**, mathematically derived
from assuming a Bernoulli-distributed outcome.

## Fitting a GLM: Maximum Likelihood Estimation (MLE)

Unlike plain linear regression's simple MSE minimization, GLMs are
typically fit by **maximum likelihood** — finding the `θ` that makes the
*observed* data most probable under the assumed distribution. In practice,
this is solved iteratively (e.g. via Iteratively Reweighted Least Squares,
or plain gradient descent on the negative log-likelihood) — and elegantly,
for the exponential family of distributions, this reduces to a very similar
gradient formula in every case:

```
∂(neg log-likelihood)/∂θ_j = (1/m) Σ (μ_i − y_i)·x_ij

  (same clean "predicted minus actual, times feature" form we saw
   in both linear regression AND logistic regression!)
```

This is the elegant payoff of the GLM framework: **one unified update
rule** works across the entire family, just by swapping in the right `μ`.

## GLMs vs. the algorithms in earlier files

| | GLMs | Decision Trees / SVM / k-NN |
|---|---|---|
| Assumes a specific output distribution? | yes (you choose it) | no |
| Relationship between features and target | linear (in the link space) | can be arbitrarily non-linear |
| Interpretability | high (coefficients have clear meaning) | varies (trees: high, SVM/k-NN: lower) |
| Handles counts, rates, proportions naturally? | yes, with the right link/family | not natively — needs preprocessing |
| Data efficiency | good with less data (fewer parameters, strong assumptions) | often needs more data |

## When to use GLMs

✅ Good for: when you know something about the *shape* of your target's
distribution (counts → Poisson, binary → Bernoulli, skewed positive →
Gamma), when interpretability matters, as principled extensions of linear
regression beyond continuous unbounded targets.

❌ Not ideal for: highly non-linear relationships between features and
target that can't be captured even after choosing a link function
(consider trees, SVM, or neural networks instead).

## The big-picture takeaway

```
                       ┌─────────────────────────┐
                       │   Generalized Linear      │
                       │   Models (GLMs)            │
                       └────────────┬────────────┘
                                    │  is the umbrella that contains...
              ┌──────────────────────┼──────────────────────┐
              ▼                      ▼                       ▼
     Linear Regression      Logistic Regression       Poisson/Gamma/...
     (file 03)               (file 04)                  Regression
```

Linear and logistic regression aren't two unrelated algorithms you had to
memorize separately — they're **two special cases of the exact same
underlying framework**, differing only in which distribution and link
function you plug in.
