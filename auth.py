"""
auth.py
=======
Authentication utilities for TaskPilot.

Includes:
  - Password hashing and verification
  - JWT token generation and verification
  - Authentication decorators for routes
"""

import jwt
import datetime
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, jsonify
from config import Config


# ═══════════════════════════════════════════════
# PASSWORD HASHING
# ═══════════════════════════════════════════════

def hash_password(password: str) -> str:
    """Hash a password using Werkzeug's security module."""
    return generate_password_hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against its hash."""
    return check_password_hash(password_hash, password)


# ═══════════════════════════════════════════════
# JWT TOKEN HANDLING
# ═══════════════════════════════════════════════

def generate_token(user_id: int, username: str, expiration_hours: int = 24) -> str:
    """
    Generate a JWT token for a user.
    
    Args:
        user_id: User's ID
        username: User's username
        expiration_hours: Token expiration in hours (default: 24)
    
    Returns:
        JWT token string
    """
    payload = {
        "user_id": user_id,
        "username": username,
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=expiration_hours)
    }
    token = jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")
    return token


def verify_token(token: str) -> dict:
    """
    Verify a JWT token and return its payload.
    
    Args:
        token: JWT token string
    
    Returns:
        Decoded token payload dictionary
    
    Raises:
        jwt.InvalidTokenError: If token is invalid or expired
    """
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise jwt.InvalidTokenError("Token has expired")
    except jwt.InvalidTokenError as e:
        raise jwt.InvalidTokenError(f"Invalid token: {str(e)}")


# ═══════════════════════════════════════════════
# AUTHENTICATION DECORATOR
# ═══════════════════════════════════════════════

def require_auth(f):
    """
    Decorator to protect routes with JWT authentication.
    Extracts token from 'Authorization: Bearer <token>' header.
    Adds 'current_user' to request context.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get token from Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"error": "Missing authorization header"}), 401

        # Parse "Bearer <token>"
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return jsonify({"error": "Invalid authorization header format"}), 401

        token = parts[1]

        # Verify token
        try:
            payload = verify_token(token)
            # Store user info in request context for route handler
            request.current_user = {
                "user_id": payload["user_id"],
                "username": payload["username"]
            }
        except jwt.InvalidTokenError as e:
            return jsonify({"error": str(e)}), 401

        return f(*args, **kwargs)

    return decorated_function


# ═══════════════════════════════════════════════
# TOKEN EXTRACTION HELPER
# ═══════════════════════════════════════════════

def get_token_from_request() -> str:
    """Extract JWT token from request Authorization header."""
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return None
    
    parts = auth_header.split()
    if len(parts) == 2 and parts[0].lower() == "bearer":
        return parts[1]
    return None
