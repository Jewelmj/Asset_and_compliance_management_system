"""
Authentication middleware for the Site-Steward API.
Provides JWT validation and role-based authorization helpers.
"""
from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt, get_jwt_identity


def jwt_required_custom():
    """
    Decorator to require JWT authentication for routes.
    
    Requirements: 1.2, 1.4
    
    Usage:
        @app.route('/protected')
        @jwt_required_custom()
        def protected_route():
            return {'message': 'Access granted'}
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                # Requirement 1.2: Validate JWT token
                verify_jwt_in_request()
                
                # Requirement 1.4: Check token expiration (handled by flask-jwt-extended)
                # If token is expired, verify_jwt_in_request() will raise an exception
                
                return fn(*args, **kwargs)
            except Exception as e:
                # Requirement 1.4: Return unauthorized error for invalid/expired tokens
                return jsonify({
                    'error': 'Unauthorized',
                    'message': 'Invalid or expired token'
                }), 401
        
        return wrapper
    return decorator


def role_required(*allowed_roles):
    """
    Decorator to require specific roles for route access.
    
    Requirements: 1.2, 1.4
    
    Args:
        *allowed_roles: Variable number of role strings (e.g., 'admin', 'foreman')
    
    Usage:
        @app.route('/admin-only')
        @jwt_required_custom()
        @role_required('admin')
        def admin_route():
            return {'message': 'Admin access granted'}
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                # Verify JWT is present
                verify_jwt_in_request()
                
                # Get claims from JWT
                claims = get_jwt()
                user_role = claims.get('role')
                
                # Check if user has required role
                if user_role not in allowed_roles:
                    return jsonify({
                        'error': 'Forbidden',
                        'message': f'Access denied. Required role: {", ".join(allowed_roles)}'
                    }), 403
                
                return fn(*args, **kwargs)
            except Exception as e:
                return jsonify({
                    'error': 'Unauthorized',
                    'message': 'Invalid or expired token'
                }), 401
        
        return wrapper
    return decorator


def get_current_user_id():
    """
    Get the current authenticated user's ID from JWT.
    
    Returns:
        User ID string from JWT identity
        
    Raises:
        Exception if JWT is not present or invalid
    """
    return get_jwt_identity()


def get_current_user_role():
    """
    Get the current authenticated user's role from JWT.
    
    Returns:
        User role string from JWT claims
        
    Raises:
        Exception if JWT is not present or invalid
    """
    claims = get_jwt()
    return claims.get('role')


def get_current_user_claims():
    """
    Get all claims from the current JWT.
    
    Returns:
        Dictionary of JWT claims
        
    Raises:
        Exception if JWT is not present or invalid
    """
    return get_jwt()
