---
title: "D18 Tarjan eDCC缩点"
categories:
- [算法, D 图论]
tags:
- 图论
---

### 题目情境

P8436 【模板】边双连通分量

**题目描述**

对于一个 $n$ 个节点 $m$ 条无向边的图，请输出其边双连通分量的个数，并且输出每个边双连通分量。

**输入格式**

第一行，两个整数 $n$ 和 $m$。

接下来 $m$ 行，每行两个整数 $u, v$，表示一条无向边。

**不保证图为简单图，图中可能有重边和自环。**

**输出格式**

第一行一个整数 $x$ 表示边双连通分量的个数。

接下来的 $x$ 行，每行第一个数 $a$ 表示该分量结点个数，然后 $a$ 个数，描述一个边双连通分量。

你可以以任意顺序输出边双连通分量与边双连通分量内的结点。

输入 #1

```
7 8
1 3
2 4
3 5
2 5
6 4
2 5
6 3
2 7
```

输出 #1

```
3
1 1
5 2 5 3 6 4
1 7
```

**样例1解释：**

![](https://cdn.luogu.com.cn/upload/image_hosting/0bzdfzeq.png)

相同颜色的点为同一个连通分量。

**数据范围：**
对于 $100\%$ 的数据，$1 \le n \le 5 \times10 ^5$，$1 \le m \le 2 \times 10^6$。

### C++代码实现

```c++
#include<bits/stdc++.h>
using namespace std;

const int N=500010,M=4000010;
int n,m,a,b;
int h[N],to[M],ne[M],idx=1;
void add(int a,int b){
  to[++idx]=b,ne[idx]=h[a],h[a]=idx;
}
int dfn[N],low[N],tim,stk[N],top,dcc[N],siz[N],cnt,bri[M];
vector<int> d[N];

void tarjan(int x,int ine){
  dfn[x]=low[x]=++tim;stk[++top]=x;
  for(int i=h[x];i;i=ne[i]){
    int y=to[i];
    if(!dfn[y]){
      tarjan(y,i);
      low[x]=min(low[x],low[y]);
      if(low[y]<dfn[x]) bri[i]=bri[i^1]=1;
    }
    else if(i!=(ine^1)) low[x]=min(low[x],dfn[y]);
  }
  
  if(dfn[x]==low[x]){
    ++cnt;
    while(1){
      int y=stk[top--];
      // dcc[y]=cnt;
      siz[cnt]++;
      d[cnt].push_back(y);
      if(x==y) break;
    }
  }
}
int main(){
  ios::sync_with_stdio(0),cin.tie(0),cout.tie(0);
  cin>>n>>m;
  while(m--){
    cin>>a>>b;add(a,b);add(b,a);
  }
  for(int i=1;i<=n;i++)if(!dfn[i])tarjan(i,0);
  cout<<cnt<<"\n";
  for(int i=1;i<=cnt;i++){
    cout<<siz[i]<<" ";
    for(int j:d[i]) cout<<j<<" ";
    cout<<"\n";
  }
}
```
