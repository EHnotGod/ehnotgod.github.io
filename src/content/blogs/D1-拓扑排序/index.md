---
title: "D1 拓扑排序"
publishDate: 2026-08-08
description: "拓扑排序：有向无环图的线性排序。"
category: algo
tags:
  - 图论
language: zh
---

### 题目情境

题目链接：https://www.luogu.com.cn/problem/B3644

**题目描述**

有个人的家族很大，辈分关系很混乱，请你帮整理一下这种关系。给出每个人的后代的信息。输出一个序列，使得每个人的后辈都比那个人后列出。

**输入格式**

第 $$1$$ 行一个整数 $$N$$（$$1 \le N \le 100$$），表示家族的人数。接下来 $$N$$ 行，第 $$i$$ 行描述第 $$i$$ 个人的后代编号 $$a_{i,j}$$，表示 $$a_{i,j}$$ 是 $$i$$ 的后代。每行最后是 $$0$$ 表示描述完毕。

**输出格式**

输出一个序列，使得每个人的后辈都比那个人后列出。如果有多种不同的序列，输出任意一种即可。

输入 #1

```
5
0
4 5 1 0
1 0
5 3 0
3 0
```

输出 #1

```
2 4 5 3 1
```

### 算法解析：

Kahn 算法：统计每个点的入度，把入度为 0 的点入队；每次取出队首加入拓扑序列，并把其后继的入度减 1，若减到 0 则入队。若队列空时还没遍历完所有点，说明图中有环。复杂度 $O(n+m)$。

### Python代码实现

```python
# 拓扑排序 Kahn算法 O(V+E)
from collections import deque
N = 110
n = int(input())
rd = [0] * N          # 入度
e = [[] for _ in range(N)]   # 邻接表
tp = []               # 拓扑序
def topo():
    q = deque()
    # 入度为0的点全部入队
    for i in range(1, n + 1):
        if rd[i] == 0:
            q.append(i)
    while q:
        u = q.popleft()     # 出队
        tp.append(u)        # 记录拓扑序
        for v in e[u]:
            rd[v] -= 1      # 删除 u->v 这条边
            if rd[v] == 0:
                q.append(v)
    return len(tp) == n
for i in range(1, n + 1):
    a = list(map(int, input().split()))
    for j in a:
        if j == 0:
            break
        e[i].append(j)
        rd[j] += 1
topo()
print(*tp)
```

### C++代码实现

```c++
// Kahn算法 O(n)
// 拓扑排序 Kahn算法 O(V+E)
#include<bits/stdc++.h>
using namespace std;

const int N=110;
int n,rd[N];
vector<int> e[N],tp;

bool topo(){
  queue<int> q;
  for(int i=1; i<=n; i++) if(!rd[i]) q.push(i); //入度为0的点均入队
  while(q.size()){
    int u=q.front(); q.pop(); //出队
    tp.push_back(u); //记录拓扑序
    for(auto v:e[u]) if(--rd[v]==0) q.push(v); //入队
  }
  return tp.size()==n;
}
int main(){
  cin>>n;
  for(int i=1,j; i<=n; i++){
    while(cin>>j,j){
      e[i].push_back(j);
      rd[j]++; //入度
    }
  }
  topo();
  for(int i=0; i<n; i++) cout<<tp[i]<<" ";
}
```
