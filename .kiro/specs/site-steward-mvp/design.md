# Design Document

## Overview

The Site-Steward MVP implements a decoupled, service-oriented architecture with a Flask API backend, two Streamlit frontends, and a PostgreSQL database. The design prioritizes rapid development, clear separation of concerns, and low initial cost while establishing a foundation for future scaling.

## Architecture

### High-Level Architecture

```
┌─────────────────┐         ┌─────────────────┐
│  Admin Portal   │         │   Field App     │
│   (Streamlit)   │         │   (Streamlit)   │
└────────┬────────┘         └────────┬────────┘
         │                           │
         │      HTTP/JSON (JWT)      │
         └───────────┬───────────────┘
                     │
              ┌──────▼──────┐
              │  Flask API  │
              │   (REST)    │
              └──────┬──────┘
                     │
         ┌───────────┴───────────┐
         │                       │
    ┌────▼────┐          ┌──────▼──────┐
    │PostgreSQL│          │  File       │
    │ Database │          │  Storage    │
    └─────────┘          └─────────────┘
         ▲
         │
    ┌────┴────────┐
    │ Compliance  │
    │ Check Script│
    └─────────────┘
```

### Technology Stack

- **Backend**: Flask 3.x, SQLAlchemy 2.x, Flask-Smorest, Flask-JWT-Extended
- **Frontend**: Streamlit 1.x, streamlit-webrtc, pyzbar, qrcode
- **Database**: PostgreSQL 15+
- **Authentication**: JWT (JSON Web Tokens)
- **Deployment**: Docker, Docker Compose

## Components and Interfaces

### 1. Backend API (Flask)

#### 1.1 Application Structure

```
api/
├── app.py                 # Flask app factory
├── config.py              # Configuration management
├── routes/
│   ├── auth.py           # Authentication endpoints
│   ├── assets.py         # Asset management endpoints
│   ├── projects.py       # Project management endpoints
│   └── subcontractors.py # Subcontractor endpoints
└── middleware/
    └── auth.py           # JWT authentication middleware
```

#### 1.2 API Endpoints

**Authentication**
- `POST /api/login` - Authenticate user, return JWT
  - Request: `{username, password}`
  - Response: `{token, user_id, role}`

**Assets**
- `GET /api/assets` - List all assets
  - Response: `[{id, name, category, project_id, project_name}]`
- `POST /api/assets` - Create new asset
  - Request: `{name, category}`
  - Response: `{id, name, category, qr_code_url}`
- `GET /api/assets/<asset_id>` - Get asset details
  - Response: `{id, name, category, project_id, project_name, history}`
- `POST /api/assets/<asset_id>/move` - Move asset to project
  - Request: `{project_id}`
  - Response: `{success, message}`

**Projects**
- `GET /api/projects` - List all projects
  - Response: `[{id, name, location, asset_count}]`
- `POST /api/projects` - Create new project
  - Request: `{name, location}`
  - Response: `{id, name, location}`
- `GET /api/projects/<project_id>/compliance` - Get compliance status
  - Response: `{project_id, subcontractors: [{id, name, status, expiry_date}]}`

**Subcontractors**
- `GET /api/subcontractors` - List all subcontractors
  - Response: `[{id, name, email, phone}]`
- `POST /api/subcontractors` - Create new subcontractor
  - Request: `{name, email, phone}`
  - Response: `{id, name, email, phone}`
- `POST /api/subcontractors/<sub_id>/document` - Upload compliance document
  - Request: `multipart/form-data {file, expiry_date, document_type}`
  - Response: `{id, file_path, expiry_date, status}`

#### 1.3 Authentication Flow

1. User submits credentials to `/api/login`
2. API validates credentials against database
3. If valid, generate JWT with user_id and role
4. Return JWT to client
5. Client stores JWT in session state
6. Client includes JWT in Authorization header: `Bearer <token>`
7. API middleware validates JWT on protected routes

#### 1.4 File Handling

- PDF uploads stored in `uploads/compliance/` directory
- File naming: `{subcontractor_id}_{document_type}_{timestamp}.pdf`
- Database stores relative file path
- API serves files via protected endpoint (future enhancement)

### 2. Database Schema

#### 2.1 Tables

