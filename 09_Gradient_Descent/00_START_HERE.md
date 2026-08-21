# Gradient Descent — Complete Study Notes 🎓

Welcome! This folder is a self-contained mini-course on **Gradient Descent**,
the workhorse optimization algorithm behind almost every ML model you'll ever train
(linear regression, logistic regression, neural networks, transformers — all of it).

## How this pack is organized

| File | What's inside | Read time |
|---|---|---|
| `00_START_HERE.md` | This index | 2 min |
| `01_the_big_analogy.md` | Intuition via a hiker-in-the-fog analogy | 8 min |
| `02_math_foundations.md` | Cost functions, gradients, the update rule, worked numeric example | 15 min |
| `03_types_of_gradient_descent.md` | Batch vs Stochastic vs Mini-batch GD, ASCII path diagrams | 10 min |
| `04_learning_rate_and_convergence.md` | Learning rate tuning, divergence, convex vs non-convex surfaces | 10 min |
| `05_advanced_optimizers.md` | Momentum, AdaGrad, RMSProp, Adam — math + comparison table | 12 min |
| `06_python_implementation.py` | Runnable from-scratch NumPy code (Batch/SGD/Mini-batch + Momentum + Adam) | run it! |
| `07_demo_dataset.csv` | Small synthetic linear dataset used by the code | — |
| `08_practice_exercises.md` | Exercises + hints + solutions to test yourself | 15 min |
| `09_cheatsheet.md` | One-page formula + terminology cheat sheet | 3 min |

## Suggested learning path

```
 START
   │
   ▼
[01] Build intuition (the analogy)
   │
   ▼
[02] Learn the actual math (derivatives → gradient → update rule)
   │
   ▼
[03] See the 3 flavors of GD (Batch / SGD / Mini-batch)
   │
   ▼
[04] Understand learning rate & convergence pitfalls
   │
   ▼
[05] Level up to modern optimizers (Momentum → Adam)
   │
   ▼
[06] Run the code, watch it converge on real numbers
   │
   ▼
[08] Test yourself with exercises
   │
   ▼
[09] Keep the cheat sheet nearby forever
   │
   ▼
  DONE — you now understand what "model.fit()" is doing under the hood
```

## Quick TL;DR (if you only read one paragraph)

Gradient descent finds the values of a model's parameters that make its
predictions as wrong as possible... in the *least* wrong way. It does this by
repeatedly nudging each parameter a small step in the direction that reduces
error the fastest — like walking downhill in fog by always stepping toward
the steepest slope under your feet — until you can't go down any further.

```
θ_new = θ_old − α · ∇J(θ)
         ▲       ▲    ▲
         │       │    └── gradient: which way is "uphill"?
         │       └────── learning rate: how big a step?
         └────────────── the parameters we're learning
```

Enjoy the descent. 🏔️
