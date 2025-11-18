# Site-Steward MVP - API Reference

## Base URL
```
http://localhost:5000/api
```

## Authentication

All endpoints except `/api/login` require JWT authentication.

### Headers
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

## Endpoints

### Authentication

#### POST /api/login
Authenticate user and receive JWT token.

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Success Response (200 OK):**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user_id": "uuid-string",
  "role": "admin"
}
```

**Error Responses:**
- `400 Bad Request`: Missing username or password
- `401 Unauthorized`: Invalid credentials

**Example:**
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

---

### Assets

#### GET /api/assets
List all assets with their current project information.

**Authentication:** Required

**Success Response (200 OK):**
```json
[
  {
    "id": "uuid-string",
    "name": "Excavator CAT 320",
    "category": "Heavy Equipment",
    "project_id": "uuid-string",
    "project_name": "Downtown Office Building"
  },
  {
    "id": "uuid-string",
    "name": "Scaffolding Set A",
    "category": "Safety Equipment",
    "project_id": null,
    "project_name": null
  }
]
```

**Example:**
```bash
curl -X GET http://localhost:5000/api/assets \
  -H "Authorization: Bearer <token>"
```

---

#### POST /api/assets
Create a new asset.

**Authentication:** Required

**Request Body:**
```json
{
  "name": "Generator 100kW",
  "category": "Power Equipment"
}
```

**Success Response (201 Created):**
```json
{
  "id": "uuid-string",
  "name": "Generator 100kW",
  "category": "Power Equipment",
  "qr_code_url": null
}
```

**Error Responses:**
- `400 Bad Request`: Missing name or category
- `401 Unauthorized`: Invalid or missing token

**Example:**
```bash
curl -X POST http://localhost:5000/api/assets \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"name": "Generator 100kW", "category": "Power Equipment"}'
```

---

#### GET /api/assets/{asset_id}
Get detailed information about a specific asset including movement history.

**Authentication:** Required

**Path Parameters:**
- `asset_id` (string): UUID of the asset

**Success Response (200 OK):**
```json
{
  "id": "uuid-string",
  "name": "Excavator CAT 320",
  "category": "Heavy Equipment",
  "project_id": "uuid-string",
  "project_name": "Downtown Office Building",
  "history": [
    {
      "id": "uuid-string",
      "project_id": "uuid-string",
      "project_name": "Downtown Office Building",
      "moved_at": "2024-11-17T10:30:00",
      "moved_by": "uuid-string"
    }
  ]
}
```

**Error Responses:**
- `404 Not Found`: Asset not found
- `401 Unauthorized`: Invalid or missing token

**Example:**
```bash
curl -X GET http://localhost:5000/api/assets/abc-123-def \
  -H "Authorization: Bearer <token>"
```

---

#### POST /api/assets/{asset_id}/move
Move an asset to a different project.

**Authentication:** Required

**Path Parameters:**
- `asset_id` (string): UUID of the asset

**Request Body:**
```json
{
  "project_id": "uuid-string"
}
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "message": "Asset moved successfully"
}
```

**Error Responses:**
- `400 Bad Request`: Missing project_id
- `404 Not Found`: Asset or project not found
- `401 Unauthorized`: Invalid or missing token

**Example:**
```bash
curl -X POST http://localhost:5000/api/assets/abc-123-def/move \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"project_id": "xyz-789-ghi"}'
```

---

### Projects

#### GET /api/projects
List all projects with asset count.

**Authentication:** Required

**Success Response (200 OK):**
```json
[
  {
    "id": "uuid-string",
    "name": "Downtown Office Building",
    "location": "123 Main St, City",
    "asset_count": 5
  },
  {
    "id": "uuid-string",
    "name": "Residential Complex Phase 2",
    "location": "456 Oak Ave, Town",
    "asset_count": 2
  }
]
```

**Example:**
```bash
curl -X GET http://localhost:5000/api/projects \
  -H "Authorization: Bearer <token>"
