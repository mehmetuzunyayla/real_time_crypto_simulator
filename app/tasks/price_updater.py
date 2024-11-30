import time
from app.utils.price_fetcher import PriceFetcher

def start_price_updater(app, interval=5):
    """
    Start a background thread to update prices periodically.
    Ensures the task runs inside the Flask application context.
    """
    def update_prices():
        with app.app_context():
            # Fetch prices once at startup
            #print("[PriceUpdater] Starting initial fetch.")
            PriceFetcher.fetch_prices()

            # Start periodic updates
            while True:
                #print("[PriceUpdater] Fetching prices...")
                PriceFetcher.fetch_prices()
                time.sleep(interval)

    # Start the thread
    import threading
    thread = threading.Thread(target=update_prices, daemon=True)
    thread.start()
    #print("[PriceUpdater] Background price updater started.")
