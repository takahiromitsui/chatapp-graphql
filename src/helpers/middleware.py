from functools import wraps
from flask import request, jsonify
from src.helpers.auth import decode_token
from src.models.user import User


def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "Token is missing"}), 401
        try:
            decoded_token = decode_token(token, "secret")
            id = decoded_token["id"]
            user = User.query.get(id)
            if not user:
                return jsonify({"message": "User not found"}), 404
            return func(*args, **kwargs)
        except:
            return jsonify({"message": "Token is invalid"}), 401
    return decorated_function