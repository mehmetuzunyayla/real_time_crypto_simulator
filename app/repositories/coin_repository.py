from app.models.coin import Coin
from app.extensions import db

class CoinRepository:
    @staticmethod
    def get_all_coins():
        return Coin.query.all()

    @staticmethod
    def get_coin_by_symbol(symbol):
        return Coin.query.filter_by(symbol=symbol).first()

    @staticmethod
    def add_coin(symbol, name, price):
        coin = Coin(symbol=symbol.upper(), name=name, price=price)
        db.session.add(coin)
        db.session.commit()
        return coin
