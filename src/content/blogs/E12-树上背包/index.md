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

**题目描述**

在大学里每个学生，为了达到一定的学分，必须从很多课程里选择一些课程来学习，在课程里有些课程必须在某些课程之前学习，如高等数学总是在其它课程之前学习。现在有 $N$ 门功课，每门课有若干学分，分别记作 $s_1,s_2,\cdots,s_N$，每门课有一门或没有直接先修课（若课程 $a$ 是课程 $b$ 的先修课即只有学完了课程 $a$，才能学习课程 $b$）。一个学生要从这些课程里选择 $M$ 门课程学习，问他能获得的最大学分是多少？

题目保证课程安排无冲突。（即不会有 $a$ 是 $b$ 的先修课，$b$ 也是 $a$ 的先修课这类情况存在。）

**输入格式**

第一行有两个整数 $N$，$M$ 用空格隔开 $(1 \leq N \leq 300$ , $1 \leq M \leq 300)$。

接下来的 $N$ 行，第 $i+1$ 行包含两个整数 $k_i$ 和 $s_i$，$k_i$ 表示第 $i$ 门课的直接先修课，$s_i$ 表示第 $i$ 门课的学分。若 $k_i=0$ 表示没有直接先修课 $(0 \leq {k_i} \leq N$,$1 \leq {s_i} \leq 20)$。

数据保证至少存在一个 $k_i=0$，即至少一门课无先修课。

**输出格式**

只有一行，选 $M$ 门课程的最大学分。

输入 #1

```
7 4
2 2
0 1
0 4
2 1
7 1
7 6
2 2
```

输出 #1

```
13
```

### 算法解析：

树上背包：在树上做依赖背包（如选课，选子课程必须先选父课程）。$f[u][j]$ 表示 $u$ 子树内选 $j$ 门课（含 $u$）的最大价值。DFS 处理完儿子后，用子树大小约束做背包合并：$f[u][j]=\max(f[u][j], f[u][j-k]+f[v][k])$。复杂度 $O(n^2)$。

### py代码实现

略

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
