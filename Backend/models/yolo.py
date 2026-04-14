from ultralytics import YOLO

# 🔥 Load model once (important for performance)
model = YOLO("yolov8n.pt")


def detect_objects(frame):
    """
    Detect objects from image (numpy array)
    Returns list of detections
    """

    results = model(frame)

    detections = []

    for r in results:
        names = r.names

        for box in r.boxes.data.tolist():
            class_id = int(box[5])

            detections.append({
                "x1": float(box[0]),
                "y1": float(box[1]),
                "x2": float(box[2]),
                "y2": float(box[3]),
                "class": names[class_id],
                "confidence": float(box[4])
            })

    return detections
