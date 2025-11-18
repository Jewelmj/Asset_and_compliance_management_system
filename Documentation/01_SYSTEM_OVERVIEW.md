# Site-Steward MVP - System Overview

## Executive Summary

Site-Steward is a comprehensive asset and compliance management system designed for construction sites. The system enables real-time asset tracking via QR codes, compliance document management, and automated expiry monitoring with email notifications.

## System Purpose

The Site-Steward MVP addresses critical challenges in construction site management:

1. **Asset Tracking**: Real-time location tracking of equipment and tools across multiple job sites
2. **Compliance Management**: Centralized storage and monitoring of subcontractor compliance documents
3. **Automated Alerts**: Proactive notifications for expiring certifications and insurance documents
4. **Mobile Access**: Field-ready mobile interface for on-site personnel
5. **Audit Trail**: Complete history of asset movements and document updates

## Key Features

### Asset Management
- Create and categorize assets (Heavy Equipment, Power Equipment, Safety Equipment, etc.)
- Generate unique QR codes for each asset
- Track asset location and movement history
- Assign assets to projects or mark as unassigned
- Mobile QR code scanning for quick asset lookup

### Compliance Monitoring
- Upload and store compliance documents (PDF format)
- Set expiry dates for certifications and insurance
- Visual status indicators (RED/GREEN) for compliance status
- Automated daily checks for expiring documents
- Email notifications for documents expiring within 30 days

### Project Management
- Create and manage multiple construction projects
- Assign assets and subcontractors to projects
- View project-specific compliance dashboard
- Track asset allocation across projects

### User Roles
- **Admin**: Full system access, manage all entities, upload documents
- **Foreman**: Field operations, scan QR codes, view compliance status

## Technology Stack

### Backend
- **Framework**: Flask (Python)
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.x
- **Authentication**: JWT (JSON Web Tokens) with Flask-JWT-Extended
- **Password Hashing**: bcrypt

### Frontend
- **Admin Portal**: Streamlit (Python) - Desktop-optimized interface
- **Field App**: Streamlit (Python) - Mobile-optimized interface
- **QR Code Generation**: qrcode library with PIL
- **QR Code Scanning**: streamlit-webrtc with pyzbar

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Database Storage**: PostgreSQL persistent volumes
- **File Storage**: Local filesystem for compliance documents
- **Email**: SMTP (configurable for Gmail, SendGrid, etc.)

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Client Layer                             │
├──────────────────────────┬──────────────────────────────────┤
│   Admin Portal           │      Field Mobile App            │
│   (Streamlit)            │      (Streamlit)                 │
│   Port: 8501             │      Port: 8502                  │
│   - Asset Management     │      - QR Code Scanner           │
│   - Document Upload      │      - Asset Movement            │
│   - Compliance Dashboard │      - Compliance Viewer         │
└──────────────┬───────────┴──────────────┬───────────────────┘
               │                          │
               │    HTTP/JSON (JWT Auth)  │
               └──────────┬───────────────┘
                          │
┌─────────────────────────▼─────────────────────────────────┐
│                   API Layer                                │
│                   Flask REST API                           │
│                   Port: 5000                               │
├────────────────────────────────────────────────────────────┤
│  Routes:                                                   │
│  - /api/login              - Authentication                │
│  - /api/assets             - Asset CRUD                    │
│  - /api/projects           - Project CRUD                  │
│  - /api/subcontractors     - Subcontractor CRUD            │
│  - /api/projects/{id}/compliance - Compliance Status       │
├────────────────────────────────────────────────────────────┤
│  Middleware:                                               │
│  - JWT Authentication      - Role-based Authorization      │
├────────────────────────────────────────────────────────────┤
│  Services:                                                 │
│  - ComplianceService       - Status calculation            │
└─────────────────────────┬──────────────────────────────────┘
                          │
