# 01 — How Supervised Learning Works

## Analogy: studying with flashcards (and an answer key)

Imagine learning a new language using flashcards. Each card has a word on
the front (the **input**) and its correct translation on the back (the
**label**, or correct answer). You flip through hundreds of cards,
guessing the translation, then checking the back to see if you were right.
Over time, you start noticing patterns — certain endings mean "plural,"
certain prefixes mean "opposite of," etc. Eventually, you can translate a
**word you've never seen before** because you've learned the *underlying
patterns*, not just memorized the specific cards.

That's exactly what supervised learning is:

```
 Flashcard front (input x)        Flashcard back (label y)
   "casa"                    ⟷        "house"
   "perro"                   ⟷        "dog"
   "rápido"                  ⟷        "fast"
        │
        ▼
   Model studies many (x, y) pairs, extracts patterns
        │
        ▼
   Given a NEW word "gato" (never seen before)
        │
        ▼
   Model predicts: "cat"  ✅ (generalized from patterns, e.g. that
                                many animal words end certain ways)
```

## The formal loop

```
        ┌─────────────────────────────────────────────────────────┐
        │                     TRAINING PHASE                       │
        │                                                           │
        │   Labeled Data                                            │
        │   {(x1,y1), (x2,y2), ..., (xm,ym)}                        │
        │         │                                                 │
        │         ▼                                                 │
        │   ┌─────────────┐        predictions ŷ                    │
        │   │   Model      │ ─────────────────────┐                 │
        │   │  f(x; θ)     │                       ▼                │
        │   └─────────────┘             ┌───────────────────┐       │
        │         ▲                     │  Compare ŷ vs. y   │       │
        │         │                     │  (Loss function)   │       │
        │         │                     └─────────┬──────────┘       │
        │         │                                │                │
        │         └──────── adjust θ ◀─────────────┘                │
        │              (e.g. via gradient descent)                  │
        └─────────────────────────────────────────────────────────┘
                                    │
                                    ▼  (training complete, θ fixed)
        ┌─────────────────────────────────────────────────────────┐
        │                    INFERENCE PHASE                       │
        │                                                           │
        │   New, unseen input x_new                                 │
        │         │                                                 │
        │         ▼                                                 │
        │   ┌─────────────┐                                         │
        │   │   Model      │ ───▶  Prediction ŷ_new                 │
        │   │  f(x; θ*)    │                                         │
        │   └─────────────┘                                         │
        └─────────────────────────────────────────────────────────┘
```

## The four essential ingredients

| Ingredient | Role | Example (house price prediction) |
|---|---|---|
| **Data** `(x, y)` | Examples with known correct answers | `x` = sq. footage, bedrooms; `y` = sale price |
| **Model** `f(x; θ)` | A parameterized function that maps input → output | `price = θ0 + θ1·sqft + θ2·bedrooms` |
| **Loss function** `L(ŷ, y)` | Measures how wrong a prediction is | Mean Squared Error |
| **Learning algorithm** | Adjusts `θ` to reduce the loss | Gradient Descent (see the companion Gradient Descent notes!) |

## Regression vs. Classification — the two flavors

```
                    SUPERVISED LEARNING
                    /                  \
                   /                    \
          REGRESSION                CLASSIFICATION
      (predict a number)         (predict a category)
              │                           │
    "What will the temperature      "Is this email spam
     be tomorrow?" → 24.5°C          or not spam?" → {spam, not spam}
              │                           │
      e.g. Linear Regression        e.g. Logistic Regression,
           GLMs                          Decision Trees, SVM, k-NN
```

| | Regression | Classification |
|---|---|---|
| Output type | continuous number | discrete label/category |
| Example task | predict house price | predict if a tumor is malignant/benign |
| Typical loss | Mean Squared Error | Cross-Entropy / Log Loss |
| Example algorithms | Linear Regression, GLMs | Logistic Regression, Decision Trees, SVM, k-NN |

## A minimal end-to-end example (conceptual)

```
Step 1: Collect labeled data
   x = house square footage      y = sale price ($)
   1000                          200,000
   1500                          280,000
   2000                          360,000
   ...

Step 2: Choose a model family
   price = θ0 + θ1 * sqft        (a simple linear model)

Step 3: Choose a loss function
   J(θ) = mean squared error between predicted and actual prices

Step 4: Train (minimize loss, e.g. with gradient descent)
   θ0, θ1 converge to values that fit the data well

Step 5: Predict on new, unseen houses
   new house: 1750 sqft  →  predicted price = θ0 + θ1*1750
```

## Key vocabulary

| Term | Meaning |
|---|---|
| Feature(s) | The input variable(s), `x` (also called predictors/independent variables) |
| Label / Target | The correct output, `y` (also called dependent variable) |
| Training set | Labeled examples used to fit the model |
| Test set | Held-out labeled examples used only to *evaluate* the final model |
| Hypothesis / Model | The function `f(x; θ)` being learned |
| Parameters `θ` | The numbers the learning algorithm tunes |
| Loss / Cost function | Measures prediction error, guides training |
| Inference | Using a trained model to predict on new data |

Next up: file `02` explains the single most important question in all of
ML — *why does a model trained on old data work on data it's never seen?*
