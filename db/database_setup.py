import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from db.models import Base
from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///dr_ir_generation.db"  # Change for PostgreSQL if needed

def init_db():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    print("Database initialized successfully.")

if __name__ == "__main__":
    init_db()
