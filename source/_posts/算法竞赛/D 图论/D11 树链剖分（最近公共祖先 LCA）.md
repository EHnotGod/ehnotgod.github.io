---
title: "D11 树链剖分（最近公共祖先 LCA）"
categories:
- [算法, D 图论]
tags:
- 图论
---

### 题目情境

**题目描述**

如题，给定一棵有根多叉树，请求出指定两个点直接最近的公共祖先。

**输入格式**

第一行包含三个正整数 $N,M,S$，分别表示树的结点个数、询问的个数和树根结点的序号。

接下来 $N-1$ 行每行包含两个正整数 $x, y$，表示 $x$ 结点和 $y$ 结点之间有一条直接连接的边（数据保证可以构成树）。

接下来 $M$ 行每行包含两个正整数 $a, b$，表示询问 $a$ 结点和 $b$ 结点的最近公共祖先。

**输出格式**

输出包含 $M$ 行，每行包含一个正整数，依次为每一个询问的结果。

**输入输出样例 #1**

输入 #1

```
5 5 4
3 1
2 4
5 1
1 4
2 4
3 2
3 5
1 2
4 5
```

输出 #1

```
4
4
1
4
4
```

对于 $100\%$ 的数据，$1 \leq N,M\leq 500000$，$1 \leq x, y,a ,b \leq N$，**不保证** $a \neq b$。


样例说明：

该树结构如下：

 ![](https://cdn.luogu.com.cn/upload/pic/2282.png) 

第一次询问：$2, 4$ 的最近公共祖先，故为 $4$。

第二次询问：$3, 2$ 的最近公共祖先，故为 $4$。

第三次询问：$3, 5$ 的最近公共祖先，故为 $1$。

第四次询问：$1, 2$ 的最近公共祖先，故为 $4$。

第五次询问：$4, 5$ 的最近公共祖先，故为 $4$。

故输出依次为 $4, 4, 1, 4, 4$。

**解析：**

![image-20250418092432087](/images/算法竞赛/D/D11-2.png)

### Python代码实现

```python
import sys
sys.setrecursionlimit(int(1e7))
N = 500010
fa = [0] * N
son = [0] * N
dep = [0] * N
siz = [0] * N
top = [0] * N
e = [[] for i in range(N)]
def dfs1(u, f):
    fa[u] = f
    siz[u] = 1
    dep[u] = dep[f] + 1
    for v in e[u]:
        if v == f:
            continue
        dfs1(v, u)
        siz[u] += siz[v]
        if siz[son[u]] < siz[v]:
            son[u] = v
def dfs2(u, t):
    top[u] = t
    if not son[u]:
        return
    dfs2(son[u], t)
    for v in e[u]:
        if v == fa[u] or v == son[u]:
            continue
        dfs2(v, v)
def lca(u, v):
    while top[u] != top[v]:
        if dep[top[u]] < dep[top[v]]:
            u, v = v, u
        u = fa[top[u]]
    if dep[u] < dep[v]:
        return u
    else:
        return v
n, m, s = map(int, input().split())
for i in range(1, n):
    a, b = map(int, input().split())
    e[a].append(b)
    e[b].append(a)
dfs1(s, 0)
dfs2(s, s)
for i in range(m):
    a, b = map(int, input().split())
    print(lca(a, b))
```

### C++代码实现

```c++
// 树链剖分 O(mlogn)
#include <iostream>
#include <cstring>
#include <algorithm>
#include <vector>
using namespace std;

const int N=500010;
int n,m,s,a,b;
vector<int> e[N];
int fa[N],son[N],dep[N],siz[N],top[N];

void dfs1(int u,int f){ //搞fa,son,dep
  fa[u]=f;siz[u]=1;dep[u]=dep[f]+1;
  for(int v:e[u]){
    if(v==f) continue;
    dfs1(v,u);
    siz[u]+=siz[v];
    if(siz[son[u]]<siz[v])son[u]=v;
  }
}
void dfs2(int u,int t){ //搞top
  top[u]=t;  //记录链头
  if(!son[u]) return; //无重儿子
  dfs2(son[u],t);     //搜重儿子
  for(int v:e[u]){
    if(v==fa[u]||v==son[u])continue;
    dfs2(v,v); //搜轻儿子
  }
}
int lca(int u,int v){
  while(top[u]!=top[v]){
    if(dep[top[u]]<dep[top[v]])swap(u,v);
    u=fa[top[u]];
  }
  return dep[u]<dep[v]?u:v;
}
int main(){
  scanf("%d%d%d",&n,&m,&s);
  for(int i=1; i<n; i++){
    scanf("%d%d",&a,&b);
    e[a].push_back(b);
    e[b].push_back(a);
  }
  dfs1(s,0);
  dfs2(s,s);
  while(m--){
    scanf("%d%d",&a,&b);
    printf("%d\n",lca(a,b));
  }
  return 0;
}
```
