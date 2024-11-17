from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Float, ForeignKey
from app.extensions import db

class Wallet(db.Model):
    __tablename__ = "wallets"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    balance = Column(Float, default=0.0)

    # Relationships
    user = relationship("User", back_populates="wallet")
    transactions = relationship("Transaction", back_populates="wallet")

    def __repr__(self):
        return f"<Wallet UserID={self.user_id} Balance={self.balance}>"
