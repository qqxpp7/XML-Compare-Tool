import customtkinter as ctk
from tkinter import ttk, scrolledtext, messagebox
import tkinter as tk
import os
import re
import random
import xml.etree.ElementTree as ET

# 創建主窗口
root = ctk.CTk()
root.title("XML Compare Tool")
root.geometry("1000x600")

"""
這是左邊功能列表
"""
# 功能列表
def on_function_button_click(function):
    selected_function.set(function)
    for widget in left_frame.winfo_children():
        if isinstance(widget, ctk.CTkButton) and widget.cget("text") in sum(categories.values(), []):
            widget.configure(fg_color="white", text_color="black")
    function_buttons[function].configure(fg_color="lightblue", text_color="black")

#建立左邊的功能列框架
left_frame = ctk.CTkFrame(root, width=200)
left_frame.pack(side="left", fill="y", padx=5, pady=10)

# 功能分類及功能列表
categories = {"":["搜尋"],
    "主功能": ["01 位置設定", "02 XML 拆分", "03 找出差異", "04 比對"],
    "其他功能": ["Copy 資料", "Element 分割"]
}

selected_function = tk.StringVar(value="02 XML 拆分")

function_buttons = {}
for category, functions in categories.items():
    if category:  # 如果類別有名稱，顯示類別標籤
        label = ctk.CTkLabel(left_frame, text=category, font=("Arial", 12, "bold"))
        label.pack(pady=5, anchor="center")
    for function in functions:
        button = ctk.CTkButton(left_frame, text=function, width=180, anchor="center", fg_color="white", text_color="black",
                               command=lambda f=function: on_function_button_click(f))
        button.pack(pady=5, anchor="center")
        function_buttons[function] = button
    # 根據類別新增分割線
    if category in ["", "主功能"]:
        line = ctk.CTkFrame(left_frame, height=2, fg_color="lightgray")
        line.pack(fill="x", pady=5)
        
# 設定初始選取項顏色為藍色
function_buttons["02 XML 拆分"].configure(fg_color="lightblue", text_color="black")

"""
以下為右邊畫面
"""
# 建立右邊的顯示框架
right_frame = ctk.CTkFrame(root)
right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=10)

# 右上
top_right_frame = ctk.CTkFrame(right_frame)
top_right_frame.pack(pady=5, padx=10, fill="x", expand=0)
# 右中
middle_right_frame = ctk.CTkFrame(right_frame)
middle_right_frame.pack(pady=5, padx=10, fill="both", expand=True)

# 右下
bottom_right_frame = ctk.CTkFrame(right_frame)
bottom_right_frame.pack(pady=5, padx=10, fill="both", expand=0)

#右中左-中中-中右
left_middle_right_frame = ctk.CTkFrame(middle_right_frame)
left_middle_right_frame.pack(pady=5, padx=5, side="left",fill="both", expand=True)
mid_middle_right_frame = ctk.CTkFrame(middle_right_frame)
mid_middle_right_frame.pack(pady=5, padx=5,side="left" ,fill="both", expand=True)
rig_middle_right_frame = ctk.CTkFrame(middle_right_frame)
rig_middle_right_frame.pack(pady=5, padx=5,side="left",fill="both" , expand=True)
# 初始化變數
before_button_var = tk.IntVar(value=1)
after_button_var = tk.IntVar(value=1)

# 新增預設輸入框 
def default_input(frame, row, label_text, entry_width,default_text):
    label = ctk.CTkLabel(bottom_right_frame, text=label_text, anchor="w")
    label.grid(row=row, column=0, pady=10, padx=50, sticky="w")
    entry = ctk.CTkEntry(bottom_right_frame, width=entry_width)
    entry.grid(row=row, column=1, sticky="w")
    entry.insert(0, default_text) # 預設 xml
    return entry
def create_valid_filename(text):
    # 使用正則表達式移除或替換檔案名中的非法字符
    return re.sub(r'[^\w\-_\.]', '', text)

def load_xml_file(path):
    files = [f for f in os.listdir(path) if f.endswith('.xml')]
    if not files:
        return None
    return os.path.join(path, random.choice(files))

def on_dropdown_select(*args):
    folder_path = selected_option.get()  # 根據選擇的選項來設置資料夾路徑
    if folder_path == "All":
        folder_path = random.choice(["Before", "After"])
    file_path = load_xml_file(folder_path)
    if file_path:
        display_xml_content(file_path)
        
def load_xml_content(file_paths):
    global tree, root_element
    if not file_paths:
        return
    tree = ET.parse(file_paths[0])
    root_element = tree.getroot()
    populate_all_nodes_list()
    display_xml_content()

def populate_all_nodes_list():
    all_possible_nodes = {child.tag for child in root_element.iter()}
    for node in all_possible_nodes:
        all_nodes_listbox.insert(tk.END, node)

