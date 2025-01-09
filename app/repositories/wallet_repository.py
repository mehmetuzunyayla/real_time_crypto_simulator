from app.models.wallet import Wallet
from app.extensions import db

class WalletRepository:
    @staticmethod
    def get_wallet_by_user_id(user_id):
        return Wallet.query.filter_by(user_id=user_id).first()

    @staticmethod
    def create_wallet(user_id, balance=1000.0):
        wallet = Wallet(user_id=user_id, balance=balance)
        db.session.add(wallet)
        db.session.commit()
        return wallet

    @staticmethod
    def update_wallet_balance(wallet_id, amount):
        wallet = Wallet.query.get(wallet_id)
        if wallet:
            wallet.balance += amount
            db.session.commit()
        return wallet
    
    @staticmethod
    def update_wallet_balance2(wallet_id, new_balance):
        wallet = Wallet.query.get(wallet_id)
        if wallet:
            wallet.balance = new_balance
            db.session.commit()
        return wallet
