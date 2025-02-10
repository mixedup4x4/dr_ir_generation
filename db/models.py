from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime, UTC  # ✅ Import timezone-aware datetime

Base = declarative_base()

# User Table
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)  # admin, approver, editor, viewer
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))  # ✅ Fixed

# Plan Table (Stores DRP/IRP Metadata)
class Plan(Base):
    __tablename__ = 'plans'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    plan_type = Column(String(10), nullable=False)  # drp or irp
    owner_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))  # ✅ Fixed
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))  # ✅ Fixed
    
    owner = relationship("User", back_populates="plans")

# User-to-Plan Relationship
User.plans = relationship("Plan", order_by=Plan.id, back_populates="owner")

# Plan Versions (Tracks history)
class PlanVersion(Base):
    __tablename__ = 'plan_versions'
    
    id = Column(Integer, primary_key=True)
    plan_id = Column(Integer, ForeignKey('plans.id'))
    version_number = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)  # Markdown content
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))  # ✅ Fixed
    
    plan = relationship("Plan", back_populates="versions")

Plan.versions = relationship("PlanVersion", order_by=PlanVersion.id, back_populates="plan")

# Logs Table (Audit Trail)
class Log(Base):
    __tablename__ = 'logs'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    action = Column(String(255), nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(UTC))  # ✅ Fixed
    
    user = relationship("User", back_populates="logs")

User.logs = relationship("Log", order_by=Log.id, back_populates="user")
