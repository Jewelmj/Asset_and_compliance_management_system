# Site-Steward MVP - Database Schema Documentation

## Overview

Site-Steward uses PostgreSQL 15 with SQLAlchemy ORM for data persistence. The schema is designed to support asset tracking, compliance management, and audit trails.

## Entity Relationship Diagram

```
┌─────────────────┐
│     users       │
│─────────────────│
│ id (PK)         │
│ username        │◄──────────┐
│ password_hash   │           │
│ role            │           │
│ email           │           │
│ created_at      │           │
└─────────────────┘           │
                              │
                              │ moved_by (FK)
                              │
┌─────────────────┐           │
│    projects     │           │
│─────────────────│           │
│ id (PK)         │◄──┐       │
│ name            │   │       │
│ location        │   │       │
│ created_at      │   │       │
└─────────────────┘   │       │
        ▲             │       │
        │             │       │
        │             │       │
        │ project_id  │       │
        │ (FK)        │       │
        │             │       │
┌─────────────────┐   │       │
│     assets      │   │       │
│─────────────────│   │       │
│ id (PK)         │   │       │
│ name            │   │       │
│ category        │   │       │
│ project_id (FK) │───┘       │
│ created_at      │           │
│ updated_at      │           │
└─────────────────┘           │
        │                     │
        │ asset_id (FK)       │
        │                     │
        ▼                     │
┌─────────────────┐           │
│ asset_history   │           │
│─────────────────│           │
│ id (PK)         │           │
│ asset_id (FK)   │───────────┘
│ project_id (FK) │───────────┐
│ moved_at        │           │
│ moved_by (FK)   │───────────┤
└─────────────────┘           │
                              │
                              │
┌─────────────────────────────┴───────────────┐
│      project_subcontractors (junction)      │
│─────────────────────────────────────────────│
│ project_id (PK, FK)                         │
│ subcontractor_id (PK, FK)                   │
└─────────────────────────────────────────────┘
                              │
                              │
                              ▼
┌─────────────────┐
│ subcontractors  │
│─────────────────│
│ id (PK)         │
│ name            │
│ email           │
│ phone           │
│ created_at      │
└─────────────────┘
        │
        │ subcontractor_id (FK)
        │
        ▼
┌─────────────────────────┐
│ compliance_documents    │
│─────────────────────────│
│ id (PK)                 │
│ subcontractor_id (FK)   │
│ document_type           │
│ file_path               │
│ expiry_date             │
│ uploaded_at             │
└─────────────────────────┘
```

## Tables

### users

Stores user accounts with authentication credentials.

| Column        | Type      | Constraints           | Description                    |
|---------------|-----------|----------------------|--------------------------------|
| id            | String    | PRIMARY KEY          | UUID                           |
| username      | String    | UNIQUE, NOT NULL     | Login username                 |
| password_hash | String    | NOT NULL             | Bcrypt hashed password         |
| role          | String    | NOT NULL             | User role (admin/foreman)      |
| email         | String    |                      | Email address                  |
| created_at    | DateTime  | DEFAULT now()        | Account creation timestamp     |

**Indexes:**
- PRIMARY KEY on `id`
- UNIQUE INDEX on `username`

**Relationships:**
- One-to-Many with `asset_history` (as moved_by_user)

**Sample Data:**
```sql
INSERT INTO users (id, username, password_hash, role, email) VALUES
('abc-123', 'admin', '$2b$12$...', 'admin', 'admin@sitesteward.com'),
('def-456', 'foreman', '$2b$12$...', 'foreman', 'foreman@sitesteward.com');
```

---

### projects

Stores construction project information.

| Column     | Type     | Constraints    | Description                |
|------------|----------|---------------|----------------------------|
| id         | String   | PRIMARY KEY   | UUID                       |
| name       | String   | NOT NULL      | Project name               |
| location   | String   |               | Project address/location   |
| created_at | DateTime | DEFAULT now() | Project creation timestamp |

**Indexes:**
- PRIMARY KEY on `id`

**Relationships:**
- One-to-Many with `assets`
- One-to-Many with `asset_history`
- Many-to-Many with `subcontractors` (via junction table)

**Sample Data:**
```sql
INSERT INTO projects (id, name, location) VALUES
('proj-001', 'Downtown Office Building', '123 Main St, City'),
('proj-002', 'Residential Complex Phase 2', '456 Oak Ave, Town');
```

---

### assets

Stores physical equipment and tools tracked by the system.

| Column     | Type     | Constraints           | Description                    |
|------------|----------|-----------------------|--------------------------------|
| id         | String   | PRIMARY KEY           | UUID                           |
| name       | String   | NOT NULL              | Asset name/description         |
| category   | String   | NOT NULL              | Asset category                 |
| project_id | String   | FOREIGN KEY, NULLABLE | Current project assignment     |
| created_at | DateTime | DEFAULT now()         | Asset creation timestamp       |
| updated_at | DateTime | DEFAULT now()         | Last update timestamp          |

**Indexes:**
- PRIMARY KEY on `id`
- FOREIGN KEY on `project_id` → `projects.id`

