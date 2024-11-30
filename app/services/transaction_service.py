from app.models.transaction import Transaction
from app.extensions import db

class TransactionService:
    @staticmethod
    def get_transactions(wallet_id):
        transactions = Transaction.query.filter_by(wallet_id=wallet_id).all()
        if not transactions:
            return {"error": "No transactions found"}, 404

        transaction_list = [
            {"id": tx.id, "amount": tx.amount, "description": tx.description, "timestamp": tx.timestamp}
            for tx in transactions
        ]
        return transaction_list, 200

    @staticmethod
    def log_transaction(wallet_id, amount, description):
        new_transaction = Transaction(
            wallet_id=wallet_id,
            amount=amount,
            description=description
        )
        db.session.add(new_transaction)
        db.session.commit()
        return {"message": "Transaction logged successfully", "transaction_id": new_transaction.id}, 201
