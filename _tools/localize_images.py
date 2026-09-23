"""把所有文章引用的图片统一收进各自的 src/content/blogs/<slug>/images/ 目录。

- `/images/...` 形式的站内引用 -> 从 public/images/ 移动到文章目录
- http(s) 外链 -> 下载到文章目录（失败则保留外链）
- 已经在本地的相对引用 -> 归位到 images/ 子目录
- frontmatter 里的 heroImage.src 同步改写

用法:
    python _tools/localize_images.py --dry-run   # 只打印计划，不动文件
    python _tools/localize_images.py             # 实际执行
"""

from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BLOGS = ROOT / "src" / "content" / "blogs"
PUBLIC_IMAGES = ROOT / "public" / "images"

IMG_RE = re.compile(r"(!\[[^\]]*\]\()([^)\s]+)(\))")
HTML_IMG_RE = re.compile(r'(<img[^>]*?src=")([^"]+)(")')
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)
HERO_SRC_RE = re.compile(r"^(\s*src:\s*)(\S+)(\s*)$", re.M)

# 没人引用、但明确属于某篇文章的孤儿图片: public 下的相对路径 -> 文章 slug
ORPHANS = {
    "算法竞赛/D/D9-3.png": "D9-重链剖分+线段树",
    "Dezero框架学习与改进/1-3.png": "自动微分与反向传播",
}

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
)


def md5(path: Path) -> str:
    return hashlib.md5(path.read_bytes()).hexdigest()


def unique_dest(images_dir: Path, name: str, source: Path) -> Path:
    """目标文件不存在直接返回；内容相同复用；内容不同加序号。"""
    dest = images_dir / name
    if not dest.exists():
        return dest
    if md5(dest) == md5(source):
        return dest  # 同一张图，直接复用
    i = 2
    while True:
        candidate = images_dir / f"{Path(name).stem}-{i}{Path(name).suffix}"
        if not candidate.exists():
            return candidate
        if md5(candidate) == md5(source):
            return candidate
        i += 1


def download(url: str, dest_dir: Path) -> Path | None:
    name = url.split("?")[0].rstrip("/").split("/")[-1] or "image.png"
    if not Path(name).suffix:
        name += ".png"
    dest = dest_dir / name
    request = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            data = response.read()
    except Exception as exc:  # noqa: BLE001
        print(f"    ! 下载失败 {url} ({exc})")
        return None
    dest.write_bytes(data)
    return dest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-download", action="store_true")
    args = parser.parse_args()

    moved = downloaded = failed = skipped = 0
    collisions: list[str] = []
    leftovers: list[str] = []

    for md in sorted(BLOGS.rglob("index*.md")):
        post_dir = md.parent
        images_dir = post_dir / "images"
        text = md.read_text(encoding="utf-8")

        refs = [m for m in IMG_RE.finditer(text) if not m.group(2).startswith("data:")]
        html_refs = [m for m in HTML_IMG_RE.finditer(text) if not m.group(2).startswith("data:")]
        if html_refs and md.name == "index.md":
            print(f"[{post_dir.name}] 注意: 存在 <img> 标签 {len(html_refs)} 处，需人工确认")

        if not refs and not text.count("heroImage"):
            continue

        def resolve(ref: str) -> tuple[Path | None, str]:
            """返回 (源文件, 失败原因)。"""
            if ref.startswith("/images/"):
                src = PUBLIC_IMAGES / ref[len("/images/") :]
                return (src, "") if src.exists() else (None, "站内图片缺失")
            if ref.startswith(("http://", "https://")):
                return None, "external"
            src = post_dir / ref
            return (src, "") if src.exists() else (None, "本地图片缺失")

        replacements: list[tuple[int, int, str]] = []
        plans: list[str] = []

        for match in refs:
            start, end, ref = match.start(2), match.end(2), match.group(2)
            src, why = resolve(ref)

            if src is None and why == "external":
                if args.no_download or args.dry_run:
                    plans.append(f"下载 {ref}")
                    downloaded += 1
                    continue
                if not images_dir.exists():
                    images_dir.mkdir(parents=True, exist_ok=True)
                got = download(ref, images_dir)
                if got is None:
                    failed += 1
                    continue
                new_ref = f"images/{got.name}"
                replacements.append((start, end, new_ref))
                plans.append(f"下载 {ref} -> {new_ref}")
                downloaded += 1
                continue

            if src is None:
                leftovers.append(f"{post_dir.name}: {ref} ({why})")
                continue

            target_dir = images_dir if src.parent != images_dir else images_dir
            if src.parent == images_dir:
                new_ref = f"images/{src.name}"
                if new_ref != ref:
                    replacements.append((start, end, new_ref))
                    plans.append(f"改写 {ref} -> {new_ref}")
                continue

            target_dir.mkdir(parents=True, exist_ok=True)
            dest = unique_dest(target_dir, src.name, src)
            if dest.name != src.name:
                collisions.append(f"{post_dir.name}: {src.name} -> {dest.name}")
            new_ref = f"images/{dest.name}"
            if not args.dry_run:
                if dest.exists() and md5(dest) == md5(src):
                    src.unlink()  # 内容一致，删掉重复的源文件
                else:
                    shutil.move(str(src), str(dest))
            replacements.append((start, end, new_ref))
            plans.append(f"移动 {ref} -> {new_ref}")
            moved += 1

        # frontmatter 的 heroImage.src
        fm = FRONTMATTER_RE.match(text)
        hero_rewrites: list[tuple[int, int, str]] = []
        if fm and "heroImage" in fm.group(1):
            fm_body = fm.group(1)
            fm_start = fm.start(1)
            for hero in HERO_SRC_RE.finditer(fm_body):
                value = hero.group(2)
                if value.startswith(("http", "/", "images/")):
                    continue
                src = post_dir / value
                if not src.exists():
                    leftovers.append(f"{post_dir.name}: heroImage src={value} 不存在")
                    continue
                images_dir.mkdir(parents=True, exist_ok=True)
                dest = unique_dest(images_dir, src.name, src)
                if not args.dry_run and src.parent != images_dir:
                    shutil.move(str(src), str(dest))
                new_value = f"images/{dest.name}"
                hero_rewrites.append((fm_start + hero.start(2), fm_start + hero.end(2), new_value))
                plans.append(f"hero {value} -> {new_value}")
                moved += 1

        if not plans:
            continue

        print(f"[{post_dir.name}]")
        for plan in plans:
            print(f"    {plan}")

        if not args.dry_run:
            for start, end, new in sorted(replacements + hero_rewrites, reverse=True):
                text = text[:start] + new + text[end:]
            md.write_text(text, encoding="utf-8")

    # 孤儿图
    for rel, slug in ORPHANS.items():
        src = PUBLIC_IMAGES / rel
        if not src.exists():
            continue
        dest_dir = BLOGS / slug / "images"
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / src.name
        print(f"[孤儿] {rel} -> {slug}/images/{src.name}")
        if not args.dry_run:
            shutil.move(str(src), str(dest))

    print("\n---- 汇总 ----")
    print(f"站内/本地移动: {moved}  下载: {downloaded}  失败: {failed}  跳过: {skipped}")
    if collisions:
        print("重名加序号:")
        for line in collisions:
            print("   ", line)
    if leftovers:
        print("需人工处理:")
        for line in leftovers:
            print("   ", line)
    if args.dry_run:
        print("(dry-run，未改动任何文件)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
