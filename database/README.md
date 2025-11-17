# Database Initialization and Seed Data

This directory contains database models, initialization scripts, and seed data for the Site-Steward MVP.

## Overview

The database uses PostgreSQL 15+ with SQLAlchemy ORM for data modeling and migrations.

## Database Schema

### Tables

- **users** - User accounts with authentication credentials
- **projects** - Construction projects
- **assets** - Physical equipment tracked via QR codes
- **subcontractors** - Third-party contractors
- **compliance_documents** - PDF documents with expiry dates
- **project_subcontractors** - Junction table for project-subcontractor relationships
- **asset_history** - Audit trail for asset movements
- **places** - Legacy table for backward compatibility

## Initialization

### Using Docker (Recommended)

1. **Start the database service:**
   ```bash
   docker-compose up -d db
   ```

2. **Initialize database tables:**
   ```bash
   make init-db
   ```
   Or manually:
   ```bash
   docker-compose exec api python database/init_db.py
   ```

3. **Initialize with seed data:**
   ```bash
   make seed-db
   ```
   Or manually:
   ```bash
   docker-compose exec api python database/init_db.py --seed
   ```

### Local Development (Without Docker)

1. **Ensure PostgreSQL is running locally**

2. **Set environment variables:**
   ```bash
   export DATABASE_URL="postgresql://admin:password@localhost:5432/sitesteward"
   ```

3. **Run initialization script:**
   ```bash
   python -m database.init_db
   ```

4. **Run with seed data:**
   ```bash
   python -m database.init_db --seed
   ```

## Seed Data

The seed data includes:

### Users
- **Admin User**
  - Username: `admin`
  - Password: `admin123`
  - Role: `admin`
  - Email: `admin@sitesteward.com`

- **Foreman User**
  - Username: `foreman`
  - Password: `foreman123`
  - Role: `foreman`
  - Email: `foreman@sitesteward.com`

### Projects
- Downtown Office Building (123 Main St, City)
- Residential Complex Phase 2 (456 Oak Ave, Town)

### Assets
- Excavator CAT 320 (Heavy Equipment) - Assigned to Downtown Office Building
- Generator 50kW (Power Equipment) - Assigned to Downtown Office Building
- Scaffolding Set A (Safety Equipment) - Unassigned

### Subcontractors
- ABC Electrical Services
  - Email: contact@abcelectrical.com
  - Phone: 555-0101
  - Documents: Liability Insurance (expires in 45 days), Safety Certification (expires in 15 days - RED status)

- XYZ Plumbing Co
  - Email: info@xyzplumbing.com
  - Phone: 555-0202
  - Documents: Liability Insurance (expires in 90 days)

### Compliance Documents
- Documents with varying expiry dates to demonstrate RED/GREEN status indicators
- RED status: Documents expiring within 30 days or already expired
- GREEN status: Documents valid for more than 30 days

## Database Management

### Reset Database
**WARNING: This will delete all data!**

```bash
docker-compose exec api python -c "from database.db import reset_db; reset_db()"
```

### Backup Database
```bash
make backup
```

### Restore Database
```bash
make restore
```

## Connection Details

### Docker Environment
- Host: `db` (internal network) or `localhost` (external)
- Port: `5432`
- Database: `sitesteward`
- User: `admin`
- Password: Set via `POSTGRES_PASSWORD` environment variable

### Environment Variables
- `DATABASE_URL` - Full PostgreSQL connection string
- `POSTGRES_DB` - Database name (default: sitesteward)
- `POSTGRES_USER` - Database user (default: admin)
- `POSTGRES_PASSWORD` - Database password (required)

## Files

- `db.py` - Database connection and session management
- `models.py` - SQLAlchemy ORM models
- `init_db.py` - Initialization and seed data script

## Troubleshooting

### Connection Refused
If you get a connection error, ensure the database service is running:
```bash
docker-compose ps db
```

### Tables Already Exist
The initialization script is idempotent and will not fail if tables already exist.

### Seed Data Already Exists
If you run the seed script multiple times, you may get unique constraint errors. Reset the database first if you need fresh seed data.

## Requirements

See `requirements.txt` for Python dependencies:
- SQLAlchemy 2.x
- psycopg2-binary
- bcrypt
