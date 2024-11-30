import jwt
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from app.config import Config
from app.models.user import User
from app.extensions import db
from app.models.wallet import Wallet  # Import Wallet

class AuthService:
    @staticmethod
    def register_user(username, email, password):
        if User.query.filter_by(email=email).first():
            return {"error": "User already exists"}, 400

        # Hash the user's password
        hashed_password = generate_password_hash(password)

        # Create the user
        new_user = User(
            username=username,
            email=email,
            password_hash=hashed_password,
        )
        db.session.add(new_user)
        db.session.flush()  # Flush to get the new user's ID before committing

        # Create a wallet for the user with a starting balance of $1000
        new_wallet = Wallet(
            user_id=new_user.id,
            balance=1000.0
        )
        db.session.add(new_wallet)

        # Commit both the user and the wallet
        db.session.commit()

        return {"message": "User registered successfully, wallet created with $1000 balance"}, 201
    @staticmethod
    def login_user(email, password):
        # Verify email and password
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password_hash, password):
            return {"error": "Invalid credentials"}, 401

        # Generate JWT token with 1-hour expiration
        payload = {
            "user_id": user.id,
            "exp": datetime.utcnow() + timedelta(hours=1)  # Token expires in 1 hour
        }
        token = jwt.encode(payload, Config.USER_SECRET_KEY, algorithm="HS256")
        return {"message": "Login successful", "token": token}, 200
