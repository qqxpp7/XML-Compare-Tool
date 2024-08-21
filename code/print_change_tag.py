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
                b_plural_tag = find_same_tag_method(before_root, tag_path1, tag_path2, '')
                a_plural_tag = find_same_tag_method(after_root, tag_path1, tag_path2, '')
                
                #[0]是index，[1]是key，[2]是element，[3]是路徑
                # 找出 list1 中不存在於 list2 中的項目               
                not_in_after = []
                for b in b_plural_tag:
                    for a in a_plural_tag:
                        if b[1] == a[1]: #key相等，對比底下所有的子element     
                            differences = compare_same_key_child(b[2], a[2])
                            for diff in differences:
                                print(f"Line {diff[0]}:")
                                print(f"Tag 1: {diff[1]} ")
                                # print(f"before path: {b[3]} ")
                                print(f"Tag 2: {diff[2]}")
                                # print(f"after path: {a[3]}")
                                print("")

                        else:
                            not_in_after.append(b[:2])
                
                # 找出 list2 中不存在於 list1 中的項目
                not_in_before = []
                for a in a_plural_tag:
                    for b in b_plural_tag:
                        if a[1] != b[1]:
                            not_in_before.append(a[:2])              
                    
                print(f"before有after沒：{not_in_after}")
                print(f"before沒after有：{not_in_before}")

def compare_same_key_child(before_tag, after_tag):
    '''
    確定行數較多的tag，以便逐行比較
    當行數有差異時，空的那邊為""
    將element不相等的存在differences並回傳
    '''
    differences = []

    if len(before_tag) == len(after_tag): #相同element的子element數量一樣
        for i in range(len(before_tag)):
            if before_tag[i].tag != after_tag[i].tag :
                print(f"tag不相等:{before_tag[i].tag} vs {after_tag[i].tag}")
                differences.append((i+1, before_tag[i], after_tag[i]))
                print('->', before_tag[i], after_tag[i])
                
            if before_tag[i].attrib != after_tag[i].attrib :
                print(f"attribute不相等:{before_tag[i].attrib} vs {after_tag[i].attrib}")
                differences.append((i+1, before_tag[i], after_tag[i]))
                
            if before_tag[i].text != after_tag[i].text :
                print(f"text不相等:{before_tag[i].text} vs {after_tag[i].text}")
                differences.append((i+1, before_tag[i], after_tag[i]))
                
    else:#相同element的子element數量不一樣！！   
        min_lines = min(len(before_tag), len(after_tag))
        for i in range(min_lines):
            if not compare_same_key_child(before_tag[i], after_tag[i]):
                continue
            
        if len(before_tag) > len(after_tag):
            for i in range(min_lines, len(before_tag)):
                print(f"刪除： {before_tag.tag}: {ET.tostring(before_tag[i], encoding='unicode').strip()}")
                differences.append((i+1, before_tag[i], ""))
        elif len(after_tag) > len(before_tag):
            for i in range(min_lines, len(after_tag)):
                print(f"新增: {after_tag.tag}: {ET.tostring(after_tag[i], encoding='unicode').strip()}")
                differences.append((i+1, "", after_tag[i]))

    return differences
                
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
        

def find_same_tag_method(node, find_parent_tag, find_child_tag, parent_path=""):
    """
    find a tag at least 2 times
    判斷find_parent_tag是不是根元素
    檢查find_child_tag是否有子元素
    再去抓取前5個子元素的text
    沒有子元素比對attribute及text
    """
    index = 0
    values_list = []
                
    if node.tag == find_parent_tag:
        for child_tag in node.findall(find_child_tag):
            if len(child_tag) > 0:
                values = [child.text for child in list(child_tag)[:5]]
                joined_values = '_'.join(values) 
                     
            else:
                attrs = '_'.join(f"{k}_{v}" for k, v in child_tag.attrib.items())
                text_value = child_tag.text if child_tag.text is not None else ""
                
                joined_values = f"{attrs}_{text_value}"  
                
            
            values_list.append([index, joined_values, child_tag]) 
            index += 1
        
    else:        
        for parent_tag in node.findall('.//' + find_parent_tag):
            for child_tag in parent_tag.findall(find_child_tag):
                if len(child_tag) > 0:
                    values = [child.text for child in list(child_tag)[:5]]
                    joined_values = '_'.join(values)       
                    
                else:
                    attrs = '_'.join(f"{k}_{v}" for k, v in child_tag.attrib.items())
                    text_value = child_tag.text if child_tag.text is not None else ""
                    joined_values = f"{attrs}_{text_value}"
                    
                values_list.append([index, joined_values, child_tag]) 
                index += 1  
            
    return values_list

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