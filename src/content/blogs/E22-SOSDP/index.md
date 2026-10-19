---
title: "E22 SOS DP（高维前缀和）"
publishDate: 2026-10-19
description: "SOS DP：用高维前缀和在 O(n·2^n) 时间内求出所有状态的子集和，附 Python、C++ 模板与超集和、按位与为零的应用。"
category: algo
tags:
  - 动态规划
  - 状态压缩
language: zh
---

### 题目情境

给定一个长度为 $2^n$ 的数组 $a$，下标视作一个 $n$ 位二进制集合。对于每个集合 $S$，求它所有子集对应的权值之和：

$$
f[S] = \sum_{T\subseteq S} a[T]
$$

这里的子集包含空集和 $S$ 本身。判断 $T$ 是否为 $S$ 的子集，可以写成 `(T & S) == T`。

例如 $S=5=(101)_2$，它的子集是 $0,1,4,5$，所以 $f[5]=a[0]+a[1]+a[4]+a[5]$。

**输入格式**

第一行一个整数 $n$。接下来输入 $2^n$ 个整数，依次表示 $a[0],a[1],\ldots,a[2^n-1]$。

约定 $0\le n\le 20$，$|a[S]|\le 10^9$。

**输出格式**

按下标顺序输出 $2^n$ 个子集和。

输入示例：

```text
3
1 2 3 4 5 6 7 8
```

输出示例：

```text
1 3 4 10 6 14 16 36
```

### 算法解析

SOS DP 的全称是 Sum Over Subsets DP，也叫高维前缀和。它适合一次性计算所有状态的子集信息。

#### 从枚举子集开始

对每个 $S$，可以用 `(T - 1) & S` 枚举它的非空子集，再单独加上空集的贡献：

```python
f = [0] * (1 << n)
for mask in range(1 << n):
    f[mask] = a[0]
    sub = mask
    while sub:
        f[mask] += a[sub]
        sub = (sub - 1) & mask
```

一个有 $k$ 个二进制 $1$ 的集合有 $2^k$ 个子集，计算所有集合需要：

$$
\sum_{k=0}^{n}\binom{n}{k}2^k=3^n
$$

因此总时间复杂度为 $O(3^n)$。当 $n$ 接近 $20$ 时，这个做法就很吃力了。

#### 按二进制位分组转移

把每个二进制位看成一条只有 $0,1$ 两个坐标的轴，子集和就是沿着这 $n$ 条轴依次累加的前缀和。

定义 $dp_i[S]$：只允许低 $i$ 位从 $S$ 中删去元素，其余位保持不变时，所有可达子集的权值和。初始时没有处理任何位，所以 $dp_0[S]=a[S]$。

处理第 $i$ 位（从 $0$ 开始编号）时：

- 如果 $S$ 的第 $i$ 位是 $0$，这一位只能保持 $0$。
- 如果这一位是 $1$，子集分成保留这一位、删去这一位两组，两组互不相交。

因此：

$$
dp_{i+1}[S]=
\begin{cases}
dp_i[S], & S\mathbin{\&}2^i=0 \\
dp_i[S]+dp_i[S\oplus 2^i], & S\mathbin{\&}2^i\ne 0
\end{cases}
$$

所有位处理完后，$dp_n[S]$ 就是所求的 $f[S]$。

#### 压成一维数组

对固定的第 $i$ 位，转移来源 `mask ^ (1 << i)` 的这一位一定是 $0$，它在本轮不会被修改，因此可以直接原地累加。

以示例中的数组为例，每处理一位，数组依次变为：

| 阶段 | 下标 0～7 的值 |
| --- | --- |
| 初始化 | 1, 2, 3, 4, 5, 6, 7, 8 |
| 处理第 0 位 | 1, 3, 3, 7, 5, 11, 7, 15 |
| 处理第 1 位 | 1, 3, 4, 10, 5, 11, 12, 26 |
| 处理第 2 位 | 1, 3, 4, 10, 6, 14, 16, 36 |

一共处理 $n$ 位，每轮遍历 $2^n$ 个状态，时间复杂度为 $O(n\cdot 2^n)$，空间复杂度为 $O(2^n)$。

### Python代码实现

```python
import sys


def sos_dp(a, n):
    f = a.copy()
    for i in range(n):
        bit = 1 << i
        for mask in range(1 << n):
            if mask & bit:
                f[mask] += f[mask ^ bit]
    return f


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    a = data[1:]
    f = sos_dp(a, n)
    print(*f)


if __name__ == "__main__":
    main()
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
    int size = 1 << n;
    vector<long long> f(size);
    for (auto &x : f) cin >> x;

    for (int i = 0; i < n; i++) {
        int bit = 1 << i;
        for (int mask = 0; mask < size; mask++) {
            if (mask & bit) {
                f[mask] += f[mask ^ bit];
            }
        }
    }

    for (int mask = 0; mask < size; mask++) {
        if (mask) cout << ' ';
        cout << f[mask];
    }
    cout << '\n';
    return 0;
}
```

### 常见变形

#### 超集和

如果要计算 $g[S]=\sum_{T\supseteq S}a[T]$，则从第 $i$ 位为 $1$ 的状态向第 $i$ 位为 $0$ 的状态累加：

```python
g = a.copy()
for i in range(n):
    bit = 1 << i
    for mask in range(1 << n):
        if (mask & bit) == 0:
            g[mask] += g[mask | bit]
```

#### 统计按位与为零的数

若数组中的数都在 $[0,2^n)$ 内，先令 `cnt[x]` 表示数值 $x$ 的出现次数，然后对 `cnt` 做子集和。

对于给定的 $x$，满足 `x & y == 0` 的 $y$ 必须是 $x$ 在这 $n$ 位内的补集的子集。因此：

```python
f = sos_dp(cnt, n)
full = (1 << n) - 1
answer = f[full ^ x]
```

这里统计的是数组元素的出现次数。如果题目要求排除当前元素本身，要另外判断它是否满足条件；例如 $x=0$ 时，需要减去它自己的那一次贡献。

### 注意事项

- 一维原地写法中，二进制位必须放在外层循环。直接交换两层循环会重复计算部分贡献。
- 初始化用 `f = a.copy()`，空集的贡献已经在数组中，不需要再额外补加。
- Python 的 `~mask` 会得到负数，求有限位补集应使用 `full ^ mask`，且保证 `mask` 在 $[0,2^n)$ 内。
- C++ 应根据答案范围选择整数类型，本例的子集和需要 `long long`。
- 若只查询一个集合的子集和，枚举其子集可能更省；SOS DP 的优势在于同时处理所有集合。
- 转移也可以合并子集最大值、最小值等信息，但要求每个子集的贡献能独立合并；涉及子集之间配对或划分的转移，需要单独分析。
- Python 中 $2^n$ 级别的列表和整数会占用较多内存，接近上界时应结合时限、内存限制评估，必要时使用 C++。

### 参考与练习

- [Codeforces：SOS Dynamic Programming 教程](https://codeforces.com/blog/entry/45223)
- [CSES：SOS Bit Problem](https://cses.fi/problemset/task/1654/)，可以结合子集和、超集和与补集练习。
