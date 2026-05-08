---
title: "A11 ST表"
categories:
- [算法, A 基础算法]
tags:
- 基础算法
---

### 题目情境

**题目描述**

给定一个长度为 $$N$$ 的数列，和 $$ M $$ 次询问，求出每一次询问的区间内数字的最大值。

**输入格式**

第一行包含两个整数 $$N,M$$，分别表示数列的长度和询问的个数。

第二行包含 $$N$$ 个整数（记为 $$a_i$$），依次表示数列的第 $$i$$ 项。

接下来 $$M$$ 行，每行包含两个整数 $$l_i,r_i$$，表示查询的区间为 $$[l_i,r_i]$$。

**输出格式**

输出包含 $$M$$ 行，每行一个整数，依次表示每一次询问的结果。

**输入输出样例**

输入 #1

```
8 8
9 3 1 7 5 6 0 8
1 6
1 5
2 7
2 6
1 8
4 8
3 7
1 8
```
输出 #1

```
9
9
7
7
9
8
7
9
```
**说明/提示**

对于 $$30\%$$ 的数据，满足 $$1\le N,M\le 10$$。

对于 $$70\%$$ 的数据，满足 $$1\le N,M\le {10}^5$$。

对于 $$100\%$$ 的数据，满足 $$1\le N\le {10}^5$$，$$1\le M\le 2\times{10}^6$$，$$a_i\in[0,{10}^9]$$，$$1\le l_i\le r_i\le N$$。
### 算法解析
![image](/images/算法竞赛/A/A11-1.png)

![image](/images/算法竞赛/A/A11-2.png)

### Python代码实现

```python
# P3865 【模板】ST 表 && RMQ 问题

import math
n, m = map(int, input().split())
h = list(map(int, input().split()))

# 使用ST表处理最大值
max_log = 20
f = [[0] * (max_log + 1) for _ in range(n + 1)]
for i in range(1, n + 1):
    f[i][0] = h[i - 1]
for j in range(1, max_log + 1):
    i = 1
    while i + 2 ** j - 1 <= n:
        mid = i + 2 ** (j - 1)
        f[i][j] = max(f[i][j - 1], f[mid][j - 1])
        i += 1
def find(l, r):
    k = int(math.log2(r - l + 1))
    ma = max(f[l][k], f[r - 2 ** k + 1][k])
    return ma
for i in range(m):
    l, r = map(int, input().split())
    print(find(l, r))
```

### C++代码实现

```c++
#include <iostream>
#include <cstring>
#include <algorithm>
#include <cmath>
using namespace std;

int f[100005][22];

int main(){
  int n,m; scanf("%d%d",&n,&m);

  for(int i=1;i<=n;i++) scanf("%d",&f[i][0]);
  for(int j=1;j<=20;j++) //枚举区间长度
    for(int i=1;i+(1<<j)-1<=n;i++) //枚举起点
      f[i][j]=max(f[i][j-1],f[i+(1<<(j-1))][j-1]);

  for(int i=1,l,r;i<=m;i++){
    scanf("%d%d",&l,&r);
    int k=log2(r-l+1); //区间长度的指数
    printf("%d\n",max(f[l][k],f[r-(1<<k)+1][k]));
  }
}
```
