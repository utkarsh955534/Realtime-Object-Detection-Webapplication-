from functools import wraps
from flask import request, jsonify
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

SECRET = os.getenv("JWT_SECRET")   # 🔥 FIX HERE

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"error": "Token missing"}), 401

        try:
            token = auth_header.split(" ")[1]
            jwt.decode(token, SECRET, algorithms=["HS256"])
        except Exception as e:
            print("TOKEN ERROR:", e)
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated