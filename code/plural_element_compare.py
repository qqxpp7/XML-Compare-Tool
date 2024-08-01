import xml.etree.ElementTree as ET
from collections import defaultdict

def parse_xml(file_path):
    tree = ET.parse(file_path)
    return tree.getroot()

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

def compare_elements(before_count, after_count, before_values, after_values):
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

def sort_path_dict(path_dict):
    sorted_dict = {}
    for key in sorted(path_dict.keys()):
        sorted_dict[key] = sorted(path_dict[key])
    return sorted_dict

def main(before_file, after_file):
    before_root = parse_xml(before_file)
    after_root = parse_xml(after_file)

    before_count, before_path_dict, before_values = count_elements(before_root)
    after_count, after_path_dict, after_values = count_elements(after_root)

    differences, moved_elements = compare_elements(before_count, after_count, before_values, after_values)
    sorted_before_path_dict = sort_path_dict(before_path_dict)
    sorted_after_path_dict = sort_path_dict(after_path_dict)

    print("Differences between XML files:")
    for path, (before, after) in differences.items():
        print(f"{path}: before={before}, after={after}")

    print("\nMoved Elements:")
    for before_path, after_paths in moved_elements.items():
        print(f"{before_path} moved to {after_paths}")

    print("\nSorted Path Dictionary for Before XML:")
    for tag, paths in sorted_before_path_dict.items():
        print(f"{tag}: {paths}")

    print("\nSorted Path Dictionary for After XML:")
    for tag, paths in sorted_after_path_dict.items():
        print(f"{tag}: {paths}")

if __name__ == "__main__":
    before_file = r"C:\Users\a9037\OneDrive\文件\GitHub\XML-Compare-Tool\Before\before_split\AuthorOne_1980-01-01.xml"  # 这里替换成实际的文件路径
    after_file = r"C:\Users\a9037\OneDrive\文件\GitHub\XML-Compare-Tool\After\after_split\AuthorOne_1980-01-01.xml"
    main(before_file, after_file)


