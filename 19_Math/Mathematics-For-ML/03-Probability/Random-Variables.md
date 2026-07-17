# Random Variables

## Math Explanation

A **random variable** is a variable whose value is the outcome of a random process — it's a function that maps outcomes of an experiment to numbers.

### Discrete vs Continuous
- **Discrete random variable**: takes countable values (e.g., number of heads in 10 coin flips: 0,1,2,...,10). Described by a **Probability Mass Function (PMF)**: `P(X = x)`.
- **Continuous random variable**: takes any value in a range (e.g., a person's height). Described by a **Probability Density Function (PDF)**: `f(x)`, where probability of a range is the area under the curve: `P(a ≤ X ≤ b) = ∫ₐᵇ f(x) dx`.

### Key properties
- PMF: `Σ P(X=x) = 1` over all possible values.
- PDF: `∫ f(x) dx = 1` over the entire domain (total probability must sum/integrate to 1).
- **CDF (Cumulative Distribution Function)**: `F(x) = P(X ≤ x)` — the probability the variable is at most `x`.

## In ML/DL

- **Model weights themselves are often treated as random variables** in Bayesian deep learning — instead of a single fixed value per weight, you maintain a distribution over plausible weight values, capturing uncertainty.
- **The output of a classification model IS a probability mass function** over the class labels — softmax outputs sum to 1, exactly satisfying the PMF property.
- **Generative models** (VAEs, GANs, diffusion models) are fundamentally about learning to sample from a complex, high-dimensional random variable (e.g., "the distribution of realistic images") using neural networks.
- **Random variables underpin the entire training process**: your training batches are (ideally) random samples from the true data distribution, and the loss you compute on a batch is itself a random variable — a noisy *estimate* of the true expected loss over the whole data distribution. This is precisely why training loss fluctuates batch-to-batch, and why techniques like batch averaging and learning rate scheduling exist to smooth out this noise.