┌─────────────────────────▼─────────────────────────────────┐
│                   Data Layer                               │
│                   PostgreSQL 15                            │
│                   Port: 5432                               │
├────────────────────────────────────────────────────────────┤
│  Tables:                                                   │
│  - users                   - User accounts & auth          │
│  - projects                - Construction projects         │
│  - assets                  - Equipment & tools             │
│  - subcontractors          - Third-party contractors       │
│  - compliance_documents    - PDF documents with expiry     │
│  - asset_history           - Movement audit trail          │
│  - project_subcontractors  - Many-to-many junction         │
└────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                   Background Services                        │
├─────────────────────────────────────────────────────────────┤
│  - Compliance Check Script (check_expiry.py)                │
│    • Runs daily via cron                                    │
│    • Queries expiring documents                             │
│    • Sends email notifications                              │
└─────────────────────────────────────────────────────────────┘
```

## Network Architecture

All services communicate through a Docker bridge network (`sitesteward-network`):

- **External Access**: Exposed ports (5000, 8501, 8502)
- **Internal Communication**: Service-to-service via Docker DNS
- **Database Access**: API connects to PostgreSQL via internal network
- **File Storage**: Shared volume mount for compliance documents

## Data Flow

### Asset Tracking Flow
1. Admin creates asset via Admin Portal
2. System generates unique QR code
3. Foreman scans QR code via Field App
4. System retrieves asset details from database
5. Foreman moves asset to new project
6. System records movement in asset_history table
7. Asset location updated in real-time

### Compliance Monitoring Flow
1. Admin uploads compliance document via Admin Portal
2. System stores PDF file and metadata in database
3. Daily cron job runs check_expiry.py script
4. Script queries documents expiring within 30 days
5. System sends email notification to administrators
6. Admin Portal displays RED/GREEN status indicators
7. Admin uploads renewed document to resolve RED status

### Authentication Flow
1. User submits credentials to /api/login endpoint
2. API validates credentials against database
3. System generates JWT token with user_id and role claims
4. Token returned to client and stored in session
5. Client includes token in Authorization header for all requests
6. API middleware validates token and extracts user claims
7. Protected routes check user role for authorization

## Security Features

### Authentication & Authorization
- JWT-based stateless authentication
- Bcrypt password hashing with salt
- Token expiration (24 hours)
- Role-based access control (RBAC)
- Protected API endpoints

### Data Security
- SQL injection prevention via SQLAlchemy ORM
- Input validation on all endpoints
- Secure file upload with type and size validation
- Environment variable configuration for secrets

### Network Security
- Docker network isolation
- Configurable HTTPS support
- CORS configuration for API access

## Deployment Models

### Development
- Docker Compose with hot-reload
- Local database with seed data
- Debug logging enabled
- Direct port access to all services

### Production
- Docker Compose with restart policies
- Persistent volume for database
- Production-grade SMTP configuration
- Reverse proxy (nginx/Traefik) for HTTPS
- Regular database backups
- Monitoring and alerting

## Scalability Considerations

### Current Architecture
- Single-instance deployment
- Suitable for small to medium construction companies
- Supports multiple concurrent users
- Handles hundreds of assets and documents

### Future Scaling Options
- Horizontal scaling of API and frontend services
- Load balancer for multiple instances
- Database replication for read scaling
- Cloud storage (S3) for compliance documents
- Redis for session management and caching
- Message queue for background tasks

## System Requirements

### Server Requirements
- **CPU**: 2+ cores
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 20GB minimum (more for compliance documents)
- **OS**: Linux (Ubuntu 20.04+), Windows Server, macOS

### Client Requirements
- **Browser**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **Mobile**: iOS 13+, Android 8+
- **Camera**: Required for QR code scanning
- **Network**: Stable internet connection

## Compliance & Standards

### Document Management
- PDF format for compliance documents
- Maximum file size: 10MB per document
- Expiry date tracking with 30-day warning threshold
- Audit trail for all document uploads

### Data Retention
- Asset history: Indefinite retention
- Compliance documents: Retained until manually deleted
- User activity logs: Available via database queries

## Support & Maintenance

### Regular Maintenance Tasks
- Daily: Automated compliance checks
- Weekly: Database backups
- Monthly: Review and update expiring documents
- Quarterly: System updates and security patches

### Monitoring Points
- Database connection health
- API response times
- Email delivery success rate
- Disk space for document storage
- Failed login attempts

## Related Documentation

- [Architecture Details](02_ARCHITECTURE.md)
- [API Reference](03_API_REFERENCE.md)
- [Database Schema](04_DATABASE_SCHEMA.md)
- [Deployment Guide](05_DEPLOYMENT_GUIDE.md)
- [User Guide](06_USER_GUIDE.md)
- [Development Guide](07_DEVELOPMENT_GUIDE.md)
- [Security Guide](08_SECURITY.md)
- [Troubleshooting](09_TROUBLESHOOTING.md)
