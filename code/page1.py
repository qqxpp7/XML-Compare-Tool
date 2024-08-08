# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 14:50:40 2024

@author: a9037
"""
import os
import difflib
import tkinter as tk
import shared_data as sd
import customtkinter as ctk
import xml.etree.ElementTree as ET
from tkinter import filedialog, messagebox

class SearchPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        '''
        右邊畫面分為上、下兩個區域
        ''' 
        self.top_right_frame = ctk.CTkFrame(self)
        self.top_right_frame.pack(pady=5, padx=10, fill="x")

        self.bottom_right_frame = ctk.CTkFrame(self)
        self.bottom_right_frame.pack(pady=5, padx=10, fill="both", expand=True)
        
        '''
        上面區域
        
        '''
        self.choose_button = ctk.CTkButton(self.top_right_frame, text="執行", width=200
                                           , command = lambda: self.load_xml_content())
        self.choose_button.pack(side=tk.RIGHT, pady=5, padx=5)
        
        self.file_path_entry = self.create_path_selector(self.top_right_frame, "查看檔案:", 400, "Browse", self.select_xml)

        
        '''
        中間區域的左邊
        會秀出檔案的Element及Text
        wrap=tk.NONE 禁用自動換行
        
        '''
        self.top_middle_right_frame = ctk.CTkFrame(self.bottom_right_frame, fg_color="transparent")
        self.top_middle_right_frame.pack(pady=5, padx=5, side="top",fill="x")
        
        self.replace_label = ctk.CTkLabel(self.top_middle_right_frame, fg_color='#FFE153', text='Replace',
                                          font=("Helvetica", 14), corner_radius	= 5)
        self.replace_label.pack(padx=2, side=tk.LEFT, fill="both", expand=True) 
        
        self.insert_label = ctk.CTkLabel(self.top_middle_right_frame, fg_color='lightgreen', text='Insert',
                                         font=("Helvetica", 14), corner_radius	= 5)
        self.insert_label.pack(padx=2, side=tk.LEFT, fill="both", expand=True)
        
        self.delete_label = ctk.CTkLabel(self.top_middle_right_frame, fg_color='#fd8082', text='Delete',
                                         font=("Helvetica", 14), corner_radius	= 5)
        self.delete_label.pack(padx=2, side=tk.LEFT, fill="both", expand=True)
        
        self.y_scrollbar = tk.Scrollbar(self.bottom_right_frame, orient=tk.VERTICAL, command=self._scroll_both)
        self.y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.line_numbers = tk.Listbox(self.bottom_right_frame, width=4, font=("Helvetica", 14))
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        self.left_listbox = tk.Listbox(self.bottom_right_frame, font=("Helvetica", 14), yscrollcommand=self._sync_scroll)
        self.left_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.left_x_scrollbar = tk.Scrollbar(self.left_listbox, orient=tk.HORIZONTAL, command=self.left_listbox.xview)
        self.left_x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.left_listbox['xscrollcommand'] = self.left_x_scrollbar.set
        self.left_listbox.bind("<Key>", lambda e: "break")


        self.right_listbox = tk.Listbox(self.bottom_right_frame, font=("Helvetica", 14), yscrollcommand=self._sync_scroll)
        self.right_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.right_x_scrollbar = tk.Scrollbar(self.right_listbox, orient=tk.HORIZONTAL, command=self.right_listbox.xview)
        self.right_x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.right_listbox['xscrollcommand'] = self.right_x_scrollbar.set
        self.right_listbox.bind("<Key>", lambda e: "break")
        
    def create_path_selector(self, frame, label_text, entry_width, button_text, command):
        label = ctk.CTkLabel(frame, text=label_text, anchor="w")
        label.pack(side=tk.LEFT, pady=5, padx=5)
        entry = ctk.CTkEntry(frame, width=entry_width)
        entry.pack(side=tk.LEFT, pady=5, padx=5)
        button = ctk.CTkButton(frame, width=120, text=button_text, command=lambda: command(entry))
        button.pack(side=tk.LEFT, pady=5, padx=5)
        return entry
    
    def select_xml(self, entry):
        '''
        只能選擇xml檔案，並且會將選擇的檔案名稱自動插入到輸入框
        '''
        xml_path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
        if xml_path:
            file_name = xml_path.split("/")[-1].split(".")[0]
            entry.delete(0, tk.END)
            entry.insert(0, file_name)
    
    def _sync_scroll(self, *args):
        self.line_numbers.yview_moveto(args[0])
        self.left_listbox.yview_moveto(args[0])
        self.right_listbox.yview_moveto(args[0])


    def _scroll_both(self, *args):
        self.line_numbers.yview(*args)
        self.left_listbox.yview(*args)
        self.right_listbox.yview(*args)
        
    def update_line_numbers(self, event=None):
        '''
        更新文件內容行數列，並且寬度會隨著數量調整
        '''
        self.line_numbers.delete(0, tk.END)
        line_count = max(self.left_listbox.size(), self.right_listbox.size())
        max_digits = len(str(line_count))
        self.line_numbers.config(width=max_digits + 1)
        for i in range(1, line_count + 1):
            self.line_numbers.insert(tk.END, str(i))
            
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
    
    
    def find_file_in_directory(self, directory, filename):
        """
        在指定的資料夾路徑中查找特定檔案名稱。
        :param directory: 資料夾路徑
        :param filename: 檔案名稱
        :return: 檔案的完整路徑（如果找到），否則返回 None
        """
        # 檢查檔案是否存在於指定資料夾
        

        for root, dirs, files in os.walk(directory):
            
            for file in files:
               if file.startswith(filename) and file.endswith('.xml'):
                   return os.path.join(root, file)
        messagebox.showinfo("File Not Found", f"No file starting with {filename} and ending with .xml found in {directory}.")
        
        return None
    
    def load_xml_content(self):
        self.before_file_directory = self.find_folders_with_split(sd.before_path.get())
        self.after_file_directory = self.find_folders_with_split(sd.after_path.get())
        self.choose_file_name = self.file_path_entry.get()
        self.before_file_path = self.find_file_in_directory(self.before_file_directory, self.choose_file_name)
        self.after_file_path = self.find_file_in_directory(self.after_file_directory, self.choose_file_name)
        
        
        if self.before_file_path and self.after_file_path:
            global bf_tree, bf_root_element, af_tree, af_root_element
            bf_tree = ET.parse(self.before_file_path)
            af_tree = ET.parse(self.after_file_path)
            bf_root_element = bf_tree.getroot()
            af_root_element = af_tree.getroot()
            
            self.display_xml_content()
        else:
            print("Files not found, cannot proceed with parsing.")
    
    def display_xml_content(self):
        """
        首先刪除之前的內容，並且以階層形式展現xml
        """
        self.left_listbox.delete(0, tk.END)
        self.right_listbox.delete(0, tk.END)
        self.line_numbers.delete(0, tk.END)
        
        def display_node(node, listbox, indent=""):
            listbox.insert(tk.END,  f"{indent}{node.tag}: {node.text.strip() if node.text and node.text.strip() else ''}\n")               
            for child in node:
                display_node(child, listbox, indent + "    ")
        
        display_node(bf_root_element, self.left_listbox)
        display_node(af_root_element, self.right_listbox)
        self.compare_files()
         
    def compare_files(self):
        base_content = self.left_listbox.get(0, tk.END)
        new_content = self.right_listbox.get(0, tk.END)
        sm = difflib.SequenceMatcher(None, base_content, new_content)
        opcodes = sm.get_opcodes()
        
        self.highlight_differences(opcodes, base_content, new_content)

    def highlight_differences(self, opcodes, base, newtxt):
        self.left_listbox.delete(0, tk.END)
        self.right_listbox.delete(0, tk.END)
        
        for tag, i1, i2, j1, j2 in opcodes:
            for i in range(i1, i2):
                self.left_listbox.insert(tk.END, base[i])
                if tag == 'replace':
                    self.left_listbox.itemconfig(tk.END, {'bg':'#FFE153'})
                elif tag == 'delete':
                    self.left_listbox.itemconfig(tk.END, {'bg':'#fd8082'})
                elif tag == 'insert':
                    self.left_listbox.insert(tk.END, "")
                    self.left_listbox.itemconfig(tk.END, {'bg':'lightgreen'})
            for j in range(j1, j2):
                self.right_listbox.insert(tk.END, newtxt[j])
                if tag == 'replace':
                    self.right_listbox.itemconfig(tk.END, {'bg':'#FFE153'})
                elif tag == 'insert':
                    self.right_listbox.itemconfig(tk.END, {'bg':'lightgreen'})
                elif tag == 'delete':
                    self.right_listbox.insert(tk.END, "")
                    self.right_listbox.itemconfig(tk.END, {'bg':'#fd8082'})
        self.update_line_numbers()





