"""
Python GUI login with tkinter styled like modern UI + image panel.
- Left panel: hiển thị ảnh (png/jpg)
- Right panel: form đăng nhập
- Sau khi login thành công -> Home: "Xin chào, <username>"
"""

import tkinter as tk
from PIL import Image, ImageTk  # pip install pillow

# Fake database (chỉnh sửa theo nhu cầu)
USERS = {
    'huutan': '12345',
    'phu': 'password123',
    'user1': 'pass1',
}

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("User Login")
        self.geometry("700x400")
        self.resizable(False, False)

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        self.container = tk.Frame(self, bg="white")
        self.container.pack(fill="both", expand=True)

        self.show_login()

    def clear_container(self):
        for w in self.container.winfo_children():
            w.destroy()

    def show_login(self):
        self.clear_container()

        # Left Panel (blue + image)
        left = tk.Frame(self.container, bg="#1E56F0", width=300, height=400)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        try:
            img = Image.open("test.jpg")  # Đặt file ảnh trong cùng thư mục
            img = img.resize((200, 200))
            self.photo = ImageTk.PhotoImage(img)
            tk.Label(left, image=self.photo, bg="#1E56F0").pack(pady=(80, 10))
        except Exception as e:
            # Nếu không load được ảnh thì fallback text
            tk.Label(left, text="Be Verified", fg="white", bg="#1E56F0",
                     font=("Arial", 20, "bold")).pack(pady=(120, 10))
            tk.Label(left, text="Join experienced Designers\non this platform.",
                     fg="white", bg="#1E56F0", font=("Arial", 10)).pack()

        # Right Panel (login form)
        right = tk.Frame(self.container, bg="white", width=400, height=400)
        right.pack(side="right", fill="both", expand=True)
        right.pack_propagate(False)

        tk.Label(right, text="USER LOGIN", bg="white", fg="#333",
                 font=("Arial", 18, "bold")).pack(pady=(50, 5))
        tk.Label(right, text="Please enter your username and password",
                 bg="white", fg="gray", font=("Arial", 10)).pack(pady=(0, 20))

        tk.Entry(right, textvariable=self.username_var, font=("Arial", 12),
                 bd=1, relief="solid").pack(pady=10, ipady=6, ipadx=60)
        tk.Entry(right, textvariable=self.password_var, show="*", font=("Arial", 12),
                 bd=1, relief="solid").pack(pady=10, ipady=6, ipadx=60)

        login_btn = tk.Button(right, text="Login", bg="#1E56F0", fg="white",
                              font=("Arial", 12, "bold"), relief="flat",
                              command=self.on_login)
        login_btn.pack(pady=20, ipadx=80, ipady=8)

        self.feedback = tk.Label(right, text="", bg="white", fg="red", font=("Arial", 10))
        self.feedback.pack()

    def on_login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get()

        if not username or not password:
            self.feedback.config(text="Please enter both fields")
            return

        if USERS.get(username) == password:
            self.show_home(username)
        else:
            self.feedback.config(text="Invalid username or password")

    def show_home(self, username):
        self.clear_container()

        home = tk.Frame(self.container, bg="white")
        home.pack(fill="both", expand=True)

        tk.Label(home, text=f"Xin chào, {username}", bg="white", fg="#1E56F0",
                 font=("Arial", 20, "bold")).pack(pady=100)

        logout_btn = tk.Button(home, text="Logout", command=self.show_login,
                               bg="#1E56F0", fg="white", font=("Arial", 12, "bold"), relief="flat")
        logout_btn.pack(ipadx=30, ipady=6)


if __name__ == "__main__":
    app = App()
    app.mainloop()
