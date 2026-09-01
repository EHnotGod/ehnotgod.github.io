---
title: "G18 卡特兰数"
publishDate: 2026-08-08
description: "卡特兰数：入栈出栈 / 括号匹配等计数。"
category: algo
tags:
  - 数学
language: zh
---
### 题目情境

题目链接：https://www.luogu.com.cn/problem/P1044

**题目描述**

![](https://cdn.luogu.com.cn/upload/image_hosting/5qxy9fz2.png)

宁宁考虑的是这样一个问题：一个操作数序列，$1,2,\ldots ,n$（图示为 1 到 3 的情况），栈 A 的深度大于 $n$。

现在可以进行两种操作，

1. 将一个数，从操作数序列的头端移到栈的头端（对应数据结构栈的 push 操作）
2. 将一个数，从栈的头端移到输出序列的尾端（对应数据结构栈的 pop 操作）

使用这两种操作，由一个操作数序列就可以得到一系列的输出序列，下图所示为由 `1 2 3` 生成序列 `2 3 1` 的过程。

![](https://cdn.luogu.com.cn/upload/image_hosting/8uwv2pa2.png)

（原始状态如上图所示）

你的程序将对给定的 $n$，计算并输出由操作数序列 $1,2,\ldots,n$ 经过操作可能得到的输出序列的总数。

**输入格式**

输入文件只含一个整数 $n$（$1 \leq n \leq 18$）。

**输出格式**

输出文件只有一行，即可能输出序列的总数目。

输入 #1

```
3

```

输出 #1

```
5

```

### 算法解析：

卡特兰数：$Cat_n=\frac{1}{n+1}C(2n,n)=\sum_{i=0}^{n-1}Cat_i\cdot Cat_{n-1-i}$，$Cat_0=1$。计数对象包括：$n$ 对括号合法序列、$n$ 个元素入栈出栈序列、$n$ 个节点二叉树形态、凸多边形三角剖分数等。递推式 $Cat_{n+1}=\frac{4n+2}{n+2}Cat_n$。

![image-20250808223834012](/images/算法竞赛/G/G18-1.png)

### C++代码

```c++
#include <iostream>
using namespace std;

int n;
long long f[20];

int main(){
  cin >> n;
  f[0] = 1;
  for(int i = 1; i <= n; i++) 
    f[i] = f[i-1]*(4*i-2)/(i+1);
  cout << f[n] << endl;
  return 0;
}
```