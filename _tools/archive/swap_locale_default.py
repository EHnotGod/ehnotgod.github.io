# -*- coding: utf-8 -*-
"""
将站点默认语言从中文切换为英文：
- 英文页面移到根目录（/），中文页面移到 /zh/
- 修正移动后的硬编码链接
"""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / "src" / "pages"

# 中文页面（移到 zh/）；保留在根目录的：404.astro, robots.txt.ts, rss.xml.ts
ZH_ITEMS = [
    "index.astro",
    "about",
    "academic",
    "archives",
    "blog",
    "collection",
    "links",
    "projects",
    "search",
    "tags",
    "terms",
]

# 1) 移动中文页面到 zh/
zh_dir = PAGES / "zh"
zh_dir.mkdir(exist_ok=True)
for item in ZH_ITEMS:
    src = PAGES / item
    if src.exists():
        dst = zh_dir / item
        if dst.exists():
            shutil.rmtree(dst) if dst.is_dir() else dst.unlink()
        shutil.move(str(src), str(dst))
        print(f"moved zh: {item}")

# 2) 移动英文页面到根目录
en_dir = PAGES / "en"
for item in en_dir.iterdir():
    dst = PAGES / item.name
    if dst.exists():
        shutil.rmtree(dst) if dst.is_dir() else dst.unlink()
    shutil.move(str(item), str(dst))
    print(f"moved en: {item.name}")

# 删除空 en 目录
if en_dir.exists() and not any(en_dir.iterdir()):
    en_dir.rmdir()
    print("removed empty en/ dir")


def patch(path: Path, pairs: list[tuple[str, str]]) -> None:
    text = path.read_text(encoding="utf-8")
    for old, new in pairs:
        if old in text:
            text = text.replace(old, new)
            print(f"  [{path.name}] {old} -> {new}")
        else:
            print(f"  [WARN] {path.name}: not found: {old}")
    path.write_text(text, encoding="utf-8")


# 3) 修正链接
print("\n== 修正链接 ==")

# 原 zh 页面（现在在 /zh/ 下）—— 内部链接加 /zh 前缀
patch(PAGES / "zh" / "index.astro", [
    ("href='/about'", "href='/zh/about'"),
])
patch(PAGES / "zh" / "tags" / "index.astro", [
    ("href={`/tags/${tag}`}", "href={`/zh/tags/${tag}`}"),
])
patch(PAGES / "zh" / "blog" / "[category]" / "[...page].astro", [
    ("href={`/blog/${prevCategory}`}", "href={`/zh/blog/${prevCategory}`}"),
    ("href={`/blog/${nextCategory}`}", "href={`/zh/blog/${nextCategory}`}"),
    ("href='/archives'", "href='/zh/archives'"),
    ("href='/collection'", "href='/zh/collection'"),
    ("href={`/tags/${tag}`}", "href={`/zh/tags/${tag}`}"),
    ("href='/tags'", "href='/zh/tags'"),
])

# 原 en 页面（现在在根目录）—— 去掉 /en 前缀
patch(PAGES / "archives" / "index.astro", [("href='/en'", "href='/'")])
patch(PAGES / "search" / "index.astro", [("href='/en'", "href='/'")])
patch(PAGES / "tags" / "index.astro", [("href='/en'", "href='/'")])
patch(PAGES / "tags" / "[tag]" / "[...page].astro", [("href='/en'", "href='/'")])
patch(PAGES / "terms" / "list.astro", [("href='/en'", "href='/'")])
patch(PAGES / "index.astro", [("href='/en/about'", "href='/about'")])
patch(PAGES / "blog" / "[category]" / "[...page].astro", [
    ("href={`/en/blog/${prevCategory}`}", "href={`/blog/${prevCategory}`}"),
    ("href={`/en/blog/${nextCategory}`}", "href={`/blog/${nextCategory}`}"),
    ("href='/en/archives'", "href='/archives'"),
    ("href='/en/collection'", "href='/collection'"),
    ("href={`/en/tags/${tag}`}", "href={`/tags/${tag}`}"),
    ("href='/en/tags'", "href='/tags'"),
])

print("\n完成")
