# 006 - Probability and Statistics Essentials

## Concept
ML is fundamentally about modeling uncertainty. This lesson covers distributions, expectation/variance, conditional probability & Bayes' theorem, and the Central Limit Theorem — the statistical backbone of Naive Bayes (module 05), evaluation metrics (module 06), and probabilistic outputs from classifiers.

## Why It Matters
Concepts like "confidence," "likelihood," and "p-value" appear throughout ML. Bayes' theorem specifically underlies an entire classification algorithm (Naive Bayes) and the intuition behind model calibration.

## Hands-On

```python
import numpy as np
from scipy import stats

# 1. Descriptive statistics
data = np.array([23, 45, 12, 67, 34, 89, 21, 56, 43, 78])
print("Mean:", np.mean(data))
print("Median:", np.median(data))
print("Std Dev:", np.std(data))
print("Variance:", np.var(data))

# 2. Probability distributions
# Normal (Gaussian) distribution - the most common assumption in ML
normal_samples = np.random.normal(loc=0, scale=1, size=1000)
print("Sample mean:", normal_samples.mean(), "| Sample std:", normal_samples.std())

# PDF value at x=0 for a standard normal
pdf_at_0 = stats.norm.pdf(0, loc=0, scale=1)
print("PDF at x=0:", pdf_at_0)

# 3. Bayes' Theorem - P(A|B) = P(B|A) * P(A) / P(B)
# Classic example: disease testing
p_disease = 0.01          # prior: 1% of population has disease
p_positive_given_disease = 0.95   # test sensitivity
p_positive_given_healthy = 0.05   # false positive rate

p_positive = (p_positive_given_disease * p_disease +
              p_positive_given_healthy * (1 - p_disease))
p_disease_given_positive = (p_positive_given_disease * p_disease) / p_positive
print(f"P(disease | positive test) = {p_disease_given_positive:.4f}")
# Note how low this is despite a 95% accurate test - base rate matters!

# 4. Central Limit Theorem - sample means approach normality regardless of
# the original distribution, which is why many ML assumptions rely on it
population = np.random.exponential(scale=2.0, size=100_000)  # skewed distribution
sample_means = [np.mean(np.random.choice(population, size=50)) for _ in range(1000)]
print("Sample means mean:", np.mean(sample_means))
print("Sample means std:", np.std(sample_means))

# 5. Hypothesis testing - t-test (used to compare model performance)
group_a = np.random.normal(50, 10, 100)  # model A scores
group_b = np.random.normal(53, 10, 100)  # model B scores
t_stat, p_value = stats.ttest_ind(group_a, group_b)
print(f"t-stat: {t_stat:.3f}, p-value: {p_value:.4f}")
if p_value < 0.05:
    print("Statistically significant difference between models")
else:
    print("No significant difference detected")
```

## Exercise
1. Simulate 10,000 coin flips (`np.random.binomial(1, 0.5, 10000)`) and verify the sample mean converges to 0.5.
2. Modify the Bayes' theorem example: what happens to `P(disease | positive)` if the prior `p_disease` drops to 0.001? Explain why in one sentence.
3. Run a paired t-test comparing two arrays of cross-validation scores from module 06 to determine if one model is significantly better.

## Key Takeaways
- Bayes' theorem shows why base rates dominate rare-event predictions — critical for imbalanced classification (module 07).
- The Central Limit Theorem justifies why we trust sample-based metrics (like cross-validation scores) to estimate true performance.
- A p-value tells you about statistical significance, not practical importance — always look at effect size too.
