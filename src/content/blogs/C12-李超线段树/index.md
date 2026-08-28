---
title: "C12 李超线段树"
publishDate: 2026-08-08
description: "李超线段树：维护一次函数最值。"
category: algo
tags:
  - 数据结构
language: zh
---

### 题目情境

题目链接：https://www.luogu.com.cn/problem/P4254

**题目描述**

Blue Mary 开公司，会陆续收到若干金融顾问的经营方案。每个顾问给出一个等差日收益序列：
- `Project S P` 表示第 $T$ 天的收益为 $f(T)=S+(T-1)\cdot P$；
- 初始时没有方案，任意天的最大收益为 0。

当收到若干方案后，Blue Mary 会进行若干次询问：
- `Query T` 要求返回当前已知所有方案在第 $T$ 天的**最大收益**（与 0 比较取较大者），并**以百元为单位向下取整**输出（例如：210 或 290 都输出 `2`）。

**输入格式**

第一行一个整数 $N$，表示操作总数；接下来 $N$ 行每行为一个操作，格式如题。

输入 #1

```
10
Project 5.10200 0.65000
Project 2.76200 1.43000
Query 4
Query 2
Project 3.80200 1.17000
Query 2
Query 3
Query 1
Project 4.58200 0.91000
Project 5.36200 0.39000
```

输出 #1

```
0
0
0
0
0
```

**说明/提示**

对于 $100\%$ 的数据，$1\le N\le 10^5$，$1\le T\le 5\times 10^4$，$0<P<100$，$|S|\le 10^5$。

### 算法解析：

李超线段树用来维护若干一次函数（直线）在某个横坐标上的最值。本题中每个经营方案对应一条直线 $f(T)=S+(T-1)\cdot P$，需要在某一天 $T$ 上查询所有方案取值的最大值。

线段树每个结点存一条"优势直线"（在当前区间中点上取值最大的一条）。插入新直线时，若新直线在中点更优则与当前直线交换，再根据左右端点的比较结果向对应的儿子递归；查询时沿根到叶子的路径取所有经过结点直线在 $x$ 处的最大值。单次插入与查询均为 $O(\log V)$（$V$ 为坐标范围）。

![](/images/算法竞赛/C/C12-1.png)

本题为银牌难度，实现细节较多，建议先理解"优势直线"的维护思想。

### Python代码实现

太难，略。

### C++代码实现

### C++代码实现

```c++
// 李超线段树 O(nlogn)
#include <iostream>
#include <cstring>
#include <algorithm>
using namespace std;

#define N 50005
#define ls u<<1
#define rs u<<1|1
int n,cnt;
struct line{
  double k,b; //斜率,截距
}p[N*2];
int tr[N*4]; //线段编号

double Y(int id,int x){ //求Y值
  return p[id].k*x+p[id].b;
}
void change(int u,int l,int r,int id){ //修改
  int mid=(l+r)>>1;
  if(Y(id,mid)>Y(tr[u],mid)) swap(id,tr[u]);
  if(Y(id,l)>Y(tr[u],l)) change(ls,l,mid,id);
  if(Y(id,r)>Y(tr[u],r)) change(rs,mid+1,r,id);
}
double query(int u,int l,int r,int x){ //查询
  if(l==r) return Y(tr[u],x);
  int mid=(l+r)>>1;
  double t=Y(tr[u],x);
  if(x<=mid) return max(t,query(ls,l,mid,x));
  else return max(t,query(rs,mid+1,r,x));
}
int main(){
  scanf("%d",&n);
  for(int i=1;i<=n;i++){
    char op[10]; scanf("%s",op);
    if(op[0]=='P'){
      double b,k; scanf("%lf%lf",&b,&k);
      p[++cnt]={k,b-k};
      change(1,1,N,cnt);
    }
    else{
      int x; scanf("%d",&x);
      printf("%d\n",(int)query(1,1,N,x)/100);
    }
  }
}
```
