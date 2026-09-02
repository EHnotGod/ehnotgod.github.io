---
title: "G31 圆排列、错排数"
publishDate: 2026-09-02
description: "圆排列与错排数：环形排列与全错位排列计数。"
category: algo
tags:
  - 数学
language: zh
---
### 题目情境

**题目描述**

圆排列：把 $n$ 个不同元素排成一圈（旋转视为同一种）的方案数；错排数 $D_n$：把 $n$ 个元素重新排列，使得每个元素都不在原来的位置上的方案数。

**说明/提示**

本页为算法笔记。

### 算法解析：

**圆排列**：$n$ 个不同元素的直线排列有 $n!$ 种；排成一圈时，任意旋转后相同算同一种，且每 $n$ 个旋转对应一个圆排列，故圆排列数为 $\frac{n!}{n}=(n-1)!$。

**错排数**：$D_n$ 表示 $n$ 个元素的错排数（每个元素都不在自己原位）。递推式 $D_n=(n-1)(D_{n-1}+D_{n-2})$，边界 $D_0=1,\ D_1=0$。含义：元素 $1$ 与某个 $i\ (i\ne1)$ 互换后，剩余 $n-2$ 个错排（$D_{n-2}$）；或 $1$ 与 $i$ 互换但 $i$ 仍可能错排（先看成 $n-1$ 规模的错排 $D_{n-1}$），共 $n-1$ 种选择。也可用容斥 $D_n=n!\sum_{i=0}^n\frac{(-1)^i}{i!}$。

### Python代码实现

```python
MOD = 10**9 + 7

# 圆排列：(n-1)!  mod MOD
def circle(n):
    res = 1
    for i in range(2, n):
        res = res * i % MOD
    return res

# 错排数：D_n = (n-1)(D_{n-1}+D_{n-2})
def derange(n):
    d = [0] * (n + 1)
    d[0], d[1] = 1, 0  # D0 = 1, D1 = 0
    for i in range(2, n + 1):
        d[i] = (i - 1) * (d[i - 1] + d[i - 2]) % MOD
    return d[n]
```

### C++代码实现

```c++
#include <bits/stdc++.h>
using namespace std;

typedef long long LL;
const LL MOD = 1e9 + 7;

LL circle(int n) { // 圆排列 (n-1)!
  LL res = 1;
  for (int i = 2; i < n; i++) res = res * i % MOD;
  return res;
}

LL derange(int n) { // 错排数 D_n
  vector<LL> d(n + 1);
  d[0] = 1; d[1] = 0;
  for (int i = 2; i <= n; i++)
    d[i] = (i - 1) * (d[i - 1] + d[i - 2]) % MOD;
  return d[n];
}

int main() {
  int n;
  cin >> n;
  cout << "圆排列: " << circle(n) << "\n";
  cout << "错排数: " << derange(n) << "\n";
  return 0;
}
```
