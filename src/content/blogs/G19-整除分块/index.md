---
title: "G19 整除分块"
publishDate: 2026-08-08
description: "整除分块：对 ⌊n/i⌋ 相同的区间合并计算。"
category: algo
tags:
  - 数学
language: zh
---
### 题目情境

题目链接：https://www.luogu.com.cn/problem/P2261

**题目描述**

给出正整数 $n$ 和 $k$，请计算

$$G(n, k) = \sum_{i = 1}^n k \bmod i$$

其中 $k\bmod i$ 表示 $k$ 除以 $i$ 的余数。

**输入格式**

输入只有一行两个整数，分别表示 $n$ 和 $k$。

**输出格式**

输出一行一个整数表示答案。

输入 #1

```
10 5

```

输出 #1

```
29
```

对于 $100\%$ 的数据，保证 $1 \leq n, k \leq 10^9$。


### 算法解析：

整除分块：$\lfloor n/i\rfloor$ 的取值只有 $O(\sqrt n)$ 段，段 $[l,r]$ 内值相同，其中 $r=\lfloor n/\lfloor n/l\rfloor\rfloor$。对形如 $\sum_{i=1}^n f(i)\cdot\lfloor n/i\rfloor$ 的求和，可按段累加 $f$ 的区间和。复杂度 $O(\sqrt n)$。

![image-20250808224555369](/images/算法竞赛/G/G19-1.png)

![image-20250808224637154](/images/算法竞赛/G/G19-2.png)

### c++代码

```c++
#include<cstdio>
#include<algorithm>
using namespace std;

typedef long long LL;

int main(){
  LL n, k, l, r, res;
  scanf("%lld%lld", &n, &k);
  res = n*k;
  for(l=1; l<=n; l=r+1){
    if(k/l == 0) break;
    r = min(k/(k/l),n); 
    res -= (k/l)*(r-l+1)*(l+r)/2;
  }
  printf("%lld", res);
  return 0;
}
```