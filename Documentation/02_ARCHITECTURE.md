# Site-Steward MVP - Architecture Documentation

## Table of Contents
1. [System Architecture](#system-architecture)
2. [Component Details](#component-details)
3. [Data Flow](#data-flow)
4. [Design Patterns](#design-patterns)
5. [Technology Decisions](#technology-decisions)

## System Architecture

### High-Level Architecture

Site-Steward follows a three-tier architecture pattern:

```
┌─────────────────────────────────────────────────────────────┐
│                  Presentation Tier                           │
│  ┌──────────────────────┐  ┌──────────────────────┐        │
│  │   Admin Portal       │  │   Field Mobile App   │        │
│  │   (Streamlit)        │  │   (Streamlit)        │        │
│  └──────────────────────┘  └──────────────────────┘        │
└─────────────────────────────────────────────────────────────┘
                          │
                    JWT over HTTP
                          │
┌─────────────────────────────────────────────────────────────┐
│                   Application Tier                           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Flask REST API                           │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐     │  │
│  │  │  Routes    │  │ Middleware │  │  Services  │     │  │
│  │  └────────────┘  └────────────┘  └────────────┘     │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                          │
                    SQLAlchemy ORM
                          │
┌─────────────────────────────────────────────────────────────┐
│                     Data Tier                                │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              PostgreSQL Database                      │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐     │  │
│  │  │   Tables   │  │   Indexes  │  │ Constraints│     │  │
│  │  └────────────┘  └────────────┘  └────────────┘     │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Presentation Tier

#### Admin Portal (Streamlit)
**Purpose**: Desktop-optimized interface for administrative tasks

**Components**:
- `app.py`: Main application entry point with authentication
- `pages/1_Assets.py`: Asset management and QR code generation
- `pages/2_Subcontractors.py`: Subcontractor CRUD operations
- `pages/3_Compliance.py`: Document upload interface
- `pages/4_Project_Hub.py`: Compliance dashboard with RED/GREEN indicators
- `utils/auth.py`: Authentication helpers and session management
- `utils/api_client.py`: HTTP client for API communication
- `config.py`: Configuration management

**Key Features**:
- Wide layout for desktop viewing
- Expanded sidebar navigation
- Multi-column layouts for data display
- File upload widgets for compliance documents
- QR code generation and download

**Technology Stack**:
- Streamlit 1.x
- Requests library for HTTP
- qrcode library for QR generation
- Pillow for image processing

#### Field Mobile App (Streamlit)
**Purpose**: Mobile-optimized interface for field operations

**Components**:
- `app.py`: Main application with simplified navigation
- `pages/scan_asset.py`: QR code scanner with camera access
- `pages/view_compliance.py`: Mobile compliance viewer
- `utils/auth.py`: Authentication helpers
- `utils/api_client.py`: HTTP client for API communication
- `utils/qr_scanner.py`: QR code scanning utilities
- `config.py`: Configuration management

**Key Features**:
- Centered layout for mobile viewing
- Collapsed sidebar by default
- Large touch targets for buttons
- Camera integration for QR scanning
- Simplified navigation flow

**Technology Stack**:
- Streamlit 1.x
- streamlit-webrtc for camera access
- pyzbar for QR code decoding
- OpenCV for image processing
- av for video streaming

### 2. Application Tier

#### Flask REST API

**Structure**:
```
api/
├── app.py                 # Application factory and configuration
├── config.py              # Configuration classes
├── routes/
│   ├── auth.py           # Authentication endpoints
│   ├── assets.py         # Asset management endpoints
│   ├── projects.py       # Project management endpoints
│   ├── subcontractors.py # Subcontractor endpoints
│   └── places.py         # Legacy endpoints (backward compatibility)
├── middleware/
│   └── auth.py           # JWT validation and authorization
└── __init__.py
```

**Routes Module**:

1. **auth.py** - Authentication
   - `POST /api/login`: User authentication and JWT generation
   - Password verification with bcrypt
   - Token generation with user_id and role claims

2. **assets.py** - Asset Management
   - `GET /api/assets`: List all assets
   - `POST /api/assets`: Create new asset
   - `GET /api/assets/<id>`: Get asset details with history
   - `POST /api/assets/<id>/move`: Move asset to project

3. **projects.py** - Project Management
   - `GET /api/projects`: List all projects
   - `POST /api/projects`: Create new project
   - `GET /api/projects/<id>/compliance`: Get compliance status

4. **subcontractors.py** - Subcontractor Management
   - `GET /api/subcontractors`: List all subcontractors
   - `POST /api/subcontractors`: Create new subcontractor
   - `POST /api/subcontractors/<id>/document`: Upload compliance document

**Middleware Module**:

1. **auth.py** - Authentication & Authorization
   - `jwt_required_custom()`: Decorator for protected routes
   - `role_required(*roles)`: Decorator for role-based access
   - `get_current_user_id()`: Extract user ID from JWT
   - `get_current_user_role()`: Extract user role from JWT
   - `get_current_user_claims()`: Get all JWT claims

**Services Module**:
```
services/
└── compliance_service.py  # Compliance status calculation
```

1. **ComplianceService**
   - `calculate_status(expiry_date)`: Calculate RED/GREEN status
   - `calculate_subcontractor_status(documents)`: Overall status

### 3. Data Tier

#### PostgreSQL Database

**Connection Management**:
```python
# database/db.py
- SessionLocal: SQLAlchemy session factory
- get_db(): Generator for request-scoped sessions
- init_db(): Create all tables
- reset_db(): Drop and recreate all tables
```

**ORM Models** (database/models.py):

1. **UserORM**: User accounts with authentication
2. **ProjectORM**: Construction projects
3. **AssetORM**: Equipment and tools
4. **SubcontractorORM**: Third-party contractors
5. **ComplianceDocumentORM**: PDF documents with expiry
6. **AssetHistoryORM**: Asset movement audit trail
7. **PlaceORM**: Legacy model for backward compatibility

**Relationships**:
- Projects ↔ Assets (One-to-Many)
- Projects ↔ Subcontractors (Many-to-Many via junction table)
- Subcontractors ↔ ComplianceDocuments (One-to-Many)
- Assets ↔ AssetHistory (One-to-Many)
- Users ↔ AssetHistory (One-to-Many)

### 4. Background Services

#### Compliance Check Script
**File**: `scripts/check_expiry.py`

**Purpose**: Automated monitoring of document expiry dates

**Functionality**:
1. Query documents expiring within 30 days
2. Format HTML email with document details
3. Send email notifications via SMTP
4. Log results to console

**Execution**:
- Manual: `python scripts/check_expiry.py`
- Scheduled: Daily via cron job
- Docker: `docker-compose exec api python scripts/check_expiry.py`

## Data Flow

### Authentication Flow

```
┌─────────┐                ┌─────────┐                ┌──────────┐
│ Client  │                │   API   │                │ Database │
└────┬────┘                └────┬────┘                └────┬─────┘
     │                          │                          │
     │ POST /api/login          │                          │
     │ {username, password}     │                          │
     ├─────────────────────────>│                          │
     │                          │                          │
     │                          │ Query user by username   │
     │                          ├─────────────────────────>│
     │                          │                          │
     │                          │ Return user record       │
     │                          │<─────────────────────────┤
     │                          │                          │
     │                          │ Verify password (bcrypt) │
     │                          │                          │
     │                          │ Generate JWT token       │
     │                          │ (user_id, role claims)   │
     │                          │                          │
     │ Return token, user_id,   │                          │
     │ role                     │                          │
     │<─────────────────────────┤                          │
     │                          │                          │
     │ Store token in session   │                          │
     │                          │                          │
```

### Asset Movement Flow

```
┌─────────┐                ┌─────────┐                ┌──────────┐
│ Field   │                │   API   │                │ Database │
│  App    │                │         │                │          │
└────┬────┘                └────┬────┘                └────┬─────┘
     │                          │                          │
     │ Scan QR Code             │                          │
     │ (asset_id extracted)     │                          │
     │                          │                          │
     │ GET /api/assets/{id}     │                          │
     │ Authorization: Bearer... │                          │
     ├─────────────────────────>│                          │
     │                          │                          │
     │                          │ Validate JWT token       │
     │                          │                          │
     │                          │ Query asset + history    │
     │                          ├─────────────────────────>│
     │                          │                          │
     │                          │ Return asset details     │
     │                          │<─────────────────────────┤
     │                          │                          │
     │ Display asset details    │                          │
     │<─────────────────────────┤                          │
     │                          │                          │
     │ User selects new project │                          │
     │                          │                          │
     │ POST /api/assets/{id}/move                          │
     │ {project_id}             │                          │
     ├─────────────────────────>│                          │
     │                          │                          │
     │                          │ Validate JWT token       │
     │                          │ Extract user_id          │
     │                          │                          │
     │                          │ Update asset.project_id  │
     │                          │ Insert asset_history     │
     │                          ├─────────────────────────>│
     │                          │                          │
     │                          │ Commit transaction       │
     │                          │<─────────────────────────┤
     │                          │                          │
     │ Success message          │                          │
     │<─────────────────────────┤                          │
     │                          │                          │
```

### Compliance Document Upload Flow

```
┌─────────┐                ┌─────────┐                ┌──────────┐
│ Admin   │                │   API   │                │ Database │
│ Portal  │                │         │                │          │
└────┬────┘                └────┬────┘                └────┬─────┘
     │                          │                          │
     │ Select subcontractor     │                          │
     │ Upload PDF file          │                          │
     │ Set expiry date          │                          │
     │                          │                          │
     │ POST /api/subcontractors/{id}/document              │
     │ multipart/form-data      │                          │
     │ - file: PDF              │                          │
     │ - expiry_date: YYYY-MM-DD│                          │
     │ - document_type: string  │                          │
     ├─────────────────────────>│                          │
     │                          │                          │
     │                          │ Validate JWT token       │
     │                          │                          │
     │                          │ Validate file type (PDF) │
     │                          │ Validate file size (<10MB)│
     │                          │                          │
     │                          │ Generate secure filename │
     │                          │ Save file to uploads/    │
     │                          │                          │
     │                          │ Insert compliance_document│
     │                          ├─────────────────────────>│
     │                          │                          │
     │                          │ Commit transaction       │
     │                          │<─────────────────────────┤
     │                          │                          │
     │                          │ Calculate status         │
     │                          │ (RED/GREEN)              │
     │                          │                          │
     │ Return document_id,      │                          │
     │ file_path, status        │                          │
     │<─────────────────────────┤                          │
     │                          │                          │
```

### Compliance Check Flow

```
┌─────────┐                ┌──────────┐                ┌──────────┐
│  Cron   │                │ Database │                │   SMTP   │
│  Job    │                │          │                │  Server  │
└────┬────┘                └────┬─────┘                └────┬─────┘
     │                          │                          │
     │ Execute check_expiry.py  │                          │
     │                          │                          │
     │ Query documents where    │                          │
     │ expiry_date <= today+30  │                          │
     ├─────────────────────────>│                          │
     │                          │                          │
     │ Return expiring docs     │                          │
     │<─────────────────────────┤                          │
     │                          │                          │
     │ For each document:       │                          │
     │ - Get subcontractor      │                          │
     │ - Get associated projects│                          │
     │ - Calculate status       │                          │
     │                          │                          │
     │ Format HTML email        │                          │
     │                          │                          │
     │ Send email notification  │                          │
     ├──────────────────────────┼─────────────────────────>│
     │                          │                          │
     │                          │ Deliver email            │
     │<─────────────────────────┼──────────────────────────┤
     │                          │                          │
     │ Log results              │                          │
     │                          │                          │
```

## Design Patterns

### 1. Repository Pattern
**Implementation**: SQLAlchemy ORM acts as repository layer
**Benefits**: 
- Abstraction of data access logic
- Easy to test with mock repositories
- Database-agnostic queries

### 2. Dependency Injection
**Implementation**: `get_db()` generator for database sessions
**Benefits**:
- Request-scoped sessions
- Automatic cleanup
- Testability

### 3. Decorator Pattern
**Implementation**: `@jwt_required_custom()` and `@role_required()`
**Benefits**:
- Reusable authentication logic
- Clean separation of concerns
- Easy to apply to multiple routes

### 4. Factory Pattern
**Implementation**: `create_app()` function in Flask
**Benefits**:
- Configurable application instances
- Easy testing with different configurations
- Blueprint registration

### 5. Service Layer Pattern
**Implementation**: `ComplianceService` for business logic
**Benefits**:
- Separation of business logic from routes
- Reusable across multiple endpoints
- Easier to test

### 6. API Client Pattern
**Implementation**: `APIClient` class in frontend apps
**Benefits**:
- Centralized HTTP logic
- Consistent error handling
- Token management

## Technology Decisions

### Why Flask?
- Lightweight and flexible
- Excellent for REST APIs
- Strong ecosystem (JWT, SQLAlchemy)
- Easy to deploy and scale

### Why Streamlit?
- Rapid development of data-driven UIs
- Python-based (consistent with backend)
- Built-in session management
- Easy deployment

### Why PostgreSQL?
- ACID compliance for data integrity
- Excellent support for relationships
- JSON support for future extensibility
- Proven reliability

### Why JWT?
- Stateless authentication
- Scalable (no server-side sessions)
- Standard format (RFC 7519)
- Easy to implement and validate

### Why Docker?
- Consistent environments
- Easy deployment
- Service isolation
- Simplified dependency management

### Why SQLAlchemy?
- Pythonic ORM
- Database-agnostic
- Excellent relationship handling
- Migration support (Alembic)

## Performance Considerations

### Database Optimization
- Indexes on foreign keys
- Indexes on username (unique)
- Connection pooling via SQLAlchemy
- Query optimization with eager loading

### API Optimization
- JWT validation caching
- Database session per request
- Efficient query patterns
- Minimal data transfer

### Frontend Optimization
- Session state caching
- Lazy loading of data
- Efficient re-rendering
- Image optimization for QR codes

## Security Architecture

### Authentication Layer
- JWT with expiration (24 hours)
- Bcrypt password hashing
- Secure token storage in session

### Authorization Layer
- Role-based access control
- Route-level protection
- Claim-based authorization

### Data Layer
- SQL injection prevention (ORM)
- Input validation
- File type validation
- File size limits

### Network Layer
- Docker network isolation
- HTTPS support (via reverse proxy)
- CORS configuration

## Scalability Architecture

### Current Limitations
- Single database instance
- Single API instance
- Local file storage

### Scaling Path
1. **Horizontal Scaling**: Multiple API instances behind load balancer
2. **Database Scaling**: Read replicas for queries
3. **File Storage**: Move to S3 or similar
4. **Caching**: Redis for sessions and frequently accessed data
5. **Message Queue**: RabbitMQ/Celery for background tasks

## Related Documentation
- [System Overview](01_SYSTEM_OVERVIEW.md)
- [API Reference](03_API_REFERENCE.md)
- [Database Schema](04_DATABASE_SCHEMA.md)
