from flask import Flask
from flask_cors import CORS
from routes.auth import auth_routes
from routes.detect import detect_routes
from routes.history import history_routes

app = Flask(__name__)

# 🔥 Proper CORS configuration
CORS(app, resources={
    r"/api/*": {
        "origins": "http://localhost:3000"
    }
})

# ✅ Register routes
app.register_blueprint(auth_routes, url_prefix='/api/auth')
app.register_blueprint(detect_routes, url_prefix='/api/detect')
app.register_blueprint(history_routes, url_prefix='/api/history')


# 🔥 Force headers (extra safety)
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)