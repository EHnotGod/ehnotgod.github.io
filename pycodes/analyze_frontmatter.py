# -*- coding: utf-8 -*-
"""扫描所有文章的 frontmatter，统计分类和标签，找出混乱/重复的标签。"""
import os
import re
import collections
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
POSTS = ROOT / "source" / "_posts"

def parse_frontmatter(text):
    """解析 --- --- 之间的 YAML frontmatter，返回 dict。"""
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    if not m:
        return {}
    body = m.group(1)
    data = {}
    current = None
    for line in body.splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        if re.match(r"^[A-Za-z_]+:", line):
            key = line.split(":", 1)[0].strip()
            val = line.split(":", 1)[1].strip()
            current = key
            data[key] = []
            if val:
                data[key].append(val)
        elif line.strip().startswith("- "):
            if current:
                data[current].append(line.strip()[2:].strip())
    return data

def main():
    all_categories = collections.Counter()
    all_tags = collections.Counter()
    files_without_fm = []
    rows = []

    for md in sorted(POSTS.rglob("*.md")):
        rel = md.relative_to(POSTS)
        text = md.read_text(encoding="utf-8-sig")  # 跳过 UTF-8 BOM
        fm = parse_frontmatter(text)
        title = fm.get("title", [""])[0]
        cats = fm.get("categories", [])
        tags = fm.get("tags", [])
        if not fm:
            files_without_fm.append(str(rel))

        rows.append({
            "file": str(rel),
            "title": title,
            "categories": cats,
            "tags": tags,
        })
        for c in cats:
            all_categories[c] += 1
        for t in tags:
            all_tags[t] += 1

    print("=" * 60)
    print(f"文章总数: {len(rows)}")
    print(f"无 frontmatter 的文件: {len(files_without_fm)}")
    for f in files_without_fm:
        print("  -", f)
    print()

    print("=" * 60)
    print("分类统计 (分类 -> 文章数):")
    for c, n in all_categories.most_common():
        print(f"  {c}: {n}")

    print()
    print("=" * 60)
    print("标签统计 (标签 -> 文章数):")
    for t, n in all_tags.most_common():
        print(f"  {t}: {n}")

    print()
    print("=" * 60)
    print("每篇文章的分类/标签:")
    for r in rows:
        print(f"[{r['file']}]")
        print(f"  title: {r['title']}")
        print(f"  categories: {r['categories']}")
        print(f"  tags: {r['tags']}")

if __name__ == "__main__":
    main()
