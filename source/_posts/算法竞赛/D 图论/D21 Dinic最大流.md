---
title: "D21 Dinic最大流"
categories:
- [算法, D 图论]
tags:
- 图论
---

### 题目情境

**题目描述**

如题，给出一个网络图，以及其源点和汇点，求出其网络最大流。

**输入格式**

第一行包含四个正整数 $n,m,s,t$，分别表示点的个数、有向边的个数、源点序号、汇点序号。

接下来 $m$ 行每行包含三个正整数 $u_i,v_i,w_i$，表示第 $i$ 条有向边从 $u_i$ 出发，到达 $v_i$，边权为 $w_i$（即该边最大流量为 $w_i$）。

**输出格式**

一行，包含一个正整数，即为该网络的最大流。

输入 #1

```
4 5 4 3
4 2 30
4 3 20
2 3 20
2 1 30
1 3 30
```

输出 #1

```
50
```

- 对于 $100\%$ 的数据，保证 $1 \leq n\leq200$，$1 \leq m\leq 5000$，$0 \leq w\lt 2^{31}$。

理论复杂度：$O(n^2m)$，实际挺快的

二分图上的Dinic更快。

### C++代码实现

```c++
// Luogu P3376 【模板】网络最大流
#include <iostream>
#include <cstring>
#include <algorithm>
#include <queue>
#define LL long long
#define N 10010
#define M 200010
using namespace std;

int n,m,S,T;
struct edge{LL v,c,ne;}e[M];
int h[N],idx=1; //从2,3开始配对
int d[N],cur[N];

void add(int a,int b,int c){
  e[++idx]={b,c,h[a]};
  h[a]=idx;
}
bool bfs(){ //对点分层，找增广路
  memset(d,0,sizeof d);
  queue<int>q; 
  q.push(S); d[S]=1;
  while(q.size()){
    int u=q.front(); q.pop();
    for(int i=h[u];i;i=e[i].ne){
      int v=e[i].v;
      if(d[v]==0 && e[i].c){
        d[v]=d[u]+1;
        q.push(v);
        if(v==T)return true;
      }
    }
  }
  return false;
}
LL dfs(int u, LL mf){ //多路增广
  if(u==T) return mf;
  LL sum=0;
  for(int i=cur[u];i;i=e[i].ne){
    cur[u]=i; //当前弧优化
    int v=e[i].v;
    if(d[v]==d[u]+1 && e[i].c){
      LL f=dfs(v,min(mf,e[i].c));
      e[i].c-=f; 
      e[i^1].c+=f; //更新残留网
      sum+=f; //累加u的流出流量
      mf-=f;  //减少u的剩余流量
      if(mf==0)break;//余量优化
    }
  }
  if(sum==0) d[u]=0; //残枝优化
  return sum;
}
LL dinic(){ //累加可行流
  LL flow=0;
  while(bfs()){
    memcpy(cur, h, sizeof h);
    flow+=dfs(S,1e9);
  }
  return flow;
}
int main(){
  int a,b,c;
  scanf("%d%d%d%d",&n,&m,&S,&T);
  while(m -- ){
    scanf("%d%d%d",&a,&b,&c);
    add(a,b,c); add(b,a,0);
  }
  printf("%lld\n",dinic());
  return 0;
}
```
