---
title: "G37 迪利克雷卷积"
publishDate: 2026-08-08
description: "狄利克雷卷积：积性函数卷积运算。"
category: algo
tags:
  - 数学
language: zh
---
### 题目情境

**题目描述**

狄利克雷卷积：积性函数的卷积运算。

**说明/提示**

本页为算法笔记。

### 算法解析：

狄利克雷卷积：$(f*g)(n)=\sum_{d\mid n}f(d)g(n/d)$，两个积性函数的卷积仍为积性函数。常见恒等式：$\mu*1=\epsilon$、$\varphi*1=id$、$id*\mu=\varphi$，是莫比乌斯反演的理论基础。

### 备注

![image-20251107164853574](/images/算法竞赛/G/G37-1.png)
