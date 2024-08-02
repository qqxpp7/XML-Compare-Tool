from deepdiff import DeepDiff
from datetime import datetime
from pprint import pprint
import xmltodict
import os


def find_diff(xml1_path, xml2_path):
    xml1_dict = xml_to_dict(xml1_path)
    xml2_dict = xml_to_dict(xml2_path)
    diff = DeepDiff(xml1_dict, xml2_dict, ignore_order=0)
    pprint(diff, indent=2)
    return diff

def xml_to_dict(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        xml_content = file.read()
        return xmltodict.parse(xml_content)

def parse_diff(diff, xml1_dict, xml2_dict):
    explanations = []
    if 'values_changed' in diff:
        explanations.extend(parse_values_changed(diff['values_changed']))
    if 'dictionary_item_removed' in diff:
        explanations.extend(parse_dict_items(diff['dictionary_item_removed'], xml1_dict, removed=True))
    if 'dictionary_item_added' in diff:
        explanations.extend(parse_dict_items(diff['dictionary_item_added'], xml2_dict, removed=False))
    if 'iterable_item_added' in diff:
        explanations.extend(parse_iterable_items(diff['iterable_item_added'], xml2_dict, added=True))
    if 'iterable_item_removed' in diff:
        explanations.extend(parse_iterable_items(diff['iterable_item_removed'], xml1_dict, added=False))
    if 'type_changes' in diff:
        explanations.extend(parse_type_changes(diff['type_changes']))
    return explanations

def parse_values_changed(values_changed):
    explanations = []
    for key, details in ensure_dict(values_changed).items():
        path = convert_path(key.split("root")[1])  # Extracts the path and converts format
        old_value = details['old_value']
        new_value = details['new_value']
        explanations.append(f"值變更於 {path}:\n從 '{old_value}' 改為 '{new_value}'。")
    return explanations

def parse_dict_items(items, xml_dict, removed):
    explanations = []
    for key in ensure_dict(items):
        path = convert_path(key.split("root")[1])  # Extracts the path and converts format
        value = eval(f"xml_dict{key.split('root')[1]}")
        if removed:
            explanations.append(f"刪除了元素於 {path}，值為：{value}。")
        else:
            explanations.append(f"新增了元素於 {path}，值為：{value}。")
    return explanations

def parse_iterable_items(items, xml_dict, added):
    explanations = []
    for key, value in ensure_dict(items).items():
        path = convert_path(key.split("root")[1])  # Extracts the path and converts format
        if added:
            explanations.append(f"新增了元素於 {path}，值為：{value}。")
        else:
            explanations.append(f"刪除了元素於 {path}，值為：{value}。")
    return explanations

def parse_type_changes(type_changes):
    explanations = []
    for key, details in ensure_dict(type_changes).items():
        path = convert_path(key.split("root")[1])  # Extracts the path and converts format
        old_type = details['old_type']
        new_type = details['new_type']
        old_value = details['old_value']
        new_value = details['new_value']
        if old_type == list and new_type == dict:
            removed_items = {str(k): old_value[k] for k in range(len(old_value)) if str(k) not in new_value}
            explanations.append(f"刪除了元素於 {path}，值為：{removed_items}。")
        elif old_type == dict and new_type == list:
            added_items = {k: new_value[k] for k in range(len(new_value)) if k not in old_value}
            explanations.append(f"新增了元素於 {path}，值為：{added_items}。")
        else:
            explanations.append(f"類型變更於 {path}:\n從 '{old_type.__name__}' 改為 '{new_type.__name__}'，\n值從 '{old_value}' 改為 '{new_value}'。")
    return explanations

def convert_path(path):
    return path.replace("][", "/").replace("[", "/").replace("]", "").replace("'", "")

def ensure_dict(items):
    if isinstance(items, dict):
        return items
    elif isinstance(items, list):
        result = {}
        for index, item in enumerate(items):
            result[str(index)] = item
        return result
    else:
        raise ValueError("Unexpected type for ensure_dict function")

xml1_path = r"C:\Users\a9037\OneDrive\文件\GitHub\XML-Compare-Tool\Before\before_split\AuthorOne_1980-01-01.xml"
xml2_path = r"C:\Users\a9037\OneDrive\文件\GitHub\XML-Compare-Tool\After\after_split\AuthorOne_1980-01-01.xml"

# 使用DeepDiff來比較兩個XML字典
diff_result = find_diff(xml1_path, xml2_path)
xml1_dict = xml_to_dict(xml1_path)
xml2_dict = xml_to_dict(xml2_path)
explanations = parse_diff(diff_result, xml1_dict, xml2_dict)

# 將結果保存到一個文本檔案中
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
repeat_new_folder = os.path.join(r"C:\Users\a9037\OneDrive\文件\GitHub\XML-Compare-Tool\Test", "diff_report")
os.makedirs(repeat_new_folder, exist_ok=True)
file_path = os.path.join(repeat_new_folder, f"diff_output_{current_time}.txt")
with open(file_path, "w", encoding="utf-8") as file:
    for explanation in explanations:
        file.write(explanation + "\n")

print(f"-------Diff analysis saved to {file_path}")
