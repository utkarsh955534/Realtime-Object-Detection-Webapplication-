from flask import Blueprint, request, jsonify
import requests
from config.db import history
from utils.auth_middleware import token_required

detect_routes = Blueprint('detect', __name__)


HF_URL = "https://utkarsh9555-yolo-space.hf.space/api/predict/"


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

        import base64

        # Convert image → base64
        image_bytes = file.read()
        base64_image = base64.b64encode(image_bytes).decode("utf-8")
        image_data = f"data:image/jpeg;base64,{base64_image}"

        # 🔥 Send to Hugging Face
        response = requests.post(
            HF_URL,
            json={
                "data": [image_data]
            }
        )

        result = response.json()

        detections = result["data"][0]

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

        # 🔥 Send directly to HF
        response = requests.post(
            HF_URL,
            json={
                "data": [data["image"]]
            }
        )

        result = response.json()

        detections = result["data"][0]

        return jsonify({"detections": detections})

    except Exception as e:
        print("WEBCAM ERROR:", e)
        return jsonify({"error": str(e)}), 500
