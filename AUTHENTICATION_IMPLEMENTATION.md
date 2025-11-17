# Authentication System Implementation

## Overview
Implemented a complete JWT-based authentication system for the Site-Steward MVP API.

## Files Created/Modified

### 1. `api/routes/auth.py` (NEW)
- **POST /api/login** endpoint for user authentication
- Password verification using bcrypt
- JWT token generation with user_id and role claims
- Proper error handling for invalid credentials
- Helper functions: `hash_password()`, `verify_password()`

### 2. `api/middleware/auth.py` (NEW)
- `jwt_required_custom()` decorator for protecting routes
- `role_required()` decorator for role-based authorization
- Helper functions:
  - `get_current_user_id()` - Extract user ID from JWT
  - `get_current_user_role()` - Extract user role from JWT
  - `get_current_user_claims()` - Get all JWT claims
- Token expiration checking
- Proper error responses for unauthorized access

### 3. `api/app.py` (MODIFIED)
- Imported and configured Flask-JWT-Extended
- Loaded configuration from config.py
- Registered auth blueprint at `/api` prefix

### 4. `api/middleware/__init__.py` (MODIFIED)
- Exported authentication middleware functions

## Requirements Satisfied

### Requirement 1.1 ✓
WHEN a user submits valid credentials to the login endpoint, THE System SHALL return a valid JWT token
- Implemented in `auth.py` login endpoint
- Returns JWT with user_id and role claims

### Requirement 1.2 ✓
WHEN a user includes a valid JWT token in the Authorization header, THE System SHALL authenticate the request and grant access to protected endpoints
- Implemented via `jwt_required_custom()` decorator
- Validates JWT from Authorization header

### Requirement 1.3 ✓
WHEN a user submits invalid credentials, THE System SHALL return an authentication error with appropriate HTTP status code
- Returns 401 Unauthorized for invalid credentials
- Returns 400 Bad Request for missing fields

### Requirement 1.4 ✓
WHEN a JWT token expires, THE System SHALL reject requests and return an unauthorized error
- Token expiration checked by flask-jwt-extended
- Returns 401 Unauthorized for expired tokens

## Usage Examples

### Login Request
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

### Response
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user_id": "uuid-here",
  "role": "admin"
}
```

### Protected Route Example
```python
from api.middleware import jwt_required_custom, role_required

@app.route('/api/admin-only')
@jwt_required_custom()
@role_required('admin')
def admin_only():
    return {'message': 'Admin access granted'}
```

### Making Authenticated Requests
```bash
curl -X GET http://localhost:5000/api/protected \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

## Testing

### Manual Testing
Run the test script after starting the API:
```bash
python test_auth.py
```

### Test Users (from seed data)
- **Admin**: username=`admin`, password=`admin123`
- **Foreman**: username=`foreman`, password=`foreman123`

## Configuration
JWT settings are configured in `api/config.py`:
- Token expiration: 24 hours
- Token location: Authorization header
- Header type: Bearer

## Security Features
- Passwords hashed with bcrypt
- JWT tokens with expiration
- Role-based access control
- Proper error handling without leaking sensitive info
- Input validation on all endpoints

## Next Steps
To use authentication in other routes:
1. Import the decorators: `from api.middleware import jwt_required_custom, role_required`
2. Add `@jwt_required_custom()` to protect routes
3. Add `@role_required('admin')` or `@role_required('foreman')` for role-specific access
4. Use `get_current_user_id()` to get the authenticated user's ID
