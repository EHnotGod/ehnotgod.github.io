# -*- coding: utf-8 -*-
"""把 算法竞赛合集.md 编译成 PDF（markdown -> html -> PyMuPDF Story）。
用系统找到的中文字体；公式 $..$ 原样保留在文本中（Story 不渲染 LaTeX）。
"""
import os
import re
import html as html_mod
import markdown
import pymupdf

MD = os.path.join(os.getcwd(), "算法竞赛合集.md")
OUT = os.path.join(os.getcwd(), "算法竞赛合集.pdf")

# 读取 markdown
with open(MD, encoding="utf-8") as f:
    md_text = f.read()

# 预处理：把图片路径转为本地存在的文件或忽略；公式降级为普通文本去 $ 
# 找 public 下的实际图片绝对路径，若存在则转 file:// 供 Story 加载（Story 支持 img src）
md_text = re.sub(
    r'!\[([^\]]*)\]\((/images/[^)]+)\)',
    lambda m: f'![{m.group(1)}](file:///D:/Desktop/github_tasks/ehnotgod.github.io/public{m.group(2)})',
    md_text,
)

# markdown -> html
body_html = markdown.markdown(
    md_text,
    extensions=["fenced_code", "tables", "sane_lists", "nl2br"],
)

# 包一层完整 HTML（含基础 CSS）
css = """
<style>
  body { font-family: "Microsoft YaHei","SimSun","Noto Sans CJK SC",sans-serif; font-size: 10.5pt; line-height: 1.5; }
  h1 { font-size: 20pt; page-break-before: always; color: #1a5276; border-bottom: 2px solid #1a5276; padding-bottom: 4px; }
  h1:first-of-type { page-break-before: avoid; }
  h2 { font-size: 14pt; color: #1f618d; border-left: 4px solid #2980b9; padding-left: 8px; margin-top: 18px; }
  h3 { font-size: 12pt; color: #2c3e50; }
  code { font-family: "Consolas","Courier New",monospace; background: #f4f4f4; padding: 1px 3px; border-radius: 3px; font-size: 9pt; }
  pre { background: #f8f8f8; border: 1px solid #ddd; border-radius: 4px; padding: 8px; font-size: 8.5pt; line-height: 1.35; white-space: pre-wrap; word-wrap: break-word; }
  pre code { background: none; padding: 0; }
  blockquote { color: #555; border-left: 4px solid #ccc; margin-left: 0; padding-left: 12px; }
  table { border-collapse: collapse; width: 100%; }
  th, td { border: 1px solid #bbb; padding: 4px 8px; }
  img { max-width: 100%; }
  a { color: #2980b9; }
</style>
"""

html_full = f"<!DOCTYPE html><html><head><meta charset='utf-8'>{css}</head><body>{body_html}</body></html>"

with open(os.path.join(os.getcwd(), "算法竞赛合集.html"), "w", encoding="utf-8") as f:
    f.write(html_full)
print("HTML 生成:", len(html_full) // 1024, "KB")

# PyMuPDF Story 渲染
doc = pymupdf.open()
writer = pymupdf.DocumentWriter(OUT)
from pymupdf import paper_rect
try:
    story = pymupdf.Story(html=html_full, archive=pymupdf.Archive(os.path.join("public", "images")))
except Exception as e:
    print("Story 初始化失败:", e)
    raise

# 设置字体（中文字体需要注册，否则可能缺字）
# Story 用 archive 解析本地图片
more = 1
page_count = 0
rect = paper_rect("a4")
while more:
    dev = writer.begin_page(rect)
    more, _ = story.place(dev)
    writer.end_page()
    page_count += 1
    if page_count > 4000:
        print("页数超限，中断")
        break
writer.close()
print(f"PDF 生成完成：{OUT}，共 {page_count} 页")
