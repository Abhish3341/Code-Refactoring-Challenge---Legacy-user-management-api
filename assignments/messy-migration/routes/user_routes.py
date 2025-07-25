from flask import Blueprint, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from models.user import User
from utils.validation import validate_user_data, validate_user_id
from utils.responses import success_response, error_response, validation_error_response
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_user_routes(user_model: User, limiter: Limiter) -> Blueprint:
    """Create user routes blueprint"""
    bp = Blueprint('users', __name__)
    
    @bp.route('/', methods=['GET'])
    def home():
        """Health check endpoint"""
        return success_response(message="User Management System")
    
    @bp.route('/users', methods=['GET'])
    @limiter.limit("50 per minute")
    def get_all_users():
        """Get all users"""
        try:
            users = user_model.get_all_users()
            return success_response(data=users)
        except Exception as e:
            logger.error(f"Error fetching users: {str(e)}")
            return error_response("Internal server error", status_code=500)
    
    @bp.route('/user/<user_id>', methods=['GET'])
    @limiter.limit("100 per minute")
    def get_user(user_id):
        """Get specific user by ID"""
        try:
            uid = validate_user_id(user_id)
            if uid is None:
                return error_response("Invalid user ID", status_code=400)
            
            user = user_model.get_user_by_id(uid)
            if user:
                return success_response(data=user)
            else:
                return error_response("User not found", status_code=404)
        except Exception as e:
            logger.error(f"Error fetching user {user_id}: {str(e)}")
            return error_response("Internal server error", status_code=500)
    
    @bp.route('/users', methods=['POST'])
    @limiter.limit("10 per minute")
    def create_user():
        """Create a new user"""
        try:
            data = request.get_json()
            if not data:
                return error_response("No JSON data provided", status_code=400)
            
            # Validate required fields
            required_fields = ['name', 'email', 'password']
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return error_response(
                    f"Missing required fields: {', '.join(missing_fields)}",
                    status_code=400
                )
            
            # Validate data
            validation_errors = validate_user_data(data)
            if validation_errors:
                return validation_error_response(validation_errors)
            
            # Create user
            user_id = user_model.create_user(
                name=data['name'].strip(),
                email=data['email'].strip().lower(),
                password=data['password']
            )
            
            if user_id:
                logger.info(f"User created successfully with ID: {user_id}")
                return success_response(
                    data={'id': user_id},
                    message="User created successfully",
                    status_code=201
                )
            else:
                return error_response("Email already exists", status_code=409)
                
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            return error_response("Internal server error", status_code=500)
    
    @bp.route('/user/<user_id>', methods=['PUT'])
    @limiter.limit("20 per minute")
    def update_user(user_id):
        """Update user information"""
        try:
            uid = validate_user_id(user_id)
            if uid is None:
                return error_response("Invalid user ID", status_code=400)
            
            data = request.get_json()
            if not data:
                return error_response("No JSON data provided", status_code=400)
            
            # Validate data
            validation_errors = validate_user_data(data)
            if validation_errors:
                return validation_error_response(validation_errors)
            
            # Update user
            name = data.get('name', '').strip() if data.get('name') else None
            email = data.get('email', '').strip().lower() if data.get('email') else None
            
            success = user_model.update_user(uid, name=name, email=email)
            
            if success:
                logger.info(f"User {uid} updated successfully")
                return success_response(message="User updated successfully")
            else:
                return error_response("User not found or email already exists", status_code=404)
                
        except Exception as e:
            logger.error(f"Error updating user {user_id}: {str(e)}")
            return error_response("Internal server error", status_code=500)
    
    @bp.route('/user/<user_id>', methods=['DELETE'])
    @limiter.limit("10 per minute")
    def delete_user(user_id):
        """Delete user by ID"""
        try:
            uid = validate_user_id(user_id)
            if uid is None:
                return error_response("Invalid user ID", status_code=400)
            
            success = user_model.delete_user(uid)
            
            if success:
                logger.info(f"User {uid} deleted successfully")
                return success_response(message="User deleted successfully")
            else:
                return error_response("User not found", status_code=404)
                
        except Exception as e:
            logger.error(f"Error deleting user {user_id}: {str(e)}")
            return error_response("Internal server error", status_code=500)
    
    @bp.route('/search', methods=['GET'])
    @limiter.limit("30 per minute")
    def search_users():
        """Search users by name"""
        try:
            name = request.args.get('name', '').strip()
            
            if not name:
                return error_response("Please provide a name to search", status_code=400)
            
            if len(name) < 2:
                return error_response("Search term must be at least 2 characters", status_code=400)
            
            users = user_model.search_users_by_name(name)
            return success_response(data=users)
            
        except Exception as e:
            logger.error(f"Error searching users: {str(e)}")
            return error_response("Internal server error", status_code=500)
    
    @bp.route('/login', methods=['POST'])
    @limiter.limit("5 per minute")
    def login():
        """User login endpoint"""
        try:
            data = request.get_json()
            if not data:
                return error_response("No JSON data provided", status_code=400)
            
            email = data.get('email', '').strip().lower()
            password = data.get('password', '')
            
            if not email or not password:
                return error_response("Email and password are required", status_code=400)
            
            user = user_model.authenticate_user(email, password)
            
            if user:
                logger.info(f"User {user['id']} logged in successfully")
                return success_response(
                    data={'user_id': user['id'], 'name': user['name']},
                    message="Login successful"
                )
            else:
                logger.warning(f"Failed login attempt for email: {email}")
                return error_response("Invalid email or password", status_code=401)
                
        except Exception as e:
            logger.error(f"Error during login: {str(e)}")
            return error_response("Internal server error", status_code=500)
    
    return bp