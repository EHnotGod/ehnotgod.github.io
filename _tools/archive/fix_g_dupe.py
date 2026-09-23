# -*- coding: utf-8 -*-
"""修复 G 系列重复的「### 题目情境」：把篇目中原有的旧题目情境块标题改为「### 备注」。
涉及：G14 G27 G29 G32 G33 G37 G45+G46 G51（原本已有题目情境，插入后重复）。
"""
import os

BASE = os.path.join("src", "content", "blogs")
NAMES = [
    "G14-拓展欧拉定理-超大幂次取余",
    "G27-求组合数-卢卡斯",
    "G29-隔板法",
    "G32-卡特兰数",
    "G33-整除分块",
    "G37-迪利克雷卷积",
    "G45+G46-第一、二类斯特林数",
    "G51-三角剖分",
]

for name in NAMES:
    p = os.path.join(BASE, name, "index.md")
    with open(p, encoding="utf-8") as f:
        c = f.read()
    # 只替换第二次出现的 ### 题目情境
    idx = c.find("### 题目情境")
    idx2 = c.find("### 题目情境", idx + 1)
    if idx2 == -1:
        print(f"WARN: no second 题目情境 in {name}")
        continue
    c = c[:idx2] + "### 备注" + c[idx2 + len("### 题目情境"):]
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.write(c)
print("fixed dupes OK")
