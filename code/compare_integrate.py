import os
import time
import xmltodict
import xml.etree.ElementTree as ET
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
    '''
    使用DeepDiff套件找出兩個檔案的差異
    順序不納入考量，如果有element交換位置
    會在analyze_element_count印出來
    '''
    xml1_dict = xml_to_dict(xml1_path)
    xml2_dict = xml_to_dict(xml2_path)
    diff = DeepDiff(xml1_dict, xml2_dict, ignore_order=1)
    pprint(diff, indent=2)
    return diff

def convert_path(path):
    '''
    將路徑地的分隔符號都轉成/
    '''
    return path.replace("][", "/").replace("[", "/").replace("]", "").replace("'", "")

def format_issue_path(path):
    '''
    將有差異tag的path都存為<>/<>格式
    確保最後兩個標籤不是數字
    '''
    parts = path.split("/")
    last_tag = ""
    second_last_tag = ""
    
    for part in reversed(parts):
        if not last_tag and not part.isdigit():
            last_tag = part
        elif not second_last_tag and not part.isdigit():
            second_last_tag = part
        if last_tag and second_last_tag:
            break
        
    return f"<{second_last_tag}>/<{last_tag}>"

def parse_diff(diff, xml1_dict, xml2_dict):
    '''
    比對兩個xml的差異
    分別有值變更、刪除、新增
    type_changes是字典變串列or串列變字典會出現的情況
    '''
    explanations = []
    issues = []
    if 'values_changed' in diff:
        for key, details in diff['values_changed'].items():
            path = convert_path(key.split("root")[1])
            old_value = details['old_value']
            new_value = details['new_value']
            explanations.append(f"值變更於 {path}:\n從 '{old_value}' 改為 '{new_value}'。")
            issues.append(format_issue_path(path))
    if 'dictionary_item_removed' in diff:
        for key in diff['dictionary_item_removed']:
            path = convert_path(key.split("root")[1])  
            value = eval(f"xml1_dict{key.split('root')[1]}")
            explanations.append(f"刪除了元素於 {path}，值為：{value}。")
            issues.append(format_issue_path(path))
    if 'dictionary_item_added' in diff:
        for key in diff['dictionary_item_added']:
            path = convert_path(key.split("root")[1])  
            value = eval(f"xml2_dict{key.split('root')[1]}")
            explanations.append(f"新增了元素於 {path}，值為：{value}。")
            issues.append(format_issue_path(path))
    if 'iterable_item_removed' in diff:
        for key in diff['iterable_item_removed']:
            path = convert_path(key.split("root")[1])  
            value = eval(f"xml1_dict{key.split('root')[1]}")
            explanations.append(f"刪除了元素於 {path}，值為：{value}。")
            issues.append(format_issue_path(path))
    if 'iterable_item_added' in diff:
        for key in diff['iterable_item_added']:
            path = convert_path(key.split("root")[1])  
            value = eval(f"xml2_dict{key.split('root')[1]}")
            explanations.append(f"新增了元素於 {path}，值為：{value}。")
            issues.append(format_issue_path(path))
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
            issues.append(format_issue_path(path))
        return explanations, issues
    return explanations, issues


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
    moved_elements = {}

    for path in all_paths:
        before = before_count.get(path, 0)
        after = after_count.get(path, 0)
        if before != after:
            differences[path] = (before, after)

    for value, before_paths in before_values.items():
        if value in after_values:
            after_paths = after_values[value]
            for bp in before_paths:
                if bp not in after_paths:
                    for ap in after_paths:
                        if bp.rsplit('/', 1)[0] == ap.rsplit('/', 1)[0]:
                            if bp not in moved_elements:
                                moved_elements[bp] = []
                            moved_elements[bp].append(ap)

    return differences, moved_elements


def analyze_deepdiff(before_file, after_file):
    '''
    使用DeepDiff來比較兩個XML字典
    '''
    diff_result = find_diff(before_file, after_file)
    explanations, issues = parse_diff(diff_result, xml_to_dict(before_file), xml_to_dict(after_file))
    return explanations, issues

def analyze_element_count(before_root, after_root):
    '''
    同名稱Element交換位置
    比較標籤位置和出現次數
    '''
    before_count, before_path_dict, before_values = count_elements(before_root)
    after_count, after_path_dict, after_values = count_elements(after_root)

    differences_count, moved_elements = compare_elements_count(before_count, after_count, before_values, after_values)

    results = []
    
    for before_path, after_paths in moved_elements.items():
        results.append(f"Before：{before_path} After：{after_paths}")
    
    return results

