# Descriptive Statistics

## Math Explanation

Descriptive statistics summarize a dataset with a few key numbers.

### Measures of central tendency
- **Mean**: `x̄ = (Σxᵢ) / n` — the average.
- **Median**: the middle value when sorted — robust to outliers (mean is not).
- **Mode**: the most frequently occurring value.

### Measures of spread
- **Range**: `max - min`.
- **Variance**: `Σ(xᵢ - x̄)² / n` (or `/(n-1)` for an unbiased "sample variance") — average squared deviation from the mean.
- **Standard deviation**: `√variance` — spread in the same units as the data.
- **Percentiles/Quartiles**: the value below which a given percentage of data falls (e.g., median = 50th percentile).

### Standardization (Z-score)
```
z = (x - μ) / σ
```
Rescales data to have mean 0 and standard deviation 1 — makes different features comparable regardless of their original scale/units.

## In ML/DL

- **Feature scaling/normalization** before training (especially for gradient-descent-based models and distance-based models like k-NN, SVM) is literally applying the Z-score formula to every feature:
```python
X_scaled = (X - X.mean(axis=0)) / X.std(axis=0)
```
Without this, features with large numeric ranges (e.g., income in dollars) can dominate features with small ranges (e.g., age in years) purely due to scale, not actual importance — and gradient descent converges much more slowly/unstably on unscaled data (see `05-Optimization/Gradient-Descent.md`).
- **Outlier detection**: often based on how many standard deviations a point is from the mean (e.g., flagging points beyond 3σ).
- **Exploratory Data Analysis (EDA)** — the first step of any real ML project — is essentially applying these descriptive statistics to understand your dataset's distribution, spread, and potential issues before modeling.
- **Batch/Layer Normalization** in deep learning computes exactly these statistics (mean, variance) on batches of activations during training to stabilize learning.
