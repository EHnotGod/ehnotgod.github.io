---
title: "E15 二维背包"
publishDate: 2026-08-08
description: "二维费用背包：体积与重量两个限制。"
category: algo
tags:
  - 动态规划
language: zh
---

### 题目情境

题目链接：https://www.luogu.com.cn/problem/P1507

### 算法解析：

二维费用背包：每个物品有两个代价（体积 $v$ 和重量 $w$）。状态 $f[j][k]$ 表示体积 $\le j$ 且重量 $\le k$ 的最大价值。转移 $f[j][k]=\max(f[j][k], f[j-v][k-w]+val)$，两个维度都逆序（01 背包）。复杂度 $O(n\cdot V\cdot W)$。

### C++代码实现

```c++
//二维费用 01背包
#include <iostream>
using namespace std;

int f[110][110];
// f[j,k]:前i个物品，体积≤j，重量≤k 的最大价值

int main(){
  int n, V, W;    //物品 容量 承重
  int v, w, val;  //体积 重量 价值
  cin>>n>>V>>W;
  for(int i=1; i<=n; i++){  //物品 
    cin>>v>>w>>val;
    for(int j=V; j>=v; j--) //体积
    for(int k=W; k>=w; k--) //重量
      f[j][k]=max(f[j][k],f[j-v][k-w]+val);
  }
  cout<<f[V][W];
}
```
