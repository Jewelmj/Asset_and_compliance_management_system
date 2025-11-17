# Docker Deployment Guide

This guide explains how to deploy the Site-Steward MVP using Docker and Docker Compose.

## Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+

## Quick Start

1. **Clone the repository and navigate to the project directory**

2. **Create environment file**
   ```bash
   cp .env.example .env
   ```

3. **Edit `.env` file with your configuration**
   - Set a secure `POSTGRES_PASSWORD`
   - Set a secure `JWT_SECRET`
   - Configure SMTP settings for email notifications
   - Update `API_URL` if needed (default: http://api:5000)

4. **Build and start all services**
   ```bash
   docker-compose up -d
   ```

5. **Initialize the database**
   ```bash
   docker-compose exec api python database/init_db.py
   ```

6. **Access the applications**
   - Admin Portal: http://localhost:8501
   - Field App: http://localhost:8502
   - API: http://localhost:5000

## Services

### PostgreSQL Database
- **Container**: sitesteward-db
- **Port**: 5432
- **Volume**: postgres_data (persistent storage)

### Flask API
- **Container**: sitesteward-api
- **Port**: 5000
- **Dependencies**: PostgreSQL
- **Volume**: ./uploads (for compliance documents)

### Admin Portal
- **Container**: sitesteward-admin
- **Port**: 8501
- **Dependencies**: API

### Field App
- **Container**: sitesteward-field
- **Port**: 8502
- **Dependencies**: API

## Common Commands

### Start services
```bash
docker-compose up -d
```

### Stop services
```bash
docker-compose down
```

### View logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api
docker-compose logs -f admin_portal
docker-compose logs -f field_app
```

### Rebuild services
```bash
# Rebuild all
docker-compose up -d --build

# Rebuild specific service
docker-compose up -d --build api
```

### Access container shell
```bash
docker-compose exec api bash
docker-compose exec db psql -U admin -d sitesteward
```

### Database operations
```bash
# Run migrations
docker-compose exec api python database/init_db.py

# Backup database
docker-compose exec db pg_dump -U admin sitesteward > backup.sql

# Restore database
docker-compose exec -T db psql -U admin sitesteward < backup.sql
```

## Environment Variables

### Required Variables
- `POSTGRES_PASSWORD`: PostgreSQL database password
- `JWT_SECRET`: Secret key for JWT token signing

### Optional Variables
- `POSTGRES_DB`: Database name (default: sitesteward)
- `POSTGRES_USER`: Database user (default: admin)
- `API_URL`: API endpoint URL (default: http://api:5000)
- `FLASK_ENV`: Flask environment (default: production)
- `SMTP_HOST`: Email server host
- `SMTP_PORT`: Email server port
- `SMTP_USER`: Email username
- `SMTP_PASSWORD`: Email password

## Troubleshooting

### Database connection issues
```bash
# Check database health
docker-compose ps db

# View database logs
docker-compose logs db

# Restart database
docker-compose restart db
```

### API not responding
```bash
# Check API logs
docker-compose logs api

# Restart API
docker-compose restart api
```

### Streamlit apps not loading
```bash
# Check logs
docker-compose logs admin_portal
docker-compose logs field_app

# Rebuild and restart
docker-compose up -d --build admin_portal field_app
```

### Clear all data and restart
```bash
docker-compose down -v
docker-compose up -d
docker-compose exec api python database/init_db.py
```

## Production Considerations

1. **Use strong passwords** for database and JWT secret
2. **Enable HTTPS** using a reverse proxy (nginx, Traefik)
3. **Set up regular backups** for the database volume
4. **Configure firewall rules** to restrict access
5. **Use Docker secrets** for sensitive data in production
6. **Monitor logs** and set up alerting
7. **Update images regularly** for security patches

## Network Architecture

All services communicate through the `sitesteward-network` bridge network:
- Frontend apps (admin_portal, field_app) → API
- API → Database
- External access via exposed ports

## Volume Management

### Persistent Data
- `postgres_data`: Database files
- `./uploads`: Compliance document uploads (bind mount)

### Backup Volumes
```bash
# Backup postgres_data volume
docker run --rm -v sitesteward_postgres_data:/data -v $(pwd):/backup ubuntu tar czf /backup/postgres_backup.tar.gz /data
```

## Scaling

To run multiple instances of frontend apps:
```bash
docker-compose up -d --scale admin_portal=2 --scale field_app=2
```

Note: You'll need to configure a load balancer for multiple instances.
