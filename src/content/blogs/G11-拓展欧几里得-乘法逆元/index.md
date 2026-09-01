---
title: "G11 拓展欧几里得-乘法逆元"
publishDate: 2026-08-08
description: "扩展欧几里得求乘法逆元。"
category: algo
tags:
  - 数学
language: zh
---
### 题目情境

**题目描述**

给定 $a,b,m$，求解同余方程 $ax\equiv b\pmod m$。

**说明/提示**

本页为算法笔记。

### 算法解析：

exgcd 求逆元：$ax\equiv b\pmod m$ 即 $ax+my=b$。用扩展欧几里得求 $ax+my=\gcd(a,m)$ 的特解，若 $b$ 能被 $\gcd$ 整除则 $x=b/d\cdot x_0\bmod m$ 为解，否则无解。当 $b=1$ 时即求 $a$ 的乘法逆元。

![image-20250808150258351](/images/算法竞赛/G/G11-1.png)

时间复杂度：$${O(logn)}$$

### C++代码实现

```c++
#include <iostream>
#include <cstring>
#include <algorithm>
using namespace std;
    
int exgcd(int a,int b,int &x,int &y){
  if(b == 0){x = 1, y = 0; return a;}
  int x1, y1, d;
  d = exgcd(b, a%b, x1, y1);
  x = y1, y = x1-a/b*y1;
  return d;
}
int main(){
  int a, b, m, x, y;
  scanf("%d%d%d", &a, &b, &m);
  int d = exgcd(a, m, x, y);
  if(b%d == 0) 
    printf("%d", 1ll*x*b/d%m);
  else puts("none");
  return 0;
}
```
