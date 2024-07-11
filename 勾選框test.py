import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import os

attachment_format="xml" # 預設副檔名為 xml

# 創建主窗口
root = ctk.CTk()
root.title("XML Compare Tool")
root.geometry("1000x600")


#建立左邊的功能列框架
left_frame = ctk.CTkFrame(root, width=200)
left_frame.pack(side="left", fill="y", padx=10, pady=10)

#建立右邊的顯示框架
right_frame = ctk.CTkFrame(root)
right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

# 新增搜尋按鈕
def search_action():
    messagebox.showinfo("Search", "Search functionality is not yet implemented.")

search_button = ctk.CTkButton(left_frame, text="Search", command=search_action, width=180, fg_color="white", text_color="black")
search_button.pack(pady=10, anchor="center")

# 新增分割線
line1 = ctk.CTkFrame(left_frame, height=2, fg_color="lightgray")
line1.pack(fill="x", pady=5)

# 功能分類及功能列表
categories = {
    "主功能": ["01 位置設定", "02 XML 拆分", "03 找出差異", "04 比對"],
    "其他功能": ["Copy 資料", "Element 分割"]
}

selected_function = tk.StringVar(value="01 位置設定")

def on_function_button_click(function):
    selected_function.set(function)
    for widget in left_frame.winfo_children():
        if isinstance(widget, ctk.CTkButton) and widget.cget("text") in categories["主功能"] + categories["其他功能"]:
            widget.configure(fg_color="white", text_color="black")
    function_buttons[function].configure(fg_color="lightblue", text_color="black")

function_buttons = {}
for category, functions in categories.items():
    label = ctk.CTkLabel(left_frame, text=category, font=("Arial", 12, "bold"))
    label.pack(pady=5, anchor="center")
    for function in functions:
        button = ctk.CTkButton(left_frame, text=function, width=180, anchor="center", fg_color="white", text_color="black",
                               command=lambda f=function: on_function_button_click(f))
        button.pack(pady=5, anchor="center")
        function_buttons[function] = button
    if category == "主功能":
        line2 = ctk.CTkFrame(left_frame, height=2, fg_color="lightgray")
        line2.pack(fill="x", pady=5)

# 位置設定部分
position_frame = ctk.CTkFrame(right_frame)
position_frame.pack(pady=20, padx=20, fill="both", expand=True)

path_before_label = ctk.CTkLabel(position_frame, text="Before 資料夾 :", anchor="w")
path_before_label.grid(row=0, column=0, pady=20, padx=20, sticky="w")
path_before_entry = ctk.CTkEntry(position_frame, width=400)
path_before_entry.grid(row=0, column=1, pady=5, padx=5)

path_after_label = ctk.CTkLabel(position_frame, text="After 資料夾 :", anchor="w")
path_after_label.grid(row=1, column=0, pady=20, padx=20, sticky="w")
path_after_entry = ctk.CTkEntry(position_frame, width=400)
path_after_entry.grid(row=1, column=1, pady=5, padx=5)

report_output_label = ctk.CTkLabel(position_frame, text="報告產出資料夾 :", anchor="w")
report_output_label.grid(row=2, column=0, pady=20, padx=20, sticky="w")
report_output_entry = ctk.CTkEntry(position_frame, width=400)
report_output_entry.grid(row=2, column=1, pady=5, padx=5)

attachment_format_label = ctk.CTkLabel(position_frame, text="加副檔名：", anchor="w")
attachment_format_label.grid(row=5, column=0, pady=20, padx=20, sticky="w")
attachment_format_entry = ctk.CTkEntry(position_frame, width=200)
attachment_format_entry.grid(row=5, column=1, pady=5, padx=5, sticky="w")

            
# 灰色按鈕的邏輯
def toggle_button(button, variable):
    if variable.get() == 0:
        button.configure(fg_color="grey")
    else:
        button.configure(fg_color="blue")

before_button_var = tk.IntVar(value=1) # 預設為藍色
after_button_var = tk.IntVar(value=1)  # 預設為藍色

def on_before_button_click():
    before_button_var.set(1 if before_button_var.get() == 0 else 0)
    toggle_button(add_extension_before_button, before_button_var)

def on_after_button_click():
    after_button_var.set(1 if after_button_var.get() == 0 else 0)
    toggle_button(add_extension_after_button, after_button_var)

add_extension_before_button = ctk.CTkButton(position_frame, text="Before", command=on_before_button_click, width=100, fg_color="grey")
add_extension_before_button.grid(row=6, column=1, pady=10, padx=10, sticky="w")

add_extension_after_button = ctk.CTkButton(position_frame, text="After", command=on_after_button_click, width=100, fg_color="grey")
add_extension_after_button.grid(row=6, column=1, pady=10, padx=10)

# 新增儲存按鈕
def save_path():
    global before_path, after_path, report_output_path
    before_path = path_before_entry.get()
    after_path = path_after_entry.get()
    report_output_path = report_output_entry.get()
    messagebox.showinfo("信息", "路徑已保存")

ok_button = ctk.CTkButton(right_frame, text="儲存", command=save_path, width=100)
ok_button.place(relx=1.0, rely=0.0, anchor="ne", x=-30, y=250)


# 新增確定按鈕
def execute():
    global before_path, after_path, report_output_path, attachment_format
    attachment_format = attachment_format_entry.get()
    
    if before_button_var.get() == 1:
        add_extension_to_files(before_path, attachment_format)
    if after_button_var.get() == 1:
        add_extension_to_files(after_path, attachment_format)
        
    messagebox.showinfo("信息", "文件名已修改")
    
ok_button = ctk.CTkButton(right_frame, text="執行", command=execute, width=100)
ok_button.place(relx=1.0, rely=0.0, anchor="ne", x=-30, y=450)

def add_extension_to_files(folder_path, extension):
    if not folder_path or not extension:
        return
    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            base, ext = os.path.splitext(filename)
            new_filename = f"{base}.{extension}"
            new_file_path = os.path.join(folder_path, new_filename)
            os.rename(file_path, new_file_path)

# 啟動主循環
root.mainloop()
