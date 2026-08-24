# 3. Gradient Descent (How Models Actually Learn)

This is the single most important algorithm in machine learning. If you understand this, you understand how ~90% of ML models are trained.

## 🔹 The Blindfolded Hiker Analogy

You're standing somewhere on a big bowl-shaped hill, blindfolded, and your goal is to reach the **lowest point** (the bottom of the valley). You can't see the whole hill, but at every step you can feel which direction is downhill.

Your strategy:
1. Feel the slope under your feet (compute the **gradient**)
2. Take a small step in the *downhill* direction
3. Repeat, feeling the new slope each time
4. Eventually you reach the bottom — where the ground feels flat (slope ≈ 0)

**That's gradient descent.** The "hill" is the error/loss function. The "bottom" is the set of weights that make the smallest possible error.

## 🔹 Putting It in ML Terms

| Hiker Analogy | ML Term |
|---|---|
| Your position on the hill | The model's current weights |
| Height of the hill at your spot | The error/loss (how wrong the model is) |
| Feeling the slope | Computing the gradient of the loss |
| Step direction (downhill) | **Negative** of the gradient |
| Step size | Learning rate |
| Reaching the bottom | The model is "trained" |

## 🔹 The Formula (don't be scared — it's simple)

```
new_weight = old_weight − (learning_rate × gradient)
```

That's it. Let's break down every piece:

- **old_weight**: where you currently are
- **gradient**: which way is "uphill" (increasing error) and how steep
- We move in the **opposite** direction of the gradient (hence the minus sign) because we want to go *downhill*, toward less error
- **learning_rate**: a small number (like 0.01) that controls step size — too big and you overshoot the valley; too small and it takes forever

## 🔹 A Tiny Worked Example

Let's say our loss function is `L(w) = (w - 4)²` — a bowl whose lowest point is at `w = 4`.

The gradient (derivative) of this is `2(w - 4)`.

Say we start at `w = 0`, with a learning rate of `0.1`:

| Step | w (current) | gradient = 2(w-4) | new w = w − 0.1×gradient |
|---|---|---|---|
| 1 | 0 | -8 | 0 − 0.1×(-8) = **0.8** |
| 2 | 0.8 | -6.4 | 0.8 − 0.1×(-6.4) = **1.44** |
| 3 | 1.44 | -5.12 | 1.44 − 0.1×(-5.12) = **1.95** |
| ... | ... | ... | ... |
| ~30 | ≈4.0 | ≈0 | **converged!** |

Notice `w` creeps closer and closer to `4` — the true minimum — with each step. That's gradient descent in action, on paper, with just algebra.

## 🔹 Why Not Just "Solve" for the Minimum Directly?

For simple problems like the one above, you could! But real ML models have **millions of weights** and very complicated, high-dimensional loss surfaces. There's no way to solve for the exact minimum directly — but taking small, repeated downhill steps *always* works and scales to any size problem. That generality is why gradient descent is everywhere in ML.

## 🔹 The 3 Flavors You'll Hear About

- **Batch Gradient Descent**: compute the gradient using *all* your data before each step (accurate but slow)
- **Stochastic Gradient Descent (SGD)**: use just *one* data point per step (fast but noisy/jumpy)
- **Mini-batch Gradient Descent**: use a small chunk (e.g. 32 data points) per step — the most common in practice, balancing speed and stability

## 🔹 What Can Go Wrong

- **Learning rate too high** → you overshoot the valley and bounce around, never settling (like taking huge leaps and jumping right over the bottom)
- **Learning rate too low** → training takes forever (like taking tiny inch-steps down a mountain)
- **Bumpy loss surfaces** → the hiker can get stuck in a small dip (a "local minimum") that isn't the true lowest point of the whole landscape

## 📝 Quick Recap
- Gradient descent = repeatedly step *downhill* on the error surface until the error is as small as possible
- Formula: `new_weight = old_weight − learning_rate × gradient`
- The gradient tells you direction + steepness; the learning rate controls how big your step is
- This one algorithm (in various forms) trains linear regression, logistic regression, and neural networks alike

👉 Go run this live in [`notebooks/gradient_descent_demo.ipynb`](notebooks/gradient_descent_demo.ipynb) to see it in action with actual code and a plot!

Next up: [04_supervised_learning.md](04_supervised_learning.md) — where gradient descent fits into the bigger picture.
