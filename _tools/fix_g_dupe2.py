# -*- coding: utf-8 -*-
"""修复所有 G 篇目重复的「### 题目情境」：第二次出现的改为「### 备注」。
"""
import os
import glob

BASE = os.path.join("src", "content", "blogs")

for d in sorted(glob.glob(os.path.join(BASE, "G*"))):
    p = os.path.join(d, "index.md")
    if not os.path.exists(p):
        continue
    with open(p, encoding="utf-8") as f:
        c = f.read()
    idx = c.find("### 题目情境")
    if idx == -1:
        continue
    idx2 = c.find("### 题目情境", idx + 1)
    if idx2 == -1:
        continue  # 只有一处，正常
    # 把第二处（及之后的所有）改为 ### 备注
    head = c[:idx2]
    tail = c[idx2:].replace("### 题目情境", "### 备注")
    c = head + tail
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.write(c)
    print(f"fixed: {os.path.basename(d)}")
print("all dupes fixed")
