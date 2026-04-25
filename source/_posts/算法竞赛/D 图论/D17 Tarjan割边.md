---
title: "D17 Tarjan割边"
categories:
- [算法, D 图论]
tags:
- 图论
---

### 题目情境

P1656 炸铁路

**题目描述**

A 国派出将军 uim，对 B 国进行战略性措施，以解救涂炭的生灵。

B 国有 $n$ 个城市，这些城市以铁路相连。任意两个城市都可以通过铁路直接或者间接到达。

uim 发现有些铁路被毁坏之后，某两个城市无法互相通过铁路到达。这样的铁路就被称为 key road。

uim 为了尽快使该国的物流系统瘫痪，希望炸毁铁路，以达到存在某两个城市无法互相通过铁路到达的效果。

然而，只有一发炮弹（A 国国会不给钱了）。所以，他能轰炸哪一条铁路呢？

**输入格式**

第一行 $n,m\ (1 \leq n\leq 150$，$1 \leq m \leq 5000)$，分别表示有 $n$ 个城市，总共 $m$ 条铁路。

以下 $m$ 行，每行两个整数 $a, b$，表示城市 $a$ 和城市 $b$ 之间有铁路直接连接。

**输出格式**

输出有若干行。

每行包含两个数字 $a,b$，其中 $a<b$，表示 $\lang a,b\rang$ 是 key road。

请注意：输出时，所有的数对 $\lang a,b\rang$ 必须按照 $a$ 从小到大排序输出；如果 $a$ 相同，则根据 $b$ 从小到大排序。

输入 #1

```
6 6
1 2
2 3
2 4
3 5
4 5
5 6
```

输出 #1

```
1 2
5 6
```

### C++代码实现

```c++
#include<bits/stdc++.h>
using namespace std;

const int N=210,M=10010;
int n,m,a,b;
int h[N],to[M],ne[M],idx=1; //从2,3开始配对
void add(int a,int b){
  to[++idx]=b;ne[idx]=h[a];h[a]=idx;
}
int dfn[N],low[N],tim,cnt;
struct bridge{
  int x,y;
  bool operator<(const bridge &t)const{
    if(x==t.x) return y<t.y;
    return x<t.x;
  }
}bri[M]; //割边

void tarjan(int x,int ine){
  dfn[x]=low[x]=++tim;
  for(int i=h[x];i;i=ne[i]){
    int y=to[i];
    if(!dfn[y]){ //若y未访问
      tarjan(y,i);
      low[x]=min(low[x],low[y]);
      if(low[y]>dfn[x]) bri[cnt++]={x,y};
    }
    else if(i!=(ine^1)) //若y已访问且不是反边
      low[x]=min(low[x],dfn[y]);
  }
}
int main(){
  cin>>n>>m;
  while(m--){
    cin>>a>>b;
    add(a,b),add(b,a);
  }
  for(int i=1;i<=n;i++) if(!dfn[i])tarjan(i,0);
  sort(bri,bri+cnt);
  for(int i=0;i<cnt;i++)
    cout<<bri[i].x<<" "<<bri[i].y<<"\n";
}
```
