---
title: "A12 ST表"
categories:
- [算法, A 基础算法]
tags:
- 基础算法
---

### 题目情境

![image-20250416090732094](/images/A/A12-1.png)

![image-20250416090758400](/images/A/A12-2.png)

![image-20250416090830823](/images/A/A12-3.png)

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
