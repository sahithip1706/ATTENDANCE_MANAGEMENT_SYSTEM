import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance Management System")
        self.root.geometry("900x500")

        self.users = {"admin": "0987"}

        self.students = []  # Loaded from DB
        self.parent_contacts = {}  # Loaded with students
        self.setup_database()
        self.role_selection_screen()

    def setup_database(self):
        self.conn = sqlite3.connect("attendance.db")
        self.cursor = self.conn.cursor()

        # Create tables if they don't exist
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                name TEXT NOT NULL
            )
        """)
        # Try to add parent_contact column
        try:
            self.cursor.execute("ALTER TABLE students ADD COLUMN parent_contact TEXT")
        except sqlite3.OperationalError:
            pass  # Column already exists

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS attendance_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                status TEXT NOT NULL
            )
        """)
        self.conn.commit()
        self.load_students()

    def load_students(self):
        self.cursor.execute("SELECT student_id, name, parent_contact FROM students")
        rows = self.cursor.fetchall()
        self.students = [f"{sid} - {name}" for sid, name, _ in rows]
        self.parent_contacts = {f"{sid} - {name}": contact for sid, name, contact in rows}

    def role_selection_screen(self):
        self.clear_frame()
        tk.Label(self.root, text="Welcome To Attendance Management System", font=("Times New Roman", 32)).pack(pady=20)
        tk.Label(self.root, text="Select Role", font=("Arial", 18)).pack(pady=20)
        tk.Button(self.root, text="Admin", width=20, command=self.admin_login).pack(pady=10)
        tk.Button(self.root, text="Student", width=20, command=self.student_portal).pack(pady=10)

    def admin_login(self):
        self.clear_frame()
        tk.Label(self.root, text="Admin Login", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Username").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        tk.Label(self.root, text="Password").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        tk.Button(self.root, text="Login", command=self.verify_login).pack(pady=10)

    def verify_login(self):
        user = self.username_entry.get()
        pwd = self.password_entry.get()
        if user in self.users and self.users[user] == pwd:
            self.admin_portal()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")

    def admin_portal(self):
        self.clear_frame()
        self.load_students()

        tk.Label(self.root, text="Admin Panel", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.root, text="Add Student", command=self.add_student_screen).pack(pady=5)

        self.selected_student = tk.StringVar()
        self.selected_student.set(self.students[0] if self.students else "")
        ttk.Combobox(self.root, textvariable=self.selected_student, values=self.students).pack(pady=5)

        tk.Button(self.root, text="Mark Present", command=lambda: self.mark_attendance("Present")).pack(pady=2)
        tk.Button(self.root, text="Mark Absent", command=lambda: self.mark_attendance("Absent")).pack(pady=2)
        tk.Button(self.root, text="View Attendance", command=self.view_attendance).pack(pady=5)
        self.status_label = tk.Label(self.root, text="", fg="green")
        self.status_label.pack(pady=5)

        tk.Button(self.root, text="Back", command=self.role_selection_screen).pack(pady=10)

    def mark_attendance(self, status):
        student = self.selected_student.get()
        if not student:
            messagebox.showwarning("No Student", "Select a student.")
            return

        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")

        self.cursor.execute("INSERT INTO attendance_records (student_name, date, time, status) VALUES (?, ?, ?, ?)",
                            (student, date, time, status))
        self.conn.commit()

        self.status_label.config(text=f"{student} marked as {status} at {time}")

        if status == "Absent":
            contact = self.parent_contacts.get(student, "unknown")
            message = f"Message sent to {contact}:\nYour child {student} was absent on {date}."
            messagebox.showinfo("Parent Notified", message)

    def view_attendance(self):
        self.clear_frame()
        self.cursor.execute("SELECT * FROM attendance_records ORDER BY id DESC")
        records = self.cursor.fetchall()

        tk.Label(self.root, text="Attendance Records", font=("Arial", 14)).pack(pady=5)
        tree = ttk.Treeview(self.root, columns=("ID", "Student", "Date", "Time", "Status"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Student", text="Student")
        tree.heading("Date", text="Date")
        tree.heading("Time", text="Time")
        tree.heading("Status", text="Status")

        for row in records:
            tree.insert("", tk.END, values=row)

        tree.pack(expand=True, fill="both")
        tk.Button(self.root, text="Back", command=self.admin_portal).pack(pady=10)

    def add_student_screen(self):
        self.clear_frame()
        tk.Label(self.root, text="Add New Student", font=("Arial", 14)).pack(pady=10)

        tk.Label(self.root, text="Student ID").pack()
        self.new_student_id = tk.Entry(self.root)
        self.new_student_id.pack()

        tk.Label(self.root, text="Name").pack()
        self.new_student_name = tk.Entry(self.root)
        self.new_student_name.pack()

        tk.Label(self.root, text="Parent Contact (Email or Phone)").pack()
        self.new_parent_contact = tk.Entry(self.root)
        self.new_parent_contact.pack()

        tk.Button(self.root, text="Save", command=self.save_new_student).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.admin_portal).pack()

    def save_new_student(self):
        sid = self.new_student_id.get().strip()
        name = self.new_student_name.get().strip()
        contact = self.new_parent_contact.get().strip()

        if not sid or not name or not contact:
            messagebox.showerror("Error", "All fields are required.")
            return

        self.cursor.execute("INSERT INTO students (student_id, name, parent_contact) VALUES (?, ?, ?)",
                            (sid, name, contact))
        self.conn.commit()
        self.load_students()
        messagebox.showinfo("Success", "Student added successfully!")
        self.admin_portal()

    def student_portal(self):
        self.clear_frame()
        self.load_students()

        tk.Label(self.root, text="Student Portal", font=("Arial", 16)).pack(pady=10)

        self.student_view = tk.StringVar()
        self.student_view.set(self.students[0] if self.students else "")
        ttk.Combobox(self.root, textvariable=self.student_view, values=self.students).pack(pady=10)

        tk.Button(self.root, text="View My Attendance", command=self.view_my_attendance).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.role_selection_screen).pack(pady=10)

    def view_my_attendance(self):
        student = self.student_view.get()
        if not student:
            messagebox.showwarning("Select Student", "Choose a student first.")
            return

        self.clear_frame()
        tk.Label(self.root, text=f"Attendance for {student}", font=("Arial", 14)).pack(pady=5)

        self.cursor.execute("SELECT date, time, status FROM attendance_records WHERE student_name=? ORDER BY id DESC", (student,))
        records = self.cursor.fetchall()

        tree = ttk.Treeview(self.root, columns=("Date", "Time", "Status"), show="headings")
        tree.heading("Date", text="Date")
        tree.heading("Time", text="Time")
        tree.heading("Status", text="Status")

        for row in records:
            tree.insert("", tk.END, values=row)

        tree.pack(expand=True, fill="both")
        tk.Button(self.root, text="Back", command=self.student_portal).pack(pady=10)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceApp(root)
    root.mainloop()
