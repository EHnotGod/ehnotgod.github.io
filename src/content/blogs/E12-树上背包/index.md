---
title: "E12 树上背包"
publishDate: 2026-08-08
description: "树上背包：在树上做依赖背包（树形 DP）。"
category: algo
tags:
  - 动态规划
language: zh
---

### 题目情境

题目链接：https://www.luogu.com.cn/problem/P2014

### 算法解析：

树上背包：在树上做依赖背包（如选课，选子课程必须先选父课程）。$f[u][j]$ 表示 $u$ 子树内选 $j$ 门课（含 $u$）的最大价值。DFS 处理完儿子后，用子树大小约束做背包合并：$f[u][j]=\max(f[u][j], f[u][j-k]+f[v][k])$。复杂度 $O(n^2)$。

### C++代码实现

```c++
// 树上背包 O(n^2)
#include <iostream>
#include <cstring>
#include <algorithm>
#include <vector>
using namespace std;

const int N=305;
vector<int> e[N];
int n,m,w[N],f[N][N],siz[N];

void dfs(int u){
  f[u][1]=w[u];siz[u]=1;
  for(int v:e[u]){
    dfs(v);
    siz[u]+=siz[v];
    for(int j=min(m+1,siz[u]);j;j--) //课程
      for(int k=0;k<=min(j-1,siz[v]);k++) //决策      
        f[u][j]=max(f[u][j],f[u][j-k]+f[v][k]);
  }
}
int main(){
  scanf("%d%d",&n,&m);
  for(int i=1,k; i<=n; i++){
    scanf("%d%d",&k,&w[i]);
    e[k].push_back(i);
  }
  dfs(0); //虚拟根节点0
  printf("%d",f[0][m+1]);
}
```
