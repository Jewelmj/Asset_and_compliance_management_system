"""
Simple manual test script for subcontractor management endpoints.
Run this after starting the Flask API server.
"""
import requests
import json
import os

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


def test_create_subcontractor(token):
    """Test creating a new subcontractor."""
    print("\n=== Test: Create new subcontractor ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        f"{API_BASE_URL}/subcontractors/",
        json={
            "name": "Test Electrical Co.",
            "email": "contact@testelectrical.com",
            "phone": "555-1234"
        },
        headers=headers
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        data = response.json()
        if 'id' in data and 'name' in data:
            print("✓ Subcontractor created successfully")
            return data['id']
        else:
            print("✗ Response missing required fields")
    else:
        print("✗ Subcontractor creation failed")
    
    return None


def test_list_subcontractors(token):
    """Test listing all subcontractors."""
    print("\n=== Test: List all subcontractors ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"{API_BASE_URL}/subcontractors/",
        headers=headers
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print("✓ Subcontractors listed successfully")
    else:
        print("✗ Failed to list subcontractors")


def test_upload_document(token, subcontractor_id):
    """Test uploading a compliance document."""
    print(f"\n=== Test: Upload document for subcontractor {subcontractor_id} ===")
    
    # Create a test PDF file
    test_file_path = "test_document.pdf"
    with open(test_file_path, "wb") as f:
        f.write(b"%PDF-1.4\nTest PDF content")
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        
        with open(test_file_path, "rb") as f:
            files = {"file": ("test_insurance.pdf", f, "application/pdf")}
            data = {
                "expiry_date": "2025-12-31",
                "document_type": "Insurance"
            }
            
            response = requests.post(
                f"{API_BASE_URL}/subcontractors/{subcontractor_id}/document",
                files=files,
                data=data,
                headers=headers
            )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 201:
            data = response.json()
            if 'id' in data and 'file_path' in data and 'status' in data:
                print("✓ Document uploaded successfully")
            else:
                print("✗ Response missing required fields")
        else:
            print("✗ Document upload failed")
    
    finally:
        # Clean up test file
        if os.path.exists(test_file_path):
            os.remove(test_file_path)


def test_upload_invalid_file_type(token, subcontractor_id):
    """Test uploading a non-PDF file."""
    print(f"\n=== Test: Upload invalid file type ===")
    
    # Create a test text file
    test_file_path = "test_document.txt"
    with open(test_file_path, "w") as f:
        f.write("This is not a PDF")
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        
        with open(test_file_path, "rb") as f:
            files = {"file": ("test_document.txt", f, "text/plain")}
            data = {
                "expiry_date": "2025-12-31",
                "document_type": "Insurance"
            }
            
            response = requests.post(
                f"{API_BASE_URL}/subcontractors/{subcontractor_id}/document",
                files=files,
                data=data,
                headers=headers
            )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 400:
            print("✓ Correctly rejected non-PDF file")
        else:
            print("✗ Should have returned 400 Bad Request")
    
    finally:
        # Clean up test file
        if os.path.exists(test_file_path):
            os.remove(test_file_path)


def test_upload_missing_fields(token, subcontractor_id):
    """Test uploading document with missing fields."""
    print(f"\n=== Test: Upload document with missing fields ===")
    
    # Create a test PDF file
    test_file_path = "test_document.pdf"
    with open(test_file_path, "wb") as f:
        f.write(b"%PDF-1.4\nTest PDF content")
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        
        with open(test_file_path, "rb") as f:
            files = {"file": ("test_insurance.pdf", f, "application/pdf")}
            data = {
                "expiry_date": "2025-12-31"
                # Missing document_type
            }
            
            response = requests.post(
                f"{API_BASE_URL}/subcontractors/{subcontractor_id}/document",
                files=files,
                data=data,
                headers=headers
            )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 400:
            print("✓ Correctly rejected missing fields")
        else:
            print("✗ Should have returned 400 Bad Request")
    
    finally:
        # Clean up test file
        if os.path.exists(test_file_path):
            os.remove(test_file_path)


def test_create_subcontractor_missing_name(token):
    """Test creating subcontractor without name."""
    print("\n=== Test: Create subcontractor without name ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        f"{API_BASE_URL}/subcontractors/",
        json={
            "email": "test@example.com",
            "phone": "555-1234"
        },
        headers=headers
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 400:
        print("✓ Correctly rejected missing name")
    else:
        print("✗ Should have returned 400 Bad Request")


def test_upload_to_nonexistent_subcontractor(token):
    """Test uploading document to non-existent subcontractor."""
    print("\n=== Test: Upload to non-existent subcontractor ===")
    
    # Create a test PDF file
    test_file_path = "test_document.pdf"
    with open(test_file_path, "wb") as f:
        f.write(b"%PDF-1.4\nTest PDF content")
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        
        with open(test_file_path, "rb") as f:
            files = {"file": ("test_insurance.pdf", f, "application/pdf")}
            data = {
                "expiry_date": "2025-12-31",
                "document_type": "Insurance"
            }
            
            response = requests.post(
                f"{API_BASE_URL}/subcontractors/nonexistent-id/document",
                files=files,
                data=data,
                headers=headers
            )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 404:
            print("✓ Correctly returned 404 for non-existent subcontractor")
        else:
            print("✗ Should have returned 404 Not Found")
    
    finally:
        # Clean up test file
        if os.path.exists(test_file_path):
            os.remove(test_file_path)


if __name__ == "__main__":
    print("=" * 60)
    print("Subcontractor Management API Test Suite")
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
        
        # Test create subcontractor with missing name
        test_create_subcontractor_missing_name(token)
        
        # Test create subcontractor
        subcontractor_id = test_create_subcontractor(token)
        
        # Test list subcontractors
        test_list_subcontractors(token)
        
        # Test document upload
        if subcontractor_id:
            test_upload_document(token, subcontractor_id)
            test_upload_invalid_file_type(token, subcontractor_id)
            test_upload_missing_fields(token, subcontractor_id)
        
        # Test upload to non-existent subcontractor
        test_upload_to_nonexistent_subcontractor(token)
        
        print("\n" + "=" * 60)
        print("Test suite completed")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\n✗ Error: Could not connect to API server")
        print("Make sure the Flask API is running on http://localhost:5000")
    except Exception as e:
        print(f"\n✗ Error: {e}")
