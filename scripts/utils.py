import os
import re
import logging
import random
import string
import shutil
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from werkzeug.security import generate_password_hash, check_password_hash

# Password Hashing
def generate_hash(password: str) -> str:
    """Generate a hashed password."""
    return generate_password_hash(password)

def verify_password(stored_hash: str, password: str) -> bool:
    """Verify a password against a stored hash."""
    return check_password_hash(stored_hash, password)

# File Handling Utilities
def safe_write(file_path, content):
    """Safely writes content to a file, creating it if necessary."""
    try:
        with open(file_path, 'w') as file:
            file.write(content)
    except Exception as e:
        logging.error(f"Error writing to {file_path}: {e}")

def backup_file(file_path):
    """Backup a file by appending a timestamp."""
    if os.path.exists(file_path):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{file_path}_{timestamp}.bak"
        shutil.copy(file_path, backup_path)
        logging.info(f"Backup created: {backup_path}")
    else:
        logging.warning("File not found.")

# String Manipulation
def sanitize_string(input_string):
    """Sanitize a string by trimming whitespace and removing unwanted characters."""
    return input_string.strip().replace("\n", "").replace("\r", "")

def generate_random_string(length=16):
    """Generate a random alphanumeric string."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Date and Time Helpers
def format_datetime(datetime_obj) -> str:
    """Return a formatted datetime string."""
    return datetime_obj.strftime('%Y-%m-%d %H:%M:%S')

def get_current_timestamp():
    """Return the current timestamp in a standardized format."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Validation Utilities
def validate_email(email):
    """Check if the provided email address is valid."""
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(pattern, email))

def validate_url(url):
    """Validate if the provided string is a proper URL."""
    pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
    return bool(re.match(pattern, url))

# Logging Helper
def setup_logging(log_file="app.log"):
    """Set up logging configuration."""
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ])

def log_message(message, level="INFO"):
    """Log a custom message at the specified level."""
    levels = {
        "INFO": logging.info,
        "ERROR": logging.error,
        "WARNING": logging.warning,
        "DEBUG": logging.debug
    }
    levels.get(level.upper(), logging.info)(message)

# Database Helpers
from db.database_setup import session
from db.models import Plan, User

def get_all_plans():
    """Retrieve all plans from the database."""
    return session.query(Plan).all()

def get_user_by_id(user_id):
    """Retrieve user by ID."""
    return session.query(User).filter(User.id == user_id).first()

# File and Directory Operations
def file_exists(file_path):
    """Check if a file or directory exists."""
    return os.path.exists(file_path)

# Data Formatting Functions
def format_currency(amount):
    """Format a number as currency."""
    return "${:,.2f}".format(amount)

def format_bullet_list(items):
    """Format a list of items into bullet points."""
    return "\n".join([f"- {item}" for item in items])

# Email Utility (SMTP)
def send_email(to_address, subject, body, from_address="noreply@example.com"):
    """Send an email."""
    try:
        msg = MIMEMultipart()
        msg['From'] = from_address
        msg['To'] = to_address
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Establish SMTP connection
        with smtplib.SMTP('smtp.example.com', 587) as server:
            server.starttls()
            server.login(from_address, "your_email_password")
            text = msg.as_string()
            server.sendmail(from_address, to_address, text)
            logging.info("Email sent successfully.")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")

# Plan Management
def get_plan_by_id(plan_id):
    """Retrieve plan by ID."""
    return session.query(Plan).filter(Plan.id == plan_id).first()

def delete_plan_by_id(plan_id):
    """Delete a plan by ID."""
    plan = session.query(Plan).filter(Plan.id == plan_id).first()
    if plan:
        session.delete(plan)
        session.commit()
        logging.info(f"Plan {plan_id} deleted.")
    else:
        logging.warning(f"Plan with ID {plan_id} not found.")
