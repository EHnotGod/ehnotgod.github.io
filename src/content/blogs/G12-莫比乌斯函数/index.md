---
title: "G12 莫比乌斯函数"
publishDate: 2026-08-08
description: "莫比乌斯函数：线性筛求 μ(n)。"
category: algo
tags:
  - 数学
language: zh
---
### 题目情境

**题目描述**

题目链接：https://www.luogu.com.cn/problem/T320132

**题目描述**

给定一个整数n，请依次输出μ(1)、μ(2)、...、μ(n)。

**输入格式**

读入一个n

**输出格式**

输出n行，第i行输出μ(i)的值

输入 #1

```
3
```

输出 #1

```
1
-1
-1
```

**说明/提示**

n<=1e7

### 算法解析：

线性筛求莫比乌斯函数：$\mu(1)=1$；质数 $\mu(p)=-1$；合数 $m=i\cdot p$：若 $p\mid i$ 则 $\mu(m)=0$（含平方因子），否则 $\mu(m)=-\mu(i)$。复杂度 $O(n)$，是莫比乌斯反演的基础。

### C++代码实现

```c++
#include <iostream>
using namespace std;

const int N = 1000010;
int p[N], vis[N], cnt;
int mu[N];

void get_mu(int n){//筛法求莫比乌斯函数
  mu[1] = 1;
  for(int i=2; i<=n; i++){
    if(!vis[i]){
      p[++cnt] = i;
      mu[i] = -1;
    }
    for(int j=1; i*p[j]<=n; j++){
      int m = i*p[j]; 
      vis[m] = 1;
      if(i%p[j] == 0){
        mu[m] = 0;
        break;
      } 
      else
        mu[m] = -mu[i];
    }
  }
}
int main(){
  int n;
  cin >> n;
  get_mu(n);
  for(int i=1; i<=n; i++)
    printf("%d\n",mu[i]);
  return 0;
}
```
