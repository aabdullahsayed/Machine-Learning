# 4. Supervised Learning (Easy Explanation)

## 🔹 The Core Idea

Supervised learning is like learning with **flashcards that have the answer on the back**.

You show the model many examples where you already know the correct answer. The model looks for patterns connecting the "question" (input) to the "answer" (output). Once trained, you show it a *new* question it's never seen, and it guesses the answer using the patterns it learned.

> **Supervised** = a "supervisor" (you) already knows and provides the correct answers during training.

## 🔹 The Two Main Types

### 1. Regression — predicting a **number**
The answer is a continuous value.

**Example:** Predicting a house's price from its size, location, and age.
- Input (features): `[1500 sqft, 3 bedrooms, 10 years old]`
- Output (label): `$280,000`

### 2. Classification — predicting a **category**
The answer is one of a fixed set of labels.

**Example:** Deciding if an email is spam or not.
- Input (features): word counts, sender info, links present
- Output (label): `Spam` or `Not Spam`

## 🔹 How Training Actually Works (step by step)

1. **Collect labeled data** — pairs of (input, correct answer)
2. **Make a guess** — the model starts with random weights and predicts an answer
3. **Measure the error** — compare the guess to the real answer using a loss function
4. **Improve** — use **gradient descent** (see file 03!) to nudge the weights so the guess gets a little closer to correct
5. **Repeat** steps 2–4 thousands of times across all your data
6. **Done** — the model's weights now encode the pattern; use it on new, unseen data

```
 Data → Predict → Measure Error → Gradient Descent Adjusts Weights → Repeat
   ↑____________________________________________________________________|
```

## 🔹 A Mini Real Example: Predicting Exam Scores from Study Hours

| Study Hours | Exam Score (actual) |
|---|---|
| 1 | 50 |
| 2 | 55 |
| 3 | 65 |
| 4 | 70 |
| 5 | 85 |

We want a simple line: `score = weight × hours + bias`

- The model **guesses** starting weights, e.g. `weight = 0`, `bias = 0` → predicts `score = 0` for everyone (very wrong!)
- It measures the error against real scores
- **Gradient descent** slowly adjusts `weight` and `bias` step by step
- After training, it might land on something like `weight ≈ 8.5`, `bias ≈ 42` → now predictions are close to the real scores
- Now if a new student studies for `6` hours, the model predicts: `8.5 × 6 + 42 ≈ 93`

This is exactly the toy example built out fully, with code, in the notebook!

## 🔹 Supervised vs Other Types (just for context)

| Type | Has labeled answers? | Example |
|---|---|---|
| **Supervised** | ✅ Yes | Predict house prices, detect spam |
| Unsupervised | ❌ No | Group customers into segments (no "correct" grouping given) |
| Reinforcement | Learns from rewards, not fixed answers | A robot learning to walk by trial & error |

*(This guide focuses only on supervised learning, as requested — the other two are just here for context.)*

## 📝 Quick Recap
- Supervised learning = learning from labeled examples (question + correct answer)
- **Regression** predicts numbers; **Classification** predicts categories
- Training = guess → measure error → use gradient descent to improve → repeat
- The "learning" in machine learning **is** gradient descent adjusting weights to reduce error

👉 Now open the notebook and watch this whole process happen with real numbers: [`notebooks/gradient_descent_demo.ipynb`](notebooks/gradient_descent_demo.ipynb)
