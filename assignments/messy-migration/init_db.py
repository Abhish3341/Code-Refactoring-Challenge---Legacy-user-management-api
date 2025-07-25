from models.user import User
from config import Config
import logging

def initialize_database():
    """Initialize database with sample data"""
    try:
        user_model = User(Config.DATABASE_PATH)
        
        # Create sample users
        sample_users = [
            ('John Doe', 'john@example.com', 'password123'),
            ('Jane Smith', 'jane@example.com', 'secret456'),
            ('Bob Johnson', 'bob@example.com', 'qwerty789')
        ]
        
        for name, email, password in sample_users:
            user_id = user_model.create_user(name, email, password)
            if user_id:
                print(f"Created user: {name} (ID: {user_id})")
            else:
                print(f"User {email} already exists, skipping...")
        
        print("Database initialized successfully!")
        
    except Exception as e:
        logging.error(f"Error initializing database: {str(e)}")
        print(f"Error initializing database: {str(e)}")

if __name__ == '__main__':
    initialize_database()