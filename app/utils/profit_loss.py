from app.utils.price_fetcher import PriceFetcher

class ProfitLossCalculator:
    @staticmethod
    def calculate_pnl(trade, current_price=None):
        """
        Calculate the Profit & Loss (PnL) for a trade.
        :param trade: Trade object containing quantity, price_at_trade, and direction.
        :param current_price: Current price of the coin.
        :return: The calculated PnL value.
        """
        # Fetch current price if not provided
        if current_price is None:
            prices, _ = PriceFetcher.get_cached_prices()
            current_price = prices.get(trade.coin_symbol.lower(), {}).get("price", 0.0)

        if trade.direction == "long":
            return (current_price - trade.price_at_trade) * trade.quantity
        elif trade.direction == "short":
            return (trade.price_at_trade - current_price) * trade.quantity
        else:
            return 0.0
