import sqlite3
import os
import threading
from datetime import datetime

class DatabaseManager:
    """
    Thread-safe SQLite database manager for Face Recognition Attendance System
    Handles multi-threaded access to SQLite database
    """

    def __init__(self, db_file="attendance.db"):
        """Initialize thread-safe SQLite database"""
        self.db_file = db_file
        self.lock = threading.Lock()  # Thread safety lock
        self.local = threading.local()  # Thread-local storage for connections

    def get_connection(self):
        """Get a connection for the current thread"""
        # Create new connection for this thread if it doesn't exist
        if not hasattr(self.local, 'connection') or self.local.connection is None:
            try:
                # check_same_thread=False allows using connection across threads with our lock
                self.local.connection = sqlite3.connect(
                    self.db_file,
                    check_same_thread=False,
                    timeout=10.0  # Wait up to 10 seconds for database lock
                )
                self.local.connection.row_factory = sqlite3.Row
            except Exception as e:
                print(f"Error creating database connection: {e}")
                return None
        return self.local.connection

    def connect(self):
        """Establish connection to SQLite database"""
        try:
            conn = self.get_connection()
            if conn:
                print("[SUCCESS] Successfully connected to SQLite database")
                return True
            return False
        except Exception as e:
            print(f"[ERROR] Error connecting to SQLite database: {e}")
            return False

    def create_tables(self):
        """Create necessary tables if they don't exist"""
        try:
            with self.lock:
                conn = self.get_connection()
                if not conn:
                    return False
                
                cursor = conn.cursor()

                # Create users table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT UNIQUE NOT NULL,
                        name TEXT NOT NULL,
                        face_image_path TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')

                # Create attendance table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS attendance (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT NOT NULL,
                        name TEXT NOT NULL,
                        check_in_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        date DATE NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                    )
                ''')

                conn.commit()
                print("[SUCCESS] Database tables created successfully")
                return True

        except Exception as e:
            print(f"[ERROR] Error creating tables: {e}")
            return False

    def add_user(self, user_id, name, face_image_path=None):
        """Add a new user to the database (thread-safe)"""
        try:
            with self.lock:
                conn = self.get_connection()
                if not conn:
                    return False
                
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (user_id, name, face_image_path) VALUES (?, ?, ?)",
                    (user_id, name, face_image_path)
                )
                conn.commit()
                print(f"[SUCCESS] User {name} added successfully")
                return True
        except Exception as e:
            print(f"[ERROR] Error adding user: {e}")
            return False

    def get_user_by_id(self, user_id):
        """Get user information by user ID (thread-safe)"""
        try:
            with self.lock:
                conn = self.get_connection()
                if not conn:
                    return None
                
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
                user = cursor.fetchone()
                return dict(user) if user else None
        except Exception as e:
            print(f"[ERROR] Error getting user: {e}")
            return None

    def get_all_users(self):
        """Get all users from database (thread-safe)"""
        try:
            with self.lock:
                conn = self.get_connection()
                if not conn:
                    return []
                
                cursor = conn.cursor()
                cursor.execute("SELECT user_id, name FROM users")
                users = cursor.fetchall()
                return [dict(user) for user in users]
        except Exception as e:
            print(f"[ERROR] Error getting users: {e}")
            return []

    def mark_attendance(self, user_id, name):
        """Mark attendance for a user (thread-safe, avoid duplicates)"""
        try:
            with self.lock:
                conn = self.get_connection()
                if not conn:
                    return False
                
                cursor = conn.cursor()
                today = datetime.now().date()

                # Check if attendance already marked for today
                cursor.execute(
                    "SELECT id FROM attendance WHERE user_id = ? AND date = ?",
                    (user_id, today)
                )

                if cursor.fetchone():
                    return False

                # Mark new attendance
                cursor.execute(
                    "INSERT INTO attendance (user_id, name, date) VALUES (?, ?, ?)",
                    (user_id, name, today)
                )
                conn.commit()
                print(f"[SUCCESS] Attendance marked for {name}")
                return True

        except Exception as e:
            print(f"[ERROR] Error marking attendance: {e}")
            return False

    def get_attendance_records(self, limit=50):
        """Get recent attendance records (thread-safe)"""
        try:
            with self.lock:
                conn = self.get_connection()
                if not conn:
                    return []
                
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM attendance ORDER BY check_in_time DESC LIMIT ?",
                    (limit,)
                )
                records = cursor.fetchall()
                return [dict(record) for record in records]
        except Exception as e:
            print(f"[ERROR] Error getting attendance records: {e}")
            return []

    def get_today_attendance(self):
        """Get today's attendance records (thread-safe)"""
        try:
            with self.lock:
                conn = self.get_connection()
                if not conn:
                    return []
                
                cursor = conn.cursor()
                today = datetime.now().date()
                cursor.execute(
                    "SELECT * FROM attendance WHERE date = ? ORDER BY check_in_time DESC",
                    (today,)
                )
                records = cursor.fetchall()
                return [dict(record) for record in records]
        except Exception as e:
            print(f"[ERROR] Error getting today's attendance: {e}")
            return []

    def close_connection(self):
        """Close database connection"""
        try:
            with self.lock:
                if hasattr(self.local, 'connection') and self.local.connection:
                    self.local.connection.close()
                    self.local.connection = None
                    print("[SUCCESS] Database connection closed")
        except Exception as e:
            print(f"[ERROR] Error closing connection: {e}")
