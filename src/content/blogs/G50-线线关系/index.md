---
title: "G50 线线关系"
publishDate: 2026-08-08
description: "计算几何：直线与线段的位置关系。"
category: algo
tags:
  - 数学
language: zh
---
### 题目情境

**题目描述**

计算几何：直线/线段位置关系与点在凸多边形内判定。

**说明/提示**

本页为算法笔记。

### 算法解析：

叉积 $cross(A,B,C)=(B-A)\times(C-A)$ 判断三点顺序：正为逆时针，负为顺时针，零为共线。点在凸多边形内：遍历每条边，点始终位于边的同一侧（叉积同号）即在内部（边上也算）。

### 备注

![image-20250517205357054](/images/算法竞赛/G/G50-1.png)

### C++代码实现

```c++
struct Point {
    long long x, y;
};

__int128 cross(const Point& A, const Point& B, const Point& C) {
    return (__int128)(B.x - A.x) * (C.y - A.y) - (__int128)(B.y - A.y) * (C.x - A.x);
}

bool pointInConvexPolygon(const vector<Point>& poly, const Point& P) {
    int n = poly.size();
    int sign = 0;
    for (int i = 0; i < n; i++) {
        __int128 c = cross(poly[i], poly[(i+1)%n], P);
        if (c == 0) continue;              // 在边上也算 inside
        if (sign == 0) sign = (c > 0 ? 1 : -1);
        else if ((c > 0) != (sign > 0)) return false;
    }
    return true;
}
```
