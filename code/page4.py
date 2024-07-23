# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 15:00:48 2024

@author: a9037
"""
import os
import time
import tkinter as tk
import customtkinter as ctk
from datetime import datetime
import shared_data as sd


class FindDifferencesPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()
        
        self.MOVE_FILE_BOOLEAN = False


    def create_widgets(self):
        
        self.sequence_label = ctk.CTkLabel(self, text="移動差異檔案：")
        self.sequence_label.grid(row=2, column=0, pady=10, padx=20, sticky="w")       
        self.sequence_var = tk.StringVar(value=" 否 ")
        self.sequence_options = ctk.CTkSegmentedButton(master=self,
             values=[" 是 ", " 否 "], variable=self.sequence_var)        
        self.sequence_options.grid(row=2, column=1, pady=10, padx=10, sticky="w")
        
        self.report_name_entry = self.default_input(self, 1,"報告書名稱：", 400, "Different_Report")
        
        execute_button = ctk.CTkButton(self, text="執行", command=self.execute, width=200)
        execute_button.grid(row=3, column=0, pady=10, padx=10)
        
        open_report_button = ctk.CTkButton(self, text="開啟檔案", command=self.open_report, 
                                           width=200, fg_color="#CD5C5C")
        open_report_button.grid(row=4, column=0, pady=10, padx=10)
    
        
    def default_input(self, frame, row, label_text, entry_width, default_text):
        '''
        有預設輸入值的標籤與輸入框
        '''
        label = ctk.CTkLabel(frame, text=label_text, anchor="w")
        label.grid(row=row, column=0, pady=20, padx=20, sticky="w")
        entry = ctk.CTkEntry(frame, width=entry_width)
        entry.grid(row=row, column=1, sticky="w")
        entry.insert(0, default_text)
        return entry  
    
    
    def find_folders_with_split(self, root_dir):
        '''
        找到資料夾下的split資料夾
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
        return self.split_folders[0]

    def move_file(self, file_name, source_directory, target_directory):
           """
           移動檔案從來源目錄到目標目錄
           """
           source_file = os.path.join(source_directory, file_name)
           target_file = os.path.join(target_directory, file_name)
           os.rename(source_file, target_file)  
               
    def open_report(self):
        '''
        開啟差異檔案移動到的資料夾
        '''
        try:
            if not os.path.exists(self.move_new_folder):
                self.messagebox.showinfo("錯誤", f"目錄 {self.move_new_folder} 不存在。")
    
            # 不同操作系統有不同的開啟資料夾方式
            if os.name == 'nt':  # Windows
                os.startfile(self.move_new_folder)
            else:
                self.messagebox.showinfo("錯誤", "不支援的操作系統。")
                
        except Exception as e:
            self.messagebox.showinfo("錯誤", f"發生錯誤: {e}")
        
    def execute(self):
        '''
        在報表輸出資料夾下面創立一個different_file資料夾
        會在底下生成差異分析的報表(txt)
        
        透過find_folders_with_split函式找到shared_data before跟after底下的split資料夾
        
        '''
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        different_new_folder = os.path.join(sd.report_output_path.get(), "different_file")
        os.makedirs(different_new_folder, exist_ok=True)
        report_name = self.report_name_entry.get() + "_" + current_time + '.txt'
        file_path = os.path.join(different_new_folder, report_name)  
        
        # 判斷 after directory 有，before directory 沒有的檔案
        self.before_file_names = os.listdir(self.find_folders_with_split(sd.before_path.get()))
        self.after_file_names = os.listdir(self.find_folders_with_split(sd.after_path.get()))
     
        for file in self.before_file_names:
            if file in self.after_file_names:
                self.after_file_names.remove(file)
        
        # 判斷 before directory 有，after directory 沒有的檔案
        self.before_file_names_2 = os.listdir(self.find_folders_with_split(sd.before_path.get()))
        self.after_file_names_2 = os.listdir(self.find_folders_with_split(sd.after_path.get()))


        for file in self.after_file_names_2:
            if file in self.before_file_names_2:
                self.before_file_names_2.remove(file)
        
        if self.sequence_var.get() == " 否 ":
            self.print_file(self.report_name_entry.get(), file_path)
            
        else:
            self.move = different_new_folder
            self.print_file(self.report_name_entry.get(), file_path, self.move)
            
            self.move_new_folder = os.path.join(sd.report_output_path.get(), "move_file")
            os.makedirs(self.move_new_folder, exist_ok=True)
            
            for file in self.before_file_names_2:
                self.move_file(file, self.find_folders_with_split(sd.before_path.get()), self.move_new_folder)
            for file in self.after_file_names:
                self.move_file(file, self.find_folders_with_split(sd.after_path.get()), self.move_new_folder)

        
    def print_file(self, file_name, file_path, move="無" ) :
        TIME_START = time.time()
        TIME_END = time.time()
        
        with open(file_path, 'a') as file:
                                
            file.write("------------------------Header ---------------------\n")
            file.write(f"執行時間     :{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write(f"花費時間     :{TIME_START-TIME_END} 秒\n")                    
            file.write("執行檔案     :before_split、after_split\n")                    
            file.write(f"輸出檔案     :{move}\n")                    
            file.write("--------------------Input Parameter ---------------------\n")           
            file.write(f"移動差異檔案  :{self.sequence_var.get()}\n")
            file.write(f"Before 數量   :{str(len(self.before_file_names))}\n")
            file.write(f"After 數量    :{str(len(self.after_file_names_2))}\n")
            file.write("--------------------內容 ---------------------\n")
            
            if self.before_file_names_2:
                file.write("before 有, after 沒有的檔案: "+ str(len(self.before_file_names_2)) + "\n")
                for files in self.before_file_names_2:
                    file.write(files + "\n")
            file.write("\n")

            if self.after_file_names:
                file.write("after 有, before 沒有的檔案: "+ str(len(self.after_file_names)) + "\n")
                for files in self.after_file_names:
                    file.write(files + "\n")
                    
            file.write("\n\n")   
            
            if os.name == 'nt':
                
                os.startfile(file_path)
                
