from app.utils.price_fetcher import PriceFetcher

class ProfitLossCalculator:
    @staticmethod
    def calculate_pnl(trade, current_price=None):
        """
        Calculate the Profit & Loss (PnL) for a trade (Only Spot Trades).
        :param trade: Trade object containing quantity and price_at_trade.
        :param current_price: Current price of the coin.
        :return: The calculated PnL value.
        """
        # Fetch current price if not provided
        if current_price is None:
            prices, _ = PriceFetcher.get_cached_prices()
            current_price = prices.get(trade.coin_symbol.lower(), {}).get("price", 0.0)

        
        return (current_price - trade.price_at_trade) * trade.quantity
