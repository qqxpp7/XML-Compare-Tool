# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 15:33:14 2024

@author: a9037
"""

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
                       
            b_count = get_attribute(before_root, tag_path1, tag_path2)
            a_count = get_attribute(after_root, tag_path1, tag_path2)
            
            if max(len(b_count), len(a_count)) == 1:
                compare_a_key(b_count[0][4], a_count[0][4], tag_path2)
            else:                
                #b_count,a_count --> [0]是index，[1]是key，[2]是element
                # 找出 list1 中不存在於 list2 中的項目               
                not_in_after = []
                for b in b_count:
                    lv_flag = False
                    for a in a_count:
                        
                        # if lv_flag: continue
                        # print('->', b[5], '-->', a[5])
                        if b[5] == a[5]: #key相等，對比底下所有的子element 

                            differences = compare_same_key_child(b[4], a[4])                            
                            for diff in differences:
                                print(f"Line {diff[0]}:")
                                print(f"before: {diff[1]} ")
                                print(f"after: {diff[2]}")
                                print("")
                            lv_flag = True  
                            break
                        
                        
                    if lv_flag == False:
                        not_in_after.append([b[3], "delete", len(b[4])])
                
                # 找出 list2 中不存在於 list1 中的項目
                not_in_before = []
                for a in a_count:
                    lv_flag_2 = False
                    for b in b_count:
                    
                        if a[5] == b[5]:
                            lv_flag_2 = True
                            break
                                                    
                    if lv_flag_2 == False:    
                        not_in_before.append([a[3],"insert", len(a[4])])              
                    
                print(f"before有after沒有：{not_in_after}")
                print(f"before沒有after有：{not_in_before}")

def get_attribute(lv_root, lv_parent_tag, lv_tag):
    """
    lv_root: 根結點
    lv_parent_tag: 父標籤
    lv_tag: 目標標籤
    
    """
    stack = [(lv_root, "", 0, None)]  # 初始化堆疊時，根節點索引設定為0。
    results = []
    
    while stack:
        node, current_path, index, parent_tag = stack.pop()  # 從堆疊中彈出一個元素
        current_path += f'/{node.tag}[{index}]'  # 根節點的路徑更新，不顯示索引

        # 檢查當前節點是否符合特定條件
        if node.tag == lv_tag  and parent_tag == lv_parent_tag:
            values = [child.text for child in list(node)[:5]]
            joined_values = '_'.join(values) 
            results.append([node.tag, node.attrib, node.text.strip(), current_path, node, joined_values])  # 符合條件，加入結果列表

        # 將所有子節點加入堆疊，注意逆序添加以保持正確的處理順序
        for i in reversed(range(len(node))):
            stack.append((node[i], current_path, i, node.tag))

    return results


def compare_a_key(before_tag, after_tag, tag_name):
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
            
def compare_same_key_child(before_tag, after_tag):
    '''
    先確定行數相同，以便逐行比較
    當行數有差異時，空的那邊為""
    將element不相等的存在differences並回傳
    '''
    differences = []

    if len(before_tag) == len(after_tag): #相同element的子element數量一樣
        for i in range(len(before_tag)):
            if before_tag[i].tag != after_tag[i].tag :
                print(f"tag不相等 :{before_tag[i].tag} vs {after_tag[i].tag}")
                differences.append((i+1, before_tag[i], after_tag[i]))
                print('->', before_tag[i].tag, after_tag[i].tag)
                
            if before_tag[i].attrib != after_tag[i].attrib :
                print(f"attribute不相等:{before_tag[i].attrib} vs {after_tag[i].attrib}")
                differences.append((i+1, before_tag[i].attrib, after_tag[i].attrib))
                
            if before_tag[i].text != after_tag[i].text :
                print(f"text不相等:{before_tag[i].text} vs {after_tag[i].text}")
                differences.append((i+1, before_tag[i].text, after_tag[i].text ))
                
    else:#相同element的子element數量不一樣！！   
        min_lines = min(len(before_tag), len(after_tag))
        for i in range(min_lines):
            if not compare_same_key_child(before_tag[i], after_tag[i]):
                continue
            
        if len(before_tag) > len(after_tag):
            for i in range(min_lines, len(before_tag)):
                print(f"刪除： {before_tag.tag}/{ET.tostring(before_tag[i], encoding='unicode').strip()}")
                differences.append((i+1, before_tag[i].tag, ""))
        elif len(after_tag) > len(before_tag):
            for i in range(min_lines, len(after_tag)):
                print(f"新增: {after_tag.tag}/{ET.tostring(after_tag[i], encoding='unicode').strip()}")
                differences.append((i+1, "", after_tag[i].tag))

    return differences
                
"""
 MAIN FUNCTION
"""    
file1 = r"C:\Users\a9037\OneDrive\文件\GitHub\XML-Compare-Tool\Before\before_split\AuthorOne_1980-01-01.xml"  
file2 = r"C:\Users\a9037\OneDrive\文件\GitHub\XML-Compare-Tool\After\after_split\AuthorOne_1980-01-01.xml"
tag_file = r"C:\Users\a9037\OneDrive\文件\GitHub\XML-Compare-Tool\Final\Compare_file_tag.txt"
    
main(file1, file2, tag_file)