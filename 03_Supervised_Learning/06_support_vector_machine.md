# 06 — Support Vector Machine (SVM)

## Analogy: the widest possible street between two neighborhoods

Imagine you need to draw a straight road separating two neighborhoods —
Team ● on one side, Team ○ on the other — such that the road is as
**wide** as possible without touching any house on either side. A wider
road gives more buffer/safety margin if a new house pops up near the
border. SVM does exactly this: instead of just finding *any* line that
separates the classes (like logistic regression might), it finds the one
**maximum-margin** line — the widest possible "street" between the two
classes.

```
   ●   ●
      ●    ●          ╲
   ●     ●              ╲   ←  margin boundary
                           ╲
   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ╲─ ─ ─ ─  ← the decision boundary (road center)
                               ╲
                                 ╲   ←  margin boundary
        ○    ○                    ╲
     ○     ○   ○
   ○    ○

   The "street" (margin) is as WIDE as possible while still
   keeping all ● on one side and all ○ on the other.
```

## Support vectors: the only points that matter

The houses (data points) **closest to the road** are the only ones that
determine where the road goes — these are called **support vectors**. All
other points further from the boundary could be moved or removed without
changing the decision boundary at all!

```
   ●   ●
      ●    ●
   ●     ●  ← this point IS a support vector (touches the margin)
   ●───────╲
             ╲
   ○──────────╲── ← this point IS a support vector (touches the margin)
        ○    ○ ╲
     ○     ○   ○
   ○    ○

   Points far from the boundary (upper-left ●'s, lower-right ○'s)
   don't influence the boundary at all — only the "close call" points do!
```

## The math: maximizing the margin

The decision boundary is `wᵀx + b = 0`. The margin width turns out to be
`2/‖w‖`. So maximizing the margin means **minimizing `‖w‖`** (equivalently
`½‖w‖²`, for convenient calculus), subject to every point being correctly
classified with some buffer:

```
minimize:    (1/2)‖w‖²

subject to:  y_i · (wᵀx_i + b) ≥ 1    for every training example i
```

This is the **hard-margin** SVM (assumes classes are perfectly separable).

## Soft margin: allowing some mistakes

Real data is rarely perfectly separable — a few points may sit on the
wrong side, or too close to the boundary. The **soft-margin** SVM adds a
slack variable `ξ_i` per point and a penalty `C` for violations:

```
minimize:    (1/2)‖w‖² + C · Σ ξ_i

subject to:  y_i · (wᵀx_i + b) ≥ 1 − ξ_i,     ξ_i ≥ 0
```

| `C` value | Effect |
|---|---|
| Large `C` | fewer allowed margin violations → narrower margin, may overfit |
| Small `C` | more tolerance for violations → wider margin, may underfit |

```
Large C (strict, narrow margin)      Small C (lenient, wide margin)

  ●   ●                                ●   ●
     ●  ╲                                 ●    ╲
  ●    ● ╲                             ●      ●  ╲
  ●──────╲                             ●─────────╲
          ╲○  ← misclassified                     ╲
  ○────────╲    point NOT tolerated      ○─────────╲○ ← misclassified point
       ○   ○╲                                  ○  ○ ╲   IS tolerated
    ○     ○                                 ○     ○  ╲
                                                        (wider street,
  (tries hard to get every                              small violations OK,
   point right — risk of overfit)                        often generalizes better)
```

## The kernel trick — handling non-linear data

Some data simply isn't separable by any straight line in its original
feature space. The **kernel trick** implicitly maps data into a
higher-dimensional space where it *becomes* linearly separable — without
ever explicitly computing that expensive high-dimensional transformation.

### Analogy: lifting a tangled 2D pattern into 3D

Imagine red dots forming a ring around blue dots on a flat table — no
straight line can separate them in 2D. But if you **lift** the red dots
upward (into a 3rd dimension) based on their distance from the center, a
flat plane sliding between them *can* now separate the two groups.

```
   2D (not linearly separable)         3D (lifted — NOW separable!)

     ○ ○ ○ ○ ○                                    ___________
   ○   ● ● ●   ○                                 /  ○  ○  ○  \    ← flat plane
   ○  ●  ●  ●  ○           lift red dots        │             │     slices between
   ○   ● ● ●   ○      ────  based on distance   │  ● ● ● ●    │     the two groups!
     ○ ○ ○ ○ ○         from center  ──────▶      \____________/
                                                    (● now "raised" in
   (● surrounded by ○,                              the middle, ○ stays low
    no line can separate)                            around the rim)
```

### Common kernels

| Kernel | Formula | Use case |
|---|---|---|
| Linear | `K(x,x') = xᵀx'` | data already linearly separable |
| Polynomial | `K(x,x') = (xᵀx' + c)^d` | curved/polynomial boundaries |
| RBF (Gaussian) | `K(x,x') = exp(−γ‖x−x'‖²)` | complex, smooth non-linear boundaries (most popular default) |
| Sigmoid | `K(x,x') = tanh(κxᵀx' + c)` | occasionally used, behaves like a neural network layer |

```
Linear kernel boundary          RBF kernel boundary (non-linear)

  ●   ●                            ○ ○ ○ ○ ○
     ●   ╲                       ○   ● ● ●   ○
  ●    ●  ╲                      ○  ●  ╱‾╲●  ○   ← curved boundary
  ────────╲                      ○   ● ╲_╱●   ○     wraps around the
  ○────────╲                       ○ ○ ○ ○ ○         cluster of ●'s
       ○   ○
```

## SVM for regression: SVR

Support Vector Regression flips the idea: instead of maximizing the margin
between classes, it tries to fit as many points as possible **within** a
margin of width `ε` around the predicted line, ignoring errors smaller
than `ε` and only penalizing points that fall outside that tube.

```
 y
  │           ×  ┌─────────────┐
  │        ×    ×│  ε-tube     │×
  │      ×      × │  around the │  ×
  │    ×        × │  fit line   │×
  │  ×          × └─────────────┘
  └──────────────────────────────── x
  (points within the ±ε tube incur NO penalty;
   only points outside the tube contribute to the loss)
```

## SVM vs. Logistic Regression vs. Decision Trees

| | Logistic Regression | SVM | Decision Trees |
|---|---|---|---|
| Boundary shape | linear (straight) | linear OR non-linear (via kernels) | axis-aligned rectangular regions |
| Handles non-linear data? | needs manual feature engineering | yes, naturally via kernels | yes, naturally |
| Sensitive to feature scaling? | yes | yes (very) | no |
| Output | probability | class label (or distance from margin) | class label / probability estimate |
| Works well with high-dimensional, sparse data? | yes | yes (especially linear kernel) | can struggle |
| Interpretability | high (coefficients) | low, especially with kernels | high (visualizable rules) |

## When to use SVM

✅ Good for: high-dimensional data (e.g. text classification), clear-margin
classification problems, small-to-medium datasets, when you need robust
performance with a well-chosen kernel.

❌ Not ideal for: very large datasets (training can be slow, roughly
`O(n²)` to `O(n³)`), noisy data with heavily overlapping classes,
situations needing well-calibrated probability outputs (though
`predict_proba` approximations exist).
