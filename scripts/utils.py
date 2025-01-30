import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime

def generate_hash(password: str) -> str:
    """Generate a hashed password."""
    return generate_password_hash(password)

def verify_password(stored_hash: str, password: str) -> bool:
    """Verify a password against a stored hash."""
    return check_password_hash(stored_hash, password)

def generate_random_string(length: int = 16) -> str:
    """Generate a random string for use in token generation or password creation."""
    return os.urandom(length).hex()

def format_datetime(datetime_obj) -> str:
    """Return a formatted datetime string."""
    return datetime_obj.strftime('%Y-%m-%d %H:%M:%S')
