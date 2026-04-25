---
title: "E25 TSP-状压DP"
categories:
- [算法, E 动态规划]
tags:
- 动态规划
---

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
