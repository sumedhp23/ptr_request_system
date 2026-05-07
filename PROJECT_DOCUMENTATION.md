# Production Tooling Request (PTR) System - Advanced Technical Architecture & Project Documentation

## 1. Project Objective
The PTR (Production Tooling Request) System is a robust enterprise-grade Django web application designed to digitize and manage the entire lifecycle of manufacturing production tools. It enforces strict procedural workflows, transitioning a tool from an initial concept request (PTR) through managerial approval, tool-room fabrication, purchase/indent generation, final QA receiving, and long-term maintenance tracking (Breakdowns, Preventive Maintenance, and Life Extension).

## 2. Technology Stack & Frameworks
*   **Backend Subsystem:** Python 3 with the **Django** Web Framework. Provides the core ORM mapping, routing logic, and state-machine business enforcement.
*   **Database:** Standardized SQL Database Configuration mapping legacy structure (`db_table` constraints like `tbl_Department`, `tbl_EmployeeMapping`) for backwards compatibility with corporate architectures.
*   **Frontend Logic:** Server-side rendered HTML5 and native JavaScript.
*   **Styling Architecture:** Pure CSS3 natively written, prioritizing standard grid-based layouts (the `.approval-table` component hierarchy) eliminating the need for heavy frameworks.
*   **PDF Generation Engine:** Powered completely client-side using `html2pdf.js`, avoiding heavy backend conversion binaries (like wkhtmlpdf).
*   **Distributed Infrastructure:** Shipped as an isolated, containerized environment orchestrated by Docker (`docker-compose.yml`) ensuring perfect dependency tracking across teams without manual environment initialization.

---

## 3. Core Database Models & Infrastructure
The application strictly normalizes data using relational database schemas configured directly within `ptr_app/models.py`.

### A. Lookup & Master Mapping Models
These foundational tables handle system hierarchies and identity logic:
*   `Department` & `Customer` & `Project` & `PartMaster`: Maps tooling targets precisely to client and inventory dimensions.
*   `MachineModel` & `TypeOfMachine`: Used during tool planning stages to constraint fabrication limits.
*   `EmployeeMapping`: Ties a physical associate's credential to a structural Role (e.g., `Designer`, `Approver`, `ToolRoom`).
*   `FormMaster` & `FormMapping`: A dedicated permission mapping layer dynamically enforcing which employee roles can view which forms.

### B. Core Operational Models
The pipeline runs on explicit Django entities:
*   **`PTRRequest`**: The nexus table. Contains over 30 fields documenting the tool's initiation (`ptrno`, `process`, `drawing`), mapping logic (`mappprovedate`, `earlydatereason`) and its core state machine position (`status`).
*   **`DesignerEntry`**: Triggers at Phase 3. Defines Tooling Information Number (TINo), specification sheets, and manufacturer (Supplier/Make) metadata.
*   **`ToolRoom` & `StoreEntry`**: Triggers at Phase 4-6. Bridges Purchase Requisitions (PR) and fabrication cost approximations.
*   **`ReceivingEntry`**: Triggers at Phase 7. The final QA block handling TVRN verification reports before the tool goes operational.

### C. Advanced Lifecycle History Models
Secondary systems manage the ongoing life of an active target:
*   **`PreventM`**: Schedules and stores cyclical inspections (Remarks, Approver logic).
*   **`Breakdown`**: Captures emergency downtime constraints tracking `Reason for Mod`, `Corrective Action (ReportNo & Status)`, and cumulative down-time hours natively.
*   **`ToolLifeExtend`**: A revision tracker mapping when a tool exceeds its initial operational lifetime, requiring formally approved dimensional resets.

---

## 4. The Request State Machine Pipeline
Every tool sequentially traverses the following hardcoded logic gates (`status` variable inside `PTRRequest`) mapped across individual HTML templates:

1.  **Status 1 (Drafting):** 
    Users log the core requirement generating an initial unique identifying number cross-referenced against projects and parts.
2.  **Status 2 (Manager Approval Stage):** 
    Routed to higher-level authorities through `manager_edit_request.html`. Managers execute tri-state decisions: Approve to proceed, Reject terminating the line, or Send Back for correction. 
3.  **Status 3 (Design Room Structuring):** 
    Designers fill down detailed metadata (Bill of Materials, inspection checks, and core structural parameters like dimensions and punch clearance).
4.  **Status 4 (Tool Room Entry):** 
    The item enters physical construction or request preparation.
