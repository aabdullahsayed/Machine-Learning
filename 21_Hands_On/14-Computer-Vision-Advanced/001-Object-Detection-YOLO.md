# 001 - Object Detection: YOLO

## Concept
Object detection locates and classifies multiple objects within an image, drawing a bounding box around each one. YOLO ("You Only Look Once") does this in a single forward pass by dividing the image into a grid and predicting boxes + class probabilities directly from each grid cell, making it fast enough for real-time use.

## Why It Matters
Detection is a step up from classification (module 11): instead of "what's in this image," it answers "what's in this image, and where." This underlies applications like autonomous driving, retail analytics, and security systems.

## Hands-On

```python
# pip install ultralytics --break-system-packages
from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt

# 1. Load a pretrained YOLO model (trained on the COCO dataset - 80 common object classes)
model = YOLO("yolov8n.pt")   # "n" = nano, smallest/fastest variant

# 2. Run detection on an image
# results = model("path/to/your/image.jpg")
# For demo purposes, using a sample image URL that ultralytics can fetch directly:
results = model("https://ultralytics.com/images/bus.jpg")

# 3. Inspect the results
for result in results:
    boxes = result.boxes  # bounding box outputs
    print(f"Detected {len(boxes)} objects")
    for box in boxes:
        cls_id = int(box.cls[0])
        cls_name = model.names[cls_id]
        confidence = float(box.conf[0])
        xyxy = box.xyxy[0].tolist()  # [x_min, y_min, x_max, y_max]
        print(f"  {cls_name}: confidence={confidence:.2f}, box={[round(c) for c in xyxy]}")

# 4. Visualize detections
annotated_image = results[0].plot()   # returns image with boxes drawn
plt.imshow(cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.title("YOLO Object Detection")
plt.savefig("yolo_detections.png")
plt.close()

# 5. Filter detections by confidence threshold and class
def filter_detections(result, min_confidence=0.5, target_classes=None):
    filtered = []
    for box in result.boxes:
        confidence = float(box.conf[0])
        cls_name = model.names[int(box.cls[0])]
        if confidence >= min_confidence and (target_classes is None or cls_name in target_classes):
            filtered.append((cls_name, confidence, box.xyxy[0].tolist()))
    return filtered

people_only = filter_detections(results[0], min_confidence=0.6, target_classes=["person"])
print("High-confidence people detections:", people_only)

# 6. The core idea behind YOLO's grid-based prediction (conceptual, not full implementation)
"""
1. Divide the image into an SxS grid (e.g., 13x13).
2. Each grid cell predicts B bounding boxes, each with:
   - (x, y, w, h): box center and size, relative to the cell
   - objectness confidence: how likely a box actually contains an object
   - class probabilities: which of the C classes it belongs to
3. Non-Maximum Suppression (NMS) then removes overlapping duplicate boxes,
   keeping only the highest-confidence box per detected object.
"""

# 7. Fine-tuning YOLO on your own custom dataset (requires a labeled dataset in YOLO format)
# model.train(data="my_dataset.yaml", epochs=50, imgsz=640)
```

## Exercise
1. Run detection on 3-5 of your own images and inspect which object classes YOLO correctly/incorrectly identifies.
2. Implement Non-Maximum Suppression from scratch (given a list of boxes with confidences, keep the highest-confidence box and remove others with high IoU overlap).
3. Compare `yolov8n.pt` (nano) vs `yolov8m.pt` (medium) on inference speed and detection quality on the same image.

## Key Takeaways
- YOLO's single-pass design (as opposed to older two-stage detectors like R-CNN, which first propose regions then classify them) is what makes it fast enough for real-time video applications.
- Detections have three components you'll always work with: bounding box coordinates, a class label, and a confidence score — filtering on confidence is essential in production use.
- Non-Maximum Suppression is a critical post-processing step that collapses multiple overlapping boxes for the same object down to one.
