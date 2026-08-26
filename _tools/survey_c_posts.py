# -*- coding: utf-8 -*-
"""调查所有 C 开头文章的 title 和图片引用"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BLOGS = ROOT / "src" / "content" / "blogs"

for d in sorted(BLOGS.iterdir(), key=lambda p: p.name.lower()):
    if not d.is_dir() or not d.name.upper().startswith("C"):
        continue
    md = d / "index.md"
    text = md.read_text(encoding="utf-8", errors="ignore")
    title = re.search(r'^title:\s*"(.*?)"', text, re.M)
    imgs = re.findall(r'!\[[^\]]*\]\(([^)]+)\)', text)
    print(f"{d.name}  |  title={title.group(1) if title else '?'}  |  图: {imgs if imgs else '无'}")
