# -*- coding: utf-8 -*-
"""F 系列重排：F3,F5,F6,F7 -> F1-F4（保持相对顺序）。
同步：文件夹名、index.md title、_tools/set_curated_descriptions.py key。
"""
import os
import re
import sys

BASE = os.path.join("src", "content", "blogs")
DESC = os.path.join("_tools", "set_curated_descriptions.py")

# 旧 -> 新
F_MAP = [
    ("F3-KMP算法", "F1-KMP算法"),
    ("F5-马拉车算法-最长回文子串", "F2-马拉车算法-最长回文子串"),
    ("F6-Trie字典树", "F3-Trie字典树"),
    ("F7-最大异或对", "F4-最大异或对"),
]


def rename_folders():
    tmp_pairs = [(old, "__TMP_" + old, new) for old, new in F_MAP]
    for old, tmp, _ in tmp_pairs:
        os.rename(os.path.join(BASE, old), os.path.join(BASE, tmp))
    for _, tmp, new in tmp_pairs:
        os.rename(os.path.join(BASE, tmp), os.path.join(BASE, new))


def update_titles():
    for old, new in F_MAP:
        num = new.split("-")[0]
        p = os.path.join(BASE, new, "index.md")
        with open(p, encoding="utf-8") as f:
            content = f.read()
        content_new = re.sub(r'title: "F\d+ ', f'title: "{num} ', content, count=1)
        if content_new == content:
            print(f"WARN: title not updated in {new}")
        with open(p, "w", encoding="utf-8", newline="") as f:
            f.write(content_new)


def update_desc():
    with open(DESC, encoding="utf-8") as f:
        content = f.read()
    for old, new in F_MAP:
        content = content.replace('"' + old + '"', '"' + new + '"')
    with open(DESC, "w", encoding="utf-8", newline="") as f:
        f.write(content)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    if mode in ("all", "folders"):
        rename_folders()
    if mode in ("all", "titles"):
        update_titles()
    if mode in ("all", "desc"):
        update_desc()
    print("F series renamed to F1-F4 OK")
