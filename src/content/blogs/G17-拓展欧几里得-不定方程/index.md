---
title: "G17 拓展欧几里得-不定方程"
publishDate: 2026-08-08
description: "扩展欧几里得：求解 ax+by=gcd(a,b)。"
category: algo
tags:
  - 数学
language: zh
---
### 题目情境

**题目描述**

给定 $a,b,c$，求解不定方程 $ax+by=c$ 的一组整数解。

**说明/提示**

本页为算法笔记。

### 算法解析：

扩展欧几里得：递归求 $ax+by=\gcd(a,b)$ 的一组特解 $(x_0,y_0)$（$b=0$ 时 $x=1,y=0$）。若 $c$ 能被 $\gcd(a,b)$ 整除，则 $x=c/d\cdot x_0,\ y=c/d\cdot y_0$ 为解，否则无解。复杂度 $O(\log)$。

### 备注

![image-20250808145533135](/images/算法竞赛/G/G17-1.png)

时间复杂度：$${O(logn)}$$

### C++代码实现

```c++
#include <iostream>
#include <cstring>
#include <algorithm>
using namespace std;
    
int exgcd(int a,int b,int &x,int &y){
  if(b == 0) {x=1, y=0; return a;}
  int x1, y1, d;
  d = exgcd(b, a%b, x1, y1);
  x = y1, y = x1-a/b*y1;
  return d;
}
int main(){
  int a, b, c, x, y;
  cin >> a >> b >> c;
  int d = exgcd(a,b,x,y);
  if(c%d == 0) 
    printf("%d %d",c/d*x,c/d*y);
  else puts("none");
  return 0;
}
```
