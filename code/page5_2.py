# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 15:15:11 2024

@author: a9037
"""
import os
import time
import random
import difflib
import tkinter as tk
import shared_data as sd
from pathlib import Path
import customtkinter as ctk
from datetime import datetime
import xml.etree.ElementTree as ET
from tkinter import messagebox, filedialog

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
        
        
        '''
        中間區域分兩個小視窗
        ''' 
        self.top_middle_right_frame = ctk.CTkFrame(self.middle_right_frame, fg_color="transparent")
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
        
        self.left_middle_right_frame = ctk.CTkFrame(self.middle_right_frame)
        self.left_middle_right_frame.pack(pady=5, padx=5, side="left", fill="both", expand=True)
        
        self.rig_middle_right_frame = ctk.CTkFrame(self.middle_right_frame)
        self.rig_middle_right_frame.pack(pady=5, padx=5, side="right", fill="y")
        
        '''
        上面區域
        
        '''
        self.label = ctk.CTkLabel(self.top_right_frame,  text='2/2    選擇Element', font=("Helvetica", 16), corner_radius	= 10)
        self.label.pack(side=tk.LEFT, fill="both") 
        
        self.choose_button = ctk.CTkButton(self.top_right_frame, text="執行", width=200
                                           , command=lambda: self.execute())
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
        
        self.tag_numbers = tk.Listbox(self.rig_middle_right_frame, width=4, font=("Helvetica", 14))
        self.tag_numbers.pack(side=tk.LEFT, fill=tk.Y)
        self.option_listbox = tk.Listbox(self.rig_middle_right_frame, font=("Helvetica",14))
        self.option_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar = tk.Scrollbar(self.rig_middle_right_frame, orient=tk.VERTICAL, command=self._scroll_both)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.option_listbox.config(yscrollcommand=self._sync_scroll)
        self.tag_numbers.config(yscrollcommand=self._sync_scroll)
        self.scrollbar.config(command=self._scroll_both)
        
        
        self.upload_button = ctk.CTkButton(self.buttons_frame, text="↥上傳", width=60, height=30,
                                   font=("Helvetica", 12), command=lambda: self.upload_file_tag())      
        self.upload_button.pack(side=tk.LEFT, pady=5, padx=1)
        
        self.download_button = ctk.CTkButton(self.buttons_frame, text="↧下載", width=60, height=30,
                                             font=("Helvetica", 12), command=lambda: self.download_file_tag())
        self.download_button.pack(side=tk.LEFT, pady=5, padx=1)
               
        self.add_button = ctk.CTkButton(self.buttons_frame, text="+", width=40, height=30, command=self.add_tag)
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
        self.sequence_label.grid(row=1, column=0, pady=5, padx=20, sticky="w")

        self.sequence_var = tk.StringVar(value=" 忽略 ")
        self.sequence_options = ctk.CTkSegmentedButton(master=self.bottom_right_frame,
                                                       values=[" 比對 ", " 忽略 "], variable=self.sequence_var)
        self.sequence_options.grid(row=1, column=1, pady=5, padx=10, sticky="w")

        self.open_folder_button = ctk.CTkButton(self.bottom_right_frame, text="AI分析" 
                                                , width=200, fg_color="#CD5C5C")
        self.open_folder_button.grid(row=2, column=0, columnspan=2, pady=10, padx=10)
        
        self.open_folder_button = ctk.CTkButton(self.bottom_right_frame, text="開啟報告" 
                                                , width=200, fg_color="#CD5C5C")
        self.open_folder_button.grid(row=2, column=2, columnspan=2, pady=10, padx=10)
 
    
    def _sync_scroll(self, *args):
        self.line_numbers.yview_moveto(args[0])
        self.tag_numbers.yview_moveto(args[0])
        self.left_listbox.yview_moveto(args[0])
        self.right_listbox.yview_moveto(args[0])
        self.option_listbox.yview_moveto(args[0])

    def _scroll_both(self, *args):
        self.line_numbers.yview(*args)
        self.tag_numbers.yview(*args)
        self.left_listbox.yview(*args)
        self.right_listbox.yview(*args)
        self.option_listbox.yview(*args)
        
    def update_tag_numbers(self, event=None):
        '''
        更新tag數量列，並且寬度會隨著數量調整
        '''
        self.tag_numbers.delete(0, tk.END)
        tag_count = self.option_listbox.size()
        max_digits = len(str(tag_count))
        self.tag_numbers.config(width=max_digits + 1)
        for i in range(1, self.option_listbox.size() + 1):
            self.tag_numbers.insert(tk.END, str(i))
            
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
        get_tags()解析XML文件並提取標籤和上一層標籤
        將結果寫入再Final底下的Compare_file_tag.txt，並自動開啟
        '''
        self.before_file_directory = self.find_folders_with_split(sd.before_path.get())
        
        self.choose_file_name = random.choice(sd.choose_5_files)
        
        self.file_path = self.find_file_in_directory(self.before_file_directory, self.choose_file_name)
        
        tree = ET.parse(self.file_path)
        root = tree.getroot()
        
        tags = []
        def get_tags(parent, parent_tag):
            for child in parent:
                tags.append(f"<{parent_tag}>/<{child.tag}>")
                get_tags(child, child.tag)
        
        get_tags(root, root.tag)

        output_file_path = os.path.join(sd.report_output_path.get(), 'Compare_file_tag.txt')
        with open(output_file_path, 'w', encoding='utf-8') as f:
            print(self.choose_file_name)
            for tag in tags:
                f.write(f"{tag}\n")
        os.startfile(output_file_path)

    
    def upload_file_tag(self):
        '''
        上傳並檢查txt文件格式及內容
        find_file_in_directory()獲取self.choose_file內所有檔案的標籤
        檢查上傳的標籤是否都存在於所有檔案的標籤內
        若所有標籤都符合，將其顯示在self.option_listbox
        '''
        self.before_file_directory = self.find_folders_with_split(sd.before_path.get())
        
        txt_file_path = filedialog.askopenfilename(title="Select file",filetypes=[("Text files", "*.txt")])
        
        if not txt_file_path:
            messagebox.showwarning("Warning", "未選取任何檔案")
            return
        
        with open(txt_file_path, 'r', encoding='utf-8') as f:
            uploaded_tags = [line.strip() for line in f if line.strip()]
       
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

        valid_tags = []
        invalid_tags = []
        for tag in uploaded_tags:
            if tag in all_tags:
                valid_tags.append(tag)
            else:
                invalid_tags.append(tag)
        
        if invalid_tags:
            messagebox.showwarning("Warning", f"Some tags are not found in the XML files and will be ignored: {', '.join(invalid_tags)}")

        self.option_listbox.delete(0, 'end')  
        for tag in valid_tags:
            self.option_listbox.insert('end', tag)
            self.update_tag_numbers()
            
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
            self.update_tag_numbers()
        else:
            messagebox.showwarning("Warning","No selection.")
    
        
    def add_tag(self):
        '''
        在option_listbox新增左邊listbox選中的tag

        '''
        left_selection = self.left_listbox.curselection() 
        right_selection = self.right_listbox.curselection()
        
        if left_selection:
            selected_text = self.left_listbox.get(left_selection)
            self.extract_and_add_tag(selected_text, bf_root_element)
            
            self.update_tag_numbers()
        elif right_selection:
            selected_text = self.right_listbox.get(right_selection)
            self.extract_and_add_tag(selected_text, af_root_element)
                    
            self.update_tag_numbers()
        else:
            messagebox.showwarning("Warning","No selection.")
            
    def extract_and_add_tag(self, selected_text, root_element):
        '''
        提取選中的標籤名稱
        遍歷節點來找到相應的節點和它的父節點
        在加入前先檢查是否已存在，如果標籤已存在，會彈出警告訊息
        '''
        tag_name = selected_text.strip().split(":")[0].strip()
        self.find_and_add_tag(root_element, tag_name)

    def find_and_add_tag(self, node, tag_name, parent_tag=None):
        
        if node.tag == tag_name and parent_tag is not None:
            formatted_tag = f"<{parent_tag}>/<{node.tag}>"
            if formatted_tag not in self.option_listbox.get(0, tk.END):
                self.option_listbox.insert(tk.END, formatted_tag)
            else:
                messagebox.showwarning("重複標籤", f"標籤 '{formatted_tag}' 已經存在於列表中！")
        for child in node:
            self.find_and_add_tag(child, tag_name, node.tag)   
            
    def load_xml_content(self):
        self.before_file_directory = self.find_folders_with_split(sd.before_path.get())
        self.after_file_directory = self.find_folders_with_split(sd.after_path.get())
        self.choose_file_name = random.choice(sd.choose_5_files)
        self.before_file_path = self.find_file_in_directory(self.before_file_directory, self.choose_file_name)
        self.after_file_path = self.find_file_in_directory(self.after_file_directory, self.choose_file_name)

        global bf_tree, bf_root_element, af_tree, af_root_element
        bf_tree = ET.parse(self.before_file_path)
        af_tree = ET.parse(self.after_file_path)
        bf_root_element = bf_tree.getroot()
        af_root_element = af_tree.getroot()
        
        self.display_xml_content()

        
    def display_xml_content(self):
        """
        首先刪除之前的內容，並且以階層形式展現xml
        """
        self.left_listbox.delete(0, tk.END)
        self.right_listbox.delete(0, tk.END)
        self.option_listbox.delete(0, tk.END)
        self.tag_numbers.delete(0, tk.END)
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
    
    def read_exclude_tags(self):
        '''
        讀取listbox要刪除的tag
        '''
        exclude_tags = [self.option_listbox.get(idx) for idx in range(self.option_listbox.size())]
        print("exclude_tags: ", exclude_tags)
        return exclude_tags

    def clean_tag(self, tag):
        return tag.strip('<>')

    def remove_excluded_tags(self, root, exclude_tags):
        '''
        將tag從資料刪除
        '''
        for tag_path in exclude_tags:
            parent_tag, child_tag = map(self.clean_tag, tag_path.split('/'))
            if parent_tag == root.tag:
                parents = [root]
            else:
                parents = root.findall(f'.//{parent_tag}')
            for parent in parents:
                for child in parent.findall(child_tag):
                    parent.remove(child)
        return root

    def get_filtered_xml_content(self, xml_path, exclude_tags):
        tree = ET.parse(xml_path)
        root = tree.getroot()
        root = self.remove_excluded_tags(root, exclude_tags)
        return ET.tostring(root, encoding='unicode')

    def compare_elements(self, element1, element2, path=''):
        changes = []
        if element1.tag != element2.tag:
            changes.append(f'Tag changed from <{element1.tag}> to <{element2.tag}> at {path}')
        if element1.text != element2.text:
            changes.append(f'Text changed in <{element1.tag}> at {path}: {element1.text} -> {element2.text}')
        
        children1 = list(element1)
        children2 = list(element2)
        
        tags1 = {child.tag for child in children1}
        tags2 = {child.tag for child in children2}
        
        added_tags = tags2 - tags1
        removed_tags = tags1 - tags2
        
        for tag in added_tags:
            changes.append(f'Added tag <{tag}> at {path}/{element1.tag}')
        for tag in removed_tags:
            changes.append(f'Removed tag <{tag}> at {path}/{element1.tag}')
        
        common_tags = tags1 & tags2
        for tag in common_tags:
            child1 = element1.find(tag)
            child2 = element2.find(tag)
            if child1 is not None and child2 is not None:
                sub_changes = self.compare_elements(child1, child2, path=f'{path}/{element1.tag}')
                changes.extend(sub_changes)
        
        return changes
    
    def compare_xml_files(self, folder1, folder2, exclude_tags):
        folder1 = Path(folder1)
        folder2 = Path(folder2)
        
        results = []
        matches = []
        
        for file1 in folder1.glob('*.xml'):
            file2 = folder2 / file1.name
            if file2.exists():
                content1 = self.get_filtered_xml_content(file1, exclude_tags)
                content2 = self.get_filtered_xml_content(file2, exclude_tags)
                
                root1 = ET.fromstring(content1)
                root2 = ET.fromstring(content2)
                
                if content1 == content2:
                    matches.append(file1.name)
                else:
                    changes = self.compare_elements(root1, root2)
                    results.append((file1.name, 'Different', changes))
            else:
                results.append((file1.name, 'Missing in folder2'))
        
        return results, matches
    
    def print_fixedtag_file(self, file_path, exclude_tags, results, matches):
        
         # 在Final底下新建fixed_tag_report，將拆分後重複文件放在那
        
        TIME_START = time.time()
        with open(file_path, 'a', encoding='utf-8') as file:
            TIME_END = time.time()
            file.write("------------------------Header ---------------------\n")
            file.write(f"執行時間     :{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write(f"花費時間     :{TIME_END - TIME_START} 秒\n")
            file.write("執行檔案      :before_split、after_split\n")
            file.write("--------------------Input Parameter ---------------------\n")
            file.write(f"檔案數量      :{len(results) + len(matches)}\n")
            file.write(f"忽略Element  :{exclude_tags}\n")
            file.write("--------------------內容 ---------------------\n")
            
            for res in results:
               file.write(f"\nFile: {res[0]}, Result: {res[1]}\n")
               if res[1] == 'Different':
                   for change in res[2]:
                       file.write(f" - {change}\n")
           
            file.write("\n固定element內容都相同：\n")
            for match in matches:
                file.write(f"{match}\n")
            file.write("\n\n")
        
        if os.name == 'nt':
            os.startfile(file_path)
    
    def print_changedtag_file(self, file_path, changed_tags, *results_lists):
        
         # 在Final底下新建fixed_tag_report，將拆分後重複文件放在那
        
        TIME_START = time.time()
        with open(file_path, 'a', encoding='utf-8') as file:
            TIME_END = time.time()
            file.write("------------------------Header ---------------------\n")
            file.write(f"執行時間     :{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write(f"花費時間     :{TIME_END - TIME_START} 秒\n")
            file.write("執行檔案      :before_split、after_split\n")
            file.write("--------------------Input Parameter ---------------------\n")
            # file.write(f"檔案數量      :{len(results) + len(matches)}\n")
            file.write(f"變動Element  :{changed_tags}\n")
            file.write("--------------------內容 ---------------------\n")
            
            for results in results_lists:
                if results:  # 檢查列表是否有資料
                    for result in results:
                        file.write(result + "\n")
        
        if os.name == 'nt':
            os.startfile(file_path)
            
    def execute(self):
        exclude_tags = self.read_exclude_tags()
        print(exclude_tags)
        self.before_file_directory = self.find_folders_with_split(sd.before_path.get())
        self.after_file_directory = self.find_folders_with_split(sd.after_path.get())
        
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        fixed_tag_new_folder = os.path.join(sd.report_output_path.get(), "fixed_tag_report")
        os.makedirs(fixed_tag_new_folder, exist_ok=True)
        file_path = os.path.join(fixed_tag_new_folder, f"fixed_tag_{current_time}.txt")

        results, matches = self.compare_xml_files(self.before_file_directory, self.after_file_directory, exclude_tags)
        self.print_fixedtag_file(file_path, exclude_tags, results, matches)