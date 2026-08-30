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

单调队列优化 DP：当转移式是 $f[i]=\max/\min(f[j])+w$ 且 $j$ 落在长度固定的滑动窗口内时，用单调队列维护候选 $j$ 的最值。本题从 $[i-m, i-1]$ 转移：队头弹出滑出窗口的下标，队尾保持 $f$ 单调，$f[i]=f[q[h]]+a[i]$，最后取能到达末尾的最小值。复杂度 $O(n)$。

### Python代码实现

```python
from collections import deque
n, m = map(int, input().split())
a = [0] + list(map(int, input().split()))

q = deque()
f = [0] * (n + 1)
ans = float("inf")
for i in range(1, n + 1):
    while q and q[0] < i - m:
        q.popleft()               # 弹出滑出窗口的下标
    while q and f[q[-1]] >= f[i - 1]:
        q.pop()                   # 队尾保持 f 单调
    q.append(i - 1)
    f[i] = f[q[0]] + a[i]         # 队头即窗口内 f 最小值
    if i >= n - m + 1:
        ans = min(ans, f[i])
print(ans)
```

### C++代码实现

```c++
// 单调队列+DP O(n)
#include<bits/stdc++.h>
using namespace std;

const int N=200010;
int n,m,a[N];
int q[N],f[N];

int main(){
  cin>>n>>m;
  for(int i=1; i<=n; i++) cin>>a[i];
  
  int ans=2e9;
  for(int i=1,h=1,t=0; i<=n; i++){
    while(h<=t && q[h]<i-m) h++;
    while(h<=t && f[q[t]]>=f[i-1]) t--;
    q[++t]=i-1;
    f[i]=f[q[h]]+a[i];
    if(i>=n-m+1) ans=min(ans,f[i]);
  }
  cout<<ans;
}
```
