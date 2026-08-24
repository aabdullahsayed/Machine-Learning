# 2. Calculus Basics (How a Model Knows It's Wrong — and by How Much)

You don't need advanced calculus for ML — just **one idea**: the derivative (slope).

## 🔹 What is a Derivative, really?

Imagine you're walking on a hill blindfolded. You can't see anything, but you can *feel* whether the ground under your feet is sloping up or down, and how steep it is.

**The derivative is exactly that feeling** — it tells you:
- Which direction is "uphill" or "downhill"
- How steep the slope is at your current spot

In math terms, if you have a function `y = f(x)`, the derivative `dy/dx` tells you how much `y` changes when you nudge `x` a tiny bit.

## 🔹 A Simple Example

Say `f(x) = x²` (a bowl shape 🥣). The derivative of `x²` is `2x`.

| x | f(x) = x² | slope = 2x | meaning |
|---|---|---|---|
| -3 | 9 | -6 | steep, pointing down-left |
| 0 | 0 | 0 | flat — the bottom of the bowl! |
| 3 | 9 | 6 | steep, pointing up-right |

Notice: the slope is **0 exactly at the lowest point**. This is the single most important fact for ML — the bottom of a bowl-shaped curve is where the slope is zero, and that bottom is often what we're trying to find.

## 🔹 Why ML Cares About Slopes

In ML, we define an **error function** (also called a *loss function*) that measures how wrong our model's predictions are. It usually looks like a bowl:

- High points on the bowl = bad predictions (big errors)
- The very bottom of the bowl = the best possible predictions (smallest error)

The derivative tells the model: *"you are currently on this part of the slope — move this way to go downhill toward less error."*

## 🔹 Partial Derivatives (don't panic, same idea)

Real ML models have many weights, not just one `x`. A **partial derivative** just means: "find the slope with respect to *one* weight, while pretending all the others are constant for a moment." We do this for every weight, one at a time, and collectively call the result the **gradient**.

> **Gradient** = a list of slopes, one for each weight, all pointing in the direction of *steepest increase* in error.

## 📝 Quick Recap
- **Derivative** = the slope at a point = "which way is downhill and how steep"
- ML's error function is shaped like a bowl — we want to reach the bottom
- **Gradient** = the slope for *every* weight at once, bundled into one vector

Next up: [03_gradient_descent.md](03_gradient_descent.md) — using this slope info to actually train a model.
