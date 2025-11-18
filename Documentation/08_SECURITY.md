# Site-Steward MVP - Security Guide

## Table of Contents
1. [Security Overview](#security-overview)
2. [Authentication & Authorization](#authentication--authorization)
3. [Data Security](#data-security)
4. [Network Security](#network-security)
5. [Application Security](#application-security)
6. [Compliance & Best Practices](#compliance--best-practices)
7. [Security Checklist](#security-checklist)

## Security Overview

Site-Steward implements multiple layers of security to protect sensitive data and ensure system integrity.

### Security Principles

1. **Defense in Depth**: Multiple security layers
2. **Least Privilege**: Minimum necessary access
3. **Secure by Default**: Security-first configuration
4. **Data Protection**: Encryption and secure storage
5. **Audit Trail**: Complete activity logging

### Threat Model

**Protected Assets**:
- User credentials and authentication tokens
- Compliance documents (PDFs)
- Asset location and movement data
- Subcontractor information
- Project details

**Potential Threats**:
- Unauthorized access to admin functions
- Data breaches and information disclosure
- SQL injection attacks
- Cross-site scripting (XSS)
- Man-in-the-middle attacks
- Brute force password attacks
- File upload vulnerabilities

---

## Authentication & Authorization

### JWT-Based Authentication

#### Token Structure

```json
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "sub": "user-id-uuid",
    "role": "admin",
    "user_id": "user-id-uuid",
    "exp": 1700000000,
    "iat": 1699913600
  },
  "signature": "..."
}
```

#### Token Security

**Token Generation**:
```python
# Strong secret key (32+ characters)
JWT_SECRET = os.getenv('JWT_SECRET')  # Never hardcode!

# Token expiration (24 hours)
access_token = create_access_token(
    identity=user.id,
    additional_claims={'role': user.role},
    expires_delta=timedelta(hours=24)
)
```

**Token Validation**:
```python
@jwt_required_custom()
def protected_route():
    # Token automatically validated
    user_id = get_jwt_identity()
    return {'user_id': user_id}
```

**Best Practices**:
- ✅ Use strong, random JWT_SECRET (32+ characters)
- ✅ Set appropriate token expiration (24 hours)
- ✅ Validate tokens on every request
- ✅ Include minimal claims in token
- ❌ Never store sensitive data in JWT payload
- ❌ Never share JWT_SECRET in code or logs

### Password Security

#### Password Hashing

```python
import bcrypt

# Hash password with salt
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

# Verify password
def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(
        password.encode('utf-8'),
        password_hash.encode('utf-8')
    )
```

**Password Requirements**:
- Minimum 8 characters
- Mix of uppercase and lowercase
- Include numbers
- Include special characters
- No common passwords
- No username in password

**Implementation**:
```python
def validate_password(password: str) -> bool:
    if len(password) < 8:
        return False
    if not any(c.isupper() for c in password):
        return False
    if not any(c.islower() for c in password):
        return False
    if not any(c.isdigit() for c in password):
        return False
    return True
```

### Role-Based Access Control (RBAC)

#### Role Definitions

**Admin Role**:
- Full system access
- Manage users, assets, projects, subcontractors
- Upload compliance documents
- View all data
- System configuration

**Foreman Role**:
- Field operations only
- Scan QR codes
- Move assets
- View compliance status
- No administrative functions

#### Implementation

```python
@role_required('admin')
def admin_only_route():
    return {'message': 'Admin access granted'}

@role_required('admin', 'foreman')
def multi_role_route():
    return {'message': 'Access granted'}
```

### Session Management

**Session Security**:
- Tokens stored in session state (not localStorage)
- Automatic logout on token expiration
- No persistent sessions
- Session timeout after inactivity

**Implementation**:
```python
# Streamlit session management
if 'token' in st.session_state:
    # Validate token
    if api.validate_token():
        # Token valid, continue
        pass
    else:
        # Token invalid, logout
        logout()
```

---

## Data Security

### Database Security

#### Connection Security

```python
# Use environment variables for credentials
DATABASE_URL = os.getenv('DATABASE_URL')

# Never hardcode credentials
# ❌ BAD
DATABASE_URL = "postgresql://admin:password@localhost/db"

# ✅ GOOD
DATABASE_URL = os.getenv('DATABASE_URL')
```

#### SQL Injection Prevention

```python
# ✅ GOOD: Use ORM (parameterized queries)
asset = db.query(AssetORM).filter(AssetORM.id == asset_id).first()

# ❌ BAD: String concatenation
query = f"SELECT * FROM assets WHERE id = '{asset_id}'"
```

#### Data Encryption

**At Rest**:
- PostgreSQL supports encryption at rest
- Enable with: `ALTER DATABASE sitesteward SET encryption = on;`
- Use encrypted volumes for database storage

**In Transit**:
- Use SSL/TLS for database connections
- Configure in connection string:
```python
DATABASE_URL = "postgresql://user:pass@host/db?sslmode=require"
```

### File Upload Security

#### Validation

```python
ALLOWED_EXTENSIONS = {'pdf'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_file_size(file):
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    return size <= MAX_FILE_SIZE
```

#### Secure File Storage

```python
from werkzeug.utils import secure_filename

# Generate secure filename
timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
original_filename = secure_filename(file.filename)
filename = f"{subcontractor_id}_{document_type}_{timestamp}_{original_filename}"

# Store outside web root
UPLOAD_FOLDER = "/app/uploads/compliance"
file_path = os.path.join(UPLOAD_FOLDER, filename)
```

**Best Practices**:
- ✅ Validate file type and size
- ✅ Use secure_filename() to sanitize names
- ✅ Store files outside web root
- ✅ Generate unique filenames
- ✅ Scan files for malware (if possible)
- ❌ Never execute uploaded files
- ❌ Never trust user-provided filenames

### Sensitive Data Handling

#### Environment Variables

```bash
# .env file (never commit to git!)
POSTGRES_PASSWORD=strong_random_password
JWT_SECRET=strong_random_secret_key
SMTP_PASSWORD=smtp_password

# Add to .gitignore
echo ".env" >> .gitignore
```

#### Secrets Management

**Development**:
- Use .env files
- Never commit secrets to git
- Use different secrets per environment

**Production**:
- Use secrets management service:
  - AWS Secrets Manager
  - Azure Key Vault
  - HashiCorp Vault
  - Docker Secrets

**Example with Docker Secrets**:
```yaml
# docker-compose.yml
services:
  api:
    secrets:
      - db_password
      - jwt_secret

secrets:
  db_password:
    external: true
  jwt_secret:
    external: true
```

---

## Network Security

### HTTPS/TLS Configuration

#### SSL Certificate Setup

```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    # SSL certificates
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;

    # SSL protocols and ciphers
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # HSTS
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Other security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
}
```

### Firewall Configuration

```bash
# Allow only necessary ports
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP (redirect to HTTPS)
sudo ufw allow 443/tcp  # HTTPS

# Deny all other incoming
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Enable firewall
sudo ufw enable
```

### Docker Network Isolation

```yaml
# docker-compose.yml
networks:
  internal:
    driver: bridge
    internal: true  # No external access
  external:
    driver: bridge

services:
  db:
    networks:
      - internal  # Database not exposed externally

  api:
    networks:
      - internal  # Can access database
      - external  # Can be accessed externally
```

### CORS Configuration

```python
from flask_cors import CORS

app = Flask(__name__)

# Production CORS configuration
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://yourdomain.com"],
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"],
        "expose_headers": ["Content-Type"],
        "supports_credentials": True,
        "max_age": 3600
    }
})
```

---

## Application Security

### Input Validation

```python
def validate_asset_input(data):
    """Validate asset creation input."""
    errors = []
    
    # Required fields
    if not data.get('name'):
        errors.append("Name is required")
    if not data.get('category'):
        errors.append("Category is required")
    
    # Length validation
    if len(data.get('name', '')) > 255:
        errors.append("Name too long (max 255 characters)")
    
    # Allowed values
    allowed_categories = ['Heavy Equipment', 'Power Equipment', 'Safety Equipment']
    if data.get('category') not in allowed_categories:
        errors.append(f"Invalid category. Allowed: {allowed_categories}")
    
    return errors

# Usage
errors = validate_asset_input(request.get_json())
if errors:
    return jsonify({"errors": errors}), 400
```

### Error Handling

```python
# ✅ GOOD: Generic error messages
try:
    user = authenticate(username, password)
except Exception:
    return jsonify({"error": "Invalid credentials"}), 401

# ❌ BAD: Detailed error messages
try:
    user = authenticate(username, password)
except UserNotFound:
    return jsonify({"error": "User not found"}), 401
except InvalidPassword:
    return jsonify({"error": "Password incorrect"}), 401
```

### Logging and Monitoring

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Log security events
logger.info(f"User {user_id} logged in successfully")
logger.warning(f"Failed login attempt for username: {username}")
logger.error(f"Unauthorized access attempt to {endpoint}")

# ❌ Never log sensitive data
# logger.info(f"Password: {password}")  # BAD!
# logger.info(f"Token: {token}")  # BAD!
```

### Rate Limiting

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route("/api/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():
    # Login logic
    pass
```

---

## Compliance & Best Practices

### OWASP Top 10 Mitigation

1. **Injection**: Use ORM, parameterized queries
2. **Broken Authentication**: JWT with expiration, strong passwords
3. **Sensitive Data Exposure**: HTTPS, encrypted storage
4. **XML External Entities**: Not applicable (no XML processing)
5. **Broken Access Control**: RBAC implementation
6. **Security Misconfiguration**: Secure defaults, regular updates
7. **XSS**: Input validation, output encoding
8. **Insecure Deserialization**: Validate all inputs
9. **Using Components with Known Vulnerabilities**: Regular updates
10. **Insufficient Logging**: Comprehensive logging

### Security Auditing

#### Regular Security Checks

```bash
# Check for vulnerable dependencies
pip install safety
safety check

# Scan for security issues
pip install bandit
bandit -r api/ services/ database/

# Check Docker images
docker scan sitesteward-api:latest
```

#### Penetration Testing

- Regular security assessments
- Automated vulnerability scanning
- Manual penetration testing
- Third-party security audits

### Incident Response

#### Security Incident Procedure

1. **Detection**: Monitor logs and alerts
2. **Containment**: Isolate affected systems
3. **Investigation**: Determine scope and impact
4. **Remediation**: Fix vulnerabilities
5. **Recovery**: Restore normal operations
6. **Post-Incident**: Document and improve

#### Breach Notification

- Notify affected users within 72 hours
- Document incident details
- Implement corrective measures
- Update security procedures

---

## Security Checklist

### Pre-Deployment

- [ ] Change all default passwords
- [ ] Generate strong JWT_SECRET
- [ ] Configure HTTPS/SSL
- [ ] Set up firewall rules
- [ ] Enable database encryption
- [ ] Configure secure CORS
- [ ] Implement rate limiting
- [ ] Set up logging and monitoring
- [ ] Review all environment variables
- [ ] Scan for vulnerabilities

### Post-Deployment

- [ ] Monitor logs regularly
- [ ] Review access logs
- [ ] Check for failed login attempts
- [ ] Update dependencies regularly
- [ ] Perform security audits
- [ ] Test backup and recovery
- [ ] Review user permissions
- [ ] Monitor system resources

### Ongoing Maintenance

- [ ] Weekly: Review security logs
- [ ] Monthly: Update dependencies
- [ ] Quarterly: Security audit
- [ ] Annually: Penetration testing
- [ ] Continuous: Monitor alerts

---

## Security Contacts

**Report Security Issues**:
- Email: security@yourdomain.com
- PGP Key: [Public key for encrypted communication]

**Response Time**:
- Critical: 4 hours
- High: 24 hours
- Medium: 1 week
- Low: 1 month

---

## Related Documentation
- [System Overview](01_SYSTEM_OVERVIEW.md)
- [Architecture](02_ARCHITECTURE.md)
- [Deployment Guide](05_DEPLOYMENT_GUIDE.md)
- [Troubleshooting](09_TROUBLESHOOTING.md)
