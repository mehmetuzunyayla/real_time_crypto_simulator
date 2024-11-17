from flask import Flask
from app.extensions import db, migrate
from app.config import Config

# Import models
from app.models.user import User
from app.models.wallet import Wallet
from app.models.coin import Coin
from app.models.trade import Trade
from app.models.transaction import Transaction

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register controllers
    from app.controllers.user_controller import bp as user_bp
    from app.controllers.wallet_controller import bp as wallet_bp
    from app.controllers.coin_controller import bp as coin_bp
    from app.controllers.trade_controller import bp as trade_bp
    from app.controllers.transaction_controller import bp as transaction_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(wallet_bp)
    app.register_blueprint(coin_bp)
    app.register_blueprint(trade_bp)
    app.register_blueprint(transaction_bp)

    return app
