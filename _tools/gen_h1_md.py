# -*- coding: utf-8 -*-
"""生成 H1-计算几何通用/index.md：逐页插入图片。"""
import os

BASE = os.path.join("src", "content", "blogs", "H1-计算几何通用")
os.makedirs(BASE, exist_ok=True)

lines = []
lines.append('---')
lines.append('title: "H1 计算几何通用"')
lines.append('publishDate: 2026-09-01')
lines.append('description: "计算几何通用：向量、点、线、多边形等基础模板。"')
lines.append('category: algo')
lines.append('tags:')
lines.append('  - 数学')
lines.append('language: zh')
lines.append('---')
lines.append('')
lines.append('### 题目情境')
lines.append('')
lines.append('**题目描述**')
lines.append('')
lines.append('计算几何通用模板：向量运算、点与线、多边形、凸包、极角排序等基础内容（整理自"计算几何专题讲座"）。')
lines.append('')
lines.append('**说明/提示**')
lines.append('')
lines.append('本页为计算几何通用笔记，逐页以图片形式呈现。')
lines.append('')
lines.append('### 算法解析：')
lines.append('')
lines.append('计算几何通用：以向量叉积、点积为核心，覆盖点的比较、直线相交、多边形面积/包含、凸包与旋转卡壳等基础模板。以下为完整笔记。')
lines.append('')

for i in range(1, 82):
    lines.append(f'![H1-{i:02d}](/images/算法竞赛/H/H1/H1-{i:02d}.png)')
    lines.append('')

content = "\n".join(lines)
with open(os.path.join(BASE, "index.md"), "w", encoding="utf-8", newline="") as f:
    f.write(content)
print("H1 md generated,", len(lines), "lines")
