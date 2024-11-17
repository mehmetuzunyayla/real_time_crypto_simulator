from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from app.models.user import User

bp = Blueprint("user", __name__, url_prefix="/users")

@bp.route("/register", methods=["POST"])
def register():
    data = request.json
    if not data.get("username") or not data.get("password") or not data.get("email"):
        return jsonify({"error": "Missing required fields"}), 400

    # Check if the user already exists
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "User already exists"}), 400

    # Create the user
    hashed_password = generate_password_hash(data["password"])
    new_user = User(
        username=data["username"],
        email=data["email"],
        password_hash=hashed_password,
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201

@bp.route("/login", methods=["POST"])
def login():
    data = request.json
    if not data.get("email") or not data.get("password"):
        return jsonify({"error": "Missing required fields"}), 400

    user = User.query.filter_by(email=data["email"]).first()
    if not user or not check_password_hash(user.password_hash, data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    # Generate a JWT (placeholder)
    token = f"dummy-token-for-{user.username}"

    return jsonify({"message": "Login successful", "token": token}), 200
