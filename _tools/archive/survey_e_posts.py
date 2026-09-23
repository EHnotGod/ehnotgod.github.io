# -*- coding: utf-8 -*-
"""调查 E 系列文章完整度"""
import re
from pathlib import Path

BLOGS = Path(__file__).resolve().parent.parent / "src" / "content" / "blogs"

for d in sorted(BLOGS.iterdir(), key=lambda p: p.name.lower()):
    if not d.is_dir() or not d.name.upper().startswith("E"):
        continue
    text = (d / "index.md").read_text(encoding="utf-8", errors="ignore")
    title = re.search(r'^title:\s*"(.*?)"', text, re.M)
    link = re.search(r"题目链接[：:]\s*(\S+)", text)
    algo = bool(re.search(r"算法解析", text))
    py = bool(re.search(r"Python代码实现|py代码实现", text))
    cpp = bool(re.search(r"C\+\+代码实现", text))
    print(
        f"{d.name} | 链接={link.group(1) if link else '无'} | 解析={'有' if algo else '无'} "
        f"| Py={'有' if py else '无'} | C++={'有' if cpp else '无'}"
    )
