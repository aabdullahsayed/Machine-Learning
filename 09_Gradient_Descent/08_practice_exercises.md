# 08 — Practice Exercises

Test your understanding. Hints are collapsed-style (just don't scroll past
them until you've tried!). Solutions are at the bottom of each section.

---

### Exercise 1 — By hand

Given `x = [1, 2]`, `y = [3, 5]`, `θ0 = 0`, `θ1 = 0`, `α = 0.1`.
Compute `θ0` and `θ1` after **one** batch gradient descent step.

**Hint:** predictions `ŷ = θ0 + θ1·x` are both 0 initially, so the errors
are simply `-y`.

<details><summary>Solution</summary>

```
ŷ = [0, 0]
errors e = ŷ - y = [-3, -5]

∂J/∂θ0 = mean(e) = (-3 + -5)/2 = -4
∂J/∂θ1 = mean(e * x) = (-3*1 + -5*2)/2 = (-3 -10)/2 = -6.5

θ0 := 0 - 0.1*(-4)   = 0.4
θ1 := 0 - 0.1*(-6.5) = 0.65
```
</details>

---

### Exercise 2 — Conceptual

Why does gradient descent use `θ − α∇J(θ)` and not `θ + α∇J(θ)`?

<details><summary>Solution</summary>

The gradient points in the direction of **steepest increase**. Since we
want to *minimize* the cost, we must move in the exact opposite direction
— hence the minus sign. Using `+` would be "gradient ascent," which
maximizes the function instead (useful in different contexts, e.g. some
reinforcement learning policy-gradient methods!).
</details>

---

### Exercise 3 — Diagnosing training curves

You train a model and log the loss every iteration. Which learning-rate
problem (too high / too low / good) does each curve suggest?

```
Curve A:  9.1, 5.4, 3.2, 2.0, 1.3, 0.9, 0.7, ...   (steadily shrinking)
Curve B:  9.1, 8.9, 8.8, 8.7, 8.6, 8.6, 8.5, ...   (barely moving)
Curve C:  9.1, 15.3, 40.2, 220.9, NaN               (blowing up)
```

<details><summary>Solution</summary>

- Curve A: **good learning rate** — smooth, healthy decrease.
- Curve B: **too small** — decreasing, but painfully slowly.
- Curve C: **too large** — diverging, eventually overflowing to NaN.
</details>

---

### Exercise 4 — Code

Using `06_python_implementation.py` as a base, modify `minibatch_gd` to
accept `batch_size=1` and confirm it behaves (numerically) like
`stochastic_gd`. Then try `batch_size=len(x)` and confirm it matches
`batch_gd`. What does this tell you about the relationship between the
three variants?

<details><summary>Solution</summary>

Mini-batch GD is really a **generalization**: batch size `1` = SGD, and
batch size `= m` (the full dataset) = Batch GD. They're all the same
algorithm; only the amount of data averaged per gradient step differs.
</details>

---

### Exercise 5 — Adam intuition

Two parameters, A and B. Parameter A's gradient has been consistently
`[0.9, 1.0, 0.95, 1.05]` over the last few steps (large & steady).
Parameter B's gradient has been `[0.01, -0.02, 0.03, -0.01]` (small &
noisy/oscillating). Which parameter will Adam effectively apply a
*larger* relative step to, and why?

<details><summary>Solution</summary>

Adam divides the step by `√v̂` — the root of the accumulated **squared**
gradients. Parameter A has large, consistent gradients → large `v̂` → its
effective step is *scaled down*. Parameter B has small gradients → small
`v̂` → its effective step is *scaled up* (relatively). This is exactly
why Adam is good with sparse/uneven gradient magnitudes across
parameters — it equalizes progress across dimensions.
</details>

---

### Exercise 6 — Open-ended

Explain, in your own words (2–3 sentences, no formulas), why training a
model with a *very* large batch size might make training slower in
wall-clock time despite needing *fewer* total updates.

<details><summary>Solution (one valid answer)</summary>

Each individual update becomes much more expensive to compute since it
processes many more examples before taking a single step, and if the
batch no longer fits efficiently in memory/GPU cache you lose the
speed benefits of vectorization/parallelism — so even though you need
fewer *updates* overall, each one takes proportionally longer, and you
also lose some of the beneficial "noise" that helps escape local
minima/saddle points faster.
</details>

---

## Self-check summary

| # | Topic tested |
|---|---|
| 1 | Manual gradient computation |
| 2 | Sign of the update rule |
| 3 | Reading loss curves |
| 4 | Batch/SGD/Mini-batch equivalence |
| 5 | Adam's per-parameter adaptivity |
| 6 | Batch size trade-offs in practice |
