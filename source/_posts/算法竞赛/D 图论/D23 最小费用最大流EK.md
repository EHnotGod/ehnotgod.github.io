---
title: "D23 最小费用最大流EK"
categories:
- [算法, D 图论]
tags:
- 图论
---

### 题目情境

**题目描述**

给出一个包含 $n$ 个点和 $m$ 条边的有向图（下面称其为网络） $G=(V,E)$，该网络上所有点分别编号为 $1 \sim n$，所有边分别编号为 $1\sim m$，其中该网络的源点为 $s$，汇点为 $t$，网络上的每条边 $(u,v)$ 都有一个流量限制 $w(u,v)$ 和单位流量的费用 $c(u,v)$。

你需要给每条边 $(u,v)$ 确定一个流量 $f(u,v)$，要求：

1.  $0 \leq f(u,v) \leq w(u,v)$（每条边的流量不超过其流量限制）；
2.  $\forall p \in \{V \setminus \{s,t\}\}$，$\sum_{(i,p) \in E}f(i,p)=\sum_{(p,i)\in E}f(p,i)$（除了源点和汇点外，其他各点流入的流量和流出的流量相等）；
3.  $\sum_{(s,i)\in E}f(s,i)=\sum_{(i,t)\in E}f(i,t)$（源点流出的流量等于汇点流入的流量）。

定义网络 $G$ 的流量 $F(G)=\sum_{(s,i)\in E}f(s,i)$，网络 $G$ 的费用 $C(G)=\sum_{(i,j)\in E} f(i,j) \times c(i,j)$。

你需要求出该网络的**最小费用最大流**，即在 $F(G)$ 最大的前提下，使 $C(G)$ 最小。

**输入格式**

输入第一行包含四个整数 $n,m,s,t$，分别代表该网络的点数 $n$，网络的边数 $m$，源点编号 $s$，汇点编号 $t$。

接下来 $m$ 行，每行四个整数 $u_i,v_i,w_i,c_i$，分别代表第 $i$ 条边的起点，终点，流量限制，单位流量费用。

**输出格式**

输出两个整数，分别为该网络的最大流 $F(G)$，以及在 $F(G)$ 最大的前提下，该网络的最小费用 $C(G)$。

输入 #1

```
4 5 4 3
4 2 30 2
4 3 20 3
2 3 20 1
2 1 30 9
1 3 40 5
```

输出 #1

```
50 280
```

对于 $100\%$ 的数据，$1 \leq n \leq 5\times 10^3$，$1 \leq m \leq 5 \times 10^4$，$1 \leq s,t \leq n$，$u_i \neq v_i$，$0 \leq w_i,c_i \leq 10^3$，且该网络的最大流和最小费用 $\leq 2^{31}-1$。

![image-20251101160808199](/images/D/D23-1.png)

### C++代码实现

```c++
// Luogu P3381 【模板】最小费用最大流
#include <iostream>
#include <cstring>
#include <algorithm>
#include <queue>
using namespace std;

const int N=5010,M=100010,INF=1e8;
int n,m,S,T;
struct edge{int v,c,w,ne;}e[M];
int h[N],idx=1;//从2,3开始配对
int d[N],mf[N],pre[N],vis[N];
int flow,cost;

void add(int a,int b,int c,int d){
  e[++idx]={b,c,d,h[a]};
  h[a]=idx;
}
bool spfa(){
  memset(d,0x3f,sizeof d);
  memset(mf,0,sizeof mf);
  queue<int> q; q.push(S);
  d[S]=0, mf[S]=INF, vis[S]=1;
  while(q.size()){
    int u=q.front(); q.pop();
    vis[u]=0;
    for(int i=h[u];i;i=e[i].ne){
      int v=e[i].v,c=e[i].c,w=e[i].w;
      if(d[v]>d[u]+w && c){
        d[v]=d[u]+w; //最短路
        pre[v]=i;
        mf[v]=min(mf[u],c);
        if(!vis[v]){
          q.push(v); vis[v]=1;
        }
      }
    }
  }
  return mf[T]>0;
}
void EK(){
  while(spfa()){
    for(int v=T;v!=S;){
      int i=pre[v];
      e[i].c-=mf[T];
      e[i^1].c+=mf[T];
      v=e[i^1].v;
    }
    flow+=mf[T]; //累加可行流
    cost+=mf[T]*d[T];//累加费用   
  }
}
int main(){
  scanf("%d%d%d%d",&n,&m,&S,&T);
  int a,b,c,d;
  while(m --){
    scanf("%d%d%d%d",&a,&b,&c,&d);
    add(a,b,c,d);
    add(b,a,0,-d);
  }
  EK();
  printf("%d %d\n",flow,cost);
  return 0;
}
```
