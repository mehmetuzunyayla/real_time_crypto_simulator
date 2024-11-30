from app.repositories.transaction_repository import TransactionRepository

class TransactionService:
    @staticmethod
    def get_transactions(wallet_id):
        transactions = TransactionRepository.get_transactions_by_wallet_id(wallet_id)
        if not transactions:
            return {"error": "No transactions found"}, 404

        transaction_list = [
            {"id": tx.id, "amount": tx.amount, "description": tx.description, "timestamp": tx.timestamp}
            for tx in transactions
        ]
        return transaction_list, 200

    @staticmethod
    def log_transaction(wallet_id, amount, description):
        transaction = TransactionRepository.log_transaction(wallet_id, amount, description)
        return {"message": "Transaction logged successfully", "transaction_id": transaction.id}, 201
