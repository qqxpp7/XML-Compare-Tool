import os
import xml.etree.ElementTree as ET
import xmltodict
from datetime import datetime
from collections import defaultdict
from deepdiff import DeepDiff
from pprint import pprint

def parse_xml(file_path):
    tree = ET.parse(file_path)
    return tree.getroot()

def xml_to_dict(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        xml_content = file.read()
        return xmltodict.parse(xml_content)

def find_diff(xml1_path, xml2_path):
    xml1_dict = xml_to_dict(xml1_path)
    xml2_dict = xml_to_dict(xml2_path)
    diff = DeepDiff(xml1_dict, xml2_dict, ignore_order=0)
    pprint(diff, indent=2)
    return diff

def convert_path(path):
    return path.replace("][", "/").replace("[", "/").replace("]", "").replace("'", "")


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
        explanations.append(f"值變更於 {path}:Before {old_value} After {new_value}。")
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

def count_elements(root):
    element_count = defaultdict(int)
    path_dict = defaultdict(list)
    path_suffix = defaultdict(int)
    element_value_dict = defaultdict(list)

    def traverse(node, path=""):
        path = f"{path}/{node.tag}"
        path_suffix[path] += 1
        full_path = f"{path}[{path_suffix[path]}]"
        element_count[full_path] += 1
        path_dict[node.tag].append(full_path)

        # Store the text value of the element
        if node.text and node.text.strip():
            element_value_dict[node.text.strip()].append(full_path)

        for child in node:
            traverse(child, path)
    
    traverse(root)
    return element_count, path_dict, element_value_dict

def compare_elements_count(before_count, after_count, before_values, after_values):
    all_paths = set(before_count.keys()).union(set(after_count.keys()))
    differences = {}

    for path in all_paths:
        before = before_count.get(path, 0)
        after = after_count.get(path, 0)
        if before != after:
            differences[path] = (before, after)

    moved_elements = {}
    for value, before_paths in before_values.items():
        if value in after_values:
            after_paths = after_values[value]
            for bp in before_paths:
                if bp not in after_paths:
                    moved_elements[bp] = after_paths

    return differences, moved_elements

def find_differences_in_text(before_values, after_values, differences):
    diff_texts = defaultdict(list)
    all_texts = set(before_values.keys()).union(set(after_values.keys()))

    for text in all_texts:
        if text in before_values and text in after_values:
            before_paths = before_values[text]
            after_paths = after_values[text]
            for path in before_paths:
                if path in differences:
                    diff_texts[text].append(path)
            for path in after_paths:
                if path in differences:
                    diff_texts[text].append(path)
        elif text in before_values or text in after_values:
            paths = before_values.get(text, []) + after_values.get(text, [])
            for path in paths:
                if path in differences:
                    diff_texts[text].append(path)

    return diff_texts

def compare_elements_structure(element1, element2, path=""):
    differences = []

    if not isinstance(element1, ET.Element) or not isinstance(element2, ET.Element):
        differences.append(f"One of the compared elements is not a valid XML Element: {path}")
        return differences

    if element1.tag != element2.tag:
        # differences.append(f"在{path}發現差異: {element1.tag} vs {element2.tag}")
        return differences

    path += "/" + element1.tag

    children1 = list(element1)
    children2 = list(element2)

    if len(children1) != len(children2):
        # differences.append(f"{path}底下的tag數量有差異: Before = {len(children1)} vs After = {len(children2)}")
        return differences

    tag_positions1 = [child.tag for child in children1]
    tag_positions2 = [child.tag for child in children2]

    if tag_positions1 != tag_positions2:
        for i, (tag1, tag2) in enumerate(zip(tag_positions1, tag_positions2)):
            if tag1 != tag2:
                differences.append(f"Tag在{path}交換順序: {tag1} 跟 {tag2}交換")

    for child1, child2 in zip(children1, children2):
        differences.extend(compare_elements_structure(child1, child2, path))

    return differences

def analyze_deepdiff(before_file, after_file):
    '''
    使用DeepDiff來比較兩個XML字典
    '''
    diff_result = find_diff(before_file, after_file)
    explanations = parse_diff(diff_result, xml_to_dict(before_file), xml_to_dict(after_file))
    return explanations

def analyze_element_count(before_root, after_root):
    '''
    比較標籤位置和出現次數
    '''
    before_count, before_path_dict, before_values = count_elements(before_root)
    after_count, after_path_dict, after_values = count_elements(after_root)

    differences_count, moved_elements = compare_elements_count(before_count, after_count, before_values, after_values)
    diff_texts = find_differences_in_text(before_values, after_values, differences_count)

    results = []
    
    # results.append("Differences in element counts between XML files:")
    # for path, (before, after) in differences_count.items():
    #     results.append(f"{path}: before={before}, after={after}")

    # results.append("\nTexts with Differences in Changed Tags:")
    # for text, paths in diff_texts.items():
    #     results.append(f"在{paths}的Text: {text} ")
    
    results.append("\n同名稱Element移動後位置:")
    for before_path, after_paths in moved_elements.items():
        results.append(f"Before：{before_path} After：{after_paths}")
    
    return results

def analyze_structure(before_root, after_root):
    '''
    比較結構和標籤順序
    '''
    differences_structure = compare_elements_structure(before_root, after_root)
    results = []

    if differences_structure:
        results.append("\n不同名稱Element位置交換:")
        for difference in differences_structure:
            results.append(difference)
    else:
        results.append("\nNo structural differences found.")
    
    return results

def save_results_to_file(results, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        for result in results:
            file.write(result + "\n")

def main(before_file, after_file):
    before_root = parse_xml(before_file)
    after_root = parse_xml(after_file)

    # 使用DeepDiff來比較兩個XML字典
    deepdiff_explanations = analyze_deepdiff(before_file, after_file)

    # 比較標籤位置和出現次數
    element_count_results = analyze_element_count(before_root, after_root)

    # 比較結構和標籤順序
    structure_results = analyze_structure(before_root, after_root)

    # 將所有結果保存到一個文本檔案中
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    repeat_new_folder = os.path.join(r"C:\Users\a9037\OneDrive\文件\GitHub\XML-Compare-Tool\Test", "diff_report")
    os.makedirs(repeat_new_folder, exist_ok=True)
    file_path = os.path.join(repeat_new_folder, f"diff_output_{current_time}.txt")

    all_results = deepdiff_explanations + element_count_results + structure_results
    save_results_to_file(all_results, file_path)

if __name__ == "__main__":
    before_file = r"C:\Users\a9037\OneDrive\文件\GitHub\XML-Compare-Tool\Before\before_split\AuthorOne_1980-01-01.xml"  # 这里替换成实际的文件路径
    after_file = r"C:\Users\a9037\OneDrive\文件\GitHub\XML-Compare-Tool\After\after_split\AuthorOne_1980-01-01.xml"
    main(before_file, after_file)
