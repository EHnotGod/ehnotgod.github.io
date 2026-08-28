---
title: "D12 强连通分量Tarjan算法"
publishDate: 2026-08-08
description: "Tarjan 强连通分量：有向图 SCC。"
category: algo
tags:
  - 图论
language: zh
---

### 题目情境

题目链接：https://www.luogu.com.cn/problem/P2863

P2863 [USACO06JAN] The Cow Prom S

**题目描述**

有一个 $$n$$ 个点，$$m$$ 条边的有向图，请求出这个图点数大于 $$1$$ 的强连通分量个数。

**输入格式**

第一行为两个整数 $$n$$ 和 $$m$$。

第二行至 $$m+1$$ 行，每一行有两个整数 $$a$$ 和 $$b$$，表示有一条从 $$a$$ 到 $$b$$ 的有向边。

**输出格式**

仅一行，表示点数大于 $$1$$ 的强连通分量个数。

输入 #1

```
5 4
2 4
3 5
1 2
4 1
```

输出 #1

```
1
```

对于全部的测试点，保证 $$2\le n \le 10^4$$，$$2\le m\le 5\times 10^4$$，$$1 \leq a, b \leq n$$。

![image-20250817142047464](/images/算法竞赛/D/D12-1.png)

### 算法解析：

Tarjan 强连通分量：DFS 时给每个点记录 $dfn$（访问序）和 $low$（子树内能回溯到的最早 $dfn$），用栈维护当前 SCC 候选。当 $low[u]==dfn[u]$ 时，$u$ 是 SCC 的根，把栈顶到 $u$ 的节点全部弹出作为一个 SCC。复杂度 $O(n+m)$。

### C++代码实现

```c++
// Tarjan算法 O(n+m)
#include<bits/stdc++.h>
using namespace std;

const int N=10010;
int n,m,a,b,ans;
vector<int> e[N]; 
int dfn[N],low[N],tim,stk[N],ins[N],top,scc[N],siz[N],cnt;

void tarjan(int x){
  dfn[x]=low[x]=++tim; //时间戳 追溯值
  stk[++top]=x,ins[x]=1;
  for(int y:e[x]){
    if(!dfn[y]){ //若y尚未访问
      tarjan(y);
      low[x]=min(low[x],low[y]); //因y是儿子
    }
    else if(ins[y]) //若y已访问且在栈中
      low[x]=min(low[x],dfn[y]); //因y是祖先或左子树点
  }

  if(dfn[x]==low[x]){ //若x是SCC的根
    ++cnt;
    while(1){
      int y=stk[top--]; ins[y]=0;
      scc[y]=cnt; //SCC的编号
      ++siz[cnt]; //SCC的大小
      if(y==x) break;
    }
  }
}
int main(){
  ios::sync_with_stdio(0),cin.tie(0),cout.tie(0);
  cin>>n>>m;
  while(m--)
    cin>>a>>b, e[a].push_back(b);
  for(int i=1;i<=n;i++) //可能不连通
    if(!dfn[i]) tarjan(i);
  for(int i=1;i<=cnt;i++)
     if(siz[i]>1) ans++;
  cout<<ans;
}
```
