# 002 - Capstone: End-to-End Computer Vision App

## Concept
A simple, complete image classification app: load an image dataset → build a small CNN → train it → evaluate it → save it → write a `predict_image(path)` function that a real app could call.

## Why It Matters
This is the shortest path from "I understand CNNs" (module 11) to "I have something that works on a real image I feed it" — the gap most learners never close.

## Hands-On

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from PIL import Image

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# --- Step 1: Data - using FashionMNIST as a simple, built-in image dataset ---
transform = transforms.Compose([transforms.ToTensor()])

train_data = datasets.FashionMNIST(root="./data", train=True, download=True, transform=transform)
test_data = datasets.FashionMNIST(root="./data", train=False, download=True, transform=transform)

train_loader = DataLoader(train_data, batch_size=64, shuffle=True)
test_loader = DataLoader(test_data, batch_size=64, shuffle=False)

class_names = ["T-shirt/top", "Trouser", "Pullover", "Dress", "Coat",
               "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"]

# --- Step 2: A small CNN ---
class SimpleCNN(nn.Module):
    def __init__(self, num_classes=10):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(1, 16, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),   # 28x28 -> 14x14
            nn.Conv2d(16, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),  # 14x14 -> 7x7
        )
        self.fc = nn.Sequential(
            nn.Flatten(),
            nn.Linear(32 * 7 * 7, 128), nn.ReLU(),
            nn.Linear(128, num_classes),
        )

    def forward(self, x):
        return self.fc(self.conv(x))

model = SimpleCNN().to(device)

# --- Step 3: Train ---
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

def train_one_epoch():
    model.train()
    total_loss = 0
    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    return total_loss / len(train_loader)

for epoch in range(3):  # keep small for a quick demo; raise for real training
    avg_loss = train_one_epoch()
    print(f"Epoch {epoch+1}: loss={avg_loss:.4f}")

# --- Step 4: Evaluate ---
model.eval()
correct, total = 0, 0
with torch.no_grad():
    for images, labels in test_loader:
        images, labels = images.to(device), labels.to(device)
        preds = model(images).argmax(dim=1)
        correct += (preds == labels).sum().item()
        total += labels.size(0)

print(f"Test accuracy: {correct/total:.4f}")

# --- Step 5: Save the model ---
torch.save(model.state_dict(), "cnn_model.pth")

# --- Step 6: A predict function a real app could call ---
def predict_image(image_path, model, class_names):
    model.eval()
    img = Image.open(image_path).convert("L").resize((28, 28))
    tensor = transforms.ToTensor()(img).unsqueeze(0).to(device)  # add batch dim
    with torch.no_grad():
        logits = model(tensor)
        pred_idx = logits.argmax(dim=1).item()
    return class_names[pred_idx]

# Example (requires an actual image file):
# print(predict_image("my_shoe.png", model, class_names))
```

## Exercise
1. Swap `FashionMNIST` for `CIFAR10` (color images, 3 input channels instead of 1) and adjust `Conv2d(1, 16, ...)` to `Conv2d(3, 16, ...)`.
2. Add data augmentation (`transforms.RandomHorizontalFlip()`) and check if test accuracy improves.
3. Reload the saved weights into a fresh `SimpleCNN()` instance with `model.load_state_dict(torch.load("cnn_model.pth"))` and confirm it still predicts correctly.

## Key Takeaways
- The full loop — data loader, model, training loop, evaluation, save, predict function — is the same shape for every vision project, regardless of dataset size.
- `model.eval()` and `torch.no_grad()` during inference disable dropout/batchnorm training behavior and skip gradient tracking, which is both faster and correct.
- A `predict_image(path)` function is the bridge between a trained model and an actual application (web app, mobile app, API) — see module 15 for deployment.
