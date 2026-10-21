---
title: "D17 Dinic最大流"
publishDate: 2026-08-08
description: "Dinic 最大流：分层图 + 阻塞流。"
category: algo
tags:
  - 图论
language: zh
---

### 题目情境

题目链接：https://www.luogu.com.cn/problem/P3376

**题目描述**

如题，给出一个网络图，以及其源点和汇点，求出其网络最大流。

**输入格式**

第一行包含四个正整数 $$n,m,s,t$$，分别表示点的个数、有向边的个数、源点序号、汇点序号。

接下来 $$m$$ 行每行包含三个正整数 $$u_i,v_i,w_i$$，表示第 $$i$$ 条有向边从 $$u_i$$ 出发，到达 $$v_i$$，边权为 $$w_i$$（即该边最大流量为 $$w_i$$）。

**输出格式**

一行，包含一个正整数，即为该网络的最大流。

输入 #1

```
4 5 4 3
4 2 30
4 3 20
2 3 20
2 1 30
1 3 30
```

输出 #1

```
50
```

- 对于 $$100\%$$ 的数据，保证 $$1 \leq n\leq200$$，$$1 \leq m\leq 5000$$，$$0 \leq w\lt 2^{31}$$。

理论复杂度：$$O(n^2m)$$，实际挺快的

二分图上的Dinic更快。

### 算法解析：

Dinic 最大流：每次用 BFS 建分层图（按到源点距离分层），再在当前分层图上用 DFS 找阻塞流（一次可增广多条路径，配合当前弧优化），反复执行直到 BFS 无法到达汇点。复杂度 $O(n^2m)$，实际表现很快。

用 `vector<vector<int>> g` 保存每个点的出边编号，边的信息统一放在 `vector<Edge> e` 中。每次添加一条原边时，连续加入正向边和容量为零的反向边，编号从 0 开始，因此编号为 `i` 的边对应的反向边始终为 `i ^ 1`。`cur[u]` 记录的是 `g[u]` 中的下标，每轮 BFS 后归零。

### py代码实现

本节给出 C++ 实现。

### C++代码实现

```c++
// Luogu P3376 【模板】网络最大流
#include <iostream>
#include <algorithm>
#include <limits>
#include <queue>
#include <vector>
using namespace std;

using LL = long long;
const LL INF = numeric_limits<LL>::max() / 4;
int n, m, S, T;
struct Edge { int to; LL cap; };
vector<Edge> e;
vector<vector<int>> g;
vector<int> d,cur;

void add(int a, int b, LL cap) {
  int id = static_cast<int>(e.size());
  e.push_back({b, cap});
  e.push_back({a, 0});
  g[a].push_back(id);
  g[b].push_back(id ^ 1);
}
bool bfs() {
  fill(d.begin(), d.end(), -1);
  queue<int> q;
  q.push(S);
  d[S] = 0;
  while (!q.empty()) {
    int u = q.front(); q.pop();
    for (int id : g[u]) {
      int v = e[id].to;
      if (d[v] == -1 && e[id].cap > 0) {
        d[v] = d[u] + 1;
        q.push(v);
      }
    }
  }
  return d[T] != -1;
}
LL dfs(int u, LL limit) {
  if (u == T) return limit;
  for (int &p = cur[u]; p < static_cast<int>(g[u].size()); ++p) {
    int id = g[u][p], v = e[id].to;
    if (d[v] == d[u] + 1 && e[id].cap > 0) {
      LL f = dfs(v, min(limit, e[id].cap));
      if (f == 0) continue;
      e[id].cap -= f;
      e[id ^ 1].cap += f;
      return f; //保留当前下标，下次可继续使用这条边的剩余容量
    }
  }
  return 0;
}
LL dinic() {
  LL flow = 0;
  while (bfs()) {
    fill(cur.begin(), cur.end(), 0);
    while (LL f = dfs(S, INF)) flow += f;
  }
  return flow;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  cin >> n >> m >> S >> T;
  g.assign(n + 1, {});
  d.assign(n + 1, 0); cur.assign(n + 1, 0);
  for (int i = 0; i < m; ++i) {
    int a, b;
    LL cap;
    cin >> a >> b >> cap;
    add(a, b, cap);
  }
  cout << dinic() << '\n';
  return 0;
}
```
