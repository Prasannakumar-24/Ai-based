# ⚡ QUICK FIX - MySQL Connection Error

## Problem
```
❌ MySQL connection failed: 2003: Can't connect to MySQL server on 'localhost:3306'
```

## Solution

### **Option 1: Start MySQL Server (If Installed)**

#### Windows - PowerShell:
```powershell
# Check if MySQL service exists
Get-Service MySQL80

# Start the service
Start-Service MySQL80

# Verify it's running
Get-Service MySQL80 | Select-Object Status
```

**If MySQL80 not found, try these:**
```powershell
# List all services containing 'mysql'
Get-Service | Where-Object {$_.Name -like "*mysql*"}

# Then start the correct one
Start-Service MySQL57    # or whatever name appears
```

**If you need to find MySQL installation:**
```powershell
# Search for MySQL installation
Get-ChildItem -Path "C:\Program Files" -Filter "MySQL*" -Recurse -Directory
```

---

### **Option 2: Use SQLite Instead (⭐ RECOMMENDED - No Server Setup)**

SQLite is built-in to Python and requires NO server installation.

#### **Step 1: Replace database module**
```powershell
cd c:\Users\ADMIN\Downloads\python\face_attendance_system

# Backup original
Copy-Item database.py database_mysql.py

# Use SQLite version instead
Copy-Item database_sqlite.py database.py
```

#### **Step 2: Run the application**
```powershell
python main.py
```

✅ **That's it! No MySQL needed!**

---

## Why Use SQLite?

| Feature | MySQL | SQLite |
|---------|-------|--------|
| **Setup** | Complex (server + config) | ✅ Instant (file-based) |
| **Installation** | Requires MySQL server | ✅ Built-in Python |
| **Performance** | Better for large systems | ✅ Good for < 1 million records |
| **Database File** | Server-based | ✅ attendance.db (local file) |
| **Cost** | Free | ✅ Free |
| **Admin Tools** | MySQL Workbench | ✅ DB Browser or GUI tools |

---

## Verification Steps

### If using SQLite:
```powershell
cd c:\Users\ADMIN\Downloads\python\face_attendance_system
python setup.py

# Should now show:
# ✅ Database connection successful
# ✅ Attendance table created
```

### If using MySQL (after starting service):
```powershell
# First, update credentials in database.py
# Set: user = 'root', password = '' (or your password)

python setup.py
```

---

## Troubleshooting

### 1. MySQL Service Not Found
**Solution**: Install MySQL or use SQLite instead
```powershell
# Download from: https://dev.mysql.com/downloads/mysql/
# Or use SQLite (no install needed)
```

### 2. Connection Refused (10061)
**Solution**: MySQL not running
```powershell
# Start it
Start-Service MySQL80

# Or use SQLite
Copy-Item database_sqlite.py database.py
python main.py
```

### 3. Access Denied / Wrong Password
**Solution**: Update credentials in database.py
```python
self.user = 'root'
self.password = ''  # Your MySQL password
```

---

## Running the Application

### With SQLite (Easiest):
```powershell
# One-time setup
Copy-Item database_sqlite.py database.py

# Run application
python main.py
```

### With MySQL (If working):
```powershell
# Ensure MySQL is running
Start-Service MySQL80

# Update credentials in database.py
# Then run
python main.py
```

---

## Next Steps

**✅ Recommended**: Use **Option 2 (SQLite)** - it's simpler and works immediately!

```powershell
Copy-Item database_sqlite.py database.py
python main.py
```

Let me know if you hit any other issues!