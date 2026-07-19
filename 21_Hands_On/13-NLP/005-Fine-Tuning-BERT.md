# 005 - Fine-Tuning BERT

## Concept
BERT (Bidirectional Encoder Representations from Transformers) is a pretrained Transformer encoder that produces contextual embeddings — the same word gets a different vector depending on its surrounding context. Fine-tuning adapts this pretrained model to a specific downstream task (e.g., sentiment classification) with a small amount of task-specific data.

## Why It Matters
Fine-tuning a pretrained language model is the standard modern approach for NLP tasks — it's the direct analog of transfer learning for images (module 11-003), and typically outperforms training from scratch by a huge margin, especially with limited labeled data.

## Hands-On

```python
# pip install transformers torch datasets --break-system-packages
import torch
from transformers import BertTokenizer, BertForSequenceClassification, AdamW
from torch.utils.data import Dataset, DataLoader

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 1. Load the pretrained tokenizer and model
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)
model = model.to(device)

# 2. See what BERT's tokenizer actually does - subword tokenization
text = "Transformers revolutionized natural language processing."
tokens = tokenizer.tokenize(text)
print("Tokens:", tokens)
# Note: unfamiliar words get split into subword pieces, e.g. "revolutionized" -> "revolution", "##ized"

encoded = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
print("Input IDs shape:", encoded["input_ids"].shape)
print("Includes [CLS] and [SEP] special tokens:", tokenizer.convert_ids_to_tokens(encoded["input_ids"][0]))

# 3. A small sentiment dataset for fine-tuning
texts = [
    "This movie was absolutely amazing, I loved it!",
    "Terrible film, complete waste of time.",
    "Best experience I've ever had at the cinema.",
    "I hated every second of this movie.",
    "Wonderful acting and a great story.",
    "Boring, predictable, and poorly made.",
] * 10   # repeat for a slightly larger demo dataset
labels = [1, 0, 1, 0, 1, 0] * 10

class SentimentDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_len=64):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        encoding = self.tokenizer(
            self.texts[idx],
            truncation=True,
            padding="max_length",
            max_length=self.max_len,
            return_tensors="pt",
        )
        return {
            "input_ids": encoding["input_ids"].squeeze(0),
            "attention_mask": encoding["attention_mask"].squeeze(0),
            "label": torch.tensor(self.labels[idx]),
        }

dataset = SentimentDataset(texts, labels, tokenizer)
loader = DataLoader(dataset, batch_size=8, shuffle=True)

# 4. Fine-tuning loop
optimizer = AdamW(model.parameters(), lr=2e-5)  # small LR - typical for fine-tuning

model.train()
for epoch in range(3):
    total_loss = 0
    for batch in loader:
        optimizer.zero_grad()
        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        labels_batch = batch["label"].to(device)

        outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels_batch)
        loss = outputs.loss
        loss.backward()
        optimizer.step()
        total_loss += loss.item()

    print(f"Epoch {epoch+1}: avg loss={total_loss/len(loader):.4f}")

# 5. Inference on new text
def predict_sentiment(text, model, tokenizer):
    model.eval()
    encoding = tokenizer(text, return_tensors="pt", truncation=True, padding=True).to(device)
    with torch.no_grad():
        outputs = model(**encoding)
        probs = torch.softmax(outputs.logits, dim=1)[0]
        pred = probs.argmax().item()
    return ("positive" if pred == 1 else "negative"), probs[pred].item()

print(predict_sentiment("This was a fantastic film!", model, tokenizer))
print(predict_sentiment("What a disappointing movie.", model, tokenizer))

# 6. Save the fine-tuned model
model.save_pretrained("./fine_tuned_bert_sentiment")
tokenizer.save_pretrained("./fine_tuned_bert_sentiment")
```

## Exercise
1. Freeze all BERT layers except the final classification head (`for param in model.bert.parameters(): param.requires_grad = False`) and compare training speed and accuracy to full fine-tuning.
2. Try a smaller, faster model like `distilbert-base-uncased` instead of `bert-base-uncased` — compare accuracy and training time.
3. Load the saved model with `BertForSequenceClassification.from_pretrained("./fine_tuned_bert_sentiment")` and verify it produces the same predictions as before saving.

## Key Takeaways
- BERT's tokenizer splits unfamiliar words into subword pieces, which lets it handle rare/unseen words gracefully without an "unknown token" problem.
- Fine-tuning uses a much smaller learning rate (typically 1e-5 to 5e-5) than training from scratch, since you're making small adjustments to already-good pretrained weights, not learning from nothing.
- The `[CLS]` token's final hidden state is what `BertForSequenceClassification` uses for classification — it's designed during pretraining to aggregate sequence-level information.
