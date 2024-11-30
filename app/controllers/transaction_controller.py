from flask import Blueprint, jsonify
from app.services.transaction_service import TransactionService
from app.utils.auth import token_required

bp = Blueprint("transaction", __name__, url_prefix="/transactions")

@bp.route("/<int:wallet_id>", methods=["GET"])
@token_required
def get_transactions(user_id, wallet_id):
    response, status_code = TransactionService.get_transactions(wallet_id)
    return jsonify(response), status_code
