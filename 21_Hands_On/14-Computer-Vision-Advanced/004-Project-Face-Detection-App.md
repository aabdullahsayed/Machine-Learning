# 004 - Project: Face Detection App

## Concept
This project builds a small, complete face detection application: detect faces in images (and optionally webcam video), draw bounding boxes, and count/crop detected faces — combining OpenCV's classical detector with a modern deep-learning-based option.

## Why It Matters
Face detection is a specialized but extremely common instance detection task with a huge number of real applications (photo tagging, attendance systems, camera autofocus). This project shows both a fast classical approach and a more accurate modern one.

## Hands-On

```python
# pip install opencv-python ultralytics --break-system-packages
import cv2
import matplotlib.pyplot as plt
import numpy as np

# ============================================
# 1. Classical approach: OpenCV's Haar Cascade (fast, works offline, no GPU needed)
# ============================================
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def detect_faces_haar(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,      # how much the image size is reduced at each scale
        minNeighbors=5,       # higher = fewer false positives, might miss some real faces
        minSize=(30, 30),
    )
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    return img, faces

# Example usage (requires a real image file):
# img, faces = detect_faces_haar("group_photo.jpg")
# print(f"Detected {len(faces)} faces")
# plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
# plt.axis("off")
# plt.savefig("haar_detections.png")

# ============================================
# 2. Modern approach: YOLO fine-tuned/pretrained for face detection
# ============================================
from ultralytics import YOLO

# A general object detector can be used, or a face-specific fine-tuned YOLO model.
# Here we demonstrate with a general model and filter for the 'person' class as
# a stand-in - in practice you would use a model fine-tuned specifically on faces.
general_model = YOLO("yolov8n.pt")

def detect_people_yolo(image_path_or_url):
    results = general_model(image_path_or_url)
    people = [box for box in results[0].boxes if general_model.names[int(box.cls[0])] == "person"]
    return results[0], people

results, people = detect_people_yolo("https://ultralytics.com/images/bus.jpg")
print(f"Detected {len(people)} people (as a proxy for face regions)")

# ============================================
# 3. Cropping detected faces out as individual images
# ============================================
def crop_detections(image, boxes):
    crops = []
    for (x, y, w, h) in boxes:
        crop = image[y:y+h, x:x+w]
        crops.append(crop)
    return crops

# ============================================
# 4. A simple webcam face-counting loop (run locally, not in this sandboxed demo)
# ============================================
"""
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.putText(frame, f"Faces: {len(faces)}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Face Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
"""

# ============================================
# 5. A small "app" function tying it together
# ============================================
def face_detection_app(image_path, method="haar"):
    if method == "haar":
        img, faces = detect_faces_haar(image_path)
        return {"n_faces": len(faces), "boxes": faces.tolist() if len(faces) else [], "annotated_image": img}
    else:
        raise ValueError("Only 'haar' method implemented in this demo")

# Example: result = face_detection_app("photo.jpg")
# print(result["n_faces"], "faces found")
```

## Exercise
1. Run `detect_faces_haar` on 5 different photos with varying lighting and angles — note where it succeeds or fails (Haar cascades struggle with profile views and poor lighting).
2. Fine-tune a YOLO model on a face-specific dataset (e.g., WIDER FACE) for meaningfully better accuracy than the general object detector used here.
3. Extend `face_detection_app` to save each cropped face as a separate image file, named `face_1.jpg`, `face_2.jpg`, etc.

## Key Takeaways
- Haar Cascades are fast and dependency-light (built into OpenCV) but less accurate than deep-learning detectors, especially on non-frontal faces or difficult lighting.
- `minNeighbors` and `scaleFactor` are the two parameters most worth tuning in Haar Cascade detection — higher `minNeighbors` trades recall for fewer false positives.
- This same "detect → box → crop → count" pattern generalizes to any single-class detection app (license plates, barcodes, defect detection) by swapping the detector.
