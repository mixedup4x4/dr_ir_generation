#!/bin/bash

# Reset the database
echo "🔄 Resetting database..."
rm dr_ir_generation.db
python main.py init

# Add users
echo "👤 Creating users..."
python main.py add-user admin adminPass123 --role admin
python main.py add-user editor1 EditorPass123 --role editor
python main.py add-user viewer1 ViewerPass123 --role viewer

# Try creating DRP plan
echo "📄 Creating a new DRP plan..."
python main.py create-plan-cli editor1 EditorPass123 "Test DRP Plan" --plan-type drp --framework nist

# Try saving a new version
echo "📝 Saving a new version..."
python main.py create-plan-cli editor1 EditorPass123 "Test DRP Plan" --plan-type drp --framework nist

# List all versions
echo "📜 Listing all versions..."
python main.py list-plans-cli

# Try rolling back to the previous version
echo "🔄 Rolling back to previous version..."
python main.py rollback-plan-cli editor1 EditorPass123 1

# Export plan to Markdown, JSON, PDF
echo "📝 Exporting to Markdown..."
python main.py export-plan-markdown-cli 1

echo "🔍 Exporting to JSON..."
python main.py export-plan-json-cli 1

echo "📄 Exporting to PDF..."
python main.py export-plan-pdf-cli 1

# List all logs
echo "📑 Listing all logs..."
python main.py view-logs editor1 EditorPass123

# Test user deletion
echo "🗑️ Deleting users..."
python main.py delete-user-cli editor1
python main.py delete-user-cli viewer1

echo "✅ Test Script Completed Successfully!"
