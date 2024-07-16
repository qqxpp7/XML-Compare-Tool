import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, messagebox
import os

class XMLCompareTool:
    def __init__(self, root):
        self.root = root
        self.root.title("XML Compare Tool")
        self.root.geometry("1000x600")

        self.selected_function = tk.StringVar(value="01 位置設定")
        self.function_buttons = {}

        self.create_left_frame()
        self.create_right_frames()
        self.create_function_buttons()

    def create_left_frame(self):
        self.left_frame = ctk.CTkFrame(self.root, width=200)
        self.left_frame.pack(side="left", fill="y", padx=10, pady=10)

    def create_right_frames(self):
        self.frames = {}
        self.frames["Search"] = Search(self.root)
        self.frames["PositionSettingPage"] = PositionSettingPage(self.root)
        self.frames["XMLSplitPage"] = XMLSplitPage(self.root)
        self.frames["FindDifferencesPage"] = FindDifferencesPage(self.root)
        self.frames["ComparisonPage"] = ComparisonPage(self.root)
        self.frames["CopyDataPage"] = CopyDataPage(self.root)
        self.frames["ElementSplitPage"] = ElementSplitPage(self.root)

        for frame in self.frames.values():
            frame.pack_forget()

        self.frames["PositionSettingPage"].pack(fill="both", expand=True)

    def create_function_buttons(self):
        categories = {
            "": ["搜尋"],
            "主功能": ["01 位置設定", "02 XML 拆分", "03 找出差異", "04 比對"],
            "其他功能": ["Copy 資料", "Element 分割"]
        }

        for category, functions in categories.items():
            if category:
                label = ctk.CTkLabel(self.left_frame, text=category, font=("Arial", 12, "bold"))
                label.pack(pady=5, anchor="center")
            for function in functions:
                button = ctk.CTkButton(self.left_frame, text=function, width=180, anchor="center", fg_color="white", text_color="black",
                                       command=lambda f=function: self.on_function_button_click(f))
                button.pack(pady=5, anchor="center")
                self.function_buttons[function] = button
            if category in ["", "主功能"]:
                line = ctk.CTkFrame(self.left_frame, height=2, fg_color="lightgray")
                line.pack(fill="x", pady=5)

        self.function_buttons["01 位置設定"].configure(fg_color="lightblue", text_color="black")

    def on_function_button_click(self, function):
        self.selected_function.set(function)
        for widget in self.left_frame.winfo_children():
            if isinstance(widget, ctk.CTkButton) and widget.cget("text") in list(self.function_buttons.keys()):
                widget.configure(fg_color="white", text_color="black")
        self.function_buttons[function].configure(fg_color="lightblue", text_color="black")

        for frame in self.frames.values():
            frame.pack_forget()
        self.frames[self.get_frame_key(function)].pack(fill="both", expand=True)

    def get_frame_key(self, function):
        mapping = {
            "搜尋":"Search",
            "01 位置設定": "PositionSettingPage",
            "02 XML 拆分": "XMLSplitPage",
            "03 找出差異": "FindDifferencesPage",
            "04 比對": "ComparisonPage",
            "Copy 資料": "CopyDataPage",
            "Element 分割": "ElementSplitPage"
        }
        return mapping.get(function, "PositionSettingPage")
    
