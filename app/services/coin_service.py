from app.repositories.coin_repository import CoinRepository
from datetime import datetime, timedelta

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
    
    @staticmethod
    def get_historical_ohlc(symbol, interval):
        """
        Retrieve OHLC historical data for a given coin symbol and interval.
        """
        # Define valid intervals
        valid_intervals = ["1m", "15m", "1h", "4h", "1d", "1w"]

        if interval not in valid_intervals:
            return {"error": "Invalid interval provided"}, 400

        # Calculate start time (last 7 days)
        now = datetime.utcnow()
        start_time = now - timedelta(days=2)

        # Query OHLC data from the repository
        ohlc_data = CoinRepository.get_ohlc_data(symbol, interval, start_time)
        
        if not ohlc_data:
            return {"error": f"No historical data found for coin: {symbol}"}, 404

        # Format the response
        response = [
            {
                "time": row["interval"].isoformat(),
                "open": float(row["open"]),
                "high": float(row["high"]),
                "low": float(row["low"]),
                "close": float(row["close"]),
            }
            for row in ohlc_data
        ]
        return response, 200