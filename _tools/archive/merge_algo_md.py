# -*- coding: utf-8 -*-
"""把 A-H 系列所有算法文章合并成一个巨大的 markdown（按系列分章）。
每章用 # 大标题分隔，每篇用 ## 标题 + frontmatter 信息 + 正文（去掉原 frontmatter 头）。
输出到 d:\Desktop\github_tasks\ehnotgod.github.io\算法竞赛合集.md
"""
import os
import re
import glob

BASE = os.path.join("src", "content", "blogs")
OUT = os.path.join(os.getcwd(), "算法竞赛合集.md")

SERIES = {
    "A": "A · 基础算法",
    "B": "B · 搜索算法",
    "C": "C · 数据结构",
    "D": "D · 图论",
    "E": "E · 动态规划",
    "F": "F · 字符串",
    "G": "G · 数学",
    "H": "H · 额外算法",
}

def natural_key(name):
    # 提取 A3 / G45 数字部分做自然排序
    m = re.match(r'^([A-H])(\d+)', name)
    if m:
        return int(m.group(2))
    return 0

def parse_md(path):
    with open(path, encoding="utf-8") as f:
        content = f.read()
    # 分离 frontmatter 与正文
    m = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.S)
    fm = {}
    body = content
    if m:
        fm_text, body = m.group(1), m.group(2)
        for line in fm_text.split("\n"):
            kv = re.match(r'^([A-Za-z_]+):\s*(.*)$', line)
            if kv:
                fm[kv.group(1)] = kv.group(2).strip().strip('"')
    return fm, body.strip()

lines = []
lines.append("# 算法竞赛合集（A-H 全系列）")
lines.append("")
lines.append("> 由 EH 博客 `src/content/blogs/` 下 A-H 系列共 124 篇文章合并生成。")
lines.append("")
lines.append("## 目录")
lines.append("")
total = 0
# 收集各系列文章
per_series = {}
for prefix in SERIES:
    dirs = [d for d in glob.glob(os.path.join(BASE, prefix + "*")) if os.path.isdir(d)]
    dirs.sort(key=lambda d: natural_key(os.path.basename(d)))
    items = []
    for d in dirs:
        p = os.path.join(d, "index.md")
        if not os.path.exists(p):
            continue
        name = os.path.basename(d)
        fm, body = parse_md(p)
        items.append((name, fm, body))
    per_series[prefix] = items
    total += len(items)

# 目录
for prefix, title in SERIES.items():
    items = per_series[prefix]
    lines.append(f"- **{title}**（{len(items)} 篇）")
    for name, fm, body in items:
        t = fm.get("title", name)
        lines.append(f"  - {t}")
lines.append("")
lines.append("---")
lines.append("")

# 正文
for prefix, title in SERIES.items():
    items = per_series[prefix]
    lines.append(f"# {title}（{len(items)} 篇）")
    lines.append("")
    for name, fm, body in items:
        t = fm.get("title", name)
        desc = fm.get("description", "")
        tags = fm.get("tags", "")
        pub = fm.get("publishDate", "")
        lines.append(f"## {t}")
        lines.append("")
        if desc:
            lines.append(f"> **描述**：{desc}")
        if pub:
            lines.append(f"> **日期**：{pub}")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append(body)
        lines.append("")
        lines.append("---")
        lines.append("")
    lines.append("")

out_text = "\n".join(lines)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(out_text)
print(f"生成完成：{OUT}")
print(f"共 {total} 篇文章，{len(out_text)//1024} KB")
