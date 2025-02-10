import pytest
from db.query import create_user, log_action  # Ensure create_user is imported
from db.database_setup import session
from db.models import Log, User

@pytest.fixture
def test_user():
    """Fixture to create a test user for log testing."""
    user = create_user("log_tester", "LogPass123!", "editor")  # Fix: Function now correctly imported
    yield user
    session.query(User).filter_by(username="log_tester").delete()
    session.commit()

def test_log_creation(test_user):
    """Test if log entries are created when an action occurs."""
    log_action(test_user.id, "Created a new test plan")
    log = session.query(Log).filter_by(user_id=test_user.id).first()
    assert log is not None

def test_multiple_logs(test_user):
    """Ensure multiple log actions are recorded correctly."""

    # Clear previous logs to ensure fresh test data
    session.query(Log).filter_by(user_id=test_user.id).delete()
    session.commit()

    log_action(test_user.id, "Created a test DRP")
    log_action(test_user.id, "Updated test DRP")

    logs = session.query(Log).filter_by(user_id=test_user.id).all()
    assert len(logs) == 2  # Now it should correctly count only the two expected logs

def test_log_integrity(test_user):
    """Ensure old logs remain unchanged when new logs are added."""

    # Clear logs to avoid contamination
    session.query(Log).filter_by(user_id=test_user.id).delete()
    session.commit()

    log_action(test_user.id, "Initial log entry")
    log_action(test_user.id, "Secondary log entry")

    logs = session.query(Log).filter_by(user_id=test_user.id).order_by(Log.timestamp.asc()).all()

    assert logs[0].action == "Initial log entry"
    assert logs[1].action == "Secondary log entry"
