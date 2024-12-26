from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService
from app.extensions import db
from app.models.user import User
from app.models.wallet import Wallet
bp = Blueprint("user", __name__, url_prefix="/users")

@bp.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    response, status_code = AuthService.register_user(username, email, password)
    return jsonify(response), status_code

@bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    response, status_code = AuthService.login_user(email, password)
    return jsonify(response), status_code

@bp.route("/delete-all", methods=["POST"])
def delete_all_users():
    # Delete all wallets (if needed due to foreign key constraints)
    Wallet.query.delete()

    # Delete all users
    User.query.delete()

    # Commit the changes to the database
    db.session.commit()

    return jsonify({"message": "All users and their wallets have been deleted"}), 200

@bp.route("/profile", methods=["GET"])
def get_profile():
    try:
        token = request.headers.get("Authorization").split(" ")[1]
        payload = AuthService.decode_token(token)
        user_id = payload["user_id"]

        profile = AuthService.get_user_profile(user_id)
        return jsonify(profile), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route("/update_username", methods=["PUT"])
def update_username():
    try:
        token = request.headers.get("Authorization").split(" ")[1]
        payload = AuthService.decode_token(token)
        user_id = payload["user_id"]

        data = request.json
        new_username = data.get("username")
        if not new_username:
            return {"error": "Username is required"}, 400

        AuthService.update_username(user_id, new_username)
        return {"message": "Username updated successfully"}, 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500