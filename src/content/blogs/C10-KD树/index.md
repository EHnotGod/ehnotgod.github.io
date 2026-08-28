---
title: "C10 KD树"
publishDate: 2026-08-08
description: "KD 树：多维最近点对 / 最近邻查询。"
category: algo
tags:
  - 数据结构
language: zh
---

### 题目情境

题目链接：https://www.luogu.com.cn/problem/P1429

**题目描述**

给定平面上 $$n$$ 个点，找出其中的一对点的距离，使得在这 $$n$$ 个点的所有点对中，该距离为所有点对中最小的

**输入格式**

第一行：$$n$$ ，保证 $$2\le n\le 200000$$ 。

接下来 $$n$$ 行：每行两个实数：$$x\ y$$ ，表示一个点的行坐标和列坐标，中间用一个空格隔开。

**输出格式**

仅一行，一个实数，表示最短距离，精确到小数点后面 $$4$$ 位。

**输入输出样例 #1**

输入 #1

```
3
1 1
1 2
2 2
```

输出 #1

```
1.0000
```

数据保证 $$0\le x,y\le 10^9$$

### 算法解析

KD-Tree 可以理解成一棵“按坐标不断切分平面”的二叉树。建树时，第一层按 x 坐标找中位数作为根，下一层按 y 坐标，再下一层又按 x，交替进行。这样每个节点既代表一个点，也代表它整棵子树中所有点所在的一个矩形区域，也就是包围盒 `L[] ~ U[]`。

查询一个点最近的已有点时，从根开始 DFS。每到一个节点，先计算查询点到当前节点的真实距离，用它更新当前最优答案 `ans`。然后分别计算查询点到左、右子树包围盒的最小可能距离 `dl、dr`。这个值表示：即使子树里存在最理想的点，它也不可能比这个距离更近。

如果某个子树的包围盒最小距离已经 `>= ans`，说明这棵子树里的所有点都不可能成为更优答案，可以直接剪枝；否则继续递归。通常先搜索 `dl、dr` 较小的一边，这样更容易提前找到更小的 `ans`，从而剪掉另一边更多节点。

你现在把任意查询点放进 `t[0]`，再设 `cur=0`，就可以直接复用原来的 `dis()`、`dis2()` 和 `query()`。因此整个算法核心就是：**KD-Tree 建树负责把点划分成区域，query 通过“点到包围盒的距离下界”进行剪枝，从而快速找到最近点。**


### py代码实现

略

### C++代码实现

```c++
// 交替建树 970ms
#include <cstdio>
#include <cstring>
#include <algorithm>
#include <cmath>
#define lc t[p].l
#define rc t[p].r
using namespace std;

const int N=200010;
double ans=2e18;
int n,K,root,cur; //K维度,root根,cur当前节点
struct KD{     //KD树节点信息
  int l,r;     //左右孩子
  double v[2]; //点的坐标值
  double L[2],U[2]; //子树区域的坐标范围
  bool operator<(const KD &b)const{return v[K]<b.v[K];}
}t[N];

void pushup(int p){ //更新p子树区域的坐标范围
  for(int i=0;i<2;i++){
    t[p].L[i]=t[p].U[i]=t[p].v[i];
    if(lc)
      t[p].L[i]=min(t[p].L[i],t[lc].L[i]),
      t[p].U[i]=max(t[p].U[i],t[lc].U[i]);
    if(rc)
      t[p].L[i]=min(t[p].L[i],t[rc].L[i]),
      t[p].U[i]=max(t[p].U[i],t[rc].U[i]);
  }
}
int build(int l,int r,int k){ //交替建树
  if(l>r) return 0;
  int m=(l+r)>>1; 
  K=k; nth_element(t+l,t+m,t+r+1); //中位数
  t[m].l=build(l,m-1,k^1);
  t[m].r=build(m+1,r,k^1);
  pushup(m);
  return m;
}
double sq(double x){return x*x;}
double dis(int p){ //当前点到p点的距离
  double s=0;
  for(int i=0;i<2;i++) 
    s+=sq(t[cur].v[i]-t[p].v[i]);
  return s;
}
double dis2(int p){ //当前点到p子树区域的最小距离
  if(!p) return 2e18; 
  double s=0;
  for(int i=0;i<2;++i)
    s+=sq(max(t[cur].v[i]-t[p].U[i],0.0))+
       sq(max(t[p].L[i]-t[cur].v[i],0.0));
  return s;
}
void query(int p){ //查询当前点的最小距离
  if(!p) return;
  if(p!=cur) ans=min(ans,dis(p));
  double dl=dis2(lc),dr=dis2(rc);
  if(dl<dr){
    if(dl<ans) query(lc);
    if(dr<ans) query(rc);
  }
  else{
    if(dr<ans) query(rc);
    if(dl<ans) query(lc);
  }
}
int main(){
  scanf("%d",&n);
  for(int i=1; i<=n; i++)
    scanf("%lf%lf",&t[i].v[0],&t[i].v[1]);
  root=build(1,n,0);
  for(cur=1; cur<=n; cur++) query(root);
  printf("%.4lf\n",sqrt(ans));
}
```
使用以下代码可以查任意点到点群的最近距离：
```c++
double queryPoint(double x,double y){
  t[0].v[0]=x;
  t[0].v[1]=y;
  cur=0;
  ans=2e18;
  query(root);
  return sqrt(ans);
}
```