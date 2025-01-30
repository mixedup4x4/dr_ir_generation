# DR/IR Plan Generator

## 📌 Overview
This project automates the generation, management, and versioning of **Disaster Recovery Plans (DRP)** and **Incident Response Plans (IRP)** in compliance with **NIST, STIG, FEDRAMP, and FISMA** standards. The tool supports multi-user access, version control, and exports plans to **Markdown, JSON, and PDF** formats.

## 🚀 Features
- **Multi-user authentication** with roles: `admin`, `approver`, `editor`, `viewer`.
- **Create, edit, and delete DRP/IRP plans** with version control.
- **Rollback to previous versions** of a plan.
- **Export plans to Markdown (`.md`), JSON (`.json`), and PDF (`.pdf`).**
- **Full audit logging** to track actions.
- **Fully automated CLI tool** built with `Typer`.
- **Cross-platform support** (macOS, Windows, Linux).

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

## 🔑 User Roles
| Role      | Permissions |
|-----------|------------|
| Admin     | Can create, edit, delete plans, view logs, manage users |
| Approver  | Can approve/reject plans |
| Editor    | Can create, edit, and rollback plans |
| Viewer    | Can only view plans |

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

## 🏗 Project Structure
```
.
├── LICENSE
├── README.md
├── main.py
├── requirements.txt
├── test_script.sh
├── db/
│   ├── database_setup.py
│   ├── models.py
│   ├── query.py
├── outputs/
│   ├── drp/
│   ├── irp/
├── scripts/
│   ├── auth.py
└── templates/
    ├── drp_master_template.md
    └── irp_master_template.md
```

## 📌 Requirements (`requirements.txt`)
```
typer
sqlalchemy
weasyprint
markdown
```
*Ensure all dependencies are installed with:*
```bash
pip install -r requirements.txt
```

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

## 🚀 Running the Test Script
To ensure everything is working correctly, run:
```bash
./test_script.sh
```

---

## ✅ Next Steps
- Expand the tool with a **web-based GUI**.
- Add **AI-powered compliance recommendations**.
- Integrate with **external security frameworks**.
- Update README

For any issues, open a GitHub issue. 🚀

