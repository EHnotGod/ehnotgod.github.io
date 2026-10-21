---
title: "G16 求组合数-线性逆推"
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

### 算法解析：

线性逆推求组合数：预处理阶乘 $fac$ 与逆阶乘 $inv$。$fac[n]$ 用快速幂求逆得 $inv[n]$，再倒推 $inv[i-1]=inv[i]\cdot i$。则 $C(n,k)=fac[n]\cdot inv[k]\cdot inv[n-k]\bmod p$。查询 $O(1)$，预处理 $O(N)$。

### Python代码实现

```python
# 按当前查询所需的最大 n 预处理阶乘和逆阶乘。
MOD = 10**9 + 7

def init(n):
    fac = [1] * (n + 1)
    inv = [1] * (n + 1)
    for i in range(1, n + 1):
        fac[i] = fac[i - 1] * i % MOD
    inv[n] = pow(fac[n], MOD - 2, MOD)
    for i in range(n, 0, -1):
        inv[i - 1] = inv[i] * i % MOD
    return fac, inv

def C(n, k, fac, inv):
    if k < 0 or k > n:
        return 0
    return fac[n] * inv[k] % MOD * inv[n - k] % MOD

# 多次查询时，先按所有查询的最大 n 调用一次 init。
n, k = 10, 3
fac, inv = init(n)
print(C(n, k, fac, inv))  # 输出 120
```
