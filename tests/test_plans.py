import pytest
from db.query import create_user, create_plan, list_plans  # Fix: Import create_user
from db.database_setup import session
from db.models import Plan, User

@pytest.fixture
def test_user():
    """Fixture to create a user for testing plans."""
    user = create_user("plan_tester", "PlanPass123!", "editor")  # Fix: Function now correctly imported
    yield user
    session.query(User).filter_by(username="plan_tester").delete()
    session.commit()

@pytest.fixture
def test_plan(test_user):
    """Fixture to create a test plan."""
    plan = create_plan("Test Plan", "drp", "plan_tester", "nist")
    yield plan
    session.query(Plan).filter_by(title="Test Plan").delete()
    session.commit()

def test_create_plan(test_plan):
    """Test if a plan is created successfully."""
    assert test_plan is not None

def test_list_plans(test_plan):
    """Test if plans are listed correctly."""
    plans = list_plans()
    assert any(plan.title == "Test Plan" for plan in plans)
