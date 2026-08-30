---
title: "E14 背包具体方案"
publishDate: 2026-08-08
description: "背包具体方案：回溯输出选择的物品。"
category: algo
tags:
  - 动态规划
language: zh
---

### 题目情境

（题目链接待补充：01 背包输出具体方案）

### 算法解析：

背包具体方案：用二维 $f[i][j]$ 记录从第 $i$ 个物品开始、容量 $j$ 的最优价值（逆序枚举物品，便于正向回溯），同时用 $p[i][j]$ 记录转移的列位置。回溯时若 $p[i][j]==j-v[i]$ 说明取了第 $i$ 个物品，输出并跳到 $(i+1, j-v[i])$；否则跳到 $(i+1, j)$。

### C++代码实现

```c++
#include<iostream>
#include<cstring>
using namespace std;

const int N = 1010;
int v[N],w[N];
int f[N][N],p[N][N];

int main(){
  int n,m; cin>>n>>m;
  for(int i=1; i<=n; i++) cin>>v[i]>>w[i];
  
  for(int i=n; i>=1; i--)   //逆序取物 
  for(int j=0; j<=m; j++){  //枚举体积
    f[i][j]=f[i+1][j];
    p[i][j]=j;              //记录路径列 
    if(j>=v[i])
      f[i][j]=max(f[i][j],f[i+1][j-v[i]]+w[i]);
    if(j>=v[i] && f[i][j]==f[i+1][j-v[i]]+w[i])
      p[i][j]=j-v[i];
  }
  
  int j=m;
  for(int i=1; i<=n; i++)
    if(p[i][j]<j){
      printf("%d ",i);
      j=p[i][j];
    }
}
```
