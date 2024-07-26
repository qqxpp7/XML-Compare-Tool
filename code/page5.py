# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 15:01:24 2024

@author: a9037
"""
import os
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
        可以輸入要加入的檔案名稱，有+的按鈕可以加入
        還有執行copy的按鈕
        
        '''
        self.mylabel = tk.Label(self.top_right_frame,  text='1/3    選擇範圍')
        self.mylabel.pack(fill="both",side=tk.LEFT) 
        
        self.choose_button = ctk.CTkButton(self.top_right_frame, text="下一頁", width=200
                                         ,command = self.choose_name_file)
        self.choose_button.pack( pady=5, padx=5)
        '''
        中間區域
        會展示出所選擇/上傳的所有檔案名稱
        
        '''
        
        self.listbox = tk.Listbox(self.middle_right_frame, font=("Helvetica",14))
        self.listbox.pack(fill="both", expand=True)
        
        self.upload_button = ctk.CTkButton(self.middle_right_frame, text="↥上傳", width=80, height=30,
                                   font=("Helvetica", 16), command=lambda: self.upload_files_list())      
        self.upload_button.pack(side=tk.RIGHT, pady=5, padx=5)
        
        self.download_button = ctk.CTkButton(self.middle_right_frame, text="↧下載", width=80, height=30,
                                             font=("Helvetica", 16), command=lambda: self.download_files_list())
        self.download_button.pack(side=tk.RIGHT, pady=5, padx=5)
        
        self.remove_button = ctk.CTkButton(self.middle_right_frame, text="-", width=80, height=30,
                                           font=("Helvetica", 16), command=self.remove_filename)
        self.remove_button.pack(side=tk.RIGHT, pady=5, padx=5)
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
        

    
    def remove_filename(self):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            self.listbox.delete(index)
    
    def download_files_list(self):
        '''
        獲取指定資料夾內的所有檔案名稱（去除副檔名） txt
        '''
        self.before_file_directory = self.find_folders_with_split(sd.before_path.get())
        
        filenames = self.get_filenames_from_directory(self.before_file_directory)

        file_path = os.path.join(sd.report_output_path.get(), 'All_file_name.txt')
        
        
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
        # valid_filenames = [name for name in txt_filenames if name in folder_filenames]
        for name in txt_filenames:
            if name in folder_filenames:
                self.listbox.insert(tk.END, f"{name}\n")
                
        invalid_filenames = [name for name in txt_filenames if name not in folder_filenames]

        if invalid_filenames:
            messagebox.showwarning("Warning", f"{invalid_filenames} 不存在")
    
    def choose_name_file(self):
        print("next")
                
    def open_folder(self):
        '''
        開啟COPY資料夾
        '''
        try:
            if not os.path.exists(sd.after_path.get()):
                self.messagebox.showinfo("錯誤", f"目錄 {self.result_directory} 不存在。")
    
            # 不同操作系統有不同的開啟資料夾方式
            if os.name == 'nt':  # Windows
                os.startfile(sd.after_path.get())
                os.startfile(sd.before_path.get())
            else:
                self.messagebox.showinfo("錯誤", "不支援的操作系統。")
                
        except Exception as e:
            self.messagebox.showinfo("錯誤", f"發生錯誤: {e}")            
                
                