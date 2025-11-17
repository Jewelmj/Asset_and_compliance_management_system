"""
Simple manual test script for project management endpoints.
Run this after starting the Flask API server.
"""
import requests
import json
from datetime import datetime, timedelta

API_BASE_URL = "http://localhost:5000/api"


def get_auth_token():
    """Get authentication token for testing."""
    response = requests.post(
        f"{API_BASE_URL}/login",
        json={
            "username": "admin",
            "password": "admin123"
        }
    )
    
    if response.status_code == 200:
        return response.json()['token']
    else:
        print("✗ Failed to get authentication token")
        return None


def test_create_project(token):
    """Test creating a new project."""
    print("\n=== Test: Create new project ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        f"{API_BASE_URL}/projects/",
        json={
            "name": "Test Construction Site",
            "location": "123 Main St"
        },
        headers=headers
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        data = response.json()
        if 'id' in data and 'name' in data and 'location' in data:
            print("✓ Project created successfully")
            return data['id']
        else:
            print("✗ Response missing required fields")
    else:
        print("✗ Project creation failed")
    
    return None


def test_list_projects(token):
    """Test listing all projects."""
    print("\n=== Test: List all projects ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"{API_BASE_URL}/projects/",
        headers=headers
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list):
            print(f"✓ Projects listed successfully ({len(data)} projects)")
        else:
            print("✗ Response should be a list")
    else:
        print("✗ Failed to list projects")


def test_get_project_compliance(token, project_id):
    """Test getting project compliance status."""
    print(f"\n=== Test: Get compliance status for project {project_id} ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"{API_BASE_URL}/projects/{project_id}/compliance",
        headers=headers
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        data = response.json()
        if 'project_id' in data and 'subcontractors' in data:
            print("✓ Compliance status retrieved successfully")
        else:
            print("✗ Response missing required fields")
    else:
        print("✗ Failed to get compliance status")


def test_create_project_missing_name(token):
    """Test creating project with missing name."""
    print("\n=== Test: Create project with missing name ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        f"{API_BASE_URL}/projects/",
        json={
            "location": "123 Main St"
            # Missing name
        },
        headers=headers
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 400:
        print("✓ Correctly rejected missing name")
    else:
        print("✗ Should have returned 400 Bad Request")


def test_get_nonexistent_project_compliance(token):
    """Test getting compliance for non-existent project."""
    print("\n=== Test: Get compliance for non-existent project ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"{API_BASE_URL}/projects/nonexistent-id/compliance",
        headers=headers
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 404:
        print("✓ Correctly returned 404 for non-existent project")
    else:
        print("✗ Should have returned 404 Not Found")


def test_unauthorized_access():
    """Test accessing endpoints without authentication."""
    print("\n=== Test: Access without authentication ===")
    
    response = requests.get(f"{API_BASE_URL}/projects/")
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 401:
        print("✓ Correctly rejected unauthorized access")
    else:
        print("✗ Should have returned 401 Unauthorized")


if __name__ == "__main__":
    print("=" * 60)
    print("Project Management API Test Suite")
    print("=" * 60)
    print("\nMake sure the Flask API is running on http://localhost:5000")
    print("and the database has been initialized with seed data.")
    
    try:
        # Get authentication token
        print("\n=== Getting authentication token ===")
        token = get_auth_token()
        
        if not token:
            print("\n✗ Cannot proceed without authentication token")
            exit(1)
        
        print(f"✓ Token obtained: {token[:50]}...")
        
        # Test unauthorized access
        test_unauthorized_access()
        
        # Test create project with missing name
        test_create_project_missing_name(token)
        
        # Test create project
        project_id = test_create_project(token)
        
        # Test list projects
        test_list_projects(token)
        
        # Test get project compliance
        if project_id:
            test_get_project_compliance(token, project_id)
        
        # Test get non-existent project compliance
        test_get_nonexistent_project_compliance(token)
        
        print("\n" + "=" * 60)
        print("Test suite completed")
        print("=" * 60)
        print("\nNote: To test compliance status calculation with actual data:")
        print("1. Create subcontractors via the API")
        print("2. Associate them with the project")
        print("3. Upload compliance documents with various expiry dates")
        print("4. Run the compliance endpoint again to see RED/GREEN status")
        
    except requests.exceptions.ConnectionError:
        print("\n✗ Error: Could not connect to API server")
        print("Make sure the Flask API is running on http://localhost:5000")
    except Exception as e:
        print(f"\n✗ Error: {e}")
