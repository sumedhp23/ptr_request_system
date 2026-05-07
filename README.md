# PTR Request System

The **Process Tool Request (PTR) System** is a comprehensive, enterprise-grade Django web application designed to manage, track, and analyze tooling requests, preventive maintenance, and designer workflows across multiple manufacturing units (ASMIPL and ASYM).

## 🚀 Features

*   **Real-Time Executive Dashboard**: High-level overview of designer workloads, active PTR distributions, and a dynamic 36-month preventive maintenance forecast.
*   **Complete Request Lifecycle**: Full tracking from request initiation, manager approval, receiving entry, to short-closing.
*   **Preventive Maintenance (PM)**: Automated scheduling and tracking for PM Plans, Breakdown Maintenance, and Tool Life Extensions.
*   **Granular Role-Based Access Control (RBAC)**: Secure access mapped dynamically through `EmployeeMapping` and `FormMapping` to restrict users to authorized pages.
*   **Excel Reporting**: Automated, stylized `.xlsx` report generations via `openpyxl` for board meetings and workload distributions.
*   **History Card Engine**: End-to-end PDF report generation for the entire lifecycle of a tool/fixture using `reportlab`.
*   **Modern UI/UX**: Premium, responsive interface built with HTML5, Vanilla CSS, and Material Icons.

## 🛠 Tech Stack

*   **Backend Framework**: Django 6.0 (Python 3.11)
*   **Database**: Microsoft SQL Server 2022 (`mcr.microsoft.com/mssql/server:2022-latest`)
*   **Database Adapter**: `mssql-django` & `pyodbc` (ODBC Driver 18)
*   **Deployment Architecture**: Fully containerized using Docker and Docker Compose.

---

## 📦 Database Information

**Does the GitHub repository include the database and its structures?**
**Yes.** The repository includes a `ptr_request_db.bak` file. This is a full SQL Server backup file. It contains the **entire database schema** (all tables, columns, foreign keys, relationships) as well as the **live data** populated within it. When you run the restore script (details below), it perfectly recreates the database exactly as it was on the original machine.

---

## ⚙️ Installation & Setup Guide

This project is fully Dockerized, meaning you don't need to install Python, SQL Server, or any drivers on your local host machine. Everything runs securely inside isolated containers.

### Prerequisites (For both Mac and Windows)
1. Install [Git](https://git-scm.com/downloads).
2. Install [Docker Desktop](https://www.docker.com/products/docker-desktop/).
   * *Windows Users:* Ensure WSL 2 (Windows Subsystem for Linux) backend is enabled in Docker Desktop settings.

### Step 1: Clone the Repository
Open your terminal (Mac) or Git Bash / PowerShell (Windows) and run:
```bash
git clone https://github.com/sumedhp23/ptr_request_system.git
cd ptr_request_system
```

### Step 2: Build and Start the Containers
Run Docker Compose to build the Django application and start the SQL Server database.
```bash
docker-compose up -d --build
```
*Wait about 30-45 seconds for SQL Server to fully boot up in the background.*

### Step 3: Restore the Database
Because the database is stored as a `.bak` file, you need to restore it into the running SQL Server container. This is a **one-time setup**.

**For Mac / Linux users:**
Simply run the included shell script:
```bash
chmod +x restore_db.sh
./restore_db.sh
```

**For Windows users:**
If you are using Git Bash or WSL, you can run the script above. If you are using standard Command Prompt or PowerShell, execute the following Docker command directly:
```powershell
docker exec -it ptr_sqlserver /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "PtrSecurePassword123!" -C -Q "RESTORE DATABASE ptr_request_db FROM DISK = '/var/opt/mssql/backup/ptr_request_db.bak' WITH REPLACE, RECOVERY;"
```

### Step 4: Access the Application
The application is now live! Open your web browser and navigate to:
**http://localhost:8500**

---

## 🛑 Stopping and Managing the Application

To stop the servers without deleting your data:
```bash
docker-compose stop
```

To start them back up later:
```bash
docker-compose start
```

If you want to completely tear down the containers and the database volume (Warning: this will delete new data entered):
```bash
docker-compose down -v
```

## 🐛 Troubleshooting

*   **Database Connection Refused / Login Failed**: Ensure that Docker Desktop is actively running. If you just ran `docker-compose up -d`, SQL Server might still be starting. Wait 30 seconds and try again.
*   **Missing ODBC Drivers**: You do not need to install ODBC drivers on your host machine. The provided `Dockerfile` automatically installs Microsoft ODBC Driver 18 securely inside the Django Linux container.
*   **Port 8500 or 1434 is already in use**: Ensure no other application is running on these ports. You can change the port mappings in `docker-compose.yml` if necessary.
