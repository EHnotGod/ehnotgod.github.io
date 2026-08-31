---
title: "G1 快速幂"
publishDate: 2026-08-08
description: "快速幂：二分求 a^b mod p。"
category: algo
tags:
  - 数学
language: zh
---
### 题目情境

题目链接：https://www.luogu.com.cn/problem/P1226

**题目描述**

给你三个整数 $$a,b,p$$，求 $$a^b \bmod p$$。

**输入格式**

输入只有一行三个整数，分别代表 $$a,b,p$$。

**输出格式**

输出一行一个字符串 `a^b mod p=s`，其中 $$a,b,p$$ 分别为题目给定的值， $$s$$ 为运算结果。

输入 #1

```
2 10 9
```

输出 #1

```
2^10 mod 9=7
```

对于 $$100\%$$ 的数据，保证 $$0\le a,b < 2^{31}$$，$$a+b>0$$，$$2 \leq p \lt 2^{31}$$。

### 算法解析：

快速幂：把指数 $b$ 按二进制拆分，$a^b$ 由 $a^{2^i}$ 的乘积组成。从低位到高位检查 $b$ 的每一位，当前位为 1 就乘上 $a^{2^i}$，同时 $a$ 每次自乘平方（$a^{2^i}=(a^{2^{i-1}})^2$）。每次运算对 $p$ 取模。复杂度 $O(\log b)$。

### Python代码实现

```python
a, b, p = map(int, input().split())
ans = pow(a, b, p)
s = "{0}^{1} mod {2}={3}".format(a, b, p, ans)
print(s)
```

### C++代码实现

```c++
#include <iostream>
using namespace std;

typedef long long LL;
int a,b,p;

int qpow(int a,int b,int p){ //快速幂
  int s=1;
  while(b){
    if(b&1) s=(LL)s*a%p;
    a=(LL)a*a%p;
    b>>=1;
  }
  return s;
}
int main(){
  cin>>a>>b>>p;
  int s=qpow(a,b,p);
  printf("%d^%d mod %d=%d\n",a,b,p,s);
  return 0;
}
```
