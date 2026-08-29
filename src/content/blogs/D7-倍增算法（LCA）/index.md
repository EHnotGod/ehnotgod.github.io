---
title: "D7 倍增算法（LCA）"
publishDate: 2026-08-08
description: "倍增法求 LCA：树上最近公共祖先。"
category: algo
tags:
  - 图论
language: zh
---

### 题目情境

题目链接：https://www.luogu.com.cn/problem/P3379

**题目描述**

如题，给定一棵有根多叉树，请求出指定两个点之间最近的公共祖先。

**输入格式**

第一行包含三个正整数 $N,M,S$，分别表示树的结点个数、询问的个数和树根结点的序号。

接下来 $N-1$ 行每行包含两个正整数 $x, y$，表示 $x$ 结点和 $y$ 结点之间有一条直接连接的边（数据保证可以构成树）。

接下来 $M$ 行每行包含两个正整数 $a, b$，表示询问 $a$ 结点和 $b$ 结点的最近公共祖先。

**输出格式**

输出包含 $M$ 行，每行包含一个正整数，依次为每一个询问的结果。

输入 #1

```
5 5 4
3 1
2 4
5 1
1 4
2 4
3 2
3 5
1 2
4 5
```

输出 #1

```
4
4
1
4
4

```

对于 $100\%$ 的数据，$1 \leq N,M\leq 5\times10^5$，$1 \leq x, y,a ,b \leq N$，**不保证** $a \neq b$。

### 算法解析：

![image-20250727163659755](/images/算法竞赛/D/D7-1.png)

![image-20250727163753894](/images/算法竞赛/D/D7-2.png)

倍增法求 LCA：先用 DFS 预处理每个点的深度 $dep[u]$ 和 $2^i$ 级祖先 $f[u][i]$（$f[u][i]=f[f[u][i-1]][i-1]$）。查询时先把较深的点跳到与另一个同深度，再一起向上跳，最后跳到 LCA 的下一个点。单次查询 $O(\log n)$，预处理 $O(n\log n)$。

### Python代码实现

```python
import sys

sys.setrecursionlimit(10 ** 7)
input = sys.stdin.readline

# 最大节点数和最大二进制位数（因为 2^20 > 10^6，足够应对 N ≤ 5e5）
N = 500_005
LOG = 20

# 邻接表存储树的边
edges = [[] for _ in range(N)]

# f[u][i] 表示节点 u 的第 2^i 级祖先
# dep[u] 存储节点 u 的深度（根节点深度为 1）
f = [[0] * (LOG + 1) for _ in range(N)]
dep = [0] * N


def dfs(u: int, parent: int) -> None:
    f[u][0] = parent
    dep[u] = dep[parent] + 1
    for i in range(1, LOG + 1):
        f[u][i] = f[f[u][i - 1]][i - 1]
    for v in edges[u]:
        if v == parent:
            continue
        dfs(v, u)


def lca(u: int, v: int) -> int:
    if dep[u] < dep[v]:
        u, v = v, u
    diff = dep[u] - dep[v]
    for i in range(LOG + 1):
        if diff & (1 << i):
            u = f[u][i]
    if u == v:
        return u
    for i in reversed(range(LOG + 1)):
        if f[u][i] != f[v][i]:
            u = f[u][i]
            v = f[v][i]
    return f[u][0]
n, m, s = map(int, input().split())
for _ in range(n - 1):
    a, b = map(int, input().split())
    edges[a].append(b)
    edges[b].append(a)
dfs(s, 0)
for _ in range(m):
    u, v = map(int, input().split())
    print(lca(u, v))
```

### C++代码实现

```c++
// 倍增法 O(nlogn)
#include<bits/stdc++.h>
using namespace std;

const int N=500005;
int n,m,s;
vector<int> e[N];
int f[N][22],dep[N];

void dfs(int u,int fa){
  f[u][0]=fa; dep[u]=dep[fa]+1;
  for(int i=1;i<=20;i++) //u的2,4,8...祖先
    f[u][i]=f[f[u][i-1]][i-1];
  for(int v:e[u])
    if(v!=fa) dfs(v,u);
}
int lca(int u,int v){
  if(dep[u]<dep[v]) swap(u,v);
  for(int i=20;~i;i--) //u先大步后小步向上跳，直到与v同层
    if(dep[f[u][i]]>=dep[v]) u=f[u][i];
  if(u==v) return v;
  for(int i=20;~i;i--) //u,v一起向上跳，直到lca的下面
    if(f[u][i]!=f[v][i]) u=f[u][i],v=f[v][i];
  return f[u][0];
}
int main(){
  scanf("%d%d%d",&n,&m,&s);
  for(int i=1,a,b; i<n; i++){
    scanf("%d%d",&a,&b);
    e[a].push_back(b);
    e[b].push_back(a);
  }
  dfs(s,0);
  for(int i=0,a,b;i<m;i++){
    scanf("%d%d",&a,&b);
    printf("%d\n",lca(a,b));
  }
}
```
