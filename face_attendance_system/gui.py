import customtkinter as ctk
from tkinter import messagebox, ttk
import threading
from datetime import datetime
from PIL import Image, ImageTk
import os

class AttendanceGUI:
    """
    Main GUI class for the Face Recognition Attendance System using CustomTkinter
    """

    def __init__(self, database_manager, face_recognition_manager):
        """
        Initialize the GUI

        Args:
            database_manager: DatabaseManager instance
            face_recognition_manager: FaceRecognitionManager instance
        """
        self.db = database_manager
        self.face_recog = face_recognition_manager

        # Configure appearance
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Create main window
        self.root = ctk.CTk()
        self.root.title("Face Recognition Attendance System")
        self.root.geometry("900x700")
        self.root.resizable(True, True)

        # Initialize variables
        self.monitoring_active = False
        self.monitoring_thread = None

        # Create GUI elements
        self.create_widgets()
        self.update_attendance_display()

    def create_widgets(self):
        """Create all GUI widgets and layout"""

        # Main container
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="Face Recognition Attendance System",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(20, 30))

        # Control buttons frame
        buttons_frame = ctk.CTkFrame(main_frame)
        buttons_frame.pack(fill="x", padx=20, pady=(0, 20))

        # Register User button
        self.register_btn = ctk.CTkButton(
            buttons_frame,
            text="Register User",
            command=self.register_user,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=50
        )
        self.register_btn.pack(side="left", padx=(0, 10), expand=True)

        # Start Attendance button
        self.start_btn = ctk.CTkButton(
            buttons_frame,
            text="Start Attendance",
            command=self.toggle_attendance_monitoring,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=50,
            fg_color="green",
            hover_color="darkgreen"
        )
        self.start_btn.pack(side="left", padx=(0, 10), expand=True)

        # View Attendance button
        self.view_btn = ctk.CTkButton(
            buttons_frame,
            text="View Attendance",
            command=self.view_attendance,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=50
        )
        self.view_btn.pack(side="left", expand=True)

        # Status frame
        status_frame = ctk.CTkFrame(main_frame)
        status_frame.pack(fill="x", padx=20, pady=(0, 20))

        # Status label
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="System Ready",
            font=ctk.CTkFont(size=16)
        )
        self.status_label.pack(pady=(10, 5))

        # Face detection status label
        self.face_status_label = ctk.CTkLabel(
            status_frame,
            text="",
            font=ctk.CTkFont(size=14),
            text_color="orange"
        )
        self.face_status_label.pack(pady=(0, 10))

        # Statistics frame
        stats_frame = ctk.CTkFrame(main_frame)
        stats_frame.pack(fill="x", padx=20, pady=(0, 20))

        # Statistics labels
        self.registered_count_label = ctk.CTkLabel(
            stats_frame,
            text="Registered Users: 0",
            font=ctk.CTkFont(size=14)
        )
        self.registered_count_label.pack(side="left", padx=(20, 40))

        self.today_attendance_label = ctk.CTkLabel(
            stats_frame,
            text="Today's Attendance: 0",
            font=ctk.CTkFont(size=14)
        )
        self.today_attendance_label.pack(side="left", padx=(0, 40))

        # Attendance display frame
        display_frame = ctk.CTkFrame(main_frame)
        display_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Attendance table
        self.create_attendance_table(display_frame)

        # Footer
        footer_label = ctk.CTkLabel(
            main_frame,
            text="Press 'q' in camera windows to stop operations",
            font=ctk.CTkFont(size=12)
        )
        footer_label.pack(pady=(0, 10))

    def create_attendance_table(self, parent):
        """Create the attendance records table"""

        # Table title
        table_title = ctk.CTkLabel(
            parent,
            text="Recent Attendance Records",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        table_title.pack(pady=(10, 10))

        # Create Treeview for attendance records
        columns = ("Date", "Time", "User ID", "Name")
        self.attendance_tree = ttk.Treeview(parent, columns=columns, show="headings", height=15)

        # Configure columns
        for col in columns:
            self.attendance_tree.heading(col, text=col)
            self.attendance_tree.column(col, width=150, anchor="center")

        # Style the treeview
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 10))
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

        # Add scrollbar
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.attendance_tree.yview)
        self.attendance_tree.configure(yscrollcommand=scrollbar.set)

        # Pack elements
        self.attendance_tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side="right", fill="y", pady=10, padx=(0, 10))

    def register_user(self):
        """Handle user registration"""
        # Create registration dialog
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Register New User")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()

        # User ID input
        id_label = ctk.CTkLabel(dialog, text="User ID:")
        id_label.pack(pady=(20, 5))
        id_entry = ctk.CTkEntry(dialog, placeholder_text="Enter unique user ID")
        id_entry.pack(pady=(0, 10), padx=20, fill="x")

        # Name input
        name_label = ctk.CTkLabel(dialog, text="Full Name:")
        name_label.pack(pady=(10, 5))
        name_entry = ctk.CTkEntry(dialog, placeholder_text="Enter full name")
        name_entry.pack(pady=(0, 20), padx=20, fill="x")

        # Register button
        def do_register():
            user_id = id_entry.get().strip()
            name = name_entry.get().strip()

            if not user_id or not name:
                messagebox.showerror("Error", "Please fill in all fields")
                return

            # Check if user already exists
            existing_user = self.db.get_user_by_id(user_id)
            if existing_user:
                messagebox.showerror("Error", f"User ID '{user_id}' already exists")
                return

            # Update status
            self.status_label.configure(text=f"Registering {name}... Please look at the camera")
            dialog.destroy()

            # Start face capture in a separate thread
            def capture_thread():
                success = self.face_recog.capture_face_images(user_id, name)
                if success:
                    self.root.after(0, lambda: messagebox.showinfo("Success", f"User {name} registered successfully!"))
                    self.root.after(0, self.update_statistics)
                else:
                    self.root.after(0, lambda: messagebox.showerror("Error", "Failed to register user"))
                self.root.after(0, lambda: self.status_label.configure(text="System Ready"))
                self.root.after(0, lambda: self.face_status_label.configure(text=""))

            threading.Thread(target=capture_thread, daemon=True).start()

        register_btn = ctk.CTkButton(dialog, text="Start Face Capture", command=do_register)
        register_btn.pack(pady=10)

    def toggle_attendance_monitoring(self):
        """Toggle attendance monitoring on/off"""
        if not self.monitoring_active:
            # Start monitoring
            self.monitoring_active = True
            self.start_btn.configure(text="Stop Attendance", fg_color="red", hover_color="darkred")
            self.status_label.configure(text="Attendance monitoring active...")

            # Start monitoring in a separate thread
            self.monitoring_thread = threading.Thread(target=self.start_monitoring_thread, daemon=True)
            self.monitoring_thread.start()
        else:
            # Stop monitoring
            self.monitoring_active = False
            self.start_btn.configure(text="Start Attendance", fg_color="green", hover_color="darkgreen")
            self.status_label.configure(text="Attendance monitoring stopped")

    def start_monitoring_thread(self):
        """Run attendance monitoring in a separate thread"""
        try:
            self.face_recog.start_attendance_monitoring()
        except Exception as e:
            print(f"Error in monitoring thread: {e}")
        finally:
            # Reset UI when monitoring stops
            if self.monitoring_active:
                self.root.after(0, lambda: self.toggle_attendance_monitoring())
            self.root.after(0, self.update_attendance_display)

    def view_attendance(self):
        """Refresh and display attendance records"""
        self.update_attendance_display()
        messagebox.showinfo("Info", "Attendance records updated")

    def update_attendance_display(self):
        """Update the attendance table with latest records"""
        # Clear existing items
        for item in self.attendance_tree.get_children():
            self.attendance_tree.delete(item)

        # Get attendance records
        records = self.db.get_attendance_records()

        # Add records to table
        for record in records:
            check_in_time = record['check_in_time']
            if isinstance(check_in_time, str):
                # Parse string datetime
                dt = datetime.fromisoformat(check_in_time.replace('Z', '+00:00'))
            else:
                dt = check_in_time

            date_str = dt.strftime("%Y-%m-%d")
            time_str = dt.strftime("%H:%M:%S")

            self.attendance_tree.insert("", "end", values=(
                date_str,
                time_str,
                record['user_id'],
                record['name']
            ))

        # Update statistics
        self.update_statistics()

    def update_statistics(self):
        """Update statistics labels"""
        registered_count = self.face_recog.get_registered_users_count()
        today_records = self.db.get_today_attendance()
        today_count = len(today_records)

        self.registered_count_label.configure(text=f"Registered Users: {registered_count}")
        self.today_attendance_label.configure(text=f"Today's Attendance: {today_count}")

    def run(self):
        """Start the GUI main loop"""
        self.root.mainloop()
