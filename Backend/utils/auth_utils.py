import jwt
import datetime
import os

SECRET = os.getenv("JWT_SECRET")

def generate_token(user):
    payload = {
        "email": user["email"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")