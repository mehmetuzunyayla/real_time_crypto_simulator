from app.models.user import User
from app.extensions import db

class UserRepository:
    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def create_user(username, email, password_hash):
        user = User(username=username, email=email, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def update_username(user_id, new_username):
        user = User.query.get(user_id)
        if user:
            user.username = new_username
            db.session.commit()