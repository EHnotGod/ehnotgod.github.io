---
title: "G27 求组合数-卢卡斯"
publishDate: 2026-08-08
description: "Lucas 定理：大组合数取模。"
category: algo
tags:
  - 数学
language: zh
---
### 题目情境

**题目描述**

求大组合数 $C(n,k)\bmod p$（$n,k$ 很大，$p$ 为素数）。

**说明/提示**

本页为算法笔记。

### 算法解析：

Lucas 定理：$C(n,k)\equiv C(n/p,k/p)\cdot C(n\%p,k\%p)\pmod p$（$p$ 为素数）。把 $n,k$ 按 $p$ 进制拆分逐位求组合数相乘。复杂度 $O(p\log_p n)$，适合 $p$ 较小而 $n,k$ 很大的情况。本篇为公式截图笔记，代码待补充。

### 备注

![image-20250808184920383](/images/算法竞赛/G/G27-1.png)

时间复杂度：$${O(plogp+log_pn)}$$