class Search(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        label = ctk.CTkLabel(self, text="搜尋頁面")
        
        label.pack(padx=10, pady=10)
        
class PositionSettingPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        self.top_right_frame = ctk.CTkFrame(self)
        self.top_right_frame.pack(pady=10, padx=10, fill="x")

        self.bottom_right_frame = ctk.CTkFrame(self)
        self.bottom_right_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.path_before_entry = self.create_path_selector(self.top_right_frame, 0, "Before 資料夾:", 400, "Browse", self.select_folder)
        self.path_after_entry = self.create_path_selector(self.top_right_frame, 1, "After 資料夾:", 400, "Browse", self.select_folder)
        self.report_output_entry = self.create_path_selector(self.top_right_frame, 2, "報告產出資料夾：", 400, "Browse", self.select_folder)
        
        save_button = ctk.CTkButton(self.top_right_frame, text="儲存", command=self.save_path, width=100)
        save_button.grid(row=3, column=2, columnspan=3, pady=20, padx=20)

        self.attachment_format_entry = self.default_input(self.bottom_right_frame, 0, "加副檔名：", 400, "xml")
        
        self.before_button_var = tk.IntVar(value=1)
        self.after_button_var = tk.IntVar(value=1)

        self.add_extension_before_button = self.create_toggle_button(self.bottom_right_frame, "Before", 1, 0, 
            lambda: self.on_button_click(self.before_button_var, self.add_extension_before_button))

        self.add_extension_after_button = self.create_toggle_button(self.bottom_right_frame, "After", 1, 1, 
            lambda: self.on_button_click(self.after_button_var, self.add_extension_after_button))
        
        ok_button = ctk.CTkButton(self.bottom_right_frame, text="修改", command=self.execute, width=100)
        ok_button.grid(row=2, column=4, columnspan=2, pady=10, padx=10)

    def create_path_selector(self, frame, row, label_text, entry_width, button_text, command):
        label = ctk.CTkLabel(frame, text=label_text, anchor="w")
        label.grid(row=row, column=0, pady=20, padx=20, sticky="w")
        entry = ctk.CTkEntry(frame, width=entry_width)
        entry.grid(row=row, column=1)
        button = ctk.CTkButton(frame, text=button_text, command=lambda: command(entry))
        button.grid(row=row, column=2)
        return entry

    def select_folder(self, entry):
        folder_path = filedialog.askdirectory()
        if folder_path:
            entry.delete(0, tk.END)
            entry.insert(0, folder_path)

    def save_path(self):
        self.before_path = self.path_before_entry.get()
        self.after_path = self.path_after_entry.get()
        self.report_output_path = self.report_output_entry.get()
        messagebox.showinfo("信息", "路徑已保存")

    def default_input(self, frame, row, label_text, entry_width, default_text):
        label = ctk.CTkLabel(frame, text=label_text, anchor="w")
        label.grid(row=row, column=0, pady=20, padx=20, sticky="w")
        entry = ctk.CTkEntry(frame, width=entry_width)
        entry.grid(row=row, column=1, sticky="w")
        entry.insert(0, default_text)
        return entry

    def toggle_button(self, button, var):
        if var.get() == 1:
            button.configure(fg_color="blue")
        else:
            button.configure(fg_color="gray")

    def on_button_click(self, button_var, button):
        button_var.set(1 if button_var.get() == 0 else 0)
        self.toggle_button(button, button_var)

    def create_toggle_button(self, frame, text, row, column, command):
        button = ctk.CTkButton(frame, text=text, command=command, width=100, fg_color="blue")
        button.grid(row=row, column=column, pady=30, padx=30, sticky="w")
        return button

    def add_extension_to_files(self, folder_path, extension):
        if not folder_path or not extension:
            return
        
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                base, ext = os.path.splitext(filename)
                new_filename = f"{base}.{extension}"
                new_file_path = os.path.join(folder_path, new_filename)
                os.rename(file_path, new_file_path)

    def execute(self):
        self.attachment_format = self.attachment_format_entry.get()
        
        if self.before_button_var.get() == 1:
            self.add_extension_to_files(self.before_path, self.attachment_format)
        if self.after_button_var.get() == 1:
            self.add_extension_to_files(self.after_path, self.attachment_format)       
        messagebox.showinfo("信息", "文件名已修改")

class XMLSplitPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        label = ctk.CTkLabel(self, text="XML 拆分功能頁面")
        label.pack(padx=10, pady=10)

class FindDifferencesPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        label = ctk.CTkLabel(self, text="找出差異功能頁面")
        label.pack(padx=10, pady=10)

class ComparisonPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        label = ctk.CTkLabel(self, text="比對功能頁面")
        label.pack(padx=10, pady=10)

class CopyDataPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        label = ctk.CTkLabel(self, text="Copy 資料功能頁面")
        label.pack(padx=10, pady=10)

class ElementSplitPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        label = ctk.CTkLabel(self, text="Element 分割功能頁面")
        label.pack(padx=10, pady=10)

if __name__ == "__main__":
    root = ctk.CTk()
    app = XMLCompareTool(root)
    root.mainloop()
