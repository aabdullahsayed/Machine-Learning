# 004 - Intro to Transformers

## Concept
The Transformer replaces recurrence entirely with self-attention: every token in a sequence directly attends to every other token in one step, weighted by learned relevance scores. This solves the long-sequence gradient problems of RNNs and enables massive parallelization during training.

## Why It Matters
Transformers are the architecture behind BERT, GPT, and virtually all modern large language models. Understanding self-attention is the single most important concept for understanding how today's LLMs actually work.

## Hands-On

```python
import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt

# 1. Self-attention, implemented from scratch (the mathematical heart of the Transformer)
def self_attention(Q, K, V):
    """
    Q, K, V: (seq_len, d_k) - Query, Key, Value matrices for one sequence
    Returns: attention output and the attention weight matrix
    """
    d_k = Q.shape[-1]
    scores = Q @ K.T / np.sqrt(d_k)              # scaled dot-product similarity
    weights = np.exp(scores) / np.exp(scores).sum(axis=-1, keepdims=True)  # softmax
    output = weights @ V
    return output, weights

np.random.seed(0)
seq_len, d_model = 5, 8
X = np.random.randn(seq_len, d_model)   # 5 tokens, 8-dim embeddings

# Learnable projection matrices (normally trained; random here for illustration)
Wq = np.random.randn(d_model, d_model) * 0.1
Wk = np.random.randn(d_model, d_model) * 0.1
Wv = np.random.randn(d_model, d_model) * 0.1

Q, K, V = X @ Wq, X @ Wk, X @ Wv
output, attn_weights = self_attention(Q, K, V)

print("Attention weight matrix (each row sums to 1):")
print(np.round(attn_weights, 2))

plt.imshow(attn_weights, cmap="viridis")
plt.colorbar(label="Attention weight")
plt.xlabel("Key position (attended TO)")
plt.ylabel("Query position (attending FROM)")
plt.title("Self-Attention Weights")
plt.savefig("attention_heatmap.png")
plt.close()

# 2. Multi-head attention using PyTorch's built-in module
d_model, num_heads = 64, 8
mha = nn.MultiheadAttention(embed_dim=d_model, num_heads=num_heads, batch_first=True)

x = torch.randn(1, 10, d_model)  # (batch=1, seq_len=10, d_model=64)
attn_output, attn_weights_torch = mha(x, x, x)   # self-attention: Q=K=V=x
print("\nMulti-head attention output shape:", attn_output.shape)
print("Attention weights shape:", attn_weights_torch.shape)  # (batch, seq_len, seq_len)

# 3. Positional encoding - Transformers have no inherent notion of order, so we add it
def positional_encoding(seq_len, d_model):
    pos = np.arange(seq_len)[:, np.newaxis]
    i = np.arange(d_model)[np.newaxis, :]
    angle_rates = 1 / np.power(10000, (2 * (i // 2)) / d_model)
    angles = pos * angle_rates
    pe = np.zeros((seq_len, d_model))
    pe[:, 0::2] = np.sin(angles[:, 0::2])
    pe[:, 1::2] = np.cos(angles[:, 1::2])
    return pe

pe = positional_encoding(seq_len=20, d_model=64)
plt.imshow(pe, cmap="RdBu", aspect="auto")
plt.xlabel("Embedding dimension")
plt.ylabel("Position in sequence")
plt.title("Positional Encoding Pattern")
plt.colorbar()
plt.savefig("positional_encoding.png")

# 4. A minimal Transformer encoder block using PyTorch's built-in layer
encoder_layer = nn.TransformerEncoderLayer(d_model=64, nhead=8, dim_feedforward=256, batch_first=True)
transformer_encoder = nn.TransformerEncoder(encoder_layer, num_layers=2)

sample_input = torch.randn(2, 10, 64)  # (batch=2, seq_len=10, d_model=64)
encoded = transformer_encoder(sample_input)
print("\nTransformer encoder output shape:", encoded.shape)  # same shape as input
```

## Exercise
1. Modify `self_attention` to add a causal mask (set upper-triangular scores to `-inf` before softmax) so each position can only attend to earlier positions — this is what GPT-style decoders use.
2. Change `num_heads` in the multi-head attention example to 1, 4, and 16 — confirm `d_model` must be divisible by `num_heads`.
3. Plot two different rows of the positional encoding matrix and explain why nearby positions produce similar-but-distinct patterns.

## Key Takeaways
- Self-attention computes a weighted average of all tokens' values, where the weights are learned similarity scores between queries and keys — this is fundamentally different from RNNs' step-by-step processing.
- Multi-head attention runs several attention computations in parallel with different learned projections, letting the model attend to different types of relationships simultaneously (e.g., syntax vs. semantics).
- Because attention has no built-in sense of order, positional encodings must be added to the input embeddings so the model knows token positions.
