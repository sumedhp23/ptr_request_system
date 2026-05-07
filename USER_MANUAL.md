# Production Tooling Request (PTR) System - User Manual

## Table of Contents
1. [Introduction](#1-introduction)
2. [System Initialization & Setup](#2-system-initialization--setup)
3. [End-to-End Workflow: The 7 Statuses](#3-end-to-end-workflow-the-7-statuses)
    - [Status 1: Raising a New PTR](#status-1-raising-a-new-ptr)
    - [Status 2: Managerial Approval](#status-2-managerial-approval)
    - [Status 3: Designer Data Entry](#status-3-designer-data-entry)
    - [Status 4: Tool Room Initialization](#status-4-tool-room-initialization)
    - [Status 5 & 6: Procurement & Indent Tracking](#status-5--6-procurement--indent-tracking)
    - [Status 7: Tool Receipt & Verification (TVRN)](#status-7-tool-receipt--verification-tvrn)
4. [Tool Lifecycle & Maintenance](#4-tool-lifecycle--maintenance)
    - [Preventive Maintenance (PM)](#preventive-maintenance-pm)
    - [Breakdown Reporting](#breakdown-reporting)
    - [Tool Life Extension](#tool-life-extension)
5. [Reporting & Exports](#5-reporting--exports)
    - [Tool History PDF Generation](#tool-history-pdf-generation)
    - [Complete Bulk Excel Export](#complete-bulk-excel-export)

---

## 1. Introduction
Welcome to the Production Tooling Request (PTR) System. This application is designed to orchestrate the lifecycle of manufacturing tools from the moment an engineer requests a new tool, through physical fabrication and QA verification, all the way to long-term cyclical maintenance. The system utilizes strict procedural status gates to ensure no tool moves into the factory floor without proper documentation and manager approval.

---

## 2. System Initialization & Setup
To run the PTR system locally on your machine for development or production access:

1. **Activate the Virtual Environment:**
   Ensure you isolate the system dependencies from your local machine. Open your terminal in the project directory and run:
   ```bash
   source venv/bin/activate
   ```
2. **Start the Development Server:**
   ```bash
   python manage.py runserver 8500
   ```
3. **Access the Application:**
   Open your browser and navigate to: `http://127.0.0.1:8500`

---

## 3. End-to-End Workflow: The 7 Statuses

The core of the PTR system is its State Machine. A tool must pass through multiple distinct statuses sequentially.

### Status 1: Raising a New PTR
**Role:** PTR Requester
*   Navigate to **Requests > Add PTR Request** on the sidebar.
*   Fill in the necessary operational parameters, such as the Customer, Part Name, Process, Quantity, and the required deadline for the tooling.
*   Once submitted, the PTR enters **Status 1** (Draft) and is forwarded to the designated manager.

### Status 2: Managerial Approval
**Role:** Manager/Approver
*   Navigate to **Manager Approval**.
*   The manager reviews the operational justification for the tool.
*   **Actions Available:**
    *   **Approve:** Upgrades the tool to Status 3.
    *   **Send Back:** Returns to the requester for modifications.
    *   **Reject:** Terminates the PTR line.

### Status 3: Designer Data Entry
**Role:** Designer
*   Navigate to **Designing Activity**.
*   Once approved, designers assign technical identifiers like the **Tooling Information Number (TINo)**, Revision History, Bill of Materials, and expected ROI parameters.
*   Submission upgrades the PTR to the physical manufacturing stage.

### Status 4: Tool Room Initialization
**Role:** Tool Room Administrator
*   The tool now enters physical tracking. Basic supplier information and expected fabrication costs are estimated.

### Status 5 & 6: Procurement & Indent Tracking
**Role:** Purchasing/Stores
*   Purchase Requisitions (PR) are logged. 
*   The system tracks expected delivery dates alongside exact financial overheads, logging the Goods Receipt Note (GRN) when materials arrive.

### Status 7: Tool Receipt & Verification (TVRN)
**Role:** QA / Receiving
*   Navigate to **Receiving Activity**.
*   Before a tool is pushed to the operational floor, QA logs visual, dimensional, and functional reports.
*   A **TVRN** (Tool Verification Report Number) is generated. 
*   The PTR is now marked **Completed (Status 7)**.

---

## 4. Tool Lifecycle & Maintenance

Once a tool achieves Status 7, it is live. The system now focuses on extending its lifespan and preventing factory downtime.

### Preventive Maintenance (PM)
*   Navigate to **PM Plan** in the sidebar.
*   Users can log cyclical checkups based on the tool's designated PM frequency.
*   Records include the Actual Date of Inspection, PM Report Number, and an Approver's digital sign-off.

### Breakdown Reporting
*   Navigate to **Breakdown**.
*   If a tool snaps or fails on the line, an emergency ticket is logged detailing the exact failure point, the corrective action applied, and the total operational hours lost.

### Tool Life Extension
*   Navigate to **Tool Life**.
*   If a tool exceeds its designated operational lifespan (e.g., designed for 10,000 punches but currently at 10,500), an official Dimensional Reset report must be filed and approved to continue utilizing the asset.

---

## 5. Reporting & Exports

The PTR System features powerful automated documentation generators to satisfy auditing requirements.

### Tool History PDF Generation
If you need to view the entire lifecycle of a single tool:
1. Navigate to the **Requests List** or the Manager Dashboard.
2. Click the **History** button next to any PTR.
3. The system will asynchronously query the database across the Designer, QA, and Breakdown modules to assemble a single chronological view.
4. Click **Download PDF** at the top. The system will silently convert the complex DOM layout into a pristine A4-sized PDF without triggering messy browser print dialogues.

### Complete Bulk Excel Export
If management requests a high-level overview of the entire factory unit:
1. Navigate to **Reports** on the main sidebar.
2. Select your Target Operating Unit (e.g., `ASMIPL` or `ASYM`).
3. Click **Download Master Report**.
4. The system leverages `openpyxl` to generate a pixel-perfect, color-coded Excel spreadsheet mapping exactly 61 columns. It outputs the data for *every* PTR in that unit sequentially, smoothly handling both incomplete drafts and fully realized tools.
