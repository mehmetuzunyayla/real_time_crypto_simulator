from flask import Flask
from app.extensions import db, migrate, socketio
from app.config import Config
from app.tasks.price_updater import start_price_updater
from app.utils.price_fetcher import PriceFetcher  # Import PriceFetcher
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)  # Ensure 'db' is passed here
    socketio.init_app(app)

    with app.app_context():
        # Initialize historical data
        PriceFetcher.initialize_historical_data()

    # Start price updater
    start_price_updater(app, interval=5)

    # Register controllers
    from app.controllers.user_controller import bp as user_bp
    from app.controllers.wallet_controller import bp as wallet_bp
    from app.controllers.coin_controller import bp as coin_bp
    from app.controllers.trade_controller import bp as trade_bp
    from app.controllers.transaction_controller import bp as transaction_bp
    from app.controllers.home_controller import bp as home_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(wallet_bp)
    app.register_blueprint(coin_bp)
    app.register_blueprint(trade_bp)
    app.register_blueprint(transaction_bp)
    app.register_blueprint(home_bp)

    return app
