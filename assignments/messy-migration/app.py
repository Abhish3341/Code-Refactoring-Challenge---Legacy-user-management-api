from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import Config
from models.user import User
from routes.user_routes import create_user_routes
import logging

def create_app():
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Configure logging
    if app.config.get('FLASK_ENV') != 'development':
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(levelname)s: %(message)s'
        )
    
    # Initialize rate limiter
    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=[app.config.get('RATELIMIT_DEFAULT', '100 per hour')]
    )
    limiter.init_app(app)
    
    # Initialize models
    user_model = User(app.config.get('DATABASE_PATH', 'users.db'))
    
    # Register blueprints
    user_routes = create_user_routes(user_model, limiter)
    app.register_blueprint(user_routes)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=(app.config.get('FLASK_ENV') == 'development'))