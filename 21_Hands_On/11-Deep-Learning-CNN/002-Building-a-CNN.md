# 002 - Building a CNN

## Concept
A Convolutional Neural Network stacks convolution layers (feature extraction) and pooling layers (downsampling), followed by one or more fully-connected layers that turn the extracted features into a final prediction.

## Why It Matters
This is the standard architecture pattern behind almost every image classification model. Once you can build and train one from scratch in PyTorch, understanding larger architectures (ResNet, VGG, EfficientNet) is mostly about scale and specific tricks, not new fundamental ideas.

## Hands-On

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 1. Data
transform = transforms.Compose([transforms.ToTensor()])
train_data = datasets.MNIST(root="./data", train=True, download=True, transform=transform)
test_data = datasets.MNIST(root="./data", train=False, download=True, transform=transform)

train_loader = DataLoader(train_data, batch_size=64, shuffle=True)
test_loader = DataLoader(test_data, batch_size=64, shuffle=False)

# 2. Define the CNN architecture
class CNN(nn.Module):
    def __init__(self, num_classes=10):
        super().__init__()
        # Feature extraction: conv -> relu -> pool, twice
        self.features = nn.Sequential(
            nn.Conv2d(in_channels=1, out_channels=16, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2),          # 28x28 -> 14x14

            nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2),          # 14x14 -> 7x7
        )
        # Classification head
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(32 * 7 * 7, 128),
            nn.ReLU(),
            nn.Dropout(0.3),                       # regularization - randomly zeroes activations
            nn.Linear(128, num_classes),
        )

    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x

model = CNN().to(device)
print(model)

# 3. Count parameters - see how much smaller this is than an equivalent fully-connected net
n_params = sum(p.numel() for p in model.parameters())
print(f"Total trainable parameters: {n_params:,}")

# 4. Train
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

def train_epoch():
    model.train()
    total_loss, correct = 0, 0
    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
        correct += (outputs.argmax(1) == labels).sum().item()
    return total_loss / len(train_loader), correct / len(train_data)

for epoch in range(3):
    avg_loss, train_acc = train_epoch()
    print(f"Epoch {epoch+1}: loss={avg_loss:.4f}, train_acc={train_acc:.4f}")

# 5. Evaluate
model.eval()
correct = 0
with torch.no_grad():
    for images, labels in test_loader:
        images, labels = images.to(device), labels.to(device)
        preds = model(images).argmax(1)
        correct += (preds == labels).sum().item()
print(f"Test accuracy: {correct/len(test_data):.4f}")

# 6. Inspect what the first-layer filters learned
first_layer_weights = model.features[0].weight.data.cpu()
print("First conv layer weight shape:", first_layer_weights.shape)  # (16, 1, 3, 3)
```

## Exercise
1. Add a third `Conv2d` + `MaxPool2d` block and observe how the flattened feature size changes (you'll need to update `Linear(32*7*7, ...)` accordingly).
2. Replace `Dropout(0.3)` with `nn.BatchNorm2d` after each conv layer (before ReLU) — does training become faster or more stable?
3. Visualize the 16 first-layer filters as small grayscale images using `matplotlib` — do any resemble edge detectors, similar to lesson 001's hand-designed kernels?

## Key Takeaways
- CNN architecture is a repeating pattern: `Conv -> Activation -> Pool`, stacked a few times, then flattened into fully-connected layers for the final prediction.
- Weight sharing (the same kernel slides across the whole image) is why CNNs have far fewer parameters than a fully-connected network on the same image size.
- `Dropout` and `BatchNorm` are the two most common regularization/stabilization tools added between the "textbook" layers shown here.
