---
title: "G33 整除分块"
publishDate: 2026-08-08
description: "整除分块：对 ⌊n/i⌋ 相同的区间合并计算。"
category: algo
tags:
  - 数学
language: zh
---
### 题目情境

**题目描述**

整除分块：对 $\lfloor n/i\rfloor$ 相同的区间合并计算。

**说明/提示**

本页为算法笔记。

### 算法解析：

整除分块：$\lfloor n/i\rfloor$ 的取值只有 $O(\sqrt n)$ 段，段 $[l,r]$ 内值相同，其中 $r=\lfloor n/\lfloor n/l\rfloor\rfloor$。对形如 $\sum_{i=1}^n f(i)\cdot\lfloor n/i\rfloor$ 的求和，可按段累加 $f$ 的区间和。复杂度 $O(\sqrt n)$。

### 备注

![image-20250808224555369](/images/算法竞赛/G/G33-1.png)

![image-20250808224637154](/images/算法竞赛/G/G33-2.png)
