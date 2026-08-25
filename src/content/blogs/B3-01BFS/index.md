---
title: "B3 01BFS"
publishDate: 2026-08-08
description: "01BFS：边权为 0/1 的最短路，用双端队列优化。"
category: algo
tags:
  - 搜索算法
language: zh
---

### 题目情境

题目链接：https://ac.nowcoder.com/acm/contest/115184/D

![image-20250930163432863](/images/算法竞赛/B/B3-1.png)

输入

```
1
3 3 2
RLD
UDU
UUL
```

输出

```
YES
```

### 算法解析：

把网格中的每个格子看成图上的一个点，从当前格子出发可以向上下左右移动：若移动方向与格子上的字符（R/L/U/D）一致，边权为 0；否则边权为 1。求从起点 $(0,0)$ 走到终点 $(n-1,m-1)$ 的最少改变方向次数，若不超过 $k$ 则可行。

边权只有 0 和 1，用 01BFS 优化：边权为 0 的边从队头插入，边权为 1 的边从队尾插入，队列始终按距离递增排列，每个点第一次出队时即得到最短路。相当于把 Dijkstra 的优先队列换成 deque，省掉一个 log。

### Python代码实现

```python
from collections import deque

t = int(input())
for _ in range(t):
    n, m, k = map(int, input().split())
    e = [[] for _ in range(n * m)]
    for i in range(n):
        s = input()
        for j in range(m):
            idx = i * m + j
            if i > 0:
                if s[j] == 'U':
                    e[idx].append((idx - m, 0))
                else:
                    e[idx].append((idx - m, 1))
            if j > 0:
                if s[j] == 'L':
                    e[idx].append((idx - 1, 0))
                else:
                    e[idx].append((idx - 1, 1))
            if i < n - 1:
                if s[j] == 'D':
                    e[idx].append((idx + m, 0))
                else:
                    e[idx].append((idx + m, 1))
            if j < m - 1:
                if s[j] == 'R':
                    e[idx].append((idx + 1, 0))
                else:
                    e[idx].append((idx + 1, 1))

    q = deque()
    vis = [-1] * (n * m)
    q.append((0, 0))
    while q:
        u, dis = q.popleft()
        if vis[u] != -1:
            continue
        vis[u] = dis
        for v, le in e[u]:
            if vis[v] == -1:
                if le == 0:
                    q.appendleft((v, dis))
                else:
                    q.append((v, dis + 1))

    if vis[n * m - 1] > k:
        print("NO")
    else:
        print("YES")
```

### C++代码实现

```c++
#include <bits/stdc++.h>
using namespace std;
#define endl "\n"
#define int long long
#define range(i, a, b) for (int i = (a); i < (b); ++i)
#define def(name, ...) auto name = [&](__VA_ARGS__)
vector<vector<pair<int, int>>> e;
// vector<int> a(n, 0);
// vector<vector<int>> dp(n + 1, vector<int>(n + 1, 0));
void solve() {
	int n, m, k; cin >> n >> m >> k;
    e.assign(n * m, vector<pair<int, int>>());
    range(i, 0, n){
        string s; cin >> s;
        range(j, 0, m){
            int idx = i * m + j;
            if (i > 0){
                if (s[j] == 'U')e[idx].push_back({idx - m, 0});
                else e[idx].push_back({idx - m, 1});
            }
            if (j > 0){
                if (s[j] == 'L')e[idx].push_back({idx - 1, 0});
                else e[idx].push_back({idx - 1, 1});
            }
            if (i < n - 1){
                if (s[j] == 'D')e[idx].push_back({idx + m, 0});
                else e[idx].push_back({idx + m, 1});
            }
            if (j < m - 1){
                if (s[j] == 'R')e[idx].push_back({idx + 1, 0});
                else e[idx].push_back({idx + 1, 1});
            }
        }
    }
    deque<pair<int, int>> q;
    vector<int> vis(n * m, -1);
    q.push_back({0, 0});
    while (q.size()){
        auto [u, dis] = q.front();
        q.pop_front();
        if (vis[u] != -1) continue;
        vis[u] = dis;
        for (auto[v, le]: e[u]){
            if (vis[v] == -1){
                if (le == 0){
                    q.push_front({v, dis});
                }
                else {
                    q.push_back({v, dis + 1});
                }
            }
        }
    }
    if (vis[n*m-1] > k){
        cout << "NO" << endl;
    }
    else {
        cout << "YES" << endl;
    }
}

signed main() {
    ios::sync_with_stdio(0);
    cin.tie(0);
    cout.tie(0);
	int t;
	cin >> t;
	while (t--) {
		solve();
	}
	return 0;
}
```
