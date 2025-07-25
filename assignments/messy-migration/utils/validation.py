import re
from typing import Dict, List, Optional

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_password(password: str) -> bool:
    """Validate password strength (minimum 6 characters)"""
    return len(password) >= 6

def validate_name(name: str) -> bool:
    """Validate name (non-empty, reasonable length)"""
    return 1 <= len(name.strip()) <= 100

def validate_user_data(data: Dict) -> Dict[str, List[str]]:
    """Validate user creation/update data"""
    errors = {}
    
    if 'name' in data:
        if not data['name'] or not validate_name(data['name']):
            errors['name'] = ['Name must be between 1 and 100 characters']
    
    if 'email' in data:
        if not data['email'] or not validate_email(data['email']):
            errors['email'] = ['Invalid email format']
    
    if 'password' in data:
        if not data['password'] or not validate_password(data['password']):
            errors['password'] = ['Password must be at least 6 characters long']
    
    return errors

def validate_user_id(user_id: str) -> Optional[int]:
    """Validate and convert user ID to integer"""
    try:
        uid = int(user_id)
        return uid if uid > 0 else None
    except (ValueError, TypeError):
        return None