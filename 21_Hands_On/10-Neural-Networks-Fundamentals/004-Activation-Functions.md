# 004 - Activation Functions

## Concept
Activation functions introduce non-linearity between layers. The choice affects training speed, gradient flow, and which layer type they're typically used in (hidden vs. output).

## Why It Matters
Picking the wrong activation is a common source of training failures — dead ReLUs, vanishing gradients with sigmoid/tanh in deep nets, or mismatched output activations for the task (e.g., sigmoid for multi-class).

## Hands-On

```python
import numpy as np
import matplotlib.pyplot as plt

z = np.linspace(-10, 10, 400)

def sigmoid(z): return 1 / (1 + np.exp(-z))
def tanh(z): return np.tanh(z)
def relu(z): return np.maximum(0, z)
def leaky_relu(z, alpha=0.01): return np.where(z > 0, z, alpha * z)
def softmax(z):
    exp_z = np.exp(z - np.max(z))  # subtract max for numerical stability
    return exp_z / exp_z.sum()

# 1. Plot each activation and its derivative
fig, axes = plt.subplots(2, 2, figsize=(10, 8))

axes[0,0].plot(z, sigmoid(z)); axes[0,0].set_title("Sigmoid")
axes[0,1].plot(z, tanh(z)); axes[0,1].set_title("Tanh")
axes[1,0].plot(z, relu(z)); axes[1,0].set_title("ReLU")
axes[1,1].plot(z, leaky_relu(z)); axes[1,1].set_title("Leaky ReLU")
plt.tight_layout()
plt.savefig("activations.png")
plt.close()

# 2. Compare derivative magnitudes - why sigmoid/tanh cause vanishing gradients
sig_deriv = sigmoid(z) * (1 - sigmoid(z))
tanh_deriv = 1 - tanh(z) ** 2
relu_deriv = (z > 0).astype(float)

print("Max sigmoid derivative:", sig_deriv.max())   # 0.25 - shrinks gradients fast when stacked
print("Max tanh derivative:", tanh_deriv.max())      # 1.0 but still squashes at extremes
print("Max ReLU derivative:", relu_deriv.max())      # 1.0, constant for z>0 - much better gradient flow

# 3. Demonstrate the "dying ReLU" problem
weights_bad_init = np.array([-5.0, -3.0, -1.0])  # large negative init pushes ReLU into 0 always
print("ReLU outputs with unlucky negative weights:", relu(weights_bad_init))
print("Leaky ReLU still passes some gradient:", leaky_relu(weights_bad_init))

# 4. Softmax for multi-class output layers
logits = np.array([2.0, 1.0, 0.1])
probs = softmax(logits)
print("Softmax probabilities:", probs, "sum:", probs.sum())  # sums to 1.0

# 5. GELU - used in modern transformers (approximate form)
def gelu(z):
    return 0.5 * z * (1 + np.tanh(np.sqrt(2/np.pi) * (z + 0.044715 * z**3)))

plt.plot(z, relu(z), label="ReLU")
plt.plot(z, gelu(z), label="GELU")
plt.legend()
plt.title("ReLU vs GELU")
plt.savefig("relu_vs_gelu.png")
```

## Exercise
1. Train the same MLP architecture from lesson 002 with `activation="tanh"` vs `"relu"` on a deeper network (5+ layers) — which converges faster?
2. Implement `swish(z) = z * sigmoid(z)` and plot it alongside ReLU and GELU.
3. Explain in your own words why softmax (not independent sigmoids) is used for the output layer of a single-label multi-class classifier.

## Key Takeaways
- **Hidden layers**: ReLU (and variants like Leaky ReLU, GELU) are the modern default — cheap to compute, mitigates vanishing gradients.
- **Output layer**: sigmoid for binary classification, softmax for multi-class (single label), linear (no activation) for regression.
- Sigmoid/tanh saturate at the extremes (derivative → 0), which is why they're mostly avoided in deep hidden stacks today.
