from flask import Blueprint, request, jsonify
from app.services.wallet_service import WalletService
from app.services.auth_service import AuthService
from app.utils.auth import token_required

bp = Blueprint("wallet", __name__, url_prefix="/wallets")

@bp.route("/", methods=["GET"])
@token_required
def get_wallet(user_id):
    response, status_code = WalletService.get_wallet(user_id)
    return jsonify(response), status_code

@bp.route("/update", methods=["POST"])
@token_required
def update_wallet(user_id):
    data = request.json
    amount = data.get("amount")

    if amount is None:
        return jsonify({"error": "Amount is required"}), 400

    response, status_code = WalletService.update_wallet(user_id, amount)
    return jsonify(response), status_code
