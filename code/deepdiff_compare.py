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
        explanations.extend(parse_values_changed(diff['values_changed'], xml1_dict, xml2_dict))
    if 'dictionary_item_removed' in diff:
        explanations.extend(parse_dict_items(diff['dictionary_item_removed'], xml1_dict, xml2_dict, removed=True))
    if 'dictionary_item_added' in diff:
        explanations.extend(parse_dict_items(diff['dictionary_item_added'], xml1_dict, xml2_dict, removed=False))
    if 'iterable_item_added' in diff:
        explanations.extend(parse_iterable_items(diff['iterable_item_added'], xml1_dict, xml2_dict, added=True))
    if 'iterable_item_removed' in diff:
        explanations.extend(parse_iterable_items(diff['iterable_item_removed'], xml1_dict, xml2_dict, added=False))
    if 'type_changes' in diff:
        explanations.extend(parse_type_changes(diff['type_changes'], xml1_dict, xml2_dict))
    return explanations

def parse_values_changed(values_changed, xml1_dict, xml2_dict):
    explanations = []
    if isinstance(values_changed, dict):
        values_changed = [values_changed]
    for details in values_changed:
        for key, detail in details.items():
            path = key.split("root")[1]  # Extracts the path
            old_value = detail['old_value']
            new_value = detail['new_value']
            explanations.append(f"值變更於 {path}:\n從 '{old_value}' 改為 '{new_value}'。")
    return explanations

def parse_dict_items(items, xml1_dict, xml2_dict, removed):
    explanations = []
    if isinstance(items, dict):
        items = [items]
    for key in items:
        path = key.split("root")[1]  # Extracts the path
        if removed:
            value = eval(f"xml1_dict{path}")
            explanations.append(f"刪除了元素於 {path}，值為：{value}。")
        else:
            value = eval(f"xml2_dict{path}")
            explanations.append(f"新增了元素於 {path}，值為：{value}。")
    return explanations

def parse_iterable_items(items, xml1_dict, xml2_dict, added):
    explanations = []
    if isinstance(items, dict):
        items = [items]
    for key in items:
        path = key.split("root")[1]  # Extracts the path
        if added:
            value = eval(f"xml2_dict{path}")
            explanations.append(f"新增了元素於 {path}，值為：{value}。")
        else:
            value = eval(f"xml1_dict{path}")
            explanations.append(f"刪除了元素於 {path}，值為：{value}。")
    return explanations

def parse_type_changes(type_changes, xml1_dict, xml2_dict):
    explanations = []
    for key, details in ensure_dict(type_changes).items():
        path = key.split("root")[1]  # Extracts the path
        old_value = details['old_value']
        new_value = details['new_value']
        if details['old_type'] == list and details['new_type'] == dict:
            removed_items = [k for k in old_value if k != new_value]
            explanations.append(f"刪除了元素於 {path}，值為：{removed_items}。")
        elif details['old_type'] == dict and details['new_type'] == list:
            added_items = [k for k in new_value if k != old_value]
            explanations.append(f"新增了元素於 {path}，值為：{added_items}。")
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

print(f"-------Diff analysis saved to {file_path}")
