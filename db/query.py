import json
import os
import markdown
from sqlalchemy.orm import sessionmaker
from db.models import Plan, PlanVersion, Log, User
from db.database_setup import DATABASE_URL
from sqlalchemy import create_engine
from weasyprint import HTML

# Ensure the outputs directory exists
os.makedirs("outputs", exist_ok=True)

# Set up database connection
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def log_action(user_id, action):
    """Logs a user action for auditing purposes.""" 
    new_log = Log(user_id=user_id, action=action)
    session.add(new_log)
    session.commit()

def create_plan(title, plan_type, owner_username, content):
    """Creates a new DRP or IRP plan and saves the initial version."""
    owner = session.query(User).filter_by(username=owner_username).first()
    if not owner:
        print("Error: Owner does not exist.")
        return False
    
    new_plan = Plan(title=title, plan_type=plan_type, owner_id=owner.id)
    session.add(new_plan)
    session.commit()

    # Save the first version of the plan
    save_plan_version(new_plan.id, content)

    log_action(owner.id, f"Created {plan_type.upper()} plan: '{title}'")
    print(f"Plan '{title}' ({plan_type.upper()}) created successfully.")
    return True

def list_plans():
    """Lists all plans."""
    plans = session.query(Plan).all()
    if not plans:
        print("No plans found.")
        return
    
    for plan in plans:
        print(f"[{plan.id}] {plan.title} ({plan.plan_type.upper()}) - Owner: {plan.owner.username}")

def delete_plan(plan_id):
    """Deletes a plan."""
    plan = session.query(Plan).filter_by(id=plan_id).first()
    if not plan:
        print("Error: Plan not found.")
        return False
    
    log_action(plan.owner_id, f"Deleted {plan.plan_type.upper()} plan: '{plan.title}'")
    session.delete(plan)
    session.commit()
    print(f"Plan '{plan.title}' deleted.")
    return True

def save_plan_version(plan_id, content):
    """Creates a new version of a plan."""
    plan = session.query(Plan).filter_by(id=plan_id).first()
    if not plan:
        print("Error: Plan not found.")
        return False
    
    # Determine the next version number
    latest_version = session.query(PlanVersion).filter_by(plan_id=plan_id).order_by(PlanVersion.version_number.desc()).first()
    next_version = (latest_version.version_number + 1) if latest_version else 1

    new_version = PlanVersion(plan_id=plan_id, version_number=next_version, content=content)
    session.add(new_version)
    session.commit()

    log_action(plan.owner_id, f"Saved version {next_version} of plan '{plan.title}'")
    print(f"Version {next_version} of plan '{plan.title}' saved successfully.")
    return True

def list_plan_versions(plan_id):
    """Lists all versions of a specific plan."""
    versions = session.query(PlanVersion).filter_by(plan_id=plan_id).order_by(PlanVersion.version_number).all()
    if not versions:
        print("No versions found for this plan.")
        return
    
    print(f"Versions for Plan ID {plan_id}:")
    for version in versions:
        print(f" - Version {version.version_number}, Created at {version.created_at}")

def rollback_plan(plan_id, version_number):
    """Rolls back a plan to a specific version."""
    version = session.query(PlanVersion).filter_by(plan_id=plan_id, version_number=version_number).first()
    if not version:
        print(f"Error: Version {version_number} not found for Plan ID {plan_id}.")
        return False

    save_plan_version(plan_id, version.content)

    plan = session.query(Plan).filter_by(id=plan_id).first()
    log_action(plan.owner_id, f"Rolled back plan '{plan.title}' to version {version_number}")
    print(f"Plan '{plan.title}' rolled back to version {version_number}.")
    return True

def export_plan_to_markdown(plan_id):
    """Exports a plan's latest version to Markdown format."""
    plan = session.query(Plan).filter_by(id=plan_id).first()
    if not plan:
        print("Error: Plan not found.")
        return False
    
    latest_version = session.query(PlanVersion).filter_by(plan_id=plan_id).order_by(PlanVersion.version_number.desc()).first()
    if not latest_version:
        print("Error: No versions available for this plan.")
        return False

    markdown_content = f"""# {plan.title}

**Plan Type:** {plan.plan_type.upper()}

## Latest Version ({latest_version.version_number})

{latest_version.content}
"""

    output_path = f"outputs/{plan.plan_type.lower()}_{plan_id}.md"
    with open(output_path, "w") as f:
        f.write(markdown_content)
    
    log_action(plan.owner_id, f"Exported plan '{plan.title}' to Markdown.")
    print(f"✅ Plan exported to {output_path}")
    return output_path

def export_plan_to_json(plan_id):
    """Exports a plan's latest version to JSON format."""
    plan = session.query(Plan).filter_by(id=plan_id).first()
    if not plan:
        print("Error: Plan not found.")
        return False
    
    latest_version = session.query(PlanVersion).filter_by(plan_id=plan_id).order_by(PlanVersion.version_number.desc()).first()
    if not latest_version:
        print("Error: No versions available for this plan.")
        return False

    json_data = {
        "title": plan.title,
        "plan_type": plan.plan_type,
        "latest_version": latest_version.version_number,
        "content": latest_version.content
    }

    output_path = f"outputs/{plan.plan_type.lower()}_{plan_id}.json"
    with open(output_path, "w") as f:
        json.dump(json_data, f, indent=4)
    
    log_action(plan.owner_id, f"Exported plan '{plan.title}' to JSON.")
    print(f"✅ Plan exported to {output_path}")
    return output_path

def export_plan_to_pdf(plan_id):
    """Exports a plan's latest version to PDF format."""
    markdown_path = export_plan_to_markdown(plan_id)
    if not markdown_path:
        return False

    # Convert Markdown to HTML
    with open(markdown_path, "r") as f:
        markdown_content = f.read()

    html_content = markdown.markdown(markdown_content)
    pdf_output_path = markdown_path.replace(".md", ".pdf")

    # Convert HTML to PDF
    HTML(string=html_content).write_pdf(pdf_output_path)

    plan = session.query(Plan).filter_by(id=plan_id).first()
    log_action(plan.owner_id, f"Exported plan '{plan.title}' to PDF.")
    print(f"✅ Plan exported to {pdf_output_path}")
    return pdf_output_path
