from sqlalchemy import Column, Integer, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from app.extensions import db

class Transaction(db.Model):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    wallet_id = Column(Integer, ForeignKey("wallets.id"), nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String(255), nullable=True)  # Example: "P&L update", "Deposit"
    timestamp = Column(db.DateTime, default=db.func.now())

    wallet = relationship("Wallet", back_populates="transactions")

    def __repr__(self):
        return f"<Transaction {self.amount} Description={self.description}>"
