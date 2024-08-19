# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 14:11:21 2024

@author: a9037
"""
import xml.etree.ElementTree as ET
import os


def run(before_file, after_file, tag_file):
    before_tree = ET.parse(before_file)
    before_root = before_tree.getroot()
    
    after_tree = ET.parse(after_file)
    after_root = after_tree.getroot()
    
    
    with open(tag_file, 'r', encoding='utf-8') as f:
        for line in f:
            find_a_tag(before_root, after_root, line)
            
def find_a_tag(before_root, after_root, tag):
    tag_path = ".//" + tag.strip("<>").replace(">/<", "/")
    tag_path = tag_path.replace(before_root.tag, "")   
    tag_path = tag_path.replace("///","//")
    
    def get_tag_info(root, tag_path):
        tag_info_list = []
        elements = root.findall(tag_path)
        for element in elements:
            name = element.tag
            attributes = element.attrib
            text = element.text.strip() if element.text else ''
            
            
            def build_paths(element, current_path):
                paths = []
                if element.tag == name:
                    paths.append(current_path)
                for index, child in enumerate(element):
                    child_path = f"{current_path}/{child.tag}[{index}]"
                    paths.extend(build_paths(child, child_path))
                return paths
            
            initial_path = f"{root.tag}"
            paths = build_paths(root, initial_path)
            
            tag_info_list.append({
                'name': name,
                'attributes': attributes,
                'text': text,
                'path': paths
            })
        return tag_info_list
    

    # 从根元素开始构建路径
    
    
    print(tag, tag_path)
    before_tag_info = get_tag_info(before_root, tag_path)
    after_tag_info = get_tag_info(after_root, tag_path)
    
    print(before_tag_info)
    print(after_tag_info)
    
    
    
    
"""
 MAIN FUNCTION
"""    
file1 = r"C:\Users\a9037\OneDrive\文件\GitHub\XML-Compare-Tool\Before\before_split\AuthorOne_1980-01-01.xml"  
file2 = r"C:\Users\a9037\OneDrive\文件\GitHub\XML-Compare-Tool\After\after_split\AuthorOne_1980-01-01.xml"
tag_file = r"C:\Users\a9037\OneDrive\文件\GitHub\XML-Compare-Tool\Final\Compare_file_tag.txt"
    
run(file1, file2, tag_file)