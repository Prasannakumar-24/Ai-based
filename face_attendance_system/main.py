#!/usr/bin/env python3
"""
Face Recognition Attendance System - Main Entry Point

This system provides automated attendance marking using face recognition.
Built with DeepFace, OpenCV, CustomTkinter, and MySQL.

Author: AI Assistant
Date: April 18, 2026
"""

import sys
import os
import io

# Fix unicode encode error on Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from database import DatabaseManager
from face_recognition_cv2 import FaceRecognitionManager
from gui import AttendanceGUI
import mysql.connector
from mysql.connector import Error

def setup_database():
    """
    Set up MySQL database and tables

    Returns:
        DatabaseManager: Configured database manager instance
    """
    print("Setting up database...")

    db = DatabaseManager()

    # Try to connect to MySQL
    if not db.connect():
        print("Failed to connect to MySQL. Please ensure:")
        print("1. MySQL server is running")
        print("2. Update database credentials in database.py")
        print("3. Create database 'face_attendance_system' manually if needed")
        return None

    # Create tables
    if not db.create_tables():
        print("Failed to create database tables")
        return None

    print("Database setup complete!")
    return db

def main():
    """
    Main function to start the Face Recognition Attendance System
    """
    print("=" * 60)
    print("   Face Recognition Attendance System")
    print("=" * 60)

    # Setup database
    db_manager = setup_database()
    if not db_manager:
        print("Exiting due to database setup failure")
        sys.exit(1)

    # Initialize face recognition manager
    print("Initializing face recognition system...")
    face_manager = FaceRecognitionManager(db_manager)
    face_manager.cooldown_seconds = 0  # Disable cooldown to fix Unknown Face bug

    # Start Web App
    print("Starting Web Frontend on http://127.0.0.1:5000...")
    from app import app, set_managers
    set_managers(db_manager, face_manager)
    try:
        app.run(host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
    except Exception as e:
        print(f"Error running application: {e}")
    finally:
        # Clean up database connection
        if db_manager:
            db_manager.close_connection()

if __name__ == "__main__":
    main()
