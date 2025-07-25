import pytest
from utils.validation import validate_email, validate_password, validate_name, validate_user_data, validate_user_id

def test_validate_email():
    """Test email validation"""
    assert validate_email("test@example.com") is True
    assert validate_email("user.name+tag@domain.co.uk") is True
    assert validate_email("invalid-email") is False
    assert validate_email("@domain.com") is False
    assert validate_email("user@") is False

def test_validate_password():
    """Test password validation"""
    assert validate_password("password123") is True
    assert validate_password("123456") is True
    assert validate_password("12345") is False  # Too short
    assert validate_password("") is False

def test_validate_name():
    """Test name validation"""
    assert validate_name("John Doe") is True
    assert validate_name("A") is True
    assert validate_name("") is False
    assert validate_name("   ") is False
    assert validate_name("A" * 101) is False  # Too long

def test_validate_user_data():
    """Test user data validation"""
    # Valid data
    valid_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "password": "password123"
    }
    errors = validate_user_data(valid_data)
    assert len(errors) == 0
    
    # Invalid data
    invalid_data = {
        "name": "",
        "email": "invalid-email",
        "password": "123"
    }
    errors = validate_user_data(invalid_data)
    assert "name" in errors
    assert "email" in errors
    assert "password" in errors

def test_validate_user_id():
    """Test user ID validation"""
    assert validate_user_id("123") == 123
    assert validate_user_id("1") == 1
    assert validate_user_id("0") is None  # Zero not allowed
    assert validate_user_id("-1") is None  # Negative not allowed
    assert validate_user_id("abc") is None  # Non-numeric
    assert validate_user_id("") is None