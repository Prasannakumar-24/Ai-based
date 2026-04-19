# Setup Guide - Face Recognition Attendance System

## Windows PowerShell - MySQL Database Setup

### Method 1: Using PowerShell with MySQL (Recommended)

```powershell
# Navigate to the project directory
cd c:\Users\ADMIN\Downloads\python\face_attendance_system

# Run the SQL schema using PowerShell
Get-Content database_schema.sql | mysql -u root -p
```

Then enter your MySQL password when prompted.

---

### Method 2: Using MySQL Directly from PowerShell

```powershell
# Without password (if no password is set)
mysql -u root < database_schema.sql

# With password
mysql -u root -p"your_password" < database_schema.sql
```

---

### Method 3: Using MySQL Command Line Tool Directly

```powershell
# Open MySQL command line
mysql -u root -p

# Once inside MySQL prompt, run:
source database_schema.sql;
```

---

### Method 4: Using Python Setup Script (Automated)

The easiest way is to use the included Python setup script:

```powershell
python setup.py
```

This will:
1. Verify Python version
2. Check all dependencies
3. Connect to MySQL
4. Create database and tables automatically
5. Create faces directory

---

## Step-by-Step Installation

### Step 1: Install MySQL
- Download from: https://dev.mysql.com/downloads/mysql/
- During installation, remember your password or set no password
- Ensure MySQL Server is running

### Step 2: Install Python Dependencies
```powershell
cd c:\Users\ADMIN\Downloads\python\face_attendance_system
pip install -r requirements.txt
```

### Step 3: Setup Database (Choose One Method)

#### Option A: Automated (Recommended)
```powershell
python setup.py
```

#### Option B: Manual with PowerShell
```powershell
Get-Content database_schema.sql | mysql -u root -p
```

### Step 4: Configure Database Credentials

Edit `database.py`:
```python
self.host = 'localhost'
self.user = 'root'  # Your MySQL username
self.password = ''  # Your MySQL password
self.database = 'face_attendance_system'
```

### Step 5: Run the Application
```powershell
python main.py
```

---

## Troubleshooting

### MySQL Command Not Found
If you get "mysql : The term 'mysql' is not recognized", MySQL is not in your PATH:

**Solution**: Add MySQL to Windows PATH
1. Find MySQL installation directory (usually `C:\Program Files\MySQL\MySQL Server 8.0\bin`)
2. Open Environment Variables
3. Add the MySQL bin directory to PATH
4. Restart PowerShell

Or use the full path:
```powershell
"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql" -u root -p < database_schema.sql
```

### MySQL Connection Refused
- Ensure MySQL Server is running
- Check if port 3306 is available
- Verify username and password

### DeepFace Installation Issues
```powershell
# Install system dependencies
pip install cmake
pip install dlib --verbose
pip install deepface
```

---

## Verification

After setup, verify everything works:

```powershell
# Test database connection
python -c "from database import DatabaseManager; db = DatabaseManager(); print('✅ Database connected!' if db.connect() else '❌ Connection failed')"

# Test face recognition
python -c "from face_recognition import FaceRecognitionManager; print('✅ Face recognition module loaded!')"

# Test GUI
python main.py
```