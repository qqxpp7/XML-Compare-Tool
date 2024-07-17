import os
import re
import random
import tkinter as tk
import customtkinter as ctk
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
        self.child_nodes = set()
        self.filename_count = {}
        self.create_widgets()        

    def create_widgets(self):
        self.top_right_frame = ctk.CTkFrame(self)
        self.top_right_frame.pack(pady=5, padx=10, fill="x")

        self.middle_right_frame = ctk.CTkFrame(self)
        self.middle_right_frame.pack(pady=5, padx=10, fill="both", expand=True)
        
        self.bottom_right_frame = ctk.CTkFrame(self)
        self.bottom_right_frame.pack(pady=5, padx=10, fill="both", expand=True)
        '''
        右邊畫面分為上、中、下三個區域
        ''' 
        
        #右中左-中中-中右
        self.left_middle_right_frame = ctk.CTkFrame(self.middle_right_frame)
        self.left_middle_right_frame.pack(pady=5, padx=5, side="left", fill="both", expand=True)
        
        self.mid_middle_right_frame = ctk.CTkFrame(self.middle_right_frame)
        self.mid_middle_right_frame.pack(pady=5, padx=5, side="left", fill="both", expand=True)
        
        self.rig_middle_right_frame = ctk.CTkFrame(self.middle_right_frame)
        self.rig_middle_right_frame.pack(pady=5, padx=5, side="left", fill="both", expand=True)
        '''
        中間區域是展示檔案element、text的部分，也有分三個小視窗
        ''' 
        
        self.selected_option = tk.StringVar()
        self.selected_option.set("Select Folder")
        self.options = ["All", "Before", "After"]
        self.create_combobox()
        '''
        上區域會選擇從"All", "Before", "After"進行檔案分割
        ''' 
        
        self.ok_button = ctk.CTkButton(self.top_right_frame, text="拆分", command=self.split_xml)
        self.ok_button.grid(row=0, column=3, pady=10, padx=10, sticky="w")

        #右中左
        self.all_nodes_listbox = tk.Listbox(self.left_middle_right_frame, selectmode=tk.SINGLE)
        self.all_nodes_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.all_nodes_listbox.bind('<<ListboxSelect>>', self.on_node_select)
        '''
        中間區域的左邊是選擇key element的小視窗，所有key element都會秀出來
        ''' 

        # 右中間框架
        self.text_area = scrolledtext.ScrolledText(self.mid_middle_right_frame, wrap=tk.WORD, width=50, height=20)
        self.text_area.pack(fill=tk.BOTH, expand=True)
        '''
        中間區域的中間會秀出檔案的element及text
        ''' 
        
        #右中右
        self.option_listbox = tk.Listbox(self.rig_middle_right_frame)
        self.option_listbox.pack(fill=tk.BOTH, expand=True)
        '''
        中間區域的右邊會展示所選擇的key視窗
        ''' 
        
        self.add_button = ctk.CTkButton(self.rig_middle_right_frame, text="+", command=self.add_child_node)
        self.add_button.pack(side=tk.LEFT, pady=5)

        self.remove_button = ctk.CTkButton(self.rig_middle_right_frame, text="-", command=self.remove_child_node)
        self.remove_button.pack(side=tk.LEFT, pady=5)

        #右下
        self.split_element_entry = self.default_input(self.bottom_right_frame, 1, "拆分Element：", 400, "book")
        self.delimiter_entry = self.default_input(self.bottom_right_frame, 2, "分隔符號：", 200, "&")
        '''
        下面區域有預設值的拆分Element跟分隔符號的輸入框
        '''
        
        # 流水號標籤
        self.sequence_label = ctk.CTkLabel(self.bottom_right_frame, text="流水號：")
        self.sequence_label.grid(row=3, column=0, pady=10, padx=50, sticky="w")       
        # 流水號選項
        self.sequence_var = tk.StringVar(value="無")
        self.sequence_options = ctk.CTkSegmentedButton(
            master=self.bottom_right_frame,
            values=["前面", "後面", "無"],
            variable=self.sequence_var,)        
        self.sequence_options.grid(row=3, column=1, pady=10, padx=10, sticky="w")
        '''
        下面區域還有是否需要流水號的選項
        '''

    def create_combobox(self):
        combobox = ttk.Combobox(self.top_right_frame,
                                textvariable=self.selected_option,
                                values=self.options, state="readonly")
        combobox.grid(row=0, column=0, pady=10, padx=30)
        self.selected_option.trace("w", self.on_dropdown_select)
        '''
        上面區域選擇從"All", "Before", "After"進行檔案分割的combobox建立
        ''' 
    
    def default_input(self, frame, row, label_text, entry_width, default_text):
        label = ctk.CTkLabel(self.bottom_right_frame, text=label_text, anchor="w")
        label.grid(row=row, column=0, pady=10, padx=50, sticky="w")
        entry = ctk.CTkEntry(self.bottom_right_frame, width=entry_width)
        entry.grid(row=row, column=1, sticky="w")
        entry.insert(0, default_text) # 預設 xml
        return entry

    def create_valid_filename(self, text):
        return re.sub(r'[^\w\-_\.]', '', text)
    '''
    使用正則表達式移除或替換檔案名中的非法字符
    '''
    def random_load_xml_file(self, path):
        files = [f for f in os.listdir(path) if f.endswith('.xml')]
        if not files:
            return None
        return os.path.join(path, random.choice(files))
    '''
    載入選定資料夾內的隨機一個xml檔案
    '''
    
    def load_xml_files(self, path):
        files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.xml')]
        return files
    '''
    載入選定資料夾內的所有xml檔案
    '''

    def on_dropdown_select(self, *args):
        self.before_path = shared_data.before_path.get()
        self.after_path = shared_data.after_path.get()
        # print(self.before_path,"%", self.after_path)
        selected_option = self.selected_option.get()  # 根據選擇的選項來設置資料夾路徑
        if selected_option == "All":
            folder_path = self.before_path
            # print(selected_option, "+", folder_path)
        elif selected_option == "Before":
            folder_path = self.before_path
            # print(selected_option, "+",folder_path)
        elif selected_option == "After":
            folder_path = self.after_path
            # print(selected_option, "+", folder_path)
        else:
            folder_path = None
        
        if folder_path:
            self.file_path = self.random_load_xml_file(folder_path)
            self.all_file_path = self.load_xml_files(folder_path)        
        if self.file_path:
            self.load_xml_content([self.file_path])
            # self.display_xml_content([self.file_path])
            print("******on dropdown select*****")
            print(self.file_path)
            print(self.all_file_path)
    '''
    選擇All的時候會隨機選擇before或after路徑，選好資料夾後會跳到load_xml_file隨機選擇一個檔案
    選好檔案路徑後再透過display_xml_content展示檔案內容
    '''
    
    def load_xml_content(self, file_paths):
        if not file_paths:
            return
        global tree, root_element
        tree = ET.parse(file_paths[0])
        self.root_element = tree.getroot()
        self.populate_all_nodes_list()
        self.display_xml_content()

    def populate_all_nodes_list(self):
        all_possible_nodes = {child.tag for child in self.root_element.iter()}
        for node in all_possible_nodes:
            self.all_nodes_listbox.insert(tk.END, node)    
    '''
    透過display_xml_content進行呼叫，傳入剛剛xml檔案的路徑，分析檔案的樹架構
    '''        
    
    def display_xml_content(self, file_paths=None):
        self.text_area.delete('1.0', tk.END)
        # self.load_xml_content(file_paths)
        print("file_paths?????")
        print(file_paths)
        
        def display_node(node, indent=""):
                if node.tag in self.child_nodes or not self.child_nodes:
                    self.text_area.insert(tk.END, f"{indent}{node.tag}: {node.text.strip() if node.text and node.text.strip() else ''}\n")               
                for child in node:
                    display_node(child, indent + "    ")

        display_node(self.root_element)

    def on_node_select(self, event):
        widget = event.widget
        selection = widget.curselection()
        if selection:
            index = selection[0]
            node = widget.get(index)
            if node in self.child_nodes:
                self.child_nodes.remove(node)
                widget.itemconfig(index, {'bg':'white'})
            else:
                self.child_nodes.add(node)
                widget.itemconfig(index, {'bg':'yellow'})
            self.update_option_list()

    def add_child_node(self):
        if len(self.child_nodes) > 5:
            messagebox.showinfo("Error", "You can select no more than 5 items.")
            return
        self.update_option_list()

    def remove_child_node(self):
        selection = self.option_listbox.curselection()
        if selection:
            index = selection[0]
            node = self.option_listbox.get(index)
            self.child_nodes.discard(node)
            self.option_listbox.delete(index)
        self.update_option_list()

    def update_option_list(self):
        self.option_listbox.delete(0, tk.END)
        for node in self.child_nodes:
            self.option_listbox.insert(tk.END, node)
        print("--------update option list--------")
        self.display_xml_content([self.file_path])

    def split_xml(self):
        if not self.child_nodes:
            messagebox.showinfo("Error", "Please select at least one child node.")
            return
        selected_option = self.selected_option.get()  # 根據選擇的選項來設置資料夾路徑
        if selected_option == "All":
            for file in self.all_file_path:
                self.save_books_from_xml(self.all_file_path, self.delimiter_entry.get(), list(self.child_nodes), self.split_element_entry.get(), shared_data.before_path)
                self.save_books_from_xml(self.all_file_path, self.delimiter_entry.get(), list(self.child_nodes), self.split_element_entry.get(), shared_data.before_path)
        else:
            for file in self.all_file_path:
                self.save_books_from_xml(self.all_file_path, self.delimiter_entry.get(), list(self.child_nodes), self.split_element_entry.get(), self.folder_path)
        messagebox.showinfo("Success", "XML split successfully!")
            
    def save_books_from_xml(self, xml_path, node_name, child_nodes, split_character, base_folder):
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
            serial_number = 2
            
            while filename in self.filename_count:
                if self.sequence_var.get() == "前面":
                    filename = f"{serial_number}{split_character}{original_filename}"
                elif self.sequence_var.get() == "後面":
                    filename = f"{original_filename[:-4]}{split_character}{serial_number}.xml"
                else:
                    filename = original_filename  # 無序號選擇
                serial_number += 1
            
            self.filename_count[filename] = 1
            node_tree = ET.ElementTree(node)
            
            # Save in the specified folder
            output_folder = os.path.join(base_folder, filename)
            os.makedirs(os.path.dirname(output_folder), exist_ok=True)
            node_tree.write(output_folder)
            print(f"File saved: {output_folder}")

            if serial_number > 2:
                print(f"Warning: Duplicate filename detected：'{original_filename}'")
