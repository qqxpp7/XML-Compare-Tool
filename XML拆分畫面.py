import tkinter as tk
import customtkinter as ctk
import re
from tkinter import scrolledtext, messagebox
import xml.etree.ElementTree as ET

def load_xml_content():
    global tree, root_element
    tree = ET.parse(file_path)
    root_element = tree.getroot()
    populate_all_nodes_list()
    display_xml_content()

def populate_all_nodes_list():
    all_possible_nodes = {child.tag for child in root_element.iter()}
    for node in all_possible_nodes:
        all_nodes_listbox.insert(tk.END, node)

def display_xml_content():
    text_area.delete('1.0', tk.END)

    def display_node(node, indent=""):
        if node.tag in child_nodes or not child_nodes:
            text_area.insert(tk.END, f"{indent}{node.tag}: {node.text.strip() if node.text and node.text.strip() else 'No content'}\n")
        for child in node:
            display_node(child, indent + "    ")

    display_node(root_element)

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
    save_books_from_xml(file_path, 'book', list(child_nodes), '_')
    messagebox.showinfo("Success", "XML split successfully!")

def create_valid_filename(text):
    return re.sub(r'[^\w\-_\.]', '', text)

def save_books_from_xml(xml_path, node_name, child_nodes, split_character):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    filename_count = {}

    nodes = [root] if root.tag == node_name else root.findall('.//' + node_name)
    
    for node in nodes:
        elements = {}
        for child in child_nodes:
            element = node.find('.//' + child)
            if element is not None:
                elements[child] = create_valid_filename(element.text)

        filename_elements = [elements[key] for key in child_nodes if key in elements]
        filename = split_character.join(filename_elements) + ".xml"
        original_filename = filename
        serial_number = 1
        
        while filename in filename_count:
            filename = f"{original_filename[:-4]}_{serial_number}.xml"
            serial_number += 1
        
        filename_count[filename] = 1
        node_tree = ET.ElementTree(node)
        node_tree.write(filename)
        print(f"File saved: {filename}")

        if serial_number > 1:
            print(f"Warning: Duplicate filename detected. '{original_filename}' has been renamed to '{filename}' to avoid overwriting.")

# 創建主窗口
root = ctk.CTk()
root.title("XML Viewer")

# 左側框架
left_frame = ctk.CTkFrame(root)
left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

add_button = ctk.CTkButton(left_frame, text="+", command=add_child_node)
add_button.pack(side=tk.TOP, pady=5)

remove_button = ctk.CTkButton(left_frame, text="-", command=remove_child_node)
remove_button.pack(side=tk.TOP, pady=5)

all_nodes_listbox = tk.Listbox(left_frame, selectmode=tk.SINGLE)
all_nodes_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
all_nodes_listbox.bind('<<ListboxSelect>>', on_node_select)

child_nodes = set()

# 中間框架
middle_frame = ctk.CTkFrame(root)
middle_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

text_area = scrolledtext.ScrolledText(middle_frame, wrap=tk.WORD, width=60, height=20)
text_area.pack(fill=tk.BOTH, expand=True)

# 右側框架
right_frame = ctk.CTkFrame(root)
right_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

middle_right_left_frame = ctk.CTkFrame(right_frame)
middle_right_left_frame.pack(pady=5, padx=5, fill="x")

middle_right_mid_frame = ctk.CTkFrame(right_frame)
middle_right_mid_frame.pack(pady=5, padx=5, fill="both", expand=True)

middle_right_rig_frame = ctk.CTkFrame(right_frame)
middle_right_rig_frame.pack(pady=5, padx=5, fill="both", expand=True)

option_listbox = tk.Listbox(middle_right_left_frame)
option_listbox.pack(fill=tk.BOTH, expand=True)

ok_button = ctk.CTkButton(middle_right_rig_frame, text="OK", command=split_xml)
ok_button.pack(side=tk.BOTTOM, pady=10)

# 加載 XML 文件
file_path = 'C:/Users/a9037/OneDrive/文件/XML_compare/After/123.xml'
load_xml_content()

root.mainloop()
