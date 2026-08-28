# -*- coding: utf-8 -*-
"""调查 D 系列文章的完整度：标题、题目链接、算法解析、Python、C++、图片"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BLOGS = ROOT / "src" / "content" / "blogs"

def has(text, pattern):
    return bool(re.search(pattern, text))

for d in sorted(BLOGS.iterdir(), key=lambda p: p.name.lower()):
    if not d.is_dir() or not d.name.upper().startswith("D"):
        continue
    md = d / "index.md"
    text = md.read_text(encoding="utf-8", errors="ignore")
    title = re.search(r'^title:\s*"(.*?)"', text, re.M)
    link = re.search(r"题目链接[：:]\s*(\S+)", text)
    algo = has(text, r"算法解析")
    py = has(text, r"Python代码实现|py代码实现")
    cpp = has(text, r"C\+\+代码实现")
    imgs = re.findall(r'!\[[^\]]*\]\(([^)]+)\)', text)
    print(
        f"{d.name}\n"
        f"  title={title.group(1) if title else '?'} | 链接={link.group(1) if link else '无'} | "
        f"算法解析={'有' if algo else '无'} | Py={'有' if py else '无'} | C++={'有' if cpp else '无'} | 图={imgs if imgs else '无'}"
    )
