# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 15:01:56 2024

@author: a9037
"""
import os
import shutil
import tkinter as tk
import shared_data as sd
import customtkinter as ctk
from tkinter import  filedialog, messagebox

'''


複製檔案到目標資料夾並重新命名

'''

class CopyDataPage(ctk.CTkFrame):
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
        
        self.file_name_entry = ctk.CTkEntry(self.top_right_frame, width=300)
        self.file_name_entry.grid(row=0, column=0, sticky="w")
        
        self.add_button = ctk.CTkButton(self.top_right_frame, text="+", width=100, height=30
                                        ,command=self.add_filename)
        self.add_button.grid(row=0, column=1, sticky="w")
         
        self.copy_button = ctk.CTkButton(self.top_right_frame, text="COPY", width=200
                                         ,command = self.copy_name_file)
        self.copy_button.grid(row=0, column=2, pady=10, padx=10, sticky="w")
        '''
        中間區域
        會展示出所選擇/上傳的所有檔案名稱
        
        '''
        self.mylabel = tk.Label(self.middle_right_frame, bg='#87CEFA', text='選擇要複製的檔案')
        self.mylabel.pack(fill="both",side=tk.TOP) 
        
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
        self.sequence_label = ctk.CTkLabel(self.bottom_right_frame, text="清空舊資料：")
        self.sequence_label.grid(row=0, column=0, pady=10, padx=20, sticky="w")

        self.sequence_var = tk.StringVar(value=" 否 ")
        self.sequence_options = ctk.CTkSegmentedButton(master=self.bottom_right_frame,
                                                       values=[" 是 ", " 否 "], variable=self.sequence_var)
        self.sequence_options.grid(row=0, column=1, pady=10, padx=10, sticky="w")

        self.open_copy_folder_button = ctk.CTkButton(self.bottom_right_frame, text="開啟COPY資料夾", 
                                                command=self.open_copy_folder, width=200, fg_color="#CD5C5C")
        self.open_copy_folder_button.grid(row=1, column=0, columnspan=2, pady=10, padx=10)


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
    

    def copy_name_file(self):
        '''
        點擊copy會開始從BEFORE、AFTER複製想要的檔案到指定路徑
        '''
        
        self.result_directory = os.path.join(sd.report_output_path.get(), 'copy')
        os.makedirs(self.result_directory, exist_ok=True)

        
        self.before_file_directory = self.find_folders_with_split(sd.before_path.get())
        self.after_file_directory = self.find_folders_with_split(sd.after_path.get())
        self.input_file_list = [item.strip()+".xml" for item in self.listbox.get(0, tk.END)]
        
        if self.sequence_var.get() == " 是 ":           
            self.clear_directory(self.result_directory)
            
        self.copy_and_rename_files(self.before_file_directory, self.after_file_directory,
                                   self.result_directory, self.input_file_list )
            
        
    def copy_and_rename_files(self, before_file_directory, after_file_directory, result_directory, file_list):
        '''
        主功能一： loop through file_list
        '''
        for file_name in file_list:
            # Copy 'before' file to target directory and rename it
            self.copy_and_rename(file_name, before_file_directory, '_before.xml', result_directory)
    
            # Copy 'after' file to target directory and rename it
            self.copy_and_rename(file_name, after_file_directory, '_after.xml', result_directory)
    
    
    def copy_and_rename(self, file_name, source_directory, suffix, result_directory):
        '''
        主功能二： Copy file from source directory to target directory and rename it
        '''
        if not os.path.exists(result_directory):
            os.makedirs(result_directory)
            
        try:
            shutil.copy(os.path.join(source_directory, file_name), result_directory)
            os.rename(
                os.path.join(result_directory, file_name),
                os.path.join(result_directory, file_name.replace('.xml', suffix))
            )
        except Exception as e:
            os.remove(os.path.join(result_directory, file_name))
            print("Error", f"An unexpected error occurred: {e}")
    
    def get_filenames_from_directory(self, directory)->list:
        '''
        獲取指定資料夾內的所有檔案名稱（去除副檔名）
        '''
        filenames = [os.path.splitext(f)[0] for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        return filenames 
    
    
    def download_files_list(self):
        '''
        獲取指定資料夾內的所有檔案名稱（去除副檔名） txt
        '''
        self.before_file_directory = self.find_folders_with_split(sd.before_path.get())
        
        filenames = self.get_filenames_from_directory(self.before_file_directory)

        file_path = os.path.join(sd.report_output_path.get(), 'copy_file_name.txt')
        
        
        with open(file_path, 'w') as file:
            for name in filenames:
                file.write(name + '\n')
        os.startfile(file_path)
    
    def update_listbox_numbers(self):
        '''
        在刪除某一列的檔名後
        會刷新全部的順序
        '''
        items = self.listbox.get(0, tk.END)
        self.listbox.delete(0, tk.END)
        for i, item in enumerate(items):
            clean_item = item.split('. ', 1)[1] if '. ' in item else item
            self.listbox.insert(tk.END, f"{i + 1}. {clean_item}")
            
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
        self.index = 1

        for name in txt_filenames:
            if name in folder_filenames:
                self.listbox.insert(tk.END, f"{self.index}. {name}\n")
                self.index += 1
                
        invalid_filenames = [name for name in txt_filenames if name not in folder_filenames]

        if invalid_filenames:
            messagebox.showwarning("Warning", f"{invalid_filenames} 不存在")
    
    def add_filename(self):
        '''
        檢查檔案名稱是否存在於資料夾中
        並檢查是否已經存在下面視窗
        '''
        self.before_file_directory = self.find_folders_with_split(sd.before_path.get())
        
        folder_filenames = self.get_filenames_from_directory(self.before_file_directory)
        
        file_name = self.file_name_entry.get()
        if not file_name:
            messagebox.showerror("Error", "檔案名稱不能為空")
            return
        
        clean_file_name = file_name.split('. ', 1)[1] if '. ' in file_name else file_name

        if clean_file_name in folder_filenames:
            listbox_items = [item.split('. ', 1)[1] if '. ' in item else item for item in self.listbox.get(0, tk.END)]
            if clean_file_name not in listbox_items:
                self.listbox.insert(tk.END, f"{len(listbox_items) + 1}. {clean_file_name}")
                self.update_listbox_numbers()
            else:
                tk.messagebox.showwarning("Warning", "已經有相同的項目")
        else:
            messagebox.showerror("Warning", f"{self.file_name_entry.get()} 不存在")
    
    def remove_filename(self):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            self.listbox.delete(index)
            self.update_listbox_numbers()
        
    def clear_directory(self, directory):
        '''
        確認資料夾存在, 存在 delete folder
        '''
        if os.path.exists(directory):
            # 刪除資料夾中的所有內容
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)  # 刪除文件或符號連結
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)  # 刪除資料夾
                except Exception as e:
                    print(f'刪除 {file_path} 時發生錯誤: {e}')
        else:
            print(f"指定的資料夾 {directory} 不存在")
    
    def open_copy_folder(self):
        '''
        開啟COPY資料夾
        '''
        try:
            if not os.path.exists(self.result_directory):
                self.messagebox.showinfo("錯誤", f"目錄 {self.result_directory} 不存在。")
    
            # 不同操作系統有不同的開啟資料夾方式
            if os.name == 'nt':  # Windows
                os.startfile(self.result_directory)
            else:
                self.messagebox.showinfo("錯誤", "不支援的操作系統。")
                
        except Exception as e:
            self.messagebox.showinfo("錯誤", f"發生錯誤: {e}")



