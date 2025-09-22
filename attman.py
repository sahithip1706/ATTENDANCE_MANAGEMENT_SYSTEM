import tkinter as tk
from tkinter import messagebox

# Sample database of users and students for demo purposes
users = {"admin": "1234"}
students = ["S001 - Alice", "S002 - Bob", "S003 - Charlie"]

# Main Application Class
class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance Management System")
        self.root.geometry("400x400")
        self.login_screen()

    def login_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Login", font=("Arial", 18)).pack(pady=20)

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
            self.mark_attendance_screen()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

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

    def mark_attendance(self, status):
      student = self.selected_student.get()
      # Here you would normally save to a database with a timestamp
      self.status_label.config(text=f"{student} marked as {status}.")

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Create GUI window
if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceApp(root)
    root.mainloop()
