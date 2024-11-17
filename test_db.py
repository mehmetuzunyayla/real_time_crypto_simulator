from app import create_app, db
from app.models.user import User

app = create_app()

with app.app_context():
    # Add a test user
    test_user = User(username="testuser", email="test@example.com", password_hash="hashedpassword")
    db.session.add(test_user)
    db.session.commit()

    # Query the test user
    user = User.query.filter_by(username="testuser").first()
    print(f"User: {user.username}, Email: {user.email}")
