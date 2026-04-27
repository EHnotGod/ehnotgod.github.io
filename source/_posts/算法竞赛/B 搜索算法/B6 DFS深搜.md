---
title: "B6 DFS深搜"
categories:
- [算法, B 搜索算法]
tags:
- 搜索算法
---

### 题目情境

![image-20250416092841158](/images/算法竞赛/B/B6-1.png)

![image-20250416092956833](/images/算法竞赛/B/B6-2.png)

![image-20250825223847899](/images/算法竞赛/B/B6-3.png)

### Python代码实现

```python
# P1219 [USACO1.5] 八皇后 Checker Challenge

N = 30
pos = [0] * N
c = [0] * N
p = [0] * N
q = [0] * N
ans = 0
def pr():
    if ans <= 3:
        for i in range(1, n + 1):
            print(pos[i], end=" ")
        print()
def dfs(i):
    global ans
    if i > n:
        ans += 1
        pr()
        return
    for j in range(1, n + 1):
        if c[j] or p[i + j] or q[i - j + n]:
            continue
        pos[i] = j
        c[j] = p[i + j] = q[i - j + n] = 1
        dfs(i + 1)
        c[j] = p[i + j] = q[i - j + n] = 0
n = int(input())
dfs(1)
print(ans)
```

### C++代码实现

```c++
#include <iostream>
#include <cstring>
#include <algorithm>
using namespace std;

const int N=30;
int n, ans;
int pos[N],c[N],p[N],q[N];

void print(){
  if(ans<=3){
    for(int i=1;i<=n;i++)
      printf("%d ",pos[i]);
    puts("");
  }
}
void dfs(int i){
  if(i>n){
    ans++; print(); return;
  }
  for(int j=1; j<=n; j++){
    if(c[j]||p[i+j]||q[i-j+n])continue;
    pos[i]=j; //记录第i行放在了第j列
    c[j]=p[i+j]=q[i-j+n]=1; //宣布占领
    dfs(i+1);
    c[j]=p[i+j]=q[i-j+n]=0; //恢复现场
  }
}
int main(){
  cin >> n;
  dfs(1);
  cout << ans;
  return 0;
}
```
