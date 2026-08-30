---
title: "E17 区间DP-环形石子"
publishDate: 2026-08-08
description: "区间 DP：环形石子合并，破环成链。"
category: algo
tags:
  - 动态规划
language: zh
---

### 题目情境

题目链接：https://www.luogu.com.cn/problem/P1880

### 算法解析：

环形石子合并：把环复制成 2 倍长度（$a[i+n]=a[i]$）破环成链。$f[i][j]$ / $g[i][j]$ 表示把 $i..j$ 合并成一堆的最小 / 最大得分，枚举分割点 $k$：$f[i][j]=\min(f[i][k]+f[k+1][j]+s[j]-s[i-1])$。答案取长度为 $n$ 的所有区间的最值。复杂度 $O(n^3)$。

### C++代码实现

```c++
#include <iostream>
#include <cstring>
#include <algorithm>
using namespace std;

const int N=210;
int n, a[N], s[N];
int f[N][N];  //f[i][j]表示把从i到j合并成一堆的得分最小值 
int g[N][N];  //g[i][j]表示把从i到j合并成一堆的得分最大值 

int main(){
  memset(f,0x3f,sizeof f); memset(g,-0x3f,sizeof g);
  scanf("%d",&n);
  for(int i=1; i<=n; i++)scanf("%d",&a[i]), a[i+n]=a[i];
  for(int i=1; i<=2*n; i++)s[i]=s[i-1]+a[i], g[i][i]=0, f[i][i]=0;
  
  int minv=1e9, maxv=-1e9;
  for(int len=2; len<=n; len++){            //区间长度 
    for(int i=1,j; (j=i+len-1)<=2*n; i++){  //区间起点
      for(int k=i; k<j; k++){               //区间分割点 
        f[i][j]=min(f[i][j],f[i][k]+f[k+1][j]+s[j]-s[i-1]);
        g[i][j]=max(g[i][j],g[i][k]+g[k+1][j]+s[j]-s[i-1]); 
      }
      minv=min(minv,f[i][i+n-1]); //f[1,n]...f[n,2n-1] 
      maxv=max(maxv,g[i][i+n-1]); //g[1,n]...g[n,2n-1]      
    }
  }
  printf("%d\n%d\n",minv,maxv);
}
```
