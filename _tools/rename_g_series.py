# -*- coding: utf-8 -*-
"""G 系列重排：30 篇 -> G1-G30 连续编号（保持相对顺序）。
同步：文件夹名、index.md title、图片引用、图片文件名、_tools/set_curated_descriptions.py key。
"""
import os
import re
import sys

BASE = os.path.join("src", "content", "blogs")
IMG = os.path.join("public", "images", "算法竞赛", "G")
DESC = os.path.join("_tools", "set_curated_descriptions.py")

# 旧目录名 -> 新目录名
FOLDER_MAP = [
    ("G1-快速幂", "G1-快速幂"),
    ("G2-高精度快速幂", "G2-高精度快速幂"),
    ("G3-矩阵快速幂", "G3-矩阵快速幂"),
    ("G5-gcd及lcm问题", "G4-gcd及lcm问题"),
    ("G8-线性筛质数", "G5-线性筛质数"),
    ("G9-欧拉函数", "G6-欧拉函数"),
    ("G10-筛法求因数个数", "G7-筛法求因数个数"),
    ("G12-莫比乌斯函数", "G8-莫比乌斯函数"),
    ("G14-拓展欧拉定理-超大幂次取余", "G9-拓展欧拉定理-超大幂次取余"),
    ("G17-拓展欧几里得-不定方程", "G10-拓展欧几里得-不定方程"),
    ("G18-拓展欧几里得-乘法逆元", "G11-拓展欧几里得-乘法逆元"),
    ("G20-扩展中国剩余定理", "G12-扩展中国剩余定理"),
    ("G22-扩展BSGS算法", "G13-扩展BSGS算法"),
    ("G23-高斯消元法", "G14-高斯消元法"),
    ("G24-矩阵求逆-高斯约旦消元法", "G15-矩阵求逆-高斯约旦消元法"),
    ("G26-求组合数-线性逆推", "G16-求组合数-线性逆推"),
    ("G27-求组合数-卢卡斯", "G17-求组合数-卢卡斯"),
    ("G32-卡特兰数", "G18-卡特兰数"),
    ("G33-整除分块", "G19-整除分块"),
    ("G43-NTT-多项式乘法", "G20-NTT-多项式乘法"),
    ("G45-第一类斯特林数", "G21-第一类斯特林数"),
    ("G46-第二类斯特林数", "G22-第二类斯特林数"),
    ("G51-三角剖分", "G23-三角剖分"),
    ("G52-凸包算法", "G24-凸包算法"),
    ("G53-旋转卡壳", "G25-旋转卡壳"),
    ("G57-自适应辛普森积分", "G26-自适应辛普森积分"),
    ("G60-有向图博弈-SG函数", "G27-有向图博弈-SG函数"),
    ("G61-线性基-max", "G28-线性基-max"),
    ("G74-拉格朗日插值法", "G29-拉格朗日插值法"),
    ("G99-超级gcd", "G30-超级gcd"),
]

# 图片文件名：旧 -> 新（注意可能冲突，用两阶段）
IMG_MAP = [
    ("G14-1.png", "G9-1.png"),
    ("G17-1.png", "G10-1.png"),
    ("G18-1.png", "G11-1.png"),
    ("G20-1.png", "G12-1.png"),
    ("G24-1.png", "G15-1.png"),
    ("G32-1.png", "G18b-1.png"),   # 临时：避免与旧 G18-1 冲突
    ("G33-1.png", "G19-1.png"),
    ("G33-2.png", "G19-2.png"),
    ("G45-1.png", "G21-1.png"),
    ("G51-1.png", "G23-1.png"),
    ("G57-1.png", "G26-1.png"),
    ("G60-1.png", "G27-1.png"),
    ("G99-1.png", "G30-1.png"),
    ("G18b-1.png", "G18-1.png"),   # 再改回真正的 G18（卡特兰数）
]


def rename_folders():
    # 两阶段避免冲突
    tmp_pairs = [(old, "__TMP_" + old, new) for old, new in FOLDER_MAP]
    for old, tmp, _ in tmp_pairs:
        if os.path.exists(os.path.join(BASE, old)):
            os.rename(os.path.join(BASE, old), os.path.join(BASE, tmp))
        else:
            print(f"WARN folder not found: {old}")
    for _, tmp, new in tmp_pairs:
        os.rename(os.path.join(BASE, tmp), os.path.join(BASE, new))


def update_titles():
    for old, new in FOLDER_MAP:
        num = new.split("-")[0]
        p = os.path.join(BASE, new, "index.md")
        with open(p, encoding="utf-8") as f:
            content = f.read()
        content_new = re.sub(r'title: "G\d+ ', f'title: "{num} ', content, count=1)
        if content_new == content:
            print(f"WARN title not changed: {new}")
        with open(p, "w", encoding="utf-8", newline="") as f:
            f.write(content_new)


def update_img_refs():
    # 文章内图片引用：把旧图名替换为新图名（先临时再最终，避免串扰）
    # 先处理临时名映射
    tmp_only = [(o, n) for o, n in IMG_MAP if n.startswith("G18b")]
    final_only = [(o, n) for o, n in IMG_MAP if not n.startswith("G18b")]
    for old, new in FOLDER_MAP:
        p = os.path.join(BASE, new, "index.md")
        with open(p, encoding="utf-8") as f:
            content = f.read()
        changed = False
        # 第一遍：G32-1 -> G18b-1
        for o, n in tmp_only:
            if o in content:
                content = content.replace(o, n)
                changed = True
        # 第二遍：其余旧->新（含 G18-1 -> G11-1 等）
        for o, n in final_only:
            if o in content:
                content = content.replace(o, n)
                changed = True
        # 第三遍：G18b-1 -> G18-1
        for o, n in IMG_MAP:
            if o == "G18b-1.png":
                content = content.replace(o, n)
                changed = True
        if changed:
            with open(p, "w", encoding="utf-8", newline="") as f:
                f.write(content)


def rename_images():
    # 两阶段：先改 G32-1 -> G18b-1，再处理其他（此时 G18-1 已被 G18->G11 腾出）
    for old, new in IMG_MAP:
        if new.startswith("G18b"):
            src = os.path.join(IMG, old)
            dst = os.path.join(IMG, new)
            if os.path.exists(src) and not os.path.exists(dst):
                os.rename(src, dst)
    for old, new in IMG_MAP:
        if not new.startswith("G18b"):
            src = os.path.join(IMG, old)
            dst = os.path.join(IMG, new)
            if os.path.exists(src) and not os.path.exists(dst):
                os.rename(src, dst)
    # 第三阶段：G18b-1 -> G18-1
    src = os.path.join(IMG, "G18b-1.png")
    dst = os.path.join(IMG, "G18-1.png")
    if os.path.exists(src) and not os.path.exists(dst):
        os.rename(src, dst)


def update_desc():
    with open(DESC, encoding="utf-8") as f:
        content = f.read()
    for old, new in FOLDER_MAP:
        content = content.replace('"' + old + '"', '"' + new + '"')
    with open(DESC, "w", encoding="utf-8", newline="") as f:
        f.write(content)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    if mode in ("all", "folders"):
        rename_folders()
    if mode in ("all", "titles"):
        update_titles()
    if mode in ("all", "imgrefs"):
        update_img_refs()
    if mode in ("all", "images"):
        rename_images()
    if mode in ("all", "desc"):
        update_desc()
    print("G series renamed to G1-G30 OK")
