"""文章规范自检：在提交前跑一遍，确保内容目录结构一致。

校验项：
  硬错误（退出码 1）
    - frontmatter 缺 title / publishDate / description / category / language
    - category 不在 src/utils/categories.ts 的白名单里
    - 正文引用了 `/images/...` 绝对路径或 http(s) 外链（应改为文章内相对路径）
    - 引用的图片文件不存在（含 heroImage.src）
  警告（退出码 0）
    - 图片没有放在该文章的 images/ 子目录
    - images/ 里存在正文没引用的孤儿图
    - 同一篇文章里存在内容完全相同的重复图
    - slug 不是 ASCII kebab-case（历史遗留，仅提示）

用法:
    python _tools/check_content.py            # 常规自检
    python _tools/check_content.py --strict   # 把警告也视为失败
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BLOGS = ROOT / "src" / "content" / "blogs"
COLLECTIONS = ROOT / "src" / "content" / "collection"
CATEGORY_FILE = ROOT / "src" / "utils" / "categories.ts"

IMG_RE = re.compile(r"!\[[^\]]*\]\(([^)\s]+)\)")
HTML_IMG_RE = re.compile(r'<img[^>]*?src="([^"]+)"')
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.S)
REQUIRED_FIELDS = ("title", "publishDate", "description", "category", "language")
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".avif"}


def load_allowed_categories() -> set[str]:
    slugs = re.findall(r"slug:\s*'([^']+)'", CATEGORY_FILE.read_text(encoding="utf-8"))
    return set(slugs)


def md5(path: Path) -> str:
    return hashlib.md5(path.read_bytes()).hexdigest()


# Astro 的 glob loader 会把目录名 slug 化（小写 + 去标点），全角括号、顿号都会消失，
# 所以合集里写 bloglist 时必须用这个 slug，而不是文件夹名字面。
NON_SLUG_CHARS = re.compile(r"[^a-z0-9\u4e00-\u9fff-]")


def post_id_of(folder_name: str) -> str:
    return NON_SLUG_CHARS.sub("", folder_name.lower())


def check_collections(known_ids: set[str], errors: list[str], warnings: list[str]) -> None:
    if not COLLECTIONS.is_dir():
        return
    for md in sorted(COLLECTIONS.rglob("*.md")):
        text = md.read_text(encoding="utf-8")
        frontmatter = FRONTMATTER_RE.match(text)
        label = f"collection/{md.name}"
        if not frontmatter:
            errors.append(f"{label}: 缺少 frontmatter")
            continue
        body = frontmatter.group(1)
        if not re.search(r"^title\s*:", body, re.M):
            errors.append(f"{label}: frontmatter 缺少 title")
        if not re.search(r"^description\s*:", body, re.M):
            warnings.append(f"{label}: 没有写 description（列表页会空着）")

        block = re.search(r"^bloglist\s*:\s*\n((?:\s+-\s*.*\n?)+)", body, re.M)
        if not block:
            warnings.append(f"{label}: bloglist 为空")
            continue
        entries = re.findall(r"-\s*(\S+)", block.group(1))
        for entry in entries:
            if entry.lower() not in known_ids:
                warnings.append(
                    f"{label}: bloglist 里的 '{entry}' 没对上任何文章"
                    f"（目录名 slug 化后应为 '{post_id_of(entry)}'）"
                )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true", help="警告也视为失败")
    args = parser.parse_args()

    allowed = load_allowed_categories()
    if not allowed:
        print("! 没能从 src/utils/categories.ts 解析出分类白名单")
        return 1

    errors: list[str] = []
    warnings: list[str] = []
    legacy_slugs: list[str] = []
    checked = 0

    for md in sorted(BLOGS.rglob("index*.md")):
        post_dir = md.parent
        slug = post_dir.name
        label = f"{slug}/{md.name}"
        text = md.read_text(encoding="utf-8")
        checked += 1

        frontmatter = FRONTMATTER_RE.match(text)
        if not frontmatter:
            errors.append(f"{label}: 缺少 frontmatter")
            continue
        body = frontmatter.group(1)
        for field in REQUIRED_FIELDS:
            if not re.search(rf"^{field}\s*:", body, re.M):
                errors.append(f"{label}: frontmatter 缺少 {field}")

        category = re.search(r"^category\s*:\s*(\S+)", body, re.M)
        if category and category.group(1) not in allowed:
            errors.append(
                f"{label}: category '{category.group(1)}' 不在白名单 "
                f"({', '.join(sorted(allowed))})"
            )

        if not SLUG_RE.match(slug):
            legacy_slugs.append(slug)

        # 封面图
        hero = re.search(r"heroImage:\s*\n(?:\s+.*\n)*?\s+src:\s*(\S+)", body)
        if hero:
            hero_src = hero.group(1).strip("'\"")
            if not (post_dir / hero_src).exists():
                errors.append(f"{label}: heroImage.src 不存在 -> {hero_src}")

        # 正文图片
        refs = IMG_RE.findall(text) + HTML_IMG_RE.findall(text)
        used: set[Path] = set()
        for ref in refs:
            if ref.startswith(("http://", "https://")):
                errors.append(f"{label}: 图片用了外链，建议下载到本地 -> {ref}")
                continue
            if ref.startswith("/"):
                errors.append(f"{label}: 图片用了绝对路径，应改为相对路径 -> {ref}")
                continue
            target = (post_dir / ref).resolve()
            if not target.exists():
                errors.append(f"{label}: 图片不存在 -> {ref}")
                continue
            used.add(target)
            if target.parent != (post_dir / "images").resolve():
                warnings.append(f"{label}: 图片没放在 images/ 子目录 -> {ref}")

        # 孤儿图 & 重复图
        images_dir = post_dir / "images"
        if images_dir.is_dir():
            seen: dict[str, Path] = {}
            for image in sorted(images_dir.rglob("*")):
                if not image.is_file() or image.suffix.lower() not in IMAGE_SUFFIXES:
                    continue
                if image.resolve() not in used:
                    warnings.append(f"{label}: images/{image.name} 未被正文引用")
                digest = md5(image)
                if digest in seen:
                    warnings.append(
                        f"{label}: images/{image.name} 与 {seen[digest].name} 内容重复"
                    )
                else:
                    seen[digest] = image

    print(f"检查文章: {checked} 篇")

    known_ids = {post_id_of(md.parent.name) for md in BLOGS.rglob("index*.md")}
    check_collections(known_ids, errors, warnings)

    if legacy_slugs:
        sample = ", ".join(legacy_slugs[:3])
        warnings.append(
            f"{len(legacy_slugs)} 篇老文章的 slug 不是 ASCII kebab-case（历史遗留，不阻塞；"
            f"新文章建议用 a12-heap 这类写法，例: {sample} ...）"
        )

    if errors:
        print(f"\n[FAIL] 错误 {len(errors)} 项:")
        for line in errors:
            print("   -", line)
    else:
        print("\n[OK] 没有硬错误")

    if warnings:
        print(f"\n[WARN] 警告 {len(warnings)} 项:")
        for line in warnings:
            print("   -", line)

    if errors or (args.strict and warnings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
