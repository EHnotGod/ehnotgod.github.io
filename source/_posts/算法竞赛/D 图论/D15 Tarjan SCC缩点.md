---
title: "D15 Tarjan SCC缩点"
categories:
- [算法, D 图论]
tags:
- 图论
---

### 题目情境

P3387 【模板】缩点

**题目描述**

给定一个 $n$ 个点 $m$ 条边有向图，每个点有一个权值，求一条路径，使路径经过的点权值之和最大。你只需要求出这个权值和。

允许多次经过一条边或者一个点，但是，重复经过的点，权值只计算一次。

**输入格式**

第一行两个正整数 $n,m$。

第二行 $n$ 个整数，其中第 $i$ 个数 $a_i$ 表示点 $i$ 的点权。

第三至 $m+2$ 行，每行两个整数 $u,v$，表示一条 $u\rightarrow v$ 的有向边。

**输出格式**

共一行，最大的点权之和。

输入 #1

```
2 2
1 1
1 2
2 1
```

输出 #1

```
2
```

对于 $100\%$ 的数据，$1\le n \le 10^4$，$1\le m \le 10^5$，$0\le a_i\le 10^3$。

![image-20250817142544858](/images/D/D15-1.png)

### C++代码实现

```c++
#include<bits/stdc++.h>
using namespace std;

const int N=100010;
int n,m,a,b;
vector<int> e[N],ne[N]; 
int dfn[N],low[N],tim,stk[N],top,scc[N],cnt;
int w[N],nw[N],d[N];

void tarjan(int x){
  dfn[x]=low[x]=++tim; 
  stk[++top]=x;
  for(int y : e[x]){
    if(!dfn[y]){
      tarjan(y);
      low[x]=min(low[x],low[y]); 
    }
    else if(!scc[y])
      low[x]=min(low[x],dfn[y]);
  }
  if(dfn[x]==low[x]){
    ++cnt;
    while(1){
      int y=stk[top--];
      scc[y]=cnt;
      if(y==x) break;
    }
  }
}
int main(){
  cin>>n>>m;
  for(int i=1;i<=n;i++) cin>>w[i];
  for(int i=1;i<=m;i++){
    cin>>a>>b;
    e[a].push_back(b);
  }
  
  for(int i=1;i<=n;i++) //缩点
    if(!dfn[i]) tarjan(i); 
  for(int x=1;x<=n;x++){ //建拓扑图
    nw[scc[x]]+=w[x];
    for(int y:e[x])
      if(scc[x]!=scc[y]) ne[scc[x]].push_back(scc[y]);
  } 
  for(int x=cnt;x;x--){ //求最长路
    if(d[x]==0) d[x]=nw[x]; //起点
    for(int y:ne[x])
      d[y]=max(d[y],d[x]+nw[y]);
  } 
  int ans=0;
  for(int i=1;i<=cnt;i++) ans=max(ans,d[i]);
  cout<<ans;
}
```
