# Seed Data Documentation

This document describes the seed data included in the Site-Steward MVP for testing and development purposes.

## Overview

The seed data provides a complete working environment with sample users, projects, assets, subcontractors, and compliance documents. This allows immediate testing of all system features without manual data entry.

## How to Load Seed Data

### Quick Start

```bash
# Using Make (recommended)
make seed-db

# Or manually with Docker
docker-compose exec api python database/init_db.py --seed
```

### Verification

After loading seed data, verify it was successful:

```bash
make verify-db
```

## Seed Data Contents

### 1. Users (2 accounts)

#### Admin User
- **ID**: Auto-generated UUID
- **Username**: `admin`
- **Password**: `admin123`
- **Role**: `admin`
- **Email**: `admin@sitesteward.com`
- **Permissions**: Full system access
- **Use Cases**: 
  - Manage assets, projects, subcontractors
  - Upload compliance documents
  - View all dashboards and reports

#### Foreman User
- **ID**: Auto-generated UUID
- **Username**: `foreman`
- **Password**: `foreman123`
- **Role**: `foreman`
- **Email**: `foreman@sitesteward.com`
- **Permissions**: Field operations
- **Use Cases**:
  - Scan QR codes
  - Move assets between projects
  - View compliance status

### 2. Projects (2 projects)

#### Project 1: Downtown Office Building
- **ID**: Auto-generated UUID
- **Name**: Downtown Office Building
- **Location**: 123 Main St, City
- **Assets**: 2 assets assigned
- **Subcontractors**: 2 subcontractors assigned

#### Project 2: Residential Complex Phase 2
- **ID**: Auto-generated UUID
- **Name**: Residential Complex Phase 2
- **Location**: 456 Oak Ave, Town
- **Assets**: 0 assets assigned
- **Subcontractors**: 1 subcontractor assigned

### 3. Assets (3 assets)

#### Asset 1: Excavator CAT 320
- **ID**: Auto-generated UUID
- **Name**: Excavator CAT 320
- **Category**: Heavy Equipment
- **Current Location**: Downtown Office Building
- **QR Code**: Can be generated via Admin Portal
- **History**: 1 movement record

#### Asset 2: Generator 50kW
- **ID**: Auto-generated UUID
- **Name**: Generator 50kW
- **Category**: Power Equipment
- **Current Location**: Downtown Office Building
- **QR Code**: Can be generated via Admin Portal

#### Asset 3: Scaffolding Set A
- **ID**: Auto-generated UUID
- **Name**: Scaffolding Set A
- **Category**: Safety Equipment
- **Current Location**: Unassigned
- **QR Code**: Can be generated via Admin Portal
- **Use Case**: Demonstrates unassigned asset

### 4. Subcontractors (2 subcontractors)

#### Subcontractor 1: ABC Electrical Services
- **ID**: Auto-generated UUID
- **Name**: ABC Electrical Services
- **Email**: contact@abcelectrical.com
- **Phone**: 555-0101
- **Projects**: Downtown Office Building
- **Documents**: 2 compliance documents
  - Liability Insurance (expires in 45 days) - GREEN status
  - Safety Certification (expires in 15 days) - RED status
- **Use Case**: Demonstrates RED compliance status

#### Subcontractor 2: XYZ Plumbing Co
- **ID**: Auto-generated UUID
- **Name**: XYZ Plumbing Co
- **Email**: info@xyzplumbing.com
- **Phone**: 555-0202
- **Projects**: Downtown Office Building, Residential Complex Phase 2
- **Documents**: 1 compliance document
  - Liability Insurance (expires in 90 days) - GREEN status
- **Use Case**: Demonstrates GREEN compliance status

### 5. Compliance Documents (3 documents)

#### Document 1: ABC Electrical - Liability Insurance
- **ID**: Auto-generated UUID
- **Subcontractor**: ABC Electrical Services
- **Type**: Liability Insurance
- **File Path**: uploads/compliance/sample_insurance.pdf
- **Expiry Date**: Current date + 45 days
- **Status**: GREEN (valid for more than 30 days)

#### Document 2: ABC Electrical - Safety Certification
- **ID**: Auto-generated UUID
- **Subcontractor**: ABC Electrical Services
- **Type**: Safety Certification
- **File Path**: uploads/compliance/sample_safety_cert.pdf
- **Expiry Date**: Current date + 15 days
- **Status**: RED (expiring within 30 days)
- **Use Case**: Will trigger email alert from compliance check script

#### Document 3: XYZ Plumbing - Liability Insurance
- **ID**: Auto-generated UUID
- **Subcontractor**: XYZ Plumbing Co
- **Type**: Liability Insurance
- **File Path**: uploads/compliance/sample_insurance2.pdf
- **Expiry Date**: Current date + 90 days
- **Status**: GREEN (valid for more than 30 days)

