from flask import Blueprint, jsonify
from app.models.coin import Coin

bp = Blueprint("coin", __name__, url_prefix="/coins")

@bp.route("/", methods=["GET"])
def get_all_coins():
    coins = Coin.query.all()
    coin_list = [{"symbol": coin.symbol, "name": coin.name, "price": coin.price} for coin in coins]
    return jsonify(coin_list), 200

@bp.route("/<symbol>", methods=["GET"])
def get_coin(symbol):
    coin = Coin.query.filter_by(symbol=symbol.upper()).first()
    if not coin:
        return jsonify({"error": "Coin not found"}), 404
    return jsonify({"symbol": coin.symbol, "name": coin.name, "price": coin.price}), 200
