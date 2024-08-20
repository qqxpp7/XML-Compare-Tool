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
            
            
            b_count = count_a_tag_method(before_root, tag_path1, tag_path2)
            a_count = count_a_tag_method(after_root, tag_path1, tag_path2)
            
            max_count = max(b_count, a_count)
            
            if max_count == 1:
                b_return = find_a_tag_method(before_root, tag_path1, tag_path2, '')
                a_return = find_a_tag_method(after_root, tag_path1, tag_path2, '')
                compare(b_return, a_return, tag_path2)
            else:
                find_same_tag_method(before_root, tag_path1, tag_path2)
                
                
def count_a_tag_method(node, find_parent_tag, find_child_tag, parent_tag=None):
    count = 0
    if node.tag == find_child_tag and parent_tag == find_parent_tag:
        count += 1
         
    for i, child in enumerate(node):        
        count += count_a_tag_method(child, find_parent_tag, find_child_tag, parent_tag = node.tag)
        
    return count            
                                       
def find_a_tag_method(node, find_parent_tag, find_child_tag, current_path, index=0, parent_tag=None):
    """
    only can find a tag in 1 time
    """
    current_path += f'/{node.tag}[{index}]'

    if node.tag == find_child_tag and parent_tag == find_parent_tag:
        return([node.tag, node.attrib, node.text.strip(), current_path])
         
    for i, child in enumerate(node):        
        result = find_a_tag_method(child, find_parent_tag, find_child_tag, current_path, i, parent_tag = node.tag)
        if result:
            return result
        
    return None

def find_same_tag_method(node, find_parent_tag, find_child_tag):
    """
    find a tag at least 2 times
    """
    if node.tag == find_parent_tag:
        for child_tag in node.findall(find_child_tag):
            values = [child.text for child in list(child_tag)[:3]]
            print(f'Book ID {child_tag.get("id")}:', values)   
    else:        
        for parent_tag in node.findall('.//find_parent_tag'):
            for child_tag in parent_tag.findall(find_child_tag):
                values = [child.text for child in list(child_tag)[:3]]
                print(f'Book ID {child_tag.get("id")}:', values)



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