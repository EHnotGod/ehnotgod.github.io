---
title: "D99 Kruscal重构树"
categories:
- [算法, D 图论]
tags:
- 图论
---

### 题目情境

**题目描述**

给定一张 $N$ 个点的无向图，记为 $1\cdots N$ 。

图中有 $M$ 条边，第 $j$ 条边的长度为 $d_j$ 。

现在有 $K$ 个询问，每个询问的格式为 $A\ \  B$，表示询问从 $A$ 走到 $B$ 的所有路径中，最长边的最小值为多少。

**输入格式**

第一行为三个整数 $N, M, K$ 。

第二行到第 $M+1$ 行，每行三个整数 $X, Y, D$ ，表示从 $X$ 与 $Y$ 之间有一条长度为 $D$ 的边。

第 $M+2$ 行到第 $M+K+1$ 行，每行两个整数 $A, B$ ，意义如上。

**输出格式**

共 $K$ 行。

对于每个询问，输出最长边的最小值。

输入 #1

```
6 6 8
1 2 5
2 3 4
3 4 3
1 4 8
2 5 7
4 6 2
1 2
1 3
1 4
2 3
2 4
5 1
6 2
6 1
```

输出 #1

```
5
5
5
4
4
7
4
5
```

$1 \leq N \leq 15000$

$1 \leq M \leq 30000$

$1 \leq D_j \leq 10^9$

$1 \leq K \leq 15000$

------

## E-动态规划

### C++代码实现

```c++
/*EHnotgod————
..............#######.....#.....#..............
..............#...........#.....#..............
..............#######.....#######..............
..............#...........#.....#..............
..............#######.....#.....#..............
*/
#include <bits/stdc++.h>
using namespace std;
#define endl "\n"
#define int long long
#define range(i, a, b) for (int i = (a); i < (b); ++i)
#define def(name, ...) auto name = [&](__VA_ARGS__)

const int N=200006;
int n, m, q;
struct edge{
  int u,v,w;
  bool operator<(const edge &t)const
  {return w < t.w;}
}edge[N];
int fa2[N],ans,cnt;
vector<int> value(N, 0);
vector<vector<int>> e(N, vector<int>());
int find(int x){
  if(fa2[x]==x) return x;
  return fa2[x]=find(fa2[x]);
}
void kruskal(){
  sort(edge,edge+m);
  cnt = n;
  for(int i=1;i<N;i++)fa2[i]=i;
  for(int i=0; i<m; i++){
    int x = find(edge[i].u);
    int y = find(edge[i].v);
    if(x!=y){
        cnt++;
        fa2[x]=cnt;
        fa2[y]=cnt;
        value[cnt] = edge[i].w;

        e[x].push_back(cnt);
        e[y].push_back(cnt);
        e[cnt].push_back(x);
        e[cnt].push_back(y);
    }
  }
}
int f[N][22],dep[N];

void dfs(int u,int fa){
  f[u][0]=fa; dep[u]=dep[fa]+1;
  for(int i=1;i<=20;i++) //u的2,4,8...祖先
    f[u][i]=f[f[u][i-1]][i-1];
  for(int v:e[u])
    if(v!=fa) dfs(v,u);
}
int lca(int u,int v){
  if(dep[u]<dep[v]) swap(u,v);
  for(int i=20;~i;i--) //u先大步后小步向上跳，直到与v同层
    if(dep[f[u][i]]>=dep[v]) u=f[u][i];
  if(u==v) return v;
  for(int i=20;~i;i--) //u,v一起向上跳，直到lca的下面
    if(f[u][i]!=f[v][i]) u=f[u][i],v=f[v][i];
  return f[u][0];
}
// vector<int> a(n, 0);
// vector<vector<int>> dp(n + 1, vector<int>(n + 1, 0));
void solve() {
	cin >> n >> m >> q;
	for (int i = 0; i < m; i++){
		cin >> edge[i].u >> edge[i].v >> edge[i].w;
	}
    kruskal();

    dfs(cnt, 0);
    
    while (q--){
        int u, v; cin >> u >> v;
        int uv = lca(u, v);
        cout << value[uv] << endl;
    }
}

signed main() {
    ios::sync_with_stdio(0);
    cin.tie(0);
    cout.tie(0);
	int t;
	t = 1;
	while (t--) {
		solve();
	}
	return 0;
}
```
