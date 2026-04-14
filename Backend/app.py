from flask import Flask
from flask_cors import CORS
import os

from routes.auth import auth_routes
from routes.detect import detect_routes
from routes.history import history_routes

app = Flask(__name__)


CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://realtime-object-detection-webapplic.vercel.app"
        ]
    }
})


app.register_blueprint(auth_routes, url_prefix='/api/auth')
app.register_blueprint(detect_routes, url_prefix='/api/detect')
app.register_blueprint(history_routes, url_prefix='/api/history')


@app.route("/")
def home():
    return {"status": "API running"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # 🔥 FIX
    app.run(host="0.0.0.0", port=port)
