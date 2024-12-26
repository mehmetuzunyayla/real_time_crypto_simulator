from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from app.extensions import db

class User(db.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(512), nullable=False)
    created_at = Column(db.DateTime, default=db.func.now())
    updated_at = Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    # Relationships
    wallet = relationship("Wallet", uselist=False, back_populates="user")
    trades = relationship("Trade", back_populates="user")

    def __repr__(self):
        return f"<User {self.username}>"
