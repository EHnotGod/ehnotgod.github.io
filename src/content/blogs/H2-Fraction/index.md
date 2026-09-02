---
title: "H2 Fraction"
publishDate: 2026-09-02
description: "Fraction：分数相关算法。"
category: algo
tags:
  - 其他
language: zh
---

### 题目情境

**题目描述**

亿万富翁 Cai 有一个非常特别的执念：只有当他的双脚牢牢踩在瓷砖的**边或顶点**上——也就是说，踩在地板瓷砖的边界上——他才会觉得舒服。

最近，他购入了一批完全相同的高档**三角形地砖**，准备使用这些地砖铺满他新豪宅里一条又长又直的走廊。

走廊可以视为二维笛卡尔平面上的一条**无限长带状区域**。

为了满足 Cai 极其严格的要求，每一块三角形地砖都必须横跨走廊的整个宽度，也就是说：每一块三角形地砖都必须同时接触走廊的两条平行边界线。

这样可以形成一个连续的、单行的三角形铺砌。

其中有一块地砖必须恰好与 Cai 最喜欢的参考三角形

$$
\triangle ABC
$$

完全重合，而所有其他地砖都必须与它**全等**。

Cai 目前正站在走廊中的一个固定位置。

经过一天漫长而疲惫的改造工作之后，他已经筋疲力尽，并且无论如何都不愿意再移动。

他希望这些瓷砖能够从参考三角形开始，自动向走廊两侧不断铺开，并且最终形成一个满足上述规则的铺砌。

当然，只有当：Cai 当前所在的点 \(D\) 恰好位于某块三角形地砖的**一条边上或者一个顶点上**

时，他才认为这次铺砌是成功的。

你的任务是判断：是否存在一种合法的走廊铺砌方式，使得点 \(D\) 恰好位于包含 \(\triangle ABC\) 的整个三角形铺砌中的某条边或某个顶点上？

走廊的两条边界定义为两条唯一确定的平行直线

$$
l_1,\ l_2,
$$

其中：

* \(l_1\) 经过点 \(A\) 和 \(B\)；
* \(l_2\) 经过点 \(C\)。

由 \((l_1,l_2)\) 所形成的带状区域的一种**铺砌（tessellation）**，指的是：使用与 \(\triangle ABC\) 全等的三角形，通过平移、旋转和翻转，将整个无限长带状区域恰好铺满，且所有三角形之间**没有重叠，也没有空隙**。

**输入格式

有多组测试数据。

第一行包含一个整数

$$
T\qquad(1\le T\le10^3),
$$

表示测试用例数量。

对于每组测试数据：

第一行包含两个整数

$$
x_a,\ y_a
\qquad(-100\le x_a,y_a\le100),
$$

表示点 \(A\) 的坐标。

第二行包含两个整数

$$
x_b,\ y_b
\qquad(-100\le x_b,y_b\le100),
$$

表示点 \(B\) 的坐标。

第三行包含两个整数

$$
x_c,\ y_c
\qquad(-100\le x_c,y_c\le100),
$$

表示点 \(C\) 的坐标。

第四行包含两个分数

$$
\frac{x_{d1}}{x_{d2}}
\qquad\text{和}\qquad
\frac{y_{d1}}{y_{d2}},
$$

其中

$$
-10^7<x_{d1},y_{d1}<10^7,
$$

并且

$$
0<x_{d2},y_{d2}<10^7.
$$

它们分别表示点 \(D\) 的 \(x\) 坐标与 \(y\) 坐标，即

$$
D=
\left(
\frac{x_{d1}}{x_{d2}},
\frac{y_{d1}}{y_{d2}}
\right).
$$

保证：

$$
A,B,C
$$

构成一个**非退化三角形**，即三点不共线。

**输出格式**

对于每组测试数据：

如果存在一种合法铺砌，使得点 \(D\) 位于铺砌中的至少一个三角形的**边或顶点**上，输出：

```text
Yes
```

否则输出：

```text
No
```

**样例输入**

