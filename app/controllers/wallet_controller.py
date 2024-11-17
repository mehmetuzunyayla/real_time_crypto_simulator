from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.wallet import Wallet

bp = Blueprint("wallet", __name__, url_prefix="/wallets")

@bp.route("/<int:user_id>", methods=["GET"])
def get_wallet(user_id):
    wallet = Wallet.query.filter_by(user_id=user_id).first()
    if not wallet:
        return jsonify({"error": "Wallet not found"}), 404
    return jsonify({"user_id": wallet.user_id, "balance": wallet.balance}), 200

@bp.route("/<int:user_id>/update", methods=["POST"])
def update_wallet(user_id):
    data = request.json
    amount = data.get("amount")
    if amount is None:
        return jsonify({"error": "Amount is required"}), 400

    wallet = Wallet.query.filter_by(user_id=user_id).first()
    if not wallet:
        return jsonify({"error": "Wallet not found"}), 404

    wallet.balance += amount
    db.session.commit()
    return jsonify({"message": "Wallet updated successfully", "balance": wallet.balance}), 200
