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
    echo "     Policy Generator Script           "
    echo "======================================="
    echo "1. Generate Disaster Recovery Plans (DRP)"
    echo "2. Generate Incident Response Plans (IRP)"
    echo "3. Exit"
    echo "======================================="
    read -p "Choose an option [1-3]: " main_choice
}

# Generate a plan from the template
generate_plan() {
    local template_file="$1"
    local output_dir="$2"
    local plan_type="$3"

    read -p "Enter a unique name for the new $plan_type (e.g., 'DRP_ProjectX'): " plan_name
    local plan_path="$output_dir/$plan_name.md"

    if [[ -f "$plan_path" ]]; then
        echo "A plan with this name already exists. Choose another name."
        return
    fi

    cp "$template_file" "$plan_path"
    echo "$plan_type has been generated at: $plan_path"

    customize_plan "$plan_path" "$plan_type"
}

# Customize the plan with placeholders
customize_plan() {
    local plan_path="$1"
    local plan_type="$2"

    echo "Customizing the $plan_type..."

    if [[ "$plan_type" == "DRP" ]]; then
        sed -i '' "s/\[System A\]/Enter critical system name here/g" "$plan_path"
        sed -i '' "s/\[e.g., 4 hours\]/Enter RTO example here/g" "$plan_path"
        sed -i '' "s/\[e.g., 15 minutes\]/Enter RPO example here/g" "$plan_path"
    elif [[ "$plan_type" == "IRP" ]]; then
        sed -i '' "s/\[e.g., Splunk, Carbon Black\]/Enter tools and resources here/g" "$plan_path"
        sed -i '' "s/\[Regulatory body or governing authority\]/Enter regulatory contact here/g" "$plan_path"
    fi

    echo "$plan_type customization completed."
}

# List all generated plans
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
                echo "======================================="
                echo "   Manage Disaster Recovery Plans      "
                echo "======================================="
                echo "1. Generate a New DRP"
                echo "2. List Existing DRPs"
                echo "3. Delete a DRP"
                echo "4. Return to Main Menu"
                echo "======================================="
                read -p "Choose an option [1-4]: " drp_choice

                case $drp_choice in
                    1) generate_plan "$DRP_TEMPLATE_FILE" "$DRP_OUTPUT_DIR" "DRP" ;;
                    2) list_plans "$DRP_OUTPUT_DIR" ;;
                    3) delete_plan "$DRP_OUTPUT_DIR" "DRP" ;;
                    4) break ;;
                    *) echo "Invalid option. Try again." ;;
                esac
            done
            ;;
        2)
            while true; do
                echo "======================================="
                echo "   Manage Incident Response Plans      "
                echo "======================================="
                echo "1. Generate a New IRP"
                echo "2. List Existing IRPs"
                echo "3. Delete an IRP"
                echo "4. Return to Main Menu"
                echo "======================================="
                read -p "Choose an option [1-4]: " irp_choice

                case $irp_choice in
                    1) generate_plan "$IRP_TEMPLATE_FILE" "$IRP_OUTPUT_DIR" "IRP" ;;
                    2) list_plans "$IRP_OUTPUT_DIR" ;;
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
