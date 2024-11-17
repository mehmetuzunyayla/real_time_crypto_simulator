from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.trade import Trade, TradeType

bp = Blueprint("trade", __name__, url_prefix="/trades")

@bp.route("/", methods=["POST"])
def create_trade():
    data = request.json
    required_fields = ["user_id", "coin_symbol", "trade_type", "quantity", "price_at_trade", "direction"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    new_trade = Trade(
        user_id=data["user_id"],
        coin_symbol=data["coin_symbol"].upper(),
        trade_type=TradeType[data["trade_type"].upper()],
        quantity=data["quantity"],
        price_at_trade=data["price_at_trade"],
        direction=data["direction"].lower()
    )
    db.session.add(new_trade)
    db.session.commit()
    return jsonify({"message": "Trade created successfully", "trade_id": new_trade.id}), 201

@bp.route("/<int:trade_id>/close", methods=["POST"])
def close_trade(trade_id):
    trade = Trade.query.get(trade_id)
    if not trade or trade.status == "closed":
        return jsonify({"error": "Trade not found or already closed"}), 404

    trade.status = "closed"
    db.session.commit()
    return jsonify({"message": "Trade closed successfully"}), 200
