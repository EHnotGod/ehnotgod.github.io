---
title: "B15 BFS广搜"
publishDate: 2026-08-08
description: "BFS 广度优先搜索：队列逐层扩展求最短路。"
category: algo
tags:
  - 搜索算法
language: zh
---

### 题目情境

题目链接：https://www.luogu.com.cn/problem/P1588

**题目描述**

FJ 丢了一头牛，决定将其找回。FJ 和牛位于数轴上，初始位置分别为 $x$ 和 $y$，牛保持不动。每次移动时，若 FJ 处于位置 $x$，他可移动至 $x+1$、$x-1$ 或 $2x$。计算 FJ 抓住牛所需的最少移动次数。

![](/images/算法竞赛/B/B15-1.png)

![](/images/算法竞赛/B/B15-2.png)

**输入格式**

第一行为一个整数 $T$，表示数据组数；接下来每行包含两个正整数 $x,y$，分别表示 FJ 和牛的坐标。

**输出格式**

对于每组数据，输出最少步数，每组数据间用换行隔开。

输入 #1

```
1
5 17
```

输出 #1

```
4
```

**说明/提示**

对于 $100\%$ 的数据，$0 \le x,y \le 10^5$。

### 算法解析：

把数轴上的每个位置看作图上的一个点，从起点 $x$ 出发，每次可移动到 $x+1$、$x-1$ 或 $2x$，用 BFS 逐层向外扩展。BFS 第一次访问到终点 $y$ 时，经过的层数就是最少步数——每一层都代表当前步数内的所有可达位置，先到即最优。

### Python代码实现

```python
# P1588 [USACO07OPEN] Catch That Cow S

def bfs():
    global x, y
    N = int(2e5 + 1)
    dis = [-1 for i in range(N)]
    dis[x] = 0
    l = 0
    q = []; q.append(x)
    while l < len(q):
        x = q[l]
        l += 1
        if x + 1 < N and dis[x + 1] == -1:
            dis[x + 1] = dis[x] + 1
            q.append(x + 1)
        if x - 1 > 0 and dis[x - 1] == -1:
            dis[x - 1] = dis[x] + 1
            q.append(x - 1)
        if 2 * x < N and dis[x * 2] == -1:
            dis[x * 2] = dis[x] + 1
            q.append(x * 2)
        if x == y:
            print(dis[y])
            return

t = int(input())
for i in range(t):
    x, y = map(int, input().split())
    bfs()
```

### C++代码实现

```c++
#include <cstring>
#include <iostream>
#include <algorithm>
#include <queue>
using namespace std;

const int N=100005;
int x, y, dis[N];

void bfs(){
  memset(dis,-1,sizeof dis); dis[x]=0;
  queue<int> q; q.push(x);
  while(q.size()){
    int x=q.front(); q.pop();
    if(x+1<N && dis[x+1]==-1){
      dis[x+1]=dis[x]+1; //前进一步
      q.push(x+1);
    }
    if(x-1>0 && dis[x-1]==-1){
      dis[x-1]=dis[x]+1; //后退一步
      q.push(x-1);
    }
    if(2*x<N && dis[2*x]==-1){
      dis[2*x]=dis[x]+1; //走到2x位置
      q.push(2*x);
    }
    if(x==y){printf("%d\n",dis[y]);return;}
  }
}
int main(){
  int T; cin>>T;
  while(T--) cin>>x>>y, bfs();
}
```
