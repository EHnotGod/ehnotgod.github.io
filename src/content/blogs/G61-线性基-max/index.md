---
title: "G61 线性基-max"
publishDate: 2026-08-08
description: "线性基：求最大异或和。"
category: algo
tags:
  - 数学
language: zh
---
### 题目情境

题目链接：https://www.luogu.com.cn/problem/P3812

**题目描述**

给定 $n$ 个数，求其中任意多个数异或的最大值。

**说明/提示**

本页为算法笔记。

### 算法解析：

线性基求最大异或和：把每个数从高位到低位插入线性基，若当前位已有基向量则异或消去，否则放入。构造后用贪心：从高位到低位，若异或该基向量能使结果变大则异或，累加得最大异或和。复杂度 $O(63n)$。

### 备注

P3812 【模板】线性基

**题目描述**

给定 $$n$$ 个整数（数字可能重复），求在这些数中选取任意个，使得他们的异或和最大。

**输入格式**

第一行一个数 $$n$$，表示元素个数

接下来一行 $$n$$ 个数

**输出格式**

仅一行，表示答案。

输入 #1

```
2
1 1
```

输出 #1

```
1
```

输入 #2

```
4
1 5 9 4
```

输出 #2

```
13
```

$$ 1 \leq n \leq 50, 0 \leq S_i < 2 ^ {50} $$

### C++代码实现

```c++
// 线性基 O(63*n)
#include <iostream>
#include <cstring>
#include <algorithm>
using namespace std;

typedef long long LL;
int n,k;
LL p[64];

void gauss(){ //高斯消元法
  for(int i=63;i>=0;i--){
    // 把当前第i位是1的数换上去
    for(int j=k;j<n;j++)
      if(p[j]>>i&1){swap(p[j],p[k]); break;}
    // 当前第i位所有向量都是0
    if((p[k]>>i&1)==0) continue;
    // 把其他数的第i位全部消为0
    for(int j=0;j<n;j++)
      if(j!=k&&(p[j]>>i&1)) p[j]^=p[k];
    // 基的个数+1
    k++; if(k==n) break;
  }
}
int main(){
  scanf("%d",&n);
  for(int i=0;i<n;i++)scanf("%lld",&p[i]);
  gauss();
  LL ans=0;
  for(int i=0;i<k;i++) ans^=p[i];
  printf("%lld\n",ans);
}
```
