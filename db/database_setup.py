from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base

# Define the database URL
DATABASE_URL = "sqlite:///dr_ir_generation.db"  # Update to your database URL (PostgreSQL, SQLite, etc.)

# Create an engine to connect to the database
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})  # For SQLite

# Create a sessionmaker instance to handle database transactions
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the tables in the database
Base.metadata.create_all(bind=engine)

# Create a session instance for use in query.py
session = Session()

def init_db():
    """Initialize the database (called once during app initialization)."""
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully.")
