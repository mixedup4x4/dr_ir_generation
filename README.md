# DR/IR Plan Generator

## 📌 Overview
This project automates the generation, management, and versioning of **Disaster Recovery Plans (DRP)** and **Incident Response Plans (IRP)** in compliance with **NIST, STIG, FEDRAMP, and FISMA** standards. The tool supports **multi-user authentication, version control, audit logging, and exporting to multiple formats**.

## 🚀 Features
- **Multi-user authentication** with roles: `admin`, `approver`, `editor`, `viewer`.
- **Plan versioning** with rollback support.
- **Audit logging** to track all actions.
- **Export plans to Markdown (`.md`), JSON (`.json`), and PDF (`.pdf`).**
- **Fully automated CLI tool** using `Typer`.
- **Cross-platform support** (macOS, Windows, Linux).
- **Comprehensive test suite** using `pytest`.

---

## 🛠 Installation

### **1. Clone the Repository**
```bash
git clone https://github.com/YOUR_USERNAME/dr_ir_generation.git
cd dr_ir_generation
```

### **2. Create a Virtual Environment (Recommended)**
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate   # Windows
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Initialize the Database**
```bash
python main.py init
```

---

## 🔑 User Roles
| Role      | Permissions |
|-----------|------------|
| Admin     | Manage users, plans, and logs |
| Approver  | Approve/reject plans |
| Editor    | Create, edit, and rollback plans |
| Viewer    | View plans only |

---

## 📌 Usage

### **👤 Add Users**
```bash
python main.py add-user admin SecurePass123 --role admin
python main.py add-user editor1 EditorPass123 --role editor
python main.py add-user viewer1 ViewerPass123 --role viewer
```

### **🔑 Login**
```bash
python main.py login admin SecurePass123
```

### **📄 Create a New Plan**
```bash
python main.py create-plan-cli editor1 EditorPass123 "Business Continuity Plan" drp "Initial test content"
```

### **📝 Save a New Plan Version**
```bash
python main.py save-plan-version-cli editor1 EditorPass123 1 "Updated content for DRP"
```

### **📜 List All Plan Versions**
```bash
python main.py list-plan-versions-cli 1
```

### **🔄 Rollback to an Earlier Version**
```bash
python main.py rollback-plan-cli editor1 EditorPass123 1 1
```

### **📑 View Logs (Admin Only)**
```bash
python main.py view-logs admin SecurePass123
```

### **📤 Export Plans**
- **Markdown:** `python main.py export-plan-markdown-cli 1`
- **JSON:** `python main.py export-plan-json-cli 1`
- **PDF:** `python main.py export-plan-pdf-cli 1`

---

## 🏗 Project Structure
```
.
├── LICENSE
├── README.md
├── main.py
├── requirements.txt
├── db/
│   ├── database_setup.py
│   ├── models.py
│   ├── query.py
├── outputs/
│   ├── drp/
│   ├── irp/
├── scripts/
│   ├── auth.py
├── templates/
│   ├── drp_master_template.md
│   └── irp_master_template.md
├── tests/
│   ├── test_users.py
│   ├── test_plans.py
│   ├── test_logs.py
```

---

## ✅ Running Tests (Pytest)

This project now uses `pytest` for testing. To run all test cases:
```bash
pytest tests/
```

Run specific test files:
```bash
pytest tests/test_users.py  # Run user-related tests
pytest tests/test_plans.py  # Run plan-related tests
pytest tests/test_logs.py   # Run log-related tests
```

---

## 📂 .gitignore (Ensure This is Included)
```
# Virtual Environment
venv/

# Database Files
*.db

# Compiled Python Files
__pycache__/
*.pyc

# Outputs & Logs
outputs/
logs/
```

---

## 🚀 Next Steps
- Optimize code for better efficiency and error handling.
- Expand test coverage and remove redundant test scripts.
- Potentially integrate a **web-based GUI**.
- Explore **AI-powered compliance recommendations**.
- Enhance documentation further after refactoring.

---

For any issues, open a GitHub issue. 🚀
