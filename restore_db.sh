#!/bin/bash
echo "Wait for SQL Server to be ready..."
sleep 20

echo "Restoring database from ptr_request_db.bak..."
docker exec -it ptr_sqlserver /opt/mssql-tools18/bin/sqlcmd \
  -S localhost -U sa -P 'PtrSecurePassword123!' -C \
  -Q "RESTORE DATABASE ptr_request_db FROM DISK = '/var/opt/mssql/backup/ptr_request_db.bak' WITH REPLACE, RECOVERY;"

echo "Database restored successfully."
echo "You can now access the system at http://localhost:8500"
