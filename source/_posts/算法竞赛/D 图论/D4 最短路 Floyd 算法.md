---
title: "D4 最短路 Floyd 算法"
categories:
- [算法, D 图论]
tags:
- 图论
---

### 题目情境

![image-20250418091227375](/images/算法竞赛/D/D4-1.png)

### Python代码实现

```python
def floyd():
    for k in range(1, n + 1):
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                d[i][j] = min(d[i][j], d[i][k] + d[k][j])


n, m = map(int, input().split())
d = [[int(1e20) for __ in range(n + 1)] for _ in range(n + 1)]
for i in range(1, n + 1):
    d[i][i] = 0
for i in range(m):
    a, b, c = map(int, input().split())
    d[a][b] = min(d[a][b], c)
    floyd()
for i in range(1, n + 1):
    print(*d[i][1:])
```

### C++代码实现

```c++
#include <iostream>
#include <cstring>
#include <algorithm>
using namespace std;
const int N=210,M=20010;
int n,m,a,b,c;
int d[N][N];

void floyd(){
  for(int k=1; k<=n; k++)
    for(int i=1; i<=n; i++)
      for(int j=1; j<=n; j++)
        d[i][j]=min(d[i][j],d[i][k]+d[k][j]);
}
int main(){
  cin>>n>>m;
  memset(d,0x3f,sizeof d);
  for(int i=1; i<=n; i++)d[i][i]=0;
  for(int i=0; i<m; i++){
    cin>>a>>b>>c;
    d[a][b]=min(d[a][b],c); //重边
  }
  floyd();
  for(int i=1;i<=n;i++){
    for(int j=1;j<=n;j++)
      printf("%d ",d[i][j]);
    puts("");
  }
  return 0;
}
```
