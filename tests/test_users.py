import pytest
from db.query import create_user, authenticate_user
from db.database_setup import session
from db.models import User

@pytest.fixture
def test_user():
    """Fixture to create a test user and clean up afterward."""
    user = create_user("test_user", "SecurePass123!", "editor")
    yield user  # Ensures user is returned properly
    session.query(User).filter_by(username="test_user").delete()
    session.commit()

def test_create_user(test_user):
    """Test if a user is created successfully."""
    assert test_user is not None

def test_authenticate_user(test_user):
    """Test user authentication with correct credentials."""
    assert authenticate_user("test_user", "SecurePass123!") is not None

def test_authenticate_user_invalid_password(test_user):
    """Test authentication with an incorrect password."""
    assert authenticate_user("test_user", "WrongPassword!") is None

def test_authenticate_non_existent_user():
    """Test authentication of a non-existent user."""
    assert authenticate_user("fake_user", "DoesNotExist!") is None
