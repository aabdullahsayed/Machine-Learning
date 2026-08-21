# Supervised Learning — Complete Study Notes 🎓

A self-contained mini-course covering the core ideas and algorithms of
supervised learning — with analogies, math, ASCII diagrams, tables, runnable
code, and demo datasets.

## Folder contents

| File | What's inside | Read time |
|---|---|---|
| `00_START_HERE.md` | This index | 2 min |
| `01_how_supervised_learning_works.md` | The core loop: data → model → prediction → feedback | 10 min |
| `02_why_model_works_on_new_data.md` | Generalization, overfitting/underfitting, bias-variance | 12 min |
| `03_linear_regression.md` | Predicting numbers — math + analogy + diagram | 10 min |
| `04_logistic_regression.md` | Predicting categories via probabilities | 10 min |
| `05_decision_tree_learning.md` | Learning by asking yes/no questions | 10 min |
| `06_support_vector_machine.md` | Maximum-margin classifiers | 10 min |
| `07_k_nearest_neighbors.md` | "You are the average of your neighbors" | 8 min |
| `08_generalized_linear_models.md` | The umbrella that connects linear/logistic/Poisson regression | 10 min |
| `09_python_implementations.py` | Runnable scikit-learn + from-scratch code for every algorithm above | run it! |
| `10_regression_dataset.csv` | Demo dataset for regression algorithms | — |
| `11_classification_dataset.csv` | Demo dataset for classification algorithms | — |
| `12_cheatsheet.md` | One-page formula & decision cheat sheet | 3 min |

## Suggested learning path

```
 START
   │
   ▼
[01] How supervised learning works (the big picture loop)
   │
   ▼
[02] Why trained models generalize to new data (the real goal)
   │
   ▼
[03] Linear Regression  ─┐
[04] Logistic Regression │  the "regression family"
[08] GLMs               ─┘  (ties 03 & 04 together, generalizes further)
   │
   ▼
[05] Decision Trees      ─┐
[06] SVM                  │  other core algorithm families
[07] k-Nearest Neighbors ─┘
   │
   ▼
[09] Run the code — see every algorithm fit real (small) datasets
   │
   ▼
[12] Keep the cheat sheet nearby forever
   │
   ▼
  DONE
```

## Quick TL;DR

Supervised learning means: **learn a mapping from inputs to outputs using
examples where we already know the correct answer**, so that later, when
given a *new* input we've never seen, the model can predict its output.

```
   ┌───────────────┐        ┌────────────┐        ┌───────────────┐
   │ Labeled data   │  ──▶  │  Learning   │  ──▶   │  Model f(x)    │
   │ (x, y) pairs   │        │  Algorithm  │        │  ready to      │
   │ "questions +   │        │  (finds     │        │  predict on    │
   │  answer key"   │        │  patterns)  │        │  NEW inputs    │
   └───────────────┘        └────────────┘        └───────────────┘
```

| If your output `y` is... | You're doing... | Example algorithms |
|---|---|---|
| A continuous number | **Regression** | Linear Regression, GLMs |
| A category / class label | **Classification** | Logistic Regression, Decision Trees, SVM, k-NN |

Enjoy the journey from raw data to predictive intelligence. 🚀
