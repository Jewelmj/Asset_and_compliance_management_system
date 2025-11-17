# Site-Steward MVP - Quick Start Guide

This guide will help you get the Site-Steward MVP up and running in minutes.

## Prerequisites

- Docker and Docker Compose installed
- Git (to clone the repository)

## Quick Start (5 minutes)

### 1. Clone and Configure

```bash
# Clone the repository
git clone <repository-url>
cd Asset_and_compliance_management_system

# Create environment file
cp .env.example .env

# Edit .env and set required variables:
# - POSTGRES_PASSWORD (required)
# - JWT_SECRET (required)
# - SMTP credentials (optional, for email notifications)
```

### 2. Build and Start Services

```bash
# Build all Docker images
make build

# Start all services
make up
```

This will start:
- PostgreSQL database on port 5432
- Flask API on port 5000
- Admin Portal on port 8501
- Field App on port 8502

### 3. Initialize Database with Seed Data

```bash
# Initialize database and add sample data
make seed-db
```

This creates:
- Admin user (username: `admin`, password: `admin123`)
- Foreman user (username: `foreman`, password: `foreman123`)
- Sample projects, assets, subcontractors, and compliance documents

### 4. Access the Applications

**Admin Portal:** http://localhost:8501
- Login with `admin` / `admin123`
- Manage assets, projects, subcontractors, and compliance documents

**Field Mobile App:** http://localhost:8502
- Login with `foreman` / `foreman123`
- Scan QR codes and view compliance status

**API Documentation:** http://localhost:5000/swagger-ui
- Interactive API documentation

## Default Credentials

### Admin User
- Username: `admin`
- Password: `admin123`
- Role: Administrator
- Access: Full system access

### Foreman User
- Username: `foreman`
- Password: `foreman123`
- Role: Site Foreman
- Access: Field operations (scan assets, view compliance)

## Sample Data

The seed data includes:

### Projects
1. **Downtown Office Building** - 123 Main St, City
2. **Residential Complex Phase 2** - 456 Oak Ave, Town

### Assets
1. **Excavator CAT 320** (Heavy Equipment) - At Downtown Office Building
2. **Generator 50kW** (Power Equipment) - At Downtown Office Building
3. **Scaffolding Set A** (Safety Equipment) - Unassigned

### Subcontractors
1. **ABC Electrical Services**
   - Has 2 compliance documents
   - One document expiring soon (RED status)

2. **XYZ Plumbing Co**
   - Has 1 compliance document
   - All documents valid (GREEN status)

## Common Commands

```bash
# View logs
make logs

# Restart services
make restart

# Stop services
make down

# Clean up everything (removes all data!)
make clean

# Backup database
make backup

# Initialize database (tables only)
make init-db

# Initialize with seed data
make seed-db
```

## Testing the Features

### 1. Asset Management (Admin Portal)
1. Go to http://localhost:8501
2. Login as admin
3. Navigate to "Assets" page
4. Create a new asset
5. Download the generated QR code

### 2. QR Code Scanning (Field App)
1. Go to http://localhost:8502
2. Login as foreman
3. Click "Scan Asset"
4. Use your phone camera to scan the QR code
5. View asset details and move to a project

### 3. Compliance Monitoring (Admin Portal)
1. Login to Admin Portal as admin
2. Navigate to "Project Hub"
3. Select a project
4. View compliance status with RED/GREEN indicators

### 4. Document Upload (Admin Portal)
1. Navigate to "Compliance" page
2. Select a subcontractor
3. Upload a PDF document
4. Set expiry date
5. View status in Project Hub

## Troubleshooting

### Services won't start
```bash
# Check if ports are already in use
docker ps

# Check logs for errors
make logs
```

### Database connection errors
```bash
# Ensure database is healthy
docker-compose ps db

# Restart database
docker-compose restart db
```

### Can't login
```bash
# Re-run seed data
make seed-db
```

### Reset everything
```bash
# Stop and remove all containers and volumes
make clean

# Start fresh
make build
make up
make seed-db
```

## Next Steps

- Read [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md) for deployment details
- Read [database/README.md](database/README.md) for database management
- Read [AUTHENTICATION_IMPLEMENTATION.md](AUTHENTICATION_IMPLEMENTATION.md) for auth details
- Customize the seed data in `database/init_db.py`
- Configure email notifications in `.env`

## Production Deployment

**Important:** Before deploying to production:

1. Change default passwords
2. Use strong JWT_SECRET
3. Configure proper SMTP settings
4. Enable HTTPS
5. Set up proper backup strategy
6. Review security settings

See [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md) for production deployment guide.

## Support

For issues or questions:
1. Check the logs: `make logs`
2. Review the documentation in each component's README
3. Check the troubleshooting section above

## Architecture

```
┌─────────────────┐         ┌─────────────────┐
│  Admin Portal   │         │   Field App     │
│   (Streamlit)   │         │   (Streamlit)   │
│  Port: 8501     │         │  Port: 8502     │
└────────┬────────┘         └────────┬────────┘
         │                           │
         │      HTTP/JSON (JWT)      │
         └───────────┬───────────────┘
                     │
              ┌──────▼──────┐
              │  Flask API  │
              │  Port: 5000 │
              └──────┬──────┘
                     │
              ┌──────▼──────┐
              │ PostgreSQL  │
              │  Port: 5432 │
              └─────────────┘
```
