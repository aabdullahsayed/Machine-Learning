# 002 - Large Language Models Overview

## Concept
Large Language Models (LLMs) are Transformer-based models (usually decoder-only, like GPT) trained on massive text corpora to predict the next token, then adapted through fine-tuning and alignment techniques to follow instructions and converse helpfully.

## Why It Matters
LLMs are the most visible and impactful ML technology of the last few years. Understanding the pipeline from "next-token prediction" to "helpful assistant" demystifies both their remarkable abilities and their well-known limitations.

## Hands-On

```python
# pip install transformers torch --break-system-packages
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# 1. Load a small open GPT-2 model to see next-token prediction directly
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")
model.eval()

# 2. The core mechanism: predicting the next token's probability distribution
prompt = "The capital of France is"
input_ids = tokenizer.encode(prompt, return_tensors="pt")

with torch.no_grad():
    outputs = model(input_ids)
    next_token_logits = outputs.logits[0, -1, :]        # logits for the NEXT token
    next_token_probs = torch.softmax(next_token_logits, dim=-1)

top5 = torch.topk(next_token_probs, 5)
print("Top 5 next-token predictions:")
for prob, idx in zip(top5.values, top5.indices):
    print(f"  {tokenizer.decode([idx])!r}: {prob.item():.4f}")

# 3. Autoregressive generation - repeatedly predict the next token and append it
generated = model.generate(
    input_ids,
    max_new_tokens=20,
    do_sample=True,
    temperature=0.7,     # lower = more deterministic/repetitive, higher = more random
    top_k=50,             # only sample from the top 50 most likely tokens
    pad_token_id=tokenizer.eos_token_id,
)
print("\nGenerated text:", tokenizer.decode(generated[0], skip_special_tokens=True))

# 4. Temperature's effect on generation diversity
def generate_with_temperature(prompt, temperature):
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    output = model.generate(input_ids, max_new_tokens=15, do_sample=True,
                             temperature=temperature, pad_token_id=tokenizer.eos_token_id)
    return tokenizer.decode(output[0], skip_special_tokens=True)

for temp in [0.2, 0.7, 1.5]:
    print(f"\ntemperature={temp}: {generate_with_temperature('Once upon a time', temp)}")

# 5. Context window limitation - LLMs can only "see" a fixed number of tokens
print("\nGPT-2's max context length:", model.config.n_positions, "tokens")

# 6. Tokenization: LLMs don't see words, they see subword tokens
text = "unbelievable tokenization"
tokens = tokenizer.tokenize(text)
print("\nTokens:", tokens)   # notice rare words get split into pieces

# 7. Conceptual overview of the modern LLM training pipeline
"""
1. Pretraining: predict the next token on trillions of tokens of raw text (unsupervised).
   -> Produces a model that's fluent but not necessarily helpful or safe.

2. Supervised Fine-Tuning (SFT): fine-tune on curated (prompt, ideal response) pairs
   written by humans, teaching the model to follow instructions.

3. RLHF / preference optimization: humans rank multiple model outputs; a reward
   model (or direct preference optimization) is used to further align the model's
   responses with human preferences (helpful, honest, harmless).

4. (Optional) Additional fine-tuning for specific domains, tool use, or safety.
"""
```

## Exercise
1. Try 3 different prompts and compare how coherent the generations are at `temperature=0.3` vs `temperature=1.2`.
2. Look at the top-5 next-token predictions for an ambiguous prompt like "I went to the bank to" — does the model show any hint of understanding multiple meanings of "bank"?
3. Research (via a quick web search) one difference between GPT-2's architecture and a modern LLM's architecture (e.g., context length, number of parameters, training data size) and summarize it in 2-3 sentences.

## Key Takeaways
- At the core, an LLM is "just" predicting the next token, one at a time — the emergent capabilities (reasoning, following instructions) come from scale and the fine-tuning/alignment stages layered on top.
- Temperature and top-k/top-p sampling control the randomness of generation — this is a knob you control, not an inherent property of the model.
- Context window size is a hard architectural limit — this is why techniques like retrieval-augmented generation (RAG) exist, to bring relevant information into that limited window rather than relying on the model to "remember" everything.
