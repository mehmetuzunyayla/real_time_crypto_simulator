from app.repositories.trade_repository import TradeRepository
from app.repositories.wallet_repository import WalletRepository
from app.utils.profit_loss import ProfitLossCalculator

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
        trade = TradeRepository.get_trade_by_id(trade_id)
        if not trade or trade.status == "closed":
            return {"error": "Trade not found or already closed"}, 404

        wallet = WalletRepository.get_wallet_by_user_id(trade.user_id)
        pnl = ProfitLossCalculator.calculate_pnl(trade)
        WalletRepository.update_wallet_balance(wallet.id, pnl)

        closed_trade = TradeRepository.close_trade(trade_id)
        return {"message": "Trade closed successfully", "pnl": pnl}, 200
    
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
            }
            for trade in trades
        ]
        return trade_list, 200

