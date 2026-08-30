---
title: "E16 分组背包"
publishDate: 2026-08-08
description: "分组背包：每组最多选一个。"
category: algo
tags:
  - 动态规划
language: zh
---

### 题目情境

题目链接：https://www.luogu.com.cn/problem/P1757

### 算法解析：

分组背包：每组内最多选一个物品。状态 $f[i][j]$ 表示前 $i$ 组、容量 $j$ 的最大价值。对每组枚举选组内哪个物品（或不选）：$f[i][j]=\max(f[i-1][j],\ \max_k f[i-1][j-v[k]]+w[k])$。可压缩为一维，容量逆序。复杂度 $O(n\cdot V\cdot s)$。

### C++代码实现

```c++
// 分组背包 朴素算法
#include<iostream>
#include<cstring>
using namespace std;

const int N=110;
int v[N][N],w[N][N],s[N];
// v[i,j]:第i组第j个物品的体积 s[i]:第i组物品的个数
int f[N][N];
// f[i,j]:前i组物品，能放入容量为j的背包的最大值

int main(){    
  int n,V; cin>>n>>V;
  for(int i=1;i<=n;i++){
    cin>>s[i];
    for(int j=1;j<=s[i];j++) cin>>v[i][j]>>w[i][j];
  }
  
  for(int i=1;i<=n;i++)     //物品组
  for(int j=1;j<=V;j++)     //体积
  for(int k=0;k<=s[i];k++)  //同组内的物品只能选一个
    if(j>=v[i][k]) f[i][j]=max(f[i][j],f[i-1][j-v[i][k]]+w[i][k]);                 

  cout<<f[n][V];
}
```
