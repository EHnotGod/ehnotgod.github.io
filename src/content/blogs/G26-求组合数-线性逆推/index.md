---
title: "G26 求组合数-线性逆推"
publishDate: 2026-08-08
description: "组合数：线性递推求逆元计算 C(n,k)。"
category: algo
tags:
  - 数学
language: zh
---
### 题目情境

**题目描述**

求组合数 $C(n,k)$（模 $10^9+7$）。

**说明/提示**

本页为算法笔记。

### 算法解析：

线性逆推求组合数：预处理阶乘 $fac$ 与逆阶乘 $inv$。$fac[n]$ 用快速幂求逆得 $inv[n]$，再倒推 $inv[i-1]=inv[i]\cdot i$。则 $C(n,k)=fac[n]\cdot inv[k]\cdot inv[n-k]\bmod p$。查询 $O(1)$，预处理 $O(N)$。

### Python代码实现

```python
# 逆推法（阶乘 + 快速幂 + 模逆）
MOD = 10**9 + 7
N = 10**6  # 最大 n

# 预处理阶乘和逆阶乘
fac = [1] * (N + 1)
inv = [1] * (N + 1)

# 计算阶乘
for i in range(1, N + 1):
    fac[i] = fac[i - 1] * i % MOD

# 快速幂
def qpow(a, b):
    res = 1
    while b:
        if b & 1:
            res = res * a % MOD
        a = a * a % MOD
        b >>= 1
    return res

# 计算逆阶乘
inv[N] = qpow(fac[N], MOD - 2)
for i in range(N, 0, -1):
    inv[i - 1] = inv[i] * i % MOD

# 组合数函数
def C(n, k):
    if k < 0 or k > n:
        return 0
    return fac[n] * inv[k] % MOD * inv[n - k] % MOD

# 使用：
print(C(10, 3))  # 输出 120
```
