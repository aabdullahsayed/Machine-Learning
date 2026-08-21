# 07 — k-Nearest Neighbors (k-NN)

## Analogy: "you are the average of the people around you"

There's an old saying: "you're the average of the five people you spend
the most time with." k-NN takes this literally as a prediction strategy:
to guess something about a new person (or data point), look at the `k`
most *similar* people (or points) you already know about, and go with
whatever they mostly are (for classification) or their average value (for
regression).

```
Want to know: is this NEW house (★) expensive or affordable?

           $$$   $$$
         $$$       $$    $$$
              ★  ← new house, unknown price category
       $         $$
     $     $        $
           $

Look at the k=5 closest known houses to ★, and vote:
  → majority are "$$" (mid-range) → predict ★ is "$$" (mid-range)
```

## How k-NN actually works (it barely "trains" at all!)

k-NN is famously called a **"lazy learner"** — it does essentially no work
during training. It just **memorizes** the entire training dataset. All the
real computation happens at *prediction time*:

```
TRAINING PHASE (k-NN):                 PREDICTION PHASE (k-NN):

  "Here's the data."                     New point x_new arrives
        │                                        │
        ▼                                        ▼
  Model literally just              1. Compute distance from x_new
  stores the data.                     to EVERY training point
  (No fitting, no gradient                       │
   descent, nothing!)                            ▼
                                       2. Pick the k closest points
                                                  │
                                                  ▼
                                       3. Classification: majority vote
                                          Regression: average their y values
```

This is the opposite of, say, linear regression, which does all its work
upfront (fitting θ) and then predicts almost instantly.

## Distance metrics — how do we measure "closeness"?

| Metric | Formula | Notes |
|---|---|---|
| Euclidean | `√Σ(x_i − x'_i)²` | most common; straight-line distance |
| Manhattan | `Σ|x_i − x'_i|` | "city block" distance; robust to outliers |
| Minkowski | `(Σ|x_i − x'_i|^p)^(1/p)` | generalizes both (p=2 → Euclidean, p=1 → Manhattan) |
| Cosine | `1 − (x·x')/(‖x‖‖x'‖)` | measures angle, not magnitude — good for text/high-dim data |

```
Euclidean distance (straight line)      Manhattan distance ("taxicab" grid)

    A                                       A
    │\                                      │
    │ \                                     │
    │  \  ← direct diagonal path            └────── ← must move along
    │   \                                             grid lines only
    │    \                                   ┌
    └─────B                                  │
                                              B
    distance = √(Δx² + Δy²)                  distance = |Δx| + |Δy|
```

## Choosing k — the most important hyperparameter

```
k = 1 (very flexible, jagged boundary)    k = large (very smooth boundary)

  ●  ●○ ●                                    ●  ●  ●
  ● ○●○ ●   ← boundary wiggles                ●  ●  ●
  ●○●○ ○●     around every single point       ─────────  ← smooth, stable
  ○ ●○○ ●                                     ○  ○  ○     boundary
  ○ ○ ●○ ○                                    ○  ○  ○

  Low bias, HIGH variance                   HIGH bias, low variance
  (overfits — sensitive to noise,           (may underfit — ignores local
   single mislabeled point flips             detail, oversmooths real
   a whole region)                           patterns)
```

| k value | Bias | Variance | Risk |
|---|---|---|---|
| Small (e.g. k=1) | low | high | overfitting — very sensitive to noise/outliers |
| Large (e.g. k=n) | high | low | underfitting — approaches "always predict majority class" |
| Just right | balanced | balanced | best generalization (tune via cross-validation) |

**Rule of thumb:** try odd values of `k` for binary classification (avoids
tie votes), and use cross-validation to pick the best `k` for your data.

## Worked mini-example

Training data (2 features), want to classify new point `x_new = (3, 3)`:

| Point | (x1, x2) | Class | Distance to (3,3) |
|---|---|---|---|
| A | (1, 2) | ○ | √(4+1) = 2.24 |
| B | (2, 3) | ○ | √(1+0) = 1.00 |
| C | (4, 3) | ● | √(1+0) = 1.00 |
| D | (5, 5) | ● | √(4+4) = 2.83 |
| E | (3, 1) | ● | √(0+4) = 2.00 |

With `k = 3`, the 3 nearest neighbors are **B (1.00), C (1.00), E (2.00)**
→ votes: ○, ●, ● → majority = **●** → predict `x_new` is class ●.

## Why feature scaling is critical for k-NN

Distance calculations are dominated by whichever feature has the largest
numeric range — unscaled features can silently make k-NN ignore
important-but-small-scale features entirely.

```
Unscaled: income ($0–$200,000) vs. age (0–100)

distance ≈ dominated almost entirely by income differences
           (thousands of dollars swamp a few years of age difference)
           → age effectively IGNORED by the distance calculation!

Fix: scale both features (e.g. to 0–1 range or standardize to mean=0, std=1)
     BEFORE computing distances.
```

## k-NN for regression

Instead of a majority vote, average the `y` values of the k nearest
neighbors (optionally weighted by inverse distance, so closer neighbors
count more):

```
ŷ_new = (1/k) Σ_{i ∈ neighbors} y_i                    (simple average)

ŷ_new = Σ w_i·y_i / Σ w_i,  where w_i = 1/distance_i    (distance-weighted)
```

## The curse of dimensionality

As the number of features grows very large, all points start looking
roughly **equidistant** from each other — "nearest" neighbors stop being
meaningfully close, and k-NN's core assumption breaks down.

```
Low dimensions (2D)                High dimensions (100D+)

  points cluster naturally,        points spread out so much that
  clear "close" vs "far"           EVERY point is roughly the same
  neighbors exist                  distance from every other point —
                                    "nearest neighbor" becomes almost
  ×  ×                             meaningless!
    ×  ×
  ×    ×
```

**Mitigation:** dimensionality reduction (e.g. PCA) before applying k-NN,
or use distance metrics/feature selection suited to high dimensions.

## k-NN vs. other algorithms

| | k-NN | Linear/Logistic Regression | Decision Trees |
|---|---|---|---|
| Training cost | ~none (just stores data) | moderate (fit θ) | moderate (build tree) |
| Prediction cost | high (compare to all points) | very low (one formula) | low (traverse tree) |
| Assumes a functional form? | no (non-parametric) | yes (linear) | no (non-parametric) |
| Sensitive to feature scaling? | yes (very) | yes | no |
| Interpretability | medium ("here are similar examples") | high | high |
| Handles non-linear boundaries? | yes, naturally | no (without engineering) | yes, naturally |

## When to use k-NN

✅ Good for: small-to-medium datasets, when decision boundaries are
irregular/non-linear, as a simple, intuitive baseline, recommender-system-
style "similar items" problems.

❌ Not ideal for: very large datasets (slow prediction — must scan all
training data each time), high-dimensional data (curse of dimensionality),
situations needing fast real-time predictions.