def compare_elements_structure(element1, element2, path=""):
    '''
    不同名稱Element交換位置
    比較結構和標籤順序
    數量一樣->刪除A，新增B，並且有交換位置也會列出
    數量有差異又交換->有刪除或新增，會忽視刪除新增的順序
    只比較兩邊名稱相符的子元素的順序
    '''
    differences = []

    if element1.tag != element2.tag:
        return differences

    path += "/" + element1.tag

    children1 = {child.tag: child for child in element1}
    children2 = {child.tag: child for child in element2}

    common_tags = set(children1.keys()) & set(children2.keys())

    for tag in common_tags:
        child1 = children1[tag]
        child2 = children2[tag]

        differences.extend(compare_elements_structure(child1, child2, path))

    tag_positions1 = [child.tag for child in element1 if child.tag in common_tags]
    tag_positions2 = [child.tag for child in element2 if child.tag in common_tags]

    if tag_positions1 != tag_positions2:
        for i, (tag1, tag2) in enumerate(zip(tag_positions1, tag_positions2)):
            if tag1 != tag2:
                differences.append(f"Tag在{path}交換順序: {tag1} 跟 {tag2}交換")

    return differences

def analyze_structure(before_root, after_root):
    '''
    確認有出現不同名稱Element交換位置
    將結果都存到results
    '''
    differences_structure = compare_elements_structure(before_root, after_root)
    results = []

    if differences_structure:
        for difference in differences_structure:
            results.append(difference)
    
    return results

        
def print_changedtag_file(file_path, deepdiff_explanations, element_count_results, structure_results, issues):
    '''
    在Final底下新建fixed_changedtag_report，將拆分後重複文件放在那
    
    '''
    TIME_START = time.time()
    with open(file_path, 'a', encoding='utf-8') as file:
        TIME_END = time.time()
        file.write("------------------------Header ---------------------\n")
        file.write(f"執行時間     :{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write(f"花費時間     :{TIME_END - TIME_START} 秒\n")
        file.write("執行檔案      :before_split、after_split\n")
        file.write("--------------------Input Parameter ---------------------\n")
        # file.write(f"檔案數量      :{len(results) + len(matches)}\n")
        file.write(f"變動Element  :{issues}\n")
        file.write("--------------------內容 ---------------------\n")
        has_element_count = False
        has_structure_change = False
        
        for result in deepdiff_explanations:
            if result:        
                file.write(result + "\n")
                    
        for result in element_count_results:
            if result:  
                if not has_element_count:  
                    file.write("\n同名稱Element移動後位置:\n")
                    has_element_count = True
                file.write(result + "\n")
                
        for result in structure_results:
            if result:     
                if not has_structure_change:  
                    file.write("\n不同名稱Element位置交換:\n")
                    has_structure_change = True
                file.write(result + "\n")
                
                
    if os.name == 'nt':
        os.startfile(file_path)
        
def main(before_file, after_file):
    before_root = parse_xml(before_file)
    after_root = parse_xml(after_file)

    # 使用DeepDiff來比較兩個XML字典
    deepdiff_explanations, issues = analyze_deepdiff(before_file, after_file)

    # 比較標籤位置和出現次數
    element_count_results = analyze_element_count(before_root, after_root)
    
    # 比較結構和標籤順序
    structure_results = analyze_structure(before_root, after_root)

    # 將所有結果保存到一個文本檔案中
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    change_tag_new_folder = os.path.join(r"C:\Users\a9037\OneDrive\文件\GitHub\XML-Compare-Tool\Test", "diff_report")
    os.makedirs(change_tag_new_folder, exist_ok=True)
    file_path = os.path.join(change_tag_new_folder, f"diff_output_{current_time}.txt")

    print_changedtag_file(file_path, deepdiff_explanations, element_count_results, structure_results, issues)

def find_differences_in_text(before_values, after_values, differences):
    '''
    目前沒有使用
    找出字的差異
    '''
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

if __name__ == "__main__":
    before_file = r"C:\Users\a9037\OneDrive\文件\GitHub\XML-Compare-Tool\Before\before_split\AuthorOne_1980-01-01.xml"  # 这里替换成实际的文件路径
    after_file = r"C:\Users\a9037\OneDrive\文件\GitHub\XML-Compare-Tool\After\after_split\AuthorOne_1980-01-01.xml"
    main(before_file, after_file)
