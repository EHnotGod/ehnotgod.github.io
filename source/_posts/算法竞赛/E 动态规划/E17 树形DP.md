---
title: "E17 树形DP"
categories:
- [算法, E 动态规划]
tags:
- 动态规划
---

### Python代码实现

```python
import sys
sys.setrecursionlimit(int(1e7))
N = 6010
head = [0] * N
to = [0] * N
ne = [0] * N
idx = 0
def add(a, b):
    global idx
    idx += 1
    to[idx] = b; ne[idx] = head[a]; head[a] = idx
w = [0] * N
fa = [0] * N
f = [[0 for i in range(2)] for j in range(N)]
def dfs(u):
    f[u][1] = w[u]
    i = head[u]
    while i != 0:
        v = to[i]
        dfs(v)
        f[u][0] += max(f[v][0], f[v][1])
        f[u][1] += f[v][0]
        i = ne[i]
n = int(input())
for i in range(1, n + 1):
    w[i] = int(input())
for i in range(n - 1):
    a, b = map(int, input().split())
    add(b, a)
    fa[a] = True
root = 1
while fa[root]:
    root += 1
dfs(root)
print(max(f[root][0], f[root][1]))
```

### C++代码实现

```c++
#include <iostream>
#include <cstring>
#include <algorithm>
using namespace std;

const int N=6010;
int head[N],to[N],ne[N],idx;
void add(int a,int b){
  to[++idx]=b,ne[idx]=head[a],head[a]=idx;
}
int n,w[N],fa[N];
int f[N][2]; //0不选,1选

void dfs(int u){
  f[u][1]=w[u];
  for(int i=head[u];i;i=ne[i]){
    int v=to[i];
    dfs(v);
    f[u][0]+=max(f[v][0],f[v][1]);
    f[u][1]+=f[v][0];
  }
}
int main(){
  cin>>n;
  for(int i=1;i<=n;i++) cin>>w[i];
  for(int i=0,a,b;i<n-1;i++){
    cin>>a>>b;
    add(b,a);
    fa[a]=true;
  }
  int root=1;
  while(fa[root]) root++;
  dfs(root);
  cout<<max(f[root][0],f[root][1]);
}
```
