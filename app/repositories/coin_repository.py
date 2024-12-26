from app.models.coin import Coin
from app.extensions import db
from app.models.price_history import PriceHistory
from sqlalchemy import func

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
    
    @staticmethod
    def get_ohlc_data(symbol, interval, start_time):
        """
        Retrieve aggregated OHLC data for the given symbol and interval using PostgreSQL.
        """
        interval_map = {
            "1m": "minute",
            "15m": "15 minutes",
            "1h": "hour",
            "4h": "4 hours",
            "1d": "day",
            "1w": "week",
        }

        if interval not in interval_map:
            raise ValueError("Invalid interval provided")

        pg_interval = interval_map[interval]

        ohlc_query = (
            db.session.query(
                func.date_trunc(pg_interval, PriceHistory.timestamp).label("interval"),
                func.min(PriceHistory.price).label("low"),
                func.max(PriceHistory.price).label("high"),
                func.min(PriceHistory.timestamp).label("min_time"),
                func.max(PriceHistory.timestamp).label("max_time"),
            )
            .filter(PriceHistory.symbol == symbol, PriceHistory.timestamp >= start_time)
            .group_by(func.date_trunc(pg_interval, PriceHistory.timestamp))
            .order_by(func.date_trunc(pg_interval, PriceHistory.timestamp))
            .all()
        )

        return [
            {
                "interval": row.interval,
                "low": row.low,
                "high": row.high,
                "open": db.session.query(PriceHistory.price)
                .filter(PriceHistory.symbol == symbol, PriceHistory.timestamp == row.min_time)
                .scalar(),
                "close": db.session.query(PriceHistory.price)
                .filter(PriceHistory.symbol == symbol, PriceHistory.timestamp == row.max_time)
                .scalar(),
            }
            for row in ohlc_query
        ]