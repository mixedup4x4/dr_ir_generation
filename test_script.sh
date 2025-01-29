#!/bin/bash

echo "🚀 Running Automated DRP/IRP Test Script..."

# Step 1: Reset the database
echo "🔄 Resetting database..."
rm -f dr_ir_generation.db
python main.py init

# Step 2: Create users
echo "👤 Creating users..."
python main.py add-user admin SecurePass123 --role admin
python main.py add-user editor1 EditorPass123 --role editor

# Step 3: Create a new DRP plan
echo "📄 Creating a new DRP plan..."
python main.py create-plan-cli editor1 EditorPass123 "Test DRP" drp "Initial test content"

# Step 4: Save a new version
echo "📝 Saving a new version..."
python main.py save-plan-version-cli editor1 EditorPass123 1 "Updated content for DRP"

# Step 5: List all versions
echo "📜 Listing all versions..."
python main.py list-plan-versions-cli 1

# Step 6: Rollback to Version 1
echo "🔄 Rolling back to version 1..."
python main.py rollback-plan-cli editor1 EditorPass123 1 1

# Step 7: Export to Markdown
echo "📝 Exporting to Markdown..."
python main.py export-plan-markdown-cli 1

# Step 8: Export to JSON
echo "🔍 Exporting to JSON..."
python main.py export-plan-json-cli 1

# Step 9: Export to PDF
echo "📄 Exporting to PDF..."
python main.py export-plan-pdf-cli 1

# Step 10: View logs
echo "📑 Viewing logs..."
python main.py view-logs admin SecurePass123

echo "✅ Test Script Completed Successfully!"

ls -l outputs/