```

---

#### POST /api/projects
Create a new project.

**Authentication:** Required

**Request Body:**
```json
{
  "name": "Harbor Bridge Construction",
  "location": "789 Harbor Rd, Port City"
}
```

**Success Response (201 Created):**
```json
{
  "id": "uuid-string",
  "name": "Harbor Bridge Construction",
  "location": "789 Harbor Rd, Port City"
}
```

**Error Responses:**
- `400 Bad Request`: Missing name
- `401 Unauthorized`: Invalid or missing token

**Example:**
```bash
curl -X POST http://localhost:5000/api/projects \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"name": "Harbor Bridge", "location": "789 Harbor Rd"}'
```

---

#### GET /api/projects/{project_id}/compliance
Get compliance status for all subcontractors on a project.

**Authentication:** Required

**Path Parameters:**
- `project_id` (string): UUID of the project

**Success Response (200 OK):**
```json
{
  "project_id": "uuid-string",
  "subcontractors": [
    {
      "id": "uuid-string",
      "name": "ABC Electrical Services",
      "status": "RED",
      "documents": [
        {
          "id": "uuid-string",
          "document_type": "Liability Insurance",
          "expiry_date": "2024-12-31",
          "status": "GREEN"
        },
        {
          "id": "uuid-string",
          "document_type": "Safety Certification",
          "expiry_date": "2024-11-25",
          "status": "RED"
        }
      ]
    },
    {
      "id": "uuid-string",
      "name": "XYZ Plumbing Co",
      "status": "GREEN",
      "documents": [
        {
          "id": "uuid-string",
          "document_type": "Liability Insurance",
          "expiry_date": "2025-02-15",
          "status": "GREEN"
        }
      ]
    }
  ]
}
```

**Status Indicators:**
- `GREEN`: All documents valid for more than 30 days
- `RED`: One or more documents expired or expiring within 30 days

**Error Responses:**
- `404 Not Found`: Project not found
- `401 Unauthorized`: Invalid or missing token

**Example:**
```bash
curl -X GET http://localhost:5000/api/projects/abc-123-def/compliance \
  -H "Authorization: Bearer <token>"
```

---

### Subcontractors

#### GET /api/subcontractors
List all subcontractors.

**Authentication:** Required

**Success Response (200 OK):**
```json
[
  {
    "id": "uuid-string",
    "name": "ABC Electrical Services",
    "email": "contact@abcelectrical.com",
    "phone": "555-0101"
  },
  {
    "id": "uuid-string",
    "name": "XYZ Plumbing Co",
    "email": "info@xyzplumbing.com",
    "phone": "555-0202"
  }
]
```

**Example:**
```bash
curl -X GET http://localhost:5000/api/subcontractors \
  -H "Authorization: Bearer <token>"
```

---

#### POST /api/subcontractors
Create a new subcontractor.

**Authentication:** Required

**Request Body:**
```json
{
  "name": "DEF HVAC Systems",
  "email": "info@defhvac.com",
  "phone": "555-0303"
}
```

**Success Response (201 Created):**
```json
{
  "id": "uuid-string",
  "name": "DEF HVAC Systems",
  "email": "info@defhvac.com",
  "phone": "555-0303"
}
```

**Error Responses:**
- `400 Bad Request`: Missing name
- `401 Unauthorized`: Invalid or missing token

**Example:**
```bash
curl -X POST http://localhost:5000/api/subcontractors \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"name": "DEF HVAC", "email": "info@defhvac.com", "phone": "555-0303"}'
```

---

#### POST /api/subcontractors/{sub_id}/document
Upload a compliance document for a subcontractor.

**Authentication:** Required

**Path Parameters:**
- `sub_id` (string): UUID of the subcontractor

**Request:** multipart/form-data
- `file` (file): PDF file (max 10MB)
- `expiry_date` (string): Date in YYYY-MM-DD format
- `document_type` (string): Type of document (e.g., "Liability Insurance", "Safety Certification")

**Success Response (201 Created):**
```json
{
  "id": "uuid-string",
  "file_path": "uploads/compliance/abc-123_Insurance_20241117_120000_document.pdf",
  "expiry_date": "2025-06-30",
  "status": "GREEN"
}
```

**Error Responses:**
- `400 Bad Request`: Missing file, expiry_date, or document_type
- `400 Bad Request`: Invalid file type (only PDF allowed)
- `400 Bad Request`: File size exceeds 10MB
- `400 Bad Request`: Invalid date format
- `404 Not Found`: Subcontractor not found
- `401 Unauthorized`: Invalid or missing token

**Example:**
```bash
curl -X POST http://localhost:5000/api/subcontractors/abc-123-def/document \
  -H "Authorization: Bearer <token>" \
  -F "file=@insurance.pdf" \
  -F "expiry_date=2025-06-30" \
  -F "document_type=Liability Insurance"
