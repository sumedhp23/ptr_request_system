# PTR/TCMR Request System

A modern, professional Django application for managing Process Tool Requests (PTR) and TCMR requests, backed by MS SQL Server.

## Prerequisites
- Python 3.12+
- Docker & Docker Compose
- ODBC Driver 18 for SQL Server (`msodbcsql18` / `mssql-tools18`)

## Setup Instructions

1. **Start the MS SQL Server Database (Docker)**
   ```bash
   docker compose up -d
   ```
   *Note: This starts MS SQL Server 2022 on port 1434.*

2. **Install Python Dependencies**
   ```bash
   pip install django mssql-django
   ```

3. **Run Database Migrations**
   ```bash
   python manage.py migrate
   ```

4. **Start the Development Server**
   ```bash
   python manage.py runserver 8500
   ```

5. **Access the Application**
   Open http://127.0.0.1:8500 in your browser.
