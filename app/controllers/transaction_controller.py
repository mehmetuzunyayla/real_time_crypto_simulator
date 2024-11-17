from flask import Blueprint, jsonify
from app.models.transaction import Transaction

bp = Blueprint("transaction", __name__, url_prefix="/transactions")

@bp.route("/<int:wallet_id>", methods=["GET"])
def get_transactions(wallet_id):
    transactions = Transaction.query.filter_by(wallet_id=wallet_id).all()
    if not transactions:
        return jsonify({"error": "No transactions found"}), 404

    transaction_list = [
        {"id": tx.id, "amount": tx.amount, "description": tx.description, "timestamp": tx.timestamp}
        for tx in transactions
    ]
    return jsonify(transaction_list), 200
