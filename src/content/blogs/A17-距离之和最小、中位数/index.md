---
title: "A17 距离之和最小、中位数"
publishDate: 2026-08-08
description: "中位数性质：使各点距离和最小的点恰是中位数。"
category: algo
tags:
  - 基础算法
language: zh
---

### 题目情境

题目链接：https://codeforces.com/problemset/problem/1486/B

![image-20250416092236944](/images/算法竞赛/A/A17-1.png)

### 算法解析

中位数性质：使各点距离和最小的点恰是中位数。

因为求的是曼哈顿距离，我们可以把x和y分开看，然后分别找到各自的x和y即为所求点。

本题的本质是贪心。

### Python代码实现

```python
t = int(input())
for _ in range(t):
    n = int(input())
    a = [0] * n
    b = [0] * n
    for i in range(n):
        a[i], b[i] = map(int, input().split())
    a.sort()
    b.sort()
    x = a[n // 2] - a[(n - 1) // 2] + 1
    y = b[n // 2] - b[(n - 1) // 2] + 1
    print(x * y)
```

### C++代码实现

```c++
#include <iostream>
#include <cstring>
#include <algorithm>
using namespace std;

const int N=1010;
int n,a[N],b[N];

int main(){
  int t; cin>>t;
  while(t--){
    cin>>n;
    for(int i=0; i<n; i++) cin>>a[i]>>b[i];
    sort(a,a+n); sort(b,b+n);

    int x=a[n/2]-a[(n-1)/2]+1;
    int y=b[n/2]-b[(n-1)/2]+1;
    cout<<1LL*x*y<<'\n';
  }
  return 0;
}
```
