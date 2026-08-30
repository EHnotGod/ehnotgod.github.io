---
title: "E11 树形DP"
publishDate: 2026-08-08
description: "树形 DP：以子树为状态的树上动态规划。"
category: algo
tags:
  - 动态规划
language: zh
---

### 题目情境

题目链接：https://www.luogu.com.cn/problem/P1352

**题目描述**

某大学有 $n$ 个职员，编号为 $1\ldots n$。

他们之间有从属关系，也就是说他们的关系就像一棵以校长为根的树，父结点就是子结点的直接上司。

现在有个周年庆宴会，宴会每邀请来一个职员都会增加一定的快乐指数 $r_i$，但是呢，如果某个职员的直接上司来参加舞会了，那么这个职员就无论如何也不肯来参加舞会了。

所以，请你编程计算，邀请哪些职员可以使快乐指数最大，求最大的快乐指数。

**输入格式**

输入的第一行是一个整数 $n$。

第 $2$ 到第 $(n + 1)$ 行，每行一个整数，第 $(i+1)$ 行的整数表示 $i$ 号职员的快乐指数 $r_i$。

第 $(n + 2)$ 到第 $2n$ 行，每行输入一对整数 $l, k$，代表 $k$ 是 $l$ 的直接上司。

**输出格式**

输出一行一个整数代表最大的快乐指数。

输入 #1

```
7
1
1
1
1
1
1
1
1 3
2 3
6 4
7 4
4 5
3 5

```

输出 #1

```
5

```


对于 $100\%$ 的数据，保证 $1\leq n \leq 6 \times 10^3$，$-128 \leq r_i\leq 127$，$1 \leq l, k \leq n$，且给出的关系一定是一棵树。

### 算法解析：

树形 DP：以子树为状态做树上 DP。$f[u][0/1]$ 分别表示 $u$ 不选 / 选时子树的最大价值：若 $u$ 不选，儿子可任选（取 $\max$）；若 $u$ 选，儿子都不能选。先 DFS 自底向上合并子树的答案。本题为“没有上司的舞会”：上司选了下属不能选。复杂度 $O(n)$。

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
