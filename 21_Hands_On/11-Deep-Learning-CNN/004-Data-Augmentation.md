# 004 - Data Augmentation

## Concept
Data augmentation artificially expands a training set by applying random, label-preserving transformations to images (flips, rotations, crops, color jitter) each time they're loaded, so the model sees a slightly different version every epoch.

## Why It Matters
It's one of the cheapest, most effective ways to reduce overfitting and improve generalization — especially valuable when you don't have a huge dataset (which is most real projects).

## Hands-On

```python
import torch
from torchvision import transforms, datasets
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
from PIL import Image

# 1. Common augmentation transforms
train_transform = transforms.Compose([
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.RandomRotation(degrees=15),
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
    transforms.RandomResizedCrop(size=224, scale=(0.8, 1.0)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Test-time transform: NO random augmentation, just resize + normalize
test_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# 2. Visualize what augmentation does to a single image
from torchvision.datasets import FakeData
sample_dataset = FakeData(size=1, image_size=(3, 256, 256), num_classes=2)
img, _ = sample_dataset[0]   # a PIL Image

visualize_transform = transforms.Compose([
    transforms.RandomHorizontalFlip(p=1.0),   # force flip for visualization
    transforms.RandomRotation(degrees=20),
])

fig, axes = plt.subplots(1, 5, figsize=(15, 3))
axes[0].imshow(img); axes[0].set_title("Original"); axes[0].axis("off")
for i in range(1, 5):
    augmented = visualize_transform(img)
    axes[i].imshow(augmented)
    axes[i].set_title(f"Augmented {i}")
    axes[i].axis("off")
plt.savefig("augmentation_examples.png")
plt.close()

# 3. Manual implementation of a simple augmentation (horizontal flip) to see the mechanism
import numpy as np

def manual_horizontal_flip(image_array):
    return image_array[:, ::-1, :]   # reverse the width axis

def manual_random_crop(image_array, crop_size):
    h, w, _ = image_array.shape
    ch, cw = crop_size
    top = np.random.randint(0, h - ch)
    left = np.random.randint(0, w - cw)
    return image_array[top:top+ch, left:left+cw, :]

fake_image = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
flipped = manual_horizontal_flip(fake_image)
cropped = manual_random_crop(fake_image, (64, 64))
print("Original shape:", fake_image.shape)
print("Flipped shape:", flipped.shape)     # same shape, mirrored
print("Cropped shape:", cropped.shape)     # smaller shape

# 4. Applying different transforms to train vs. validation splits of the SAME dataset
# train_data = datasets.ImageFolder("data/train", transform=train_transform)
# val_data = datasets.ImageFolder("data/val", transform=test_transform)  # no augmentation!
```

## Exercise
1. Add `transforms.RandomErasing()` (randomly blacks out a rectangular patch) to `train_transform` — this simulates occlusion and is a strong regularizer.
2. Train the CNN from lesson 002 on MNIST with and without augmentation (e.g., small rotations) for the same number of epochs — compare test accuracy.
3. Explain in your own words why you should apply strong augmentation to the *training* set but only resize/normalize on the *validation/test* set.

## Key Takeaways
- Augmentation should be applied only to the training set — validation and test data must reflect real, unaltered inputs to give an honest performance estimate.
- Good augmentations preserve the label (a horizontally flipped cat photo is still a cat) — augmentations that could change the label (e.g., flipping a "6" digit into a "9") should be avoided for that task.
- Augmentation and transfer learning (lesson 003) are complementary: augmentation fights overfitting on your data, transfer learning gives you a strong starting point.
