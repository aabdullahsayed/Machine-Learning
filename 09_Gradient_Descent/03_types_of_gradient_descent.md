# 03 — Batch vs Stochastic vs Mini-Batch Gradient Descent

All three variants use the exact same update rule
`θ := θ − α·∇J(θ)` — they only differ in **how much data** is used to
compute the gradient at each step.

## Analogy continued: how many hikers scout the slope?

- **Batch GD** — you send your *entire hiking group* out to feel the slope
  in every direction, average their readings, then everyone takes one step
  together. Accurate, but slow to organize each time.
- **Stochastic GD (SGD)** — you ask just *one random hiker* what the slope
  feels like under their feet, and the whole group steps based on that.
  Fast and cheap, but noisy — one hiker's local footing might not represent
  the true average slope.
- **Mini-batch GD** — you send a *small squad* (say, 32 hikers) to sample
  the slope and average their readings. A practical middle ground — the
  default in real-world deep learning.

## 1. Batch Gradient Descent

Uses **all `m` training examples** for every single update.

```
θ := θ − α · (1/m) Σ_{i=1}^{m} ∇J_i(θ)
```

- ✅ Stable, smooth convergence path
- ✅ Guaranteed to converge to the global minimum for convex problems
- ❌ Very slow / memory-heavy for large datasets (must load everything)
- ❌ One update per full pass through the data

## 2. Stochastic Gradient Descent (SGD)

Uses **exactly 1 random example** per update.

```
θ := θ − α · ∇J_i(θ)          for a randomly picked example i
```

- ✅ Very fast updates, works with huge/streaming datasets
- ✅ Noise can help escape shallow local minima
- ❌ Noisy, zig-zagging path — never fully "settles"
- ❌ Needs a decaying learning rate to truly converge

## 3. Mini-Batch Gradient Descent (the industry default)

Uses a **small batch** of `b` examples (commonly 32, 64, 128, 256).

```
θ := θ − α · (1/b) Σ_{i=1}^{b} ∇J_i(θ)
```

- ✅ Balances speed and stability
- ✅ Exploits vectorized/GPU hardware efficiently (batch matrix ops)
- ✅ Still has a *little* helpful noise to escape bad local minima
- ❌ Introduces a new hyperparameter: batch size

## ASCII comparison: path taken toward the minimum

```
Batch GD (smooth, direct)      SGD (noisy, jittery)        Mini-Batch (in between)

  start                          start                        start
    \                            /\  /\                          \
     \                          /  \/  \  /\                      \_
      \                        /       \/  \                       \_
       \                      /             \  /\                    \_
        \                    /               \/  \                     \_
         \___minimum          _______minimum       \___minimum           \___minimum
```

## Side-by-side comparison table

| Property | Batch GD | Stochastic GD | Mini-Batch GD |
|---|---|---|---|
| Examples per update | all `m` | 1 | `b` (e.g. 32–256) |
| Update frequency per epoch | 1 | `m` | `m/b` |
| Gradient estimate | exact | very noisy | moderately noisy |
| Convergence path | smooth curve | zig-zag | mostly smooth, some noise |
| Speed per update | slow | fast | fast (GPU-friendly) |
| Memory usage | high | very low | low–medium |
| Can escape local minima | rarely | often | sometimes |
| Typical use case | small datasets, convex problems | online/streaming learning | deep learning (default) |

## Epoch vs. iteration — don't confuse them

```
1 epoch = one full pass through the entire training set

Batch GD:      1 epoch = 1  update   (whole dataset used at once)
SGD:           1 epoch = m  updates  (one per example)
Mini-batch GD: 1 epoch = m/b updates (one per mini-batch)
```

Example: dataset of `m = 10,000` examples, batch size `b = 100`:

```
updates per epoch = 10,000 / 100 = 100 updates
```

## Rule of thumb for choosing

| Dataset size | Recommended variant |
|---|---|
| Small (fits in memory, < ~10k rows) | Batch GD is fine |
| Large / doesn't fit in memory | Mini-batch GD |
| Streaming / online data arriving continuously | SGD (or mini-batch with small `b`) |
| Deep learning (almost always) | Mini-batch GD (32–256), often with Adam (file 05) |
