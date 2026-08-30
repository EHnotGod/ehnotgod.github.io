---
title: "E16 TSP-状压DP"
publishDate: 2026-08-08
description: "状压 DP：旅行商问题（TSP）。"
category: algo
tags:
  - 动态规划
language: zh
---

### 题目情境

题目链接：https://www.luogu.com.cn/problem/P1171

**题目描述**

某乡有 $n$ 个村庄，有一个售货员，他要到各个村庄去售货，各村庄之间的路程 $s_{i,j}$ 是已知的，且 $A$ 村到 $B$ 村与 $B$ 村到 $A$ 村的路大多不同。为了提高效率，他从商店出发到每个村庄一次，然后返回商店所在的村，假设商店所在的村庄为 $1$，他不知道选择什么样的路线才能使所走的路程最短。请你帮他选择一条最短的路。

**输入格式**

第一行是一个整数，表示村庄数 $n$。  
接下来 $n$ 行，每行 $n$ 个整数，第 $i$ 行的第 $j$ 个整数表示 $i$ 到 $j$ 的单向路径的距离 $s_{i,j}$。

**输出格式**

一行一个整数表示最短的路程。

输入 #1

```
3
0 2 1
1 0 2
2 1 0
```

输出 #1

```
3
```

对全部的测试数据，保证 $2 \leq n \leq 20$，$1 \leq s_{i,j} < 10^3$。

### 算法解析：

TSP 状压 DP：$dp[mask][j]$ 表示已访问集合为 $mask$、当前在城市 $j$ 的最小路程。转移：从任意 $k\in mask$（$k\ne j$）走来，$dp[mask][j]=\min(dp[mask \oplus 2^j][k]+s[k][j])$。最后回到起点，$ans=\min_j(dp[2^n-1][j]+s[j][0])$。复杂度 $O(2^n\cdot n^2)$。

### Python代码实现

```python
n = int(input())
s = []
for i in range(n):
    s.append(list(map(int, input().split())))

dp = [[1145145 ** 5 for i in range(n)] for _ in range(2 ** n)]
dp[2 ** 0][0] = 0
for i in range(2 ** n):
    for j in range(n):
        if i & 2 ** j:
            for k in range(n):
                if i & 2 ** k and k != j:
                    dp[i][j] = min(dp[i][j], dp[i ^ 2 ** j][k] + s[k][j])
# 为了回到原点
ans = min(dp[2 ** n - 1][j] + s[j][0] for j in range(1, n))
print(ans)
```

### C++代码实现

```c++
#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<vector<int>> s(n, vector<int>(n));
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            cin >> s[i][j];
        }
    }
    const int INF = 1e9;  // 比较大的数即可
    vector<vector<int>> dp(1 << n, vector<int>(n, INF));
    dp[1][0] = 0; // 只访问了点0，最后停在0
    for (int mask = 0; mask < (1 << n); mask++) {
        for (int j = 0; j < n; j++) {
            if (mask & (1 << j)) { // j在集合中
                for (int k = 0; k < n; k++) {
                    if ((mask & (1 << k)) && k != j) {
                        dp[mask][j] = min(dp[mask][j],
                                          dp[mask ^ (1 << j)][k] + s[k][j]);
                    }
                }
            }
        }
    }
    int ans = INF;
    for (int j = 1; j < n; j++) {
        ans = min(ans, dp[(1 << n) - 1][j] + s[j][0]);
    }
    cout << ans << "\n";
    return 0;
}
```
