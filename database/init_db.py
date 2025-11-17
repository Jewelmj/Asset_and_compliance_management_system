"""
Database initialization script for Site-Steward.
Creates all tables and optionally seeds initial data.

Usage:
    python database/init_db.py           # Create tables only
    python database/init_db.py --seed    # Create tables and seed data

Docker Usage:
    docker-compose exec api python database/init_db.py --seed
"""
from database.db import init_db as create_tables, engine
from database.models import (
    UserORM, ProjectORM, AssetORM, SubcontractorORM,
    ComplianceDocumentORM, AssetHistoryORM, PlaceORM
)
import sys
import uuid
from datetime import datetime, timedelta
import bcrypt


def init_db():
    """Initialize database by creating all tables."""
    print("Initializing database...")
    print(f"Database URL: {engine.url}")
    
    try:
        create_tables()
        print("✓ Database tables created successfully.")
    except Exception as e:
        print(f"✗ Error creating database tables: {e}")
        sys.exit(1)


def seed_data():
    """Seed initial data for development/testing."""
    from database.db import SessionLocal
    
    print("Seeding initial data...")
    db = SessionLocal()
    
    try:
        # Create admin user with default credentials
        admin_password = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        admin_user = UserORM(
            id=str(uuid.uuid4()),
            username="admin",
            password_hash=admin_password,
            role="admin",
            email="admin@sitesteward.com"
        )
        db.add(admin_user)
        
        # Create foreman user
        foreman_password = bcrypt.hashpw("foreman123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        foreman_user = UserORM(
            id=str(uuid.uuid4()),
            username="foreman",
            password_hash=foreman_password,
            role="foreman",
            email="foreman@sitesteward.com"
        )
        db.add(foreman_user)
        
        # Create sample projects
        project1 = ProjectORM(
            id=str(uuid.uuid4()),
            name="Downtown Office Building",
            location="123 Main St, City"
        )
        project2 = ProjectORM(
            id=str(uuid.uuid4()),
            name="Residential Complex Phase 2",
            location="456 Oak Ave, Town"
        )
        db.add(project1)
        db.add(project2)
        
        # Create sample assets
        asset1 = AssetORM(
            id=str(uuid.uuid4()),
            name="Excavator CAT 320",
            category="Heavy Equipment",
            project_id=project1.id
        )
        asset2 = AssetORM(
            id=str(uuid.uuid4()),
            name="Generator 50kW",
            category="Power Equipment",
            project_id=project1.id
        )
        asset3 = AssetORM(
            id=str(uuid.uuid4()),
            name="Scaffolding Set A",
            category="Safety Equipment"
        )
        db.add(asset1)
        db.add(asset2)
        db.add(asset3)
        
        # Create sample subcontractors
        subcontractor1 = SubcontractorORM(
            id=str(uuid.uuid4()),
            name="ABC Electrical Services",
            email="contact@abcelectrical.com",
            phone="555-0101"
        )
        subcontractor2 = SubcontractorORM(
            id=str(uuid.uuid4()),
            name="XYZ Plumbing Co",
            email="info@xyzplumbing.com",
            phone="555-0202"
        )
        db.add(subcontractor1)
        db.add(subcontractor2)
        
        # Associate subcontractors with projects
        project1.subcontractors.append(subcontractor1)
        project1.subcontractors.append(subcontractor2)
        project2.subcontractors.append(subcontractor2)
        
        # Create sample compliance documents
        doc1 = ComplianceDocumentORM(
            id=str(uuid.uuid4()),
            subcontractor_id=subcontractor1.id,
            document_type="Liability Insurance",
            file_path="uploads/compliance/sample_insurance.pdf",
            expiry_date=(datetime.now() + timedelta(days=45)).date()
        )
        doc2 = ComplianceDocumentORM(
            id=str(uuid.uuid4()),
            subcontractor_id=subcontractor1.id,
            document_type="Safety Certification",
            expiry_date=(datetime.now() + timedelta(days=15)).date(),
            file_path="uploads/compliance/sample_safety_cert.pdf"
        )
        doc3 = ComplianceDocumentORM(
            id=str(uuid.uuid4()),
            subcontractor_id=subcontractor2.id,
            document_type="Liability Insurance",
            file_path="uploads/compliance/sample_insurance2.pdf",
            expiry_date=(datetime.now() + timedelta(days=90)).date()
        )
        db.add(doc1)
        db.add(doc2)
        db.add(doc3)
        
        # Create sample asset history
        history1 = AssetHistoryORM(
            id=str(uuid.uuid4()),
            asset_id=asset1.id,
            project_id=project1.id,
            moved_by=admin_user.id
        )
        db.add(history1)
        
        db.commit()
        print("✓ Initial data seeded successfully.")
        print("\nDefault credentials:")
        print("  Admin - username: admin, password: admin123")
        print("  Foreman - username: foreman, password: foreman123")
    except Exception as e:
        db.rollback()
        print(f"✗ Error seeding data: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
    
    # Optionally seed data
    if len(sys.argv) > 1 and sys.argv[1] == '--seed':
        seed_data()