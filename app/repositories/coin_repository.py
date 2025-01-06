from app.models.coin import Coin
from app.extensions import db
from app.models.price_history import PriceHistory
from sqlalchemy import func,text

class CoinRepository:
    @staticmethod
    def get_all_coins():
        """
        Retrieve all unique coins from price_history.
        """
        query = text("SELECT DISTINCT symbol FROM price_history;")
        result = db.session.execute(query).fetchall()
        
        return [row[0].upper() for row in result]  # row[0] because fetchall() returns tuples
    
    @staticmethod
    def get_coin_by_symbol(symbol):
        """
        Retrieve the latest price entry for a specific coin, ensuring case-insensitivity.
        """
        query = text("""
            SELECT symbol, price, timestamp
            FROM price_history
            WHERE LOWER(symbol) = LOWER(:symbol)  -- Ensure case insensitivity
            ORDER BY timestamp DESC
            LIMIT 1;
        """)
        result = db.session.execute(query, {"symbol": symbol}).fetchone()
        
        if result:
            return {"symbol": result[0].upper(), "price": result[1], "timestamp": result[2]}  # Format response
        return None

    @staticmethod
    def add_coin(symbol, name, price):
        coin = Coin(symbol=symbol.upper(), name=name, price=price)
        db.session.add(coin)
        db.session.commit()
        return coin
    
    @staticmethod
    def get_ohlc_data(symbol, interval, start_time):
        """
        Retrieve aggregated OHLC (Open-High-Low-Close) data for the given symbol and interval.
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

        query = text(f"""
            WITH price_data AS (
                SELECT 
                    date_trunc('{pg_interval}', timestamp) AS interval,
                    symbol,
                    price,
                    timestamp
                FROM price_history
                WHERE symbol = :symbol AND timestamp >= :start_time
            ),
            grouped_data AS (
                SELECT
                    interval,
                    MIN(price) AS low,
                    MAX(price) AS high
                FROM price_data
                GROUP BY interval
            ),
            open_prices AS (
                SELECT DISTINCT ON (interval) interval, price AS open_price
                FROM price_data
                ORDER BY interval, timestamp ASC
            ),
            close_prices AS (
                SELECT DISTINCT ON (interval) interval, price AS close_price
                FROM price_data
                ORDER BY interval, timestamp DESC
            )
            SELECT 
                gd.interval,
                gd.low,
                gd.high,
                op.open_price,
                cp.close_price
            FROM grouped_data gd
            JOIN open_prices op ON gd.interval = op.interval
            JOIN close_prices cp ON gd.interval = cp.interval
            ORDER BY gd.interval;
        """)


        result = db.session.execute(query, {"symbol": symbol, "start_time": start_time}).fetchall()

        return [
            {
                "interval": row[0].isoformat() if hasattr(row[0], "isoformat") else row[0],
                "low": float(row[1]),
                "high": float(row[2]),
                "open": float(row[3]),
                "close": float(row[4]),
            }
            for row in result
        ]