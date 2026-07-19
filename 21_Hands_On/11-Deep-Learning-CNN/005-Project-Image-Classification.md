# 005 - Project: Image Classification

## Concept
This project combines convolution/pooling (001), CNN architecture (002), transfer learning (003), and data augmentation (004) into one complete image classifier trained end-to-end, with proper train/val splits and a saved final model.

## Why It Matters
This is the point where all of module 11's individual pieces come together into the kind of project you'd actually build for a real image classification task.

## Hands-On

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import models, transforms, datasets
from torch.utils.data import DataLoader, random_split

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# --- Step 1: Transforms - augmentation for train, plain resize/normalize for val ---
train_transform = transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])
val_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# --- Step 2: Load data (using CIFAR10 as a stand-in for a real custom dataset) ---
full_train = datasets.CIFAR10(root="./data", train=True, download=True, transform=train_transform)
test_data = datasets.CIFAR10(root="./data", train=False, download=True, transform=val_transform)

train_size = int(0.9 * len(full_train))
val_size = len(full_train) - train_size
train_data, val_data = random_split(full_train, [train_size, val_size])

train_loader = DataLoader(train_data, batch_size=64, shuffle=True)
val_loader = DataLoader(val_data, batch_size=64, shuffle=False)
test_loader = DataLoader(test_data, batch_size=64, shuffle=False)

class_names = ["airplane", "automobile", "bird", "cat", "deer",
               "dog", "frog", "horse", "ship", "truck"]

# --- Step 3: Transfer learning setup ---
model = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
for param in model.parameters():
    param.requires_grad = False
model.fc = nn.Linear(model.fc.in_features, len(class_names))
model = model.to(device)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.fc.parameters(), lr=0.001)

# --- Step 4: Training loop with validation tracking + best-model checkpointing ---
best_val_acc = 0.0

def evaluate(loader):
    model.eval()
    correct, total = 0, 0
    with torch.no_grad():
        for images, labels in loader:
            images, labels = images.to(device), labels.to(device)
            preds = model(images).argmax(1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)
    return correct / total

for epoch in range(3):  # keep small for a demo; raise for real training
    model.train()
    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

    val_acc = evaluate(val_loader)
    print(f"Epoch {epoch+1}: val_accuracy={val_acc:.4f}")

    if val_acc > best_val_acc:
        best_val_acc = val_acc
        torch.save(model.state_dict(), "best_model.pth")
        print("  -> new best model saved")

# --- Step 5: Final test evaluation using the BEST checkpoint, not the last epoch ---
model.load_state_dict(torch.load("best_model.pth"))
test_acc = evaluate(test_loader)
print(f"Final test accuracy (best checkpoint): {test_acc:.4f}")

# --- Step 6: A predict function for a single image ---
from PIL import Image

def predict_image(image_path, model, class_names, transform):
    model.eval()
    img = Image.open(image_path).convert("RGB")
    tensor = transform(img).unsqueeze(0).to(device)
    with torch.no_grad():
        logits = model(tensor)
        probs = torch.softmax(logits, dim=1)[0]
        pred_idx = probs.argmax().item()
    return class_names[pred_idx], probs[pred_idx].item()

# Example: predict_image("my_photo.jpg", model, class_names, val_transform)
```

## Exercise
1. Unfreeze `model.layer4` (like lesson 003) after 2 epochs of head-only training, and continue training with a lower learning rate — does test accuracy improve?
2. Add a confusion matrix (`sklearn.metrics.confusion_matrix`) on the test set to see which classes get confused most often.
3. Try `models.resnet34` or `models.efficientnet_b0` as the backbone instead of `resnet18` and compare accuracy vs. training time.

## Key Takeaways
- Always evaluate on a validation set during training to choose the best checkpoint — the last epoch is not always the best one.
- The full pattern — augment train data only, use transfer learning, checkpoint the best model, evaluate once on a held-out test set — is the standard shape of a real image classification project.
- A `predict_image` function turns the trained model into something directly usable in an application, exactly as in the module 15 deployment lessons.
