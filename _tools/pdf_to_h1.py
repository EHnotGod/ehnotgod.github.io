# -*- coding: utf-8 -*-
"""把 计算几何-EH修改版 (3).pdf 的每一页渲染为 PNG，存入
public/images/算法竞赛/H/H1/ 目录（命名 H1-01.png ... H1-81.png）。"""
import os
import pymupdf

PDF = r"D:\Desktop\计算几何-EH修改版 (3).pdf"
OUT = os.path.join("public", "images", "算法竞赛", "H", "H1")
os.makedirs(OUT, exist_ok=True)

doc = pymupdf.open(PDF)
n = doc.page_count
print("pages:", n)
for i in range(n):
    pix = doc[i].get_pixmap(dpi=110)
    out = os.path.join(OUT, f"H1-{i+1:02d}.png")
    pix.save(out)
    if i % 10 == 0 or i == n - 1:
        print(f"saved {i+1}/{n} -> {out}")
doc.close()
print("DONE")
