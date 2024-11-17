from sqlalchemy import Column, String, Float
from app.extensions import db

class Coin(db.Model):
    __tablename__ = "coins"
    symbol = Column(String(10), primary_key=True)  # Example: BTC, ETH
    name = Column(String(50), nullable=False)     # Example: Bitcoin, Ethereum
    price = Column(Float, nullable=False)

    def __repr__(self):
        return f"<Coin {self.symbol} Price={self.price}>"
