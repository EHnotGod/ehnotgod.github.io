---
title: "D19 Tarjan vDCC缩点"
categories:
- [算法, D 图论]
tags:
- 图论
---

### 题目情境

P8435 【模板】点双连通分量

**题目描述**

对于一个 $n$ 个节点 $m$ 条无向边的图，请输出其点双连通分量的个数，并且输出每个点双连通分量。

**输入格式**

第一行，两个整数 $n$ 和 $m$。

接下来 $m$ 行，每行两个整数 $u, v$，表示一条无向边。

**输出格式**

第一行一个整数 $x$ 表示点双连通分量的个数。

接下来的 $x$ 行，每行第一个数 $a$ 表示该分量结点个数，然后 $a$ 个数，描述一个点双连通分量。

你可以以任意顺序输出点双连通分量与点双连通分量内的结点。

输入 #4

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

输出 #4

```
3
2 7 2
5 5 2 4 6 3
2 3 1
```

输入 #5

```
1 1
1 1
```

输出 #5

```
1
1 1
```

说明/提示

**样例四解释：**

![](https://cdn.luogu.com.cn/upload/image_hosting/huvwgbuo.png)

相同颜色的点为同一个分量里的结点。

**温馨提示：请认真考虑孤立点与自环（样例五）的情况。**

------------

**数据范围：**
对于 $100\%$ 的数据，$1 \le n \le 5 \times10 ^5$，$1 \le m \le 2 \times 10^6$。

### C++代码实现

```c++
#include<bits/stdc++.h>
using namespace std;

const int N=500010;
int n,m,a,b;
vector<int> e[N],ne[N],dcc[N];
int dfn[N],low[N],tot,stk[N],top,cut[N],root,cnt;

void tarjan(int x){
  if(x==root&&!e[x].size()){ //孤立点
        dcc[++cnt].push_back(x);
        return;
    }  
  dfn[x]=low[x]=++tot; stk[++top]=x;
  int son=0;
  for(int y:e[x]){
    if(!dfn[y]){ //若y未访问
      tarjan(y);
      low[x]=min(low[x],low[y]); 
      if(low[y]>=dfn[x]){
        son++;
        if(x!=root||son>1)cut[x]=1; //割点
        
        ++cnt;
        while(1){
          int z=stk[top--];
          dcc[cnt].push_back(z);
          if(z==y) break; //让x留在栈中
        }
        dcc[cnt].push_back(x); //vDCC
      }
    }
    else //若y已访问
      low[x]=min(low[x],dfn[y]);
  }
}
int main(){
  ios::sync_with_stdio(0),cin.tie(0),cout.tie(0);
  cin>>n>>m;
  while(m--){
    cin>>a>>b;
    if(a==b) continue; //忽略自环
    e[a].push_back(b),
    e[b].push_back(a);
  }
  for(root=1;root<=n;root++)if(!dfn[root])tarjan(root);
  cout<<cnt<<"\n";
  for(int i=1;i<=cnt;i++){
    cout<<dcc[i].size()<<" ";
    for(int j:dcc[i])cout<<j<<" ";
    cout<<"\n";
  }
}
```
