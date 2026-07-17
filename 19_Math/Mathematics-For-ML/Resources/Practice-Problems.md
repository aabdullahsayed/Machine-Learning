# Extra Practice Problems (Cross-Topic)

Short exercises that combine multiple folders — good for a final review pass.

## 1. Derive MSE loss's gradient by hand
For `L(w) = (1/n)Σ(yᵢ - wxᵢ)²`, derive `∂L/∂w` by hand using the chain rule. Verify with `sympy` or PyTorch autograd.

## 2. Connect entropy to decision trees
Given a dataset with a binary label split `60% class A, 40% class B`, compute the entropy by hand. Then simulate a split that produces two child nodes: one `90% A, 10% B` and one `20% A, 80% B`. Compute the information gain of this split.

## 3. Implement logistic regression completely from scratch
Combine: the sigmoid function (`02-Calculus/Derivatives.md`), binary cross-entropy loss (`06-Information-Theory/Cross-Entropy.md`), its gradient (derived via chain rule), and gradient descent (`05-Optimization/Gradient-Descent.md`) — no libraries except NumPy. Train it on a small toy binary classification dataset and confirm it converges.

## 4. Explain regularization through 3 different lenses
For L2 regularization specifically, explain it in your own words from: (a) the loss-function-penalty perspective, (b) the constrained-optimization perspective (`05-Optimization/Lagrange-Multipliers.md`), and (c) the Bayesian-prior perspective (`03-Probability/Bayes-Theorem.md`). Confirm all three describe the same underlying mathematical object.

## 5. PCA vs SVD, hands-on
Implement PCA two different ways on the same dataset: (a) via eigendecomposition of the covariance matrix, (b) via direct SVD of the centered data matrix. Confirm both give the same principal components (up to sign flips).

## 6. Diagnose a training curve
Given a plot where training loss keeps decreasing but validation loss starts increasing after epoch 20, explain (using bias-variance vocabulary) what's happening, and list 3 concrete interventions from this repo (`05-Optimization`, `07-ML-Applications/Regularization.md`) that would address it.

## 7. Full "math to code" trace
Pick any one modern loss function (e.g., focal loss, or triplet loss) not covered explicitly in this repo. Research its mathematical formula, and write a short explanation connecting it back to concepts from this repo (entropy? MLE? a distance/norm? a probability distribution assumption?).

✅ These problems intentionally force you to connect ideas across folders — that's the actual skill being tested in ML interviews and real research/engineering work.
