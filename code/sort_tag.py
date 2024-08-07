# -*- coding: utf-8 -*-
"""
不同的tag位置交換，會印出資訊
但是不會讀text
"""

import xml.etree.ElementTree as ET

def parse_xml(file):
    tree = ET.parse(file)
    root = tree.getroot()
    return root

def compare_elements(element1, element2, path=""):
    """
    有個串列存所有的diff
    isinstance判斷兩個路徑是否為樹
    如果發現有不同的tag會添加到diff串列
    """
    differences = []

    if not isinstance(element1, ET.Element) or not isinstance(element2, ET.Element):
        differences.append(f"One of the compared elements is not a valid XML Element: {path}")
        return differences

    if element1.tag != element2.tag:
        differences.append(f"在{path}發現差異: {element1.tag} vs {element2.tag}")
        return differences

    path += "/" + element1.tag

    children1 = list(element1)
    children2 = list(element2)

    if len(children1) != len(children2):
        differences.append(f"{path}底下的tag數量有差異: Before = {len(children1)} vs After = {len(children2)}")
        return differences

    tag_positions1 = [child.tag for child in children1]
    tag_positions2 = [child.tag for child in children2]

    if tag_positions1 != tag_positions2:
        for i, (tag1, tag2) in enumerate(zip(tag_positions1, tag_positions2)):
            if tag1 != tag2:
                differences.append(f"Tag在{path}交換順序: {tag1} 跟 {tag2}交換")

    for child1, child2 in zip(children1, children2):
        differences.extend(compare_elements(child1, child2, path))

    return differences

def main():
    before_file = parse_xml(r"C:\Users\a9037\OneDrive\文件\GitHub\XML-Compare-Tool\Before\before_split\AuthorOne_1980-01-01.xml")  
    after_file = parse_xml(r"C:\Users\a9037\OneDrive\文件\GitHub\XML-Compare-Tool\After\after_split\AuthorOne_1980-01-01.xml")
   
    differences = compare_elements(before_file, after_file)

    if differences:
        print("Differences found:")
        for difference in differences:
            print(difference)
    else:
        print("No differences found.")

if __name__ == "__main__":
    main()
