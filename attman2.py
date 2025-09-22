import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime

# Sample login credentials
users = {"admin": "1234"}
students = ["S001 - Alice", "S002 - Bob", "S003 - Charlie"]

class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance Management System")
        self.root.geometry("500x500")

        self.setup_database()
        self.login_screen()

    def setup_database(self):
        self.conn = sqlite3.connect("attendance.db")
        self.cursor = self.conn.cursor()
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

    def login_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Login", font=("Arial", 20)).pack(pady=20)

        tk.Label(self.root, text="Username").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        tk.Label(self.root, text="Password").pack()
        self.password_entry = tk.Entry(self.root, show='*')
        self.password_entry.pack()

        tk.Button(self.root, text="Login", command=self.authenticate_user).pack(pady=10)

    def authenticate_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in users and users[username] == password:
            self.main_menu_screen()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def main_menu_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Attendance Management", font=("Arial", 18)).pack(pady=20)

        tk.Button(self.root, text="Mark Attendance", width=20, command=self.mark_attendance_screen).pack(pady=10)
        tk.Button(self.root, text="View Attendance", width=20, command=self.view_attendance_screen).pack(pady=10)
        tk.Button(self.root, text="Logout", width=20, command=self.login_screen).pack(pady=20)

    def mark_attendance_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Mark Attendance", font=("Arial", 16)).pack(pady=20)

        tk.Label(self.root, text="Select Student").pack()
        self.selected_student = tk.StringVar()
        self.selected_student.set(students[0])
        tk.OptionMenu(self.root, self.selected_student, *students).pack()

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

    def view_attendance_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Attendance Records", font=("Arial", 16)).pack(pady=20)

        # Treeview Table
        tree = ttk.Treeview(self.root, columns=("ID", "Name", "Date", "Time", "Status"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Name", text="Student Name")
        tree.heading("Date", text="Date")
        tree.heading("Time", text="Time")
        tree.heading("Status", text="Status")
        tree.pack(expand=True, fill="both", padx=10, pady=10)

        # Fetch records
        self.cursor.execute("SELECT * FROM attendance_records ORDER BY id DESC")
        records = self.cursor.fetchall()
        for row in records:
            tree.insert("", "end", values=row)

        tk.Button(self.root, text="Back", command=self.main_menu_screen).pack(pady=10)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Launch the application
if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceApp(root)
    root.mainloop()
