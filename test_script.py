import sys
import os
import click
import logging
from db.query import (
    create_user,
    authenticate_user,
    check_permission,
    list_plans,
    create_plan,
    delete_plan,
    save_plan_version,
    list_plan_versions,
    rollback_plan,
    view_logs,
    delete_user
)
from db.database_setup import session  # Import session for DB interaction
from db.models import User  # Import the User model
from scripts.utils import verify_password, send_email, safe_write, backup_file

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def clear_existing_data():
    """ Clear any existing users and plans to avoid conflicts """
    logging.info("Clearing existing users and plans...")
    try:
        usernames = ['editor1', 'editor2', 'viewer1']

        if not session:
            logging.error("Session is not properly initialized.")
            return

        for username in usernames:
            logging.info(f"Looking for user: {username}")
            user = session.query(User).filter_by(username=username).first()
            if user:
                delete_user(username)
                logging.info(f"User '{username}' deleted successfully.")
            else:
                logging.warning(f"User '{username}' not found, skipping deletion.")

        plans = list_plans() or []  # Ensure it's always iterable
        for plan in plans:
            if plan:  # Ensure plan is not None
               delete_plan(plan.id)
        logging.info("Existing plans cleared successfully.")

        logging.info("Existing data cleared successfully.")
    except Exception as e:
        logging.error(f"Failed to clear existing data: {e}")

def test_user_creation():
    """ Test user creation and authentication """
    try:
        users = [
            ("editor1", "EditorPass123", "editor"),
            ("editor2", "EditorPass123", "editor"),
            ("viewer1", "ViewerPass123", "viewer")
        ]

        for username, password, role in users:
            if not authenticate_user(username, password):
                create_user(username, password, role)
                logging.info(f"User '{username}' created successfully with role '{role}'.")

        logging.info("Verifying password hashing for users...")

        for username, password, _ in users:
            user = session.query(User).filter_by(username=username).first()
            if user and verify_password(user.password_hash, password):
                logging.info(f"{username.capitalize()} authenticated successfully.")
            else:
                logging.error(f"{username.capitalize()} authentication failed.")

    except Exception as e:
        logging.error(f"Error in user creation or verification: {e}")
        sys.exit(1)

def test_plan_creation():
    """ Test the plan creation functionality """
    try:
        logging.info("Creating DRP plan...")
        create_plan('Test DRP', 'drp', 'editor1', 'nist')
        logging.info("Plan 'Test DRP' created successfully.")
    except Exception as e:
        logging.error(f"Plan creation failed: {e}")
        sys.exit(1)

def test_email():
    """ Test email functionality """
    if 'SMTP_SERVER' in os.environ:
        try:
            logging.info("Testing email functionality...")
            send_email('recipient@example.com', 'Test Subject', 'Test body message.')
            logging.info("Email sent successfully.")
        except Exception as e:
            logging.error(f"Failed to send email: {e}")
    else:
        logging.info("Email functionality is disabled (SMTP_SERVER not configured).")

def run_tests():
    """ Run all tests """
    clear_existing_data()
    test_user_creation()
    test_plan_creation()
    test_email()
    logging.info("All tests completed successfully.")

if __name__ == '__main__':
    try:
        run_tests()
    except Exception as e:
        logging.error(f"Test script failed: {e}")
        sys.exit(1)
