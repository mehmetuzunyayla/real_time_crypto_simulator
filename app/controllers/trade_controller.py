from flask import Blueprint, request, jsonify
from app.services.trade_service import TradeService
from app.utils.auth import token_required

bp = Blueprint("trade", __name__, url_prefix="/trades")

@bp.route("/", methods=["POST"])
@token_required
def create_trade(user_id):
    data = request.json
    coin_symbol = data.get("coin_symbol")
    trade_type = data.get("trade_type")
    quantity = data.get("quantity")
    price_at_trade = data.get("price_at_trade")
    direction = data.get("direction")

    if not all([coin_symbol, trade_type, quantity, price_at_trade, direction]):
        return jsonify({"error": "Missing required fields"}), 400

    response, status_code = TradeService.create_trade(user_id, coin_symbol, trade_type, quantity, price_at_trade, direction)
    return jsonify(response), status_code

@bp.route("/<int:trade_id>/close", methods=["POST"])
@token_required
def close_trade(user_id, trade_id):
    response, status_code = TradeService.close_trade(trade_id)
    return jsonify(response), status_code

@bp.route("/history", methods=["GET"])
@token_required
def get_trade_history(user_id):
    response, status_code = TradeService.get_trades_by_user_id(user_id)
    return jsonify(response), status_code