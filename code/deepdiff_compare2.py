from deepdiff import DeepDiff
from datetime import datetime
from pprint import pprint
import xmltodict
import os
'''
增、刪、改可解決，有換位置就無法抓到(同一層)
相同tag換位置會視為修改text
'''

def find_diff(xml1_path, xml2_path):
    xml1_dict = xml_to_dict(xml1_path)
    xml2_dict = xml_to_dict(xml2_path)
    diff = DeepDiff(xml1_dict, xml2_dict, ignore_order=0)
    pprint (diff, indent = 2)
    return diff

def xml_to_dict(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        xml_content = file.read()
        return xmltodict.parse(xml_content)

def convert_path(path):
    return path.replace("][", "/").replace("[", "/").replace("]", "").replace("'", "")

def parse_diff(diff, xml1_dict, xml2_dict):
    explanations = []
    if 'values_changed' in diff:
        for key, details in diff['values_changed'].items():
            path = convert_path(key.split("root")[1])
            old_value = details['old_value']
            new_value = details['new_value']
            explanations.append(f"值變更於 {path}:\n從 '{old_value}' 改為 '{new_value}'。")
    if 'dictionary_item_removed' in diff:
        for key in diff['dictionary_item_removed']:
            path = convert_path(key.split("root")[1])  
            value = eval(f"xml1_dict{key.split('root')[1]}")
            explanations.append(f"刪除了元素於 {path}，值為：{value}。")
    if 'dictionary_item_added' in diff:
        for key in diff['dictionary_item_added']:
            path = convert_path(key.split("root")[1])  
            value = eval(f"xml2_dict{key.split('root')[1]}")
            explanations.append(f"新增了元素於 {path}，值為：{value}。")
    if 'iterable_item_removed' in diff:
        for key in diff['iterable_item_removed']:
            path = convert_path(key.split("root")[1])  
            value = eval(f"xml1_dict{key.split('root')[1]}")
            explanations.append(f"刪除了元素於 {path}，值為：{value}。")
    if 'iterable_item_added' in diff:
        for key in diff['iterable_item_added']:
            path = convert_path(key.split("root")[1])  
            value = eval(f"xml2_dict{key.split('root')[1]}")
            explanations.append(f"新增了元素於 {path}，值為：{value}。")
    if 'type_changes' in diff:
        for key, details in ensure_dict(diff['type_changes']).items():
            path = convert_path(key.split("root")[1]) 
            old_value = details['old_value']
            new_value = details['new_value']
            print(old_value, new_value)
            if details['old_type'] == list and details['new_type'] == dict:  
                removed_items = [k for k in old_value if k != new_value]
                explanations.append(f"刪除了元素於 {path}，值為：{removed_items}。")
                if new_value not in old_value:
                    added_items = new_value  
                    explanations.append(f"新增了元素於 {path}，值為：{added_items}。")
            elif details['old_type'] == dict and details['new_type'] == list:
                added_items = [k for k in new_value if k != old_value]
                explanations.append(f"新增了元素於 {path}，值為：{added_items}。")
                if old_value not in new_value:
                    removed_items = old_value 
                    explanations.append(f"刪除了元素於 {path}，值為：{removed_items}。")
        return explanations
    return explanations


def ensure_dict(items):
    if isinstance(items, dict):
        return items
    elif isinstance(items, list):
        result = {}
        for item in items:
            result.update(item)
        return result
    else:
        raise ValueError("Unexpected type for ensure_dict function")
        
xml1_path = r"C:\Users\a9037\OneDrive\文件\GitHub\XML-Compare-Tool\Before\before_split\AuthorOne_1980-01-01.xml"
xml2_path = r"C:\Users\a9037\OneDrive\文件\GitHub\XML-Compare-Tool\After\after_split\AuthorOne_1980-01-01.xml"

# 使用DeepDiff來比較兩個XML字典
diff_result = find_diff(xml1_path, xml2_path)
explanations = parse_diff(diff_result, xml_to_dict(xml1_path), xml_to_dict(xml2_path))

# 將結果保存到一個文本檔案中
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
repeat_new_folder = os.path.join(r"C:\Users\a9037\OneDrive\文件\GitHub\XML-Compare-Tool\Test", "diff_report")
os.makedirs(repeat_new_folder, exist_ok=True)
file_path = os.path.join(repeat_new_folder, f"diff_output_{current_time}.txt")
with open(file_path, "w", encoding="utf-8") as file:
    for explanation in explanations:
        file.write(explanation + "\n")