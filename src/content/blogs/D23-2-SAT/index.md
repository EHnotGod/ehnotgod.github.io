---
title: "D23 2-SAT"
publishDate: 2026-08-08
description: "2-SAT：变量拆点 + Tarjan 强连通判定与构造。"
category: algo
tags:
  - 图论
language: zh
---

### 题目情境

题目链接：https://www.luogu.com.cn/problem/P4782

**题目描述**

有 $n$ 个布尔变量 $x_1\sim x_n$，另有 $m$ 个需要满足的条件，每个条件的形式都是 「$x_i$ 为 `true` / `false` 或 $x_j$ 为 `true` / `false`」。比如 「$x_1$ 为真或 $x_3$ 为假」、「$x_7$ 为假或 $x_2$ 为假」。

2-SAT 问题的目标是给每个变量赋值使得所有条件得到满足。

**输入格式**

第一行两个整数 $n$ 和 $m$，意义如题面所述。

接下来 $m$ 行每行 $4$ 个整数 $i$, $a$, $j$, $b$，表示 「$x_i$ 为 $a$ 或 $x_j$ 为 $b$」($a, b\in \{0,1\}$)

**输出格式**

如无解，输出 `IMPOSSIBLE`；

否则输出 `POSSIBLE`，下一行 $n$ 个整数 $x_1\sim x_n$（$x_i\in\{0,1\}$），表示构造出的解。

输入 #1

```
3 1
1 1 3 0
```

输出 #1

```
POSSIBLE
0 0 0
```

**说明/提示**

$1\leq n, m\leq 10^6$ , 前 $3$ 个点卡小错误，后面 $5$ 个点卡效率。

由于数据随机生成，可能会含有 10 0 10 0 之类的坑，但按照最常规写法的写的标程没有出错，各个数据点卡什么的提示在标程里。

### 算法解析：

2-SAT 把每个变量 $x_i$ 拆成两个点：$i$ 表示 $x_i$ 为真、$i+n$ 表示 $x_i$ 为假。条件「$x_i$ 为 $a$ 或 $x_j$ 为 $b$」等价于两条蕴含边：
- $\neg x_i^a \rightarrow x_j^b$（若 $x_i$ 不满足 $a$，则 $x_j$ 必须满足 $b$）
- $\neg x_j^b \rightarrow x_i^a$（对称）

建图后用 Tarjan 求强连通分量。若某个变量 $x_i$ 的两种取值（$i$ 与 $i+n$）在同一个 SCC 中，则矛盾无解，输出 `IMPOSSIBLE`；否则有解：对每个变量取 $scc$ 编号较大的那个取值（Tarjan 求出的 $scc$ 编号是拓扑序的逆序，取大者即取拓扑序靠后的可行值）。复杂度 $O(n+m)$。

### Python代码实现

```python
import sys
sys.setrecursionlimit(10**6)
input = sys.stdin.readline

def tarjan(sz, edges):
    g = [[] for _ in range(sz)]
    for u, v in edges:
        g[u].append(v)
    dfn = [0] * sz; low = [0] * sz; scc = [0] * sz
    stk = []; in_stk = [False] * sz
    time = 0; cnt = 0
    def dfs(u):
        nonlocal time, cnt
        time += 1
        dfn[u] = low[u] = time
        stk.append(u); in_stk[u] = True
        for v in g[u]:
            if not dfn[v]:
                dfs(v)
                low[u] = min(low[u], low[v])
            elif in_stk[v]:
                low[u] = min(low[u], dfn[v])
        if low[u] == dfn[u]:
            cnt += 1
            while True:
                x = stk.pop(); in_stk[x] = False
                scc[x] = cnt
                if x == u: break
    for i in range(sz):
        if not dfn[i]:
            dfs(i)
    return scc

n, m = map(int, input().split())
edges = []
for _ in range(m):
    i, a, j, b = map(int, input().split())
    xi = i if a == 1 else i + n      # xi 为 a 的结点
    xj = j if b == 1 else j + n      # xj 为 b 的结点
    xi_neg = i + n if a == 1 else i  # xi 不满足 a
    xj_neg = j + n if b == 1 else j  # xj 不满足 b
    edges.append((xi_neg, xj))  # ¬xi_a -> xj_b
    edges.append((xj_neg, xi))  # ¬xj_b -> xi_a

scc = tarjan(2 * n + 1, edges)
ans = []
for i in range(1, n + 1):
    if scc[i] == scc[i + n]:
        print("IMPOSSIBLE")
        sys.exit()
    ans.append('1' if scc[i] > scc[i + n] else '0')
print("POSSIBLE")
print(' '.join(ans))
```

### C++代码实现

```c++
// 2-SAT+tarjan O(n+m)
#include<bits/stdc++.h>
using namespace std;

const int N=2000005;
int n,m;
int hd[N],to[N],ne[N],idx;
int dfn[N],low[N],tim,stk[N],top,scc[N],cnt;

void add(int a,int b){
  to[++idx]=b,ne[idx]=hd[a],hd[a]=idx;
}
void tarjan(int x){
  dfn[x]=low[x]=++tim;
  stk[++top]=x;
  for(int i=hd[x];i;i=ne[i]){
    int y=to[i];
    if(!dfn[y]){
      tarjan(y);
      low[x]=min(low[x],low[y]);
    }
    else if(!scc[y]) low[x]=min(low[x],dfn[y]);
  }
  if(low[x]==dfn[x]){
    ++cnt;
    for(int y=-1;y!=x;) scc[y=stk[top--]]=cnt;
  }
}
int main(){
  scanf("%d%d",&n,&m);
  for(int i,a,j,b;m--;){
    scanf("%d%d%d%d",&i,&a,&j,&b);
    add(i+!a*n,j+b*n); //xi拆成i和i+n
    add(j+!b*n,i+a*n);
  }
  for(int i=1;i<=2*n;i++)if(!dfn[i]) tarjan(i);
  for(int i=1;i<=n;i++)if(scc[i]==scc[i+n]){
    puts("IMPOSSIBLE");
    return 0;
  }
  puts("POSSIBLE");
  for(int i=1;i<=n;i++)printf("%d ",scc[i]>scc[i+n]);
  return 0;
}
```