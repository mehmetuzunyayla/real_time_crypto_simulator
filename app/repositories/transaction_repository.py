from app.models.transaction import Transaction
from app.extensions import db

class TransactionRepository:
    @staticmethod
    def get_transactions_by_wallet_id(wallet_id):
        return Transaction.query.filter_by(wallet_id=wallet_id).all()

    @staticmethod
    def log_transaction(wallet_id, amount, description):
        transaction = Transaction(wallet_id=wallet_id, amount=amount, description=description)
        db.session.add(transaction)
        db.session.commit()
        return transaction
