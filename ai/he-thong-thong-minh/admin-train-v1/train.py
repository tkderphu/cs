import tkinter as tk
from tkinter import ttk, messagebox, Toplevel, Checkbutton, IntVar
from PIL import Image, ImageTk
from models import TrainedModel
import threading
import time
import os
import cv2
from dao import SampleDao
from controller import TrainModelController
from dao import TrainedModelDao
AVAILABLE_MODELS = ["CNN", "Random Forest", "Landmark"]

sampleDao = SampleDao()
trainedModelDao = TrainedModelDao()
SAMPLES_DB = sampleDao.get_list_sample()
trainModelController = TrainModelController(sampleDao, trainedModelDao)
def get_eye_from_db(sample):
    """
    Trả về ảnh vùng mắt được cắt theo (x_min, y_min, x_max, y_max) từ DB.
    """
    path = "./images/" + sample.image_file_path
    if not os.path.exists(path):
        return None

    img = cv2.imread(path)
    if img is None:
        return None

    h, w, _ = img.shape
    x_min, y_min, x_max, y_max = (
        max(sample.x_min, 0),
        max(sample.y_min, 0),
        min(sample.x_max, w),
        min(sample.y_max, h),
    )

    cropped = img[y_min:y_max, x_min:x_max]
    if cropped.size == 0:
        return None

    cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)
    return Image.fromarray(cropped)

class TrainModelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Train Model Management")
        self.root.geometry("850x650")

        self.selected_model = tk.StringVar()
        self.selected_samples = []

        self.admin_home_frame = None
        self.train_frame = None

        self.create_admin_home()

    # ===================== ADMIN HOME =====================
    def create_admin_home(self):
        self.clear_frames()

        self.admin_home_frame = ttk.Frame(self.root, padding=30)
        self.admin_home_frame.pack(expand=True, fill="both")

        ttk.Label(
            self.admin_home_frame,
            text="ADMIN HOME",
            font=("Arial", 20, "bold")
        ).pack(pady=30)

        ttk.Button(
            self.admin_home_frame,
            text="Train model",
            command=self.create_train_frame,
            width=25
        ).pack(pady=15)

    # ===================== TRAIN FRAME =====================
    def create_train_frame(self):
        self.clear_frames()
        self.train_frame = ttk.Frame(self.root, padding=20)
        self.train_frame.pack(fill="both", expand=True)

        frame_top = ttk.Frame(self.train_frame, padding=10)
        frame_top.pack(fill="x")

        ttk.Label(frame_top, text="Chọn mô hình:", font=("Arial", 11, "bold")).pack(side="left", padx=5)
        self.model_select = ttk.Combobox(
            frame_top,
            textvariable=self.selected_model,
            values=AVAILABLE_MODELS,
            state="readonly",
            width=25
        )
        self.model_select.pack(side="left", padx=5)
        self.model_select.current(0)

        ttk.Button(frame_top, text="Chọn mẫu", command=self.open_sample_dialog).pack(side="left", padx=5)
        ttk.Button(frame_top, text="Xem mẫu đã chọn", command=self.show_selected_samples).pack(side="left", padx=5)

        # ---- Train button ----
        self.train_btn = ttk.Button(self.train_frame, text="Huấn luyện mô hình", command=self.start_training)
        self.train_btn.pack(pady=15)

        # ---- Kết quả ----
        self.result_frame = ttk.LabelFrame(self.train_frame, text="Kết quả huấn luyện", padding=10)
        self.result_frame.pack(fill="x", padx=10, pady=10)
        self.result_text = tk.StringVar()
        ttk.Label(self.result_frame, textvariable=self.result_text, justify="left").pack(anchor="w")

        # ---- Save model ----
        self.save_btn = ttk.Button(self.train_frame, text="Lưu model", command=self.save_model)
        self.save_btn.pack(pady=10)
        self.save_btn["state"] = "disabled"

        # ---- Back button ----
        ttk.Button(self.train_frame, text="Quay lại Admin Home", command=self.create_admin_home).pack(pady=15)

    # ===================== CLEAR FRAMES =====================
    def clear_frames(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ------------------- Chọn mẫu -------------------
    def open_sample_dialog(self):
        dialog = Toplevel(self.root)
        dialog.title("Chọn các mẫu")
        dialog.geometry("550x450")

        ttk.Label(dialog, text="Chọn các mẫu để huấn luyện:").pack(pady=5)
        frame_all = ttk.Frame(dialog)
        frame_all.pack(fill="x", pady=5)
        select_all_var = IntVar(value=0)
        select_all_chk = Checkbutton(frame_all, text="Chọn tất cả", variable=select_all_var)
        select_all_chk.pack(side="left", padx=10)

        canvas = tk.Canvas(dialog)
        scrollbar = ttk.Scrollbar(dialog, orient="vertical", command=canvas.yview)
        scroll_frame = ttk.Frame(canvas)
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        sample_vars = []

        for s in SAMPLES_DB:
            frame_item = ttk.Frame(scroll_frame, padding=5)
            frame_item.pack(fill="x")

            var = IntVar(value=1 if s in self.selected_samples else 0)
            eye_img = get_eye_from_db(s)
            if eye_img is None:
                eye_img = Image.new("RGB", (80, 80), "gray")
            else:
                eye_img = eye_img.resize((80, 80))

            photo = ImageTk.PhotoImage(eye_img)
            lbl_img = ttk.Label(frame_item, image=photo)
            lbl_img.image = photo
            lbl_img.pack(side="left")

            text = f"{os.path.basename(s.image_file_path)} ({s.label})"
            chk = Checkbutton(frame_item, text=text, variable=var)
            chk.pack(side="left", padx=10)
            sample_vars.append((var, s))

        def toggle_select_all():
            for var, _ in sample_vars:
                var.set(select_all_var.get())

        def confirm_selection():
            self.selected_samples = [s for var, s in sample_vars if var.get() == 1]
            if not self.selected_samples:
                messagebox.showwarning("Cảnh báo", "Bạn chưa chọn mẫu nào!")
                return
            dialog.destroy()
            messagebox.showinfo("Thành công", f"Đã chọn {len(self.selected_samples)} mẫu!")

        select_all_chk.config(command=toggle_select_all)
        ttk.Button(dialog, text="Xác nhận", command=confirm_selection).pack(pady=10)

    # ------------------- Xem mẫu đã chọn -------------------
    def show_selected_samples(self):
        if not self.selected_samples:
            messagebox.showinfo("Thông báo", "Bạn chưa chọn mẫu nào!")
            return

        dialog = Toplevel(self.root)
        dialog.title("Các mẫu đã chọn")
        dialog.geometry("550x400")

        ttk.Label(dialog, text="Các mẫu đã chọn:").pack(pady=5)
        canvas = tk.Canvas(dialog)
        scrollbar = ttk.Scrollbar(dialog, orient="vertical", command=canvas.yview)
        scroll_frame = ttk.Frame(canvas)
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        selected_vars = []

        for s in self.selected_samples:
            frame_item = ttk.Frame(scroll_frame, padding=5)
            frame_item.pack(fill="x")

            eye_img = get_eye_from_db(s)
            if eye_img is None:
                eye_img = Image.new("RGB", (100, 100), "gray")
            else:
                eye_img = eye_img.resize((100, 100))
            photo = ImageTk.PhotoImage(eye_img)
            lbl_img = ttk.Label(frame_item, image=photo)
            lbl_img.image = photo
            lbl_img.pack(side="left")

            var = IntVar(value=0)
            Checkbutton(frame_item, text=f"{os.path.basename(s.image_file_path)}\nLabel: {s.label}", variable=var).pack(side="left", padx=10)
            selected_vars.append((var, s))

        def delete_selected():
            to_delete = [s for var, s in selected_vars if var.get() == 1]
            if not to_delete:
                messagebox.showinfo("Thông báo", "Chưa chọn ảnh nào để xóa!")
                return
            for s in to_delete:
                if s in self.selected_samples:
                    self.selected_samples.remove(s)
            messagebox.showinfo("Thành công", f"Đã xóa {len(to_delete)} ảnh!")
            dialog.destroy()

        ttk.Button(dialog, text="🗑 Xóa ảnh đã chọn", command=delete_selected).pack(pady=5)
        ttk.Button(dialog, text="Đóng", command=dialog.destroy).pack(pady=5)

    # ------------------- Train model -------------------
    def start_training(self):
        if not self.selected_samples:
            messagebox.showwarning("Thiếu dữ liệu", "Bạn cần chọn các mẫu trước khi train!")
            return

        model_name = self.selected_model.get()
        messagebox.showinfo("Huấn luyện", f"Bắt đầu huấn luyện mô hình: {model_name}")
        threading.Thread(target=self.train_model_process, daemon=True).start()

    def train_model_process(self):
        self.train_btn["state"] = "disabled"
        self.result_text.set("Đang huấn luyện...")

        model_name = self.selected_model.get()
        train_model = TrainedModel(
            None,
            model_name,
            None,
            None,
            None,
            None,
            None,
            self.selected_samples
        )
        result = trainModelController.train(train_model)

        self.trained_model = result

        if result is None:
            self.result_text.set("Huấn luyện thất bại — không có mẫu hợp lệ hoặc lỗi trong quá trình xử lý.")
            self.train_btn["state"] = "normal"
            return

        train_count = len(result.training_samples) if result.training_samples else 0
        test_count = max(0, len(self.selected_samples) - train_count)

        self.result_text.set(
            f"Số lượng mẫu dùng cho train: {train_count}\n"
            f"Số mẫu cho test: {test_count}\n"
            f"Accuracy: {result.accuracy:.2f}\n"
            f"F1 score: {result.f1:.2f}\n"
            f"Precision: {result.precision:.2f}\n"
            f"Recall: {result.recall:.2f}"
        )
        self.train_btn["state"] = "normal"
        self.save_btn["state"] = "normal"



    # ------------------- Save model -------------------
    def save_model(self):
        trained_model = self.trained_model
        succecss = trainedModelDao.save(trained_model)
        if succecss:
            messagebox.showinfo("Lưu model", f"Model '{trained_model.name}' đã được lưu thành công!")
        else:
            messagebox.showerror("Có lỗi khi lưu model", f"Model '{trained_model.name}'!")


# ===================== RUN APP ==========================
if __name__ == "__main__":
    root = tk.Tk()
    app = TrainModelApp(root)
    root.mainloop()