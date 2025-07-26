import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:5000"

def test_health_check():
    """Test the health check endpoint"""
    print("🔍 Testing Health Check...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_get_all_users():
    """Test getting all users"""
    print("🔍 Testing Get All Users...")
    response = requests.get(f"{BASE_URL}/users")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_create_user():
    """Test creating a new user (Security: Password hashing)"""
    print("🔍 Testing Create User (Security: Password Hashing)...")
    user_data = {
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "securepassword123"
    }
    response = requests.post(f"{BASE_URL}/users", json=user_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json().get('data', {}).get('id') if response.status_code == 201 else None

def test_create_duplicate_user():
    """Test creating duplicate user (Security: Validation)"""
    print("🔍 Testing Duplicate User Creation (Security: Validation)...")
    user_data = {
        "name": "Duplicate User",
        "email": "john@example.com",  # This email already exists
        "password": "password123"
    }
    response = requests.post(f"{BASE_URL}/users", json=user_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_invalid_data():
    """Test input validation (Security: Data validation)"""
    print("🔍 Testing Input Validation (Security)...")
    invalid_data = {
        "name": "",  # Invalid: empty name
        "email": "invalid-email",  # Invalid: bad email format
        "password": "123"  # Invalid: too short
    }
    response = requests.post(f"{BASE_URL}/users", json=invalid_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_get_user_by_id(user_id):
    """Test getting user by ID"""
    if not user_id:
        user_id = 1  # Use existing user
    print(f"🔍 Testing Get User by ID ({user_id})...")
    response = requests.get(f"{BASE_URL}/user/{user_id}")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_update_user(user_id):
    """Test updating user"""
    if not user_id:
        user_id = 1  # Use existing user
    print(f"🔍 Testing Update User ({user_id})...")
    update_data = {
        "name": "Updated Name"
    }
    response = requests.put(f"{BASE_URL}/user/{user_id}", json=update_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_search_users():
    """Test user search functionality"""
    print("🔍 Testing User Search...")
    response = requests.get(f"{BASE_URL}/search?name=John")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_login():
    """Test user login (Security: Password verification)"""
    print("🔍 Testing User Login (Security: Password Verification)...")
    login_data = {
        "email": "john@example.com",
        "password": "password123"
    }
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_invalid_login():
    """Test invalid login (Security: Authentication)"""
    print("🔍 Testing Invalid Login (Security: Authentication)...")
    login_data = {
        "email": "john@example.com",
        "password": "wrongpassword"
    }
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_rate_limiting():
    """Test rate limiting (Security: DoS protection)"""
    print("🔍 Testing Rate Limiting (Security: DoS Protection)...")
    print("Making multiple rapid requests to login endpoint...")
    
    login_data = {
        "email": "test@example.com",
        "password": "wrongpassword"
    }
    
    for i in range(7):  # Try 7 requests (limit is 5 per minute)
        response = requests.post(f"{BASE_URL}/login", json=login_data)
        print(f"Request {i+1}: Status {response.status_code}")
        if response.status_code == 429:
            print("✅ Rate limiting is working!")
            break
    print()

def run_all_tests():
    """Run all API tests"""
    print("=" * 60)
    print("🚀 TESTING REFACTORED USER MANAGEMENT API")
    print("=" * 60)
    print()
    
    try:
        # Basic functionality tests
        test_health_check()
        test_get_all_users()
        
        # Security tests
        new_user_id = test_create_user()
        test_create_duplicate_user()
        test_invalid_data()
        
        # CRUD operations
        test_get_user_by_id(new_user_id)
        test_update_user(new_user_id)
        test_search_users()
        
        # Authentication tests
        test_login()
        test_invalid_login()
        
        # Security: Rate limiting test
        test_rate_limiting()
        
        print("=" * 60)
        print("✅ ALL TESTS COMPLETED!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to the API. Make sure the server is running on http://localhost:5000")
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

if __name__ == "__main__":
    run_all_tests()