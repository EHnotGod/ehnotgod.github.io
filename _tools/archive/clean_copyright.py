# -*- coding: utf-8 -*-
"""清理 Copyright.astro 中的 Axi 签名 SVG 与赞助条"""
import re
from pathlib import Path

p = Path(r"src/components/pages/Copyright.astro")
text = p.read_text(encoding="utf-8")

# 1) 删除签名 SVG 容器
text, n1 = re.subn(
    r"<div class=\"absolute bottom-2 right-2 w-20 h-10 signature-container\">.*?</div>\n",
    "",
    text,
    count=1,
    flags=re.S,
)

# 2) 删除赞助条（Buy me a cup of coffee）
text, n2 = re.subn(
    r"<div class='mx-6 rounded-b-xl border border-t-0 px-3 pb-1\.5 pt-1 sm:mx-8 sm:px-4'>.*?</div>\n",
    "",
    text,
    count=1,
    flags=re.S,
)

p.write_text(text, encoding="utf-8")
print(f"signature removed: {n1}, sponsorship removed: {n2}")
