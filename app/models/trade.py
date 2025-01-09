from sqlalchemy import Column, Integer, Float, ForeignKey, String, Enum
from sqlalchemy.orm import relationship
from app.extensions import db
import enum

class TradeType(enum.Enum):
    SPOT = "spot"
    FUTURES = "futures"

class Trade(db.Model):
    __tablename__ = "trades"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    coin_symbol = Column(String(10), ForeignKey("coins.symbol"), nullable=False)
    trade_type = Column(Enum(TradeType), nullable=False)
    quantity = Column(Float, nullable=False)
    price_at_trade = Column(Float, nullable=False)  # Price when the trade was made
    direction = Column(String(10), nullable=False)  # "long" or "short"
    status = Column(String(10), default="open")     # "open" or "closed"
    close_pnl = Column(Float, nullable=True)  # ✅ New column to store profit/loss when trade is closed

    user = relationship("User", back_populates="trades")
    coin = relationship("Coin")

    def __repr__(self):
        return f"<Trade {self.trade_type} {self.direction} {self.quantity} {self.coin_symbol}>"
