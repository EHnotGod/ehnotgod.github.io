---
title: "D9 倍增算法（LCA）"
categories:
- [算法, D 图论]
tags:
- 图论
---

### 题目情境

题面同D11

![image-20250727163659755](/images/D/D9-1.png)

![image-20250727163753894](/images/D/D9-2.png)

### Python代码实现

```python
import sys

sys.setrecursionlimit(10 ** 7)
input = sys.stdin.readline

# 最大节点数和最大二进制位数（因为 2^20 > 10^6，足够应对 N ≤ 5e5）
N = 500_005
LOG = 20

# 邻接表存储树的边
edges = [[] for _ in range(N)]

# f[u][i] 表示节点 u 的第 2^i 级祖先
# dep[u] 存储节点 u 的深度（根节点深度为 1）
f = [[0] * (LOG + 1) for _ in range(N)]
dep = [0] * N


def dfs(u: int, parent: int) -> None:
    """
    从 u 开始对整棵树做一次深度优先遍历，顺便预处理二倍祖先 f[u][i] 和深度 dep[u]。

    参数:
      u      - 当前节点
      parent - u 的父节点（0 表示虚拟根）
    """
    # 初始化 u 的 2^0 祖先（也就是父节点）和深度
    f[u][0] = parent
    dep[u] = dep[parent] + 1

    # 依次计算 f[u][1..LOG]，即 2^1、2^2、…、2^LOG 级祖先
    for i in range(1, LOG + 1):
        # f[u][i] = f[ f[u][i-1] ][i-1]
        f[u][i] = f[f[u][i - 1]][i - 1]

    # 遍历所有相邻的孩子 v，继续 dfs
    for v in edges[u]:
        if v == parent:
            continue
        dfs(v, u)


def lca(u: int, v: int) -> int:
    """
    计算节点 u 和 v 的最近公共祖先（Lowest Common Ancestor）。

    思路：
      1. 如果 u、v 深度不一致，先把深度较深的节点提升到与另一节点同层。
      2. 如果此时 u == v，则直接返回。
      3. 否则，从最高位开始尝试让 u、v 同时往上跳，直到它们的父节点相同为止。
      4. 最后返回它们共同的父节点。
    """
    # 保证 dep[u] ≥ dep[v]
    if dep[u] < dep[v]:
        u, v = v, u

    # 先把 u 提升到与 v 相同的深度
    diff = dep[u] - dep[v]
    for i in range(LOG + 1):
        if diff & (1 << i):
            u = f[u][i]

    # 如果相等，则这个节点就是 LCA
    if u == v:
        return u

    # 从最高位开始，若 u、v 的 2^i 祖先不同，则同时跳上去
    for i in reversed(range(LOG + 1)):
        if f[u][i] != f[v][i]:
            u = f[u][i]
            v = f[v][i]

    # 此时 u、v 的父节点就是 LCA
    return f[u][0]


# ------------------------------
# 读取输入、构建树并回答查询
# ------------------------------

# n: 节点数； m: 查询次数； s: 以 s 为根的 LCA 树
n, m, s = map(int, input().split())

# 读取 n-1 条边，建立无向树
for _ in range(n - 1):
    a, b = map(int, input().split())
    edges[a].append(b)
    edges[b].append(a)

# 从根 s 开始 dfs 预处理
dfs(s, 0)

# 处理 m 次 LCA 查询
for _ in range(m):
    u, v = map(int, input().split())
    print(lca(u, v))
```

### C++代码实现

```c++
// 倍增法 O(nlogn)
#include<bits/stdc++.h>
using namespace std;

const int N=500005;
int n,m,s;
vector<int> e[N];
int f[N][22],dep[N];

void dfs(int u,int fa){
  f[u][0]=fa; dep[u]=dep[fa]+1;
  for(int i=1;i<=20;i++) //u的2,4,8...祖先
    f[u][i]=f[f[u][i-1]][i-1];
  for(int v:e[u])
    if(v!=fa) dfs(v,u);
}
int lca(int u,int v){
  if(dep[u]<dep[v]) swap(u,v);
  for(int i=20;~i;i--) //u先大步后小步向上跳，直到与v同层
    if(dep[f[u][i]]>=dep[v]) u=f[u][i];
  if(u==v) return v;
  for(int i=20;~i;i--) //u,v一起向上跳，直到lca的下面
    if(f[u][i]!=f[v][i]) u=f[u][i],v=f[v][i];
  return f[u][0];
}
int main(){
  scanf("%d%d%d",&n,&m,&s);
  for(int i=1,a,b; i<n; i++){
    scanf("%d%d",&a,&b);
    e[a].push_back(b);
    e[b].push_back(a);
  }
  dfs(s,0);
  for(int i=0,a,b;i<m;i++){
    scanf("%d%d",&a,&b);
    printf("%d\n",lca(a,b));
  }
}
```