```

---

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "error": "Bad Request",
  "message": "Detailed error message"
}
```

### 401 Unauthorized
```json
{
  "error": "Unauthorized",
  "message": "Invalid or expired token"
}
```

### 403 Forbidden
```json
{
  "error": "Forbidden",
  "message": "Access denied. Required role: admin"
}
```

### 404 Not Found
```json
{
  "error": "Not Found",
  "message": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal Server Error",
  "message": "Error details"
}
```

---

## Authentication Flow

### 1. Login
```bash
# Request
POST /api/login
{
  "username": "admin",
  "password": "admin123"
}

# Response
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user_id": "abc-123-def",
  "role": "admin"
}
```

### 2. Use Token in Subsequent Requests
```bash
GET /api/assets
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

### 3. Token Expiration
Tokens expire after 24 hours. When a token expires, you'll receive a 401 Unauthorized response. Re-authenticate to get a new token.

---

## Rate Limiting

Currently, no rate limiting is implemented. For production deployment, consider implementing rate limiting using:
- Flask-Limiter
- nginx rate limiting
- API Gateway rate limiting

---

## CORS Configuration

CORS is not explicitly configured in the current implementation. For production deployment with frontend on different domain:

```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://yourdomain.com"],
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

---

## Pagination

Currently, list endpoints return all results. For large datasets, implement pagination:

**Recommended Query Parameters:**
- `page` (int): Page number (default: 1)
- `per_page` (int): Items per page (default: 20, max: 100)

**Recommended Response Format:**
```json
{
  "items": [...],
  "page": 1,
  "per_page": 20,
  "total": 150,
  "pages": 8
}
```

---

## Filtering and Sorting

Currently not implemented. Recommended query parameters:

**Filtering:**
- `category`: Filter assets by category
- `project_id`: Filter assets by project
- `status`: Filter by compliance status (RED/GREEN)

**Sorting:**
- `sort_by`: Field to sort by
- `order`: asc or desc

**Example:**
```bash
GET /api/assets?category=Heavy Equipment&sort_by=name&order=asc
```

---

## Webhooks

Currently not implemented. For future implementation, consider:
- Document upload notifications
- Compliance status changes
- Asset movement events

---

## API Versioning

Current version: v1 (implicit)

For future versions, consider:
- URL versioning: `/api/v2/assets`
- Header versioning: `Accept: application/vnd.sitesteward.v2+json`

---

## Testing the API

### Using cURL

```bash
# Login
TOKEN=$(curl -s -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  | jq -r '.token')

# List assets
curl -X GET http://localhost:5000/api/assets \
  -H "Authorization: Bearer $TOKEN"

# Create asset
curl -X POST http://localhost:5000/api/assets \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Asset","category":"Test Category"}'
```

### Using Python Requests

```python
import requests

# Login
response = requests.post('http://localhost:5000/api/login', json={
    'username': 'admin',
    'password': 'admin123'
})
token = response.json()['token']

# List assets
headers = {'Authorization': f'Bearer {token}'}
response = requests.get('http://localhost:5000/api/assets', headers=headers)
assets = response.json()
print(assets)
```

### Using Postman

1. Create a new request
2. Set method and URL
3. Add Authorization header: `Bearer <token>`
4. Add request body (for POST requests)
5. Send request

---

## Related Documentation
- [System Overview](01_SYSTEM_OVERVIEW.md)
- [Architecture](02_ARCHITECTURE.md)
- [Database Schema](04_DATABASE_SCHEMA.md)
- [Development Guide](07_DEVELOPMENT_GUIDE.md)
