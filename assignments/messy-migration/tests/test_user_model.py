import pytest
import tempfile
import os
from models.user import User

@pytest.fixture
def temp_db():
    """Create a temporary database for testing"""
    fd, path = tempfile.mkstemp()
    os.close(fd)
    yield path
    os.unlink(path)

@pytest.fixture
def user_model(temp_db):
    """Create a User model instance with temporary database"""
    return User(temp_db)

def test_create_user(user_model):
    """Test user creation"""
    user_id = user_model.create_user("Test User", "test@example.com", "password123")
    assert user_id is not None
    assert isinstance(user_id, int)

def test_create_duplicate_email(user_model):
    """Test creating user with duplicate email"""
    user_model.create_user("User 1", "test@example.com", "password123")
    duplicate_id = user_model.create_user("User 2", "test@example.com", "password456")
    assert duplicate_id is None

def test_get_user_by_id(user_model):
    """Test retrieving user by ID"""
    user_id = user_model.create_user("Test User", "test@example.com", "password123")
    user = user_model.get_user_by_id(user_id)
    
    assert user is not None
    assert user['name'] == "Test User"
    assert user['email'] == "test@example.com"
    assert 'password_hash' not in user  # Should not expose password hash

def test_authenticate_user(user_model):
    """Test user authentication"""
    user_model.create_user("Test User", "test@example.com", "password123")
    
    # Valid credentials
    user = user_model.authenticate_user("test@example.com", "password123")
    assert user is not None
    assert user['email'] == "test@example.com"
    
    # Invalid password
    user = user_model.authenticate_user("test@example.com", "wrongpassword")
    assert user is None
    
    # Invalid email
    user = user_model.authenticate_user("wrong@example.com", "password123")
    assert user is None

def test_update_user(user_model):
    """Test user update"""
    user_id = user_model.create_user("Test User", "test@example.com", "password123")
    
    # Update name
    success = user_model.update_user(user_id, name="Updated Name")
    assert success is True
    
    user = user_model.get_user_by_id(user_id)
    assert user['name'] == "Updated Name"

def test_delete_user(user_model):
    """Test user deletion"""
    user_id = user_model.create_user("Test User", "test@example.com", "password123")
    
    success = user_model.delete_user(user_id)
    assert success is True
    
    user = user_model.get_user_by_id(user_id)
    assert user is None

def test_search_users(user_model):
    """Test user search"""
    user_model.create_user("John Doe", "john@example.com", "password123")
    user_model.create_user("Jane Smith", "jane@example.com", "password456")
    
    results = user_model.search_users_by_name("John")
    assert len(results) == 1
    assert results[0]['name'] == "John Doe"
    
    results = user_model.search_users_by_name("Smith")
    assert len(results) == 1
    assert results[0]['name'] == "Jane Smith"