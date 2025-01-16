# Policy Generation Scripts

This repository contains two powerful Bash scripts for managing Disaster Recovery Plans (DRP) and Incident Response Plans (IRP). These scripts align with **NIST 800-53**, **FISMA**, and **FedRAMP** standards, ensuring compliance and usability across organizations of all sizes.

## Directory Structure

```
.
├── LICENSE
├── README.md
├── interactive_policy.sh
├── outputs
│   ├── drp
│   │   └── drp_test1.md
│   └── irp
├── policy_generator.sh
└── templates
    ├── drp_master_template.md
    └── irp_master_template.md

5 directories, 7 files
```

## Scripts Overview

### 1. `interactive_policy.sh`
An interactive script that guides users through creating and customizing DRP and IRP documents directly in the terminal.

#### Features
- **Interactive Data Entry**: Users are prompted to provide details for each section of the plan.
- **Plan Management**:
  - Create new plans.
  - View and edit existing plans.
  - Delete plans by name.
- **User-Friendly Prompts**: Includes examples and help for each input field.
- **Dynamic Output**: Saves progress to `outputs/drp` or `outputs/irp`.

#### Usage
1. Run the script: `./interactive_policy.sh`
2. Choose to work on DRP or IRP.
3. Follow prompts to create, view/edit, or delete plans.

---

### 2. `policy_generator.sh`
A batch script for generating DRP and IRP documents from master templates.

#### Features
- **Template-Based Generation**: Uses `templates/drp_master_template.md` and `templates/irp_master_template.md` as baselines.
- **Batch Customization**: Automatically replaces placeholders in the templates with user-provided data.
- **Plan Management**:
  - Generate new plans.
  - List existing plans.
  - Delete plans by name.

#### Usage
1. Run the script: `./policy_generator.sh`
2. Choose to generate or manage DRPs or IRPs.
3. Follow the menu to create or delete plans.

---

## Templates
### DRP Template (`templates/drp_master_template.md`)
- Comprehensive structure for disaster recovery planning.
- Includes sections for:
  - Purpose
  - Objectives
  - Scope
  - Risk Assessment
  - Recovery Strategies
  - Testing and Maintenance
  - Appendices

### IRP Template (`templates/irp_master_template.md`)
- Detailed framework for incident response management.
- Covers:
  - Incident Categories
  - Incident Response Phases
  - Communication Plan
  - Testing and Maintenance
  - Appendices

---

## Outputs
Generated plans are stored in the `outputs` directory:

- **DRPs**: Saved in `outputs/drp`
- **IRPs**: Saved in `outputs/irp`

---

## Prerequisites
- **Bash Shell**: Ensure you are using a system with Bash installed.
- **Pandoc**: Required for converting Markdown to `.docx` (if extended functionality is added).

Install Pandoc (if needed):
```bash
brew install pandoc  # For macOS
sudo apt install pandoc  # For Ubuntu/Debian
```

---

## How to Contribute
1. Fork the repository.
2. Create a new branch: `git checkout -b feature-branch`
3. Commit changes: `git commit -m 'Add new feature'`
4. Push to the branch: `git push origin feature-branch`
5. Open a pull request.

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Feedback and Support
If you have any issues or suggestions, please open an issue in the repository or contact us directly.
