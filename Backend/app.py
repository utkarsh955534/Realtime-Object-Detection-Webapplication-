from flask import Flask
from flask_cors import CORS
import os

from routes.auth import auth_routes
from routes.detect import detect_routes
from routes.history import history_routes

app = Flask(__name__)


FRONTEND_URL = "https://realtime-object-detection-webapplic.vercel.app"


CORS(
    app,
    origins=[FRONTEND_URL],
    supports_credentials=True
)


@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = FRONTEND_URL
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    return response


@app.route("/api/<path:path>", methods=["OPTIONS"])
def options_handler(path):
    return "", 200

app.register_blueprint(auth_routes, url_prefix='/api/auth')
app.register_blueprint(detect_routes, url_prefix='/api/detect')
app.register_blueprint(history_routes, url_prefix='/api/history')


@app.route("/")
def home():
    return {"status": "API running"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
