from flask import Blueprint, request, jsonify
from ultralytics import YOLO
import cv2
import numpy as np
from config.db import history
from utils.auth_middleware import token_required

detect_routes = Blueprint('detect', __name__)

# 🔥 Load model once (IMPORTANT)
model = YOLO("yolov8n.pt")

# =========================
# 📁 FILE UPLOAD DETECTION
# =========================
@detect_routes.route('/upload', methods=['POST'])
@token_required
def upload():
    try:
        file = request.files.get("file")

        if not file:
            return jsonify({"error": "File required"}), 400

        # Convert file to image
        file_bytes = np.frombuffer(file.read(), np.uint8)
        frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        results = model(frame)

        detections = []

        for r in results:
            for box in r.boxes.data.tolist():
                detections.append({
                    "x1": box[0],
                    "y1": box[1],
                    "x2": box[2],
                    "y2": box[3],
                    "class": model.names[int(box[5])],
                    "confidence": float(box[4])
                })

        # Save history
        history.insert_one({
            "file": file.filename,
            "detections": detections
        })

        return jsonify({"detections": detections})

    except Exception as e:
        print("UPLOAD ERROR:", e)
        return jsonify({"error": str(e)}), 500


# =========================
# 🎥 WEBCAM DETECTION
# =========================
@detect_routes.route('/webcam', methods=['POST'])
@token_required
def webcam():
    try:
        data = request.json

        if not data or "image" not in data:
            return jsonify({"error": "No image provided"}), 400

        # Decode base64 image
        import base64

        img_data = base64.b64decode(data["image"].split(",")[1])
        np_arr = np.frombuffer(img_data, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        results = model(frame)

        detections = []

        for r in results:
            for box in r.boxes.data.tolist():
                detections.append({
                    "x1": box[0],
                    "y1": box[1],
                    "x2": box[2],
                    "y2": box[3],
                    "class": model.names[int(box[5])],
                    "confidence": float(box[4])
                })

        return jsonify({"detections": detections})

    except Exception as e:
        print("WEBCAM ERROR:", e)
        return jsonify({"error": str(e)}), 500
