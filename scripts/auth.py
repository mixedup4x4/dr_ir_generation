import sys
import os

# Add the project root to sys.path to resolve module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import bcrypt
from sqlalchemy.orm import sessionmaker
from db.models import User
from db.database_setup import DATABASE_URL
from sqlalchemy import create_engine

# Set up database connection
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Role hierarchy for access control
ROLE_HIERARCHY = {
    "admin": 3,     # Full access
    "approver": 2,  # Can approve plans
    "editor": 1,    # Can create/edit plans
    "viewer": 0     # Read-only access
}

def hash_password(password):
    """Hashes a password using bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed_password):
    """Verifies a password against the stored hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def check_permission(user, required_role):
    """Checks if a user has the required role to perform an action."""
    user_role_level = ROLE_HIERARCHY.get(user.role, 0)
    required_role_level = ROLE_HIERARCHY.get(required_role, 0)
    return user_role_level >= required_role_level

def create_user(username, password, role="viewer"):
    """Creates a new user with a hashed password and role."""
    if session.query(User).filter_by(username=username).first():
        print("Error: Username already exists.")
        return False

    hashed_password = hash_password(password)
    new_user = User(username=username, password_hash=hashed_password, role=role)
    session.add(new_user)
    session.commit()
    print(f"User '{username}' created successfully with role '{role}'.")
    return True

def authenticate_user(username, password):
    """Authenticates a user and checks their role."""
    user = session.query(User).filter_by(username=username).first()
    if user and verify_password(password, user.password_hash):
        print(f"User '{username}' authenticated successfully. Role: {user.role}")
        return user
    print("Authentication failed.")
    return None

def list_users():
    """Lists all registered users."""
    users = session.query(User).all()
    if not users:
        print("No users found.")
        return
    print("\nRegistered Users:")
    for user in users:
        print(f" - {user.username} (Role: {user.role})")

def delete_user(username):
    """Deletes a user from the database."""
    user = session.query(User).filter_by(username=username).first()
    if not user:
        print(f"Error: User '{username}' not found.")
        return False
    session.delete(user)
    session.commit()
    print(f"User '{username}' deleted successfully.")
    return True

if __name__ == "__main__":
    # Quick test
    create_user("admin", "securepassword", "admin")
    authenticate_user("admin", "securepassword")
    list_users()