### 6. Asset History (1 record)

#### History 1: Excavator Movement
- **ID**: Auto-generated UUID
- **Asset**: Excavator CAT 320
- **Project**: Downtown Office Building
- **Moved By**: Admin user
- **Moved At**: Current timestamp
- **Use Case**: Demonstrates asset tracking history

### 7. Project-Subcontractor Relationships

The junction table creates the following relationships:

- **Downtown Office Building** ↔ ABC Electrical Services
- **Downtown Office Building** ↔ XYZ Plumbing Co
- **Residential Complex Phase 2** ↔ XYZ Plumbing Co

## Compliance Status Demonstration

The seed data is designed to demonstrate both compliance statuses:

### GREEN Status (Compliant)
- XYZ Plumbing Co: All documents valid for > 30 days
- ABC Electrical - Liability Insurance: Valid for 45 days

### RED Status (Non-Compliant)
- ABC Electrical - Safety Certification: Expires in 15 days
- This will appear in red on the Project Hub dashboard
- This will trigger email alerts from the compliance check script

## Testing Scenarios

### Scenario 1: Asset Tracking
1. Login as admin
2. View Excavator CAT 320 in Assets page
3. See it's assigned to Downtown Office Building
4. Generate QR code
5. Login as foreman on Field App
6. Scan QR code
7. Move asset to Residential Complex Phase 2
8. View updated location and history

### Scenario 2: Compliance Monitoring
1. Login as admin
2. Navigate to Project Hub
3. Select Downtown Office Building
4. See ABC Electrical with RED status (Safety Certification expiring)
5. See XYZ Plumbing with GREEN status
6. Run compliance check script
7. Receive email alert for ABC Electrical

### Scenario 3: Document Upload
1. Login as admin
2. Navigate to Compliance page
3. Select ABC Electrical Services
4. Upload new Safety Certification with future expiry date
5. Return to Project Hub
6. See status change from RED to GREEN

## Customizing Seed Data

To customize the seed data, edit `database/init_db.py`:

```python
def seed_data():
    # Modify user credentials
    admin_password = bcrypt.hashpw("your_password".encode('utf-8'), bcrypt.gensalt())
    
    # Add more projects
    project3 = ProjectORM(
        id=str(uuid.uuid4()),
        name="Your Project Name",
        location="Your Location"
    )
    
    # Add more assets, subcontractors, etc.
```

After modifying, reload the seed data:

```bash
# Reset database (WARNING: deletes all data)
docker-compose down -v
docker-compose up -d
make seed-db
```

## Security Notes

### Production Deployment

**IMPORTANT**: Before deploying to production:

1. **Change Default Passwords**
   ```python
   # Use strong, unique passwords
   admin_password = bcrypt.hashpw("strong_random_password".encode('utf-8'), bcrypt.gensalt())
   ```

2. **Remove Test Data**
   - Don't use seed data in production
   - Create real users through the application
   - Use proper onboarding process

3. **Secure Credentials**
   - Store passwords in environment variables
   - Use secrets management (AWS Secrets Manager, Azure Key Vault)
   - Never commit passwords to version control

## File Paths

The seed data references these file paths:
- `uploads/compliance/sample_insurance.pdf`
- `uploads/compliance/sample_safety_cert.pdf`
- `uploads/compliance/sample_insurance2.pdf`

**Note**: These are placeholder paths. The actual PDF files don't exist in the seed data. When testing document upload functionality, you'll need to upload real PDF files through the Admin Portal.

## Database Schema

The seed data populates these tables:
- `users`
- `projects`
- `assets`
- `subcontractors`
- `compliance_documents`
- `project_subcontractors` (junction table)
- `asset_history`

For complete schema details, see `database/models.py` and `database/README.md`.

## Troubleshooting

### Seed Data Won't Load

```bash
# Check database is running
docker-compose ps db

# Check logs
docker-compose logs api

# Try resetting database
docker-compose down -v
docker-compose up -d
make seed-db
```

### Duplicate Key Errors

If you run seed data multiple times, you may get unique constraint errors. Reset the database first:

```bash
docker-compose down -v
docker-compose up -d
make seed-db
```

### Can't Login with Default Credentials

```bash
# Verify seed data was loaded
make verify-db

# If verification fails, reload seed data
make seed-db
```

## Related Documentation

- [database/README.md](README.md) - Database initialization guide
- [database/init_db.py](init_db.py) - Seed data implementation
- [scripts/verify_seed_data.py](../scripts/verify_seed_data.py) - Verification script
- [QUICKSTART.md](../QUICKSTART.md) - Quick start guide
