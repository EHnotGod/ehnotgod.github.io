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

### 算法解析：

线性基求最大异或和：把每个数从高位到低位插入线性基，若当前位已有基向量则异或消去，否则放入。构造后用贪心：从高位到低位，若异或该基向量能使结果变大则异或，累加得最大异或和。复杂度 $O(63n)$。

看这个原始 $x$ 最后能不能成功插入线性基。

### C++代码实现

```c++
// 线性基 O(63*n)
#include <iostream>
#include <cstring>
#include <algorithm>
using namespace std;

typedef long long LL;
int n;
LL p[64];

void insert(LL x){ //贪心法
  for(int i=63;i>=0;--i){
    if(x>>i&1){  //x第i位为1
      if(!p[i]){ //不存在则加入
        p[i]=x; 
        break;
      }
      x^=p[i];   //存在则异或
    }
  }
}
int main(){
  scanf("%d",&n);
  for(int i=0;i<n;i++){
    LL x; scanf("%lld",&x);
    insert(x);
  }
  LL ans=0;
  for(int i=63;i>=0;i--) ans=max(ans,ans^p[i]);
  printf("%lld\n",ans);
}
```
