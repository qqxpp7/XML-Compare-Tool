# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 09:46:47 2024

@author: a9037
"""

import os
import time
from lxml import etree
from pathlib import Path
from datetime import datetime
import xml.etree.ElementTree as ET
from collections import defaultdict


def read_exclude_tags(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    exclude_tags = [line.strip() for line in lines]
    print("exclude_tags: ", exclude_tags)
    return exclude_tags

def clean_tag(tag):
    return tag.strip('<>')

def remove_excluded_tags(root, exclude_tags):
    for tag_path in exclude_tags:
        parent_tag, child_tag = map(clean_tag, tag_path.split('/'))
        if parent_tag == root.tag:
            parents = [root]
        else:
            parents = root.findall(f'.//{parent_tag}')
        for parent in parents:
            for child in parent.findall(child_tag):
                parent.remove(child)
    return root

def get_filtered_xml_content(xml_path, exclude_tags):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    root = remove_excluded_tags(root, exclude_tags)
    # print("root: ", ET.tostring(root, encoding='unicode'))
    return ET.tostring(root, encoding='unicode')

def compare_elements(element1, element2, path=''):
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
            sub_changes = compare_elements(child1, child2, path=f'{path}/{element1.tag}')
            changes.extend(sub_changes)
    
    return changes


def compare_xml_files(folder1, folder2, exclude_tags):
    folder1 = Path(folder1)
    folder2 = Path(folder2)
    
    results = []
    matches = []
    
    for file1 in folder1.glob('*.xml'):
        file2 = folder2 / file1.name
        if file2.exists():
            content1 = get_filtered_xml_content(file1, exclude_tags)
            content2 = get_filtered_xml_content(file2, exclude_tags)
            
            root1 = ET.fromstring(content1)
            root2 = ET.fromstring(content2)
            
            if content1 == content2:
                matches.append((file1.name, '固定element內容都相同'))
            else:
                changes = compare_elements(root1, root2)
                results.append((file1.name, 'Different', changes))
        else:
            results.append((file1.name, 'Missing in folder2'))
    
    return results, matches
            


def print_fixedtag_file(file_path, exclude_tags, file_name, results, matches):
    
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
        file.write(f"忽略Element :{exclude_tags}\n")
        file.write("--------------------內容 ---------------------\n")
        
        for res in results:
            file.write(f"File: {res[0]}, Result: {res[1]}\n")
            if res[1] == 'Different':
                for change in res[2]:
                    file.write(f" - {change}\n")
        
        for match in matches:
            file.write(f"File: {match[0]}, Result: {match[1]}\n")
        
        file.write("\n\n")
    
    if os.name == 'nt':
        os.startfile(file_path)
        
# Example usage:
exclude_tags = read_exclude_tags(r"C:\Users\a9037\OneDrive\文件\GitHub\XML-Compare-Tool\Final\Compare_file_tag.txt")
before_path = r"C:\Users\a9037\OneDrive\文件\GitHub\XML-Compare-Tool\Before\before_split"
after_path = r"C:\Users\a9037\OneDrive\文件\GitHub\XML-Compare-Tool\After\after_split"

current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
fixed_tag_new_folder = os.path.join(r"C:\Users\a9037\OneDrive\文件\GitHub\XML-Compare-Tool\Final", "fixed_tag_report")
os.makedirs(fixed_tag_new_folder, exist_ok=True)
report_name = "fixed_tag_" + current_time + '.txt'
file_path = os.path.join(fixed_tag_new_folder, report_name)

results, matches = compare_xml_files(before_path, after_path, exclude_tags)
print_fixedtag_file(file_path, exclude_tags, report_name, results, matches)


            

