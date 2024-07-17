import tkinter as tk

before_path = tk.StringVar()
after_path = tk.StringVar()
report_output_path = tk.StringVar()

def init_shared_vars():
    global before_path, after_path, report_output_path
    before_path.set("Before")  # 預設值，可以根據實際情況修改
    after_path.set("After")    # 預設值，可以根據實際情況修改
    report_output_path.set("ReportOutput")  # 預設值，可以根據實際情況修改
