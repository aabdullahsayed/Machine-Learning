# 003 - Sequence-to-Sequence Models

## Concept
A Seq2Seq model maps an input sequence to an output sequence of possibly different length, using an encoder (compresses the input into a context representation) and a decoder (generates the output step by step from that context). Attention lets the decoder look back at all encoder states instead of relying on one fixed-size summary.

## Why It Matters
This architecture is the foundation of machine translation, text summarization, and chatbots, and it's the direct conceptual ancestor of the Transformer (module 13), which replaced the RNN encoder/decoder with attention entirely.

## Hands-On

```python
import torch
import torch.nn as nn
import random

# Toy task: reverse a sequence of digits, e.g., [1,2,3,4] -> [4,3,2,1]
# This is small enough to train quickly while showing the full seq2seq mechanism.

VOCAB_SIZE = 10       # digits 0-9
SOS_TOKEN = 10        # start-of-sequence marker
EOS_TOKEN = 11
VOCAB_SIZE_WITH_TOKENS = 12

def make_reverse_dataset(n_samples=500, seq_len=5):
    data = []
    for _ in range(n_samples):
        seq = [random.randint(0, 9) for _ in range(seq_len)]
        target = seq[::-1]
        data.append((seq, target))
    return data

dataset = make_reverse_dataset()

# 1. Encoder - compresses the input sequence into a final hidden state
class Encoder(nn.Module):
    def __init__(self, vocab_size, hidden_size):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, hidden_size)
        self.gru = nn.GRU(hidden_size, hidden_size, batch_first=True)

    def forward(self, x):
        embedded = self.embedding(x)
        outputs, hidden = self.gru(embedded)
        return outputs, hidden   # outputs needed for attention; hidden is the summary

# 2. Decoder with simple attention - looks back at ALL encoder outputs, not just the summary
class AttentionDecoder(nn.Module):
    def __init__(self, vocab_size, hidden_size):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, hidden_size)
        self.gru = nn.GRU(hidden_size * 2, hidden_size, batch_first=True)
        self.attn = nn.Linear(hidden_size * 2, 1)
        self.out = nn.Linear(hidden_size, vocab_size)

    def forward(self, input_token, hidden, encoder_outputs):
        embedded = self.embedding(input_token)                     # (batch, 1, hidden)

        # Compute attention scores: how relevant is each encoder output to the current decoder state?
        seq_len = encoder_outputs.size(1)
        hidden_expanded = hidden.permute(1, 0, 2).repeat(1, seq_len, 1)
        attn_input = torch.cat([hidden_expanded, encoder_outputs], dim=2)
        attn_scores = self.attn(attn_input).squeeze(2)              # (batch, seq_len)
        attn_weights = torch.softmax(attn_scores, dim=1)

        # Weighted sum of encoder outputs = "context vector" for this decoding step
        context = torch.bmm(attn_weights.unsqueeze(1), encoder_outputs)  # (batch, 1, hidden)

        gru_input = torch.cat([embedded, context], dim=2)
        output, hidden = self.gru(gru_input, hidden)
        prediction = self.out(output.squeeze(1))
        return prediction, hidden, attn_weights

# 3. Training loop with teacher forcing (feed the TRUE previous token during training)
hidden_size = 32
encoder = Encoder(VOCAB_SIZE_WITH_TOKENS, hidden_size)
decoder = AttentionDecoder(VOCAB_SIZE_WITH_TOKENS, hidden_size)

params = list(encoder.parameters()) + list(decoder.parameters())
optimizer = torch.optim.Adam(params, lr=0.005)
criterion = nn.CrossEntropyLoss()

def train_step(seq, target, teacher_forcing_ratio=0.5):
    optimizer.zero_grad()
    seq_t = torch.tensor(seq).unsqueeze(0)
    target_t = torch.tensor(target + [EOS_TOKEN]).unsqueeze(0)

    encoder_outputs, hidden = encoder(seq_t)
    decoder_input = torch.tensor([[SOS_TOKEN]])
    loss = 0

    for t in range(target_t.size(1)):
        prediction, hidden, _ = decoder(decoder_input, hidden, encoder_outputs)
        loss += criterion(prediction, target_t[:, t])
        use_teacher_forcing = random.random() < teacher_forcing_ratio
        decoder_input = target_t[:, t].unsqueeze(1) if use_teacher_forcing else prediction.argmax(1, keepdim=True)

    loss.backward()
    optimizer.step()
    return loss.item() / target_t.size(1)

for epoch in range(30):
    total_loss = 0
    for seq, target in dataset:
        total_loss += train_step(seq, target)
    if epoch % 5 == 0:
        print(f"Epoch {epoch}: avg loss={total_loss/len(dataset):.4f}")
```

## Exercise
1. After training, write an `evaluate(seq)` function that decodes greedily (no teacher forcing) and check if the model correctly reverses a new sequence like `[7, 2, 9, 0, 4]`.
2. Visualize the attention weights (`attn_weights`) for one example as a heatmap — do they align diagonally-reversed, as you'd expect for a reversal task?
3. Try `teacher_forcing_ratio=1.0` vs `0.0` — which trains faster, and which generalizes better at inference time (when there's no ground truth to "cheat" with)?

## Key Takeaways
- Encoder-decoder architectures separate "understanding the input" (encoder) from "generating the output" (decoder), letting input and output sequences have different lengths.
- Attention solves the "one fixed-size vector must summarize the whole input" bottleneck by letting the decoder re-examine all encoder states at each output step.
- Teacher forcing (feeding ground truth during training) speeds up training but can create a train/inference mismatch — a known limitation that later architectures address with different training strategies.
