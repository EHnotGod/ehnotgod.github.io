---
title: "G60 有向图博弈-SG函数"
categories:
- [算法, G 数学]
tags:
- 数学
---

### 题目情境

![image-20251010103151069](/images/G/G60-1.png)

**题目描述**

给定一个有 N 个节点的有向无环图，图中某些节点上有棋子，两名玩家交替移动棋子。

玩家每一步可将任意一颗棋子沿一条有向边移动到另一个点，无法移动者输掉游戏。

对于给定的图和棋子初始位置，双方都会采取最优的行动，询问先手必胜还是先手必败。

**输入格式**

第一行，三个整数 N , M, K，N 表示图中节点总数，M 表示图中边的条数，K 表示棋子的个数。

接下来 M 行，每行两个整数 X, Y 表示有一条边从 X 出发指向 Y。

接下来一行，K 个空格间隔的整数，表示初始时，棋子所在的节点编号。

**输出格式**

若先手胜，输出 `win`，否则输出 `lose`。

### C++代码实现

```c++
#include <cstdio>
#include <cstring>
#include <set>
using namespace std;

const int N=2005,M=10005;
int n,m,k,a,b,x;
int h[N],to[M],ne[M],tot; //邻接表
int f[N];

void add(int a,int b){
  to[++tot]=b,ne[tot]=h[a],h[a]=tot;
}
int sg(int u){
  // 记忆化搜索
  if(f[u]!=-1) return f[u]; 
  // 把子节点的sg值插入集合
  set<int> S;
  for(int i=h[u];i;i=ne[i]) 
    S.insert(sg(to[i]));
  // mex运算求当前节点的sg值并记忆
  for(int i=0; ;i++) 
    if(!S.count(i)) return f[u]=i;
}
int main(){
  scanf("%d%d%d",&n,&m,&k);
  for(int i=0;i<m;i++)
    scanf("%d%d",&a,&b), add(a,b);
  memset(f,-1,sizeof f); 
  int res=0;
  for(int i=0;i<k;i++)
    scanf("%d",&x),res^=sg(x);
  if(res) puts("win");
  else puts("lose");
}
```
