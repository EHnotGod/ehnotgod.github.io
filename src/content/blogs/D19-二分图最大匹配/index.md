---
title: "D19 二分图最大匹配"
publishDate: 2026-08-08
description: "二分图最大匹配：匈牙利算法。"
category: algo
tags:
  - 图论
language: zh
---

### 题目情境

题目链接：https://www.luogu.com.cn/problem/P3386

**题目描述**

给定一个二分图，其左部点的个数为 $$n$$，右部点的个数为 $$m$$，边数为 $$e$$，求其最大匹配的边数。

左部点从 $$1$$ 至 $$n$$ 编号，右部点从 $$1$$ 至 $$m$$ 编号。

**输入格式**

输入的第一行是三个整数，分别代表 $$n$$，$$m$$ 和 $$e$$。

接下来 $$e$$ 行，每行两个整数 $$u, v$$，表示存在一条连接左部点 $$u$$ 和右部点 $$v$$ 的边。

**输出格式**

输出一行一个整数，代表二分图最大匹配的边数。

输入 #1

```
1 1 1
1 1
```

输出 #1

```
1
```

### 算法解析：

匈牙利算法求二分图最大匹配：对每个左部点尝试匹配一个右部点，若该右部点已被匹配，则递归尝试让它的原配重新寻找新的右部点（即寻找增广路），成功则匹配数 +1。复杂度 $O(ne)$。

匈牙利算法直接用 `vector<vector<int>> g` 保存每个左部点相邻的右部点，不需要额外的边结构。

也可以建立流网络：源点连向所有左部点，原图的边从左部连向右部，所有右部点连向汇点，每条边容量为 1。最大流即最大匹配，Dinic 在这个网络上的复杂度为 $O((n+m+e)\sqrt{n+m})$。邻接表保存边编号，正反向边连续存入 `vector<Edge>`，通过 `id ^ 1` 配对；当前弧保存邻接表下标，每轮分层后归零。

### C++代码实现

匈牙利算法：

```c++
// Luogu P3386 【模板】二分图最大匹配
#include <iostream>
#include <algorithm>
#include <vector>
using namespace std;

int n, m, k;
vector<vector<int>> g;
vector<int> match; //match[v] 为右部点 v 匹配的左部点
vector<bool> vis;

bool augment(int u) {
  for (int v : g[u]) {
    if (vis[v]) continue;
    vis[v] = true;
    if (match[v] == 0 || augment(match[v])) {
      match[v] = u;
      return true;
    }
  }
  return false;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  cin >> n >> m >> k;
  g.assign(n + 1, {});
  match.assign(m + 1, 0); vis.assign(m + 1, false);

  for (int i = 0; i < k; ++i) {
    int u, v;
    cin >> u >> v;
    g[u].push_back(v);
  }
  int answer = 0;
  for (int u = 1; u <= n; ++u) {
    fill(vis.begin(), vis.end(), false);
    if (augment(u)) ++answer;
  }
  cout << answer << '\n';
  return 0;
}
```

Dinic 算法：

```c++
// Luogu P3386 【模板】二分图最大匹配
#include <iostream>
#include <algorithm>
#include <queue>
#include <vector>
using namespace std;

const int INF = 1000000000;
int n, m, k, S, T;
struct Edge { int to, cap; };
vector<Edge> e;
vector<vector<int>> g;
vector<int> d,cur;

void add(int a, int b, int cap) {
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
int dfs(int u, int limit) {
  if (u == T) return limit;
  for (int &p = cur[u]; p < static_cast<int>(g[u].size()); ++p) {
    int id = g[u][p], v = e[id].to;
    if (d[v] == d[u] + 1 && e[id].cap > 0) {
      int f = dfs(v, min(limit, e[id].cap));
      if (f == 0) continue;
      e[id].cap -= f;
      e[id ^ 1].cap += f;
      return f;
    }
  }
  return 0;
}
int dinic() {
  int flow = 0;
  while (bfs()) {
    fill(cur.begin(), cur.end(), 0);
    while (int f = dfs(S, INF)) flow += f;
  }
  return flow;
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  cin >> n >> m >> k;

  S = 0;
  T = n + m + 1;
  g.assign(T + 1, {});
  d.assign(T + 1, 0); cur.assign(T + 1, 0);
  for (int i = 0; i < k; ++i) {
    int u, v;
    cin >> u >> v;
    add(u, v + n, 1);
  }
  for (int u = 1; u <= n; ++u) add(S, u, 1);
  for (int v = 1; v <= m; ++v) add(v + n, T, 1);
  cout << dinic() << '\n';
  return 0;
}
```
