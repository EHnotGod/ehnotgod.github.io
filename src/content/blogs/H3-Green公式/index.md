---
title: "H3 Green公式"
publishDate: 2026-09-02
description: "Green 公式：格林公式。"
category: algo
tags:
  - 其他
language: zh
---

### 题目情境

题目链接：https://qoj.ac/contest/2585/problem/14939

**题目描述**

![Problem D. 很多喷洒器](/images/算法竞赛/H/H3/H3-1.png)

### 算法解析：

这题求多个圆的面积并。做法是枚举每个圆，计算它的圆周被其他圆覆盖的角度区间，将这些区间合并，剩下的“裸露圆弧”就是圆并边界。然后利用 **Green 公式**

$$
S=\frac12\oint_{\partial\Omega}(x\,dy-y\,dx)
$$

把边界积分转成面积。对圆心 \((x_0,y_0)\)、半径 \(R\) 的圆弧 \(\theta\in[l,r]\)，参数化为

$$
x=x_0+R\cos\theta,\quad y=y_0+R\sin\theta
$$

代入 Green 公式，可得该圆弧的面积贡献

$$
\frac12\left[R^2(r-l)+Rx_0(\sin r-\sin l)+Ry_0(\cos l-\cos r)\right].
$$

把所有未被覆盖圆弧的贡献累加，即得到所有圆的并集面积。整体复杂度为

$$
O(n^2\log n).
$$

### py代码

```python
import math

PI = math.pi
TAU = 2 * PI
EPS = 1e-12

def solve():
    n = int(input())
    c = [tuple(map(float, input().split())) for _ in range(n)]
    ans = 0.0

    def arc(x, y, R, l, r):
        return (R*R*(r-l)
                + R*x*(math.sin(r)-math.sin(l))
                + R*y*(math.cos(l)-math.cos(r))) / 2

    for i, (x, y, R) in enumerate(c):
        seg = []
        covered = False

        for j, (X, Y, r) in enumerate(c):
            if i == j:
                continue

            dx, dy = X-x, Y-y
            d = math.hypot(dx, dy)

            # 重合圆，只保留一个
            if d < EPS and abs(R-r) < EPS:
                if j < i:
                    covered = True
                    break
                continue

            # 当前圆被完全覆盖
            if d + R <= r + EPS:
                covered = True
                break

            # 相离，或另一个圆完全在当前圆内部
            if d >= R+r-EPS or d+r <= R+EPS:
                continue

            a = math.atan2(dy, dx)
            co = (R*R + d*d - r*r) / (2*R*d)
            b = math.acos(max(-1, min(1, co)))

            l = (a-b) % TAU
            rr = (a+b) % TAU

            if l <= rr:
                seg.append((l, rr))
            else:
                seg.append((l, TAU))
                seg.append((0, rr))

        if covered:
            continue

        seg.sort()
        now = 0.0

        for l, r in seg:
            if l > now:
                ans += arc(x, y, R, now, l)
            now = max(now, r)

        if now < TAU:
            ans += arc(x, y, R, now, TAU)

    print(f"{ans:.15f}")

T = int(input())
for _ in range(T):
    solve()
```