```text
4
-2 1
0 0
0 2
2/1 0/1
-2 1
0 0
0 2
1/1 0/1
0 1
-2 1
0 2
1/2 7/4
0 1
-2 1
0 2
-3/2 3/4
```

**样例输出**

```text
Yes
No
Yes
No
```

图中的前两个样例可以理解为：

* **Case 1：Yes**：点 \(D\) 正好落在某条三角形边界上；
* **Case 2：No**：点 \(D\) 落在某个三角形的内部，因此不满足要求。

这道题的核心其实不是一般意义上的“三角形铺砖搜索”，而是要研究：**一个三角形横跨两条平行线以后，沿走廊方向不断翻折/镜像铺砌，其所有边界点会形成什么样的周期结构。**

![铺砌示意图](/images/算法竞赛/H/H2/H2-1.png)

### 算法解析：

略，主要是介绍Fraction的用法

### py代码：

```python
import fractions
t = int(input())

def cross(a, b):
    return a.x * b.y - b.x * a.y

class pt:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, p):
        return pt(self.x + p.x,
                  self.y + p.y)
    def __sub__(self, p):
        return pt(self.x - p.x,
                  self.y - p.y)
    def __mul__(self, d):
        return pt(self.x * d,
                self.y * d)
    def __truediv__(self, d):
        return pt(self.x / d,
                self.y / d)
    def __str__(self):
        return f"({self.x}, {self.y})"
    def __eq__(self, p):
        return self.x == p.x and self.y == p.y

class line:
    def __init__(self, p, q):
        self.v = q - p
        self.c = cross(self.v, p)

def side(ln, p):
    return cross(ln.v, p) - ln.c

def inter(l1, l2):
    d = cross(l1.v, l2.v)
    return (l2.v * l1.c - l1.v * l2.c) / d

def dot(v, w):
    return v.x* w.x+ v.y* w.y




def slave():
    xa, ya = map(int, input().split())
    xb, yb = map(int, input().split())
    xc, yc = map(int, input().split())
    xa_f = fractions.Fraction(xa, 1)
    ya_f = fractions.Fraction(ya, 1)
    xb_f = fractions.Fraction(xb, 1)
    yb_f = fractions.Fraction(yb, 1)
    xc_f = fractions.Fraction(xc, 1)
    yc_f = fractions.Fraction(yc, 1)
    a = pt(xa_f, ya_f)
    b = pt(xb_f, yb_f)
    c = pt(xc_f, yc_f)
    xd, yd = input().split()
    xd1, xd2 = map(int, xd.split("/"))
    yd1, yd2 = map(int, yd.split("/"))
    xd_f = fractions.Fraction(xd1, xd2)
    yd_f = fractions.Fraction(yd1, yd2)
    d = pt(xd_f, yd_f)

    ln_ab = line(a, b)
    ln_c = line(c, b - a + c)

    # 看看在不在线上
    if cross(a - b, a - d) == 0 or cross(a - b, c - d) == 0:
        return 1
    # 看看在不在线内
    if side(ln_ab, d) * side(ln_c, d) > 0:
        return 0
    ln1 = line(d, d + c - a)
    ln2 = line(d, d + c - b)
    h1 = inter(ln1, ln_c)
    h2 = inter(ln2, ln_c)
    def pan(h, can=c):
        f1 = 0; f2 = 0
        if (b - a).x == 0 or (h - can).x % abs((b - a).x) == 0:
            f1 = 1
        if (b - a).y == 0 or (h - can).y % abs((b - a).y) == 0:
            f2 = 1
        return f1 and f2

    if pan(h1) or pan(h2):
        return 1
    if dot(a - b, a - c) == 0:
        ln3 = line(d, d + c - a * 2+ b)
        h3 = inter(ln3, ln_ab)
        if h3 != a and pan(h3, a):
            return 1
    if dot(a - b, b - c) == 0:
        ln3 = line(d, d + c + a - b * 2)
        h3 = inter(ln3, ln_ab)
        if h3 != b and pan(h3, b):
            return 1

    return 0

for _ in range(t):
    print("Yes" if slave() else "No")
```

