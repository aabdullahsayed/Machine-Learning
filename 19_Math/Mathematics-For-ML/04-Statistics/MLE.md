# Maximum Likelihood Estimation (MLE)

## Math Explanation

**MLE** is a method for estimating the parameters of a probability distribution that make the **observed data most probable**.

### The idea
Given data `x1, x2, ..., xn` assumed to come from a distribution with unknown parameter(s) `θ`, the **likelihood** function is:
```
L(θ) = P(x1, x2, ..., xn | θ) = Π P(xᵢ | θ)     (product, assuming independent samples)
```
MLE finds:
```
θ_MLE = argmax_θ  L(θ)
```

### Log-likelihood (a practical trick)
Products of many small probabilities cause numerical underflow, and are harder to differentiate. Since `log` is monotonically increasing, maximizing `L(θ)` is equivalent to maximizing `log L(θ)`, which turns the product into a **sum**:
```
log L(θ) = Σ log P(xᵢ | θ)
```
This is why you'll almost always see "log-likelihood" in practice, not raw likelihood.

### Worked example: MLE for a Gaussian's mean
Given data assumed Gaussian with known `σ`, unknown `μ`, maximizing the log-likelihood with respect to `μ` (by taking the derivative, setting to 0) gives:
```
μ_MLE = (1/n) Σ xᵢ    ← just the sample mean!
```
This confirms something intuitive: the "best" estimate of a Gaussian's mean, in the MLE sense, is simply the average of your observed data.

## In ML/DL

- **Nearly every standard loss function IS derived from maximum likelihood estimation** — this is one of the deepest, most important connections in ML theory:
  - **Mean Squared Error (MSE)** loss for regression is exactly the MLE solution if you assume your data has Gaussian-distributed noise around the true value.
  - **Cross-entropy loss** for classification is exactly the MLE solution if you assume your data follows a Categorical/Bernoulli distribution (i.e., it's the negative log-likelihood of the correct class).
- **This means "minimizing the loss function" during training and "performing MLE" are, in most standard setups, literally the same mathematical operation**, just framed differently — minimizing negative log-likelihood = maximizing log-likelihood = maximizing likelihood.
```python
# Cross-entropy loss IS negative log-likelihood of the true class
import numpy as np
predicted_probs = np.array([0.7, 0.2, 0.1])   # model's softmax output
true_class = 0                                    # ground truth class index
nll_loss = -np.log(predicted_probs[true_class])     # this is literally the cross-entropy loss
```
- **Understanding this connection explains WHY certain loss functions are the "natural" choice** for certain problems — MSE isn't arbitrary for regression, and cross-entropy isn't arbitrary for classification; both are principled consequences of assuming a specific noise/output distribution and applying MLE.
- **Logistic regression** is derived entirely via MLE under a Bernoulli-distributed output assumption.
