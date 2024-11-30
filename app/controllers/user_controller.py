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