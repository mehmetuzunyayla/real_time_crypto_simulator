from app.repositories.coin_repository import CoinRepository

class CoinService:
    @staticmethod
    def get_all_coins():
        coins = CoinRepository.get_all_coins()
        coin_list = [{"symbol": coin.symbol, "name": coin.name, "price": coin.price} for coin in coins]
        return coin_list, 200

    @staticmethod
    def get_coin(symbol):
        coin = CoinRepository.get_coin_by_symbol(symbol)
        if not coin:
            return {"error": "Coin not found"}, 404
        return {"symbol": coin.symbol, "name": coin.name, "price": coin.price}, 200
