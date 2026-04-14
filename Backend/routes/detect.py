from flask import Blueprint, request, jsonify
from models.yolo import detect_objects
from config.db import history
from utils.auth_middleware import token_required
import os, base64, cv2, numpy as np

detect_routes = Blueprint('detect', __name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@detect_routes.route('/upload', methods=['POST'])
@token_required
def upload():
    file = request.files['file']
    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    detections = detect_objects(path)

    history.insert_one({
        "file": file.filename,
        "detections": detections
    })

    return jsonify({"detections": detections})


@detect_routes.route('/webcam', methods=['POST'])
def webcam_detect():
    data = request.json['image']

    img_data = base64.b64decode(data.split(',')[1])
    np_arr = np.frombuffer(img_data, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    detections = detect_objects(frame)

    return jsonify({"detections": detections})