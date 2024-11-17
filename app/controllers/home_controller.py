from flask import Blueprint

bp = Blueprint("home", __name__)

@bp.route("/", methods=["GET"])
def home():
    return "Welcome to the Real-Time Crypto Simulator!", 200
