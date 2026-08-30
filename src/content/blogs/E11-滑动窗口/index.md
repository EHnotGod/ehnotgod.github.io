---
title: "E11 滑动窗口"
publishDate: 2026-08-08
description: "滑动窗口：双端队列（单调队列）维护区间最值。"
category: algo
tags:
  - 动态规划
language: zh
---

### 题目情境

题目链接：https://www.luogu.com.cn/problem/P1886

**题目描述**

有一个长为 $$n$$ 的序列 $$a$$，以及一个大小为 $$k$$ 的窗口。现在这个从左边开始向右滑动，每次滑动一个单位，求出每次滑动后窗口中的最大值和最小值。

### 算法解析：

单调队列维护窗口内最值：用双端队列存下标，保证队列内元素对应值单调。每次新元素入队前，把队尾比它小（求最大值）/大（求最小值）的元素弹出；同时把滑出窗口的下标从队头弹出。队头即当前窗口最值。复杂度 $O(n)$。

### Python代码实现

```python
import sys
from collections import deque

input = sys.stdin.readline

n, k = map(int, input().split())
a = [0] * (n + 1)  # Using 1-based indexing to match the C++ code
a[1:] = list(map(int, input().split()))

# Maintain window minimum
q = deque()
for i in range(1, n + 1):
    while len(q) > 0 and a[q[-1]] >= a[i]:
        q.pop()
    q.append(i)
    while q[0] < i - k + 1:
        q.popleft()
    if i >= k:
        print(a[q[0]], end=' ')
print()

# Maintain window maximum
q = deque()
for i in range(1, n + 1):
    while len(q) > 0 and a[q[-1]] <= a[i]:
        q.pop()
    q.append(i)
    while q[0] < i - k + 1:
        q.popleft()
    if i >= k:
        print(a[q[0]], end=' ')
```

### C++代码实现

```c++
#include <iostream>
#include <deque>
using namespace std;

const int N=1000010;
int a[N];
deque<int> q;

int main(){
  int n, k; scanf("%d%d", &n, &k);
  for(int i=1; i<=n; i++) scanf("%d", &a[i]);

  // 维护窗口最小值
  q.clear();                              //清空队列
  for(int i=1; i<=n; i++){                //枚举序列
    while(!q.empty() && a[q.back()]>=a[i]) q.pop_back(); //队尾出队(队列不空且新元素更优)
    q.push_back(i);                       //队尾入队(存储下标 方便判断队头出队)
    while(q.front()<i-k+1) q.pop_front(); //队头出队(队头元素滑出窗口)
    if(i>=k) printf("%d ",a[q.front()]);  //使用最值
  }
  puts("");

  // 维护窗口最大值
  q.clear();
  for(int i=1; i<=n; i++){
    while(!q.empty() && a[q.back()]<=a[i]) q.pop_back();
    q.push_back(i);
    while(q.front()<i-k+1) q.pop_front();
    if(i>=k) printf("%d ",a[q.front()]);
  }
}
```
