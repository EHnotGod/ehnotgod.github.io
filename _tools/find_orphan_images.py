# -*- coding: utf-8 -*-
"""找出 public/images 下未被任何 src 文件引用的孤儿图片"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMG_ROOT = ROOT / "public" / "images"

# 收集 src 下所有可能引用图片的文本
src_texts = []
for p in ROOT.glob("src/**/*"):
    if p.is_file() and p.suffix.lower() in {".md", ".astro", ".ts", ".mjs", ".js", ".json", ".css"}:
        try:
            src_texts.append((p, p.read_text(encoding="utf-8", errors="ignore")))
        except Exception:
            pass

def is_referenced(filename: str) -> bool:
    pat = re.escape(filename)
    for _, text in src_texts:
        if re.search(pat, text):
            return True
    return False

orphans = []
referenced = 0
for img in sorted(IMG_ROOT.rglob("*")):
    if not img.is_file():
        continue
    if img.suffix.lower() not in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}:
        continue
    rel = img.relative_to(ROOT).as_posix()
    if is_referenced(img.name):
        referenced += 1
    else:
        orphans.append(rel)

print(f"图片总数: {referenced + len(orphans)}, 已引用: {referenced}, 孤儿: {len(orphans)}")
for rel in orphans:
    print("孤儿:", rel)
