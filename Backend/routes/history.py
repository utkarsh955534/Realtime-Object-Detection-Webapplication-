from flask import Blueprint, jsonify
from config.db import history

history_routes = Blueprint('history', __name__)

@history_routes.route('/', methods=['GET'])
def get_history():
    data = list(history.find({}, {"_id": 0}))
    return jsonify(data)