---
title: "G61 线性基-max"
categories:
- [算法, G 数学]
tags:
- 数学
---

### 题目情境

P3812 【模板】线性基

**题目描述**

给定 $n$ 个整数（数字可能重复），求在这些数中选取任意个，使得他们的异或和最大。

**输入格式**

第一行一个数 $n$，表示元素个数

接下来一行 $n$ 个数

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

$ 1 \leq n \leq 50, 0 \leq S_i < 2 ^ {50} $

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
