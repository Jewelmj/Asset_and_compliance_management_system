"""
Unit tests for the ComplianceService.
Tests the RED/GREEN status calculation logic.
"""
from datetime import datetime, timedelta
from services.compliance_service import ComplianceService


def test_calculate_status_expired():
    """Test that expired documents return RED status."""
    print("\n=== Test: Expired document ===")
    
    # Document expired yesterday
    expiry_date = (datetime.now() - timedelta(days=1)).date()
    status = ComplianceService.calculate_status(expiry_date)
    
    print(f"Expiry Date: {expiry_date}")
    print(f"Status: {status}")
    
    if status == "RED":
        print("✓ Correctly marked as RED")
    else:
        print("✗ Should be RED")


def test_calculate_status_expiring_soon():
    """Test that documents expiring within 30 days return RED status."""
    print("\n=== Test: Document expiring in 15 days ===")
    
    # Document expiring in 15 days
    expiry_date = (datetime.now() + timedelta(days=15)).date()
    status = ComplianceService.calculate_status(expiry_date)
    
    print(f"Expiry Date: {expiry_date}")
    print(f"Status: {status}")
    
    if status == "RED":
        print("✓ Correctly marked as RED")
    else:
        print("✗ Should be RED")


def test_calculate_status_expiring_exactly_30_days():
    """Test that documents expiring exactly in 30 days return RED status."""
    print("\n=== Test: Document expiring in exactly 30 days ===")
    
    # Document expiring in exactly 30 days
    expiry_date = (datetime.now() + timedelta(days=30)).date()
    status = ComplianceService.calculate_status(expiry_date)
    
    print(f"Expiry Date: {expiry_date}")
    print(f"Status: {status}")
    
    if status == "RED":
        print("✓ Correctly marked as RED")
    else:
        print("✗ Should be RED")


def test_calculate_status_valid():
    """Test that documents valid for more than 30 days return GREEN status."""
    print("\n=== Test: Document expiring in 60 days ===")
    
    # Document expiring in 60 days
    expiry_date = (datetime.now() + timedelta(days=60)).date()
    status = ComplianceService.calculate_status(expiry_date)
    
    print(f"Expiry Date: {expiry_date}")
    print(f"Status: {status}")
    
    if status == "GREEN":
        print("✓ Correctly marked as GREEN")
    else:
        print("✗ Should be GREEN")


def test_calculate_status_null():
    """Test that null expiry date returns RED status."""
    print("\n=== Test: Null expiry date ===")
    
    status = ComplianceService.calculate_status(None)
    
    print(f"Expiry Date: None")
    print(f"Status: {status}")
    
    if status == "RED":
        print("✓ Correctly marked as RED")
    else:
        print("✗ Should be RED")


def test_calculate_subcontractor_status_all_green():
    """Test subcontractor status when all documents are GREEN."""
    print("\n=== Test: Subcontractor with all GREEN documents ===")
    
    # Mock documents with valid expiry dates
    class MockDoc:
        def __init__(self, expiry_date):
            self.expiry_date = expiry_date
    
    documents = [
        MockDoc((datetime.now() + timedelta(days=60)).date()),
        MockDoc((datetime.now() + timedelta(days=90)).date()),
    ]
    
    status = ComplianceService.calculate_subcontractor_status(documents)
    
    print(f"Status: {status}")
    
    if status == "GREEN":
        print("✓ Correctly marked as GREEN")
    else:
        print("✗ Should be GREEN")


def test_calculate_subcontractor_status_one_red():
    """Test subcontractor status when one document is RED."""
    print("\n=== Test: Subcontractor with one RED document ===")
    
    # Mock documents with mixed expiry dates
    class MockDoc:
        def __init__(self, expiry_date):
            self.expiry_date = expiry_date
    
    documents = [
        MockDoc((datetime.now() + timedelta(days=60)).date()),  # GREEN
        MockDoc((datetime.now() + timedelta(days=10)).date()),  # RED
    ]
    
    status = ComplianceService.calculate_subcontractor_status(documents)
    
    print(f"Status: {status}")
    
    if status == "RED":
        print("✓ Correctly marked as RED")
    else:
        print("✗ Should be RED")


def test_calculate_subcontractor_status_no_documents():
    """Test subcontractor status when no documents exist."""
    print("\n=== Test: Subcontractor with no documents ===")
    
    status = ComplianceService.calculate_subcontractor_status([])
    
    print(f"Status: {status}")
    
    if status == "RED":
        print("✓ Correctly marked as RED")
    else:
        print("✗ Should be RED")


if __name__ == "__main__":
    print("=" * 60)
    print("Compliance Service Unit Tests")
    print("=" * 60)
    
    test_calculate_status_expired()
    test_calculate_status_expiring_soon()
    test_calculate_status_expiring_exactly_30_days()
    test_calculate_status_valid()
    test_calculate_status_null()
    test_calculate_subcontractor_status_all_green()
    test_calculate_subcontractor_status_one_red()
    test_calculate_subcontractor_status_no_documents()
    
    print("\n" + "=" * 60)
    print("Test suite completed")
    print("=" * 60)
