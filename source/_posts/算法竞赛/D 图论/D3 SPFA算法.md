---
title: "D3 SPFA算法"
categories:
- [算法, D 图论]
tags:
- 图论
---

### 题目情境

**题目描述**

给定一个 $n$ 个点的有向图，请求出图中是否存在**从顶点 $1$ 出发能到达**的负环。

负环的定义是：一条边权之和为负数的回路。

**输入格式**

输入的第一行是一个整数 $T$，表示测试数据的组数。对于每组数据的格式如下：

第一行有两个整数，分别表示图的点数 $n$ 和接下来给出边信息的条数 $m$。

接下来 $m$ 行，每行三个整数 $u, v, w$。

- 若 $w \geq 0$，则表示存在一条从 $u$ 至 $v$ 边权为 $w$ 的边，还存在一条从 $v$ 至 $u$ 边权为 $w$ 的边。
- 若 $w < 0$，则只表示存在一条从 $u$ 至 $v$ 边权为 $w$ 的边。

**输出格式**

对于每组数据，输出一行一个字符串，若所求负环存在，则输出 `YES`，否则输出 `NO`。

输入 #1

```
2
3 4
1 2 2
1 3 4
2 3 1
3 1 -3
3 3
1 2 3
2 3 4
3 1 -8
```

输出 #1

```
NO
YES
```

对于全部的测试点，保证：

- $1 \leq n \leq 2 \times 10^3$，$1 \leq m \leq 3 \times 10^3$。
- $1 \leq u, v \leq n$，$-10^4 \leq w \leq 10^4$。
- $1 \leq T \leq 10$。

### C++代码实现

```c++
#include <bits/stdc++.h>
using namespace std;
const int N = 2010;
int n, m;
int d[N], vis[N], cnt[N];
struct Edge {
    int v, w;
};
vector<Edge> g[N];
bool spfa() { // 判负环
    memset(d, 0x3f, sizeof d); d[1] = 0;
    memset(vis, 0, sizeof vis);
    memset(cnt, 0, sizeof cnt);
    queue<int> q; 
    q.push(1); 
    vis[1] = 1; // 在队中
    while (!q.empty()) {
        int u = q.front(); q.pop(); 
        vis[u] = 0;
        for (auto &e : g[u]) {
            int v = e.v, w = e.w;
            if (d[v] > d[u] + w) { // 松弛
                d[v] = d[u] + w;
                cnt[v] = cnt[u] + 1; // 边数
                if (cnt[v] >= n) return true; // 有负环
                if (!vis[v]) {
                    q.push(v);
                    vis[v] = 1;
                }
            }
        }
    }
    return false;
}

int main() {
    int T; 
    scanf("%d", &T);
    while (T--) {
        scanf("%d%d", &n, &m);
        for (int i = 1; i <= n; i++) g[i].clear();
        for (int i = 1; i <= m; i++) {
            int u, v, w;
            scanf("%d%d%d", &u, &v, &w);
            g[u].push_back({v, w});
            if (w >= 0) g[v].push_back({u, w});
        }
        puts(spfa() ? "YES" : "NO");
    }
}
```
