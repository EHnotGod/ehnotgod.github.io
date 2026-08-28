---
title: "C9 扫描线"
publishDate: 2026-08-08
description: "扫描线：矩形面积并 / 周长并。"
category: algo
tags:
  - 数据结构
language: zh
---

### 题目情境

题目链接：https://www.luogu.com.cn/problem/P5490

**题目描述**

求 $$n$$ 个四边平行于坐标轴的矩形的面积并。

**输入格式**

第一行一个正整数 $$n$$。

接下来 $$n$$ 行每行四个非负整数 $$x_1, y_1, x_2, y_2$$，表示一个矩形的四个端点坐标为 $$(x_1, y_1),(x_1, y_2),(x_2, y_2),(x_2, y_1)$$。

**输出格式**

一行一个正整数，表示 $$n$$ 个矩形的并集覆盖的总面积。

输入 #1

```
2
100 100 200 200
150 150 250 255
```

输出 #1

```
18000
```

对于 $$100\%$$ 的数据，$$1 \le n \le {10}^5$$，$$0 \le x_1 < x_2 \le {10}^9$$，$$0 \le y_1 < y_2 \le {10}^9$$。

### 算法解析

![image-20250826121538028](/images/算法竞赛/C/C9-1.png)

核心思路是把每个矩形拆成两条水平边：下边记 `+1` 表示矩形开始，上边记 `-1` 表示矩形结束，然后按 `y` 从小到大扫描。扫描到某条边时，就在线段树中给它对应的 `x` 区间加上或减去覆盖次数；线段树的 `len[1]` 始终表示当前所有矩形在 x 轴上的总覆盖长度，重叠部分只算一次。因此从当前高度 `L[i].y` 到下一条边 `L[i+1].y` 之间的面积就是 `len[1] * (L[i+1].y-L[i].y)`。由于 x 坐标可能很大，所以先把所有 `x1、x2` 排序去重做离散化；其中离散后的第 `i` 段实际上表示 `[X[i],X[i+1])`，因此原区间 `[x1,x2)` 要在线段树中更新 `[l,r-1]`，而节点 `[l,r]` 的真实长度就是 `X[r+1]-X[l]`。


### C++代码实现

```c++
// 扫描线+线段树+离散化 1.4s
#include <iostream>
#include <cstdio>
#include <algorithm>
using namespace std;

#define ls u<<1
#define rs u<<1|1
const int N=200005;
struct line{   //扫描线
  int x1,x2,y;
  int tag;     //入边:+1,出边:-1
  bool operator<(line &t){return y<t.y;}
}L[N];
int cnt[N*8],len[N*8]; //线段树
int X[N];              //X坐标
void pushup(int u,int l, int r){
  if(cnt[u]) len[u]=X[r+1]-X[l]; //r → X[r+1]
  else len[u]=len[ls]+len[rs];
}
void change(int u,int l,int r,int a,int b,int tag){
  if(a>r || b<l) return; //越界
  if(a<=l && r<=b){      //覆盖
    cnt[u]+=tag;
    pushup(u,l,r);
    return;
  }
  int m=l+r>>1;
  change(ls,l,m,a,b,tag); //裂开
  change(rs,m+1,r,a,b,tag);
  pushup(u,l,r);
}
int main(){
  int n,x1,x2,y1,y2; scanf("%d",&n);
  for(int i=1; i<=n; i++){
    scanf("%d%d%d%d",&x1,&y1,&x2,&y2);
    L[i]={x1,x2,y1,1};
    L[n+i]={x1,x2,y2,-1};
    X[i]=x1; X[n+i]=x2;         
  }
  n*=2;
  sort(L+1,L+n+1); //扫描线排序
  sort(X+1,X+n+1); //X坐标排序
  int s=unique(X+1,X+n+1)-X-1; //去重
  
  long long ans=0;
  for(int i=1; i<n; i++){
    int l=lower_bound(X+1,X+s+1,L[i].x1)-X;
    int r=lower_bound(X+1,X+s+1,L[i].x2)-X;
    change(1,1,s,l,r-1,L[i].tag); //x2 → r-1
    ans+=1ll*(L[i+1].y-L[i].y)*len[1];
  }
  printf("%lld\n",ans);
}
```
