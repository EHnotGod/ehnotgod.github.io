---
title: "D5 全源 Johnson 算法"
categories:
- [算法, D 图论]
tags:
- 图论
---

### 题目情境

**题目描述**

给定一个包含 $n$ 个结点和 $m$ 条带权边的有向图，求所有点对间的最短路径长度，一条路径的长度定义为这条路径上所有边的权值和。

注意：边权**可能**为负，且图中**可能**存在重边和自环；

**输入格式**

第 $1$ 行：$2$ 个整数 $n,m$，表示给定有向图的结点数量和有向边数量。

接下来 $m$ 行：每行 $3$ 个整数 $u,v,w$，表示有一条权值为 $w$ 的有向边从编号为 $u$ 的结点连向编号为 $v$ 的结点。

**输出格式**

若图中存在负环，输出仅一行 $-1$。

若图中不存在负环：

输出 $n$ 行：令 $dis_{i,j}$ 为从 $i$ 到 $j$ 的最短路，在第 $i$ 行输出 $\sum\limits_{j=1}^n j\times dis_{i,j}$，注意这个结果可能超过 int 存储范围。

如果不存在从 $i$ 到 $j$ 的路径，则 $dis_{i,j}=10^9$；如果 $i=j$，则 $dis_{i,j}=0$。

**输入输出样例 #1**

输入 #1

```
5 7
1 2 4
1 4 10
2 3 7
4 5 3
4 2 -2
3 4 -3
5 3 4
```

输出 #1

```
128
1000000072
999999978
1000000026
1000000014
```

**输入输出样例 #2**

输入 #2

```
5 5
1 2 4
3 4 9
3 4 -3
4 5 3
5 3 -2
```

输出 #2

```
-1
```

对于 $100\%$ 的数据，$1\leq n\leq 3\times 10^3,\ \ 1\leq m\leq 6\times 10^3,\ \ 1\leq u,v\leq n,\ \ -3\times 10^5\leq w\leq 3\times 10^5$。

**解析：**EH不会，只是默默地放图片说明一切。

![image-20250418091441310](/images/算法竞赛/D/D5-1.png)

### Python代码实现

```python
import heapq

class Edge():
    def __init__(self, v, w):
        self.v = v
        self.w = w

def spfa():
    global h, vis, cnt
    q = []; l = 0
    h = [int(1e20) for i in range(n + 1)]
    vis = [False for i in range(n + 1)]
    h[0] = 0; vis[0] = True; q.append(0)
    while len(q) > l:
        u = q[l]; l += 1; vis[u] = False
        for ed in e[u]:
            v = ed.v; w = ed.w
            if h[v] > h[u] + w:
                h[v] = h[u] + w
                cnt[v] = cnt[u] + 1
                if cnt[v] > n:
                    print(-1);exit()
                if not vis[v]:
                    q.append(v)
                    vis[v] = True

def dijkstra(s):
    global h, vis, cnt
    for i in range(n + 1):
        d[i] = int(1e9)
    vis = [False for i in range(n + 1)]
    d[s] = 0
    q = []
    heapq.heappush(q, [0, s])
    while len(q) > 0:
        t = heapq.heappop(q)
        u = t[1]
        if vis[u]:
            continue
        vis[u] = 1
        for ed in e[u]:
            v = ed.v
            w = ed.w
            if d[v] > d[u] + w:
                d[v] = d[u] + w
                heapq.heappush(q, [d[v], v])



n, m = map(int, input().split())
e = [[] for i in range(n + 1)]
h = [0] * (n + 1)
d = [0] * (n + 1)
vis = [0] * (n + 1)
cnt = [0] * (n + 1)
for i in range(m):
    a, b, c = map(int, input().split())
    e[a].append(Edge(b, c))
for i in range(1, n + 1):
    e[0].append(Edge(i, 0))
spfa()
for u in range(1, n + 1):
    for ed in e[u]:
        ed.w += h[u] - h[ed.v]
for i in range(1, n + 1):
    dijkstra(i)
    ans = 0
    for j in range(1, n + 1):
        if d[j] == int(1e9):
            ans += j * int(1e9)
        else:
            ans += j * (d[j] + h[j] - h[i])
    print(ans)
```

### C++代码实现

```c++
#include<algorithm>
#include<cstring>
#include<iostream>
#include<queue>
#define N 30010
#define INF 1000000000
using namespace std;

int n,m,a,b,c;
struct edge{int v,w;};
vector<edge> e[N];
int vis[N],cnt[N];
long long h[N],d[N];

void spfa(){
    queue<int>q;
    memset(h,63,sizeof h);
    memset(vis,false,sizeof vis);
    h[0]=0,vis[0]=1;q.push(0);
    while(q.size()){
        int u=q.front(); q.pop();vis[u]=0;
        for(auto ed : e[u]){
            int v=ed.v,w=ed.w;
            if(h[v]>h[u]+w){
                h[v]=h[u]+w;
        cnt[v]=cnt[u]+1;
        if(cnt[v]>n){
          printf("-1\n");exit(0);
        }
                if(!vis[v])q.push(v),vis[v]=1;
            }
        }
    }
}
void dijkstra(int s){
    priority_queue<pair<long long,int>>q;
    for(int i=1;i<=n;i++)d[i]=INF;
    memset(vis,false,sizeof vis);
    d[s]=0; q.push({0,s});
    while(q.size()){
        int u=q.top().second;q.pop();
        if(vis[u])continue;
        vis[u]=1;
        for(auto ed : e[u]){
            int v=ed.v,w=ed.w;
            if(d[v]>d[u]+w){
                d[v]=d[u]+w;
                if(!vis[v]) q.push({-d[v],v});
            }
        }
    }
}
int main(){
  cin>>n>>m;
  for(int i=0;i<m;i++)
    cin>>a>>b>>c, e[a].push_back({b,c});
    for(int i=1;i<=n;i++)
      e[0].push_back({i,0});//加虚拟边

    spfa();
    for(int u=1;u<=n;u++)
      for(auto &ed:e[u])
        ed.w+=h[u]-h[ed.v];//构造新边
    for(int i=1;i<=n;i++){
        dijkstra(i);
        long long ans=0;
        for(int j=1;j<=n;j++){
            if(d[j]==INF) ans+=(long long)j*INF;
            else ans+=(long long)j*(d[j]+h[j]-h[i]);
        }
        printf("%lld\n",ans);
    }
    return 0;
}
```
