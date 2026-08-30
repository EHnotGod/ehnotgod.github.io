---
title: "E23 线性DP K笔买卖"
publishDate: 2026-08-08
description: "线性 DP：最多 k 笔股票买卖的最大收益。"
category: algo
tags:
  - 动态规划
language: zh
---

### 题目情境

（题目链接待补充：最多 k 笔股票买卖）

### 算法解析：

最多 $k$ 笔股票交易：$f[i][j][0/1]$ 表示前 $i$ 天、已完成 $j$ 笔交易、当前不持有/持有股票的最大收益。不持有：$f[i][j][0]=\max(f[i-1][j][0], f[i-1][j][1]+w[i])$（卖出）；持有：$f[i][j][1]=\max(f[i-1][j][1], f[i-1][j-1][0]-w[i])$（买入，开新一笔交易）。答案 $f[n][k][0]$。复杂度 $O(nk)$。

### C++代码实现

```c++
#include<iostream>
#include<cstring>
using namespace std;

const int N=100010, M=110;
int w[N], f[N][M][2];

int main(){
  int n, k; cin >> n >> k;
  for(int i=1; i<=n; i++) cin >> w[i];
  
  for(int j=0; j<=k; j++) f[0][j][1]=-1e6;

  for(int i=1; i<=n; i++)
  for(int j=1; j<=k; j++){
    f[i][j][0]=max(f[i-1][j][0], f[i-1][j][1]+w[i]);
    f[i][j][1]=max(f[i-1][j][1], f[i-1][j-1][0]-w[i]);
  }
  
  cout << f[n][k][0];
}
```
