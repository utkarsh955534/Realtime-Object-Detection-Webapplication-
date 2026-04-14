from flask import Blueprint, request, jsonify
import requests
import base64
from config.db import history
from utils.auth_middleware import token_required

detect_routes = Blueprint('detect', __name__)

# ✅ FINAL CORRECT HF URL
HF_URL = "https://utkarsh9555-yolo-space.hf.space/predict"


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

        # 🔥 Convert image → base64 (NO prefix)
        image_bytes = file.read()
        base64_image = base64.b64encode(image_bytes).decode("utf-8")

        # 🔥 Send to HF (IMPORTANT FIX)
        response = requests.post(
    HF_URL,
    json={"image": image},
    timeout=30
)

result = response.json()
detections = result["detections"]

        print("HF UPLOAD RESPONSE:", response.text)

        if response.status_code != 200:
            return jsonify({
                "error": "HF failed",
                "status": response.status_code,
                "response": response.text
            }), 500

        result = response.json()

        # 🔥 SAFE PARSING
        if isinstance(result, list):
            detections = result
        elif "data" in result:
            detections = result["data"][0]
        else:
            return jsonify({"error": "Invalid HF response"}), 500

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
            return jsonify({"error": "No image"}), 400

        image = data["image"]

        # 🔥 REMOVE base64 prefix
        if "base64," in image:
            image = image.split("base64,")[1]

        # 🔥 Send to HF (IMPORTANT FIX)
        response = requests.post(
            HF_URL,
            json={
                "data": [image],
                "fn_index": 0
            },
            timeout=30
        )

        print("HF WEBCAM RESPONSE:", response.text)

        if response.status_code != 200:
            return jsonify({
                "error": "HF failed",
                "status": response.status_code,
                "response": response.text
            }), 500

        result = response.json()

        # 🔥 SAFE PARSING
        if isinstance(result, list):
            detections = result
        elif "data" in result:
            detections = result["data"][0]
        else:
            return jsonify({"error": "Invalid HF response"}), 500

        return jsonify({"detections": detections})

    except Exception as e:
        print("WEBCAM ERROR:", e)
        return jsonify({"error": str(e)}), 500
