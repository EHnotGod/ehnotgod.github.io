---
title: "E20 单调队列优化dp"
publishDate: 2026-08-08
description: "单调队列优化 DP：维护滑动窗口最值转移。"
category: algo
tags:
  - 动态规划
language: zh
---

### 题目情境

题目链接：https://www.luogu.com.cn/problem/P1725

**题目描述**

小河可以看作一列格子依次编号为 $0$ 到 $n$，琪露诺只能从编号小的格子移动到编号大的格子。当她在格子 $i$ 时，她只移动到区间 $[i+L,\ i+R]$ 中的任意一格。每一个格子都有一个冰冻指数 $a_i$，当琪露诺停留在那一格时就可以得到那一格的冰冻指数。琪露诺希望在到达对岸时获取最大的冰冻指数。

开始时，琪露诺在编号 $0$ 的格子上，只要她下一步的位置编号大于 $n$ 就算到达对岸。

**输入格式**

第一行三个正整数 $n,L,R$。

第二行共 $n+1$ 个整数，第 $i$ 个数表示编号为 $i-1$ 的格子的冰冻指数 $a_{i-1}$。

**输出格式**

一个整数，表示最大冰冻指数。

输入 #1

```
5 2 3
0 12 3 11 7 -2
```

输出 #1

```
11
```

**说明/提示**

对于 $60\%$ 的数据，$1\le n\le 10^4$；对于 $100\%$ 的数据，$1\le n\le 2\times 10^5$，$1\le L\le R\le n$，$-1000\le a_i\le 1000$。数据保证最终答案不超过 $2^{31}-1$。

### 算法解析：

设 $f[i]$ 为停在格子 $i$ 时的最大冰冻指数，初始 $f[0]=a_0$，其余状态不可达。转移为 $f[i]=a_i+\max_{i-R\le j\le i-L}f[j]$。用单调队列维护这个区间：加入新下标 $i-L$，弹出小于 $i-R$ 的下标，队尾保持 $f$ 值递减，队头即最优前驱。最后从满足 $i+R>n$ 的可达格子中取最大值。每个下标最多入队、出队一次，时间和空间复杂度均为 $O(n)$。

### Python代码实现

```python
from collections import deque
import sys

data = list(map(int, sys.stdin.buffer.read().split()))
n, L, R = data[:3]
a = data[3:]
q = deque()
f = [float('-inf')] * (n + 1)
f[0] = a[0]
for i in range(1, n + 1):
    j = i - L
    if j >= 0 and f[j] != float('-inf'):
        while q and f[q[-1]] <= f[j]:
            q.pop()
        q.append(j)
    while q and q[0] < i - R:
        q.popleft()
    if q:
        f[i] = f[q[0]] + a[i]
print(max(f[max(0, n - R + 1):]))
```

### C++代码实现

```c++
// 单调队列优化区间最大值转移，O(n)
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n,L,R;
  cin >> n >> L >> R;
  vector<int> a,q;
  vector<long long> f;
  a.assign(n+1,0);
  q.assign(n+1,0);
  const long long NEG=-(1LL<<60);
  f.assign(n+1,NEG);
  for (int i=0; i<=n; ++i) cin >> a[i];
  f[0]=a[0];
  int h=0,t=0;
  for (int i=1; i<=n; ++i) {
    int j=i-L; //新进入候选区间的状态
    if (j>=0 && f[j]!=NEG) {
      while (h<t && f[q[t-1]]<=f[j]) --t;
      q[t++]=j;
    }
    while (h<t && q[h]<i-R) ++h;
    if (h<t) f[i]=f[q[h]]+a[i];
  }
  long long ans=NEG;
  for (int i=max(0,n-R+1); i<=n; ++i) ans=max(ans,f[i]);
  cout << ans << '\n';
}
```
