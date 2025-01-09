import os
from dotenv import load_dotenv


load_dotenv()
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")  # Keep your existing secret key
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "postgresql://yourusername:yourpassword@localhost:5432/yourdatabasename"
    )  # Update this with PostgreSQL credentials
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    USER_SECRET_KEY = os.getenv("USER_SECRET_KEY", "default_user_secret_key")  # Keep your JWT secret key
