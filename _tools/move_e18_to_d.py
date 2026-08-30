# -*- coding: utf-8 -*-
"""把 E18-树的重心 移到 D 系列（作为 D21，紧跟 D20-树的直径）。
同步：文件夹、title、图片引用+文件、_tools/set_curated_descriptions.py key。
D: D21->D22, D22->D23, D23->D24；E: E19-E22 -> E18-E21。
"""
import os
import re
import shutil

BASE = os.path.join("src", "content", "blogs")
DIMG = os.path.join("public", "images", "算法竞赛", "D")
DESC = os.path.join("_tools", "set_curated_descriptions.py")

# D 系列顺延：旧 -> 新
D_MAP = [
    ("D21-Kruscal重构树", "D22-Kruscal重构树"),
    ("D22-2-SAT", "D23-2-SAT"),
    ("D23-2-SAT-前缀优化建图", "D24-2-SAT-前缀优化建图"),
]
# E18 移入 D21
E18 = "E18-树的重心"
D21 = "D21-树的重心"
# E 系列补洞
E_MAP = [
    ("E19-数位DP", "E18-数位DP"),
    ("E20-Windy数", "E19-Windy数"),
    ("E21-单调队列优化dp", "E20-单调队列优化dp"),
    ("E22-斜率优化DP", "E21-斜率优化DP"),
]
# D 图片改名
DIMG_MAP = [
    ("D21-1.png", "D22-1.png"),
    ("D23-1.png", "D24-1.png"),
]


def move_folders():
    # 先 E18 移到 D21 临时名
    src = os.path.join(BASE, E18)
    tmp_d21 = os.path.join(BASE, "__TMP_D21-树的重心")
    shutil.move(src, tmp_d21)
    # D 系列顺延：从大到小改，避免冲突（先改最大编号）
    for old, new in reversed(D_MAP):
        os.rename(os.path.join(BASE, old), os.path.join(BASE, new))
    # E 系列补洞：从大到小
    for old, new in reversed(E_MAP):
        os.rename(os.path.join(BASE, old), os.path.join(BASE, new))
    # E18 -> D21
    os.rename(tmp_d21, os.path.join(BASE, D21))


def update_title(path, num):
    with open(path, encoding="utf-8") as f:
        content = f.read()
    content_new = re.sub(r'title: "E\d+ |title: "D\d+ ', f'title: "{num} ', content, count=1)
    if content_new == content:
        print(f"WARN: title not changed in {path}")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(content_new)


def update_titles():
    # 新 D21
    update_title(os.path.join(BASE, D21, "index.md"), "D21")
    for old, new in D_MAP:
        num = new.split("-")[0]
        update_title(os.path.join(BASE, new, "index.md"), num)
    for old, new in E_MAP:
        num = new.split("-")[0]
        update_title(os.path.join(BASE, new, "index.md"), num)


def rename_d_images():
    for old, new in DIMG_MAP:
        src = os.path.join(DIMG, old)
        dst = os.path.join(DIMG, new)
        if os.path.exists(src) and not os.path.exists(dst):
            os.rename(src, dst)
        elif not os.path.exists(src):
            print(f"WARN: image not found {old}")


def update_d_img_refs():
    # 只改 D 系列新文件夹里被顺延的引用
    for old, new in D_MAP:
        p = os.path.join(BASE, new, "index.md")
        with open(p, encoding="utf-8") as f:
            content = f.read()
        changed = False
        for oimg, nimg in DIMG_MAP:
            if oimg in content:
                content = content.replace(oimg, nimg)
                changed = True
        if changed:
            with open(p, "w", encoding="utf-8", newline="") as f:
                f.write(content)


def update_desc():
    with open(DESC, encoding="utf-8") as f:
        content = f.read()
    # 删除 E18 key
    e18_key = '"' + E18 + '"'
    if e18_key in content:
        content = content.replace(e18_key + ":", '"_REMOVED_E18_":', 1)
    # E 补洞
    for old, new in E_MAP:
        content = content.replace('"' + old + '"', '"' + new + '"')
    # D 顺延
    for old, new in D_MAP:
        content = content.replace('"' + old + '"', '"' + new + '"')
    # 新增 D21 key（放在 D20 之后）
    d20_key = '"D20-树的直径"'
    if d20_key in content:
        content = content.replace(
            d20_key,
            d20_key + ',\n    "D21-树的重心": "树的重心：删去后最大子树最小。",',
            1,
        )
    with open(DESC, "w", encoding="utf-8", newline="") as f:
        f.write(content)


if __name__ == "__main__":
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    if mode in ("all", "folders"):
        move_folders()
    if mode in ("all", "titles"):
        update_titles()
    if mode in ("all", "dimages"):
        rename_d_images()
    if mode in ("all", "dimgrefs"):
        update_d_img_refs()
    if mode in ("all", "desc"):
        update_desc()
    print("move E18 -> D21 OK")
