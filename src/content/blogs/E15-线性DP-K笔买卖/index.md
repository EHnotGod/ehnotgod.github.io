---
title: "E15 线性DP K笔买卖"
publishDate: 2026-08-08
description: "线性 DP：最多 k 笔股票买卖的最大收益。"
category: algo
tags:
  - 动态规划
language: zh
---

### 题目情境

https://www.luogu.com.cn/problem/U281153

**题目描述**

给你一支股票，给出这个股票的N天的价格，Ai表示这个股票在第i天的价格
	每一天都可以去买卖这支股票，但是你只能买卖K次（在买股票前需要先全部卖出然后重新买进，被视为一次）

**输入格式**

第一行包含整数 N 和 K，表示数组的长度以及你可以完成的最大交易笔数。

	第二行包含 N 个不超过 10000 的正整数，表示完整的数组。
    
	1≤N≤1e5，1≤k≤100

**输出格式**

输出一个整数，表示最大利润。

输入 #1

```
3 2
2 4 1
```

输出 #1

```
2
```

输入 #2

```
6 2
3 2 6 5 0 3
```

输出 #2

```
7
```

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
