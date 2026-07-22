# 004 - Self-Supervised Learning

## Concept
Self-supervised learning trains models using labels automatically derived from the data itself (no human annotation needed) — for example, predicting masked words, predicting the next frame in a video, or recognizing whether two augmented views come from the same image.

## Why It Matters
Labeled data is expensive and limited; unlabeled data is abundant. Self-supervised pretraining (BERT's masked language modeling, GPT's next-token prediction, contrastive image learning) is how nearly every modern large model gets its foundational capabilities before any task-specific fine-tuning.

## Hands-On

```python
import torch
import torch.nn as nn
import numpy as np

# ============================================
# 1. Masked Language Modeling (the pretext task behind BERT)
# ============================================
# pip install transformers --break-system-packages
from transformers import BertTokenizer, BertForMaskedLM

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
mlm_model = BertForMaskedLM.from_pretrained("bert-base-uncased")
mlm_model.eval()

text = "The [MASK] sat on the mat."
input_ids = tokenizer.encode(text, return_tensors="pt")
mask_idx = (input_ids == tokenizer.mask_token_id).nonzero()[0, 1].item()

with torch.no_grad():
    logits = mlm_model(input_ids).logits

top5 = torch.topk(logits[0, mask_idx], 5)
print("Top 5 predictions for the masked token:")
for score, idx in zip(top5.values, top5.indices):
    print(f"  {tokenizer.decode([idx])!r}: {score.item():.2f}")
# The model never saw a human-labeled "correct answer" - the label IS the original
# word, automatically hidden and revealed. This is the self-supervision.

# ============================================
# 2. Contrastive learning for images (SimCLR-style idea, simplified)
# ============================================
# Core idea: two augmented views of the SAME image should have similar embeddings;
# views from DIFFERENT images should have dissimilar embeddings.

def contrastive_loss(embeddings_a, embeddings_b, temperature=0.5):
    """
    embeddings_a, embeddings_b: (batch_size, embed_dim) - two augmented views
    of the same batch of images, paired by index.
    """
    embeddings_a = nn.functional.normalize(embeddings_a, dim=1)
    embeddings_b = nn.functional.normalize(embeddings_b, dim=1)

    # Cosine similarity between all pairs (a_i, b_j)
    similarity_matrix = embeddings_a @ embeddings_b.T / temperature

    # The "label" for row i is index i - matching pairs are on the diagonal,
    # generated automatically from the batch structure, no human annotation needed
    labels = torch.arange(embeddings_a.size(0))
    loss = nn.functional.cross_entropy(similarity_matrix, labels)
    return loss

batch_size, embed_dim = 8, 32
torch.manual_seed(0)
view_a = torch.randn(batch_size, embed_dim)
view_b = view_a + torch.randn(batch_size, embed_dim) * 0.1   # simulate "augmented but related" views

loss = contrastive_loss(view_a, view_b)
print("\nContrastive loss (related views):", loss.item())

unrelated_b = torch.randn(batch_size, embed_dim)   # completely unrelated embeddings
loss_unrelated = contrastive_loss(view_a, unrelated_b)
print("Contrastive loss (unrelated views):", loss_unrelated.item())
# Loss should be lower when views are actually related, confirming the mechanism works

# ============================================
# 3. Next-token prediction (GPT's pretext task) - the label is just "the next word"
# ============================================
sentence = "self supervised learning uses the data itself as the label"
words = sentence.split()

# Each (input, target) pair is generated automatically from raw text
training_pairs = [(words[:i], words[i]) for i in range(1, len(words))]
for inp, target in training_pairs[:5]:
    print(f"Input: {' '.join(inp)!r} -> Predict: {target!r}")

# ============================================
# 4. Why this matters for downstream fine-tuning
# ============================================
"""
After self-supervised pretraining, the model has learned general-purpose
representations (of language, or of images) WITHOUT any task-specific labels.
Fine-tuning (module 13-005, module 11-003) then adapts these representations
to a specific labeled task using far fewer labeled examples than would be
needed to train from scratch.
"""
```

## Exercise
1. Try masking a different word in the BERT example and see if the top predictions make sense given the sentence.
2. Extend `contrastive_loss` to handle a batch where some "augmented" pairs are corrupted (very different from their original) and verify the loss increases accordingly.
3. Write out, in your own words, why next-token prediction counts as "self-supervised" rather than "unsupervised" (hint: think about whether there's a label at all, and where it comes from).

## Key Takeaways
- The defining trick of self-supervised learning is generating labels automatically from the structure of unlabeled data (mask a word, compare augmented views, predict the next token) rather than needing human annotation.
- This is precisely why massive pretraining is possible: the "labels" scale with the amount of raw data available, not with expensive human labeling effort.
- Self-supervised pretraining followed by supervised fine-tuning on a smaller labeled dataset is the dominant modern paradigm across both NLP (module 13) and vision (module 11).
