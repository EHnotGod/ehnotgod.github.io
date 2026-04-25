---
title: "B15 BFS广搜"
categories:
- [算法, B 搜索算法]
tags:
- 搜索算法
---

### 题目情境

![image-20250416093032988](/images/B/B15-1.png)

![image-20250825223816587](/images/B/B15-2.png)

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
