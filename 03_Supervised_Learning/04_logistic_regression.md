# 04 — Logistic Regression

## Analogy: a "confidence dial," not a yes/no switch

Imagine a doctor examining a patient and deciding "is this tumor
malignant?" A good doctor doesn't just blurt out yes/no — they form a
**confidence level** first ("I'm 85% sure this is malignant") and only
then convert that confidence into a decision using some threshold
("above 50% confidence → treat as malignant"). Logistic regression works
exactly like this: it first computes a probability, then thresholds it
into a class.

```
Raw evidence  ──▶  Confidence dial  ──▶  Decision
(features x)        (probability,          (class label)
                      0% to 100%)
                                             
      "size=3cm,           "85% malignant"      "MALIGNANT"
       irregular            ────dial────►         (since 85% > 50%
       shape, ..."         0%    ▲    100%          threshold)
                                85%
```

## Why not just use linear regression for classification?

Linear regression outputs unbounded numbers (`-∞` to `+∞`), but
probabilities must live strictly between 0 and 1. We need a function that
**squashes** any real number into that range — enter the **sigmoid**.

```
Linear regression output              Sigmoid function
(can be ANY real number)               squashes it into (0, 1)

  z                                      σ(z)
  │                                      1 ┤              ______________
  │      ×                                 │           ╱‾
  │    ×                                   │         ╱
  │  ×                                     │       ╱
  │×          ×                       0.5 ─┤─────╱───────────────────
  │       ×                                │   ╱
  │            ×                           │ ╱
  │                 ×                    0 ┤______________
  └──────────────────── x                  └──────────────────── z
  unbounded, can't be                      always between 0 and 1 —
  read as a probability                    ready to be read as P(y=1)
```

## The sigmoid (logistic) function

```
σ(z) = 1 / (1 + e^(-z))
```

| z (input) | σ(z) (output) |
|---|---|
| -∞ | → 0 |
| 0 | 0.5 |
| +∞ | → 1 |
| large negative | close to 0 |
| large positive | close to 1 |

## The full model

```
z = θ0 + θ1·x1 + θ2·x2 + ... + θn·xn        (same linear combination as before!)
ŷ = σ(z) = 1 / (1 + e^(-z))                  (squash into a probability)

Predicted class = 1 if ŷ ≥ 0.5, else 0       (threshold, adjustable)
```

## The decision boundary

Because `σ(z) = 0.5` exactly when `z = 0`, the **decision boundary** is
where `θ0 + θ1·x1 + θ2·x2 + ... = 0` — a straight line (or hyperplane in
higher dimensions), same as linear regression's line, just now used to
*separate classes* instead of fit a trend.

```
  x2
   │      ●  ●
   │   ●    ●  ●         ● = class 1
   │  ●   ●               ╲
   │  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ╲──── decision boundary (z = 0)
   │        ○   ○            ╲
   │      ○    ○  ○           
   │    ○   ○                  ○ = class 0
   └──────────────────────── x1
```

## Why not use MSE as the cost function here?

Squared error with a sigmoid creates a **non-convex** cost surface (many
local minima), making gradient descent unreliable. Instead, logistic
regression uses **log loss / binary cross-entropy**, which is convex for
this model:

```
J(θ) = −(1/m) Σ [ y_i·log(ŷ_i) + (1−y_i)·log(1−ŷ_i) ]
```

### Why this particular formula? Intuition:

```
If true label y = 1:
   loss = −log(ŷ)         → loss is 0 when ŷ=1 (perfect), → ∞ as ŷ→0 (very wrong & confident)

If true label y = 0:
   loss = −log(1−ŷ)       → loss is 0 when ŷ=0 (perfect), → ∞ as ŷ→1 (very wrong & confident)
```

```
Loss
 │
 │\                              (y=1 case: −log(ŷ))
 │ \
 │  \
 │   \___
 │       \______
 │              \_____________
 └───────────────────────────── ŷ (predicted probability)
 0                            1
 (heavily penalizes confident WRONG predictions —
  this is what makes it a good training signal)
```

## Gradient of the cost function — surprisingly clean!

Despite the sigmoid non-linearity, the gradient of log loss w.r.t. θ turns
out to have the **exact same form** as linear regression's gradient:

```
∂J/∂θ_j = (1/m) Σ (ŷ_i − y_i)·x_ij
```

So the gradient descent update rule looks identical to linear regression's
— only the definition of `ŷ` (now passed through sigmoid) differs.

## Multi-class classification: Softmax Regression

For more than 2 classes, generalize with the **softmax function**, which
turns a vector of raw scores into a probability distribution over `K` classes:

```
P(y=k | x) = e^(z_k) / Σ_{j=1}^{K} e^(z_j)
```

```
Raw scores z:  [2.0, 1.0, 0.1]      (class A, B, C)
                    │
                    ▼ softmax
Probabilities:  [0.66, 0.24, 0.10]   (sums to 1.0)
                    │
                    ▼
Prediction: class A (highest probability)
```

## Evaluation metrics for classification

| Metric | Formula | Best for |
|---|---|---|
| Accuracy | `(TP+TN)/(total)` | balanced classes |
| Precision | `TP/(TP+FP)` | minimizing false alarms |
| Recall (Sensitivity) | `TP/(TP+FN)` | minimizing missed positives |
| F1 Score | `2·(Precision·Recall)/(Precision+Recall)` | balance of precision & recall |
| ROC-AUC | area under ROC curve | overall ranking quality across thresholds |

### Confusion matrix

```
                     Predicted
                  Positive  Negative
Actual Positive │   TP    │   FN    │
Actual Negative │   FP    │   TN    │
```

## When to use logistic regression

✅ Good for: binary/multi-class classification, when you want interpretable
probabilities (not just hard labels), as a strong, fast baseline, when
classes are roughly linearly separable.

❌ Not ideal for: highly non-linear decision boundaries (without feature
engineering or kernels — consider SVM/trees instead).
