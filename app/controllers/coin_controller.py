from flask import Blueprint, jsonify, request
from app.services.coin_service import CoinService
from app.models.price_history import PriceHistory
from app.utils.price_fetcher import PriceFetcher

bp = Blueprint("coin", __name__, url_prefix="/coins")

@bp.route("/", methods=["GET"])
def get_all_coins():
    response, status_code = CoinService.get_all_coins()
    return jsonify(response), status_code

@bp.route("/<symbol>", methods=["GET"])
def get_coin(symbol):
    response, status_code = CoinService.get_coin(symbol)
    return jsonify(response), status_code

@bp.route("/prices", methods=["GET"])
def get_all_cached_prices():
    response, status_code = PriceFetcher.get_cached_prices()
    return jsonify(response), status_code

@bp.route("/history/<symbol>", methods=["GET"])
def get_price_history(symbol):
    """
    Retrieve historical price data for a given coin symbol.
    """
    interval = request.args.get("interval", "1m")  # Default interval is 1 minute
    response, status_code = CoinService.get_historical_ohlc(symbol, interval)
    return jsonify(response), status_code
