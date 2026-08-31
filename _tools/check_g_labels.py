# -*- coding: utf-8 -*-
import os, re, glob

BASE = os.path.join("src", "content", "blogs")
issues = []
for d in sorted(glob.glob(os.path.join(BASE, "G*"))):
    p = os.path.join(d, "index.md")
    with open(p, encoding="utf-8") as f:
        lines = f.read().split("\n")
    for i, line in enumerate(lines):
        m = re.match(r'^### (Python|C\+\+)代码实现', line)
        if m:
            expected = m.group(1)
            # 找标题后第一个代码块
            for j in range(i + 1, min(i + 4, len(lines))):
                cm = re.match(r'^```([A-Za-z0-9+]*)', lines[j])
                if cm:
                    lang = cm.group(1)
                    ok = (expected == "Python" and lang == "python") or (expected == "C++" and lang == "c++")
                    if not ok:
                        issues.append(f"{os.path.basename(d)}: 行{i+1} [{expected}] -> ```{lang}")
                    break
if issues:
    print("MISMATCH:")
    for s in issues:
        print(" ", s)
else:
    print("ALL G LABELS OK")
