---
title: "D21 树的重心"
publishDate: 2026-08-08
description: "树的重心：删去后最大子树最小。"
category: algo
tags:
  - 图论
language: zh
---

### 题目情境

题目链接：https://www.luogu.com.cn/problem/P1364

**题目描述**

给定一个 $n$ 个节点的**无根树**，节点按照 $1 \sim n$ 编号，并且无**自环**和**重边**。求它的重心，如果有多个重心，按照编号从小到大的顺序依次输出。

**输入格式**

第一行：一个整数 $n$，含义见题目描述。  
接下来 $n-1$ 行，每行两个整数 $u,v$，代表 $u$ 和 $v$ 之间有一条连边。

**输出格式**

仅一行，按照编号从小到大输出重心。

输入 #1

```
6
1 2
2 3
2 5
3 4
3 6
```

输出 #1

```
2 3
```

输入 #2

```
8
1 2
2 3
3 4
4 5
5 6
6 7
7 8

```

输出 #2

```
4 5
```


对于 $100\%$ 的数据，$2 \leq n \leq 5 \times 10^4$。

### 算法解析：

树的重心：删去某点后，剩余连通块中最大者最小。DFS 求每个点的子树大小 $siz[u]$，则删去 $u$ 后最大子树为 $\max(儿子们的 siz,\ n-siz[u])$（$n-siz[u]$ 是上方部分），取所有点的最小值即重心对应的值。复杂度 $O(n)$。

### Python代码实现

```python
import sys
sys.setrecursionlimit(100000)
input = sys.stdin.readline
n = int(input())
e = [[] for i in range(n + 1)]
for i in range(n - 1):
    u, v = map(int, input().split())
    e[u].append(v); e[v].append(u)
siz = [0] * (n + 1)
f = [0] * (n + 1)
cnt = int(1e9)
def dfs(u, p):
    global cnt
    siz[u] = 1
    for v in e[u]:
        if v != p:
            dfs(v, u)
            siz[u] += siz[v]
            f[u] = max(f[u], siz[v])
    f[u] = max(f[u], n - siz[u])
    cnt = min(cnt, f[u])
dfs(1, 0)
for i in range(1, n + 1):
    if f[i] == cnt:
        print(i, end = " ")
```

### C++代码实现

```c++
// 树的重心 树形DP O(n)
#include<bits/stdc++.h>
using namespace std;

const int N=50010;
int n,siz[N],f[N],cnt=1e9;
vector<int> e[N],g;

void dfs(int u,int fa){
  siz[u]=1;
  for(auto v:e[u]){
    if(v==fa) continue;
    dfs(v,u);
    f[u]=max(f[u],siz[v]); //u的最大子树
    siz[u]+=siz[v];
  }
  f[u]=max(f[u],n-siz[u]); //删除u后的最大连通块
  cnt=min(cnt,f[u]);       //最大块最小化
}
int main(){
  scanf("%d",&n);
  for(int i=1,a,b;i<n;i++){
    scanf("%d%d",&a,&b);
    e[a].push_back(b);
    e[b].push_back(a);
  }
  dfs(1,0);
  for(int i=1;i<=n;i++) if(f[i]==cnt) g.push_back(i);
  for(int v:g) printf("%d ",v);
}
```
