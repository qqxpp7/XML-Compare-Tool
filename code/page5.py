# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 15:01:24 2024

@author: a9037
"""
import os
import re
import random
import tkinter as tk
import shared_data as sd
import customtkinter as ctk
from tkinter import  filedialog, messagebox


class ComparisonPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        '''
        右邊畫面分為上、中、下三個區域
        ''' 
        self.top_right_frame = ctk.CTkFrame(self)
        self.top_right_frame.pack(pady=5, padx=10, fill="x")

        self.middle_right_frame = ctk.CTkFrame(self)
        self.middle_right_frame.pack(pady=5, padx=10, fill="both", expand=True)
        
        self.bottom_right_frame = ctk.CTkFrame(self)
        self.bottom_right_frame.pack(pady=5, padx=10, fill="x")
        
        '''
        上面區域

        
        '''
        self.mylabel = ctk.CTkLabel(self.top_right_frame,  text='1/2    選擇範圍', font=("Helvetica", 16), corner_radius	= 10)
        self.mylabel.pack(fill="both",side=tk.LEFT) 
        
        self.choose_button = ctk.CTkButton(self.top_right_frame, text="下一頁", width=200
                                         ,command = self.choose_name_file)
        self.choose_button.pack(side=tk.RIGHT, pady=1, padx=1)
        '''
        中間區域
        會展示出所選擇/上傳的所有檔案名稱
        
        '''
        self.buttons_frame = ctk.CTkFrame(self.middle_right_frame, bg_color=self.middle_right_frame.cget("bg_color"))
        self.buttons_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.line_numbers = tk.Listbox(self.middle_right_frame, width=4, font=("Helvetica", 14))
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        
        self.listbox = tk.Listbox(self.middle_right_frame, font=("Helvetica", 14))
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.scrollbar = tk.Scrollbar(self.middle_right_frame, orient=tk.VERTICAL, command=self._scroll_both)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.line_numbers.config(yscrollcommand=self._sync_scroll)
        self.listbox.config(yscrollcommand=self._sync_scroll)
        self.scrollbar.config(command=self._scroll_both)
        
        self.listbox.bind('<KeyRelease>', self.update_line_numbers)
        self.listbox.bind('<MouseWheel>', self.update_line_numbers)
        self.listbox.bind('<ButtonRelease-1>', self.update_line_numbers)
 
        self.upload_button = ctk.CTkButton(self.buttons_frame, text="↥上傳", width=80, height=30,
                                           font=("Helvetica", 14), command=self.upload_files_list)
        self.upload_button.pack(side=tk.RIGHT, padx=5)

        self.download_button = ctk.CTkButton(self.buttons_frame, text="↧下載", width=80, height=30,
                                             font=("Helvetica", 14), command=self.download_files_list)
        self.download_button.pack(side=tk.RIGHT, padx=5)

        self.remove_button = ctk.CTkButton(self.buttons_frame, text="-", width=80, height=30,
                                           font=("Helvetica", 16), command=self.remove_filename)
        self.remove_button.pack(side=tk.RIGHT, padx=5)
        '''
        下面區域
        清空舊資料的選擇
        開啟COPY資料夾的按鈕
        
        '''
        self.sequence_label = ctk.CTkLabel(self.bottom_right_frame, text="全選：")
        self.sequence_label.grid(row=0, column=0, pady=10, padx=20, sticky="w")

        self.sequence_var = tk.StringVar(value=" 否 ")
        self.sequence_options = ctk.CTkSegmentedButton(master=self.bottom_right_frame,
                                                       values=[" 是 ", " 否 "], variable=self.sequence_var)
        self.sequence_options.grid(row=0, column=1, pady=10, padx=10, sticky="w")

        self.open_folder_button = ctk.CTkButton(self.bottom_right_frame, text="開啟Before、After資料夾", 
                                                command=self.open_folder, width=200, fg_color="#CD5C5C")
        self.open_folder_button.grid(row=1, column=0, columnspan=2, pady=10, padx=10)
    
    def _sync_scroll(self, *args):
        self.line_numbers.yview_moveto(args[0])
        self.listbox.yview_moveto(args[0])

    def _scroll_both(self, *args):
        self.line_numbers.yview(*args)
        self.listbox.yview(*args)
        
    def update_line_numbers(self, event=None):
        '''
        更新數量列，並且寬度會隨著數量調整
        '''
        self.line_numbers.delete(0, tk.END)
        line_count = self.listbox.size()
        max_digits = len(str(line_count))
        self.line_numbers.config(width=max_digits + 1)
        for i in range(1, self.listbox.size() + 1):
            self.line_numbers.insert(tk.END, str(i))      
    
    def remove_filename(self):
        '''
        刪除在listbox選中的檔名
        並呼叫更新數列的函式
        '''
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            self.listbox.delete(index)
            self.update_line_numbers()
            
    def find_folders_with_split(self, root_dir):
        '''
        找到資料夾下的split資料夾，如果沒找到就返回原本資料夾
        os.walk會返回三個值
        dirpath：當前遍歷到的目錄路徑
        dirnames：當前目錄下的所有目錄名稱列表
        filenames：當前目錄下的所有檔案名稱列表
        '''
        self.split_folders = []
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for dirname in dirnames:
                if 'split' in dirname:
                    self.split_folders.append(os.path.join(dirpath, dirname))
                    
        if self.split_folders:
            return self.split_folders[0]
        
        return root_dir 
    
    def get_filenames_from_directory(self, directory)->list:
        '''
        獲取指定資料夾內的所有檔案名稱（去除副檔名）
        '''
        filenames = [os.path.splitext(f)[0] for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        return filenames 
    
    
    def download_files_list(self):
        '''
        獲取before資料夾內的所有檔案名稱（去除副檔名） txt
        最後會自動開啟txt
        '''
        self.before_file_directory = self.find_folders_with_split(sd.before_path.get())
        
        filenames = self.get_filenames_from_directory(self.before_file_directory)

        file_path = os.path.join(sd.report_output_path.get(), 'Compare_file_name.txt')
        
        
        with open(file_path, 'w') as file:
            for name in filenames:
                file.write(name + '\n')
        os.startfile(file_path)
    
    def upload_files_list(self):
        '''
        讀取 txt 文件, 比對合法和不合法的檔案名稱
        directory是before_split
        txt_file_path 是可以選取資料夾內的txt檔案
        valid_filenames會呈現在text_area
        invalid_filenames會跳出messagebox警告
        '''
        self.before_file_directory = self.find_folders_with_split(sd.before_path.get())
        
        txt_file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if not txt_file_path:
            messagebox.showwarning("Warning", "未選取任何檔案")
            return
        
        folder_filenames = self.get_filenames_from_directory(self.before_file_directory)
        
        with open(txt_file_path, 'r') as file:
            txt_filenames = [line.strip() for line in file.readlines()]
            
        self.listbox.delete(0, tk.END)
        
        invalid_filenames = [name for name in txt_filenames if name not in folder_filenames]
        valid_filenames = [name for name in txt_filenames if name in folder_filenames]
        
        for filename in valid_filenames:
            self.listbox.insert(tk.END, filename)
            self.update_line_numbers()
            
        if invalid_filenames:
            messagebox.showwarning("Warning", f"{invalid_filenames} 不存在")
            
    def process_listbox_content(self, listbox):
        '''
        使用正則表達式去除listbox字串前面的數字順序和後面的換行符號
        '''
        raw_content = listbox.get(0, tk.END)
        processed_content = []
    
        for item in raw_content:
            
            clean_item = re.sub(r'^\d+\.\s*', '', item).strip()
            processed_content.append(clean_item)
    
        return processed_content

    def choose_name_file(self):
        
        if self.sequence_var.get() == " 否 " and self.listbox.size() > 0:
            self.choose_file = self.process_listbox_content(self.listbox)
            sd.choose_file = self.choose_file
            if len(sd.choose_file) <= 5:
                sd.choose_5_files = sd.choose_file
            else:
                sd.choose_5_files = random.sample(sd.choose_file, 5)
            print(sd.choose_file)
            print(sd.choose_5_files)
            
        else:
            self.before_file_directory = self.find_folders_with_split(sd.before_path.get())
            self.choose_file = self.get_filenames_from_directory(self.before_file_directory)
            sd.choose_file = self.choose_file
            if len(sd.choose_file) <= 5:
                sd.choose_5_files = sd.choose_file
            else:
                sd.choose_5_files = random.sample(sd.choose_file, 5)
            print(sd.choose_file)
            print(sd.choose_5_files)
            
        self.controller.switch_to_page5_2()
        # self.controller.show_frame("ComparisonPage_2")
       
                
    def open_folder(self):
        '''
        開啟before及after split的資料夾
        '''
        try:
            if not os.path.exists(sd.after_path.get()):
                self.messagebox.showinfo("錯誤", f"目錄 {self.result_directory} 不存在。")
    
            # 不同操作系統有不同的開啟資料夾方式
            if os.name == 'nt':  # Windows
                os.startfile(self.find_folders_with_split(sd.after_path.get()))
                os.startfile(self.find_folders_with_split(sd.before_path.get()))
            else:
                self.messagebox.showinfo("錯誤", "不支援的操作系統。")
                
        except Exception as e:
            self.messagebox.showinfo("錯誤", f"發生錯誤: {e}")            
                
                