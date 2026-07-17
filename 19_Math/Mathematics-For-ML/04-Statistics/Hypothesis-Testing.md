# Hypothesis Testing

## Math Explanation

Hypothesis testing is a formal framework for deciding whether an observed effect in data is likely "real" or could plausibly be due to random chance.

### The framework
1. **Null hypothesis (H0)**: the "boring" default assumption (e.g., "there's no difference between A and B").
2. **Alternative hypothesis (H1)**: what you're trying to find evidence for (e.g., "B is better than A").
3. Compute a **test statistic** and a **p-value**: the probability of seeing data this extreme (or more extreme) *if* the null hypothesis were actually true.
4. If `p-value < significance level (commonly 0.05)` → **reject the null hypothesis** — the effect is considered "statistically significant."

### Important nuance
A small p-value does NOT mean "the alternative hypothesis is true with high probability" — it means "if there were truly no effect, seeing data this extreme would be unlikely." This is a commonly misunderstood distinction, worth internalizing carefully.

### Type I and Type II errors
| | H0 is actually True | H0 is actually False |
|---|---|---|
| **Reject H0** | Type I Error (false positive) | Correct |
| **Fail to reject H0** | Correct | Type II Error (false negative) |

## In ML/DL

- **A/B testing model deployments**: when you deploy a new model version and want to know if it *really* improves a business metric (click-through rate, conversion) or if the observed improvement is just noise, you run a formal hypothesis test comparing the two groups' outcomes.
- **Comparing two models' performance**: is Model A's 92.3% accuracy *really* better than Model B's 91.8%, or is that difference just noise from the specific test set? Statistical significance testing (e.g., a paired t-test across cross-validation folds) answers this rigorously, rather than trusting a single number.
- **Feature selection**: statistical tests (chi-squared test, ANOVA) can help identify which features have a statistically significant relationship with the target variable before feeding them into a model.
- **Understanding "statistically significant improvement" claims** in ML research papers requires this exact framework — a paper claiming a new architecture is "better" should ideally show this improvement is significant across multiple runs/seeds, not a single lucky training run.

```python
from scipy import stats
# Compare accuracy scores from 2 models across 10 cross-validation folds
model_a_scores = [0.91, 0.92, 0.90, 0.93, 0.91, 0.92, 0.90, 0.91, 0.92, 0.91]
model_b_scores = [0.93, 0.94, 0.92, 0.95, 0.93, 0.94, 0.92, 0.93, 0.94, 0.93]
t_stat, p_value = stats.ttest_rel(model_a_scores, model_b_scores)
print(f"p-value: {p_value}")   # p < 0.05 -> difference is likely statistically significant
```
