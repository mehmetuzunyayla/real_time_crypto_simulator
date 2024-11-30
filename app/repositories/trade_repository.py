from app.models.trade import Trade
from app.extensions import db

class TradeRepository:
    @staticmethod
    def get_trade_by_id(trade_id):
        return Trade.query.get(trade_id)

    @staticmethod
    def get_trades_by_user_id(user_id):
        return Trade.query.filter_by(user_id=user_id).all()

    @staticmethod
    def create_trade(user_id, coin_symbol, trade_type, quantity, price_at_trade, direction):
        trade = Trade(
            user_id=user_id,
            coin_symbol=coin_symbol.upper(),
            trade_type=trade_type,
            quantity=quantity,
            price_at_trade=price_at_trade,
            direction=direction.lower()
        )
        db.session.add(trade)
        db.session.commit()
        return trade

    @staticmethod
    def close_trade(trade_id):
        trade = Trade.query.get(trade_id)
        if trade and trade.status != "closed":
            trade.status = "closed"
            db.session.commit()
        return trade
