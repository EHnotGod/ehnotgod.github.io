---
title: "D47 树的直径"
publishDate: 2026-08-08
description: "树的直径：两次 DFS/BFS 求最远点对。"
category: algo
tags:
  - 图论
language: zh
---

### 题目情境

题目链接：https://www.luogu.com.cn/problem/B4016

B4016 树的直径

**题目描述**

给定一棵 $$n$$ 个结点的树，树没有边权。请求出树的直径是多少，即树上最长的不重复经过一个点的路径长度是多少。

**输入格式**

第一行输入一个正整数 $$n$$，表示结点个数。

第二行开始，往下一共 $$n-1$$ 行，每一行两个正整数 $$(u,v)$$，表示一条边。

**输出格式**

输出一行，表示树的直径是多少。

输入 #1

```
5
1 2
2 4
4 5
2 3
```

输出 #1

```
3
```

数据保证，$$1 \leq n \leq 10^5$$。

![image-20250816214118195](/images/算法竞赛/D/D47-1.png)

### 算法解析：

树的直径即树上最长路径。方法：任选一点出发 DFS/BFS 找到最远点 $p$，再从 $p$ 出发 DFS/BFS 找到最远点 $q$，则 $p$ 到 $q$ 的路径就是直径（原理：从任意点出发的最远点必是直径的一个端点）。无负边权时也可用树形 DP 求。复杂度 $O(n)$。

### C++代码实现

```c++
// 树的直径 正边权 两次DFS O(n)
#include<bits/stdc++.h>
using namespace std;

const int N=100005;
int n,rt,d[N];
vector<pair<int,int>> e[N];

void dfs(int u,int fa){
  if(d[rt]<d[u]) rt=u; //记录最远点
  for(auto [v,w]:e[u]){
    if(v==fa) continue;
    d[v]=d[u]+w; //d[v]从根走到v的距离
    dfs(v,u);
  }
}
int main(){
  cin>>n;
  for(int i=1,x,y;i<n;i++){
    cin>>x>>y;
    e[x].emplace_back(y,1);
    e[y].emplace_back(x,1);
  }
  dfs(1,0);  //找出离1最远的点rt
  d[rt]=0;
  dfs(rt,0); //找出离rt最远的点
  cout<<d[rt];
}
```

```c++
// 树的直径 正负边权 树形DP O(n)
#include<bits/stdc++.h>
using namespace std;

const int N=100005;
int n,mxd,d[N]; //d[u]从u点向下走的最长距离
vector<pair<int,int>> e[N];

void dfs(int u,int fa){
  for(auto [v,w]:e[u]){
    if(v==fa) continue;
    dfs(v,u);
    mxd=max(mxd,d[u]+w+d[v]); //拼凑直径
    d[u]=max(d[u],d[v]+w);    //更新d[u]
  }
}
int main(){
  cin>>n;
  for(int i=1,x,y;i<n;i++){
    cin>>x>>y;
    e[x].emplace_back(y,1);
    e[y].emplace_back(x,1);
  }
  dfs(1,0);
  cout<<mxd;
}
```
