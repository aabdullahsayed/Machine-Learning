# Vectors

## Math Explanation

A **vector** is an ordered list of numbers representing a point (or direction) in space.
```
v = [v1, v2, ..., vn]  ∈ ℝⁿ
```
Example: `v = [3, 4]` is a point in 2D space, or an arrow from the origin `(0,0)` to `(3,4)`.

### Key operations
- **Addition**: `[1,2] + [3,4] = [4,6]` (element-wise)
- **Scalar multiplication**: `2 * [1,2] = [2,4]`
- **Dot product**: `a · b = Σ aᵢbᵢ = a1*b1 + a2*b2 + ... + an*bn` → returns a **scalar**
- **Magnitude (L2 norm)**: `||v|| = √(v1² + v2² + ... + vn²)` — the vector's length
- **Unit vector**: `v / ||v||` — same direction, length 1

### Geometric meaning of the dot product
```
a · b = ||a|| ||b|| cos(θ)
```
- If `a · b = 0` → vectors are **orthogonal** (perpendicular, 90°)
- If `a · b > 0` → vectors point in a "similar" direction (angle < 90°)
- If `a · b < 0` → vectors point in "opposite" directions (angle > 90°)

## In ML/DL

- **Every data point is a vector.** A row in your dataset (features: age, income, height) is literally a vector in ℝⁿ.
- **Word embeddings** (Word2Vec, GloVe, BERT) represent words as vectors in high-dimensional space — "king" and "queen" are vectors close together because their dot product/cosine similarity is high.
- **Cosine similarity** (used everywhere in NLP/recommendation systems) is exactly the `cos(θ)` from the dot-product formula above:
```python
import numpy as np
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
```
- **A neuron's weighted sum** `w1*x1 + w2*x2 + ... + b` is literally a dot product `w · x + b` — the fundamental operation in every neural network layer.
- **Weight vectors** in linear models (logistic regression, linear regression) define a direction in feature space; the model's prediction is a dot product between weights and input features.
