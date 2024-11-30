import requests
import time
from app.models.price_history import PriceHistory
from app.extensions import db

class PriceFetcher:
    BASE_URL = "https://api.binance.com/api/v3/ticker/price"
    COIN_LIST = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT", "DOGEUSDT",
                 "SOLUSDT", "DOTUSDT", "LTCUSDT", "LINKUSDT", "UNIUSDT",
                 "XLMUSDT", "VETUSDT", "TRXUSDT", "XMRUSDT", "XTZUSDT",
                 "AAVEUSDT", "THETAUSDT", "EOSUSDT", "ATOMUSDT", "FILUSDT"]
    cached_prices = {}

    @staticmethod
    def fetch_prices():
        """
        Fetch prices for all coins in COIN_LIST from Binance.
        Save historical data in the database.
        """
        try:
            response = requests.get(PriceFetcher.BASE_URL)
            response.raise_for_status()
            data = response.json()

            # Filter data for COIN_LIST
            filtered_data = {
                item["symbol"]: float(item["price"])
                for item in data if item["symbol"] in PriceFetcher.COIN_LIST
            }

            # Log fetched data
            #print(f"[PriceFetcher] Fetched prices at {time.time()}:\n{filtered_data}")

            # Update cached prices
            PriceFetcher.cached_prices = {
                symbol: {"price": price, "last_updated": time.time()}
                for symbol, price in filtered_data.items()
            }

            # Save historical prices to the database
            for symbol, price in filtered_data.items():
                coin_symbol = symbol[:-4]  # Remove 'USDT' from the symbol
                price_entry = PriceHistory(symbol=coin_symbol.lower(), price=price)
                db.session.add(price_entry)
            db.session.commit()

            return {"message": "Prices updated successfully"}, 200
        except Exception as e:
            print(f"[PriceFetcher] Error fetching prices: {str(e)}")
            return {"error": str(e)}, 500

    @staticmethod
    def get_cached_prices():
        """
        Retrieve cached prices for all coins.
        """
        if not PriceFetcher.cached_prices:
            return {"error": "Prices are not available yet, please wait for the initial fetch."}, 503
        return PriceFetcher.cached_prices, 200
