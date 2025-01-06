from app.repositories.coin_repository import CoinRepository
from datetime import datetime, timedelta

class CoinService:
    @staticmethod
    def get_all_coins():
        """
        Retrieve all unique coins from price_history.
        """
        coins = CoinRepository.get_all_coins()
        coin_list = [{"symbol": coin} for coin in coins]  # Adjusted to match new repository return format
        return coin_list, 200

    @staticmethod
    def get_coin(symbol):
        """
        Retrieve the latest price for a specific coin.
        """
        coin = CoinRepository.get_coin_by_symbol(symbol)
        if not coin:
            return {"error": "Coin not found"}, 404
        return {"symbol": coin["symbol"], "price": coin["price"], "timestamp": coin["timestamp"]}, 200
    
    @staticmethod
    def get_historical_ohlc(symbol, interval):
        """
        Retrieve OHLC historical data for a given coin symbol and interval.
        """
        ohlc_data = CoinRepository.get_ohlc_data(symbol, interval, datetime.utcnow() - timedelta(days=3))

        if not ohlc_data:
            return {"error": f"No historical data found for coin: {symbol}"}, 404

        # Ensure interval is treated as a datetime before calling isoformat()
        response = [
            {
                "time": row["interval"] if isinstance(row["interval"], str) else row["interval"].isoformat(),
                "open": float(row["open"]),
                "high": float(row["high"]),
                "low": float(row["low"]),
                "close": float(row["close"]),
            }
            for row in ohlc_data
        ]
        return response, 200