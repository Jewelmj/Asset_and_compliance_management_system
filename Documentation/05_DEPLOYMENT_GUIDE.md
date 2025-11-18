# Site-Steward MVP - Deployment Guide

## Table of Contents
1. [Quick Start](#quick-start)
2. [Development Deployment](#development-deployment)
3. [Production Deployment](#production-deployment)
4. [Cloud Deployment](#cloud-deployment)
5. [Configuration](#configuration)
6. [Monitoring](#monitoring)
7. [Backup Strategy](#backup-strategy)

## Quick Start

### Prerequisites
- Docker 20.10+
- Docker Compose 2.0+
- 4GB RAM minimum
- 20GB disk space

### 5-Minute Deployment

```bash
# 1. Clone repository
git clone <repository-url>
cd Asset_and_compliance_management_system

# 2. Create environment file
cp .env.example .env

# 3. Edit .env and set required variables
nano .env  # or use your preferred editor

# 4. Build and start services
make build
make up

# 5. Initialize database with seed data
make seed-db

# 6. Access applications
# Admin Portal: http://localhost:8501
# Field App: http://localhost:8502
# API: http://localhost:5000
```

Default credentials:
- Admin: `admin` / `admin123`
- Foreman: `foreman` / `foreman123`

---

## Development Deployment

### Local Development Setup

#### 1. Environment Configuration

Create `.env` file:
```bash
# Database Configuration
POSTGRES_DB=sitesteward
POSTGRES_USER=admin
POSTGRES_PASSWORD=dev_password_123

# JWT Configuration
JWT_SECRET=dev_secret_key_change_in_production

# API Configuration
API_URL=http://localhost:5000
FLASK_ENV=development

# Email Configuration (Optional for development)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=noreply@sitesteward.com
ALERT_EMAIL_RECIPIENTS=admin@example.com
```

#### 2. Build Services

```bash
# Build all Docker images
docker-compose build

# Or build specific service
docker-compose build api
docker-compose build admin_portal
docker-compose build field_app
```

#### 3. Start Services

```bash
# Start all services in detached mode
docker-compose up -d

# Or start with logs visible
docker-compose up

# Start specific service
docker-compose up -d api
```

#### 4. Initialize Database

```bash
# Create tables only
make init-db

# Create tables and seed data
make seed-db

# Verify seed data
make verify-db
```

#### 5. View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api
docker-compose logs -f admin_portal
docker-compose logs -f field_app
docker-compose logs -f db
```

#### 6. Development with Hot Reload

```bash
# Start in development mode
make dev

# Or manually
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

---

## Production Deployment

### Pre-Deployment Checklist

- [ ] Change default passwords
- [ ] Generate strong JWT_SECRET
- [ ] Configure production SMTP settings
- [ ] Set up HTTPS/SSL certificates
- [ ] Configure firewall rules
- [ ] Set up backup strategy
- [ ] Configure monitoring and alerting
- [ ] Review security settings
- [ ] Test disaster recovery procedures
- [ ] Document deployment procedures

### Production Environment Configuration

Create `.env` file with production values:

```bash
# Database Configuration
POSTGRES_DB=sitesteward
POSTGRES_USER=admin
POSTGRES_PASSWORD=<strong-random-password>

# JWT Configuration (Generate with: openssl rand -hex 32)
JWT_SECRET=<strong-random-secret-64-chars>

# API Configuration
API_URL=https://api.yourdomain.com
FLASK_ENV=production

# Email Configuration
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=<sendgrid-api-key>
SMTP_FROM_EMAIL=noreply@yourdomain.com
ALERT_EMAIL_RECIPIENTS=admin@yourdomain.com,manager@yourdomain.com
```

### Generate Strong Secrets

```bash
# Generate JWT secret
openssl rand -hex 32

# Generate database password
openssl rand -base64 32
```

### Production Docker Compose

Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  db:
    restart: always
    environment:
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - internal

  api:
    restart: always
    environment:
      FLASK_ENV: production
    volumes:
      - ./uploads:/app/uploads
      - ./logs:/app/logs
    networks:
      - internal
      - external

  admin_portal:
    restart: always
    networks:
      - external

  field_app:
    restart: always
    networks:
      - external

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - api
      - admin_portal
      - field_app
    networks:
      - external
    restart: always

networks:
  internal:
    driver: bridge
  external:
    driver: bridge

volumes:
  postgres_data:
    driver: local
```

### HTTPS Configuration with Nginx

Create `nginx.conf`:

```nginx
events {
    worker_connections 1024;
}

http {
    upstream api {
        server api:5000;
    }

    upstream admin {
        server admin_portal:8501;
    }

    upstream field {
        server field_app:8501;
    }

    # Redirect HTTP to HTTPS
    server {
        listen 80;
        server_name yourdomain.com;
        return 301 https://$server_name$request_uri;
    }

    # API Server
    server {
        listen 443 ssl http2;
        server_name api.yourdomain.com;

        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;

        location / {
            proxy_pass http://api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }

    # Admin Portal
    server {
        listen 443 ssl http2;
        server_name admin.yourdomain.com;

        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;

        location / {
            proxy_pass http://admin;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }
    }

    # Field App
    server {
        listen 443 ssl http2;
        server_name field.yourdomain.com;

        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;

        location / {
            proxy_pass http://field;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }
    }
}
```

### SSL Certificate Setup

#### Using Let's Encrypt (Recommended)

```bash
# Install certbot
sudo apt-get install certbot

# Generate certificates
sudo certbot certonly --standalone -d yourdomain.com -d api.yourdomain.com -d admin.yourdomain.com -d field.yourdomain.com

# Copy certificates
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem ./ssl/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ./ssl/key.pem

# Set up auto-renewal
sudo certbot renew --dry-run
```

#### Using Self-Signed Certificate (Development Only)

```bash
# Generate self-signed certificate
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout ssl/key.pem -out ssl/cert.pem
```

### Deploy to Production

```bash
# 1. Pull latest code
git pull origin main

# 2. Build images
docker-compose -f docker-compose.yml -f docker-compose.prod.yml build

# 3. Stop existing services
docker-compose down

# 4. Start production services
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# 5. Initialize database (first time only)
docker-compose exec api python database/init_db.py

# 6. Verify deployment
docker-compose ps
docker-compose logs -f
```

### Firewall Configuration

```bash
# Allow SSH
sudo ufw allow 22/tcp

# Allow HTTP and HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Enable firewall
sudo ufw enable

# Check status
sudo ufw status
```

---

## Cloud Deployment

### AWS Deployment

#### Using EC2

1. **Launch EC2 Instance**
   - AMI: Ubuntu 22.04 LTS
   - Instance Type: t3.medium (2 vCPU, 4GB RAM)
   - Storage: 30GB EBS
   - Security Group: Allow ports 22, 80, 443

2. **Install Docker**
```bash
# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Add user to docker group
sudo usermod -aG docker $USER
```

3. **Deploy Application**
```bash
# Clone repository
git clone <repository-url>
cd Asset_and_compliance_management_system

# Configure environment
cp .env.example .env
nano .env

# Deploy
docker-compose up -d
```

4. **Configure RDS (Optional)**
   - Create PostgreSQL RDS instance
   - Update DATABASE_URL in .env
   - Remove db service from docker-compose.yml

#### Using ECS (Elastic Container Service)

1. **Push Images to ECR**
```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Tag and push images
docker tag sitesteward-api:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/sitesteward-api:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/sitesteward-api:latest
```

2. **Create ECS Task Definition**
3. **Create ECS Service**
4. **Configure Application Load Balancer**

### Azure Deployment

#### Using Azure Container Instances

```bash
# Login to Azure
az login

# Create resource group
az group create --name sitesteward-rg --location eastus

# Create container registry
az acr create --resource-group sitesteward-rg --name sitestewardacr --sku Basic

# Push images to ACR
az acr login --name sitestewardacr
docker tag sitesteward-api:latest sitestewardacr.azurecr.io/sitesteward-api:latest
docker push sitestewardacr.azurecr.io/sitesteward-api:latest

# Deploy container group
az container create \
  --resource-group sitesteward-rg \
  --name sitesteward-api \
  --image sitestewardacr.azurecr.io/sitesteward-api:latest \
  --dns-name-label sitesteward-api \
  --ports 5000
```

### Google Cloud Platform

#### Using Cloud Run

```bash
# Build and push to Container Registry
gcloud builds submit --tag gcr.io/PROJECT_ID/sitesteward-api

# Deploy to Cloud Run
gcloud run deploy sitesteward-api \
  --image gcr.io/PROJECT_ID/sitesteward-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

## Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| POSTGRES_DB | Yes | sitesteward | Database name |
| POSTGRES_USER | Yes | admin | Database user |
| POSTGRES_PASSWORD | Yes | - | Database password |
| JWT_SECRET | Yes | - | JWT signing secret |
| API_URL | No | http://api:5000 | API base URL |
| FLASK_ENV | No | production | Flask environment |
| SMTP_HOST | No | - | SMTP server host |
| SMTP_PORT | No | 587 | SMTP server port |
| SMTP_USER | No | - | SMTP username |
| SMTP_PASSWORD | No | - | SMTP password |
| SMTP_FROM_EMAIL | No | - | From email address |
| ALERT_EMAIL_RECIPIENTS | No | - | Comma-separated emails |

### Scheduled Tasks

Set up cron job for compliance checks:

```bash
# Edit crontab
crontab -e

# Add daily compliance check at 8:00 AM
0 8 * * * cd /path/to/project && docker-compose exec -T api python scripts/check_expiry.py >> /var/log/compliance_check.log 2>&1
```

---

## Monitoring

### Health Checks

```bash
# API health check
curl http://localhost:5000/

# Database health check
docker-compose exec db pg_isready -U admin

# Check all services
docker-compose ps
```

### Logging

```bash
# View logs
docker-compose logs -f

# Export logs
docker-compose logs > logs.txt

# Configure log rotation
# Add to /etc/logrotate.d/docker-compose
/var/lib/docker/containers/*/*.log {
  rotate 7
  daily
  compress
  missingok
  delaycompress
  copytruncate
}
```

### Monitoring Tools

- **Prometheus**: Metrics collection
- **Grafana**: Visualization
- **ELK Stack**: Log aggregation
- **Sentry**: Error tracking
- **Uptime Robot**: Uptime monitoring

---

## Backup Strategy

### Database Backups

#### Automated Daily Backups

```bash
# Create backup script
cat > backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
docker-compose exec -T db pg_dump -U admin sitesteward > "$BACKUP_DIR/backup_$DATE.sql"
# Keep only last 30 days
find $BACKUP_DIR -name "backup_*.sql" -mtime +30 -delete
EOF

chmod +x backup.sh

# Add to crontab (daily at 2 AM)
0 2 * * * /path/to/backup.sh
```

#### Manual Backup

```bash
# Backup database
make backup

# Or manually
docker-compose exec db pg_dump -U admin sitesteward > backup.sql
```

#### Restore from Backup

```bash
# Restore database
docker-compose exec -T db psql -U admin sitesteward < backup.sql
```

### File Backups

```bash
# Backup compliance documents
tar -czf uploads_backup.tar.gz uploads/

# Restore compliance documents
tar -xzf uploads_backup.tar.gz
```

### Cloud Backups

#### AWS S3

```bash
# Install AWS CLI
pip install awscli

# Backup to S3
aws s3 cp backup.sql s3://your-bucket/backups/backup_$(date +%Y%m%d).sql
aws s3 sync uploads/ s3://your-bucket/uploads/
```

---

## Troubleshooting

### Common Issues

#### Services Won't Start

```bash
# Check logs
docker-compose logs

# Check port conflicts
sudo netstat -tulpn | grep LISTEN

# Restart services
docker-compose restart
```

#### Database Connection Errors

```bash
# Check database is running
docker-compose ps db

# Check database logs
docker-compose logs db

# Restart database
docker-compose restart db
```

#### Out of Disk Space

```bash
# Check disk usage
df -h

# Clean up Docker
docker system prune -a

# Remove old backups
find /backups -name "backup_*.sql" -mtime +30 -delete
```

---

## Related Documentation
- [System Overview](01_SYSTEM_OVERVIEW.md)
- [Architecture](02_ARCHITECTURE.md)
- [Security Guide](08_SECURITY.md)
- [Troubleshooting](09_TROUBLESHOOTING.md)
