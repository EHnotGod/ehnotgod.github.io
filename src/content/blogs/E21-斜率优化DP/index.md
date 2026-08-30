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

斜率优化 DP：当转移式中含 $f[j]+a[i]\cdot b[j]$ 这类项时，把候选 $j$ 看作平面上的点 $(dx,dy)$，用凸包维护最优斜率。用单调队列使相邻点斜率单调（下凸包），每次用当前斜率弹出队头不优的点，队头即最优转移。本题为玩具装箱（HNOI2008），复杂度 $O(n)$。

### Python代码实现

```python
import sys
input = sys.stdin.readline

while True:
    line = input()
    if not line:
        break
    n, m = map(int, line.split())
    s = [0] + list(map(int, input().split()))
    for i in range(1, n + 1):
        s[i] += s[i - 1]

    def dy(i, j):
        return f[i] + s[i] * s[i] - f[j] - s[j] * s[j]

    def dx(i, j):
        return s[i] - s[j]

    f = [0] * (n + 1)
    q = [0] * (n + 1)
    h, t = 1, 0
    for i in range(1, n + 1):
        while h < t and dy(i - 1, q[t]) * dx(q[t], q[t - 1]) <= dx(i - 1, q[t]) * dy(q[t], q[t - 1]):
            t -= 1
        t += 1
        q[t] = i - 1
        while h < t and dy(q[h + 1], q[h]) <= dx(q[h + 1], q[h]) * 2 * s[i]:
            h += 1
        j = q[h]
        f[i] = f[j] + (s[i] - s[j]) * (s[i] - s[j]) + m
    print(f[n])
```

### C++代码实现

```c++
#include <iostream>
#include <cstring>
#include <algorithm>
using namespace std;

typedef long long LL;
const int N = 500010;
int n,m,q[N];
LL s[N],f[N];

LL dy(int i,int j){return f[i]+s[i]*s[i]-f[j]-s[j]*s[j];}
LL dx(int i,int j){return s[i]-s[j];}
int main(){
  while(~scanf("%d%d",&n,&m)){
    for(int i=1;i<=n;i++)scanf("%lld",&s[i]),s[i]+=s[i-1];

    int h=1,t=0;
    for(int i=1;i<=n;i++){
      while(h<t && dy(i-1,q[t])*dx(q[t],q[t-1])
                 <=dx(i-1,q[t])*dy(q[t],q[t-1])) t--;
      q[++t]=i-1;      
      while(h<t && dy(q[h+1],q[h])
                 <=dx(q[h+1],q[h])*2*s[i]) h++;
      int j=q[h];
      f[i]=f[j]+(s[i]-s[j])*(s[i]-s[j])+m;
    }
    printf("%lld\n",f[n]);
  }
}
```
