import xml.etree.ElementTree as ET

def parse_xml(file):
    tree = ET.parse(file)
    root = tree.getroot()
    elements = {}
    
    all_paths, all_tag_pairs = collect_paths(root)
    
    for node, tag_pair, path in zip(root.iter(), all_tag_pairs, all_paths):
        # 确保字典中有这个键
        if tag_pair not in elements:
            elements[tag_pair] = []
        
        # 添加元素的属性、文本和路径到字典
        elements[tag_pair].append((node.attrib, node.text.strip() if node.text else "", path))
    
    return elements


def collect_paths(element, parent_path='', parent=None):
    '''
    full_path產生當前元素的完整路徑
    path_parts處理最後兩個標籤的路徑，並去掉標籤中的索引部分
    '''
    paths = [] 
    tag_pairs = [] 
    
    tag_name = element.tag
    
    if parent is not None:
        siblings = list(parent)
        index = siblings.index(element)
    else:
        index = 0  
    
    full_path = f'{parent_path}/{tag_name}[{index}]'
    paths.append(full_path)
    
    
    path_parts = full_path.split('/')
    if len(path_parts) > 2:
        
        tag1 = path_parts[-2].split('[')[0]
        tag2 = path_parts[-1].split('[')[0]
        tag_pairs.append(f'{tag1}/{tag2}')
    else:
        tag_pairs.append(path_parts[-1].split('[')[0])
    
    for child in element:
        child_paths, child_tag_pairs = collect_paths(child, full_path, parent=element)
        paths.extend(child_paths)
        tag_pairs.extend(child_tag_pairs)
    
    return paths, tag_pairs


def compare_xml(file1, file2):
    elements1 = parse_xml(file1)
    elements2 = parse_xml(file2)
    
    all_tags = set(elements1.keys()).union(set(elements2.keys()))
    differences = {
        'position_swap': [],
        'added': [],
        'deleted': [],
        'modified': []
    }

    for tag in all_tags:
        elems1 = elements1.get(tag, [])
        elems2 = elements2.get(tag, [])
        
        max_common = min(len(elems1), len(elems2))
        
        # 比較元素位置
        for i in range(max_common):
            attr1, text1, path1 = elems1[i]
            attr2, text2, path2 = elems2[i]
            if path1 != path2:
                differences['position_swap'].append(tag)
            
            # 檢查是否有修改
            if attr1 != attr2 or text1 != text2:
                differences['modified'].append((tag, path1, path2, (attr1, text1), (attr2, text2)))
        
        # 檢查新增和刪除的元素，並按照路徑排序
        if len(elems1) > max_common:
            for i in range(max_common, len(elems1)):
                differences['deleted'].append((tag, elems1[i]))
        
        if len(elems2) > max_common:
            for i in range(max_common, len(elems2)):
                differences['added'].append((tag, elems2[i]))
    
    # 根據路徑排序新增和刪除的元素
    differences['added'].sort(key=lambda x: x[1][2])
    differences['deleted'].sort(key=lambda x: x[1][2])
    
    return differences

# 使用範例
file1 = r"C:\Users\a9037\OneDrive\文件\GitHub\XML-Compare-Tool\Before\before_split\AuthorOne_1980-01-01.xml"  
file2 = r"C:\Users\a9037\OneDrive\文件\GitHub\XML-Compare-Tool\After\after_split\AuthorOne_1980-01-01.xml"
diffs = compare_xml(file1, file2)

# 輸出差異
if diffs['position_swap']:
    print("=== 元素位置交換 ===")
    for tag in diffs['position_swap']:
        print(f"元素: {tag}")

if diffs['added']:
    print("\n=== 新增元素 ===")
    for tag, detail in diffs['added']:
        print(f"元素: {tag.split('[')[0]}, 詳細資訊: {detail}")

if diffs['deleted']:
    print("\n=== 刪除元素 ===")
    for tag, detail in diffs['deleted']:
        print(f"元素: {tag.split('[')[0]}, 詳細資訊: {detail}")

if diffs['modified']:
    print("\n=== 修改元素 ===")
    for tag, path1, path2, detail1, detail2 in diffs['modified']:
        print(f"元素: {tag.split('[')[0]}")
        print(f"位置1: {path1}, 詳細資訊1: {detail1}")
        print(f"位置2: {path2}, 詳細資訊2: {detail2}")