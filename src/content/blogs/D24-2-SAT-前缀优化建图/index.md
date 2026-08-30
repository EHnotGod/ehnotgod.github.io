---
title: "D24 2-SAT-前缀优化建图"
publishDate: 2026-08-08
description: "2-SAT 前缀优化建图：每部分恰选一个 + 边至少一端选。"
category: algo
tags:
  - 图论
language: zh
---

### 题目情境

题目链接：https://www.luogu.com.cn/problem/P6378

**题目描述**

$n$ 个点 $m$ 条边的无向图被分成 $k$ 个部分。每个部分包含一些点。

请选择一些关键点，使得每个部分**恰**有一个关键点，且每条边**至少**有一个端点是关键点。

**输入格式**

第一行三个整数 $n,m,k$。

接下来 $m$ 行，每行两个整数 $a,b$，表示有一条 $a,b$ 间的边。

接下来 $k$ 行，每行第一个整数为 $w$，表示这个部分有 $w$ 个点；接下来 $w$ 个整数，为在这个部分中的点的编号。

**输出格式**

若可能选出请输出 `TAK`，否则输出 `NIE`。

输入 #1

```
6 5 2
1 2
3 1
1 4
5 2
6 2
3 3 4 2
3 1 6 5
```

输出 #1

```
TAK
```

**说明/提示**

#### 数据规模与约定

对于全部的测试点，保证 $1\le k,w\le n\le 10^6$，$\sum w=n$，$1\le a,b\le n$，$0\le m\le 10^6$。

### 算法解析：

![2-SAT 前缀优化建图示意](/images/算法竞赛/D/D24-1.png)

2-SAT 建模：每个点选/不选拆成两个点。对边 $(a,b)$，要求至少一端选，得到两条蕴含边：不选 $a$ 则选 $b$、不选 $b$ 则选 $a$。

难点在「每个部分恰选一个」。若两两连边是 $O(w^2)$，需用**前缀优化**：对某部分的点 $p_1,\dots,p_w$ 引入前缀节点 $pre[i]$（表示前 $i$ 个点至少选一个），连边：
- $p_i$ 选 $\rightarrow pre[i]$ 选
- $pre[i-1]$ 选 $\rightarrow pre[i]$ 选（前缀传递）
- $p_i$ 选 $\rightarrow pre[i-1]$ 不选（选 $p_i$ 则前 $i-1$ 个都不能选，保证恰一个）

总点数 $4n$（选/不选/前缀选/前缀不选），边数 $O(n+m)$。建图后 Tarjan 判 SCC：若某个点选与不选在同一 SCC 则输出 `NIE`，否则 `TAK`。数据较大（$n\le 10^6$），Python 版仅用于理解，竞赛建议用 C++。

### Python代码实现

```python
import sys
sys.setrecursionlimit(10**7)
input = sys.stdin.readline

n, m, k = map(int, input().split())
N = 4 * n + 1
g = [[] for _ in range(N)]

def x0(x): return x            # 选
def x1(x): return x + n        # 不选
def p0(x): return x + 2 * n    # 前缀选
def p1(x): return x + 3 * n    # 前缀不选

def add(a, b):
    g[a].append(b)

for _ in range(m):
    x, y = map(int, input().split())
    add(x1(x), x0(y))  # 不选x 则选y
    add(x1(y), x0(x))  # 不选y 则选x

for _ in range(k):
    wl = list(map(int, input().split()))
    w = wl[0]
    p = None
    for j, x in enumerate(wl[1:], 1):
        add(x0(x), p0(x))
        add(p1(x), x1(x))
        if j != 1:
            add(p0(p), p0(x))
            add(p1(x), p1(p))
            add(p0(p), x1(x))
            add(x0(x), p1(p))
        p = x

# Tarjan 求 SCC
dfn = [0] * N; low = [0] * N; scc = [0] * N
stk = []; inst = [False] * N
tim = 0; cnt = 0

def dfs(u):
    global tim, cnt
    tim += 1
    dfn[u] = low[u] = tim
    stk.append(u); inst[u] = True
    for v in g[u]:
        if not dfn[v]:
            dfs(v)
            low[u] = min(low[u], low[v])
        elif inst[v]:
            low[u] = min(low[u], dfn[v])
    if low[u] == dfn[u]:
        cnt += 1
        while True:
            y = stk.pop(); inst[y] = False
            scc[y] = cnt
            if y == u:
                break

for i in range(1, N):
    if not dfn[i]:
        dfs(i)

for i in range(1, n + 1):
    if scc[x0(i)] == scc[x1(i)]:
        print("NIE")
        sys.exit()
print("TAK")
```

### C++代码实现

```c++
#include<bits/stdc++.h>
using namespace std;

#define x0(x) x     //点
#define x1(x) x+n   //反点
#define p0(x) x+2*n //前缀点
#define p1(x) x+3*n //前缀反点
#define N 8000010
int n,m,k,w;
int dfn[N],low[N],scc[N],stk[N],tim,top,cnt;
int head[N],to[N],ne[N],idx;

void add(int a,int b){
  to[++idx]=b;
  ne[idx]=head[a];
  head[a]=idx;
}
void tarjan(int x){
  dfn[x]=low[x]=++tim;
  stk[++top]=x;
  for(int i=head[x];i;i=ne[i]){
    int y=to[i];
    if(!dfn[y]){ //若y尚未访问
      tarjan(y);
      low[x]=min(low[x],low[y]);
    }
    else if(!scc[y]) //若y已访问且未处理
      low[x]=min(low[x],dfn[y]);
  }
  
  if(low[x]==dfn[x]){ //若x是SCC的根
    ++cnt;
    for(int y=-1;y!=x;)
      scc[y=stk[top--]]=cnt;
  }
}
int main(){
  scanf("%d%d%d",&n,&m,&k);
  for(int i=1,x,y;i<=m;++i){
    scanf("%d%d",&x,&y);
    add(x1(x),x0(y)); //不选x 则选y
    add(x1(y),x0(x)); //不选y 则选x
  }
  for(int i=1;i<=k;++i){ //前缀优化
    scanf("%d",&w);
    for(int j=1,x,p;j<=w;++j){
      scanf("%d",&x);
      add(x0(x),p0(x)); //向下连
      add(p1(x),x1(x)); //向下连
      if(j!=1){
        add(p0(p),p0(x)); //向右连
        add(p1(x),p1(p)); //向左连
        add(p0(p),x1(x)); //向右下连
        add(x0(x),p1(p)); //向左下连
      }
      p=x; //记录前一个x
    }
  }
  for(int i=1;i<=4*n;++i)if(!dfn[i])tarjan(i);
  for(int i=1;i<=n;++i)
    if(scc[i]==scc[i+n]) return puts("NIE"),0;
  puts("TAK");
}
```