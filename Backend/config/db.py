import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise Exception("❌ MONGO_URI not found in .env")

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)

    # 🔥 Force connection check
    client.server_info()

    db = client["ai_detection"]

    users = db["users"]
    history = db["history"]

    print("✅ MongoDB connected successfully")

except Exception as e:
    print("❌ MongoDB connection failed:", e)
    raise e