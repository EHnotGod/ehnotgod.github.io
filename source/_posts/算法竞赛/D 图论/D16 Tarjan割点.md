---
title: "D16 Tarjan割点"
categories:
- [算法, D 图论]
tags:
- 图论
---

### 题目情境

P3388 【模板】割点（割顶）

**题目描述**

给出一个 $n$ 个点，$m$ 条边的无向图，求图的割点。

**输入格式**

第一行输入两个正整数 $n,m$。

下面 $m$ 行每行输入两个正整数 $x,y$ 表示 $x$ 到 $y$ 有一条边。

**输出格式**

第一行输出割点个数。

第二行按照节点编号从小到大输出节点，用空格隔开。

输入 #1

```
6 7
1 2
1 3
1 4
2 5
3 5
4 5
5 6
```

输出 #1

```
1 
5
```

对于全部数据，$1\leq n \le 2\times 10^4$，$1\leq m \le 1 \times 10^5$。

点的编号均大于 $0$ 小于等于 $n$。

**Tarjan 图不一定连通。**

### C++代码实现

```c++
#include<bits/stdc++.h>
using namespace std;

const int N=20010;
int n,m,a,b;
vector<int> e[N];
int dfn[N],low[N],tim,cut[N],root;

void tarjan(int x){
  dfn[x]=low[x]=++tim;
  int son=0; //x的儿子个数
  for(int y:e[x]){
    if(!dfn[y]){ //若y未访问
      tarjan(y);
      low[x]=min(low[x],low[y]); 
      if(low[y]>=dfn[x]){
        son++;
        if(x!=root||son>1) cut[x]=1;
      }
    }
    else //若y已访问
      low[x]=min(low[x],dfn[y]); //注:dfn不能换成low
  }
}
int main(){
  cin>>n>>m;
  while(m --){
    cin>>a>>b;
    e[a].push_back(b),
    e[b].push_back(a);
  }
  for(root=1;root<=n;root++) if(!dfn[root]) tarjan(root);
  
  int ans=0;
  for(int i=1;i<=n;i++) if(cut[i]) ans++;
  cout<<ans<<"\n";
  for(int i=1;i<=n;i++) if(cut[i]) cout<<i<<" ";
}
```
