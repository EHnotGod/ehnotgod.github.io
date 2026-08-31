---
title: "G11 筛法求约数和"
publishDate: 2026-08-08
description: "线性筛求每个数的约数和。"
category: algo
tags:
  - 数学
language: zh
---
### 题目情境

**题目描述**

给定 $n$，输出 $1\sim n$ 每个数的约数和 $\sigma(i)$。

**说明/提示**

本页为算法笔记。

### 算法解析：

线性筛求约数和：质数 $\sigma(p)=p+1$；合数 $m=i\cdot p$：若 $p\mid i$ 用 $\sigma(m)=\sigma(i)\cdot(p^{a+1}-1)/(p-1)$ 合并，否则 $\sigma(m)=\sigma(i)\cdot(p+1)$。本篇代码待补充，思路同线性筛维护最小质因子次数。

