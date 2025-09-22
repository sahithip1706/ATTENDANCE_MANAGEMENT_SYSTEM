import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime

class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance Management System")
        self.root.geometry("600x500")

        self.users = {"admin": "1234"}
        self.students = []
        self.parent_contacts = {"S001 - Alice": "alice_parent@example.com","S002 - Bob": "bob_parent@example.com",
                                "S003 - Charlie": "charlie_parent@example.com","S004 - Diana": "diana_parent@example.com"}
        self.setup_database()
        self.role_selection_screen()

    def setup_database(self):
        self.conn = sqlite3.connect("attendance.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                name TEXT NOT NULL,
                parent_contact TEXT
            )
        """)
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

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def role_selection_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Welcome to Attendance System", font=("Arial", 18)).pack(pady=30)
        tk.Button(self.root, text="Admin Login", width=20, command=self.admin_login_screen).pack(pady=10)
        tk.Button(self.root, text="Student Access", width=20, command=self.student_entry_screen).pack(pady=10)

    def admin_login_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Admin Login", font=("Arial", 20)).pack(pady=20)

        tk.Label(self.root, text="Username").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        tk.Label(self.root, text="Password").pack()
        self.password_entry = tk.Entry(self.root, show='*')
        self.password_entry.pack()

        tk.Button(self.root, text="Login", command=self.authenticate_admin).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.role_selection_screen).pack()

    def authenticate_admin(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username in self.users and self.users[username] == password:
            self.main_menu_screen()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def main_menu_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Admin Dashboard", font=("Arial", 18)).pack(pady=20)

        tk.Button(self.root, text="Mark Attendance", width=20, command=self.mark_attendance_screen).pack(pady=10)
        tk.Button(self.root, text="View All Attendance", width=20, command=self.view_attendance_screen).pack(pady=10)
        tk.Button(self.root, text="Add Student", width=20, command=self.add_student_screen).pack(pady=10)
        tk.Button(self.root, text="Logout", width=20, command=self.role_selection_screen).pack(pady=20)

    def mark_attendance_screen(self):
        self.clear_screen()
        self.load_students()

        tk.Label(self.root, text="Mark Attendance", font=("Arial", 16)).pack(pady=20)

        tk.Label(self.root, text="Select Student").pack()
        self.selected_student = tk.StringVar()
        if self.students:
            self.selected_student.set(self.students[0])
        tk.OptionMenu(self.root, self.selected_student, *self.students).pack()

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Mark Present", bg="green", fg="white",
                  command=lambda: self.mark_attendance("Present")).pack(side="left", padx=10)
        tk.Button(button_frame, text="Mark Absent", bg="red", fg="white",
                  command=lambda: self.mark_attendance("Absent")).pack(side="left", padx=10)

        self.status_label = tk.Label(self.root, text="", fg="blue", font=("Arial", 12))
        self.status_label.pack(pady=10)

        tk.Button(self.root, text="Back", command=self.main_menu_screen).pack(pady=10)

    def mark_attendance(self, status):
        student = self.selected_student.get()
        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")

        self.cursor.execute("INSERT INTO attendance_records (student_name, date, time, status) VALUES (?, ?, ?, ?)",
                            (student, date, time, status))
        self.conn.commit()
        self.status_label.config(text=f"{student} marked as {status} at {time}")

        if status == "Absent":
            contact = self.parent_contacts.get(student, "unknown")
            message = f"Message sent to {contact}: Your child {student} was absent on {date}."
            messagebox.showinfo("Parent Notified", message)

    def view_attendance_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="All Attendance Records", font=("Arial", 16)).pack(pady=20)

        tree = ttk.Treeview(self.root, columns=("ID", "Name", "Date", "Time", "Status"), show="headings")
        for col in ("ID", "Name", "Date", "Time", "Status"):
            tree.heading(col, text=col)
        tree.pack(expand=True, fill="both", padx=10, pady=10)

        self.cursor.execute("SELECT * FROM attendance_records ORDER BY id DESC")
        for row in self.cursor.fetchall():
            tree.insert("", "end", values=row)

        tk.Button(self.root, text="Back", command=self.main_menu_screen).pack(pady=10)

    def add_student_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Add New Student", font=("Arial", 18)).pack(pady=20)

        tk.Label(self.root, text="Student ID (e.g., S004)").pack()
        self.new_student_id = tk.Entry(self.root)
        self.new_student_id.pack(pady=5)

        tk.Label(self.root, text="Student Name").pack()
        self.new_student_name = tk.Entry(self.root)
        self.new_student_name.pack(pady=5)

        tk.Label(self.root, text="Parent Contact (email/phone)").pack()
        self.new_parent_contact = tk.Entry(self.root)
        self.new_parent_contact.pack(pady=5)

        tk.Button(self.root, text="Add Student", command=self.save_new_student).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.main_menu_screen).pack()

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
        messagebox.showinfo("Success", f"Student {sid} - {name} added!")
        self.main_menu_screen()

    def student_entry_screen(self):
        self.clear_screen()
        self.load_students()

        tk.Label(self.root, text="Student Access", font=("Arial", 18)).pack(pady=20)
        tk.Label(self.root, text="Enter Your ID & Name (e.g., S001 - Alice)").pack()
        self.student_name_entry = tk.Entry(self.root, width=40)
        self.student_name_entry.pack(pady=10)

        tk.Button(self.root, text="View My Attendance", command=self.view_student_attendance).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.role_selection_screen).pack()

    def view_student_attendance(self):
        name = self.student_name_entry.get().strip()
        self.cursor.execute("SELECT date, time, status FROM attendance_records WHERE student_name=? ORDER BY id DESC", (name,))
        records = self.cursor.fetchall()

        if not records:
            messagebox.showinfo("No Records", "No attendance found or invalid student.")
            return

        self.clear_screen()
        tk.Label(self.root, text=f"Attendance for {name}", font=("Arial", 16)).pack(pady=20)

        tree = ttk.Treeview(self.root, columns=("Date", "Time", "Status"), show="headings")
        for col in ("Date", "Time", "Status"):
            tree.heading(col, text=col)
        tree.pack(expand=True, fill="both", padx=10, pady=10)

        for row in records:
            tree.insert("", "end", values=row)

        tk.Button(self.root, text="Back", command=self.role_selection_screen).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceApp(root)
    root.mainloop()