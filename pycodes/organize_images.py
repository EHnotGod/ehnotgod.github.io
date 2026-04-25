"""
1. 扫描所有博文 md，收集被引用的图片名
2. 删除 source/images/ 下未被引用的图片（保留 avatar/background/wechatpay 等系统图片）
3. 按前缀字母分子目录（A/、B/、... 、I/），移动图片并更新 md 引用
"""
import re
import os
import shutil

BASE   = r"C:\Users\DELL\Documents\GitHub\ehnotgod.github.io"
IMAGES = os.path.join(BASE, r"source\images")
POSTS  = os.path.join(BASE, r"source\_posts\算法竞赛")

# 不参与整理的系统图片
SYSTEM = {'avatar.png', 'background.png', 'wechatpay.png',
          'apple-touch-icon-next.png', 'favicon-32x32-next.png',
          'favicon-16x16-next.png', 'logo.svg'}


def collect_referenced(posts_root):
    """返回所有博文中引用的图片文件名集合，以及 {filename: [fp, ...]} 出现位置。"""
    refs = {}   # filename -> [md file path]
    for root, _, files in os.walk(posts_root):
        for fn in files:
            if not fn.endswith('.md'):
                continue
            fp = os.path.join(root, fn)
            with open(fp, encoding='utf-8') as f:
                content = f.read()
            for m in re.finditer(r'!\[[^\]]*\]\(/images/([^)]+)\)', content):
                img = m.group(1)
                # 去掉可能已有的子目录前缀（如 A/A12-1.png）
                basename = os.path.basename(img)
                refs.setdefault(basename, []).append(fp)
    return refs


def get_subdir(filename):
    """根据文件名前缀决定子目录，如 A12-1.png -> A，B6-1.png -> B。"""
    m = re.match(r'^([A-Z])\d', filename)
    return m.group(1) if m else None


def main():
    print("─── 扫描引用 ─────────────────────────────")
    refs = collect_referenced(POSTS)
    print(f"博文共引用 {len(refs)} 张图片")

    # 列出 source/images/ 下所有普通文件（不含子目录）
    all_imgs = {
        fn for fn in os.listdir(IMAGES)
        if os.path.isfile(os.path.join(IMAGES, fn))
    }

    # ── 1. 删除未引用图片 ──────────────────────────────────────
    print("\n─── 删除未引用图片 ──────────────────────")
    deleted = 0
    for fn in sorted(all_imgs):
        if fn in SYSTEM:
            continue
        basename = os.path.basename(fn)
        if basename not in refs:
            os.remove(os.path.join(IMAGES, fn))
            print(f"  删除: {fn}")
            deleted += 1
    print(f"共删除 {deleted} 张未引用图片")

    # ── 2. 创建子目录并移动图片，更新 md 引用 ──────────────────
    print("\n─── 整理到子目录 ────────────────────────")
    # 重新读取 refs（文件名 -> md路径列表）
    moved = 0
    skipped = 0
    rename_map = {}   # old_path_in_url -> new_path_in_url，用于 md 替换

    for basename, md_files in refs.items():
        subdir = get_subdir(basename)
        if subdir is None:
            skipped += 1
            continue

        src = os.path.join(IMAGES, basename)
        dst_dir = os.path.join(IMAGES, subdir)
        dst = os.path.join(dst_dir, basename)

        if not os.path.exists(src):
            print(f"  [警告] 文件不存在: {basename}")
            continue

        os.makedirs(dst_dir, exist_ok=True)
        shutil.move(src, dst)
        moved += 1

        old_url = f'/images/{basename}'
        new_url = f'/images/{subdir}/{basename}'
        rename_map[old_url] = new_url

    print(f"共移动 {moved} 张，跳过无前缀 {skipped} 张")

    # ── 3. 批量更新所有 md 文件 ──────────────────────────────
    print("\n─── 更新 md 引用 ─────────────────────────")
    updated = 0
    for root, _, files in os.walk(POSTS):
        for fn in files:
            if not fn.endswith('.md'):
                continue
            fp = os.path.join(root, fn)
            with open(fp, encoding='utf-8') as f:
                content = f.read()
            new_content = content
            for old_url, new_url in rename_map.items():
                new_content = new_content.replace(old_url, new_url)
            if new_content != content:
                with open(fp, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                updated += 1
    print(f"共更新 {updated} 篇 md 文件")
    print("\n完成！")


if __name__ == '__main__':
    main()
