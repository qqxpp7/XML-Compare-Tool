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
from tkinter import ttk, messagebox, scrolledtext

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
        
        self.add_button = ctk.CTkButton(self.top_right_frame, text="+", width=100, height=30, command=self.is_filename_in_directory)
        self.add_button.grid(row=0, column=1, sticky="w")
         
        self.copy_button = ctk.CTkButton(self.top_right_frame, text="COPY", width=200, command = self.copy_name_file)
        self.copy_button.grid(row=0, column=2, pady=10, padx=10, sticky="w")
        '''
        中間區域
        會展示出所選擇/上傳的所有檔案名稱
        
        '''
        self.text_area = scrolledtext.ScrolledText(self.middle_right_frame, wrap=tk.NONE, font=("Helvetica",14))
        self.text_area.pack(fill="both", expand=True)
        
        self.upload_button = ctk.CTkButton(self.middle_right_frame, text="↥", width=80, height=30, command=self.upload_files_list)
        self.upload_button.pack(side=tk.RIGHT, pady=5, padx=5)
        
        self.download_button = ctk.CTkButton(self.middle_right_frame, text="↧", width=80, height=30, command=self.download_files_list)
        self.download_button.pack(side=tk.RIGHT, pady=5, padx=5)
        
        self.remove_button = ctk.CTkButton(self.middle_right_frame, text="-", width=80, height=30, command=self.clear_directory)
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

        open_copy_folder_button = ctk.CTkButton(self.bottom_right_frame, text="開啟COPY資料夾", command=self.open_copy_folder,
                                                width=200, fg_color="#CD5C5C")
        open_copy_folder_button.grid(row=1, column=0, columnspan=2, pady=10, padx=10)

    def copy_name_file(self):
        self.before_file_directory = sd.before_path.get()
        self.after_file_directory = sd.after_path.get()
        self.result_directory = os.path.join(sd.result_path.get(), 'copy')
    
        self.file_name_report = os.path.join(sd.result_path.get(), 'filename_list.txt')
    
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
    
        os.startfile(result_directory)
    
    
    def copy_and_rename(self, file_name, source_directory, suffix, result_directory):
        '''
        主功能二： Copy file from source directory to target directory and rename it
        '''
        if not os.path.exists(result_directory):
            os.makedirs(result_directory)
    
        shutil.copy(os.path.join(source_directory, file_name), result_directory)
        os.rename(
            os.path.join(result_directory, file_name),
            os.path.join(result_directory, file_name.replace('.xml', suffix))
        )
    
    def get_filenames_from_directory(self, directory)->list:
        '''
        獲取指定資料夾內的所有檔案名稱（去除副檔名）
        '''
        filenames = [os.path.splitext(f)[0] for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        return filenames
    
    
    
    def download_files_list(self, directory, output_file):
        '''
        獲取指定資料夾內的所有檔案名稱（去除副檔名） txt
        '''
        filenames = self.get_filenames_from_directory(directory)
        
        with open(output_file, 'w') as file:
            for name in filenames:
                file.write(name + '\n')
    
    def upload_files_list(self, directory, txt_file_path)-> (list, list):
        '''
        讀取 txt 文件, 比對合法和不合法的檔案名稱
        '''
        folder_filenames = self.get_filenames_from_directory(directory)
    
        with open(txt_file_path, 'r') as file:
            txt_filenames = [line.strip() for line in file.readlines()]
        
        valid_filenames = [name for name in txt_filenames if name in folder_filenames]
        invalid_filenames = [name for name in txt_filenames if name not in folder_filenames]
        
        return valid_filenames, invalid_filenames
    
    
    def is_filename_in_directory(self, directory, filename)-> bool:
        '''
        檢查檔案名稱是否存在於資料夾中
        '''
        folder_filenames = self.get_filenames_from_directory(directory)
        return filename in folder_filenames
    
    
    
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
            if not os.path.exists(self.copy_new_folder):
                self.messagebox.showinfo("錯誤", f"目錄 {self.move_new_folder} 不存在。")
    
            # 不同操作系統有不同的開啟資料夾方式
            if os.name == 'nt':  # Windows
                os.startfile(self.copy_new_folder)
            else:
                self.messagebox.showinfo("錯誤", "不支援的操作系統。")
                
        except Exception as e:
            self.messagebox.showinfo("錯誤", f"發生錯誤: {e}")
    
            '''
    if __name__ == "__main__":
        before_file_directory = sd.before_path.get()
        after_file_directory = sd.after_path.get()
        result_directory = os.path.join(sd.result_path.get(), 'copy')
    
        file_name_report = os.path.join(sd.result_path.get(), 'filename_list.txt')
    
        # 頁面(最後再處理)
    
        # 下載全部 file_name.txt
        download_files_list(before_file_directory, file_name_report)
    
        # 上傳對應資料 filename.txt
        directory = os.path.expanduser('~/Desktop')
        txt_file_path = os.path.expanduser('~/Desktop/filename.txt')
        valid_filenames, invalid_filenames = upload_files_list(directory, txt_file_path)
    
        # 檢查單一名稱
        file_name = '123'
        if is_filename_in_directory(directory, '123'):
            print('true')
        else:
            print('false')
    
    
        print(f"合法檔案名稱: {valid_filenames}")
        print(f"不合法檔案名稱: {invalid_filenames}")
    
        clear_directory(before_file_directory)
    
        copy_and_rename_files(before_file_directory, after_file_directory, result_directory, input_file_list )
        '''

