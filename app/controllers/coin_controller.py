from flask import Blueprint, jsonify
from app.services.coin_service import CoinService

bp = Blueprint("coin", __name__, url_prefix="/coins")

@bp.route("/", methods=["GET"])
def get_all_coins():
    response, status_code = CoinService.get_all_coins()
    return jsonify(response), status_code

@bp.route("/<symbol>", methods=["GET"])
def get_coin(symbol):
    response, status_code = CoinService.get_coin(symbol)
    return jsonify(response), status_code
