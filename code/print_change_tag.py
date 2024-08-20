# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 16:47:49 2024

@author: a9037
"""


import xml.etree.ElementTree as ET

def main(before_file, after_file, tag_file):
    before_tree = ET.parse(before_file)
    before_root = before_tree.getroot()
    
    after_tree = ET.parse(after_file)
    after_root = after_tree.getroot()
    
    with open(tag_file, 'r', encoding='utf-8') as f:
        for line in f:
            tag_path1, tag_path2 = line.strip("<>\n").replace(">/<", "/").split('/')
            
            b_return = find_a_tag_method(before_root, tag_path1, tag_path2, '')
            a_return = find_a_tag_method(after_root, tag_path1, tag_path2, '')
            compare(b_return, a_return, tag_path2)
            
                                       
def find_a_tag_method(node, find_parent_tag, find_child_tag, current_path, index=0, parent_tag=None):
    """
    only can find a tag in 1 times
    """
    current_path += f'/{node.tag}[{index}]'

    if node.tag == find_child_tag and parent_tag == find_parent_tag:
        return([node.tag, node.attrib, node.text.strip(), current_path])
         
    for i, child in enumerate(node):        
        result = find_a_tag_method(child, find_parent_tag, find_child_tag, current_path, i, parent_tag = node.tag)
        if result:
            return result
        
    return None

def compare(before_tag, after_tag, tag_name):
    '''
    當before_tag不為空，after_tag為空，則是刪除
    當before_tag為空，after_tag不為空，則是新增
    
    '''
    if before_tag != None and after_tag == None:
        delete_tag = []
        delete_tag.append(f"{tag_name}")
        print(f"delete:{delete_tag}")
    elif before_tag == None and after_tag != None:
        insert_tag = []
        insert_tag.append(f"{tag_name}")
        print(f"insert:{insert_tag}")
    else:
        attribute_change = []
        text_change = []
        place_change = []
        
        if before_tag[1] != after_tag[1]:
            attribute_change.append(f"{tag_name}")
        if before_tag[2] != after_tag[2]:
            text_change.append(f"{tag_name}")
        if before_tag[3] != after_tag[3]:
            place_change.append(f"{tag_name}")
"""
 MAIN FUNCTION
"""    
file1 = r"C:\Users\a9037\OneDrive\文件\GitHub\XML-Compare-Tool\Before\before_split\AuthorOne_1980-01-01.xml"  
file2 = r"C:\Users\a9037\OneDrive\文件\GitHub\XML-Compare-Tool\After\after_split\AuthorOne_1980-01-01.xml"
tag_file = r"C:\Users\a9037\OneDrive\文件\GitHub\XML-Compare-Tool\Final\Compare_file_tag.txt"
    
main(file1, file2, tag_file)