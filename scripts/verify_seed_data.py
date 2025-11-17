"""
Verification script to check if seed data was loaded correctly.
Run this after initializing the database with seed data.

Usage:
    python scripts/verify_seed_data.py
    
Docker Usage:
    docker-compose exec api python scripts/verify_seed_data.py
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.db import SessionLocal
from database.models import (
    UserORM, ProjectORM, AssetORM, SubcontractorORM,
    ComplianceDocumentORM, AssetHistoryORM
)


def verify_seed_data():
    """Verify that seed data was loaded correctly."""
    db = SessionLocal()
    
    try:
        print("Verifying seed data...\n")
        
        # Check users
        users = db.query(UserORM).all()
        print(f"✓ Users: {len(users)} found")
        for user in users:
            print(f"  - {user.username} ({user.role})")
        
        # Check projects
        projects = db.query(ProjectORM).all()
        print(f"\n✓ Projects: {len(projects)} found")
        for project in projects:
            print(f"  - {project.name} ({project.location})")
        
        # Check assets
        assets = db.query(AssetORM).all()
        print(f"\n✓ Assets: {len(assets)} found")
        for asset in assets:
            location = asset.project.name if asset.project else "Unassigned"
            print(f"  - {asset.name} ({asset.category}) - {location}")
        
        # Check subcontractors
        subcontractors = db.query(SubcontractorORM).all()
        print(f"\n✓ Subcontractors: {len(subcontractors)} found")
        for sub in subcontractors:
            print(f"  - {sub.name} ({sub.email})")
        
        # Check compliance documents
        documents = db.query(ComplianceDocumentORM).all()
        print(f"\n✓ Compliance Documents: {len(documents)} found")
        for doc in documents:
            print(f"  - {doc.document_type} for {doc.subcontractor.name} (expires: {doc.expiry_date})")
        
        # Check asset history
        history = db.query(AssetHistoryORM).all()
        print(f"\n✓ Asset History: {len(history)} records found")
        
        # Verify expected counts
        print("\n" + "="*50)
        print("Verification Summary:")
        print("="*50)
        
        expected = {
            "Users": (users, 2),
            "Projects": (projects, 2),
            "Assets": (assets, 3),
            "Subcontractors": (subcontractors, 2),
            "Compliance Documents": (documents, 3),
            "Asset History": (history, 1)
        }
        
        all_good = True
        for name, (items, expected_count) in expected.items():
            actual_count = len(items)
            status = "✓" if actual_count >= expected_count else "✗"
            print(f"{status} {name}: {actual_count} (expected: {expected_count})")
            if actual_count < expected_count:
                all_good = False
        
        print("\n" + "="*50)
        if all_good:
            print("✓ All seed data verified successfully!")
            print("\nDefault credentials:")
            print("  Admin - username: admin, password: admin123")
            print("  Foreman - username: foreman, password: foreman123")
        else:
            print("✗ Some seed data is missing. Please run: make seed-db")
            sys.exit(1)
            
    except Exception as e:
        print(f"✗ Error verifying seed data: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    verify_seed_data()
