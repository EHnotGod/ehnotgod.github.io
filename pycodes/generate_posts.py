"""
根据 src/总板子/A.md（代码）和 B.md（题目描述）自动生成各分章节的 Hexo 博文。
图片统一复制到 source/images/，引用路径改为 /images/filename。
"""
import re
import os
import shutil

BASE = r"C:\Users\DELL\Documents\GitHub\ehnotgod.github.io"
SRC     = os.path.join(BASE, r"src\总板子")
POSTS   = os.path.join(BASE, r"source\_posts\算法竞赛")
IMAGES  = os.path.join(BASE, r"source\images")

# 字母前缀 → 分类名
CAT = {
    'A': 'A 基础算法',
    'B': 'B 搜索算法',
    'C': 'C 数据结构',
    'D': 'D 图论',
    'E': 'E 动态规划',
    'F': 'F 字符串',
    'G': 'G 数学',
    'H': 'H 邪教',
    'I': 'I 典题',
}


# ─── 解析函数 ─────────────────────────────────────────────────────────────────

def parse_sections(fp):
    """
    解析 markdown，返回 [(title, body), ...] 列表。
    仅识别 ### 和 #### 开头的标题（排除代码块内部的伪标题）。
    """
    with open(fp, encoding='utf-8') as f:
        lines = f.readlines()

    sections = []
    cur_title = None
    cur_body = []
    in_code = False

    for line in lines:
        stripped = line.rstrip()
        # 切换代码块状态
        if stripped.startswith('```'):
            in_code = not in_code

        if not in_code:
            m = re.match(r'^#{3,4} (.+)$', stripped)
            if m:
                if cur_title is not None:
                    sections.append((cur_title, ''.join(cur_body).strip()))
                cur_title = m.group(1).strip()
                cur_body = []
                continue

        if cur_title is not None:
            cur_body.append(line)

    if cur_title is not None:
        sections.append((cur_title, ''.join(cur_body).strip()))

    return sections


def get_key(title):
    """从标题中提取节编号，如 'A1', 'C2.5', 'D99'。"""
    m = re.match(r'^([A-Z]\d+(?:\.\d+)*)', title)
    return m.group(1) if m else None


def get_prefix(title):
    m = re.match(r'^([A-Z])', title)
    return m.group(1) if m else None


def sort_key(k):
    """排序键：先按字母，再按数字（支持小数如 2.5）。"""
    m = re.match(r'^([A-Z])(\d+)((?:\.\d+)*)', k)
    if m:
        letter = m.group(1)
        num = int(m.group(2))
        sub = tuple(int(x) for x in m.group(3).split('.') if x)
        return (letter, num, sub)
    return (k, 0, ())


def fix_images(text):
    """将相对图片路径改为 /images/filename。"""
    return re.sub(
        r'!\[([^\]]*)\]\((?!https?://|/)([^)]+)\)',
        lambda m: f'![{m.group(1)}](/images/{os.path.basename(m.group(2))})',
        text,
    )


def extract_codes(text):
    """提取 Python 和 C++ 代码块。"""
    py  = re.findall(r'```python\n(.*?)```', text, re.DOTALL)
    cpp = re.findall(r'```c\+\+\n(.*?)```', text, re.DOTALL)
    return py, cpp


def make_post(title, category, b_body, py_blocks, cpp_blocks):
    """生成单篇博文内容字符串。"""
    tag = category.split(' ', 1)[1]
    # 标题含特殊字符时用引号包裹
    safe_title = title.replace('"', '\\"')
    lines = [
        '---',
        f'title: "{safe_title}"',
        'categories:',
        f'- [算法, {category}]',
        'tags:',
        f'- {tag}',
        '---',
        '',
    ]

    if b_body:
        lines += ['### 题目情境', '', b_body, '']

    if py_blocks:
        lines += ['### Python代码实现', '']
        for block in py_blocks:
            lines.append(f'```python\n{block.rstrip()}\n```')
            lines.append('')

    if cpp_blocks:
        lines += ['### C++代码实现', '']
        for block in cpp_blocks:
            lines.append(f'```c++\n{block.rstrip()}\n```')
            lines.append('')

    return '\n'.join(lines)


# ─── 主流程 ───────────────────────────────────────────────────────────────────

def main():
    # 1. 复制图片
    os.makedirs(IMAGES, exist_ok=True)
    n_img = 0
    for fn in os.listdir(SRC):
        if fn.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
            shutil.copy2(os.path.join(SRC, fn), os.path.join(IMAGES, fn))
            n_img += 1
    print(f"[图片] 已复制 {n_img} 张到 source/images/")

    # 2. 解析两个文件
    a_sections = parse_sections(os.path.join(SRC, 'A.md'))
    b_sections = parse_sections(os.path.join(SRC, 'B.md'))

    # 3. B.md 建立索引（key → 和 清理名 →）
    b_by_key  = {}   # 'A1' -> (title, body)
    b_by_name = {}   # '高精度加法' -> (title, body)

    for title, body in b_sections:
        k = get_key(title)
        if not k:
            continue
        b_by_key[k] = (title, body)
        clean = re.sub(r'^[A-Z]\d+(?:\.\d+)*\s*[、，,]?\s*', '', title).strip()
        b_by_name[clean] = (title, body)

    # 4. A.md 建立索引，无前缀节（如"二维前缀和"）按名称匹配到 B.md
    a_by_key = {}   # 'A1' -> [body, ...]

    for title, body in a_sections:
        k = get_key(title)
        if k:
            a_by_key.setdefault(k, []).append(body)
        else:
            # 尝试按名称匹配
            name = title.strip()
            if name in b_by_name:
                bk = get_key(b_by_name[name][0])
                if bk:
                    a_by_key.setdefault(bk, []).append(body)

    # 5. 合并所有条目（B.md 优先，A.md 补充）
    all_entries = {}  # key -> canonical title
    for k, (title, _) in b_by_key.items():
        all_entries[k] = title
    for title, _ in a_sections:
        k = get_key(title)
        if k and k not in all_entries:
            all_entries[k] = title

    # 6. 生成博文
    os.makedirs(POSTS, exist_ok=True)
    created = 0
    skipped = 0

    for k in sorted(all_entries.keys(), key=sort_key):
        title  = all_entries[k]
        prefix = get_prefix(title)
        if prefix not in CAT:
            skipped += 1
            continue

        category = CAT[prefix]

        _, b_body = b_by_key.get(k, (title, ''))
        b_body = fix_images(b_body)

        a_content = '\n\n'.join(a_by_key.get(k, []))
        py_blocks, cpp_blocks = extract_codes(a_content)

        post_content = make_post(title, category, b_body, py_blocks, cpp_blocks)

        folder = os.path.join(POSTS, category)
        os.makedirs(folder, exist_ok=True)

        safe = re.sub(r'[\\/:*?"<>|]', '_', title)
        fp = os.path.join(folder, f'{safe}.md')

        with open(fp, 'w', encoding='utf-8') as f:
            f.write(post_content)

        created += 1
        print(f'  [{k}] {title}')

    print(f'\n✓ 生成 {created} 篇博文，跳过 {skipped} 个无效节')


if __name__ == '__main__':
    main()
