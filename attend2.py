import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
import requests

class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance Management System")
        self.db_connection()
        self.create_widgets()

    def db_connection(self):
        self.conn = sqlite3.connect("attendance.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                parent_contact TEXT NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                date TEXT,
                status TEXT,
                FOREIGN KEY(student_id) REFERENCES students(student_id)
            )
        """)
        self.conn.commit()

    def create_widgets(self):
        self.clear_frame()
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=20, pady=20)
        tk.Label(self.main_frame, text="Welcome to Attendance System", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.main_frame, text="Admin", width=20, command=self.admin_login).pack(pady=5)
        tk.Button(self.main_frame, text="Student", width=20, command=self.student_view).pack(pady=5)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def admin_login(self):
        self.clear_frame()
        self.admin_frame = tk.Frame(self.root)
        self.admin_frame.pack(padx=20, pady=20)
        tk.Label(self.admin_frame, text="Admin Panel", font=("Arial", 14)).pack(pady=10)
        tk.Button(self.admin_frame, text="Mark Attendance", command=self.mark_attendance).pack(pady=5)
        tk.Button(self.admin_frame, text="View Attendance", command=self.view_attendance).pack(pady=5)
        tk.Button(self.admin_frame, text="Add Student", command=self.add_student).pack(pady=5)
        tk.Button(self.admin_frame, text="Back", command=self.create_widgets).pack(pady=5)

    def student_view(self):
        self.clear_frame()
        self.student_frame = tk.Frame(self.root)
        self.student_frame.pack(padx=20, pady=20)
        tk.Label(self.student_frame, text="Student View", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.student_frame, text="Enter your Name:").pack()
        self.student_name_entry = tk.Entry(self.student_frame)
        self.student_name_entry.pack(pady=5)
        tk.Button(self.student_frame, text="View Attendance", command=self.display_student_attendance).pack(pady=5)
        tk.Button(self.student_frame, text="Back", command=self.create_widgets).pack(pady=5)

    def add_student(self):
        self.clear_frame()
        self.add_frame = tk.Frame(self.root)
        self.add_frame.pack(padx=20, pady=20)
        tk.Label(self.add_frame, text="Add New Student", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.add_frame, text="Name:").pack()
        self.name_entry = tk.Entry(self.add_frame)
        self.name_entry.pack()
        tk.Label(self.add_frame, text="Parent Contact (10-digit):").pack()
        self.contact_entry = tk.Entry(self.add_frame)
        self.contact_entry.pack()
        tk.Button(self.add_frame, text="Add", command=self.insert_student).pack(pady=5)
        tk.Button(self.add_frame, text="Back", command=self.admin_login).pack(pady=5)

    def insert_student(self):
        name = self.name_entry.get()
        contact = self.contact_entry.get()
        if name and contact and len(contact) == 10 and contact.isdigit():
            self.cursor.execute("INSERT INTO students (name, parent_contact) VALUES (?, ?)", (name, contact))
            self.conn.commit()
            messagebox.showinfo("Success", "Student added successfully.")
        else:
            messagebox.showerror("Error", "Invalid input. Please check name and contact number.")

    def mark_attendance(self):
        self.clear_frame()
        self.attendance_frame = tk.Frame(self.root)
        self.attendance_frame.pack(padx=20, pady=20)
        tk.Label(self.attendance_frame, text="Mark Attendance", font=("Arial", 14)).pack(pady=10)
        self.cursor.execute("SELECT student_id, name, parent_contact FROM students")
        self.students = self.cursor.fetchall()
        self.attendance_vars = {}
        for student_id, name, contact in self.students:
            var = tk.StringVar(value="Present")
            frame = tk.Frame(self.attendance_frame)
            frame.pack()
            tk.Label(frame, text=f"StudID: {student_id} - {name}", width=30, anchor='w').pack(side='left')
            tk.Radiobutton(frame, text="Present", variable=var, value="Present").pack(side='left')
            tk.Radiobutton(frame, text="Absent", variable=var, value="Absent").pack(side='left')
            self.attendance_vars[student_id] = (var, name, contact)
        tk.Button(self.attendance_frame, text="Submit", command=self.submit_attendance).pack(pady=10)
        tk.Button(self.attendance_frame, text="Back", command=self.admin_login).pack()

    def submit_attendance(self):
        date = datetime.now().strftime("%Y-%m-%d")
        for student_id, (var, name, contact) in self.attendance_vars.items():
            status = var.get()
            self.cursor.execute("INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)", (student_id, date, status))
            if status == "Absent":
                self.send_sms(contact, name, date)
        self.conn.commit()
        messagebox.showinfo("Success", "Attendance marked and SMS sent to absentees' parents.")

    def send_sms(self, number, student_name, date):
        api_key = "RWXrCNbaHqMowxnZuBT0hKkpdS9v4sDfgGA28Ujm6YtylzQeiOyDk9zpmacHl6IM1rCetwS3uZKYhgvJ"
        message = f"Alert: Your child {student_name} was absent on {date}."
        payload = {
            'sender_id': 'FSTSMS',
            'message': message,
            'language': 'english',
            'route': 'p',
            'numbers': number,
        }
        headers = {
            'authorization': api_key,
            'Content-Type': "application/x-www-form-urlencoded",
            'Cache-Control': "no-cache"
        }
        try:
            response = requests.post("https://www.fast2sms.com/dev/bulk", data=payload, headers=headers)
            print(f"SMS response: {response.text}")
        except Exception as e:
            print("SMS error:", e)

    def view_attendance(self):
        self.clear_frame()
        self.view_frame = tk.Frame(self.root)
        self.view_frame.pack(padx=20, pady=20)
        tk.Label(self.view_frame, text="All Attendance Records", font=("Arial", 14)).pack(pady=10)
        self.cursor.execute("""
            SELECT students.name, attendance.date, attendance.status 
            FROM attendance 
            JOIN students ON attendance.student_id = students.student_id 
            ORDER BY attendance.date DESC
        """)
        records = self.cursor.fetchall()
        tree = ttk.Treeview(self.view_frame, columns=("Name", "Date", "Status"), show='headings', height=15)
        tree.heading("Name", text="Name")
        tree.heading("Date", text="Date")
        tree.heading("Status", text="Status")
        for record in records:
            tree.insert('', tk.END, values=record)
        tree.pack()
        tk.Button(self.view_frame, text="Back", command=self.admin_login).pack(pady=10)

    def display_student_attendance(self):
        name = self.student_name_entry.get()
        if not name:
            messagebox.showerror("Error", "Please enter your name.")
            return
        self.cursor.execute("""
            SELECT attendance.date, attendance.status 
            FROM attendance 
            JOIN students ON attendance.student_id = students.student_id 
            WHERE students.name = ?
            ORDER BY attendance.date DESC
        """, (name,))
        records = self.cursor.fetchall()
        if not records:
            messagebox.showinfo("No Records", "No attendance records found.")
            return
        self.clear_frame()
        frame = tk.Frame(self.root)
        frame.pack(padx=20, pady=20)
        tk.Label(frame, text=f"Attendance for {name}", font=("Arial", 14)).pack(pady=10)
        tree = ttk.Treeview(frame, columns=("Date", "Status"), show='headings', height=15)
        tree.column("Date", width=150)
        tree.column("Status", width=100)

        for rec in records:
            tree.insert('', tk.END, values=rec)
        tree.pack()
        tk.Button(frame, text="Back", command=self.create_widgets).pack(pady=10)

root = tk.Tk()
app = AttendanceApp(root)
root.mainloop()
