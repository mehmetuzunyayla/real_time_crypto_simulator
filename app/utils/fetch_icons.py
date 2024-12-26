import os
import requests

ICON_BASE_URL = "https://www.cryptocompare.com"  # Base URL for icons
SAVE_DIR = "app/static/icons"
API_URL = "https://min-api.cryptocompare.com/data/all/coinlist"
COIN_LIST = ["BTC", "ETH", "BNB", "ADA", "DOGE", "SOL", "DOT", "LTC", "LINK", "UNI",
             "XLM", "VET", "TRX", "XMR", "XTZ", "AAVE", "THETA", "EOS", "ATOM", "FIL"]

def fetch_and_save_icons():
    # Ensure the directory exists
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    try:
        # Fetch all coin data from CryptoCompare
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()["Data"]

        for coin in COIN_LIST:
            coin_data = data.get(coin)
            if coin_data and "ImageUrl" in coin_data:
                icon_url = ICON_BASE_URL + coin_data["ImageUrl"]
                file_path = os.path.join(SAVE_DIR, f"{coin.lower()}.png")

                # Download and save the icon
                icon_response = requests.get(icon_url, stream=True)
                icon_response.raise_for_status()
                with open(file_path, "wb") as f:
                    for chunk in icon_response.iter_content(1024):
                        f.write(chunk)

                print(f"Saved icon for {coin} at {file_path}")
            else:
                print(f"Icon not found for {coin}")
    except Exception as e:
        print(f"Error fetching icons: {e}")


if __name__ == "__main__":
    fetch_and_save_icons()