**users**
```sql
CREATE TABLE users (
    id VARCHAR PRIMARY KEY,
    username VARCHAR UNIQUE NOT NULL,
    password_hash VARCHAR NOT NULL,
    role VARCHAR NOT NULL,  -- 'admin' or 'foreman'
    email VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**assets**
```sql
CREATE TABLE assets (
    id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    category VARCHAR NOT NULL,
    project_id VARCHAR REFERENCES projects(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**projects**
```sql
CREATE TABLE projects (
    id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    location VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**subcontractors**
```sql
CREATE TABLE subcontractors (
    id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    email VARCHAR,
    phone VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**compliance_documents**
```sql
CREATE TABLE compliance_documents (
    id VARCHAR PRIMARY KEY,
    subcontractor_id VARCHAR REFERENCES subcontractors(id),
    document_type VARCHAR NOT NULL,
    file_path VARCHAR NOT NULL,
    expiry_date DATE NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**project_subcontractors** (junction table)
```sql
CREATE TABLE project_subcontractors (
    project_id VARCHAR REFERENCES projects(id),
    subcontractor_id VARCHAR REFERENCES subcontractors(id),
    PRIMARY KEY (project_id, subcontractor_id)
);
```

**asset_history** (for tracking movements)
```sql
CREATE TABLE asset_history (
    id VARCHAR PRIMARY KEY,
    asset_id VARCHAR REFERENCES assets(id),
    project_id VARCHAR REFERENCES projects(id),
    moved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    moved_by VARCHAR REFERENCES users(id)
);
```

### 3. Admin Portal (Streamlit)

#### 3.1 Application Structure

```
admin_portal/
├── app.py                # Main Streamlit app
├── pages/
│   ├── 1_Assets.py       # Asset management
│   ├── 2_Projects.py     # Project management
│   ├── 3_Subcontractors.py  # Subcontractor CRUD
│   ├── 4_Compliance.py   # Document upload
│   └── 5_Dashboard.py    # Project hub
├── utils/
│   ├── api_client.py     # API communication
│   ├── auth.py           # Authentication helpers
│   └── qr_generator.py   # QR code generation
└── config.py             # Configuration
```

#### 3.2 Page Designs

**Login Page (app.py)**
- Username and password inputs
- Login button
- On success: store JWT in `st.session_state['token']`
- Redirect to Assets page

**Asset Management Page**
- Form to create new asset (name, category)
- On submit: POST to `/api/assets`
- Display generated QR code using `qrcode` library
- Show QR as image with download button
- Table of all assets with current locations

**Subcontractor Management Page**
- Form to add new subcontractor
- Table of existing subcontractors
- Edit/Delete buttons (inline forms)

**Compliance Upload Page**
- Dropdown to select subcontractor
- File uploader for PDF
- Date picker for expiry date
- Document type selector
- Upload button

**Project Hub Page**
- Dropdown to select project
- Display compliance status table
- Color-coded status: 🟢 GREEN / 🔴 RED
- Show expiry dates
- Filter options

### 4. Field Mobile App (Streamlit)

#### 4.1 Application Structure

```
field_app/
├── app.py                # Main app with navigation
├── pages/
│   ├── scan.py           # QR scanner page
│   └── compliance.py     # Compliance viewer
├── utils/
│   ├── api_client.py     # API communication
│   ├── auth.py           # Authentication
│   └── qr_scanner.py     # Camera and QR detection
└── config.py             # Configuration
```

#### 4.2 QR Scanning Implementation

**Technology**: streamlit-webrtc + pyzbar

**Flow**:
1. User clicks "Scan Asset" button
2. App initializes WebRTC video stream
3. Each video frame processed by pyzbar
4. When QR detected, extract asset ID
5. Call `GET /api/assets/<asset_id>`
6. Display asset details
7. Show "Move Asset" button
8. On move: show project selector, call POST endpoint

**Code Pattern**:
```python
from streamlit_webrtc import webrtc_streamer
from pyzbar import pyzbar
import cv2

def qr_scanner_callback(frame):
    img = frame.to_ndarray(format="bgr24")
    decoded = pyzbar.decode(img)
    if decoded:
        asset_id = decoded[0].data.decode()
        st.session_state['scanned_asset_id'] = asset_id
    return frame

webrtc_streamer(
    key="qr-scanner",
    video_frame_callback=qr_scanner_callback
)
```

#### 4.3 Mobile Optimization

- Minimal UI elements
- Large touch targets (buttons)
- Responsive layout
- Fast loading (minimal dependencies)
- Clear visual feedback

### 5. Compliance Check Script

#### 5.1 Implementation

**File**: `scripts/check_expiry.py`

**Execution**: Daily cron job at 8:00 AM

**Logic**:
```python
1. Connect to PostgreSQL using SQLAlchemy
2. Query: SELECT * FROM compliance_documents 
         WHERE expiry_date BETWEEN NOW() AND NOW() + INTERVAL '30 days'
3. For each document:
   - Get subcontractor details
   - Get associated projects
   - Compose email with details
   - Send via smtplib
4. Log results to file
```

**Email Configuration**:
- SMTP server: smtp.gmail.com:587
- Credentials from environment variables
- Email template with document details

**Cron Configuration**:
```
0 8 * * * /usr/bin/python3 /app/scripts/check_expiry.py >> /var/log/compliance_check.log 2>&1
```

## Data Models

### SQLAlchemy Models

**User Model**
```python
class User(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)
    email = Column(String)
```

**Asset Model**
```python
class Asset(Base):
    __tablename__ = 'assets'
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    project_id = Column(String, ForeignKey('projects.id'))
    project = relationship('Project', back_populates='assets')
    history = relationship('AssetHistory', back_populates='asset')
```

**Project Model**
```python
class Project(Base):
    __tablename__ = 'projects'
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String)
    assets = relationship('Asset', back_populates='project')
    subcontractors = relationship('Subcontractor', secondary='project_subcontractors')
```

**Subcontractor Model**
```python
class Subcontractor(Base):
    __tablename__ = 'subcontractors'
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String)
    phone = Column(String)
    documents = relationship('ComplianceDocument', back_populates='subcontractor')
    projects = relationship('Project', secondary='project_subcontractors')
```

**ComplianceDocument Model**
```python
class ComplianceDocument(Base):
    __tablename__ = 'compliance_documents'
    id = Column(String, primary_key=True)
    subcontractor_id = Column(String, ForeignKey('subcontractors.id'))
    document_type = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    expiry_date = Column(Date, nullable=False)
    subcontractor = relationship('Subcontractor', back_populates='documents')
```

## Error Handling

### API Error Responses

**Standard Error Format**:
```json
{
    "error": "Error type",
    "message": "Human-readable message",
    "status_code": 400
}
```

**Error Types**:
- 400 Bad Request: Invalid input data
- 401 Unauthorized: Missing or invalid JWT
- 404 Not Found: Resource doesn't exist
- 409 Conflict: Duplicate resource
- 500 Internal Server Error: Unexpected errors

### Frontend Error Handling

**Streamlit Error Display**:
- Use `st.error()` for user-facing errors
- Use `st.warning()` for validation issues
- Use `st.success()` for confirmations
- Log errors to console for debugging

**API Communication Errors**:
- Network errors: Display "Connection failed" message
- Timeout errors: Display "Request timed out" message
- Authentication errors: Redirect to login
- Validation errors: Display field-specific messages

## Testing Strategy

### Unit Tests

**Backend (pytest)**:
- Test each API endpoint with valid/invalid inputs
- Test authentication middleware
- Test database models and relationships
- Test compliance calculation logic
- Mock database for isolated tests

**Coverage Target**: 80% for core business logic

### Integration Tests

**API Integration**:
- Test complete user flows (create asset → move asset)
- Test authentication flow end-to-end
- Test file upload and storage
- Use test database

### Manual Testing

**Frontend Testing**:
- Test all Streamlit pages manually
- Test QR scanning on actual mobile devices
- Test responsive layout on different screen sizes
- Test error scenarios (network failures, invalid inputs)

**QR Scanning Prototype**:
- Build standalone QR scanner test app
- Test on iOS and Android devices
- Verify camera permissions
- Test in different lighting conditions

### Deployment Testing

**Docker Testing**:
- Build all containers
- Test with Docker Compose locally
- Verify environment variable configuration
- Test database migrations

## Security Considerations

### Authentication
- Passwords hashed using bcrypt
- JWT tokens expire after 24 hours
- Tokens include user role for authorization
- HTTPS required in production

### File Upload Security
- Validate file type (PDF only)
- Limit file size (10MB max)
- Sanitize filenames
- Store outside web root
- Scan for malware (future enhancement)

### Database Security
- Use parameterized queries (SQLAlchemy ORM)
- Principle of least privilege for database user
- Regular backups
- Connection pooling with limits

### API Security
- Rate limiting (future enhancement)
- CORS configuration for known origins
- Input validation on all endpoints
- SQL injection prevention via ORM

## Performance Considerations

### Database Optimization
- Index on frequently queried fields (asset.id, project.id)
- Connection pooling (max 20 connections)
- Lazy loading for relationships
- Pagination for large result sets (future)

### API Performance
- Response caching for static data (future)
- Gzip compression for responses
- Async file uploads (future)
- Database query optimization

### Frontend Performance
- Minimize API calls (cache in session state)
- Lazy load images
- Optimize QR code generation
- Debounce search inputs

## Deployment Architecture

### Docker Compose Setup

```yaml
version: '3.8'
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: sitesteward
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  api:
    build: ./api
    ports:
      - "5000:5000"
    environment:
      DATABASE_URL: postgresql://admin:${DB_PASSWORD}@db:5432/sitesteward
      JWT_SECRET: ${JWT_SECRET}
    depends_on:
      - db
  
  admin_portal:
    build: ./admin_portal
    ports:
      - "8501:8501"
    environment:
      API_URL: http://api:5000
  
  field_app:
    build: ./field_app
    ports:
      - "8502:8501"
    environment:
      API_URL: http://api:5000
```

### Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `JWT_SECRET`: Secret key for JWT signing
- `SMTP_HOST`: Email server host
- `SMTP_USER`: Email username
- `SMTP_PASSWORD`: Email password
- `API_URL`: Backend API URL for frontends

## Future Enhancements

### Post-MVP Features
- Cloud storage for PDFs (S3/Azure Blob)
- Advanced reporting and analytics
- Mobile native apps (React Native)
- Real-time notifications (WebSockets)
- Barcode scanning support
- Offline mode for field app
- Multi-tenancy support
- Advanced role-based access control
- Audit logging
- API rate limiting
- Automated testing pipeline
