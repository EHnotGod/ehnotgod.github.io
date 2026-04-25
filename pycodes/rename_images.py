"""
将 source/images/ 中的时间戳图片重命名为 节编号-序号.ext 格式，
同时更新所有 source/_posts/算法竞赛/ 下 md 文件的引用路径。
"""
import re
import os

BASE   = r"C:\Users\DELL\Documents\GitHub\ehnotgod.github.io"
SRC_A  = os.path.join(BASE, r"src\总板子\A.md")
SRC_B  = os.path.join(BASE, r"src\总板子\B.md")
IMAGES = os.path.join(BASE, r"source\images")
POSTS  = os.path.join(BASE, r"source\_posts\算法竞赛")


def parse_section_images(fp):
    """返回 {section_key: [img_filename, ...]} 保持出现顺序，去重。"""
    with open(fp, encoding='utf-8') as f:
        lines = f.readlines()

    result   = {}   # key -> [list of img filenames in order]
    cur_key  = None
    seen_in_section = {}
    in_code  = False

    for line in lines:
        stripped = line.rstrip()
        if stripped.startswith('```'):
            in_code = not in_code
        if in_code:
            continue

        m_head = re.match(r'^#{3,4} (.+)$', stripped)
        if m_head:
            title = m_head.group(1).strip()
            m_key = re.match(r'^([A-Z]\d+(?:\.\d+)*)', title)
            cur_key = m_key.group(1) if m_key else None
            if cur_key and cur_key not in result:
                result[cur_key] = []
                seen_in_section[cur_key] = set()
            continue

        if cur_key is None:
            continue

        # 匹配图片引用（相对路径或绝对路径 /images/...）
        for img_m in re.finditer(
            r'!\[[^\]]*\]\((?:/images/)?([^)]+)\)', stripped
        ):
            fname = os.path.basename(img_m.group(1))
            if fname not in seen_in_section[cur_key]:
                result[cur_key].append(fname)
                seen_in_section[cur_key].add(fname)

    return result


def build_rename_map(a_imgs, b_imgs):
    """合并两份图片列表，构建 old_name -> new_name 映射。"""
    mapping = {}
    # 合并：以 B.md 为基础，A.md 补充
    all_keys = list(dict.fromkeys(list(b_imgs.keys()) + list(a_imgs.keys())))

    for key in all_keys:
        imgs_b = b_imgs.get(key, [])
        imgs_a = a_imgs.get(key, [])
        # 合并去重，保持顺序
        seen = set()
        combined = []
        for f in imgs_b + imgs_a:
            if f not in seen:
                combined.append(f)
                seen.add(f)

        for idx, fname in enumerate(combined, 1):
            if fname in mapping:
                continue  # 同一图片若出现在多节，只命名一次
            ext = os.path.splitext(fname)[1].lower()
            new_name = f"{key}-{idx}{ext}"
            mapping[fname] = new_name

    return mapping


def rename_images(mapping):
    """重命名 source/images/ 下的文件。"""
    renamed = 0
    for old, new in mapping.items():
        src = os.path.join(IMAGES, old)
        dst = os.path.join(IMAGES, new)
        if os.path.exists(src) and not os.path.exists(dst):
            os.rename(src, dst)
            renamed += 1
        elif not os.path.exists(src):
            print(f"  [警告] 源文件不存在: {old}")
    print(f"[图片] 已重命名 {renamed} 张")


def update_md_files(mapping):
    """更新所有博文中的图片引用。"""
    updated = 0
    for root, _, files in os.walk(POSTS):
        for fn in files:
            if not fn.endswith('.md'):
                continue
            fp = os.path.join(root, fn)
            with open(fp, encoding='utf-8') as f:
                content = f.read()

            new_content = content
            for old, new in mapping.items():
                # 替换 /images/old_name
                new_content = new_content.replace(
                    f'/images/{old}', f'/images/{new}'
                )

            if new_content != content:
                with open(fp, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                updated += 1

    print(f"[博文] 已更新 {updated} 篇 md 文件中的图片引用")


def main():
    print("解析图片引用...")
    a_imgs = parse_section_images(SRC_A)
    b_imgs = parse_section_images(SRC_B)

    print("构建重命名映射...")
    mapping = build_rename_map(a_imgs, b_imgs)
    for old, new in sorted(mapping.items(), key=lambda x: x[1]):
        print(f"  {old}  →  {new}")

    print(f"\n共 {len(mapping)} 张图片待重命名")
    rename_images(mapping)
    update_md_files(mapping)
    print("\n完成！")


if __name__ == '__main__':
    main()
