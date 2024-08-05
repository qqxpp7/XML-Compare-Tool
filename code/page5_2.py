# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 15:15:11 2024

@author: a9037
"""
import os
import random
import tkinter as tk
import shared_data as sd
import customtkinter as ctk
import xml.etree.ElementTree as ET
from tkinter import ttk, messagebox, filedialog

class ComparisonPage_2(ctk.CTkFrame):
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
        
        #右中左-中中-中右
        '''
        中間區域分兩個小視窗
        ''' 
        self.mylabel = tk.Label(self.middle_right_frame, bg='#87CEFA', text='選擇忽略或比對的key')
        self.mylabel.pack(fill="both",side=tk.TOP) 
        
        self.left_middle_right_frame = ctk.CTkFrame(self.middle_right_frame)
        self.left_middle_right_frame.pack(pady=5, padx=5, side="left", fill="both", expand=True)
        
        self.rig_middle_right_frame = ctk.CTkFrame(self.middle_right_frame)
        self.rig_middle_right_frame.pack(pady=5, padx=5, side="right", fill="y")
        
        '''
        上面區域
        
        '''
        self.mylabel = tk.Label(self.top_right_frame,  text='2/2    選擇Element', font=("Helvetica", 16))
        self.mylabel.pack(fill="both",side=tk.LEFT) 
        
        self.choose_button = ctk.CTkButton(self.top_right_frame, text="執行", width=200)
                                         
        self.choose_button.pack(side=tk.RIGHT, pady=5, padx=5)
        
        self.return_button = ctk.CTkButton(self.top_right_frame, text="上一頁", width=200
                                         , command=lambda: self.controller.show_frame("ComparisonPage"))
        
        self.return_button.pack(side=tk.LEFT, pady=5, padx=5)
        
        #右中左
        '''
        中間區域的左邊
        會秀出檔案的Element及Text
        wrap=tk.NONE 禁用自動換行
        
        '''
        
        self.y_scrollbar = tk.Scrollbar(self.left_middle_right_frame, orient=tk.VERTICAL, command=self._scroll_both)
        self.y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.line_numbers = tk.Listbox(self.left_middle_right_frame, width=4, font=("Helvetica", 14))
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        self.left_listbox = tk.Listbox(self.left_middle_right_frame, font=("Helvetica", 14), yscrollcommand=self._sync_scroll)
        self.left_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.left_x_scrollbar = tk.Scrollbar(self.left_listbox, orient=tk.HORIZONTAL, command=self.left_listbox.xview)
        self.left_x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.left_listbox['xscrollcommand'] = self.left_x_scrollbar.set
        self.left_listbox.bind("<Key>", lambda e: "break")


        self.right_listbox = tk.Listbox(self.left_middle_right_frame, font=("Helvetica", 14), yscrollcommand=self._sync_scroll)
        self.right_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.right_x_scrollbar = tk.Scrollbar(self.right_listbox, orient=tk.HORIZONTAL, command=self.right_listbox.xview)
        self.right_x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.right_listbox['xscrollcommand'] = self.right_x_scrollbar.set
        self.right_listbox.bind("<Key>", lambda e: "break")
        
        
        #右中右
        '''
        中間區域的右邊
        展示所選擇的key視窗，以及新增(+)與刪除(-)的按鈕
        ''' 
       
        self.buttons_frame = ctk.CTkFrame(self.rig_middle_right_frame, bg_color=self.middle_right_frame.cget("bg_color"))
        self.buttons_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.line_numbers = tk.Listbox(self.rig_middle_right_frame, width=4, font=("Helvetica", 14))
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        self.option_listbox = tk.Listbox(self.rig_middle_right_frame, font=("Helvetica",14))
        self.option_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar = tk.Scrollbar(self.rig_middle_right_frame, orient=tk.VERTICAL, command=self._scroll_both)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.option_listbox.config(yscrollcommand=self._sync_scroll)
        self.line_numbers.config(yscrollcommand=self._sync_scroll)
        self.scrollbar.config(command=self._scroll_both)
        
        self.option_listbox.bind('<KeyRelease>', self.update_line_numbers)
        self.option_listbox.bind('<MouseWheel>', self.update_line_numbers)
        self.option_listbox.bind('<ButtonRelease-1>', self.update_line_numbers)
        
        self.upload_button = ctk.CTkButton(self.buttons_frame, text="↥上傳", width=60, height=30,
                                   font=("Helvetica", 12), command=lambda: self.upload_file_tag())      
        self.upload_button.pack(side=tk.LEFT, pady=5, padx=1)
        
        self.download_button = ctk.CTkButton(self.buttons_frame, text="↧下載", width=60, height=30,
                                             font=("Helvetica", 12), command=lambda: self.download_file_tag())
        self.download_button.pack(side=tk.LEFT, pady=5, padx=1)
               
        self.add_button = ctk.CTkButton(self.buttons_frame, text="+", width=40, height=30)
        self.add_button.pack(side=tk.LEFT, pady=5,padx=1)

        self.remove_button = ctk.CTkButton(self.buttons_frame, text="-", width=40, height=30, command=self.remove_tag)
        self.remove_button.pack(side=tk.LEFT,pady=5,padx=1)
        
        
        '''
        下面區域
        清空舊資料的選擇
        開啟COPY資料夾的按鈕
        
        '''
        self.report_name_entry = self.default_input(self.bottom_right_frame, 0
                                                    , "報告書名稱：", 400, "Compare_Report")
        
        self.sequence_label = ctk.CTkLabel(self.bottom_right_frame, text="比對模式：")
        self.sequence_label.grid(row=1, column=0, pady=10, padx=20, sticky="w")

        self.sequence_var = tk.StringVar(value=" 忽略 ")
        self.sequence_options = ctk.CTkSegmentedButton(master=self.bottom_right_frame,
                                                       values=[" 比對 ", " 忽略 "], variable=self.sequence_var)
        self.sequence_options.grid(row=1, column=1, pady=10, padx=10, sticky="w")

        self.open_folder_button = ctk.CTkButton(self.bottom_right_frame, text="AI分析" 
                                                , width=200, fg_color="#CD5C5C")
        self.open_folder_button.grid(row=2, column=0, columnspan=2, pady=10, padx=10)
        
        self.open_folder_button = ctk.CTkButton(self.bottom_right_frame, text="開啟報告" 
                                                , width=200, fg_color="#CD5C5C")
        self.open_folder_button.grid(row=2, column=2, columnspan=2, pady=10, padx=10)
    
    def _sync_scroll(self, *args):
        self.line_numbers.yview_moveto(args[0])
        self.left_listbox.yview_moveto(args[0])
        self.right_listbox.yview_moveto(args[0])
        self.option_listbox.yview_moveto(args[0])

    def _scroll_both(self, *args):
        self.line_numbers.yview(*args)
        self.left_listbox.yview(*args)
        self.right_listbox.yview(*args)
        self.option_listbox.yview(*args)
        
    def update_line_numbers(self, event=None):
        '''
        更新數量列，並且寬度會隨著數量調整
        '''
        self.line_numbers.delete(0, tk.END)
        line_count = self.option_listbox.size()
        max_digits = len(str(line_count))
        self.line_numbers.config(width=max_digits + 1)
        for i in range(1, self.option_listbox.size() + 1):
            self.line_numbers.insert(tk.END, str(i)) 
        
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
        return None
    
    
    def download_file_tag(self):
        '''
        下載隨機一份選擇檔案內所有的tag及它的上一層
        
        '''
        self.before_file_directory = self.find_folders_with_split(sd.before_path.get())
        
        self.choose_file_name = random.choice(sd.choose_5_files)
        
        self.file_path = self.find_file_in_directory(self.before_file_directory, self.choose_file_name)
        
        # 解析XML文件並提取標籤和上一層標籤
        tree = ET.parse(self.file_path)
        root = tree.getroot()
        
        tags = []
        def get_tags(parent, parent_tag):
            for child in parent:
                tags.append(f"<{parent_tag}>/<{child.tag}>")
                get_tags(child, child.tag)
        
        get_tags(root, root.tag)

        # 將結果寫入文本檔案
        output_file_path = os.path.join(sd.report_output_path.get(), 'Compare_file_tag.txt')
        
        with open(output_file_path, 'w', encoding='utf-8') as f:
            print(self.choose_file_name)
            for tag in tags:
                f.write(f"{tag}\n")
        
        # 自動開啟生成的文件
        os.startfile(output_file_path)

    
    def upload_file_tag(self):
        '''
        上傳並檢查txt文件格式及內容
        '''
        self.before_file_directory = self.find_folders_with_split(sd.before_path.get())
        
        txt_file_path = filedialog.askopenfilename(title="Select file",filetypes=[("Text files", "*.txt")])
        
        if not txt_file_path:
            messagebox.showwarning("Warning", "未選取任何檔案")
            return
        
        with open(txt_file_path, 'r', encoding='utf-8') as f:
            uploaded_tags = [line.strip() for line in f if line.strip()]
       
        # 獲取self.choose_file內所有檔案的標籤
        all_tags = set()
        for file_name in sd.choose_5_files:
            full_path = self.find_file_in_directory(self.before_file_directory, file_name)
            if full_path:
                tree = ET.parse(full_path)
                root = tree.getroot()
                def get_all_tags(parent, parent_tag):
                    for child in parent:
                        all_tags.add(f"<{parent_tag}>/<{child.tag}>")
                        get_all_tags(child, child.tag)
                get_all_tags(root, root.tag)

        # 檢查上傳的標籤是否都存在於所有檔案的標籤內
        valid_tags = []
        invalid_tags = []
        for tag in uploaded_tags:
            if tag in all_tags:
                valid_tags.append(tag)
            else:
                invalid_tags.append(tag)
        
        if invalid_tags:
            messagebox.showwarning("Warning", f"Some tags are not found in the XML files and will be ignored: {', '.join(invalid_tags)}")

        # 若所有標籤都符合，將其顯示在self.option_listbox
        self.option_listbox.delete(0, 'end')  # 清空現有的列表
        for tag in valid_tags:
            self.option_listbox.insert('end', tag)
            self.update_line_numbers()
            
        messagebox.showinfo("Success", "Tags uploaded and verified successfully.")
        
        
    def remove_tag(self):
        '''
        刪除在option_listbox選中的tag
        並呼叫更新數列的函式
        '''
        selection = self.option_listbox.curselection()
        if selection:
            index = selection[0]
            self.option_listbox.delete(index)
            self.update_line_numbers()
            
    def update_listbox_numbers(self):
        '''
        在刪除某一列的檔名後
        會刷新全部的順序
        '''
        items = self.listbox.get(0, tk.END)
        self.listbox.delete(0, tk.END)
        for i, item in enumerate(items):
            if '. ' in item:
                name = item.split('. ',1 )[1]  # Remove the existing numbering
            else:
                name = item
            self.listbox.insert(tk.END, f"{i + 1}. {name}")        
            
    def load_xml_content(self):
        self.before_file_directory = self.find_folders_with_split(sd.before_path.get())
        self.after_file_directory = self.find_folders_with_split(sd.after_path.get())
        
        self.before_file_path = self.find_file_in_directory(self.before_file_directory, self.choose_file_name)
        self.after_file_path = self.find_file_in_directory(self.after_file_directory, self.choose_file_name)

        global bf_tree, bf_root_element, af_tree, af_root_element
        bf_tree = ET.parse(self.before_file_path[0])
        af_tree = ET.parse(self.after_file_path[0])
        self.bf_root_element = bf_tree.getroot()
        self.af_root_element = af_tree.getroot()
        
        self.display_xml_content()
        
        
    def display_xml_content(self):
        """
        首先刪除之前的內容，並且以階層形式展現xml
        """
        self.left_listbox.delete(0, tk.END)
        
        def display_node(node, indent=""):
            self.left_listbox.insert(tk.END,  f"{indent}{node.tag}: {node.text.strip() if node.text and node.text.strip() else ''}\n")               
            for child in node:
                display_node(child, indent + "    ")
        
        display_node(self.root_element)