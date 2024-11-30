import jwt
from flask import request, jsonify
from functools import wraps
from app.config import Config  # Import Config to access SECRET_KEY

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"error": "Token is missing"}), 401

        try:
            # Extract token after "Bearer "
            token = auth_header.split(" ")[1]
            data = jwt.decode(token, Config.USER_SECRET_KEY, algorithms=["HS256"])
            user_id = data["user_id"]
        except IndexError:
            return jsonify({"error": "Bearer token malformed"}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(user_id, *args, **kwargs)
    return decorated
