import typer
from scripts.auth import create_user, authenticate_user, check_permission
from db.query import (
    create_plan, list_plans, delete_plan, save_plan_version, list_plan_versions,
    rollback_plan, export_plan_to_markdown, export_plan_to_json, export_plan_to_pdf
)
from db.database_setup import init_db
from sqlalchemy.orm import sessionmaker
from db.models import Log
from db.database_setup import DATABASE_URL
from sqlalchemy import create_engine

app = typer.Typer()

# Set up database connection
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

@app.command()
def init():
    """Initialize the database."""
    init_db()
    print("Database initialized.")

@app.command()
def add_user(username: str, password: str, role: str = typer.Option("viewer", help="Role of the user (admin, approver, editor, viewer)")):
    """Add a new user with a specific role."""
    create_user(username, password, role)

@app.command()
def login(username: str, password: str):
    """Authenticate a user."""
    user = authenticate_user(username, password)
    if user:
        typer.echo(f"Logged in as {user.username} (Role: {user.role})")
    else:
        typer.echo("Login failed. Invalid credentials.")

@app.command()
def create_plan_cli(username: str, password: str, title: str, plan_type: str, content: str):
    """Create a new DRP or IRP plan."""
    user = authenticate_user(username, password)
    if not user:
        typer.echo("Authentication failed.")
        return
    
    if not check_permission(user, "editor"):
        typer.echo("Access denied: You do not have permission to create plans.")
        return
    
    create_plan(title, plan_type, username, content)

@app.command()
def list_plans_cli():
    """List all plans."""
    list_plans()

@app.command()
def delete_plan_cli(username: str, password: str, plan_id: int):
    """Delete a plan."""
    user = authenticate_user(username, password)
    if not user:
        typer.echo("Authentication failed.")
        return
    
    if not check_permission(user, "admin"):
        typer.echo("Access denied: Only admins can delete plans.")
        return
    
    delete_plan(plan_id)

@app.command()
def save_plan_version_cli(username: str, password: str, plan_id: int, content: str):
    """Save a new version of an existing plan."""
    user = authenticate_user(username, password)
    if not user:
        typer.echo("Authentication failed.")
        return
    
    if not check_permission(user, "editor"):
        typer.echo("Access denied: You do not have permission to modify plans.")
        return
    
    save_plan_version(plan_id, content)

@app.command()
def list_plan_versions_cli(plan_id: int):
    """List all versions of a plan."""
    list_plan_versions(plan_id)

@app.command()
def rollback_plan_cli(username: str, password: str, plan_id: int, version_number: int):
    """Rollback a plan to a previous version."""
    user = authenticate_user(username, password)
    if not user:
        typer.echo("Authentication failed.")
        return
    
    if not check_permission(user, "editor"):
        typer.echo("Access denied: You do not have permission to rollback plans.")
        return
    
    rollback_plan(plan_id, version_number)

@app.command()
def export_plan_markdown_cli(plan_id: int):
    """Export a plan to Markdown format."""
    export_plan_to_markdown(plan_id)

@app.command()
def export_plan_json_cli(plan_id: int):
    """Export a plan to JSON format."""
    export_plan_to_json(plan_id)

@app.command()
def export_plan_pdf_cli(plan_id: int):
    """Export a plan to PDF format."""
    export_plan_to_pdf(plan_id)

@app.command()
def view_logs(username: str, password: str):
    """Allow admins to view audit logs."""
    user = authenticate_user(username, password)
    if not user or not check_permission(user, "admin"):
        typer.echo("Access denied: Only admins can view logs.")
        return
    
    logs = session.query(Log).all()
    if not logs:
        typer.echo("No logs found.")
        return
    
    for log in logs:
        typer.echo(f"[{log.timestamp}] - {log.action}")

if __name__ == "__main__":
    app()
