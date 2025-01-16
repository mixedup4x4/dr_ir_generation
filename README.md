# DR/IR Generation

This repository, **dr_ir_generation**, contains a versatile **policy_generator.sh** script designed to streamline the creation, customization, and maintenance of two critical organizational documents:

- **Disaster Recovery Plan (DRP)**
- **Incident Response Plan (IRP)**

The script provides a user-friendly, menu-driven interface for building plans aligned with **NIST 800-53**, **FISMA**, and **FedRAMP** standards. It is tailored for organizations of any size, ensuring compliance and industry best practices.

## Features
- **Template-Based Generation**: Uses predefined templates stored in the `templates` folder.
- **Menu-Driven Input**: Guides users through entering required information for DRP and IRP.
- **Progress Saving**: Saves user inputs for later continuation.
- **Final Output in .docx Format**: Generates professional `.docx` documents using `pandoc`.
- **Company Logo Integration**: Allows embedding a logo into the plans.
- **Organized Output Structure**: Saves files to specific `drp` and `irp` folders for better organization.

## Prerequisites
Ensure the following tools are installed on your system:
1. **Bash** (Default shell for most UNIX-based systems)
2. **pandoc**:
   ```bash
   brew install pandoc  # macOS
   sudo apt-get install pandoc  # Ubuntu/Debian
   ```
3. **Templates**:
   - `templates/drp_master_template.md`
   - `templates/irp_master_template.md`

   These templates are included in this repository.

## Folder Structure
```
.
├── templates
│   ├── drp_master_template.md
│   ├── irp_master_template.md
├── drp
│   ├── drp_progress.txt
│   ├── disaster_recovery_program.docx
├── irp
│   ├── irp_progress.txt
│   ├── incident_response_plan.docx
└── policy_generator.sh
```

## Usage
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/dr_ir_generation.git
   cd dr_ir_generation
   ```

2. **Make the Script Executable**:
   ```bash
   chmod +x policy_generator.sh
   ```

3. **Run the Script**:
   ```bash
   ./policy_generator.sh
   ```

4. **Follow the Menu**:
   - Select **Disaster Recovery Plan (DRP)** or **Incident Response Plan (IRP)**.
   - Enter details, review saved progress, generate drafts, or add a company logo.

5. **Generated Outputs**:
   - DRP-related files are saved in the `drp` folder.
   - IRP-related files are saved in the `irp` folder.

## Customization
- Modify the templates in the `templates` folder to suit your organization’s specific needs.
- Add additional sections or refine existing ones to reflect specific compliance requirements or organizational policies.

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Open a pull request.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

Feel free to reach out with questions, issues, or suggestions to improve this project!
