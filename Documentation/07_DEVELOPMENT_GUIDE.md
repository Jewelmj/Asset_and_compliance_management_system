# Site-Steward MVP - Development Guide

## Table of Contents
1. [Development Environment Setup](#development-environment-setup)
2. [Project Structure](#project-structure)
3. [Development Workflow](#development-workflow)
4. [Testing](#testing)
5. [Code Style and Standards](#code-style-and-standards)
6. [Contributing](#contributing)

## Development Environment Setup

### Prerequisites

- Python 3.9+
- Docker 20.10+
- Docker Compose 2.0+
- Git
- Code editor (VS Code recommended)

### Local Setup Without Docker

#### 1. Clone Repository

```bash
git clone <repository-url>
cd Asset_and_compliance_management_system
```

#### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Set Up PostgreSQL

```bash
# Install PostgreSQL (if not already installed)
# On Ubuntu:
sudo apt-get install postgresql postgresql-contrib

# On macOS:
brew install postgresql

# Create database
createdb sitesteward

# Create user
psql -c "CREATE USER admin WITH PASSWORD 'password';"
psql -c "GRANT ALL PRIVILEGES ON DATABASE sitesteward TO admin;"
```

#### 5. Configure Environment

```bash
# Create .env file
cp .env.example .env

# Edit .env
DATABASE_URL=postgresql://admin:password@localhost:5432/sitesteward
JWT_SECRET=dev_secret_key
FLASK_ENV=development
```

#### 6. Initialize Database

```bash
python database/init_db.py --seed
```

#### 7. Run Services

```bash
# Terminal 1: Run API
cd api
python app.py

# Terminal 2: Run Admin Portal
cd admin_portal
streamlit run app.py --server.port 8501

# Terminal 3: Run Field App
cd field_app
streamlit run app.py --server.port 8502
```

### Development with Docker

```bash
# Build and start services
docker-compose up --build

# Or use development mode with hot-reload
make dev
```

### IDE Setup (VS Code)

#### Recommended Extensions

- Python (Microsoft)
- Pylance
- Docker
- GitLens
- SQLTools
- Thunder Client (API testing)

#### VS Code Settings

Create `.vscode/settings.json`:

```json
{
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "python.formatting.blackArgs": ["--line-length", "100"],
  "editor.formatOnSave": true,
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false,
  "[python]": {
    "editor.rulers": [100],
    "editor.tabSize": 4
  }
}
```

---

## Project Structure

```
Asset_and_compliance_management_system/
├── api/                          # Flask REST API
│   ├── app.py                   # Application factory
│   ├── config.py                # Configuration classes
│   ├── routes/                  # API endpoints
│   │   ├── auth.py             # Authentication routes
│   │   ├── assets.py           # Asset management routes
│   │   ├── projects.py         # Project management routes
│   │   └── subcontractors.py  # Subcontractor routes
│   ├── middleware/              # Middleware components
│   │   └── auth.py             # JWT authentication
│   └── Dockerfile              # API container definition
│
├── admin_portal/                # Admin web interface
│   ├── app.py                  # Main Streamlit app
│   ├── config.py               # Configuration
│   ├── pages/                  # Streamlit pages
│   │   ├── 1_Assets.py        # Asset management page
│   │   ├── 2_Subcontractors.py # Subcontractor page
│   │   ├── 3_Compliance.py    # Document upload page
│   │   └── 4_Project_Hub.py   # Compliance dashboard
│   ├── utils/                  # Utility modules
│   │   ├── auth.py            # Authentication helpers
│   │   └── api_client.py      # API client
│   └── Dockerfile             # Admin portal container
│
├── field_app/                   # Field mobile interface
│   ├── app.py                  # Main Streamlit app
│   ├── config.py               # Configuration
│   ├── pages/                  # Streamlit pages
│   │   ├── scan_asset.py      # QR scanner page
│   │   └── view_compliance.py # Compliance viewer
│   ├── utils/                  # Utility modules
│   │   ├── auth.py            # Authentication helpers
│   │   ├── api_client.py      # API client
│   │   └── qr_scanner.py      # QR scanning utilities
│   └── Dockerfile             # Field app container
│
├── database/                    # Database layer
│   ├── db.py                   # Database connection
│   ├── models.py               # SQLAlchemy ORM models
│   ├── init_db.py              # Initialization script
│   └── README.md               # Database documentation
│
├── services/                    # Business logic services
│   └── compliance_service.py   # Compliance calculations
│
├── scripts/                     # Utility scripts
│   ├── check_expiry.py         # Compliance check script
│   └── verify_seed_data.py     # Data verification script
│
├── uploads/                     # File storage
│   └── compliance/             # Compliance documents
│
├── Documentation/               # Project documentation
│   ├── 01_SYSTEM_OVERVIEW.md
│   ├── 02_ARCHITECTURE.md
│   ├── 03_API_REFERENCE.md
│   ├── 04_DATABASE_SCHEMA.md
│   ├── 05_DEPLOYMENT_GUIDE.md
│   ├── 06_USER_GUIDE.md
│   ├── 07_DEVELOPMENT_GUIDE.md
│   ├── 08_SECURITY.md
│   └── 09_TROUBLESHOOTING.md
│
├── docker-compose.yml           # Docker Compose configuration
├── docker-compose.dev.yml       # Development overrides
├── requirements.txt             # Python dependencies
├── Makefile                     # Common commands
├── .env.example                 # Environment template
├── .gitignore                   # Git ignore rules
└── README.md                    # Project README
```

---

## Development Workflow

### Creating a New Feature

#### 1. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

#### 2. Implement Feature

Follow the appropriate guide based on what you're adding:

**Adding a New API Endpoint**:

1. Create route function in appropriate file under `api/routes/`
2. Add authentication decorator if needed
3. Implement business logic
4. Add error handling
5. Update API documentation

Example:
```python
# api/routes/assets.py

@assets_bp.route("/<asset_id>/assign", methods=["POST"])
@jwt_required_custom()
def assign_asset_to_user(asset_id):
    """Assign an asset to a user."""
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        
        # Validation
        if not user_id:
            return jsonify({"error": "user_id is required"}), 400
        
        # Business logic
        db = next(get_db())
        asset = db.query(AssetORM).filter(AssetORM.id == asset_id).first()
        
        if not asset:
            return jsonify({"error": "Asset not found"}), 404
        
        # Update asset
        asset.assigned_user_id = user_id
        db.commit()
        
        return jsonify({"success": True}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
```

**Adding a New Database Model**:

1. Define model in `database/models.py`
2. Add relationships
3. Create migration (if using Alembic)
4. Update seed data if needed

Example:
```python
# database/models.py

class VehicleORM(Base):
    """Vehicle model for tracking company vehicles."""
    __tablename__ = "vehicles"
    
    id = Column(String, primary_key=True)
    make = Column(String, nullable=False)
    model = Column(String, nullable=False)
    license_plate = Column(String, unique=True)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    assets = relationship("AssetORM", back_populates="vehicle")
```

**Adding a New Streamlit Page**:

1. Create page file in `admin_portal/pages/` or `field_app/pages/`
2. Implement page logic
3. Add navigation link in main app
4. Test responsiveness

Example:
```python
# admin_portal/pages/5_Reports.py

import streamlit as st
from admin_portal.utils.api_client import APIClient

st.set_page_config(page_title="Reports", page_icon="📊")

st.title("📊 Reports")

# Check authentication
if not st.session_state.get('token'):
    st.error("Please login first")
    st.stop()

# Initialize API client
api = APIClient()

# Implement report logic
report_type = st.selectbox("Select Report", ["Asset Summary", "Compliance Status"])

if report_type == "Asset Summary":
    assets = api.get("assets")
    st.dataframe(assets)
```

#### 3. Test Feature

```bash
# Run tests
python -m pytest tests/

# Manual testing
# Start services and test manually
```

#### 4. Commit Changes

```bash
git add .
git commit -m "feat: add asset assignment to users"
```

#### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
# Create pull request on GitHub/GitLab
```

### Code Review Checklist

- [ ] Code follows project style guidelines
- [ ] All tests pass
- [ ] New features have tests
- [ ] Documentation updated
- [ ] No sensitive data in code
- [ ] Error handling implemented
- [ ] Logging added where appropriate
- [ ] Performance considered

---

## Testing

### Running Tests

```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_auth.py

# Run with coverage
python -m pytest --cov=api --cov=services

# Run with verbose output
python -m pytest -v
```

### Writing Tests

#### API Endpoint Tests

```python
# tests/test_assets.py

import pytest
from api.app import create_app
from database.db import SessionLocal
from database.models import AssetORM

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def auth_token(client):
    response = client.post('/api/login', json={
        'username': 'admin',
        'password': 'admin123'
    })
    return response.json['token']

def test_create_asset(client, auth_token):
    response = client.post('/api/assets', 
        headers={'Authorization': f'Bearer {auth_token}'},
        json={
            'name': 'Test Asset',
            'category': 'Test Category'
        }
    )
    assert response.status_code == 201
    assert 'id' in response.json

def test_list_assets(client, auth_token):
    response = client.get('/api/assets',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    assert response.status_code == 200
    assert isinstance(response.json, list)
```

#### Service Tests

```python
# tests/test_compliance_service.py

from datetime import datetime, timedelta
from services.compliance_service import ComplianceService

def test_calculate_status_green():
    expiry_date = datetime.now().date() + timedelta(days=60)
    status = ComplianceService.calculate_status(expiry_date)
    assert status == "GREEN"

def test_calculate_status_red():
    expiry_date = datetime.now().date() + timedelta(days=15)
    status = ComplianceService.calculate_status(expiry_date)
    assert status == "RED"

def test_calculate_status_expired():
    expiry_date = datetime.now().date() - timedelta(days=5)
    status = ComplianceService.calculate_status(expiry_date)
    assert status == "RED"
```

### Manual Testing

#### API Testing with cURL

```bash
# Login
TOKEN=$(curl -s -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  | jq -r '.token')

# Test endpoint
curl -X GET http://localhost:5000/api/assets \
  -H "Authorization: Bearer $TOKEN"
```

#### API Testing with Postman

1. Import API collection
2. Set environment variables
3. Run test suite
4. Review results

---

## Code Style and Standards

### Python Style Guide

Follow PEP 8 with these specifics:

- Line length: 100 characters
- Indentation: 4 spaces
- String quotes: Double quotes for strings, single for dict keys
- Imports: Grouped and sorted

### Code Formatting

```bash
# Format code with black
black --line-length 100 .

# Sort imports
isort .

# Lint code
pylint api/ services/ database/
```

### Naming Conventions

**Variables and Functions**:
```python
# Use snake_case
user_id = "123"
def get_asset_details():
    pass
```

**Classes**:
```python
# Use PascalCase
class AssetManager:
    pass

class ComplianceService:
    pass
```

**Constants**:
```python
# Use UPPER_SNAKE_CASE
MAX_FILE_SIZE = 10 * 1024 * 1024
DEFAULT_TIMEOUT = 30
```

**Database Models**:
```python
# Use PascalCase with ORM suffix
class AssetORM(Base):
    pass
```

### Documentation Standards

**Docstrings**:
```python
def calculate_status(expiry_date):
    """
    Calculate compliance status based on expiry date.
    
    Args:
        expiry_date (date): Document expiration date
        
    Returns:
        str: "RED" if expired or expiring within 30 days, "GREEN" otherwise
        
    Raises:
        ValueError: If expiry_date is None
        
    Example:
        >>> from datetime import datetime, timedelta
        >>> expiry = datetime.now().date() + timedelta(days=60)
        >>> calculate_status(expiry)
        'GREEN'
    """
    pass
```

**Comments**:
```python
# Good: Explain why, not what
# Calculate days until expiry to determine urgency level
days_until_expiry = (expiry_date - today).days

# Bad: Obvious comment
# Get the current date
today = datetime.now().date()
```

### Git Commit Messages

Follow conventional commits:

```
feat: add asset assignment feature
fix: resolve QR code scanning issue
docs: update API documentation
style: format code with black
refactor: simplify compliance calculation
test: add tests for asset movement
chore: update dependencies
```

---

## Contributing

### Getting Started

1. Fork the repository
2. Clone your fork
3. Create a feature branch
4. Make your changes
5. Run tests
6. Submit pull request

### Pull Request Process

1. Update documentation
2. Add tests for new features
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Request review from maintainers

### Code Review Guidelines

**For Reviewers**:
- Be constructive and respectful
- Focus on code quality and maintainability
- Check for security issues
- Verify tests are adequate
- Ensure documentation is updated

**For Contributors**:
- Respond to feedback promptly
- Make requested changes
- Keep pull requests focused
- Write clear commit messages

---

## Debugging

### API Debugging

```python
# Enable debug mode in Flask
app.run(debug=True)

# Add breakpoints
import pdb; pdb.set_trace()

# Use logging
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug("Debug message")
```

### Database Debugging

```python
# Enable SQL logging
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Inspect queries
from sqlalchemy import inspect
inspector = inspect(engine)
print(inspector.get_table_names())
```

### Streamlit Debugging

```python
# Use st.write for debugging
st.write("Debug:", variable)

# Use st.exception for errors
try:
    # code
except Exception as e:
    st.exception(e)
```

---

## Performance Optimization

### Database Optimization

```python
# Use eager loading
assets = db.query(AssetORM).options(
    joinedload(AssetORM.project)
).all()

# Use pagination
assets = db.query(AssetORM).limit(20).offset(page * 20).all()

# Add indexes
Index('idx_asset_project', AssetORM.project_id)
```

### API Optimization

```python
# Cache responses
from functools import lru_cache

@lru_cache(maxsize=100)
def get_project_compliance(project_id):
    # expensive operation
    pass

# Use connection pooling
engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20)
```

---

## Related Documentation
- [System Overview](01_SYSTEM_OVERVIEW.md)
- [Architecture](02_ARCHITECTURE.md)
- [API Reference](03_API_REFERENCE.md)
- [Database Schema](04_DATABASE_SCHEMA.md)
