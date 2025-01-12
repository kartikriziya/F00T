# init_db.py
from app import app, db
from models import User, Game, Drive, Play

def init_database():
    with app.app_context():
        # Drop all existing tables
        db.drop_all()
        
        # Create all tables
        db.create_all()
        
        # Create a test user
        test_user = User(
            username="coach",
            password="password123"  # In production, use password hashing!
        )
        db.session.add(test_user)
        db.session.commit()
        
        print("Database initialized!")

if __name__ == "__main__":
    init_database()