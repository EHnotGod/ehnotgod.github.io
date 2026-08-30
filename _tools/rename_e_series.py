# -*- coding: utf-8 -*-
"""E 系列重排：E4,E5,E6,E8,... -> E1-E22 连续编号（保持相对顺序）。
同步：文件夹名、index.md title、图片文件名、文章内图片引用、_tools/set_curated_descriptions.py key。
"""
import os
import re

BASE = os.path.join("src", "content", "blogs")
IMG = os.path.join("public", "images", "算法竞赛", "E")
DESC = os.path.join("_tools", "set_curated_descriptions.py")

# 旧目录名 -> 新目录名（按现有相对顺序）
FOLDER_MAP = [
    ("E4-最长上升子序列（二分优化）", "E1-最长上升子序列（二分优化）"),
    ("E5-最长公共子序列", "E2-最长公共子序列"),
    ("E6-最长公共子串", "E3-最长公共子串"),
    ("E8-01背包", "E4-01背包"),
    ("E9-完全背包", "E5-完全背包"),
    ("E10-多重背包", "E6-多重背包"),
    ("E11-滑动窗口", "E7-滑动窗口"),
    ("E14-混合背包", "E8-混合背包"),
    ("E15-二维背包", "E9-二维背包"),
    ("E16-分组背包", "E10-分组背包"),
    ("E17-树形DP", "E11-树形DP"),
    ("E18-树上背包", "E12-树上背包"),
    ("E19-背包方案数", "E13-背包方案数"),
    ("E20-背包具体方案", "E14-背包具体方案"),
    ("E23-线性DP-K笔买卖", "E15-线性DP-K笔买卖"),
    ("E25-TSP-状压DP", "E16-TSP-状压DP"),
    ("E29-区间DP-环形石子", "E17-区间DP-环形石子"),
    ("E32-树的重心", "E18-树的重心"),
    ("E36-数位DP", "E19-数位DP"),
    ("E37-Windy数", "E20-Windy数"),
    ("E43-单调队列优化dp", "E21-单调队列优化dp"),
    ("E51-斜率优化DP", "E22-斜率优化DP"),
]

# 图片文件名映射（旧 -> 新）
IMG_MAP = [
    ("E4-1.png", "E1-1.png"),
    ("E5-1.png", "E2-1.png"),
    ("E5-2.png", "E2-2.png"),
    ("E6-1.png", "E3-1.png"),
    ("E6-2.png", "E3-2.png"),
    ("E8-1.png", "E4-1.png"),
    ("E9-1.png", "E5-1.png"),
    ("E10-1.png", "E6-1.png"),
]


def rename_folders():
    # 两阶段：先改临时名避免冲突
    tmp_pairs = [(old, "__TMP_" + old, new) for old, new in FOLDER_MAP]
    for old, tmp, _ in tmp_pairs:
        os.rename(os.path.join(BASE, old), os.path.join(BASE, tmp))
    for _, tmp, new in tmp_pairs:
        os.rename(os.path.join(BASE, tmp), os.path.join(BASE, new))


def update_titles():
    for old, new in FOLDER_MAP:
        num = new.split("-")[0]  # "E1"
        p = os.path.join(BASE, new, "index.md")
        with open(p, encoding="utf-8") as f:
            content = f.read()
        content_new = re.sub(r'title: "E\d+ ', f'title: "{num} ', content, count=1)
        if content_new == content:
            print(f"WARN: title not updated in {new}")
        with open(p, "w", encoding="utf-8", newline="") as f:
            f.write(content_new)


def rename_images():
    for old, new in IMG_MAP:
        src = os.path.join(IMG, old)
        dst = os.path.join(IMG, new)
        if os.path.exists(src):
            os.rename(src, dst)
        else:
            print(f"WARN: image not found {old}")


def update_img_refs():
    # 文章内图片引用：新目录名 -> 内部路径 E??-n.png 改为新名
    # 旧目录名 -> 该文件内的旧图片名 -> 新图片名
    old_to_new_img = dict(IMG_MAP)
    for old, new in FOLDER_MAP:
        p = os.path.join(BASE, new, "index.md")
        with open(p, encoding="utf-8") as f:
            content = f.read()
        changed = False
        for oimg, nimg in IMG_MAP:
            if ("/" + oimg) in content or ("(" + oimg + ")") in content:
                content = content.replace(oimg, nimg)
                changed = True
        if changed:
            with open(p, "w", encoding="utf-8", newline="") as f:
                f.write(content)


def update_desc_keys():
    with open(DESC, encoding="utf-8") as f:
        content = f.read()
    for old, new in FOLDER_MAP:
        old_key = '"' + old + '"'
        new_key = '"' + new + '"'
        content = content.replace(old_key, new_key)
    with open(DESC, "w", encoding="utf-8", newline="") as f:
        f.write(content)


if __name__ == "__main__":
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    if mode in ("all", "folders"):
        rename_folders()
    if mode in ("all", "titles"):
        update_titles()
    if mode in ("all", "images"):
        rename_images()
    if mode in ("all", "imgrefs"):
        update_img_refs()
    if mode in ("all", "desc"):
        update_desc_keys()
    print("E series done OK")
