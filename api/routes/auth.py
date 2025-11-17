"""
Authentication routes for the Site-Steward API.
Handles user login and JWT token generation.
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
import bcrypt
from database.db import get_db
from database.models import UserORM

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Authenticate user and return JWT token.
    
    Request body:
        {
            "username": "string",
            "password": "string"
        }
    
    Response:
        {
            "token": "jwt_token_string",
            "user_id": "user_id",
            "role": "admin|foreman"
        }
    
    Requirements: 1.1, 1.2, 1.3, 1.4
    """
    try:
        # Get request data
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'Bad Request',
                'message': 'Request body is required'
            }), 400
        
        username = data.get('username')
        password = data.get('password')
        
        # Validate input
        if not username or not password:
            return jsonify({
                'error': 'Bad Request',
                'message': 'Username and password are required'
            }), 400
        
        # Get database session
        db = next(get_db())
        
        # Find user by username
        user = db.query(UserORM).filter(UserORM.username == username).first()
        
        # Requirement 1.3: Return error for invalid credentials
        if not user:
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Invalid credentials'
            }), 401
        
        # Verify password using bcrypt
        if not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Invalid credentials'
            }), 401
        
        # Requirement 1.1: Generate JWT token with user_id and role claims
        additional_claims = {
            'role': user.role,
            'user_id': user.id
        }
        
        access_token = create_access_token(
            identity=user.id,
            additional_claims=additional_claims
        )
        
        # Requirement 1.1: Return JWT token
        return jsonify({
            'token': access_token,
            'user_id': user.id,
            'role': user.role
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password string
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(password: str, password_hash: str) -> bool:
    """
    Verify a password against a hash.
    
    Args:
        password: Plain text password
        password_hash: Hashed password
        
    Returns:
        True if password matches, False otherwise
    """
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
