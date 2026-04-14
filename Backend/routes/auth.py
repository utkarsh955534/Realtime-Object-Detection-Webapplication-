from flask import Blueprint, request, jsonify
from config.db import users
from utils.auth_utils import generate_token
import bcrypt

auth_routes = Blueprint('auth', __name__)

# 🔐 REGISTER
@auth_routes.route('/register', methods=['POST'])
def register():
    data = request.json

    # ✅ Check required fields
    if not data.get("email") or not data.get("password"):
        return jsonify({"error": "Email and Password are required"}), 400

    email = data["email"]
    password = data["password"]

    # ✅ Check if user already exists
    existing_user = users.find_one({"email": email})
    if existing_user:
        return jsonify({"error": "User already exists"}), 409

    # ✅ Hash password
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    # ✅ Insert user
    users.insert_one({
        "email": email,
        "password": hashed,
        "role": "user"
    })

    return jsonify({"msg": "Registered successfully"}), 201


# 🔐 LOGIN
@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.json

    # ✅ Check required fields
    if not data.get("email") or not data.get("password"):
        return jsonify({"error": "Email and Password are required"}), 400

    email = data["email"]
    password = data["password"]

    user = users.find_one({"email": email})

    if user and bcrypt.checkpw(password.encode(), user["password"]):
        token = generate_token(user)
        return jsonify({"token": token}), 200

    return jsonify({"error": "Invalid credentials"}), 401