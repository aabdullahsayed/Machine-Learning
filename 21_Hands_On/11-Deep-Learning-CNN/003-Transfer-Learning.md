# 003 - Transfer Learning

## Concept
Transfer learning takes a model pre-trained on a huge dataset (typically ImageNet, 1.4M images) and reuses its learned features for a new, often much smaller, dataset — either by freezing most layers and only training a new final layer, or by fine-tuning the whole network with a low learning rate.

## Why It Matters
Training a CNN from scratch needs huge datasets and compute. Transfer learning lets you get excellent results with a few hundred or thousand images by standing on the shoulders of models already trained on millions of images.

## Hands-On

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import models, transforms, datasets
from torch.utils.data import DataLoader

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 1. Load a pre-trained model (ResNet18, trained on ImageNet)
model = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)

# 2. Freeze all existing layers - we don't want to destroy their learned features
for param in model.parameters():
    param.requires_grad = False

# 3. Replace the final classification layer for our new task
# ResNet18's original final layer outputs 1000 classes (ImageNet); we replace it
num_classes = 2   # e.g., "cat" vs "dog"
model.fc = nn.Linear(model.fc.in_features, num_classes)
# Only this new layer has requires_grad=True by default (freshly created)

model = model.to(device)

# 4. Preprocessing MUST match what the pre-trained model expects
preprocess = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],   # ImageNet mean/std - required
                          std=[0.229, 0.224, 0.225]),
])

# Example: loading a custom folder-structured dataset (uncomment with real data)
# train_data = datasets.ImageFolder("data/train", transform=preprocess)
# train_loader = DataLoader(train_data, batch_size=32, shuffle=True)

# 5. Train only the new final layer (feature extraction approach)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.fc.parameters(), lr=0.001)  # only optimize the new layer

def train_epoch(loader):
    model.train()
    total_loss = 0
    for images, labels in loader:
        images, labels = images.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    return total_loss / len(loader)

# for epoch in range(5):
#     avg_loss = train_epoch(train_loader)
#     print(f"Epoch {epoch+1}: loss={avg_loss:.4f}")

# 6. Fine-tuning approach - unfreeze the last few layers with a small learning rate
for name, param in model.named_parameters():
    if "layer4" in name or "fc" in name:   # unfreeze only the last block + head
        param.requires_grad = True

fine_tune_optimizer = optim.Adam(
    filter(lambda p: p.requires_grad, model.parameters()), lr=0.0001  # smaller lr for fine-tuning
)

# 7. Compare parameter counts: frozen vs. trainable
total_params = sum(p.numel() for p in model.parameters())
trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
print(f"Total params: {total_params:,}, Trainable: {trainable_params:,} "
      f"({100*trainable_params/total_params:.1f}%)")
```

## Exercise
1. Compare training a `resnet18` from scratch (`weights=None`) vs. pretrained on a small dataset (e.g., 200 images per class) — transfer learning should win by a wide margin.
2. Try a different backbone, `models.mobilenet_v2(weights=...)`, and adapt the final classifier layer name (it's `.classifier`, not `.fc`) accordingly.
3. Experiment with unfreezing progressively more layers (`layer3` and `layer4` vs. just `layer4`) and compare validation accuracy and training time.

## Key Takeaways
- Feature extraction (freeze everything, train only a new head) is fast and works well when your new dataset is small and similar to ImageNet's domain.
- Fine-tuning (unfreeze some/all layers with a low learning rate) can push accuracy higher when you have more data, but risks "catastrophic forgetting" of pretrained features if the learning rate is too high.
- Always match the preprocessing (resize, normalization stats) to what the pretrained model was originally trained with — mismatched preprocessing silently tanks performance.
