from db.query import create_user, create_plan, delete_plan, delete_user
from werkzeug.security import generate_password_hash

# Create sample users
def add_sample_users():
    users = [
        ("admin", "adminPass123", "admin"),
        ("editor1", "EditorPass123", "editor"),
        ("viewer1", "ViewerPass123", "viewer")
    ]
    
    for username, password, role in users:
        create_user(username, password, role)
        print(f"Created user: {username} with role: {role}")

# Create sample DRP/IRP plans
def add_sample_plans():
    plans = [
        ("CyberSecurity Recovery Plan", "drp", "admin", "nist"),
        ("Disaster Recovery Plan", "drp", "editor1", "nist"),
        ("Incident Response Plan", "irp", "editor1", "nist")
    ]
    
    for title, plan_type, username, framework in plans:
        create_plan(title, plan_type, username, framework)
        print(f"Created plan: {title} of type {plan_type}")

# Remove all sample users and plans
def remove_sample_data():
    users_to_remove = ["admin", "editor1", "viewer1"]
    for username in users_to_remove:
        delete_user(username)
        print(f"Deleted user: {username}")
    
    # Delete all plans (you can specify plan ids or delete all based on your needs)
    plans = [1, 2, 3]  # Use actual plan IDs to delete, or loop through all
    for plan_id in plans:
        delete_plan(plan_id)
        print(f"Deleted plan with ID: {plan_id}")

if __name__ == "__main__":
    print("🔄 Populating sample data...")
    add_sample_users()
    add_sample_plans()

    print("\n💥 Removing sample data...")
    remove_sample_data()
