# 002 - Image Segmentation

## Concept
Segmentation classifies every individual pixel in an image, not just drawing boxes. Semantic segmentation labels each pixel by class (e.g., "road", "car", "sky"); instance segmentation additionally distinguishes between separate objects of the same class.

## Why It Matters
Segmentation gives pixel-precise understanding needed for tasks like medical image analysis (tumor boundaries), autonomous driving (drivable area), and photo editing (background removal) — far more granular than detection's bounding boxes.

## Hands-On

```python
# pip install ultralytics torch torchvision --break-system-packages
import torch
import numpy as np
import matplotlib.pyplot as plt

# 1. Instance segmentation with YOLO (extends the detector from lesson 001)
from ultralytics import YOLO

seg_model = YOLO("yolov8n-seg.pt")   # segmentation variant
results = seg_model("https://ultralytics.com/images/bus.jpg")

for result in results:
    if result.masks is not None:
        print(f"Detected {len(result.masks)} instance masks")
        print("Mask shape per instance:", result.masks.data[0].shape)

annotated = results[0].plot()
plt.imshow(annotated[:, :, ::-1])
plt.axis("off")
plt.title("Instance Segmentation")
plt.savefig("instance_segmentation.png")
plt.close()

# 2. Semantic segmentation with a pretrained DeepLabV3 (torchvision)
from torchvision.models.segmentation import deeplabv3_resnet50, DeepLabV3_ResNet50_Weights
from torchvision import transforms
from PIL import Image
import urllib.request

weights = DeepLabV3_ResNet50_Weights.DEFAULT
seg_net = deeplabv3_resnet50(weights=weights)
seg_net.eval()

preprocess = weights.transforms()

# Download a sample image
url = "https://ultralytics.com/images/bus.jpg"
urllib.request.urlretrieve(url, "sample.jpg")
img = Image.open("sample.jpg").convert("RGB")
input_tensor = preprocess(img).unsqueeze(0)

with torch.no_grad():
    output = seg_net(input_tensor)["out"][0]

# Each pixel gets a predicted class (21 classes in the Pascal VOC categories DeepLabV3 uses)
predicted_classes = output.argmax(0).numpy()
print("Segmentation map shape:", predicted_classes.shape)
print("Unique classes detected:", np.unique(predicted_classes))

class_names = weights.meta["categories"]
detected_names = [class_names[c] for c in np.unique(predicted_classes)]
print("Detected categories:", detected_names)

# 3. Visualize the segmentation mask overlaid on the image
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.imshow(img)
plt.title("Original")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(predicted_classes, cmap="tab20")
plt.title("Semantic Segmentation Map")
plt.axis("off")
plt.savefig("semantic_segmentation.png")

# 4. Compute the pixel area (as a % of the image) belonging to each detected class
total_pixels = predicted_classes.size
for cls_id in np.unique(predicted_classes):
    pct = (predicted_classes == cls_id).sum() / total_pixels * 100
    print(f"{class_names[cls_id]}: {pct:.1f}% of image")
```

## Exercise
1. Extract a binary mask for just one class (e.g., "person") and use it to blur or replace the background of the image — a simplified version of video call background effects.
2. Compare the instance segmentation masks from YOLO to the semantic segmentation map from DeepLabV3 on the same image — where do the boundaries agree/disagree?
3. Compute Intersection over Union (IoU) between a predicted mask and a hand-drawn "ground truth" rectangle mask you define yourself, to practice the standard segmentation evaluation metric.

## Key Takeaways
- Semantic segmentation labels pixels by class only (all cars share one label); instance segmentation additionally separates individual object instances (car #1 vs car #2).
- Segmentation models produce a per-pixel class map the same spatial size as the input, unlike classification (one label) or detection (a handful of boxes).
- IoU (Intersection over Union) is the standard metric for evaluating segmentation quality — it measures overlap between predicted and ground-truth masks.