**Relationships:**
- Many-to-One with `projects`
- One-to-Many with `asset_history`

**Categories:**
- Heavy Equipment
- Power Equipment
- Safety Equipment
- Hand Tools
- Vehicles
- Other

**Sample Data:**
```sql
INSERT INTO assets (id, name, category, project_id) VALUES
('asset-001', 'Excavator CAT 320', 'Heavy Equipment', 'proj-001'),
('asset-002', 'Generator 50kW', 'Power Equipment', 'proj-001'),
('asset-003', 'Scaffolding Set A', 'Safety Equipment', NULL);
```

---

### subcontractors

Stores third-party contractor information.

| Column     | Type     | Constraints    | Description                        |
|------------|----------|---------------|------------------------------------|
| id         | String   | PRIMARY KEY   | UUID                               |
| name       | String   | NOT NULL      | Subcontractor company name         |
| email      | String   |               | Contact email                      |
| phone      | String   |               | Contact phone number               |
| created_at | DateTime | DEFAULT now() | Subcontractor creation timestamp   |

**Indexes:**
- PRIMARY KEY on `id`

**Relationships:**
- One-to-Many with `compliance_documents`
- Many-to-Many with `projects` (via junction table)

**Sample Data:**
```sql
INSERT INTO subcontractors (id, name, email, phone) VALUES
('sub-001', 'ABC Electrical Services', 'contact@abcelectrical.com', '555-0101'),
('sub-002', 'XYZ Plumbing Co', 'info@xyzplumbing.com', '555-0202');
```

---

### compliance_documents

Stores compliance document metadata and file references.

| Column            | Type     | Constraints    | Description                    |
|-------------------|----------|---------------|--------------------------------|
| id                | String   | PRIMARY KEY   | UUID                           |
| subcontractor_id  | String   | FOREIGN KEY   | Associated subcontractor       |
| document_type     | String   | NOT NULL      | Type of document               |
| file_path         | String   | NOT NULL      | Path to PDF file               |
| expiry_date       | Date     | NOT NULL      | Document expiration date       |
| uploaded_at       | DateTime | DEFAULT now() | Upload timestamp               |

**Indexes:**
- PRIMARY KEY on `id`
- FOREIGN KEY on `subcontractor_id` → `subcontractors.id`
- INDEX on `expiry_date` (for compliance checks)

**Relationships:**
- Many-to-One with `subcontractors`

**Document Types:**
- Liability Insurance
- Workers Compensation Insurance
- Safety Certification
- License
- Bond
- Other

**Sample Data:**
```sql
INSERT INTO compliance_documents (id, subcontractor_id, document_type, file_path, expiry_date) VALUES
('doc-001', 'sub-001', 'Liability Insurance', 'uploads/compliance/insurance.pdf', '2025-06-30'),
('doc-002', 'sub-001', 'Safety Certification', 'uploads/compliance/safety.pdf', '2024-11-25'),
('doc-003', 'sub-002', 'Liability Insurance', 'uploads/compliance/insurance2.pdf', '2025-02-15');
```

---

### asset_history

Audit trail for asset movements between projects.

| Column     | Type     | Constraints           | Description                |
|------------|----------|-----------------------|----------------------------|
| id         | String   | PRIMARY KEY           | UUID                       |
| asset_id   | String   | FOREIGN KEY           | Asset being moved          |
| project_id | String   | FOREIGN KEY, NULLABLE | Destination project        |
| moved_at   | DateTime | DEFAULT now()         | Movement timestamp         |
| moved_by   | String   | FOREIGN KEY, NULLABLE | User who moved the asset   |

**Indexes:**
- PRIMARY KEY on `id`
- FOREIGN KEY on `asset_id` → `assets.id`
- FOREIGN KEY on `project_id` → `projects.id`
- FOREIGN KEY on `moved_by` → `users.id`
- INDEX on `asset_id` (for history queries)
- INDEX on `moved_at` (for chronological queries)

**Relationships:**
- Many-to-One with `assets`
- Many-to-One with `projects`
- Many-to-One with `users`

**Sample Data:**
```sql
INSERT INTO asset_history (id, asset_id, project_id, moved_by, moved_at) VALUES
('hist-001', 'asset-001', 'proj-001', 'abc-123', '2024-11-17 10:30:00'),
('hist-002', 'asset-001', 'proj-002', 'def-456', '2024-11-18 14:15:00');
```

---

### project_subcontractors (Junction Table)

Many-to-many relationship between projects and subcontractors.

| Column            | Type   | Constraints           | Description              |
|-------------------|--------|-----------------------|--------------------------|
| project_id        | String | PRIMARY KEY, FOREIGN KEY | Project reference     |
| subcontractor_id  | String | PRIMARY KEY, FOREIGN KEY | Subcontractor reference |

**Indexes:**
- COMPOSITE PRIMARY KEY on (`project_id`, `subcontractor_id`)
- FOREIGN KEY on `project_id` → `projects.id`
- FOREIGN KEY on `subcontractor_id` → `subcontractors.id`

