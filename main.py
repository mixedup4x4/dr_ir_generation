import click
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))
from db.query import create_user, authenticate_user, check_permission, list_plans, delete_plan, save_plan_version, list_plan_versions, rollback_plan, view_logs, delete_user

from db.database_setup import init_db

@click.group()
def cli():
    """Command-line interface for managing DRP/IRP plans."""
    pass

@cli.command()
def init():
    """Initialize the database."""
    init_db()
    click.echo("Database initialized.")

@cli.command()
@click.argument('username')
@click.argument('password')
@click.option('--role', default='viewer', help="Role of the user (admin, approver, editor, viewer)")
def add_user(username, password, role):
    """Add a new user with a specific role."""
    create_user(username, password, role)

@cli.command()
@click.argument('username')
@click.argument('password')
def login(username, password):
    """Authenticate a user."""
    user = authenticate_user(username, password)
    if user:
        click.echo(f"Logged in as {user.username} (Role: {user.role})")
    else:
        click.echo("Login failed. Invalid credentials.")

@cli.command()
@click.argument('username')
@click.argument('title')
@click.argument('plan_type')
@click.argument('framework')
def create_plan_cli(username, title, plan_type, framework):
    """Create a new DRP or IRP plan."""
    user = authenticate_user(username, "fake")  # Simulating login
    if not user:
        click.echo("Authentication failed.")
        return

    if not check_permission(user, "editor"):
        click.echo("Access denied: You do not have permission to create plans.")
        return

    create_plan(title, plan_type, username, framework)

@cli.command()
def list_plans_cli():
    """List all plans."""
    list_plans()

@cli.command()
@click.argument('username')
@click.argument('plan_id', type=int)
def delete_plan_cli(username, plan_id):
    """Delete a plan."""
    user = authenticate_user(username, "fake")  # Simulating login
    if not user:
        click.echo("Authentication failed.")
        return

    if not check_permission(user, "admin"):
        click.echo("Access denied: Only admins can delete plans.")
        return

    delete_plan(plan_id)

@cli.command()
@click.argument('username')
def delete_user_cli(username):
    """Delete a user by their username."""
    delete_user(username)

@cli.command()
@click.argument('username')
@click.argument('password')
def view_logs_cli(username, password):
    """View logs of actions taken."""
    user = authenticate_user(username, password)
    if not user:
        click.echo("Authentication failed.")
        return

    if not check_permission(user, "admin"):
        click.echo("Access denied: Only admins can view logs.")
        return

    logs = view_logs(user)
    if logs:
        for log in logs:
            click.echo(f"{log.timestamp} - {log.action}")
    else:
        click.echo("No logs found.")

if __name__ == "__main__":
    cli()
