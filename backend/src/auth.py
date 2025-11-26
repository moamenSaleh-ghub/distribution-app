"""
Authentication helper module for JWT token generation and validation.
"""
# In Lambda, when zip is unpacked, the root is added to sys.path
# Our zip has src/ at root, so jwt is at src/jwt/
# We need to import it as from src import jwt, or add src to path
# Since other modules use absolute imports like src.db, we'll use the same pattern
# But jwt is a third-party package, so we need to handle it differently
import sys
import os

# Get the directory containing src/ (the Lambda task root)
# __file__ in Lambda will be /var/task/src/auth.py
# So dirname(dirname(__file__)) gives us /var/task
# We need to add /var/task/src to path so we can import jwt
task_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_path = os.path.join(task_root, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Now import jwt - it should be at src/jwt/ which is now in path as jwt/
import jwt
import time
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

# TODO: Move this to SSM Parameter Store or AWS Secrets Manager for production
JWT_SECRET = "CHANGE_ME_TO_A_LONG_RANDOM_SECRET_AT_LEAST_32_CHARACTERS_LONG_FOR_HS256"
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 12


class AuthenticationError(Exception):
    """Raised when authentication fails"""
    pass


def generate_token(user_identifier: str, expiration_hours: Optional[int] = None) -> str:
    """
    Generate a JWT token for a user.
    
    Args:
        user_identifier: User identifier (e.g., "admin")
        expiration_hours: Optional expiration time in hours (defaults to JWT_EXPIRATION_HOURS)
    
    Returns:
        JWT token string
    """
    if expiration_hours is None:
        expiration_hours = JWT_EXPIRATION_HOURS
    
    now = datetime.utcnow()
    expiration = now + timedelta(hours=expiration_hours)
    
    payload = {
        "sub": user_identifier,
        "exp": int(expiration.timestamp()),
        "iat": int(now.timestamp())
    }
    
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def verify_token(token: str) -> Dict[str, Any]:
    """
    Verify and decode a JWT token.
    
    Args:
        token: JWT token string
    
    Returns:
        Decoded payload dictionary
    
    Raises:
        AuthenticationError: If token is invalid or expired
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise AuthenticationError("Token has expired")
    except jwt.InvalidTokenError as e:
        raise AuthenticationError(f"Invalid token: {str(e)}")


def extract_and_verify_token(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract and verify JWT token from API Gateway event.
    
    Args:
        event: API Gateway event dictionary
    
    Returns:
        Decoded token payload
    
    Raises:
        AuthenticationError: If token is missing, invalid, or expired
    """
    headers = event.get("headers", {}) or {}
    
    # API Gateway may lowercase header names
    auth_header = headers.get("Authorization") or headers.get("authorization")
    
    if not auth_header:
        raise AuthenticationError("Authorization header is missing")
    
    # Check for Bearer token format
    if not auth_header.startswith("Bearer "):
        raise AuthenticationError("Authorization header must be in format 'Bearer <token>'")
    
    token = auth_header[7:].strip()  # Remove "Bearer " prefix
    
    if not token:
        raise AuthenticationError("Token is missing")
    
    return verify_token(token)

