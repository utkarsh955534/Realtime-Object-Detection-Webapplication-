from ultralytics import YOLO

model = YOLO("yolov8n.pt")

def detect_objects(frame):
    results = model(frame)
    detections = []

    for r in results:
        names = r.names   

        for box in r.boxes.data.tolist():
            class_id = int(box[5])   

            detections.append({
                "x1": box[0],
                "y1": box[1],
                "x2": box[2],
                "y2": box[3],
                "class": names[class_id],   
                "confidence": float(box[4])
            })

    return detections