import os
import re
import random
import tkinter as tk
import customtkinter as ctk
from datetime import datetime
import xml.etree.ElementTree as ET
from tkinter import ttk, messagebox, scrolledtext
import shared_data 

class XMLSplitPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.file_path = None
        self.all_file_path = None
        self.folder_path = None
        self.child_nodes = list()
        self.filename_count = {}
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
        中間區域分三個小視窗
        ''' 
        self.mylabel = tk.Label(self.middle_right_frame, bg='#87CEFA', text='選擇命名的key')
        self.mylabel.pack(fill="both",side=tk.TOP) 
        
        self.left_middle_right_frame = ctk.CTkFrame(self.middle_right_frame)
        self.left_middle_right_frame.pack(pady=5, padx=5, side="left", fill="both", expand=True)
        
        self.mid_middle_right_frame = ctk.CTkFrame(self.middle_right_frame)
        self.mid_middle_right_frame.pack(pady=5, padx=5, side="left", fill="both", expand=True)
        
        self.rig_middle_right_frame = ctk.CTkFrame(self.middle_right_frame)
        self.rig_middle_right_frame.pack(pady=5, padx=5, side="left", fill="both", expand=True)
        
        '''
        上區域會選擇從"All", "Before", "After"進行檔案分割
        ''' 
        self.selected_option = tk.StringVar()
        self.selected_option.set("Select Folder")
        self.options = ["All", "Before", "After"]
        self.create_combobox()
               
        self.ok_button = ctk.CTkButton(self.top_right_frame, text="拆分", command=self.split_xml)
        self.ok_button.grid(row=0, column=3, pady=10, padx=10, sticky="w")


        #右中左
        '''
        中間區域的左邊
        選擇key element的小視窗，所有key element都會在這邊
        ''' 
        self.scrollbar = tk.Scrollbar(self.left_middle_right_frame) 
        self.scrollbar.pack(side='right', fill='y')        
        
        self.all_nodes_listbox = tk.Listbox(self.left_middle_right_frame, selectmode=tk.SINGLE, yscrollcommand=self.scrollbar.set, font=("Helvetica",14))
        self.all_nodes_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        # self.all_nodes_listbox.bind('<<ListboxSelect>>', self.on_node_select)
        
                  
        # 右中間框架
        '''
        中間區域的中間
        會秀出檔案的Element及Text
        wrap=tk.NONE 禁用自動換行
        '''
        self.text_area = scrolledtext.ScrolledText(self.mid_middle_right_frame, wrap=tk.NONE, width=50, height=20, font=("Helvetica",14))
        self.text_area.pack(fill=tk.BOTH, expand=True)
        
        self.x_scrollbar = tk.Scrollbar(self.mid_middle_right_frame, orient=tk.HORIZONTAL, command=self.text_area.xview)
        self.x_scrollbar.pack(side='bottom', fill='x')
        self.text_area['xscrollcommand'] = self.x_scrollbar.set
        #Lock the text area to read-only
        self.text_area.bind("<Key>", lambda e: "break")
         
        
        #右中右
        '''
        中間區域的右邊
        展示所選擇的key視窗，以及新增(+)與刪除(-)的按鈕
        ''' 
        self.option_listbox = tk.Listbox(self.rig_middle_right_frame, font=("Helvetica",14))
        self.option_listbox.pack(fill=tk.BOTH, expand=True)
               
        self.add_button = ctk.CTkButton(self.rig_middle_right_frame, text="+",width=80,height=30, command=self.add_child_node)
        self.add_button.pack(side=tk.LEFT, pady=5,padx=5)

        self.remove_button = ctk.CTkButton(self.rig_middle_right_frame, text="-",width=80,height=30, command=self.remove_child_node)
        self.remove_button.pack(side=tk.LEFT,pady=5,padx=5)


        #右下
        '''
        下面區域
        有預設值的拆分Element跟分隔符號的輸入框
        流水號標籤，共有三個選項
        '''
        self.split_element_entry = self.default_input(self.bottom_right_frame, 1, "拆分Element：", 400, "")
        self.delimiter_entry = self.default_input(self.bottom_right_frame, 2, "分隔符號：", 50, "_")
             

        self.sequence_label = ctk.CTkLabel(self.bottom_right_frame, text="流水號：")
        self.sequence_label.grid(row=3, column=0, pady=10, padx=50, sticky="w")       
        self.sequence_var = tk.StringVar(value="無")
        self.sequence_options = ctk.CTkSegmentedButton(master=self.bottom_right_frame,
             values=["前面", "後面", "無"],variable=self.sequence_var,)        
        self.sequence_options.grid(row=3, column=1, pady=10, padx=10, sticky="w")
        

    def create_combobox(self):
        '''
        上面區域選擇從"All", "Before", "After"進行檔案分割的combobox建立
        ''' 
        combobox = ttk.Combobox(self.top_right_frame, textvariable=self.selected_option,
                                values=self.options, state="readonly")
        combobox.grid(row=0, column=0, pady=10, padx=30)
        self.selected_option.trace("w", self.on_dropdown_select)
        
    
    def default_input(self, frame, row, label_text, entry_width, default_text):
        label = ctk.CTkLabel(self.bottom_right_frame, text=label_text, anchor="w")
        label.grid(row=row, column=0, pady=10, padx=50, sticky="w")
        entry = ctk.CTkEntry(self.bottom_right_frame, width=entry_width)
        entry.grid(row=row, column=1, sticky="w")
        entry.insert(0, default_text) # 預設 xml
        return entry


    def create_valid_filename(self, text):
        '''
        使用正則表達式移除或替換檔案名中的非法字符
        '''
        return re.sub(r'[^\w\-_\.]', '', text)
 
    
    def random_load_xml_file(self, *paths):
        '''
        載入選定資料夾內的隨機一個xml檔案
        '''
        files = []
        for path in paths:
            if os.path.isdir(path):
                files.extend([os.path.join(path, f) for f in os.listdir(path) if f.endswith('.xml')])
        if not files:
            return None
        return random.choice(files)
    
    
    def load_xml_files(self, *paths):
        '''
        載入選定資料夾內的所有xml檔案
        '''
        files = []
        for path in paths:
            if os.path.isdir(path):
                files.extend([os.path.join(path, f) for f in os.listdir(path) if f.endswith('.xml')])
        return files

    
    def on_dropdown_select(self, *args):
        '''
        選擇All的時候會隨機選擇before或after路徑，選好資料夾後會跳到load_xml_file隨機選擇一個檔案
        選好檔案路徑後再透過display_xml_content展示檔案內容
        '''
        self.before_path = shared_data.before_path.get()
        self.after_path = shared_data.after_path.get()
        
        self.option_listbox.delete(0, tk.END)
        self.child_nodes.clear()
        
        selected_option = self.selected_option.get()  # 根據選擇的選項來設置資料夾路徑
        if selected_option == "All":
            self.folder_path = [self.before_path, self.after_path]  # 使用列表來存儲多個路徑   
        elif selected_option == "Before":
            self.folder_path = [self.before_path]
            # print(selected_option, "+",folder_path)
        elif selected_option == "After":
            self.folder_path = [self.after_path]
            # print(selected_option, "+", folder_path)
        else:
            self.folder_path = None
        
        if self.folder_path:
            self.file_path = self.random_load_xml_file(*self.folder_path)
        if self.file_path:
            self.load_xml_content([self.file_path])
            # self.display_xml_content([self.file_path])

        
    def load_xml_content(self, file_paths):
        if not file_paths:
            return
        global tree, root_element
        tree = ET.parse(file_paths[0])
        self.root_element = tree.getroot()
        self.populate_all_nodes_list()
        self.display_xml_content()
        self.split_element_entry.delete(0, tk.END)
        self.split_element_entry.insert(0, self.all_possible_nodes[1])


    def populate_all_nodes_list(self):
        """
        先刪除之前的右中左的all_nodes_listbox
        再讀取xml，並根據順序 insert tag to all_possible_nodes , 去重
        **如果xml有出現重複的tag，可能也會去掉
        """
        self.all_nodes_listbox.delete(0, tk.END)
        
        self.all_possible_nodes = []
        for child in self.root_element.iter():
            if child.tag not in self.all_possible_nodes:
                self.all_possible_nodes.append(child.tag)        
                
        for node in self.all_possible_nodes:
            self.all_nodes_listbox.insert(tk.END, node)            
    
    
    def display_xml_content(self, file_paths=None):
        """
        首先刪除之前的內容，並且以階層形式展現xml
        """
        self.text_area.delete('1.0', tk.END)
        
        def display_node(node, indent=""):
            self.text_area.insert(tk.END,  f"{indent}{node.tag}: {node.text.strip() if node.text and node.text.strip() else ''}\n")               
            for child in node:
                display_node(child, indent + "    ")
        
        display_node(self.root_element)


    def add_child_node(self):
        '''
        在左邊all_nodes_listbox選中要的tag，點下+會變黃色
        右邊的option_listbox會新增tag
        最多選5個tag
        '''
        selection = self.all_nodes_listbox.curselection()
        if selection:
            index = selection[0]
            node = self.all_nodes_listbox.get(index)
                           
            if len(self.child_nodes) > 4:
                messagebox.showinfo("Error", "You can select no more than 5 items.")
                return
            else:
                self.child_nodes.append(node)
                self.all_nodes_listbox.itemconfig(index, {'bg':'yellow'})
                
        self.update_option_list()


    def remove_child_node(self):
        '''
        在右邊option_listbox選中要刪除的tag，點下-option_listbox會減少tag       
        items會展示所有的tag，透過node得知目前在右邊選中的tag
        在左邊all_nodes_listbox會變回白色
        '''
        selection = self.option_listbox.curselection()
        if selection:
            index = selection[0]
            node = self.option_listbox.get(index)
            self.child_nodes.remove(node)
            
            items = self.all_nodes_listbox.get(0, tk.END)
            config_index = items.index(node)
            self.all_nodes_listbox.itemconfig(config_index, {'bg':'white'})
        self.update_option_list()


    def update_option_list(self):
        '''
        更新右邊的option_list，首先會先刪除畫面
        將node一行一行插入
        '''
        self.option_listbox.delete(0, tk.END)
        for node in self.child_nodes:
            self.option_listbox.insert(tk.END, node)


    def split_xml(self):
        if not self.child_nodes:
            messagebox.showinfo("Error", "Please select at least one child node.")
            return
        
        selected_option = self.selected_option.get()  # 根據選擇的選項來設置資料夾路徑
        self.filename_count.clear()
        
        # 創建進度條視窗
        progress_window = tk.Toplevel()
        progress_window.title("Processing")
        progress_label = tk.Label(progress_window, text="Processing, please wait...")
        progress_label.pack(pady=10)
        progress_bar = ttk.Progressbar(progress_window)
        progress_bar.pack(pady=10)
        
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        repeat_new_folder = os.path.join(shared_data.report_output_path.get(), "repeat_file")
        os.makedirs(repeat_new_folder, exist_ok=True)
        file_path = os.path.join(repeat_new_folder, f"repeat_file_{current_time}.txt")
        
        self.all_file_path = self.load_xml_files(self.folder_path[0])
        total_files = len(self.all_file_path)  # 計算Before文件數量
        progress_bar['maximum'] = total_files * 2
        
        def update_progress():
            progress_window.update_idletasks()
            
        if selected_option == "All":
            # 確保新資料夾已經創建
            before_new_folder = os.path.join(self.before_path, "before_split")
            after_new_folder = os.path.join(self.after_path, "after_split")
            os.makedirs(before_new_folder, exist_ok=True)
            os.makedirs(after_new_folder, exist_ok=True)
                        
            # before
            self.all_file_path = self.load_xml_files(self.folder_path[0])
            for i, file in enumerate(self.all_file_path):
                self.save_books_from_xml(file, self.split_element_entry.get(), list(self.child_nodes), 
                                         self.delimiter_entry.get(), before_new_folder)
                progress_bar['value'] = i + 1
                update_progress()  
                
            has_value_greater_than_one = any(value > 1 for value in self.filename_count.values())
            if has_value_greater_than_one:
                messagebox.showinfo("警告"," Duplicate filename detected in Before")   
            self.print_file(self.filename_count, 'Before', self.split_element_entry.get(), self.child_nodes,
                            self.delimiter_entry.get(), self.sequence_var.get(), file_path, False)
            
            # after
            self.filename_count.clear()
            self.all_file_path = self.load_xml_files(self.folder_path[1]) 
            
            for i, file in enumerate(self.all_file_path):
                self.save_books_from_xml(file, self.split_element_entry.get(), list(self.child_nodes), 
                                         self.delimiter_entry.get(), after_new_folder)
                progress_bar['value'] = i + 1 + total_files
                update_progress()
                
            has_value_greater_than_one = any(value > 1 for value in self.filename_count.values())
            if has_value_greater_than_one:
                messagebox.showinfo("警告"," Duplicate filename detected in After")
                
            # 打開資料夾
            messagebox.showinfo("Success", "XML split successfully!")
            if os.name == 'nt':
                    os.startfile(before_new_folder)
                    os.startfile(after_new_folder)
            self.print_file(self.filename_count, 'After', self.split_element_entry.get(), self.child_nodes, 
                            self.delimiter_entry.get(), self.sequence_var.get(), file_path)
                    
        elif selected_option == "Before":
            before_new_folder = os.path.join(self.before_path, "before_split")
            os.makedirs(before_new_folder, exist_ok=True)
            self.all_file_path = self.load_xml_files(*self.folder_path)  
            for i, file in enumerate(self.all_file_path):
                self.save_books_from_xml(file, self.split_element_entry.get(), list(self.child_nodes),
                                         self.delimiter_entry.get(), before_new_folder)
                progress_bar['value'] = i + 1
                update_progress()
                
            has_value_greater_than_one = any(value > 1 for value in self.filename_count.values())
            if has_value_greater_than_one:
                messagebox.showinfo("警告"," Duplicate filename detected in Before")    
            
            messagebox.showinfo("Success", "XML split successfully!")
            if os.name == 'nt':  # For Windows
                os.startfile(before_new_folder)   
            self.print_file(self.filename_count, 'Before', self.split_element_entry.get(), self.child_nodes,
                            self.delimiter_entry.get(), self.sequence_var.get(), file_path)
            
        elif selected_option == "After":
            after_new_folder = os.path.join(self.after_path, "after_split")
            os.makedirs(after_new_folder, exist_ok=True)
            self.all_file_path = self.load_xml_files(*self.folder_path)  
            for i, file in enumerate(self.all_file_path):
                self.save_books_from_xml(file, self.split_element_entry.get(), list(self.child_nodes), 
                                         self.delimiter_entry.get(), after_new_folder)
                progress_bar['value'] = i + 1
                update_progress()
                
            has_value_greater_than_one = any(value > 1 for value in self.filename_count.values())
            if has_value_greater_than_one:
                messagebox.showinfo("警告"," Duplicate filename detected in After")
            
            messagebox.showinfo("Success", "XML split successfully!")
            if os.name == 'nt':  # For Windows
                os.startfile(after_new_folder)
            self.print_file(self.filename_count, 'After', self.split_element_entry.get(), self.child_nodes, 
                            self.delimiter_entry.get(), self.sequence_var.get(), file_path)
        else:
            messagebox.showinfo("Error", "Please select at least one option.")
        
        progress_window.destroy()

            
    def save_books_from_xml(self, xml_path, node_name, child_nodes, split_character, base_folder):
        try:
            # Load the XML file
            tree = ET.parse(xml_path)
            root = tree.getroot()

            nodes = [root] if root.tag == node_name else root.findall('.//' + node_name)
            
            for node in nodes:
                elements = {}
                for child in child_nodes:
                    element = node.find('.//' + child)
                    if element is not None:
                        elements[child] = self.create_valid_filename(element.text)                                            
    
                # Create filename based on the elements
                filename_elements = [elements[key] for key in child_nodes if key in elements]
                filename = split_character.join(filename_elements) + ".xml"
                original_filename = filename
                
                #計算檔案出現次數
                if original_filename in self.filename_count:
                    self.filename_count[original_filename] += 1
                else:
                    self.filename_count[original_filename] = 1                
                
                #當出現次數=1維持原檔名
                if self.filename_count[original_filename] > 1:                                    
                    if self.sequence_var.get() == "前面":
                        filename = f"{self.filename_count[original_filename]}{split_character}{original_filename}.xml"
                    elif self.sequence_var.get() == "後面":
                        filename = f"{original_filename[:-4]}{split_character}{self.filename_count[original_filename]}.xml"
                    else:
                        filename = original_filename  # 無序號選擇
                else:
                    filename = original_filename
                
                node_tree = ET.ElementTree(node)

                # Save in the specified folder
                output_folder = os.path.join(base_folder, filename)
                node_tree.write(output_folder, encoding="UTF-8")
    

        except Exception as e:
            print(f"Error processing file {xml_path}: {e}")
        
    def print_file(self, count_dict, file_name, split_element, child_nodes, delimiter, sequence, file_path, open_file_boolean=True ):
        '''
        在Final底下新建repeat_file，將拆分後重複文件放在那
        
        '''
              
        with open(file_path, 'a') as file:
                                
            file.write("------------------------Header ---------------------\n")
            file.write(f"執行時間     :{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write(f"執行檔案     :{file_name}\n")                    
            file.write("--------------------Input Parameter ---------------------\n")           
            file.write(f"拆分Element :{split_element}\n")
            file.write(f"命名Key     :{child_nodes}\n")
            file.write(f"分隔符號    :{delimiter}\n")
            file.write(f"流水號選擇  :{sequence}\n")
            file.write("--------------------內容 ---------------------\n")
            
            for key, value in count_dict.items():
                if value >= 2:
                     # 將資料寫入文本文件
                    file.write(f"{key} 出現 {value} 次.\n")
            
            file.write("\n\n")       
            if os.name == 'nt' and open_file_boolean:
                
                os.startfile(file_path)