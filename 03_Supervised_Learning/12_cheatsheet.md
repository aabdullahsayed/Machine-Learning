# 12 — Supervised Learning Cheat Sheet

## The big picture

```
Labeled data (x, y)  ──▶  Learning algorithm  ──▶  Model f(x;θ)  ──▶  Predict on NEW x
```

## Regression vs. Classification

| | Regression | Classification |
|---|---|---|
| Output | continuous number | discrete category |
| Loss | MSE / RMSE / MAE | Log Loss / Cross-Entropy |
| Algorithms here | Linear Regression, GLMs | Logistic Regression, Trees, SVM, k-NN |

## Generalization essentials

| Concept | One-liner |
|---|---|
| Overfitting | model memorizes noise; low train error, high test error |
| Underfitting | model too simple; high error on both train and test |
| Bias-Variance | `Error = Bias² + Variance + Irreducible Noise` |
| Train/Val/Test split | never evaluate on data the model trained on |
| Regularization (L1/L2) | penalizes large weights to reduce overfitting |

## Algorithm-by-algorithm quick reference

| Algorithm | Predicts | Core idea | Key hyperparameter(s) | Strength | Weakness |
|---|---|---|---|---|---|
| **Linear Regression** | number | best-fit straight line, minimize MSE | none / regularization `λ` | interpretable, fast | assumes linearity |
| **Logistic Regression** | category (via probability) | sigmoid-squashed linear combo, minimize log loss | regularization `C`/`λ` | interpretable, gives probabilities | linear boundary only |
| **Decision Tree** | number or category | recursive yes/no splits, maximize purity gain | `max_depth`, `min_samples_leaf` | interpretable, non-linear, mixed feature types | overfits if unconstrained |
| **SVM** | category (or number w/ SVR) | maximize margin between classes | `C`, `kernel`, `gamma` | strong in high-dim, kernel trick for non-linear data | slow on large datasets |
| **k-NN** | number or category | vote/average of k nearest points | `k`, distance metric | simple, no training, non-linear | slow prediction, curse of dimensionality |
| **GLM (general)** | number/count/rate/etc. | linear predictor + link function + distribution | choice of `family` + `link` | principled, flexible for non-Gaussian targets | still assumes a linear relationship (in link space) |

## Formulas at a glance

```
Linear Regression:     ŷ = θ0 + θ1x1 + ... + θnxn
Cost (MSE):             J(θ) = (1/2m)Σ(ŷ-y)²

Logistic Regression:   ŷ = σ(θᵀx) = 1/(1+e^(-θᵀx))
Cost (Log Loss):        J(θ) = -(1/m)Σ[y·log(ŷ) + (1-y)·log(1-ŷ)]

Decision Tree split:   Gini = 1 - Σp_k²      Entropy = -Σp_k·log2(p_k)

SVM objective:         minimize (1/2)‖w‖² + CΣξ_i
                        s.t. y_i(wᵀx_i+b) ≥ 1-ξ_i

k-NN prediction:       classification: majority vote of k nearest
                        regression: ŷ = (1/k)Σ y_i  of k nearest

GLM:                   g(μ) = θᵀx   (link function connects linear
                                      predictor to distribution mean)
```

## Decision boundary shapes (mental picture)

```
Linear/Logistic Regression       Decision Tree               SVM (RBF kernel)          k-NN
      ╲                            ┌──┬──┐                     ___                    (irregular,
       ╲                           │  │  │                    /   \                    follows local
        ╲  (straight line)         └──┴──┘  (rectangles)      \___/  (smooth curve)     point density)
```

## Choosing an algorithm — quick decision guide

```
Is the target a continuous number?
   │
  YES ──▶ Is the relationship roughly linear?
   │           │
   │          YES ──▶ Linear Regression (or GLM if non-Gaussian noise)
   │           │
   │           NO ──▶ Decision Tree / Ensemble, or engineer polynomial features
   │
  NO (categorical target) ──▶ Need probabilities / interpretability?
                                  │
                                 YES ──▶ Logistic Regression
                                  │
                                 NO ──▶ Non-linear boundary needed?
                                            │
                                           YES ──▶ SVM (kernel) / Decision Tree / k-NN
                                            │
                                           NO ──▶ Logistic Regression (simplest, fast)
```

## Evaluation metrics cheat sheet

| Task | Metric | Formula / Notes |
|---|---|---|
| Regression | RMSE | `√[(1/m)Σ(ŷ-y)²]` — same units as target |
| Regression | R² | fraction of variance explained (1.0 = perfect) |
| Classification | Accuracy | `(TP+TN)/total` — misleading on imbalanced data |
| Classification | Precision | `TP/(TP+FP)` — minimize false alarms |
| Classification | Recall | `TP/(TP+FN)` — minimize missed positives |
| Classification | F1 | harmonic mean of precision & recall |

## Preprocessing checklist

| Step | Needed for |
|---|---|
| Feature scaling (standardize/normalize) | Logistic Regression, SVM, k-NN, GLMs (gradient-based fit) — **not** needed for Decision Trees |
| Handle missing values | all algorithms |
| Encode categorical variables | all algorithms (trees can sometimes handle natively) |
| Train/test split | all algorithms, always |
| Check class balance | classification tasks especially |

Keep this page open as you experiment — it summarizes 90% of what you need
day to day when choosing and applying a supervised learning algorithm.
