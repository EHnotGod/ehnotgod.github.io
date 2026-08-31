---
title: "G62 线性基-k"
publishDate: 2026-08-08
description: "线性基：求第 k 小异或值。"
category: algo
tags:
  - 数学
language: zh
---
### 题目情境

**题目描述**

给定若干数，$m$ 次询问第 $k$ 小的异或值。

**说明/提示**

本页为算法笔记。

### 算法解析：

线性基求第 $k$ 小：构造线性基后（高斯消元形式），把 $k$ 的二进制位对应选取基向量异或。若原集合能异或出 0 则 $k$ 先减 1；$k\ge2^{s}$（$s$ 为基大小）则无解输出 -1。本题为 HDU 3949 XOR，非洛谷题。

### 备注

![image-20250826122239735](/images/算法竞赛/G/G62-1.png)

### C++代码实现

```c++
// 线性基 O(63*n)
#include <iostream>
#include <cstring>
#include <algorithm>
using namespace std;

typedef long long LL;
const int N=10005;
int T,n,m,s;
LL p[N];

void gauss(){
  s=0;
  for(int i=63;i>=0;i--){
    // 把当前第i位是1的数换上去
    for(int j=s;j<n;j++)
      if(p[j]>>i&1){swap(p[j],p[s]);break;}
    // 当前第i位所有向量都是0
    if((p[s]>>i&1)==0) continue;
    // 把其他数的第i位全部消为0
    for(int j=0;j<n;j++)
      if(j!=s&&(p[j]>>i&1)) p[j]^=p[s];
    // 有多组测试数据，不break，会被上一组数据影响
    s++; if(s==n) break;
  }
}
int main(){
  scanf("%d",&T);
  for(int C=1;C<=T;C++){
    printf("Case #%d:\n",C);
    scanf("%d",&n);
    for(int i=0;i<n;i++)scanf("%lld",&p[i]);
    gauss(); //高斯消元法构造线性基
    scanf("%d",&m);
    while(m--){
      LL k; scanf("%lld",&k); //第k小
      if(s<n) k--;      //如果能凑出0
      if(k>=(1ll<<s)) puts("-1");
      else{
        LL ans=0;
        for(int i=0;i<s;i++)
          if(k>>i&1) ans^=p[s-i-1];
        printf("%lld\n",ans);
      }
    }
  }
}
```
