# Bayes' Theorem

## Math Explanation

Bayes' theorem tells you how to **update your belief** about something (a hypothesis) after observing new evidence:
```
P(H | E) = P(E | H) · P(H) / P(E)
```
- `P(H)`: **prior** — your belief about hypothesis H before seeing evidence
- `P(E | H)`: **likelihood** — how probable the evidence is, if H is true
- `P(E)`: **evidence** (a normalizing constant, ensures probabilities sum to 1)
- `P(H | E)`: **posterior** — your updated belief about H after seeing evidence E

### Worked example: medical test
A disease affects 1% of people. A test is 99% accurate (both for true positives and true negatives). If you test positive, what's the actual probability you have the disease?
```
P(Disease) = 0.01
P(Positive | Disease) = 0.99
P(Positive | No Disease) = 0.01  (false positive rate)

P(Positive) = P(Positive|Disease)P(Disease) + P(Positive|No Disease)P(No Disease)
            = 0.99*0.01 + 0.01*0.99 = 0.0198

P(Disease | Positive) = (0.99 * 0.01) / 0.0198 ≈ 0.50
```
**Surprising result**: even with a "99% accurate" test, a positive result only means ~50% actual probability of disease, because the disease is rare (this is the classic, widely-cited illustration of why Bayes' theorem matters — intuition about probability is often wrong without the math).

## In ML/DL

- **Naive Bayes classifiers** directly apply Bayes' theorem: `P(class | features) ∝ P(features | class) · P(class)`, using the "naive" independence assumption to make `P(features|class)` tractable as a product of per-feature probabilities.
- **Bayesian Machine Learning**: instead of learning one "best" set of parameters, treat parameters themselves as random variables with a **prior** distribution, then use Bayes' theorem to compute a **posterior** distribution over parameters after seeing training data — this naturally captures model uncertainty (crucial in high-stakes applications like medical diagnosis or autonomous driving).
```
P(parameters | data) ∝ P(data | parameters) · P(parameters)
      posterior              likelihood         prior
```
- **Regularization as a Bayesian prior**: L2 regularization is mathematically equivalent to placing a Gaussian prior on the weights (favoring small weights); L1 regularization corresponds to a Laplace prior (favoring sparsity). This is a deep and commonly-tested connection between optimization and Bayesian statistics.
- **Spam filters** (a classic early ML application) use Bayes' theorem directly: `P(spam | words in email)`, computed from `P(words | spam)` and the base rate `P(spam)`.
