import logging
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from db.database_setup import session
from db.models import User, Plan, Log, PlanVersion

# Ensure logging is configured
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# User Management
def create_user(username, password, role):
    """Create a new user with a hashed password."""
    existing_user = session.query(User).filter_by(username=username).first()
    if existing_user:
        logging.warning(f"User '{username}' already exists. Skipping creation.")
        return existing_user  # Avoid duplicate users

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password_hash=hashed_password, role=role)
    session.add(new_user)

    try:
        session.commit()
        logging.info(f"User '{username}' created successfully with role '{role}'.")
        return new_user
    except IntegrityError:
        session.rollback()
        logging.error(f"User '{username}' could not be created due to a database constraint error.")
        return None
    except Exception as e:
        session.rollback()
        logging.error(f"Failed to create user '{username}': {e}")
        return None

def authenticate_user(username, password):
    """Authenticate user by verifying password."""
    try:
        user = session.query(User).filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            logging.info(f"User '{username}' authenticated successfully. Role: {user.role}")
            return user
        else:
            logging.warning("Login failed. Invalid credentials.")
            return None
    except Exception as e:
        logging.error(f"Authentication error: {e}")
        return None

# Plan Management
def create_plan(title, plan_type, username, framework):
    """Create a DRP or IRP plan associated with a user."""
    try:
        user = session.query(User).filter_by(username=username).first()
        if not user:
            logging.error(f"User '{username}' not found. Cannot create plan.")
            return None

        new_plan = Plan(title=title, plan_type=plan_type, owner_id=user.id)
        session.add(new_plan)
        session.commit()
        logging.info(f"Plan '{title}' ({plan_type}) created successfully.")
        return new_plan
    except Exception as e:
        session.rollback()
        logging.error(f"Plan creation failed: {e}")
        return None

def list_plans():
    """List all plans with error handling."""
    try:
        plans = session.query(Plan).all()
        for plan in plans:
            owner_name = plan.owner.username if plan.owner else "[None]"
            logging.info(f"Plan ID: {plan.id}, Title: {plan.title}, Type: {plan.plan_type}, Owner: {owner_name}")
        return plans
    except Exception as e:
        session.rollback()
        logging.error(f"Error retrieving plans: {e}")
        return []

# Logging Actions
def log_action(user_id, action):
    """Log user actions."""
    try:
        new_log = Log(user_id=user_id, action=action)
        session.add(new_log)
        session.commit()
        logging.info(f"Logged action: {action}")
    except Exception as e:
        session.rollback()
        logging.error(f"Failed to log action: {e}")