5.  **Status 5 & 6 (Stores/Purchase Tracking):** 
    Indent generation. Standardizes the generation of PR references tracking associated financial outlays and exact Good Receipt Dates (GRN).
6.  **Status 7 (Verification & Quality Check):** 
    The final hurdle before live plant insertion. The `ReceivingEntry` model captures visual/dimensional checks generating the critical Verification Report number (TVRN).

---

## 5. Major Engineering Upgrades & Modernization

During the current engineering lifecycle, the team drastically refactored cross-module UI systems and compiled the historically scattered data into unified reporting engines:

### 1. Standardization of the `.approval-table` CSS Architecture
*   **Target:** Dozens of forms were previously rendering inconsistently.
*   **Solution:** Built a global CSS framework `approval-table` enforced globally. This normalized padding, standard text weights, dynamic cell hovering, and exact border alignments across `manager_edit_request`, `pm_plan`, and `designer_entry_list` forms, providing a highly premium and coherent user experience.

### 2. Universal Tool History Card (Print-Optimized PDF Generator)
*   **The Business Problem:** Determining the maintenance and lifecycle metadata of a single tool meant jumping across 5 different database views dynamically.
*   **The Development:** 
    A unified comprehensive endpoint `history_card_view` was assembled. This controller asynchronously queries the `PTRRequest` metadata alongside `DesignerEntry`, `ReceivingEntry`, `PreventM`, `Breakdown`, and `ToolLifeExtend` records to assemble a monolithic timeline array.
*   **The Render Implementation (`history_card_pdf.html`):** 
    A flawless Print-Optimized grid was built mapping natively to the strict A4 dimensions required by internal QA archiving standards. It implements rigid bounding boxes preventing overlapping layouts.
    
### 3. Integrated Client-Side Direct Download Engine (`html2pdf.js`)
*   **The Challenge:** Traditional browser-native `window.print()` dialogues require users to manually shift output settings or execute "Save as PDF", causing enormous workflow friction.
*   **Advanced Fixes Implemented:**
    1.  Overwrote native print triggers with seamless JavaScript promise layers. Output processes smoothly via `html2canvas` generating a direct 1-click silent physical download event named iteratively (`ASMIPL-XXX_Tool_History.pdf`).
    2.  Engineered a custom Loader UI overlay mapping. It instantly abstracts the messy DOM resizing behind a professional "Generating PDF Document..." spinner resolving upon completion.
    3.  Implemented dynamic window cleanup routines: the target generation-tab automatically tears itself down post-render, eliminating browser bloat.

### 4. Direct Graphic Integration
*   Integrated high-resolution corporate vector assets natively placed across all PDF exports perfectly mapped inside constraint headers.

### 5. Advanced Complete Excel Reporting Engine
*   **The Business Problem:** Need to extract 61 columns of data spanning multiple tables (Admin, Designer, CM, Tool Room, PM) into a single, standardized corporate Excel template.
*   **The Development:** Engineered a bulk export engine (`export_report_excel` in `views.py`) leveraging the `openpyxl` library.
*   **Features:**
    *   **Unit-Based Bulk Processing:** Generates a unified report sorting every PTR (regardless of draft or completed status) for a specific operational unit (ASMIPL / ASYM).
    *   **Dynamic Template Generation:** Hardcodes A4-style merged grid headers, exact RGB corporate color coding, and dynamic title adjustment directly in Python, entirely bypassing template files.
    *   **Graceful Degradation:** Safely parses missing downstream data utilizing robust `try/except` mapping, ensuring clean blank cells instead of system exceptions for uncompleted PTRs.

## 6. Dependency & Deployment Notes
### Virtual Environment & Local Setup
To prevent OS-level system conflicts, this project isolates dependencies using a native python virtual environment. 
A stripped-down `requirements.txt` maps explicitly the backend load requirements (`Django 6.0`, `mssql-django`, `openpyxl`, `pyodbc`).
To spin up locally:
1. `source venv/bin/activate`
2. `pip install -r requirements.txt`
3. `python manage.py runserver 8500`

### Distributed Infrastructure
This project embraces isolated development boundaries minimizing OS conflicts natively via Docker protocols.
The core database mirrors correctly bounded container ports mapped externally avoiding persistent state-sharing errors. To pass the workflow natively, one effectively only uses `docker-compose up` completely bypassing manual Python VM dependencies. Let standard GitHub repositories execute change tracking explicitly.
