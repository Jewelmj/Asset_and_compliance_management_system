"""
Simple manual test script for asset management endpoints.
Run this after starting the Flask API server.
"""
import requests
import json

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


def test_create_asset(token):
    """Test creating a new asset."""
    print("\n=== Test: Create new asset ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        f"{API_BASE_URL}/assets/",
        json={
            "name": "Test Drill",
            "category": "Power Tools"
        },
        headers=headers
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        data = response.json()
        if 'id' in data and 'name' in data and 'category' in data:
            print("✓ Asset created successfully")
            return data['id']
        else:
            print("✗ Response missing required fields")
    else:
        print("✗ Asset creation failed")
    
    return None


def test_list_assets(token):
    """Test listing all assets."""
    print("\n=== Test: List all assets ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"{API_BASE_URL}/assets/",
        headers=headers
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print("✓ Assets listed successfully")
    else:
        print("✗ Failed to list assets")


def test_get_asset_details(token, asset_id):
    """Test getting asset details."""
    print(f"\n=== Test: Get asset details for {asset_id} ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"{API_BASE_URL}/assets/{asset_id}",
        headers=headers
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        data = response.json()
        if 'id' in data and 'history' in data:
            print("✓ Asset details retrieved successfully")
        else:
            print("✗ Response missing required fields")
    else:
        print("✗ Failed to get asset details")


def test_move_asset(token, asset_id, project_id):
    """Test moving an asset to a project."""
    print(f"\n=== Test: Move asset {asset_id} to project {project_id} ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        f"{API_BASE_URL}/assets/{asset_id}/move",
        json={
            "project_id": project_id
        },
        headers=headers
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print("✓ Asset moved successfully")
        else:
            print("✗ Move operation did not return success")
    else:
        print("✗ Failed to move asset")


def test_create_asset_missing_fields(token):
    """Test creating asset with missing fields."""
    print("\n=== Test: Create asset with missing fields ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        f"{API_BASE_URL}/assets/",
        json={
            "name": "Test Asset"
            # Missing category
        },
        headers=headers
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 400:
        print("✓ Correctly rejected missing fields")
    else:
        print("✗ Should have returned 400 Bad Request")


def test_get_nonexistent_asset(token):
    """Test getting details of non-existent asset."""
    print("\n=== Test: Get non-existent asset ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"{API_BASE_URL}/assets/nonexistent-id",
        headers=headers
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 404:
        print("✓ Correctly returned 404 for non-existent asset")
    else:
        print("✗ Should have returned 404 Not Found")


def test_unauthorized_access():
    """Test accessing endpoints without authentication."""
    print("\n=== Test: Access without authentication ===")
    
    response = requests.get(f"{API_BASE_URL}/assets/")
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 401:
        print("✓ Correctly rejected unauthorized access")
    else:
        print("✗ Should have returned 401 Unauthorized")


if __name__ == "__main__":
    print("=" * 60)
    print("Asset Management API Test Suite")
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
        
        # Test create asset with missing fields
        test_create_asset_missing_fields(token)
        
        # Test create asset
        asset_id = test_create_asset(token)
        
        # Test list assets
        test_list_assets(token)
        
        # Test get asset details
        if asset_id:
            test_get_asset_details(token, asset_id)
        
        # Test get non-existent asset
        test_get_nonexistent_asset(token)
        
        # Test move asset (requires a project to exist)
        print("\n=== Note: Move asset test requires a project ===")
        print("Create a project first, then uncomment and update the test below")
        # if asset_id:
        #     test_move_asset(token, asset_id, "your-project-id-here")
        
        print("\n" + "=" * 60)
        print("Test suite completed")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\n✗ Error: Could not connect to API server")
        print("Make sure the Flask API is running on http://localhost:5000")
    except Exception as e:
        print(f"\n✗ Error: {e}")