**Sample Data:**
```sql
INSERT INTO project_subcontractors (project_id, subcontractor_id) VALUES
('proj-001', 'sub-001'),
('proj-001', 'sub-002'),
('proj-002', 'sub-002');
```

---

### places (Legacy)

Legacy table for backward compatibility. Not actively used in MVP.

| Column   | Type   | Constraints  | Description      |
|----------|--------|-------------|------------------|
| id       | String | PRIMARY KEY | UUID             |
| name     | String |             | Place name       |
| location | String |             | Place location   |

**Note:** This table exists for backward compatibility with earlier versions. New implementations should use the `projects` table instead.

---

## Database Initialization

### Create Tables

```python
from database.db import init_db

init_db()
```

### Seed Data

```python
from database.init_db import seed_data

seed_data()
```

### Reset Database

```python
from database.db import reset_db

reset_db()  # WARNING: Deletes all data!
```

---

## Queries

### Common Queries

#### Get all assets with project names
```python
from database.db import get_db
from database.models import AssetORM

db = next(get_db())
assets = db.query(AssetORM).all()

for asset in assets:
    print(f"{asset.name} - {asset.project.name if asset.project else 'Unassigned'}")
```

#### Get compliance status for a project
```python
from database.models import ProjectORM, ComplianceDocumentORM
from services.compliance_service import ComplianceService

db = next(get_db())
project = db.query(ProjectORM).filter(ProjectORM.id == project_id).first()

for subcontractor in project.subcontractors:
    status = ComplianceService.calculate_subcontractor_status(subcontractor.documents)
    print(f"{subcontractor.name}: {status}")
```

#### Get expiring documents
```python
from datetime import datetime, timedelta
from database.models import ComplianceDocumentORM

db = next(get_db())
thirty_days_from_now = datetime.now().date() + timedelta(days=30)

expiring_docs = db.query(ComplianceDocumentORM).filter(
    ComplianceDocumentORM.expiry_date <= thirty_days_from_now
).all()
```

#### Get asset movement history
```python
from database.models import AssetHistoryORM

db = next(get_db())
history = db.query(AssetHistoryORM).filter(
    AssetHistoryORM.asset_id == asset_id
).order_by(AssetHistoryORM.moved_at.desc()).all()

for record in history:
    print(f"{record.moved_at}: Moved to {record.project.name} by {record.moved_by_user.username}")
```

---

## Migrations

Currently, the system uses a simple table creation approach. For production, consider using Alembic for migrations:

### Setup Alembic

```bash
pip install alembic
alembic init alembic
```

### Create Migration

```bash
alembic revision --autogenerate -m "Add new column"
```

### Apply Migration

```bash
alembic upgrade head
```

---

## Backup and Restore

### Backup

```bash
# Using Docker
docker-compose exec db pg_dump -U admin sitesteward > backup.sql

# Using Make
make backup
```

### Restore

```bash
# Using Docker
docker-compose exec -T db psql -U admin sitesteward < backup.sql

# Using Make
make restore
```

---

## Performance Optimization

### Indexes

Current indexes:
- `users.username` (UNIQUE)
- `assets.project_id` (FOREIGN KEY)
- `compliance_documents.subcontractor_id` (FOREIGN KEY)
- `compliance_documents.expiry_date` (for compliance checks)
- `asset_history.asset_id` (for history queries)

### Query Optimization

Use eager loading to avoid N+1 queries:

```python
from sqlalchemy.orm import joinedload

# Load assets with projects in one query
assets = db.query(AssetORM).options(joinedload(AssetORM.project)).all()

# Load project with subcontractors and documents
project = db.query(ProjectORM).options(
    joinedload(ProjectORM.subcontractors).joinedload(SubcontractorORM.documents)
).filter(ProjectORM.id == project_id).first()
```

### Connection Pooling

SQLAlchemy automatically manages connection pooling. Configure in `database/db.py`:

```python
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)
```

---

## Data Integrity

### Constraints

- **Primary Keys**: Ensure unique identification
- **Foreign Keys**: Maintain referential integrity
- **NOT NULL**: Prevent missing required data
- **UNIQUE**: Prevent duplicate usernames

### Cascading Deletes

Currently not implemented. Consider adding:

```python
# In models.py
class ProjectORM(Base):
    assets = relationship("AssetORM", back_populates="project", cascade="all, delete-orphan")
```

---

## Security Considerations

### Password Storage
- Passwords hashed with bcrypt
- Salt automatically generated
- Never store plain text passwords

### SQL Injection Prevention
- SQLAlchemy ORM prevents SQL injection
- Always use parameterized queries
- Never concatenate user input into SQL

### Data Access
- Use database sessions per request
- Close sessions after use
- Implement row-level security if needed

---

## Related Documentation
- [System Overview](01_SYSTEM_OVERVIEW.md)
- [Architecture](02_ARCHITECTURE.md)
- [API Reference](03_API_REFERENCE.md)
- [Development Guide](07_DEVELOPMENT_GUIDE.md)
