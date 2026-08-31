---
title: "G8 线性筛质数"
publishDate: 2026-08-08
description: "线性筛（欧拉筛）：O(n) 筛质数。"
category: algo
tags:
  - 数学
language: zh
---
### 题目情境

题目链接：https://www.luogu.com.cn/problem/P3383

**题目描述**

本题已更新，从判断素数改为了查询第 $k$ 小的素数。  

**题目描述**

如题，给定一个范围 $n$，有 $q$ 个询问，每次输出第 $k$ 小的素数。

**输入格式**

第一行包含两个正整数 $n,q$，分别表示查询的范围和查询的个数。

接下来 $q$ 行每行一个正整数 $k$，表示查询第 $k$ 小的素数。

**输出格式**

输出 $q$ 行，每行一个正整数表示答案。

输入 #1

```
100 5
1
2
3
4
5
```

输出 #1

```
2
3
5
7
11
```

**说明/提示**

【数据范围】  
对于 $100\%$ 的数据，$n = 10^8$，$1 \le q \le 10^6$，保证查询的素数不大于 $n$。


### 算法解析：

欧拉筛（线性筛）：每个合数只被其最小质因子筛掉一次。枚举 $i$，若未被标记则是质数加入表；再枚举已有质数 $p$，标记 $i\cdot p$，当 $i\%p==0$ 时 break（保证每个合数只被最小质因子筛）。$O(n)$ 得质数表后直接回答第 $k$ 小质数。

### Python代码实现

```python
n, q = map(int, input().split())

# 使用欧拉筛（线性筛）来找出所有素数
vis = [True] * (n + 1)
prim = []
for i in range(2, n + 1):
    if vis[i]:
        prim.append(i)
    for p in prim:
        if i * p > n:
            break
        vis[i * p] = False
        if i % p == 0:
            break

for _ in range(q):
    k = int(input())
    print(prim[k - 1])
```

### C++代码实现

```c++
#include <iostream>
#include <cstring>
#include <algorithm>
using namespace std;

const int N = 100000010;
int vis[N];  //划掉合数
int prim[N]; //记录质数
int cnt; //质数个数

void get_prim(int n){ //线性筛法
  for(int i=2; i<=n; i++){
    if(!vis[i]) prim[++cnt] = i;
    for(int j=1; 1ll*i*prim[j]<=n; j++){
      vis[i*prim[j]] = 1;
      if(i%prim[j] == 0) break;
    }
  }
}
int main(){
    int n, q, k;
    scanf("%d %d", &n, &q);
    get_prim(n);
    while(q--){
        scanf("%d", &k);
        printf("%d\n", prim[k]);
    }
    return 0;
}
```
