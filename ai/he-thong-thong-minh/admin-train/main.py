import tkinter as tk
from tkinter import ttk, messagebox


# --- Mock results for demo ---
mock_results = {
    "SVM (HOG)":     {"accuracy": 0.85, "f1": 0.83, "precision": 0.87, "recall": 0.82},
    "Random Forest": {"accuracy": 0.88, "f1": 0.86, "precision": 0.89, "recall": 0.84},
    "MobileNetV2":   {"accuracy": 0.92, "f1": 0.91, "precision": 0.93, "recall": 0.90},
}

class TrainerApp(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("👁️ Drowsy Driver – Model Training Dashboard")
        self.geometry("850x500")

        # Dataset selection
        tk.Label(self, text="Choose dataset:").pack(anchor="w", padx=10, pady=5)
        self.dataset_var = tk.StringVar()
        datasets = ["Eyes Dataset V1", "Eyes Dataset V2"]
        dataset_cb = ttk.Combobox(self, textvariable=self.dataset_var, values=datasets, state="readonly")
        dataset_cb.current(0)
        dataset_cb.pack(fill="x", padx=10)

        # Multi-model selection (Listbox)
        tk.Label(self, text="Choose models to train (Ctrl+Click for multiple):").pack(anchor="w", padx=10, pady=5)
        self.model_listbox = tk.Listbox(self, selectmode="multiple", height=5, exportselection=False)
        for model in mock_results.keys():
            self.model_listbox.insert(tk.END, model)
        self.model_listbox.pack(fill="x", padx=10, pady=5)

        # Train button
        tk.Button(self, text="Train Selected Models", command=self.train_models).pack(pady=10)

        # Results table (add "Model" column)
        self.tree = ttk.Treeview(
            self,
            columns=("model", "accuracy", "f1", "precision", "recall"),
            show="headings",
            height=7
        )
        for col in ("model", "accuracy", "f1", "precision", "recall"):
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=150 if col == "model" else 120, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Define row colors
        self.tree.tag_configure("best", background="#c8e6c9")   # light green
        self.tree.tag_configure("normal", background="#ffffff") # white

        # Save button
        tk.Button(self, text="Save Selected Model", command=self.save_model).pack(pady=10)

    def train_models(self):
        # Clear old rows
        for row in self.tree.get_children():
            self.tree.delete(row)

        selected_indices = self.model_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("No Selection", "Please select at least one model.")
            return

        # Collect results
        results = []
        for idx in selected_indices:
            model_name = self.model_listbox.get(idx)
            metrics = mock_results[model_name]
            results.append((model_name, metrics))

        # Find best by accuracy
        best_model = max(results, key=lambda x: x[1]["accuracy"])[0]

        # Insert rows with color tags
        for model_name, metrics in results:
            tag = "best" if model_name == best_model else "normal"
            self.tree.insert("", "end", iid=model_name, values=(
                model_name,
                metrics["accuracy"], metrics["f1"], metrics["precision"], metrics["recall"]
            ), tags=(tag,))

        messagebox.showinfo("Training Complete", f"Training finished.\nBest model: {best_model}")

    def save_model(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a model from the results table to save.")
            return
        model_name = self.tree.item(selected_item)["values"][0]  # first column is model name
        messagebox.showinfo("Model Saved", f"✅ Model '{model_name}' has been saved to the database!")

# --- Home Window ---
class HomeApp(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("🏠 Home Dashboard")
        self.geometry("400x250")

        tk.Label(self, text="Welcome to Drowsy Driver System", font=("Arial", 14)).pack(pady=20)

        # Open training dashboard
        tk.Button(self, text="Open Model Training Dashboard", command=self.open_training).pack(pady=20)

        # Logout button
        tk.Button(self, text="Logout", command=self.logout).pack(pady=10)

    def open_training(self):
        TrainerApp(self)

    def logout(self):
        self.destroy()
        self.master.deiconify()  # Show login window again


# --- Login Window ---
class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔑 Login")
        self.root.geometry("300x200")

        tk.Label(root, text="Username").pack(pady=5)
        self.username_entry = tk.Entry(root)
        self.username_entry.pack(pady=5)

        tk.Label(root, text="Password").pack(pady=5)
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(root, text="Login", command=self.check_login).pack(pady=10)

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        # Hardcode for demo
        if username == "admin" and password == "123":
            messagebox.showinfo("Login Success", f"Welcome {username}!")
            self.root.withdraw()   # hide login
            HomeApp(self.root)     # open home
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")


# --- Main Entry ---
if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
