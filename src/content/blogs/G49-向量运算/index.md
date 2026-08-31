---
title: "G49 向量运算"
publishDate: 2026-08-08
description: "向量运算：点积、叉积、模长等。"
category: algo
tags:
  - 数学
language: zh
---
### 题目情境

**题目描述**

向量的点积、模长与夹角计算。

**说明/提示**

本页为算法笔记。

### 算法解析：

向量运算：点积 $a\cdot b=x_ax_b+y_ay_b$，几何意义为模长乘夹角的余弦；模长 $|a|=\sqrt{x^2+y^2}$；夹角 $\theta=\arccos(a\cdot b/(|a||b|))$。叉积 $a\times b=x_ay_b-y_ax_b$ 表示有向面积与旋转方向。

### 备注

![image-20250517204844570](/images/算法竞赛/G/G49-1.png)

### Python代码实现

```python
import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def dot(a, b):  # 求点积
    return a.x * b.x + a.y * b.y

def length(a):  # 求模长
    return math.sqrt(a.x * a.x + a.y * a.y)

def angle(a, b):  # 求夹角（单位：弧度）
    return math.acos(dot(a, b) / (length(a) * length(b)))
```

### C++代码实现

```c++
double dot(Point a, Point b) { // 求点积
    return a.x * b.x + a.y * b.y;
}

double len(Point a) { // 求模长
    return sqrt(a.x * a.x + a.y * a.y);
}

double angle(Point a, Point b) { // 求夹角
    return acos(dot(a, b) / len(a) / len(b));
}
```
