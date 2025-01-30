#!/bin/bash

echo "🚀 Running Automated DRP/IRP Test Script..."
ERRORS=0

# Step 1: Reset Database
echo "🔄 Resetting database..."
python main.py init || { echo "❌ Database reset failed. Exiting."; ERRORS=1; exit 1; }

# Step 2: Create Users
echo "👤 Creating users..."
python main.py add-user admin SecurePass123 --role admin || { echo "❌ User 'admin' creation failed."; ERRORS=1; }
python main.py add-user editor EditorPass123 --role editor || { echo "❌ User 'editor' creation failed."; ERRORS=1; }
python main.py add-user viewer ViewerPass123 --role viewer || { echo "❌ User 'viewer' creation failed."; ERRORS=1; }

# Step 3: Login and Check Password Hashing
echo "🔑 Checking password hashing for admin..."
python main.py login admin SecurePass123 || { echo "❌ Login failed for admin."; ERRORS=1; }
python main.py login editor EditorPass123 || { echo "❌ Login failed for editor."; ERRORS=1; }
python main.py login viewer ViewerPass123 || { echo "❌ Login failed for viewer."; ERRORS=1; }

# Step 4: Create a new DRP plan (test plan creation)
echo "📄 Creating a new DRP plan..."
python main.py create-plan-cli editor EditorPass123 "Test DRP Plan" --plan-type drp --framework nist || { echo "❌ Plan creation failed."; ERRORS=1; }

# Step 5: Save a new version of the plan
echo "📝 Saving a new version..."
python main.py create-plan-cli editor EditorPass123 "Test DRP Plan Updated" --plan-type drp --framework nist || { echo "❌ Saving version failed."; ERRORS=1; }

# Step 6: Rollback to previous version
echo "🔄 Rolling back to previous version..."
python main.py rollback-plan editor EditorPass123 "Test DRP Plan" || { echo "❌ Rollback failed."; ERRORS=1; }

# Step 7: List all versions of the plan
echo "📜 Listing all versions..."
python main.py list-plan-versions 1 || { echo "❌ Listing versions failed."; ERRORS=1; }

# Step 8: Logging actions performed on the plan
echo "📑 Viewing logs..."
python main.py view-logs admin SecurePass123 || { echo "❌ Viewing logs failed."; ERRORS=1; }

# Step 9: Test file handling
echo "📝 Testing file handling (safe write and backup)..."
python -c "from scripts.utils import safe_write, backup_file; safe_write('test_file.txt', 'Hello World'); backup_file('test_file.txt')" || { echo "❌ File handling failed."; ERRORS=1; }

# Step 10: Test email sending (simulated)
echo "📧 Testing email functionality..."
python -c "from scripts.utils import send_email; send_email('recipient@example.com', 'Test Subject', 'This is a test email body.')" || { echo "❌ Email functionality failed."; ERRORS=1; }

# If there were any errors, report and exit
if [ $ERRORS -ne 0 ]; then
  echo "❌ Test Script Failed. Some tests did not pass."
  exit 1
else
  echo "✅ Test Script Completed Successfully!"
fi
