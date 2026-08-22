# -*- coding: utf-8 -*-
"""
将 Hexo 博客文章迁移到 Axi-Theme (Astro) 内容集合。

来源: _archive/source/_posts/**/*.md
目标: src/content/blogs/<slug>/index.mdx

- 分类简化: 算法竞赛->algo, 机器学习->ml, Dezero/torch->dl
- 日期: 旧站发布日 2026-08-08（决策树/随机森林为 2026-08-09）
- 描述: 由正文首段自动生成
- 标签: 保留原标签 + 算法竞赛子分类
"""
import os
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "_archive" / "source" / "_posts"
DST = ROOT / "src" / "content" / "blogs"
IMG_SRC = ROOT / "_archive" / "source" / "images"
IMG_DST = ROOT / "public" / "images"

# 简化分类映射：目录相对路径 -> (分类 slug, 子分类标签)
CATEGORY_MAP = {
    "算法竞赛": ("algo", None),
    "机器学习": ("ml", None),
    "Dezero框架学习与改进": ("dl", "深度学习底层"),
    "torch": ("dl", "深度学习底层"),
}

# 算法竞赛子分类（字母前缀 -> 标签名）
SUB_CATEGORY = {
    "A 基础算法": "基础算法",
    "B 搜索算法": "搜索算法",
    "C 数据结构": "数据结构",
    "D 图论": "图论",
    "E 动态规划": "动态规划",
    "F 字符串": "字符串",
    "G 数学": "数学",
    "H 邪教": "邪教",
    "I 典题": "典题",
}

# 特定文章的发布日期覆盖（旧站 08/09 区分）
DATE_OVERRIDE = {
    "决策树算法": "2026-08-09",
    "随机森林": "2026-08-09",
}
DEFAULT_DATE = "2026-08-08"


def parse_frontmatter(text: str):
    """解析 YAML frontmatter，返回 (frontmatter_dict, body)"""
    m = re.match(r"^---\s*\r?\n(.*?)\r?\n---\s*\r?\n?", text, re.S)
    if not m:
        return {}, text
    fm_text, body = m.group(1), text[m.end():]
    fm = {}
    lines = fm_text.splitlines()
    current_key = None
    for line in lines:
        key_match = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if key_match:
            current_key = key_match.group(1)
            val = key_match.group(2).strip().strip('"').strip("'")
            if current_key in ("categories", "tags"):
                fm[current_key] = []
                if val:  # 单行写法: tags: [a, b]
                    fm[current_key] = [v.strip() for v in val.strip("[]").split(",") if v.strip()]
            else:
                fm[current_key] = val
            continue
        list_match = re.match(r"^\s*-\s*(.*)$", line)
        if list_match and current_key in ("categories", "tags"):
            item = list_match.group(1).strip()
            # categories 可能是嵌套数组 - [算法, A 基础算法]
            if item.startswith("["):
                inner = [v.strip().strip('"').strip("'") for v in item.strip("[]").split(",")]
                fm[current_key].append(inner)
            else:
                fm[current_key].append(item.strip('"').strip("'"))
    return fm, body


def escape_yaml(s: str) -> str:
    """转义 YAML 双引号字符串中的特殊字符"""
    return s.replace("\\", "\\\\").replace('"', '\\"')


def sanitize_slug(title: str) -> str:
    """由标题生成 slug"""
    slug = re.sub(r"\s+", "-", title.strip())
    slug = re.sub(r"[\\/:*?\"<>|\u0000-\u001f]", "", slug)
    return slug


def make_description(body: str, max_len: int = 150) -> str:
    """从正文第一段（跳过标题）生成描述"""
    # 去掉代码块
    text = re.sub(r"```.*?```", " ", body, flags=re.S)
    # 去掉行内代码和图片
    text = re.sub(r"!\[.*?\]\(.*?\)", " ", text)
    text = re.sub(r"`[^`]*`", " ", text)
    # 去掉 markdown 链接/加粗/斜体符号
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"[*_>`~]", " ", text)
    # 跳过标题行与空行，取第一个内容充实（>=15 字）的非空段落
    paragraphs = [
        p.strip()
        for p in text.split("\n")
        if p.strip() and not p.strip().startswith("#") and len(p.strip()) >= 15
    ]
    desc = paragraphs[0] if paragraphs else ""
    # 数学公式内容去掉
    desc = re.sub(r"\$\$.*?\$\$", "", desc, flags=re.S)
    desc = re.sub(r"\$[^$]*\$", "", desc)
    desc = re.sub(r"\s+", " ", desc).strip()
    if len(desc) > max_len:
        desc = desc[:max_len].rstrip() + "…"
    return desc or "算法学习笔记"


def main():
    # 清理旧产物（避免残留 .mdx / 旧 index）
    if DST.exists():
        for old in DST.rglob("*"):
            if old.is_file() and old.name.startswith("index"):
                old.unlink()
    posts = sorted(SRC.rglob("*.md"))
    migrated, skipped = [], []
    for src in posts:
        rel = src.relative_to(SRC)
        parts = list(rel.parts)
        top = parts[0]
        if top not in CATEGORY_MAP:
            skipped.append((str(rel), f"未知顶层分类: {top}"))
            continue
        category, extra_tag = CATEGORY_MAP[top]

        text = src.read_text(encoding="utf-8-sig", errors="replace")
        fm, body = parse_frontmatter(text)
        title = fm.get("title", src.stem).strip()
        if not title:
            title = src.stem

        # 标签
        tags = []
        raw_tags = fm.get("tags", [])
        if isinstance(raw_tags, list):
            tags = [t for t in raw_tags if isinstance(t, str)]
        if extra_tag:
            tags.append(extra_tag)
        # 算法竞赛子分类作为标签
        if top == "算法竞赛" and len(parts) > 1:
            sub = parts[1]
            if sub in SUB_CATEGORY:
                tags.append(SUB_CATEGORY[sub])
        # 去重保序
        seen = set()
        tags = [t for t in tags if not (t in seen or seen.add(t))]

        # 日期
        date = DATE_OVERRIDE.get(title, DEFAULT_DATE)

        # slug
        slug = sanitize_slug(title)

        # 生成 frontmatter
        desc = escape_yaml(make_description(body))
        fm_lines = [
            "---",
            f'title: "{escape_yaml(title)}"',
            f"publishDate: {date}",
            f'description: "{desc}"',
            f"category: {category}",
            f"tags:",
        ]
        for t in tags:
            fm_lines.append(f"  - {t}")
        fm_lines.append("language: zh")
        fm_lines.append("---")
        fm_lines.append("")

        # 写入 index.md（纯 markdown，避免 MDX 把 < 当 JSX 解析）
        out_dir = DST / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / "index.md"
        out_file.write_text("\n".join(fm_lines) + "\n" + body.lstrip("\n"), encoding="utf-8")
        migrated.append((str(rel), category, slug, len(tags)))

    # 复制图片
    img_count = 0
    if IMG_SRC.exists():
        for img in IMG_SRC.rglob("*"):
            if img.is_file():
                target = IMG_DST / img.relative_to(IMG_SRC)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(img, target)
                img_count += 1

    print(f"== 迁移完成 ==")
    print(f"文章: {len(migrated)} 篇, 跳过: {len(skipped)} 个, 图片: {img_count} 张")
    print("\n-- 迁移清单 --")
    for rel, cat, slug, ntags in migrated:
        print(f"  [{cat}] {rel} -> {slug} ({ntags} tags)")
    if skipped:
        print("\n-- 跳过 --")
        for rel, reason in skipped:
            print(f"  {rel}: {reason}")


if __name__ == "__main__":
    main()
