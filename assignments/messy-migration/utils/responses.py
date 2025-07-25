from flask import jsonify
from typing import Any, Dict, List

def success_response(data: Any = None, message: str = None, status_code: int = 200):
    """Create a successful JSON response"""
    response_data = {'success': True}
    
    if message:
        response_data['message'] = message
    if data is not None:
        response_data['data'] = data
    
    return jsonify(response_data), status_code

def error_response(message: str, errors: Dict = None, status_code: int = 400):
    """Create an error JSON response"""
    response_data = {
        'success': False,
        'message': message
    }
    
    if errors:
        response_data['errors'] = errors
    
    return jsonify(response_data), status_code

def validation_error_response(errors: Dict[str, List[str]]):
    """Create a validation error response"""
    return error_response(
        message="Validation failed",
        errors=errors,
        status_code=422
    )