from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.sql import func
from app.extensions import db

class PriceHistory(db.Model):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(10), nullable=False)  # Coin symbol (e.g., BTC)
    price = Column(Float, nullable=False)       # Price in USD
    timestamp = Column(DateTime, default=func.now())  # Timestamp of the record
