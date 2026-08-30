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

题目链接：https://www.luogu.com.cn/problem/U224067

**题目描述**

有 $n$ 件物品和一个容量是 $m$ 的背包。每件物品只能使用一次。

第 $i$ 件物品的体积是 $w_i$，价值是 $v_i$。

求解将哪些物品装入背包，可使这些物品的总体积不超过背包容量，且总价值最大。

如果有多种方案能使得选取的物品达到最大价值，输出任何一种即可。

**输入格式**

第一行两个整数，$n$，$m$，用空格隔开，分别表示物品数量和背包容积。

接下来有 $n$ 行，每行两个整数 $w_i,v_i$，用空格隔开，分别表示第 $i$ 件物品的体积和价值。

**输出格式**

输出两行，第一行包含一个整数，表示最优解中取走了多少件物品。

第二行包含若干个用空格隔开的整数，表示最优解中所选物品的编号序列。

输入 #1

```
4 5
1 2
2 4
3 4
4 6
```

输出 #1

```
2
1 4
```

- 对于 $100\%$ 的数据，有 $1 \le n,m \le 1000,0 \le v_i,w_i \le 1000$.

### 算法解析：

背包具体方案：用二维 $f[i][j]$ 记录从第 $i$ 个物品开始、容量 $j$ 的最优价值（逆序枚举物品，便于正向回溯），同时用 $p[i][j]$ 记录转移的列位置。回溯时若 $p[i][j]==j-v[i]$ 说明取了第 $i$ 个物品，输出并跳到 $(i+1, j-v[i])$；否则跳到 $(i+1, j)$。

### C++代码实现

```c++
#include<bits/stdc++.h>
using namespace std;

const int N=1005;
int n,m,v[N],w[N];
int f[N][N],path[N];

int main(){
  cin>>n>>m;
  for(int i=1;i<=n;i++)cin>>v[i]>>w[i];
  
  for(int i=n;i>=1;i--){
    for(int j=0;j<=m;j++){
      f[i][j]=f[i+1][j];
      if(j>=v[i])f[i][j]=max(f[i][j],f[i+1][j-v[i]]+w[i]);
    }
  }
  
  int j=m,cnt=0;
  for(int i=1;i<=n;i++){
    if(j>=v[i]&&f[i][j]==f[i+1][j-v[i]]+w[i]){
      path[++cnt]=i;
      j-=v[i];
    }
  }
  cout<<cnt<<endl;
  for(int i=1;i<=cnt;i++) cout<<path[i]<<" ";
}
```