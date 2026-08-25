# -*- coding: utf-8 -*-
"""
只重新生成每篇文章 frontmatter 的 description 字段（保留数学变量、清理标点空格）。
不修改正文内容。
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BLOGS = ROOT / "src" / "content" / "blogs"


def math_to_text(s: str) -> str:
    """把 LaTeX 片段转成可读纯文本（保留变量名）"""
    s = re.sub(r"\\le(q)?\b", "≤", s)
    s = re.sub(r"\\ge(q)?\b", "≥", s)
    s = re.sub(r"\\times\b", "×", s)
    s = re.sub(r"\\cdot\b", "·", s)
    s = re.sub(r"\\dots\b", "…", s)
    s = re.sub(r"\\ldots\b", "…", s)
    s = re.sub(r"\\cdots\b", "…", s)
    s = re.sub(r"\\sim\b", "~", s)
    s = re.sub(r"\\sum\b", "∑", s)
    s = re.sub(r"\\min\b", "min", s)
    s = re.sub(r"\\max\b", "max", s)
    s = re.sub(r"\\ne\b", "≠", s)
    s = re.sub(r"\\in\b", "∈", s)
    s = re.sub(r"\\le\b", "≤", s)
    s = re.sub(r"\\ge\b", "≥", s)
    # \frac{a}{b} -> a/b
    s = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", r"\1/\2", s)
    # \text{x}, \operatorname{x}, \mathrm{x}, \mathbf{x}, \mathbb{x} -> x
    s = re.sub(
        r"\\(?:operatorname|text|mathrm|mathbf|mathbb|mathit|mathsf)\{([^{}]*)\}",
        r"\1",
        s,
    )
    # 下标 {..} -> [..]；上标 {..} -> ^..
    s = re.sub(r"\_\{([^{}]*)\}", r"[\1]", s)
    s = re.sub(r"\^\{([^{}]*)\}", r"^\1", s)
    # 残余 { } 去掉
    s = re.sub(r"[{}]", "", s)
    # 去掉剩余反斜杠命令
    s = re.sub(r"\\[a-zA-Z]+\s*", "", s)
    s = s.replace("\\", "")
    return s.strip()


def make_description(body: str, max_len: int = 150) -> str:
    text = re.sub(r"```.*?```", " ", body, flags=re.S)  # 去代码块
    text = re.sub(r"!\[.*?\]\(.*?\)", " ", text)  # 去图片
    text = re.sub(r"`[^`]*`", " ", text)  # 去行内代码
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)  # 链接保留文字
    text = re.sub(r"[*_>`~]", " ", text)  # 去强调符号
    # 数学公式 -> 可读文本（保留变量名）
    text = re.sub(r"\$\$(.*?)\$\$", lambda m: math_to_text(m.group(1)), text, flags=re.S)
    text = re.sub(r"\$([^$]+)\$", lambda m: math_to_text(m.group(1)), text)
    def is_link_line(p: str) -> bool:
        # 跳过纯链接/"题目链接：https://..." 这类行，不适合当描述
        if re.match(r"^https?://", p):
            return True
        if re.match(r"^[^\n：:]*[：:]\s*https?://", p):
            return True
        return False

    # 找第一段（跳过标题行、跳过过短的标签行、跳过链接行）
    paragraphs = [
        p.strip()
        for p in text.split("\n")
        if p.strip()
        and not p.strip().startswith("#")
        and len(p.strip()) >= 15
        and not is_link_line(p.strip())
    ]
    desc = paragraphs[0] if paragraphs else ""
    # 清理空白与中文标点前后空格
    desc = re.sub(r"\s+", " ", desc).strip()
    desc = re.sub(r"\s*([，。；：！？、])\s*", r"\1", desc)
    desc = re.sub(r"\s+([,.;:!?])", r"\1", desc)
    if len(desc) > max_len:
        desc = desc[:max_len].rstrip() + "…"
    return desc or "算法学习笔记"


def main():
    changed, samples = 0, []
    for md in sorted(BLOGS.rglob("index.md")):
        text = md.read_text(encoding="utf-8")
        m = re.match(r"^(---\s*\n)(.*?)(\n---)", text, re.S)
        if not m:
            continue
        head, fm, tail = m.group(1), m.group(2), m.group(3)
        body = text[m.end():]
        new_desc = make_description(body)
        new_desc_esc = new_desc.replace("\\", "\\\\").replace('"', '\\"')
        old_line = re.search(r"^description:.*$", fm, re.M)
        old_desc = old_line.group(0).replace("description: ", "").strip('"') if old_line else ""
        new_fm = re.sub(r"^description:.*$", f'description: "{new_desc_esc}"', fm, count=1, flags=re.M)
        if new_fm != fm:
            md.write_text(head + new_fm + tail + body, encoding="utf-8")
            changed += 1
            samples.append((md.parent.name, old_desc, new_desc))

    print(f"== 更新了 {changed} 篇文章的 description ==")
    print("\n-- 抽查前 12 篇（旧 → 新）--")
    for name, old, new in samples[:12]:
        print(f"\n[{name}]\n  旧: {old}\n  新: {new}")


if __name__ == "__main__":
    main()
