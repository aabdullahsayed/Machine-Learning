# 001 - Attention Mechanism Deep Dive

## Concept
This lesson goes deeper than module 13's introduction, covering the full scaled dot-product attention formula, why scaling matters, causal (masked) attention for autoregressive generation, and how attention patterns can be inspected and interpreted.

## Why It Matters
Attention is the single mechanism responsible for most of the recent leaps in NLP and increasingly in vision (Vision Transformers). A precise, hands-on understanding of it pays off across nearly every modern architecture you'll encounter.

## Hands-On

```python
import numpy as np
import torch
import torch.nn.functional as F
import matplotlib.pyplot as plt

# 1. The full scaled dot-product attention formula, step by step
def scaled_dot_product_attention(Q, K, V, mask=None):
    d_k = Q.shape[-1]
    scores = Q @ K.transpose(-2, -1) / np.sqrt(d_k)   # (seq_len, seq_len)

    if mask is not None:
        scores = scores.masked_fill(mask == 0, float("-inf"))

    weights = F.softmax(scores, dim=-1)
    output = weights @ V
    return output, weights

seq_len, d_k = 6, 16
torch.manual_seed(0)
Q = torch.randn(seq_len, d_k)
K = torch.randn(seq_len, d_k)
V = torch.randn(seq_len, d_k)

output, weights = scaled_dot_product_attention(Q, K, V)
print("Output shape:", output.shape)
print("Attention weights sum per row (should be 1.0):", weights.sum(dim=-1))

# 2. Why scale by sqrt(d_k)? Without it, large d_k pushes softmax into saturated, near-one-hot regions
def compare_scaling(d_k_values=[8, 64, 512]):
    for d_k in d_k_values:
        Q = torch.randn(1, d_k)
        K = torch.randn(seq_len, d_k)
        raw_scores = Q @ K.T
        scaled_scores = raw_scores / np.sqrt(d_k)
        print(f"d_k={d_k}: raw score std={raw_scores.std():.2f}, scaled score std={scaled_scores.std():.2f}")

compare_scaling()

# 3. Causal (masked) attention - used in GPT-style decoders so token t can't see future tokens
def causal_mask(seq_len):
    return torch.tril(torch.ones(seq_len, seq_len))   # lower-triangular = 1, rest = 0

mask = causal_mask(seq_len)
print("\nCausal mask (1 = can attend, 0 = masked):")
print(mask)

causal_output, causal_weights = scaled_dot_product_attention(Q, K, V, mask=mask)
plt.imshow(causal_weights.detach().numpy(), cmap="viridis")
plt.title("Causal Attention Weights (upper triangle masked)")
plt.colorbar()
plt.savefig("causal_attention.png")
plt.close()

# 4. Multi-head attention from scratch - splitting Q, K, V into multiple smaller subspaces
class MultiHeadAttentionScratch(torch.nn.Module):
    def __init__(self, d_model, num_heads):
        super().__init__()
        assert d_model % num_heads == 0
        self.num_heads = num_heads
        self.d_head = d_model // num_heads
        self.Wq = torch.nn.Linear(d_model, d_model)
        self.Wk = torch.nn.Linear(d_model, d_model)
        self.Wv = torch.nn.Linear(d_model, d_model)
        self.Wo = torch.nn.Linear(d_model, d_model)

    def forward(self, x, mask=None):
        batch, seq_len, d_model = x.shape
        Q = self.Wq(x).view(batch, seq_len, self.num_heads, self.d_head).transpose(1, 2)
        K = self.Wk(x).view(batch, seq_len, self.num_heads, self.d_head).transpose(1, 2)
        V = self.Wv(x).view(batch, seq_len, self.num_heads, self.d_head).transpose(1, 2)

        scores = Q @ K.transpose(-2, -1) / np.sqrt(self.d_head)
        if mask is not None:
            scores = scores.masked_fill(mask == 0, float("-inf"))
        weights = F.softmax(scores, dim=-1)
        attended = weights @ V

        attended = attended.transpose(1, 2).contiguous().view(batch, seq_len, d_model)
        return self.Wo(attended)

mha_scratch = MultiHeadAttentionScratch(d_model=64, num_heads=8)
x = torch.randn(2, 10, 64)
out = mha_scratch(x)
print("\nMulti-head attention (from scratch) output shape:", out.shape)

# 5. Cross-attention (used in encoder-decoder models) vs self-attention
# Self-attention: Q, K, V all come from the SAME sequence
# Cross-attention: Q comes from the decoder, K and V come from the encoder's output
def cross_attention_demo():
    decoder_state = torch.randn(1, 5, 64)   # decoder's queries
    encoder_output = torch.randn(1, 10, 64)  # encoder's keys/values (different seq_len is fine!)
    output, weights = scaled_dot_product_attention(decoder_state[0], encoder_output[0], encoder_output[0])
    print("Cross-attention output shape:", output.shape, "(matches decoder seq_len, not encoder's)")

cross_attention_demo()
```

## Exercise
1. Verify empirically that without the `1/sqrt(d_k)` scaling, softmax outputs become increasingly one-hot (nearly all weight on a single position) as `d_k` grows — print `weights.max()` with and without scaling at `d_k=512`.
2. Visualize the attention weights from `MultiHeadAttentionScratch` for 2 different heads on the same input — do different heads attend to noticeably different patterns?
3. Implement "sliding window attention" (each position only attends to its k nearest neighbors) as a mask variant, and explain why this might be used for very long sequences.

## Key Takeaways
- Scaling by `sqrt(d_k)` keeps the dot products in a range where softmax gradients don't vanish — without it, training becomes unstable at higher dimensions.
- Causal masking is what makes GPT-style models autoregressive — at generation time, position t genuinely cannot see positions after it, only during training does the mask enforce this artificially over the full sequence at once.
- Multi-head attention isn't just "attention done multiple times" — each head projects into its own smaller subspace, letting different heads specialize in different types of relationships (e.g., one head tracking syntax, another tracking coreference).
