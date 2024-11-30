from app.models.wallet import Wallet
from app.extensions import db

class WalletService:
    @staticmethod
    def get_wallet(user_id):
        wallet = Wallet.query.filter_by(user_id=user_id).first()
        if not wallet:
            return {"error": "Wallet not found"}, 404
        return {"user_id": wallet.user_id, "balance": wallet.balance}, 200

    @staticmethod
    def update_wallet(user_id, amount):
        wallet = Wallet.query.filter_by(user_id=user_id).first()
        if not wallet:
            return {"error": "Wallet not found"}, 404

        wallet.balance += amount
        db.session.commit()
        return {"message": "Wallet updated successfully", "balance": wallet.balance}, 200
