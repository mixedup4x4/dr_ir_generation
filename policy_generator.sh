#!/bin/bash

# Directories for templates and outputs
TEMPLATE_DIR="templates"
DRP_OUTPUT_DIR="drp"
IRP_OUTPUT_DIR="irp"

# Files for templates
DRP_TEMPLATE_FILE="$TEMPLATE_DIR/drp_master_template.md"
IRP_TEMPLATE_FILE="$TEMPLATE_DIR/irp_master_template.md"

# Files for progress and final outputs
DRP_SAVE_FILE="$DRP_OUTPUT_DIR/drp_progress.txt"
IRP_SAVE_FILE="$IRP_OUTPUT_DIR/irp_progress.txt"
DRP_DOCX_FILE="$DRP_OUTPUT_DIR/disaster_recovery_program.docx"
IRP_DOCX_FILE="$IRP_OUTPUT_DIR/incident_response_plan.docx"

# Function to display the main menu
show_menu() {
    clear
    echo "==============================="
    echo "   Management Program Script   "
    echo "==============================="
    echo "1. Work on Disaster Recovery Plan (DRP)"
    echo "2. Work on Incident Response Plan (IRP)"
    echo "3. Exit"
    echo "==============================="
    read -p "Choose an option [1-3]: " main_choice
}

# Function to display the sub-menu for a selected plan
show_plan_menu() {
    local plan_type="$1"
    clear
    echo "==============================="
    echo "   $plan_type Management Menu   "
    echo "==============================="
    echo "1. Fill in $plan_type Details"
    echo "2. Review Saved Progress"
    echo "3. Generate Final Draft (.docx)"
    echo "4. Add Company Logo"
    echo "5. Return to Main Menu"
    echo "==============================="
    read -p "Choose an option [1-5]: " plan_choice
}

# Function to initialize directories and templates
initialize_directories() {
    mkdir -p "$TEMPLATE_DIR" "$DRP_OUTPUT_DIR" "$IRP_OUTPUT_DIR"
}

# Function to initialize a plan with its master template
initialize_plan() {
    local template_file="$1"
    local save_file="$2"

    if [[ ! -f "$save_file" ]]; then
        echo "Initializing from master template..."
        cp "$template_file" "$save_file"
        echo "Template loaded into $save_file."
    else
        echo "A saved plan already exists. Continuing with existing progress."
    fi
}

# Function to fill in details for a plan
fill_details() {
    local template_file="$1"
    local save_file="$2"

    initialize_plan "$template_file" "$save_file"

    echo "Filling in details..."
    echo "Leave blank to skip a field or press Ctrl+C to return to the menu."

    read -p "Enter Purpose: " purpose
    if [[ -n "$purpose" ]]; then
        sed -i '' "/## Purpose/a\\
$purpose" "$save_file"
    fi

    read -p "Enter Objectives (comma-separated): " objectives
    if [[ -n "$objectives" ]]; then
        sed -i '' "/## Objectives/a\\
$objectives" "$save_file"
    fi

    read -p "Enter Scope: " scope
    if [[ -n "$scope" ]]; then
        sed -i '' "/## Scope/a\\
$scope" "$save_file"
    fi

    echo "Enter Key Contacts (type 'done' to finish):"
    while :; do
        read -p "Contact Name: " contact_name
        [[ "$contact_name" == "done" ]] && break
        read -p "Title/Role: " role
        read -p "Contact Information: " contact_info
        echo "- Name: $contact_name, Role: $role, Info: $contact_info" >> "$save_file"
    done

    echo "Details saved."
    sleep 2
}

# Function to review saved progress for a plan
review_progress() {
    local save_file="$1"

    if [[ -f "$save_file" ]]; then
        echo "==============================="
        echo "       Saved Progress          "
        echo "==============================="
        cat "$save_file"
    else
        echo "No progress saved yet."
    fi
    echo
    read -p "Press Enter to return to the menu..."
}

# Function to generate the final draft in .docx format
generate_docx() {
    local save_file="$1"
    local docx_file="$2"

    if [[ -f "$save_file" ]]; then
        echo "Generating final draft in .docx format..."
        {
            echo "# Final Plan"
            echo
            cat "$save_file"
        } > "temp.md"

        pandoc temp.md -o "$docx_file" --standalone
        rm temp.md

        echo "Draft saved as $docx_file."
    else
        echo "No data available to generate the draft."
    fi
    sleep 2
}

# Function to add a company logo
add_logo() {
    local save_file="$1"

    read -p "Enter the path to the company logo file: " logo_path
    if [[ -f "$logo_path" ]]; then
        echo "![Company Logo]($logo_path)" >> "$save_file"
        echo "Logo added to saved progress."
    else
        echo "Invalid file path. Logo not added."
    fi
    sleep 2
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
            1) fill_details "$DRP_TEMPLATE_FILE" "$DRP_SAVE_FILE" ;;
            2) review_progress "$DRP_SAVE_FILE" ;;
            3) generate_docx "$DRP_SAVE_FILE" "$DRP_DOCX_FILE" ;;
            4) add_logo "$DRP_SAVE_FILE" ;;
            5) break ;;
            *) echo "Invalid option. Try again." ;;
            esac
        done
        ;;
    2)
        while true; do
            show_plan_menu "Incident Response Plan (IRP)"
            case $plan_choice in
            1) fill_details "$IRP_TEMPLATE_FILE" "$IRP_SAVE_FILE" ;;
            2) review_progress "$IRP_SAVE_FILE" ;;
            3) generate_docx "$IRP_SAVE_FILE" "$IRP_DOCX_FILE" ;;
            4) add_logo "$IRP_SAVE_FILE" ;;
            5) break ;;
            *) echo "Invalid option. Try again." ;;
            esac
        done
        ;;
    3)
        echo "Exiting the program. Goodbye!"
        break
        ;;
    *)
        echo "Invalid option. Try again."
        sleep 2
        ;;
    esac
done

