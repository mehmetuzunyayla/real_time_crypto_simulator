import time
from app.utils.price_fetcher import PriceFetcher

def start_price_updater(app, interval=5):
    import threading
    import time

    def fetch_prices_periodically():
        while True:
            with app.app_context():
                PriceFetcher.fetch_prices()
            time.sleep(interval)

    thread = threading.Thread(target=fetch_prices_periodically)
    thread.daemon = True
    thread.start()
