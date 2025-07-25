import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-me'
    DATABASE_PATH = os.environ.get('DATABASE_PATH') or 'users.db'
    FLASK_ENV = os.environ.get('FLASK_ENV') or 'development'
    
    # Rate limiting
    RATELIMIT_STORAGE_URL = "memory://"
    RATELIMIT_DEFAULT = "100 per hour"