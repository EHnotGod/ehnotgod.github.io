---
title: "E21 斜率优化DP"
publishDate: 2026-08-08
description: "斜率优化 DP：凸包维护转移斜率。"
category: algo
tags:
  - 动态规划
language: zh
---

### 题目情境

题目链接：https://www.luogu.com.cn/problem/P3195

**题目描述**

P 教授要去看奥运，但他舍不下他的玩具，于是决定把所有的玩具运到北京。他有编号为 $1\sim n$ 的 $n$ 件玩具，第 $i$ 件玩具经过压缩后的一维长度为 $c_i$。为了方便整理，P 教授要求在一个一维容器中的玩具编号是连续的。同时如果一个一维容器中有多个玩具，那么两件玩具之间要加入一个单位长度的填充物。形式地说，如果将第 $i$ 件玩具到第 $j$ 个玩具放到一个容器中，那么容器的长度将为 $j-i+\sum_{k=i}^{j} c_k$。

制作容器的费用与容器的长度有关，如果容器长度为 $x$，其制作费用为 $(x-L)^2$，其中 $L$ 是一个常量。P 教授不关心容器的数目，但他希望所有容器的总费用最小。

**输入格式**

第一行有两个整数，用一个空格隔开，分别代表 $n$ 和 $L$。

第 $2$ 到第 $n+1$ 行，每行一个整数，第 $(i+1)$ 行的整数代表第 $i$ 件玩具的长度 $c_i$。

**输出格式**

输出一行一个整数，代表所有容器的总费用最小是多少。

输入 #1

```
5 4
3
4
2
1
4
```

输出 #1

```
1
```

**说明/提示**

对于全部的测试点，$1\le n\le 5\times 10^4$，$1\le L\le 10^7$，$1\le c_i\le 10^7$。

### 算法解析：

令 $s_i=\sum_{k=1}^{i}(c_k+1)$，把第 $j+1$ 到第 $i$ 件玩具装进一个容器的费用为 $(s_i-s_j-L-1)^2$。设 $x_i=s_i-L-1$，则 $f[i]=x_i^2+\min_{j<i}(f[j]+s_j^2-2x_i s_j)$。把候选状态看成点 $(s_j,f[j]+s_j^2)$，维护下凸包。由于 $c_i>0$，横坐标和查询斜率都递增，可用单调队列在线性时间内完成所有转移。C++ 中平方与叉乘使用 `__int128` 中间值，避免前缀和平方溢出；状态数组在每组输入后按 $n$ 初始化。时间和空间复杂度均为 $O(n)$。

### Python代码实现

```python
import sys

data = iter(map(int, sys.stdin.buffer.read().split()))
while True:
    try:
        n = next(data)
    except StopIteration:
        break
    L = next(data)
    s = [0] * (n + 1)
    f = [0] * (n + 1)
    q = [0] * (n + 1)
    for i in range(1, n + 1):
        s[i] = s[i - 1] + next(data) + 1

    def dy(i, j):
        return f[i] + s[i] * s[i] - f[j] - s[j] * s[j]

    def dx(i, j):
        return s[i] - s[j]

    h, t = 0, 1
    for i in range(1, n + 1):
        x = s[i] - L - 1
        while h + 1 < t and dy(q[h + 1], q[h]) <= 2 * x * dx(q[h + 1], q[h]):
            h += 1
        j = q[h]
        f[i] = f[j] + (x - s[j]) ** 2
        while h + 1 < t and dy(q[t - 1], q[t - 2]) * dx(i, q[t - 1]) >= dy(i, q[t - 1]) * dx(q[t - 1], q[t - 2]):
            t -= 1
        q[t] = i
        t += 1
    print(f[n])
```

### C++代码实现

```c++
#include <bits/stdc++.h>
using namespace std;

using LL=long long;
vector<LL> s,f;
vector<int> q;

__int128 dy(int i,int j) {
  return (__int128)f[i]+(__int128)s[i]*s[i]-f[j]-(__int128)s[j]*s[j];
}
LL dx(int i,int j) { return s[i]-s[j]; }

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  LL L;
  while (cin >> n >> L) {
    s.assign(n+1,0);
    f.assign(n+1,0);
    q.assign(n+1,0);
    for (int i=1; i<=n; ++i) {
      LL c;
      cin >> c;
      s[i]=s[i-1]+c+1;
    }
    int h=0,t=1; //候选0已经入队
    for (int i=1; i<=n; ++i) {
      LL x=s[i]-L-1;
      while (h+1<t && dy(q[h+1],q[h])<=(__int128)2*x*dx(q[h+1],q[h])) ++h;
      int j=q[h];
      LL d=x-s[j];
      f[i]=(LL)((__int128)f[j]+(__int128)d*d);
      while (h+1<t && dy(q[t-1],q[t-2])*dx(i,q[t-1])>=dy(i,q[t-1])*dx(q[t-1],q[t-2])) --t;
      q[t++]=i;
    }
    cout << f[n] << '\n';
  }
}
```
