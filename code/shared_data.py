import tkinter as tk

# 這些變數應在主窗口創建後初始化
before_path = None
after_path = None
report_output_path = None

def init_shared_vars():
    global before_path, after_path, report_output_path
    before_path = tk.StringVar()
    after_path = tk.StringVar()
    report_output_path = tk.StringVar()
