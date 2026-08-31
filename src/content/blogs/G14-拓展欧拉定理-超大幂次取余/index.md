---
title: "G14 拓展欧拉定理-超大幂次取余"
publishDate: 2026-08-08
description: "扩展欧拉定理：超大幂次取模降幂。"
category: algo
tags:
  - 数学
language: zh
---

### 题目情境

**题目描述**

求超大幂次 $a^b \bmod m$（$b$ 极大，无法直接读入）。

**说明/提示**

本页为算法笔记。

### 算法解析：

扩展欧拉定理：当 $b\ge\varphi(m)$ 时 $a^b\equiv a^{b\bmod\varphi(m)+\varphi(m)}\pmod m$（$a$ 与 $m$ 互质时指数取 $b\bmod\varphi(m)$）。用于超大幂次取模降幂：先求 $\varphi(m)$，再把指数降下来快速幂。

没啥好说的，这个只需要记住公式就行了。

![image-20250808145039890](/images/算法竞赛/G/G14-1.png)
