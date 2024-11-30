from app.repositories.wallet_repository import WalletRepository
from app.repositories.transaction_repository import TransactionRepository

class WalletService:
    @staticmethod
    def get_wallet(user_id):
        wallet = WalletRepository.get_wallet_by_user_id(user_id)
        if not wallet:
            return {"error": "Wallet not found"}, 404
        return {"user_id": wallet.user_id, "balance": wallet.balance}, 200

    @staticmethod
    def update_wallet(user_id, amount):
        wallet = WalletRepository.get_wallet_by_user_id(user_id)
        if not wallet:
            return {"error": "Wallet not found"}, 404

        updated_wallet = WalletRepository.update_wallet_balance(wallet.id, amount)
        TransactionRepository.log_transaction(wallet.id, amount, "Wallet update")
        return {"message": "Wallet updated successfully", "balance": updated_wallet.balance}, 200
