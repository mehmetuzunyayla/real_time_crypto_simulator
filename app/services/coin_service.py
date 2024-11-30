from app.models.coin import Coin

class CoinService:
    @staticmethod
    def get_all_coins():
        coins = Coin.query.all()
        coin_list = [{"symbol": coin.symbol, "name": coin.name, "price": coin.price} for coin in coins]
        return coin_list, 200

    @staticmethod
    def get_coin(symbol):
        coin = Coin.query.filter_by(symbol=symbol.upper()).first()
        if not coin:
            return {"error": "Coin not found"}, 404
        return {"symbol": coin.symbol, "name": coin.name, "price": coin.price}, 200
