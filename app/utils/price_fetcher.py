import requests
import time
from datetime import datetime, timedelta
from app.models.price_history import PriceHistory
from app.extensions import db, socketio
from sqlalchemy.exc import SQLAlchemyError


class PriceFetcher:
    BASE_URL = "https://api.binance.com/api/v3/ticker/24hr"  # Binance 24-hour stats endpoint
    HISTORICAL_URL = "https://api.binance.com/api/v3/klines"  # Binance Klines endpoint
    COIN_LIST = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT", "DOGEUSDT",
                 "SOLUSDT", "DOTUSDT", "LTCUSDT", "LINKUSDT", "UNIUSDT",
                 "XLMUSDT", "VETUSDT", "TRXUSDT", "XMRUSDT", "XTZUSDT",
                 "AAVEUSDT", "THETAUSDT", "EOSUSDT", "ATOMUSDT", "FILUSDT"]
    cached_prices = {}

    @staticmethod
    def initialize_historical_data():
        """
        Initialize the historical data for the last 3 days.
        Deletes old data and fetches the latest values from Binance.
        """
        try:
            # Clear existing historical data
            db.session.query(PriceHistory).delete()
            db.session.commit()
            print("[PriceFetcher] Cleared old historical data.")

            # Fetch and save historical data for the last 3 days for each coin
            for symbol in PriceFetcher.COIN_LIST:
                params = {
                    "symbol": symbol,
                    "interval": "1m",  # Fetch 1-minute data
                    "startTime": int((datetime.utcnow() - timedelta(days=2)).timestamp() * 1000),
                    "endTime": int(datetime.utcnow().timestamp() * 1000),
                    "limit": 1000  # Binance allows fetching up to 1000 records per request
                }
                response = requests.get(PriceFetcher.HISTORICAL_URL, params=params)
                response.raise_for_status()
                data = response.json()

                # Save the fetched data to the database
                for item in data:
                    timestamp = datetime.fromtimestamp(item[0] / 1000)
                    price = float(item[4])  # Closing price
                    price_entry = PriceHistory(symbol=symbol.lower(), price=price, timestamp=timestamp)
                    db.session.add(price_entry)
                db.session.commit()
                print(f"[PriceFetcher] Historical data saved for {symbol}.")

        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"[PriceFetcher] Database error: {str(e)}")
        except Exception as e:
            print(f"[PriceFetcher] Error initializing historical data: {str(e)}")

    @staticmethod
    def fetch_prices():
        """
        Fetch live prices for all coins and broadcast them via WebSocket.
        """
        try:
            response = requests.get(PriceFetcher.BASE_URL)
            response.raise_for_status()
            data = response.json()

            # Filter and structure data for COIN_LIST
            filtered_data = {}
            for item in data:
                symbol = item["symbol"]
                if symbol in PriceFetcher.COIN_LIST:
                    current_price = float(item["lastPrice"])
                    daily_change = float(item["priceChangePercent"])  # Directly from Binance API

                    # Build filtered data structure without icons
                    filtered_data[symbol] = {
                        "price": current_price,
                        "daily_change": daily_change
                    }

            # Update cached prices
            PriceFetcher.cached_prices = filtered_data

            # Save historical prices to the database
            for symbol, data in filtered_data.items():
                coin_symbol = symbol[:-4]  # Remove 'USDT' from the symbol
                price_entry = PriceHistory(symbol=coin_symbol.lower(), price=data["price"])
                db.session.add(price_entry)
            db.session.commit()

            # Broadcast prices to WebSocket clients
            socketio.emit('price_update', PriceFetcher.cached_prices)

            return {"message": "Prices updated and broadcasted successfully"}, 200
        except Exception as e:
            print(f"[PriceFetcher] Error fetching prices: {str(e)}")
            return {"error": str(e)}, 500

    @staticmethod
    def get_cached_prices():
        """
        Retrieve cached prices for all coins. If prices are not available yet, return an error.
        """
        if not PriceFetcher.cached_prices:
            return {"error": "Prices are not available yet, please wait for the initial fetch."}, 503
        return PriceFetcher.cached_prices, 200
