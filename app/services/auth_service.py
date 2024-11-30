import jwt
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from app.config import Config
from app.repositories.user_repository import UserRepository
from app.repositories.wallet_repository import WalletRepository

class AuthService:
    @staticmethod
    def register_user(username, email, password):
        existing_user = UserRepository.get_user_by_email(email)
        if existing_user:
            return {"error": "User already exists"}, 400

        hashed_password = generate_password_hash(password)
        user = UserRepository.create_user(username, email, hashed_password)
        WalletRepository.create_wallet(user_id=user.id, balance=0.0)

        return {"message": f"User {user.username} registered successfully"}, 201

    @staticmethod
    def login_user(email, password):
        user = UserRepository.get_user_by_email(email)
        if not user or not check_password_hash(user.password_hash, password):
            return {"error": "Invalid credentials"}, 401

        payload = {
            "user_id": user.id,
            "exp": datetime.utcnow() + timedelta(hours=1)
        }
        token = jwt.encode(payload, Config.USER_SECRET_KEY, algorithm="HS256")
        return {"message": "Login successful", "token": token}, 200
