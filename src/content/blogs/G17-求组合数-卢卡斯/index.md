---
title: "G17 求组合数-卢卡斯"
publishDate: 2026-08-08
description: "Lucas 定理：大组合数取模。"
category: algo
tags:
  - 数学
language: zh
---
### 题目情境

题目链接：https://www.luogu.com.cn/problem/P3807

**题目描述**

给定整数 $n, m, p$ 的值，求出 $C_{n + m}^n \bmod p$ 的值。

输入数据保证 $p$ 为质数。

注: $C$ 表示组合数。

**输入格式**

第一行一个整数 $T$，表示数据组数。

对于每组数据: 

一行，三个整数 $n, m, p$。

**输出格式**

对于每组数据，输出一行，一个整数，表示所求的值。

输入 #1

```
2
1 2 5
2 1 5
```

输出 #1

```
3
3
```

说明/提示

对于 $100\%$ 的数据，$1 \leq n, m, p \leq 10^5$，$1 \leq T \leq 10$。

### 算法解析：

Lucas 定理：$C(n,k)\equiv C(n/p,k/p)\cdot C(n\%p,k\%p)\pmod p$（$p$ 为素数）。把 $n,k$ 按 $p$ 进制拆分逐位求组合数相乘。复杂度 $O(p\log_p n)$，适合 $p$ 较小而 $n,k$ 很大的情况。本篇为公式截图笔记，代码待补充。

### c++代码

```c++
#include <iostream>
using namespace std;

typedef long long LL;
const int N = 100010;
LL f[N], g[N];

LL qpow(LL a, int b, int p){
  LL res = 1;
  while(b){
    if(b & 1) res=res*a%p;
    a = a*a%p;
    b >>= 1;
  }
  return res;
}
void init(int p){
  f[0] = g[0] = 1;
  for(int i=1; i<=p; i++){
    f[i] = f[i-1]*i%p;
    g[i] = g[i-1]*qpow(i,p-2,p)%p;
  }   
}
LL getC(int n, int m, int p){
  return f[n]*g[m]*g[n-m]%p;
}
int lucas(LL n, LL m, int p){
  if(m==0) return 1;
  return lucas(n/p,m/p,p)*getC(n%p,m%p,p)%p;
}
int main(){
  int q, n, m, p;
  cin >> q;
  while(q--){
    cin >> n >> m >> p;
    init(p);
    printf("%d\n",lucas(n+m,n,p));
  }
  return 0;
}
```