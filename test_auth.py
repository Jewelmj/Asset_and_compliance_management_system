"""
Simple manual test script for authentication endpoints.
Run this after starting the Flask API server.
"""
import requests
import json

API_BASE_URL = "http://localhost:5000/api"


def test_login_success():
    """Test successful login with valid credentials."""
    print("\n=== Test: Login with valid credentials ===")
    
    response = requests.post(
        f"{API_BASE_URL}/login",
        json={
            "username": "admin",
            "password": "admin123"
        }
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        data = response.json()
        if 'token' in data and 'user_id' in data and 'role' in data:
            print("✓ Login successful - JWT token received")
            return data['token']
        else:
            print("✗ Login response missing required fields")
    else:
        print("✗ Login failed")
    
    return None


def test_login_invalid_credentials():
    """Test login with invalid credentials."""
    print("\n=== Test: Login with invalid credentials ===")
    
    response = requests.post(
        f"{API_BASE_URL}/login",
        json={
            "username": "admin",
            "password": "wrongpassword"
        }
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 401:
        print("✓ Correctly rejected invalid credentials")
    else:
        print("✗ Should have returned 401 Unauthorized")


def test_login_missing_fields():
    """Test login with missing fields."""
    print("\n=== Test: Login with missing fields ===")
    
    response = requests.post(
        f"{API_BASE_URL}/login",
        json={
            "username": "admin"
        }
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 400:
        print("✓ Correctly rejected missing password")
    else:
        print("✗ Should have returned 400 Bad Request")


def test_protected_route_with_token(token):
    """Test accessing a protected route with valid token."""
    print("\n=== Test: Access protected route with valid token ===")
    print("Note: This test requires a protected endpoint to be implemented")
    print(f"Token: {token[:50]}...")


def test_protected_route_without_token():
    """Test accessing a protected route without token."""
    print("\n=== Test: Access protected route without token ===")
    print("Note: This test requires a protected endpoint to be implemented")


if __name__ == "__main__":
    print("=" * 60)
    print("Authentication System Test Suite")
    print("=" * 60)
    print("\nMake sure the Flask API is running on http://localhost:5000")
    print("and the database has been initialized with seed data.")
    
    try:
        # Test successful login
        token = test_login_success()
        
        # Test invalid credentials
        test_login_invalid_credentials()
        
        # Test missing fields
        test_login_missing_fields()
        
        # Test protected routes (if token was obtained)
        if token:
            test_protected_route_with_token(token)
            test_protected_route_without_token()
        
        print("\n" + "=" * 60)
        print("Test suite completed")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\n✗ Error: Could not connect to API server")
        print("Make sure the Flask API is running on http://localhost:5000")
    except Exception as e:
        print(f"\n✗ Error: {e}")
