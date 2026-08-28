---
title: "D7 Kruscal算法"
publishDate: 2026-08-08
description: "Kruscal 最小生成树：按边权排序 + 并查集。"
category: algo
tags:
  - 图论
language: zh
---

### 题目情境

题目链接：https://www.luogu.com.cn/problem/P3366

**题目描述**

如题，给出一个无向图，求出最小生成树（Kruskal：按边权从小到大排序，用并查集维护连通性）。

### 算法解析：

Kruskal 求最小生成树：把所有边按边权升序排序，依次尝试加入，若边的两端点当前不连通（并查集不同集合）则加入，直到连成 $n-1$ 条边；若最终边数不足 $n-1$ 说明图不连通（输出 orz）。复杂度 $O(m\log m)$。

### Python代码实现

```python
class Edge():
    def __init__(self, u, v, w):
        self.u = u
        self.v = v
        self.w = w

def find(x):
    if fa[x] == x:
        return x
    fa[x] = find(fa[x])
    return fa[x]
def union(x, y):
    fa[find(x)] = find(y)
def kruskal():
    global ans, cnt
    e.sort(key=lambda k:k.w)
    for i in range(m):
        x = find(e[i].u)
        y = find(e[i].v)
        if x != y:
            union(x, y)
            ans += e[i].w
            cnt += 1
    return cnt == n - 1


n, m = map(int, input().split())
fa = [i for i in range(n + 1)]
ans, cnt = 0, 0
e = []
for i in range(m):
    u, v, w = map(int, input().split())
    e.append(Edge(u, v, w))
if not kruskal():
    print("orz")
else:
    print(ans)
```

### C++代码实现

```c++
// Luogu P3366 【模板】最小生成树
#include <iostream>
#include <cstring>
#include <algorithm>
using namespace std;

const int N=200006;
int n, m;
struct edge{
  int u,v,w;
  bool operator<(const edge &t)const
  {return w < t.w;}
}e[N];
int fa[N],ans,cnt;

int find(int x){
  if(fa[x]==x) return x;
  return fa[x]=find(fa[x]);
}
bool kruskal(){
  sort(e,e+m);
  for(int i=1;i<=n;i++)fa[i]=i;
  for(int i=0; i<m; i++){
    int x=find(e[i].u);
    int y=find(e[i].v);
    if(x!=y){
      fa[x]=y;
      ans+=e[i].w;
      cnt++;
    }
  }
  return cnt==n-1;
}
int main(){
  cin>>n>>m;
  for(int i=0; i<m; i++)
    cin>>e[i].u>>e[i].v>>e[i].w;
  if(!kruskal()) puts("orz");
  else printf("%d\n",ans);
  return 0;
}
```
