import xml.etree.ElementTree as ET
import re
import os
import random

def create_valid_filename(text):
    # 使用正則表達式移除或替換檔案名中的非法字符
    return re.sub(r'[^\w\-_\.]', '', text)

def random_load_xml_file(path):
    files = [f for f in os.listdir(path) if f.endswith('.xml')]
    if not files:
        return None
    return os.path.join(path, random.choice(files))

def load_xml_files(path):
    # List all files that end with '.xml' in the specified directory
    files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.xml')]
    return files

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
# Global dictionary to keep track of filename occurrences
filename_count = {}
# Example usage
folder_path = 'C:/Users/a9037/OneDrive/文件/XML_compare/After'
file_path = load_xml_files(folder_path)
node_name = 'book'
child_nodes = ['name', 'birthdate']  # Add other child nodes as needed
split_character = '&'
for file in file_path:
    print(file)
    save_books_from_xml(file, node_name, child_nodes,split_character)
