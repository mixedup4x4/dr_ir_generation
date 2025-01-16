#!/bin/bash

# Directories for templates and outputs
TEMPLATE_DIR="templates"
DRP_OUTPUT_DIR="outputs/drp"
IRP_OUTPUT_DIR="outputs/irp"

# Template files
DRP_TEMPLATE_FILE="$TEMPLATE_DIR/drp_master_template.md"
IRP_TEMPLATE_FILE="$TEMPLATE_DIR/irp_master_template.md"

# Initialize directories
initialize_directories() {
    mkdir -p "$TEMPLATE_DIR" "$DRP_OUTPUT_DIR" "$IRP_OUTPUT_DIR"
}

# Display the main menu
show_main_menu() {
    clear
    echo "======================================="
    echo "     Interactive Policy Generator      "
    echo "======================================="
    echo "1. Create/Manage Disaster Recovery Plans (DRP)"
    echo "2. Create/Manage Incident Response Plans (IRP)"
    echo "3. Exit"
    echo "======================================="
    read -p "Choose an option [1-3]: " main_choice
}

# Display the sub-menu for managing plans
show_plan_menu() {
    local plan_type="$1"
    clear
    echo "======================================="
    echo "   Manage $plan_type Plans             "
    echo "======================================="
    echo "1. Create a New $plan_type"
    echo "2. View/Edit Existing $plan_type"
    echo "3. Delete a $plan_type"
    echo "4. Exit to Main Menu"
    echo "======================================="
    read -p "Choose an option [1-4]: " plan_choice
}

# List all plans in a directory
list_plans() {
    local plan_dir="$1"
    echo "======================================="
    echo "   Existing Plans                     "
    echo "======================================="
    if [[ -d "$plan_dir" && $(ls "$plan_dir" 2>/dev/null) ]]; then
        ls "$plan_dir" | sed 's/.md$//' # Display plans without .md extension
    else
        echo "No plans found."
    fi
    echo "======================================="
}

# Create a new plan interactively
create_plan() {
    local template_file="$1"
    local plan_dir="$2"
    local plan_type="$3"

    read -p "Enter a unique name for the new $plan_type: " plan_name
    local plan_path="$plan_dir/$plan_name.md"

    if [[ -f "$plan_path" ]]; then
        echo "A plan with this name already exists. Choose another name."
        return
    fi

    cp "$template_file" "$plan_path"
    echo "$plan_type template created. Let's fill in the details interactively."

    fill_plan_interactively "$plan_path" "$plan_type"
}

# Fill in the plan interactively
fill_plan_interactively() {
    local plan_path="$1"
    local plan_type="$2"

    echo "Filling out the $plan_type interactively..."
    echo "Leave blank to skip any field."

    # Common sections for both DRP and IRP
    read -p "Enter the purpose of the $plan_type: " purpose
    echo "## Purpose" > "$plan_path"
    echo "$purpose" >> "$plan_path"
    echo "" >> "$plan_path"

    read -p "Enter objectives (comma-separated): " objectives
    echo "## Objectives" >> "$plan_path"
    echo "$objectives" >> "$plan_path"
    echo "" >> "$plan_path"

    read -p "Enter scope (what systems/assets are covered): " scope
    echo "## Scope" >> "$plan_path"
    echo "$scope" >> "$plan_path"
    echo "" >> "$plan_path"

    echo "Entering Key Contacts (Press Enter to skip any contact)..."
    echo "## Key Contacts and Roles" >> "$plan_path"

    for role in "Coordinator" "IT Lead" "Communication Lead" "Business Process Owner"; do
        read -p "Enter name for $role: " name
        read -p "Enter contact information for $role: " contact_info
        echo "- **$role**: $name, $contact_info" >> "$plan_path"
    done

    # Specific sections for DRP
    if [[ "$plan_type" == "DRP" ]]; then
        echo "Entering Risk Assessment..."
        echo "## Risk Assessment" >> "$plan_path"

        read -p "Describe threats (e.g., natural disasters, cyberattacks): " threats
        echo "### Threat Analysis" >> "$plan_path"
        echo "$threats" >> "$plan_path"
        echo "" >> "$plan_path"

        read -p "Enter Recovery Time Objective (RTO) examples: " rto
        echo "### Business Impact Analysis (BIA)" >> "$plan_path"
        echo "**Recovery Time Objective (RTO):** $rto" >> "$plan_path"
        echo "" >> "$plan_path"
    fi

    # Specific sections for IRP
    if [[ "$plan_type" == "IRP" ]]; then
        echo "Entering Incident Categories..."
        echo "## Incident Categories" >> "$plan_path"

        read -p "Describe incident categories (e.g., malware, insider threats): " categories
        echo "### Classification of Incidents" >> "$plan_path"
        echo "$categories" >> "$plan_path"
        echo "" >> "$plan_path"

        read -p "Enter tools/resources used (e.g., Splunk, Carbon Black): " tools
        echo "### Tools and Resources" >> "$plan_path"
        echo "$tools" >> "$plan_path"
        echo "" >> "$plan_path"
    fi

    echo "Details have been added to $plan_type. You can view or edit it later."
}

# View or edit an existing plan
view_or_edit_plan() {
    local plan_dir="$1"
    local plan_type="$2"

    list_plans "$plan_dir"
    read -p "Enter the name of the $plan_type to view/edit: " plan_name
    local plan_path="$plan_dir/$plan_name.md"

    if [[ -f "$plan_path" ]]; then
        echo "======================================="
        echo "   Viewing/Editing $plan_name          "
        echo "======================================="
        cat "$plan_path"
        echo "======================================="
        read -p "Press Enter to continue editing interactively..."

        fill_plan_interactively "$plan_path" "$plan_type"
    else
        echo "$plan_type '$plan_name' not found."
    fi
}

# Delete a plan
delete_plan() {
    local plan_dir="$1"
    local plan_type="$2"

    list_plans "$plan_dir"
    read -p "Enter the name of the $plan_type to delete: " plan_name
    local plan_path="$plan_dir/$plan_name.md"

    if [[ -f "$plan_path" ]]; then
        rm "$plan_path"
        echo "$plan_type '$plan_name' deleted."
    else
        echo "$plan_type '$plan_name' not found."
    fi
}

# Main program loop
initialize_directories

while true; do
    show_main_menu
    case $main_choice in
        1)
            while true; do
                show_plan_menu "Disaster Recovery Plan (DRP)"
                case $plan_choice in
                    1) create_plan "$DRP_TEMPLATE_FILE" "$DRP_OUTPUT_DIR" "DRP" ;;
                    2) view_or_edit_plan "$DRP_OUTPUT_DIR" "DRP" ;;
                    3) delete_plan "$DRP_OUTPUT_DIR" "DRP" ;;
                    4) break ;;
                    *) echo "Invalid option. Try again." ;;
                esac
            done
            ;;
        2)
            while true; do
                show_plan_menu "Incident Response Plan (IRP)"
                case $plan_choice in
                    1) create_plan "$IRP_TEMPLATE_FILE" "$IRP_OUTPUT_DIR" "IRP" ;;
                    2) view_or_edit_plan "$IRP_OUTPUT_DIR" "IRP" ;;
                    3) delete_plan "$IRP_OUTPUT_DIR" "IRP" ;;
                    4) break ;;
                    *) echo "Invalid option. Try again." ;;
                esac
            done
            ;;
        3) echo "Goodbye!" ; exit 0 ;;
        *) echo "Invalid option. Try again." ;;
    esac
done