def display_xml_content(file_paths=None):
    text_area.delete('1.0', tk.END)
    if not file_paths:
        return

    for file_path in file_paths:
        tree = ET.parse(file_path)
        root_element = tree.getroot()

        def display_node(node, indent=""):
            if node.tag in child_nodes or not child_nodes:
                text_area.insert(tk.END, f"{indent}{node.tag}: {node.text.strip() if node.text and node.text.strip() else 'No content'}\n")
            for child in node:
                display_node(child, indent + "    ")

        display_node(root_element)
        text_area.insert(tk.END, "\n")
        
def on_node_select(event):
    widget = event.widget
    selection = widget.curselection()
    if selection:
        index = selection[0]
        node = widget.get(index)
        if node in child_nodes:
            child_nodes.remove(node)
            widget.itemconfig(index, {'bg':'white'})
        else:
            child_nodes.add(node)
            widget.itemconfig(index, {'bg':'yellow'})
        update_option_list()

def add_child_node():
    if len(child_nodes) > 5:
        messagebox.showinfo("Error", "You can select no more than 5 items.")
        return
    update_option_list()

def remove_child_node():
    selection = option_listbox.curselection()
    if selection:
        index = selection[0]
        node = option_listbox.get(index)
        child_nodes.discard(node)
        option_listbox.delete(index)
    update_option_list()

def update_option_list():
    option_listbox.delete(0, tk.END)
    for node in child_nodes:
        option_listbox.insert(tk.END, node)
    display_xml_content()

def split_xml():
    if not child_nodes:
        messagebox.showinfo("Error", "Please select at least one child node.")
        return
    save_books_from_xml(file_path, delimiter_entry, list(child_nodes), split_element_entry)
    messagebox.showinfo("Success", "XML split successfully!")
        
def create_combobox():
    combobox = ttk.Combobox(top_right_frame, textvariable=selected_option, values=options)
    combobox.grid(row=0, column=0, pady=10, padx=30)
    selected_option.trace("w", on_dropdown_select)
    
def save_books_from_xml(xml_path, node_name, child_nodes, split_character):
    # Load the XML file
    tree = ET.parse(xml_path)
    root = tree.getroot()
    nodes = [root] if root.tag == node_name else root.findall('.//' + node_name)
    
    for node in nodes:
        elements = {}
        for child in child_nodes:
            element = node.find('.//' + child)
            if element is not None:
                elements[child] = create_valid_filename(element.text)

        # Create filename based on the elements
        filename_elements = [elements[key] for key in child_nodes if key in elements]
        filename = split_character.join(filename_elements) + ".xml"
        original_filename = filename
        serial_number = 2
        
        while filename in filename_count:
            filename = f"{original_filename[:-4]}{split_character}{serial_number}.xml"
            serial_number += 1
        
        filename_count[filename] = 1
        node_tree = ET.ElementTree(node)
        node_tree.write(filename)
        print(f"File saved: {filename}")

        if serial_number > 2:
            print(f"Warning: Duplicate filename detected. '{original_filename}' has been renamed to '{filename}' to avoid overwriting.")    

# 下拉式選單的選項
options = ["All", "Before", "After"]
selected_option = tk.StringVar()
selected_option.set(options[0])
create_combobox()
# Global dictionary to keep track of filename occurrences
filename_count = {}
ok_button = ctk.CTkButton(top_right_frame, text="拆分", command=split_xml)
ok_button.grid(row=0, column=3, pady=10, padx=10, sticky="w")

#右中左
all_nodes_listbox = tk.Listbox(left_middle_right_frame, selectmode=tk.SINGLE)
all_nodes_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
all_nodes_listbox.bind('<<ListboxSelect>>', on_node_select)

child_nodes = set()

# 右中間框架
text_area = scrolledtext.ScrolledText(mid_middle_right_frame, wrap=tk.WORD, width=50, height=20)
text_area.pack(fill=tk.BOTH, expand=True)

#右中右
option_listbox = tk.Listbox(rig_middle_right_frame)
option_listbox.pack(fill=tk.BOTH, expand=True)

add_button = ctk.CTkButton(rig_middle_right_frame, text="+", command=add_child_node)
add_button.pack(side=tk.LEFT, pady=5)

remove_button = ctk.CTkButton(rig_middle_right_frame, text="-", command=remove_child_node)
remove_button.pack(side=tk.LEFT, pady=5)

#右下
split_element_entry = default_input(bottom_right_frame, 1, "拆分Element：", 400, "ns0:abap")
delimiter_entry = default_input(bottom_right_frame, 2, "分隔符號：", 200, "&")

# 流水號標籤
sequence_label = ctk.CTkLabel(bottom_right_frame, text="流水號：")
sequence_label.grid(row=3, column=0, pady=10, padx=50, sticky="w")
# 流水號選項
sequence_var = tk.StringVar(value="無")
sequence_options = ctk.CTkSegmentedButton(
    master=bottom_right_frame,
    values=["前面", "後面", "無"],
    variable=sequence_var,
)
sequence_options.grid(row=3, column=1, pady=10, padx=10, sticky="w")

#啟動主循環
root.mainloop()
