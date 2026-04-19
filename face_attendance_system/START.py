#!/usr/bin/env python3
"""
🚀 MASTER SETUP - One Command Solution
Handles all database setup issues automatically
"""

import os
import sys
import subprocess
import shutil
import time

def print_banner():
    print("\n" + "="*70)
    print("  🚀 Face Recognition Attendance System - MASTER SETUP")
    print("="*70)

def setup_sqlite():
    """Quick SQLite setup"""
    print("\n📦 Setting up SQLite...")
    try:
        # Backup MySQL version if exists
        if os.path.exists("database.py") and "mysql" in open("database.py").read().lower():
            shutil.copy("database.py", "database_mysql_backup.py")
        
        # Copy SQLite
        shutil.copy("database_sqlite.py", "database.py")
        print("✅ SQLite activated")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def start_mysql_service():
    """Try to start MySQL service on Windows"""
    print("\n🔧 Attempting to start MySQL service...")
    try:
        # Find MySQL service
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", 
             "Get-Service | Where-Object {$_.Name -like '*mysql*'} | Select-Object -First 1 -ExpandProperty Name"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        service_name = result.stdout.strip()
        if not service_name:
            print("⚠️ MySQL service not found")
            return False
        
        print(f"Found service: {service_name}")
        
        # Try to start it
        subprocess.run(
            ["powershell", "-NoProfile", "-Command", f"Start-Service {service_name}"],
            capture_output=True,
            timeout=10
        )
        
        time.sleep(2)
        
        # Verify running
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", 
             f"(Get-Service {service_name}).Status"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if "Running" in result.stdout:
            print(f"✅ {service_name} started successfully")
            return True
        else:
            print(f"❌ {service_name} failed to start")
            return False
            
    except Exception as e:
        print(f"⚠️ Could not start service: {e}")
        return False

def test_mysql():
    """Test MySQL connection"""
    try:
        import mysql.connector
        connection = mysql.connector.connect(
            host='localhost',
            user='prasanna kumar',
            password='ajay'
        )
        connection.close()
        print("✅ MySQL connection successful")
        return True
    except Exception as e:
        print(f"❌ MySQL not available: {str(e)[:50]}...")
        return False

def main():
    """Main setup"""
    print_banner()
    
    print("\n🔍 Analyzing system...")
    print("-" * 70)
    
    # Check if MySQL is available
    mysql_available = test_mysql()
    
    print("\n" + "-" * 70)
    print("📋 RECOMMENDED OPTIONS:")
    print("-" * 70)
    
    if mysql_available:
        print("\n✅ MySQL is available!")
        print("\nYou can:")
        print("  1. Use MySQL (advanced)")
        print("  2. Use SQLite (recommended)")
        print("\nBest choice: SQLite (faster setup)")
    else:
        print("\n❌ MySQL not available")
        print("\nOptions:")
        print("  1. Start MySQL service (if installed)")
        print("  2. Use SQLite (recommended)")
        print("\nBest choice: SQLite (instant)")
    
    print("\n" + "-" * 70)
    choice = input("\nChoose 1 (MySQL) or 2 (SQLite) [2]: ").strip() or "2"
    
    if choice == "1":
        if mysql_available:
            print("\n✅ MySQL is ready! Running application...")
            run_app()
        else:
            print("\n🔧 Attempting to start MySQL...")
            if start_mysql_service():
                print("\n✅ MySQL is now running!")
                run_app()
            else:
                print("\n⚠️ Could not start MySQL")
                print("Switching to SQLite instead...")
                if setup_sqlite():
                    run_app()
    else:
        print("\n📦 Setting up SQLite (instant)...")
        if setup_sqlite():
            print("✅ SQLite ready!")
            run_app()

def run_app():
    """Run the application"""
    print("\n" + "="*70)
    print("🎉 Setup Complete! Starting Application...")
    print("="*70 + "\n")
    
    time.sleep(1)
    
    try:
        # Run main.py
        os.system("python main.py")
    except Exception as e:
        print(f"Error running application: {e}")
        print("Try running manually: python main.py")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
