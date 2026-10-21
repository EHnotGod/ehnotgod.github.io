---
title: "E10 分组背包"
publishDate: 2026-08-08
description: "分组背包：每组最多选一个。"
category: algo
tags:
  - 动态规划
language: zh
---

### 题目情境

题目链接：https://www.luogu.com.cn/problem/P1757

**题目描述**

自 $01$ 背包问世之后，小 A 对此深感兴趣。一天，小 A 去远游，却发现他的背包不同于 $01$ 背包，他的物品大致可分为 $k$ 组，每组中的物品相互冲突，现在，他想知道最大的利用价值是多少。

**输入格式**

两个数 $m,n$，表示一共有 $n$ 件物品，背包能承受的最大重量为 $m$。

接下来 $n$ 行，每行 $3$ 个数 $a_i,b_i,c_i$，表示物品的重量，利用价值，所属组数。

**输出格式**

一个数，最大的利用价值。

输入 #1

```
45 3
10 10 1
10 5 1
50 400 2
```

输出 #1

```
10
```

$0 \leq m \leq 1000$，$1 \leq n \leq 1000$，$1\leq k\leq 100$，$a_i, b_i, c_i$ 在 `int` 范围内。

### 算法解析：

分组背包：每组内最多选一个物品。先按照输入中的组号归类，状态 $f[i][j]$ 表示前 $i$ 组、容量 $j$ 的最大价值。枚举不选这一组，或者选其中一件：$f[i][j]=\max(f[i-1][j],\ \max_{(v,w)\in group_i} f[i-1][j-v]+w)$。每次转移都读取上一组的状态，避免同组物品重复选取。设物品总数为 $n$、组数为 $k$，时间复杂度 $O(nV)$，空间复杂度 $O(kV)$。

### C++代码实现

```c++
// 分组背包，每组最多选一个
#include <bits/stdc++.h>
using namespace std;

int main() {
  int V,n;
  cin >> V >> n;
  map<int, vector<pair<int,int>>> groups;
  for (int i=0; i<n; ++i) {
    int v,w,id;
    cin >> v >> w >> id;
    groups[id].push_back({v,w});
  }
  vector<vector<long long>> f;
  f.assign(groups.size()+1, vector<long long>(V+1,0));
  int i=0;
  for (const auto &[id, items] : groups) {
    ++i;
    f[i]=f[i-1]; //这一组不选物品
    for (int j=0; j<=V; ++j)
      for (auto [v,w] : items)
        if (j>=v) f[i][j]=max(f[i][j],f[i-1][j-v]+w);
  }
  cout << f[i][V] << '\n';
}
```
