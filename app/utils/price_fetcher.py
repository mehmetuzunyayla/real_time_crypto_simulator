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
                 "XLMUSDT", "VETUSDT", "TRXUSDT", "XVGUSDT", "XTZUSDT",
                 "AAVEUSDT", "THETAUSDT", "EOSUSDT", "ATOMUSDT", "FILUSDT"]
    cached_prices = {}

    @staticmethod
    def initialize_historical_data():
        """
        Fetches historical data for each coin in small chunks to avoid API limitations.
        """
        try:
            db.session.query(PriceHistory).delete()  # Clear previous data
            db.session.commit()
            print("[PriceFetcher] Cleared old historical data.")

            for symbol in PriceFetcher.COIN_LIST:
                print(f"[PriceFetcher] Fetching historical data for {symbol}...")

                end_time = int(datetime.utcnow().timestamp() * 1000)
                start_time = int((datetime.utcnow() - timedelta(days=3)).timestamp() * 1000)

                while start_time < end_time:
                    params = {
                        "symbol": symbol,
                        "interval": "1m",  # 1-minute data
                        "startTime": start_time,
                        "endTime": end_time,
                        "limit": 1000  # Fetch 1000 records at a time
                    }
                    response = requests.get(PriceFetcher.HISTORICAL_URL, params=params)
                    response.raise_for_status()
                    data = response.json()

                    if not data:
                        print(f"[PriceFetcher] No more historical data for {symbol}.")
                        break

                    for item in data:
                        timestamp = datetime.fromtimestamp(item[0] / 1000)
                        price = float(item[4])  # Closing price
                        price_entry = PriceHistory(symbol=symbol.lower(), price=price, timestamp=timestamp)
                        db.session.add(price_entry)

                    db.session.commit()
                    print(f"[PriceFetcher] Saved {len(data)} historical records for {symbol}.")

                    # ✅ Fixed timestamp handling for pagination
                    start_time = data[-1][0] + 1  # Move forward by 1 millisecond

                    # Avoid hitting Binance API rate limits
                    time.sleep(0.5)

        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"[PriceFetcher] Database error: {str(e)}")
        except Exception as e:
            print(f"[PriceFetcher] Error initializing historical data: {str(e)}")
            
    @staticmethod
    def fetch_prices():
        """
        Fetch live prices for all coins and store them in price_history.
        Ensures symbols are always stored in "btcusdt" format.
        """
        try:
            response = requests.get(PriceFetcher.BASE_URL)
            response.raise_for_status()
            data = response.json()

            filtered_data = {}
            for item in data:
                symbol = item["symbol"]

                if symbol in PriceFetcher.COIN_LIST:
                    # Convert symbol to lowercase and ensure "usdt" is always included
                    standardized_symbol = symbol.lower()

                    current_price = float(item["lastPrice"])
                    daily_change = float(item["priceChangePercent"])

                    # Store in cache for WebSocket updates
                    filtered_data[standardized_symbol] = {
                        "price": current_price,
                        "daily_change": daily_change
                    }

                    # Save to database
                    price_entry = PriceHistory(
                        symbol=standardized_symbol,
                        price=current_price,
                        timestamp=datetime.utcnow()
                    )
                    db.session.add(price_entry)

            # Commit all changes to database
            db.session.commit()

            # Update cached prices
            PriceFetcher.cached_prices = filtered_data

            # Broadcast prices to WebSocket clients
            socketio.emit('price_update', PriceFetcher.cached_prices)

            return {"message": "Prices updated and broadcasted successfully"}, 200

        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"[PriceFetcher] Database error: {str(e)}")
            return {"error": str(e)}, 500

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
