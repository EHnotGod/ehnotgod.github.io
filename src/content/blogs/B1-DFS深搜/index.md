---
title: "B1 DFS深搜"
publishDate: 2026-08-08
description: "DFS 深度优先搜索：递归遍历所有状态。"
category: algo
tags:
  - 搜索算法
language: zh
---

### 题目情境

题目链接：https://www.luogu.com.cn/problem/P1219

**题目描述**

一个如下的 $6 \times 6$ 的跳棋棋盘，有六个棋子被放置在棋盘上，使得每行、每列有且只有一个，每条对角线（包括两条主对角线的所有平行线）上至多有一个棋子。

![](https://cdn.luogu.com.cn/upload/image_hosting/3h71x0yf.png)

上面的布局可以用序列 $2\ 4\ 6\ 1\ 3\ 5$ 来描述，第 $i$ 个数字表示在第 $i$ 行的相应位置有一个棋子，如下：

行号 $1\ 2\ 3\ 4\ 5\ 6$

列号 $2\ 4\ 6\ 1\ 3\ 5$

这只是棋子放置的一个解。请编一个程序找出所有棋子放置的解。  
并把它们以上面的序列方法输出，解按字典顺序排列。  
请输出前 $3$ 个解。最后一行是解的总个数。

**输入格式**

一行一个正整数 $n$，表示棋盘是 $n \times n$ 大小的。

**输出格式**

前三行为前三个解，每个解的两个数字之间用一个空格隔开。第四行只有一个数字，表示解的总数。

输入 #1

```
6

```

输出 #1

```
2 4 6 1 3 5
3 6 2 5 1 4
4 1 5 2 6 3
4

```

**说明/提示**

对于 $100\%$ 的数据，$6 \le n \le 13$。

### 算法解析：

1. 从第1行开始放，然后尝试放第2·n行。

2. 对于第i行，依次枚举第1·n列，如果第j列能放下，则记住位置，宣布占领该位置（i）的辐射区域，然后继续搜索第i+1行。

3. 如果第i+1行的n列均放不下，则退回第i行的状态空间，恢复现场，尝试第i行的下一列。

4. 如果能放满n行.说明找到了一种合法方案，则ans+1，打印方案，接着返回上一行，继续搜索另一个合法方案，直到搜完所有可能方案。

5. 因为是逐行逐列搜的，先搜到的字典序一定最小。

![](/images/算法竞赛/B/B1-3.png)

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
