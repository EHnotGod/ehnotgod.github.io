---
title: "G13 费马小定理"
publishDate: 2026-08-08
description: "费马小定理：a^(p-1) ≡ 1 (mod p)。"
category: algo
tags:
  - 数学
language: zh
---
### 题目情境

**题目描述**

给定 $a,p$（$p$ 为素数且 $a$ 与 $p$ 互质），求 $a$ 在模 $p$ 下的乘法逆元。

**说明/提示**

本页为算法笔记。

### 算法解析：

费马小定理：$p$ 为素数且 $\gcd(a,p)=1$ 时 $a^{p-1}\equiv1\pmod p$，故 $a\cdot a^{p-2}\equiv1\pmod p$，即逆元 $a^{-1}\equiv a^{p-2}\pmod p$。用快速幂求 $a^{p-2}\bmod p$ 即可。

### 备注

没啥好说的，直接记结论得了。

![image-20250418170352053](/images/算法竞赛/G/G13-1.png)

### Python代码实现

```python
a, p = map(int, input().split())
print(pow(a, p - 2, p))
```

### C++代码实现

```c++
#include<iostream>
using namespace std;

typedef long long LL;
int a, p;

int quickpow(LL a, int b, int p){
  int res = 1;
  while(b){
    if(b & 1) res = res*a%p;
    a = a*a%p;
    b >>= 1;
  }
  return res;
}
int main(){
  cin >> a >> p;
  if(a % p)
    printf("%d\n",quickpow(a,p-2,p));
  return 0;
}
```
