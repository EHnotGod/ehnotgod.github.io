---
title: "D8 Kruscal算法"
categories:
- [算法, D 图论]
tags:
- 图论
---

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
