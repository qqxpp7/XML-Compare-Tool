import tkinter as tk
import json
import os

# 全域變數的宣告
before_path = None
after_path = None
report_output_path = None

def init_shared_vars():
    global before_path, after_path, report_output_path 
    before_path = tk.StringVar()
    after_path = tk.StringVar()
    report_output_path = tk.StringVar()

    load_vars_from_file() # 初始化時從檔案加載變數
    

def save_vars_to_file():
    '''
    會在page2儲存路徑時呼叫，並且將路徑存到json資料下
    w：寫入模式，如果檔案已經存在，它會被覆蓋；如果檔案不存在，會創建一個新的檔案。
    json.dump 會把 data 寫入json檔案
    '''
    data = {
        "before_path": before_path.get(),
        "after_path": after_path.get(),
        "report_output_path": report_output_path.get()
    }
    with open('shared_data.json', 'w') as file:
        json.dump(data, file)


def load_vars_from_file():
    '''
    會在一開始呼叫json檔案讀取之前存的路徑，並自動存到全域參數中
    '''
    if os.path.exists('shared_data.json'):
        with open('shared_data.json', 'r') as file:
            data = json.load(file)
            before_path.set(data.get("before_path", ""))
            after_path.set(data.get("after_path", ""))
            report_output_path.set(data.get("report_output_path", ""))

