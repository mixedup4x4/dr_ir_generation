#!/bin/bash

# Directories for templates and outputs
TEMPLATE_DIR="templates"
DRP_OUTPUT_DIR="outputs/drp"
IRP_OUTPUT_DIR="outputs/irp"

# Files for templates
DRP_TEMPLATE_FILE="$TEMPLATE_DIR/drp_master_template.md"
IRP_TEMPLATE_FILE="$TEMPLATE_DIR/irp_master_template.md"

# Function to display the main menu
show_menu() {
    clear
    echo "==============================="
    echo "   Management Program Script   "
    echo "==============================="
    echo "1. Manage Disaster Recovery Plans (DRPs)"
    echo "2. Manage Incident Response Plans (IRPs)"
    echo "3. Help"
    echo "4. Exit"
    echo "==============================="
    read -p "Choose an option [1-4]: " main_choice
}

# Function to display the sub-menu for managing plans
show_plan_menu() {
    local plan_type="$1"
    clear
    echo "==============================="
    echo "   $plan_type Management Menu   "
    echo "==============================="
    echo "1. Create New $plan_type"
    echo "2. List Existing $plan_type"
    echo "3. View/Edit a $plan_type"
    echo "4. Delete a $plan_type"
    echo "5. Generate Final Draft (.docx)"
    echo "6. Help"
    echo "7. Return to Main Menu"
    echo "==============================="
    read -p "Choose an option [1-7]: " plan_choice
}

# Function to initialize directories and templates
initialize_directories() {
    mkdir -p "$TEMPLATE_DIR" "$DRP_OUTPUT_DIR" "$IRP_OUTPUT_DIR"
}

# Function to list existing plans
list_plans() {
    local plan_type="$1"
    local plan_dir="$2"

    if [[ -d "$plan_dir" ]]; then
        echo "==============================="
        echo "   Existing $plan_type Plans   "
        echo "==============================="
        local plans=("$(ls "$plan_dir" 2>/dev/null)")
        if [[ ${#plans[@]} -gt 0 ]]; then
            for plan in "$plan_dir"/*.md; do
                echo "$(basename "$plan" .md)"
            done
        else
            echo "No $plan_type plans found."
        fi
    else
        echo "No $plan_type plans directory found."
    fi
    echo
    read -p "Press Enter to return to the menu..."
}

# Function to create a new plan
create_plan() {
    local template_file="$1"
    local plan_dir="$2"
    local plan_type="$3"

    read -p "Enter a unique name for the new $plan_type (e.g., 'DRP_ProjectX'): " plan_name
    local save_file="$plan_dir/$plan_name.md"

    if [[ -f "$save_file" ]]; then
        echo "A plan with this name already exists. Choose another name."
        return
    fi

    cp "$template_file" "$save_file"
    echo "New $plan_type created: $plan_name"
}

# Function to view or edit a plan
view_plan() {
    local plan_type="$1"
    local plan_dir="$2"

    list_plans "$plan_type" "$plan_dir"
    read -p "Enter the name of the $plan_type to view/edit: " plan_name
    local plan_file="$plan_dir/$plan_name.md"

    if [[ -f "$plan_file" ]]; then
        nano "$plan_file"
    else
        echo "$plan_type '$plan_name' not found."
    fi
}

# Function to delete a plan
delete_plan() {
    local plan_type="$1"
    local plan_dir="$2"

    list_plans "$plan_type" "$plan_dir"
    read -p "Enter the name of the $plan_type to delete: " plan_name
    local plan_file="$plan_dir/$plan_name.md"

    if [[ -f "$plan_file" ]]; then
        rm "$plan_file"
        echo "$plan_type '$plan_name' deleted."
    else
        echo "$plan_type '$plan_name' not found."
    fi
}

# Function to generate a final draft in .docx format
generate_docx() {
    local plan_type="$1"
    local plan_dir="$2"

    list_plans "$plan_type" "$plan_dir"
    read -p "Enter the name of the $plan_type to generate (.docx): " plan_name
    local save_file="$plan_dir/$plan_name.md"
    local docx_file="$plan_dir/$plan_name.docx"

    if [[ -f "$save_file" ]]; then
        echo "Generating final draft for $plan_name in .docx format..."
        pandoc "$save_file" -o "$docx_file" --standalone
        echo "Draft saved as $docx_file."
    else
        echo "$plan_type '$plan_name' not found."
    fi
}

# Initialize directories
initialize_directories

# Main program loop
while true; do
    show_menu
    case $main_choice in
    1)
        while true; do
            show_plan_menu "Disaster Recovery Plan (DRP)"
            case $plan_choice in
            1) create_plan "$DRP_TEMPLATE_FILE" "$DRP_OUTPUT_DIR" "DRP" ;;
            2) list_plans "DRP" "$DRP_OUTPUT_DIR" ;;
            3) view_plan "DRP" "$DRP_OUTPUT_DIR" ;;
            4) delete_plan "DRP" "$DRP_OUTPUT_DIR" ;;
            5) generate_docx "DRP" "$DRP_OUTPUT_DIR" ;;
            6) show_help "DRP" ;;
            7) break ;;
            *) echo "Invalid option. Try again." ;;
            esac
        done
        ;;
    2)
        while true; do
            show_plan_menu "Incident Response Plan (IRP)"
            case $plan_choice in
            1) create_plan "$IRP_TEMPLATE_FILE" "$IRP_OUTPUT_DIR" "IRP" ;;
            2) list_plans "IRP" "$IRP_OUTPUT_DIR" ;;
            3) view_plan "IRP" "$IRP_OUTPUT_DIR" ;;
            4) delete_plan "IRP" "$IRP_OUTPUT_DIR" ;;
            5) generate_docx "IRP" "$IRP_OUTPUT_DIR" ;;
            6) show_help "IRP" ;;
            7) break ;;
            *) echo "Invalid option. Try again." ;;
            esac
        done
        ;;
    3)
        show_help "Main Menu"
        ;;
    4)
        echo "Exiting the program. Goodbye!"
        break
        ;;
    *)
        echo "Invalid option. Try again." ;;
    esac
done
