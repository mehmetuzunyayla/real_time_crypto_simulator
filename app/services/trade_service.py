from app.repositories.trade_repository import TradeRepository
from app.repositories.wallet_repository import WalletRepository
from app.utils.profit_loss import ProfitLossCalculator
from app.utils.price_fetcher import PriceFetcher

class TradeService:
    @staticmethod
    def create_trade(user_id, coin_symbol, trade_type, quantity, price_at_trade, direction):
        wallet = WalletRepository.get_wallet_by_user_id(user_id)
        if not wallet or wallet.balance < (quantity * price_at_trade):
            return {"error": "Insufficient balance"}, 400

        trade = TradeRepository.create_trade(user_id, coin_symbol, trade_type, quantity, price_at_trade, direction)
        WalletRepository.update_wallet_balance(wallet.id, -(quantity * price_at_trade))
        return {"message": "Trade created successfully", "trade_id": trade.id}, 201

    @staticmethod
    def close_trade(trade_id):
        """
        Closes an open trade, calculates PnL, and updates the user's wallet balance.
        :param trade_id: ID of the trade to close.
        :return: Updated trade with close PnL and modified wallet balance.
        """
        if not isinstance(trade_id, int):
            return {"error": "Invalid trade ID."}, 400

        trade = TradeRepository.get_trade_by_id(trade_id)
        if not trade:
            return {"error": "Trade not found"}, 404

        if trade.status != "open":
            return {"error": "Trade is already closed"}, 400

        # ✅ Fetch latest price from PriceFetcher
        prices, _ = PriceFetcher.get_cached_prices()
        current_price = prices.get(trade.coin_symbol.lower(), {}).get("price", 0.0)

        # ✅ Calculate PnL
        close_pnl = ProfitLossCalculator.calculate_pnl(trade, current_price)

        # ✅ Store `close_pnl` in the trade record
        updated_trade = TradeRepository.close_trade(trade_id, close_pnl)

        # ✅ Ensure `close_pnl` is saved
        updated_trade.close_pnl = close_pnl

        # ✅ Update wallet balance
        wallet = WalletRepository.get_wallet_by_user_id(updated_trade.user_id)
        if not wallet:
            return {"error": "Wallet not found"}, 404

        total_return = (trade.quantity * trade.price_at_trade) + close_pnl
        WalletRepository.update_wallet_balance2(wallet.id, wallet.balance + total_return)

        return {
            "message": "Trade closed successfully",
            "close_pnl": close_pnl,
            "new_wallet_balance": wallet.balance + total_return
        }, 200
    
    @staticmethod
    def get_trades_by_user_id(user_id):
        trades = TradeRepository.get_trades_by_user_id(user_id)
        if not trades:
            return {"error": "No trades found"}, 404
        
        trade_list = [
            {
                "id": trade.id,
                "coin_symbol": trade.coin_symbol,
                "trade_type": trade.trade_type.value,
                "direction": trade.direction,
                "quantity": trade.quantity,
                "price_at_trade": trade.price_at_trade,
                "status": trade.status,
                "close_pnl": trade.close_pnl if trade.status == "closed" else None  # ✅ Ensure PnL is included

            }
            for trade in trades
        ]
        return trade_list, 200

