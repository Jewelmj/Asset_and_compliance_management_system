# Site-Steward MVP - Troubleshooting Guide

## Table of Contents
1. [Common Issues](#common-issues)
2. [Authentication Problems](#authentication-problems)
3. [Database Issues](#database-issues)
4. [API Problems](#api-problems)
5. [Frontend Issues](#frontend-issues)
6. [QR Code Scanning Problems](#qr-code-scanning-problems)
7. [Email Notification Issues](#email-notification-issues)
8. [Performance Problems](#performance-problems)
9. [Docker Issues](#docker-issues)
10. [Getting Help](#getting-help)

## Common Issues

### Services Won't Start

**Symptom**: Docker containers fail to start or exit immediately

**Diagnosis**:
```bash
# Check service status
docker-compose ps

# View logs
docker-compose logs

# Check specific service
docker-compose logs api
docker-compose logs db
```

**Solutions**:

1. **Port Conflicts**:
```bash
# Check if ports are in use
# Windows:
netstat -ano | findstr :5000
netstat -ano | findstr :8501
netstat -ano | findstr :5432

# Linux/Mac:
lsof -i :5000
lsof -i :8501
lsof -i :5432

# Solution: Stop conflicting services or change ports in docker-compose.yml
```

2. **Missing Environment Variables**:
```bash
# Check .env file exists
ls -la .env

# Verify required variables
cat .env | grep POSTGRES_PASSWORD
cat .env | grep JWT_SECRET

# Solution: Create .env from .env.example
cp .env.example .env
nano .env
```

3. **Docker Resources**:
```bash
# Check Docker resources
docker system df

# Clean up if needed
docker system prune -a

# Restart Docker daemon
# Windows: Restart Docker Desktop
# Linux: sudo systemctl restart docker
```

### Application Not Accessible

**Symptom**: Cannot access application at http://localhost:8501

**Diagnosis**:
```bash
# Check if service is running
docker-compose ps admin_portal

# Check if port is exposed
docker-compose port admin_portal 8501

# Test connection
curl http://localhost:8501
```

**Solutions**:

1. **Service Not Running**:
```bash
# Start services
docker-compose up -d

# Restart specific service
docker-compose restart admin_portal
```

2. **Wrong URL**:
- Admin Portal: http://localhost:8501
- Field App: http://localhost:8502
- API: http://localhost:5000

3. **Firewall Blocking**:
```bash
# Windows: Check Windows Firewall
# Linux: Check ufw
sudo ufw status

# Allow ports if needed
sudo ufw allow 8501/tcp
```

---

## Authentication Problems

### Cannot Login

**Symptom**: Login fails with "Invalid credentials" error

**Diagnosis**:
```bash
# Check if database is initialized
docker-compose exec api python scripts/verify_seed_data.py

# Check API logs
docker-compose logs api | grep login
```

**Solutions**:

1. **Database Not Seeded**:
```bash
# Initialize database with seed data
make seed-db

# Or manually
docker-compose exec api python database/init_db.py --seed
```

2. **Wrong Credentials**:
- Default admin: `admin` / `admin123`
- Default foreman: `foreman` / `foreman123`
- Check for typos (case-sensitive)

3. **API Not Responding**:
```bash
# Check API health
curl http://localhost:5000/

# Restart API
docker-compose restart api
```

### Token Expired

**Symptom**: "Invalid or expired token" error after some time

**Diagnosis**:
- Tokens expire after 24 hours
- Check token expiration in JWT payload

**Solutions**:

1. **Re-login**:
- Simply log out and log back in
- Token will be refreshed

2. **Extend Token Lifetime** (if needed):
```python
# api/config.py
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=48)  # Extend to 48 hours
```

### Session Lost

**Symptom**: Logged out unexpectedly

**Diagnosis**:
- Check browser console for errors
- Check if session state is cleared

**Solutions**:

1. **Browser Refresh**:
- Streamlit sessions are lost on page refresh
- Re-login after refresh

2. **Persistent Sessions** (future enhancement):
```python
# Store token in browser localStorage
# Requires custom Streamlit component
```

---

## Database Issues

### Connection Refused

**Symptom**: "Connection refused" or "could not connect to server"

**Diagnosis**:
```bash
# Check if database is running
docker-compose ps db

# Check database logs
docker-compose logs db

# Test connection
docker-compose exec db psql -U admin -d sitesteward -c "SELECT 1;"
```

**Solutions**:

1. **Database Not Running**:
```bash
# Start database
docker-compose up -d db

# Wait for database to be ready
docker-compose exec db pg_isready -U admin
```

2. **Wrong Connection String**:
```bash
# Check DATABASE_URL in .env
cat .env | grep DATABASE_URL

# Should be:
DATABASE_URL=postgresql://admin:password@db:5432/sitesteward
```

3. **Database Not Initialized**:
```bash
# Initialize database
docker-compose exec api python database/init_db.py
```

### Database Locked

**Symptom**: "database is locked" or "deadlock detected"

**Diagnosis**:
```bash
# Check active connections
docker-compose exec db psql -U admin -d sitesteward -c "SELECT * FROM pg_stat_activity;"
```

**Solutions**:

1. **Restart Database**:
```bash
docker-compose restart db
```

2. **Kill Blocking Queries**:
```sql
-- Find blocking queries
SELECT pid, query FROM pg_stat_activity WHERE state = 'active';

-- Kill specific query
SELECT pg_terminate_backend(pid);
```

### Data Corruption

**Symptom**: Unexpected data or errors when querying

**Diagnosis**:
```bash
# Check database integrity
docker-compose exec db psql -U admin -d sitesteward -c "VACUUM ANALYZE;"
```

**Solutions**:

1. **Restore from Backup**:
```bash
# Restore database
docker-compose exec -T db psql -U admin sitesteward < backup.sql
```

2. **Reset Database** (⚠️ Deletes all data):
```bash
docker-compose down -v
docker-compose up -d
make seed-db
```

---

## API Problems

### API Returns 500 Error

**Symptom**: Internal Server Error (500) responses

**Diagnosis**:
```bash
# Check API logs
docker-compose logs api | tail -50

# Check for Python errors
docker-compose logs api | grep "Traceback"
```

**Solutions**:

1. **Check Error Details**:
```bash
# View full error trace
docker-compose logs api
```

2. **Common Causes**:
- Database connection issues
- Missing environment variables
- Invalid data in request
- Code errors

3. **Restart API**:
```bash
docker-compose restart api
```

### API Returns 401 Unauthorized

**Symptom**: All requests return 401 even with token

**Diagnosis**:
```bash
# Test login endpoint
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Test with token
curl -X GET http://localhost:5000/api/assets \
  -H "Authorization: Bearer <token>"
```

**Solutions**:

1. **Invalid Token**:
- Token may be expired
- Token may be malformed
- Re-login to get new token

2. **JWT_SECRET Mismatch**:
```bash
# Check JWT_SECRET is set
docker-compose exec api printenv JWT_SECRET

# Restart API after changing JWT_SECRET
docker-compose restart api
```

### API Slow Response

**Symptom**: API requests take a long time

**Diagnosis**:
```bash
# Check API logs for slow queries
docker-compose logs api | grep "slow"

# Monitor database performance
docker-compose exec db psql -U admin -d sitesteward -c "SELECT * FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10;"
```

**Solutions**:

1. **Database Optimization**:
```sql
-- Add indexes
CREATE INDEX idx_asset_project ON assets(project_id);
CREATE INDEX idx_compliance_expiry ON compliance_documents(expiry_date);

-- Analyze tables
VACUUM ANALYZE;
```

2. **Increase Resources**:
```yaml
# docker-compose.yml
services:
  api:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
```

---

## Frontend Issues

### Streamlit App Not Loading

**Symptom**: Blank page or "Please wait..." message

**Diagnosis**:
```bash
# Check frontend logs
docker-compose logs admin_portal
docker-compose logs field_app

# Check browser console for errors
# Open browser DevTools (F12)
```

**Solutions**:

1. **Restart Frontend**:
```bash
docker-compose restart admin_portal
docker-compose restart field_app
```

2. **Clear Browser Cache**:
- Hard refresh: Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac)
- Clear browser cache and cookies

3. **Check API Connection**:
```bash
# Verify API_URL in .env
cat .env | grep API_URL

# Should be accessible from frontend container
docker-compose exec admin_portal curl http://api:5000/
```

### UI Elements Not Responding

**Symptom**: Buttons don't work, forms don't submit

**Diagnosis**:
- Check browser console for JavaScript errors
- Check if Streamlit is in "disconnected" state

**Solutions**:

1. **Refresh Page**:
- Streamlit may have lost connection
- Refresh browser (F5)

2. **Check WebSocket Connection**:
- Streamlit uses WebSockets
- Check if WebSockets are blocked by firewall/proxy

3. **Restart Streamlit**:
```bash
docker-compose restart admin_portal
```

### Data Not Updating

**Symptom**: Changes not reflected in UI

**Diagnosis**:
- Check if API request succeeded
- Check browser network tab for failed requests

**Solutions**:

1. **Refresh Page**:
- Streamlit caches data
- Use st.rerun() or refresh browser

2. **Clear Cache**:
```python
# In Streamlit app
st.cache_data.clear()
```

---

## QR Code Scanning Problems

### Camera Not Working

**Symptom**: Camera doesn't activate or shows error

**Diagnosis**:
- Check browser console for errors
- Check camera permissions

**Solutions**:

1. **Grant Camera Permissions**:
- Browser will prompt for camera access
- Allow camera access in browser settings

2. **HTTPS Required**:
- Most browsers require HTTPS for camera access
- Use HTTPS in production
- For development, use localhost (allowed without HTTPS)

3. **Browser Compatibility**:
- Use Chrome 90+ or Safari 14+
- Some browsers don't support camera on HTTP

### QR Code Not Detected

**Symptom**: Camera works but QR code not recognized

**Diagnosis**:
- Check QR code quality
- Check lighting conditions

**Solutions**:

1. **Improve Lighting**:
- Ensure good lighting
- Avoid glare and shadows

2. **QR Code Quality**:
- Print QR codes at sufficient size (at least 2x2 inches)
- Ensure QR code is not damaged or dirty
- Regenerate QR code if needed

3. **Camera Distance**:
- Hold phone 6-12 inches from QR code
- Ensure QR code fills most of camera view

4. **Camera Focus**:
- Tap screen to focus (on mobile)
- Keep phone steady while scanning

---

## Email Notification Issues

### Emails Not Sending

**Symptom**: Compliance check script runs but no emails received

**Diagnosis**:
```bash
# Run compliance check manually
docker-compose exec api python scripts/check_expiry.py

# Check for SMTP errors in output
```

**Solutions**:

1. **SMTP Not Configured**:
```bash
# Check SMTP settings in .env
cat .env | grep SMTP

# Required variables:
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=noreply@sitesteward.com
ALERT_EMAIL_RECIPIENTS=admin@example.com
```

2. **Gmail App Password**:
- Regular Gmail password won't work
- Generate App Password: https://myaccount.google.com/apppasswords
- Use App Password as SMTP_PASSWORD

3. **Firewall Blocking**:
```bash
# Check if port 587 is open
telnet smtp.gmail.com 587

# Allow outbound SMTP
sudo ufw allow out 587/tcp
```

### Emails Going to Spam

**Symptom**: Emails sent but arrive in spam folder

**Solutions**:

1. **Configure SPF/DKIM**:
- Add SPF record to DNS
- Configure DKIM signing
- Use reputable SMTP service (SendGrid, Mailgun)

2. **Improve Email Content**:
- Use professional from address
- Include unsubscribe link
- Avoid spam trigger words

---

## Performance Problems

### High CPU Usage

**Symptom**: System slow, high CPU usage

**Diagnosis**:
```bash
# Check container resource usage
docker stats

# Check processes
docker-compose exec api top
```

**Solutions**:

1. **Limit Container Resources**:
```yaml
# docker-compose.yml
services:
  api:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
```

2. **Optimize Queries**:
- Add database indexes
- Use eager loading
- Implement pagination

### High Memory Usage

**Symptom**: Out of memory errors

**Diagnosis**:
```bash
# Check memory usage
docker stats

# Check for memory leaks
docker-compose logs api | grep "MemoryError"
```

**Solutions**:

1. **Increase Memory Limit**:
```yaml
# docker-compose.yml
services:
  api:
    deploy:
      resources:
        limits:
          memory: 2G
```

2. **Optimize Code**:
- Close database sessions
- Clear caches
- Avoid loading large datasets

### Disk Space Full

**Symptom**: "No space left on device" errors

**Diagnosis**:
```bash
# Check disk usage
df -h

# Check Docker disk usage
docker system df
```

**Solutions**:

1. **Clean Up Docker**:
```bash
# Remove unused containers, images, volumes
docker system prune -a

# Remove old backups
find /backups -name "backup_*.sql" -mtime +30 -delete
```

2. **Increase Disk Space**:
- Add more storage
- Move uploads to external storage (S3)

---

## Docker Issues

### Docker Daemon Not Running

**Symptom**: "Cannot connect to Docker daemon"

**Solutions**:

1. **Start Docker**:
```bash
# Windows: Start Docker Desktop
# Linux:
sudo systemctl start docker

# Mac: Start Docker Desktop
```

2. **Check Docker Status**:
```bash
docker info
```

### Permission Denied

**Symptom**: "Permission denied" when running Docker commands

**Solutions**:

1. **Add User to Docker Group** (Linux):
```bash
sudo usermod -aG docker $USER
newgrp docker
```

2. **Use sudo** (temporary):
```bash
sudo docker-compose up
```

### Image Build Fails

**Symptom**: Docker build fails with errors

**Diagnosis**:
```bash
# Check build logs
docker-compose build --no-cache

# Check Dockerfile syntax
docker-compose config
```

**Solutions**:

1. **Clear Build Cache**:
```bash
docker-compose build --no-cache
```

2. **Check Dockerfile**:
- Verify base image exists
- Check for syntax errors
- Ensure all files are accessible

---

## Getting Help

### Diagnostic Information

When reporting issues, include:

```bash
# System information
uname -a
docker --version
docker-compose --version

# Service status
docker-compose ps

# Recent logs
docker-compose logs --tail=100

# Environment (sanitized)
cat .env | grep -v PASSWORD | grep -v SECRET
```

### Log Collection

```bash
# Collect all logs
docker-compose logs > logs.txt

# Collect specific service logs
docker-compose logs api > api_logs.txt
docker-compose logs db > db_logs.txt
```

### Support Channels

- **Documentation**: Check all documentation files
- **GitHub Issues**: Report bugs and feature requests
- **Email Support**: support@yourdomain.com
- **Community Forum**: forum.yourdomain.com

### Before Asking for Help

1. Check this troubleshooting guide
2. Search existing issues
3. Try basic troubleshooting steps
4. Collect diagnostic information
5. Provide clear description of problem

---

## Quick Reference

### Restart Everything

```bash
docker-compose restart
```

### Reset Everything (⚠️ Deletes all data)

```bash
docker-compose down -v
docker-compose up -d
make seed-db
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api
```

### Check Service Health

```bash
# API
curl http://localhost:5000/

# Database
docker-compose exec db pg_isready -U admin

# All services
docker-compose ps
```

---

## Related Documentation
- [System Overview](01_SYSTEM_OVERVIEW.md)
- [Deployment Guide](05_DEPLOYMENT_GUIDE.md)
- [User Guide](06_USER_GUIDE.md)
- [Security Guide](08_SECURITY.md)
