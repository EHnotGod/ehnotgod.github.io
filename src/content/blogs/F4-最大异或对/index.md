---
title: "F4 最大异或对"
publishDate: 2026-08-08
description: "Trie + 贪心：求最大异或对。"
category: algo
tags:
  - 字符串
language: zh
---

### 题目情境

题目链接：https://www.luogu.com.cn/problem/P10471

**题目描述**

给定 $n$ 个整数 $a_1\sim a_n$，任选两个数 $a_i, a_j\ (i\ne j)$，求它们的按位异或 $a_i\oplus a_j$ 的最大值。

**输入格式**

第一行一个整数 $n$。

第二行 $n$ 个整数 $a_1\sim a_n$。

**输出格式**

一个整数，表示最大异或值。

**说明/提示**

数据保证 $1\le n\le 10^5$，$0\le a_i<2^{31}$。

### 算法解析：

01 Trie + 贪心：把每个数从高位到低位插入 01 Trie（31 位）。查询一个数 $x$ 的最大异或时，从高位开始尽量走与当前位相反的边（$1-j$），使异或结果当前位为 1，累加 $2^i$；无相反边则走相同边。对每个数查询取最大值。插入、查询均 $O(31)$，总复杂度 $O(31n)$。

### Python代码实现

```python
ch = [[0, 0]]  # 初始化Trie树，根节点为0

def insert(x):
    p = 0
    for i in range(30, -1, -1):
        j = (x >> i) & 1
        if ch[p][j] == 0:
            ch.append([0, 0])  # 创建新节点
            ch[p][j] = len(ch) - 1  # 更新指针到新节点
        p = ch[p][j]

def query(x):
    p = 0
    res = 0
    for i in range(30, -1, -1):
        j = (x >> i) & 1
        opposite = 1 - j
        if ch[p][opposite]:
            res += (1 << i)
            p = ch[p][opposite]
        else:
            p = ch[p][j]
    return res

n = int(input())
a = list(map(int, input().split()))
for num in a:
    insert(num)
ans = 0
for num in a:
    ans = max(ans, query(num))
print(ans)
```

### C++代码实现

```c++
// 01Trie 最大异或对
#include <iostream>
using namespace std;

const int N=100010;
int n, a[N];
int ch[N*31][2],cnt;

void insert(int x){
  int p=0;
  for(int i=30; i>=0; i--){
    int j=x>>i&1; //取出第i位
    if(!ch[p][j])ch[p][j]=++cnt;
    p=ch[p][j];
  }
}
int query(int x){
  int p=0,res=0;
  for(int i=30; i>=0; i--){
    int j=x>>i&1;
    if(ch[p][!j]){
      res += 1<<i; //累加位权
      p=ch[p][!j];
    }
    else p=ch[p][j];
  }
  return res;
}
int main(){
  cin>>n;
  for(int i=1; i<=n; i++)
    cin>>a[i],insert(a[i]);
  int ans=0;
  for(int i=1; i<=n; i++)
    ans=max(ans,query(a[i]));
  cout<<ans;
  return 0;
}
```
