from app.models.trade import Trade, TradeType
from app.extensions import db

class TradeService:
    @staticmethod
    def create_trade(user_id, coin_symbol, trade_type, quantity, price_at_trade, direction):
        new_trade = Trade(
            user_id=user_id,
            coin_symbol=coin_symbol.upper(),
            trade_type=TradeType[trade_type.upper()],
            quantity=quantity,
            price_at_trade=price_at_trade,
            direction=direction.lower(),
        )
        db.session.add(new_trade)
        db.session.commit()
        return {"message": "Trade created successfully", "trade_id": new_trade.id}, 201

    @staticmethod
    def close_trade(trade_id):
        trade = Trade.query.get(trade_id)
        if not trade or trade.status == "closed":
            return {"error": "Trade not found or already closed"}, 404

        trade.status = "closed"
        db.session.commit()
        return {"message": "Trade closed successfully"}, 200
