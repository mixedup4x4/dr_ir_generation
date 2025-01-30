from db.database_setup import session
from db.models import User, Plan, PlanVersion, Log  # Ensure User is imported
from werkzeug.security import check_password_hash   # To securely compare passwords
from scripts.utils import generate_hash, verify_password, format_datetime   #import functions

def log_action(user_id, action):
    """Log an action performed by the user."""
    new_log = Log(user_id=user_id, action=action)
    session.add(new_log)
    session.commit()
    print(f"Logged action: {action} at {format_datetime(new_log.timestamp)}")
def view_logs(user):
    """Retrieve logs for the given user."""
    logs = session.query(Log).filter_by(user_id=user.id).all()
    return logs

# In db/query.py
from utils import verify_password  # Import the function

def authenticate_user(username, password):
    """Authenticate a user by verifying the password."""
    user = session.query(User).filter_by(username=username).first()
    if user and verify_password(user.password_hash, password):  # Verify the password hash
        print(f"User '{username}' authenticated successfully. Role: {user.role}")
        return user
    else:
        print("Login failed. Invalid credentials.")
        return None

def check_permission(user, permission_level):
    """Check if the user has the required permission level."""
    if permission_level == "admin" and user.role == "admin":
        return True
    elif permission_level == "editor" and user.role in ["admin", "editor"]:
        return True
    elif permission_level == "viewer" and user.role in ["admin", "editor", "viewer"]:
        return True
    return False

from werkzeug.security import generate_password_hash

def create_user(username, password, role):
    """Create a new user with a hashed password."""
    hashed_password = generate_hash(password)  # Hash the password
    new_user = User(username=username, password_hash=hashed_password, role=role)
    session.add(new_user)
    session.commit()
    print(f"User '{username}' created successfully with role '{role}'.")

def delete_user(username):
    """Delete a user by their username."""
    user = session.query(User).filter_by(username=username).first()
    if user:
        session.delete(user)
        session.commit()
        print(f"User '{username}' deleted successfully.")
    else:
        print(f"User '{username}' not found.")

def save_plan_version(plan_id, content):
    """Save a new version of a plan and log the action."""
    plan = session.query(Plan).filter_by(id=plan_id).first()
    if plan:
        # Improved version numbering: Find the max version number and increment it
        new_version_number = session.query(PlanVersion).filter_by(plan_id=plan.id).count() + 1
        new_version = PlanVersion(plan_id=plan.id, version_number=new_version_number, content=content)
        session.add(new_version)
        session.commit()

        # Log the action after saving the new version
        log_action(plan.owner_id, f"Saved version {new_version_number} of plan '{plan.title}'")
        print(f"Version {new_version_number} of plan '{plan.title}' saved successfully.")
    else:
        print(f"Plan with ID {plan_id} not found.")

def create_plan(title, plan_type, username, framework):
    """Create a new DRP or IRP plan."""
    user = session.query(User).filter_by(username=username).first()  # User model used here
    if user:
        new_plan = Plan(title=title, plan_type=plan_type, owner_id=user.id)
        session.add(new_plan)
        session.commit()

        # Save the first version
        save_plan_version(new_plan.id, f"Initial content for {plan_type} plan.")
        print(f"Plan '{title}' ({plan_type}) created successfully.")
    else:
        print(f"User '{username}' not found.")

def rollback_plan(plan_id, version_number):
    """Rollback a plan to a previous version."""
    plan = session.query(Plan).filter_by(id=plan_id).first()
    if plan:
        # Get the specific version
        version_to_rollback = session.query(PlanVersion).filter_by(plan_id=plan_id, version_number=version_number).first()
        if version_to_rollback:
            plan.versions = [version_to_rollback]  # Rollback to that version
            session.commit()

            # Log the rollback action
            log_action(plan.owner_id, f"Rolled back plan '{plan.title}' to version {version_number}")
            print(f"Plan '{plan.title}' rolled back to version {version_number}.")
        else:
            print(f"Version {version_number} not found for plan '{plan.title}'.")
    else:
        print(f"Plan with ID {plan_id} not found.")

def list_plan_versions(plan_id):
    """List all versions of a specific plan."""
    plan = session.query(Plan).filter_by(id=plan_id).first()
    if plan:
        versions = plan.versions
        for version in versions:
            print(f"Version {version.version_number}, Created at {version.created_at}")
    else:
        print(f"Plan with ID {plan_id} not found.")

def list_plans():
    """List all plans."""
    plans = session.query(Plan).all()
    for plan in plans:
        print(f"ID: {plan.id}, Title: {plan.title}, Type: {plan.plan_type}, Owner: {plan.owner.username}")

def delete_plan(plan_id):
    """Delete a plan."""
    plan = session.query(Plan).filter_by(id=plan_id).first()
    if plan:
        session.delete(plan)
        session.commit()
        print(f"Plan '{plan.title}' deleted successfully.")
    else:
        print(f"Plan with ID {plan_id} not found.")
