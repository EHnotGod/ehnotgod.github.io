---
title: "G32 卡特兰数"
publishDate: 2026-08-08
description: "卡特兰数：入栈出栈 / 括号匹配等计数。"
category: algo
tags:
  - 数学
language: zh
---
### 题目情境

**题目描述**

卡特兰数：入栈出栈 / 括号匹配等计数。

**说明/提示**

本页为算法笔记。

### 算法解析：

卡特兰数：$Cat_n=\frac{1}{n+1}C(2n,n)=\sum_{i=0}^{n-1}Cat_i\cdot Cat_{n-1-i}$，$Cat_0=1$。计数对象包括：$n$ 对括号合法序列、$n$ 个元素入栈出栈序列、$n$ 个节点二叉树形态、凸多边形三角剖分数等。递推式 $Cat_{n+1}=\frac{4n+2}{n+2}Cat_n$。

### 备注

![image-20250808223834012](/images/算法竞赛/G/G32-1.png)
