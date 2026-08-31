---
title: "G24 矩阵求逆-高斯约旦消元法"
publishDate: 2026-08-08
description: "高斯-约旦消元求矩阵逆。"
category: algo
tags:
  - 数学
language: zh
---
### 题目情境

题目链接：https://www.luogu.com.cn/problem/P4783

**题目描述**

求一个 $N\times N$ 的矩阵的逆矩阵。答案对 ${10}^9+7$ 取模。

**输入格式**

第一行有一个整数 $N$，代表矩阵的大小；

接下来 $N$ 行，每行 $N$ 个整数，其中第 $i$ 行第 $j$ 列的数代表矩阵中的元素 $a_{i j}$。

**输出格式**

若矩阵可逆，则输出 $N$ 行，每行 $N$ 个整数，其中第 $i$ 行第 $j$ 列的数代表逆矩阵中的元素 $b_{i j}$，答案对 ${10}^9+7$ 取模；

否则只输出一行 `No Solution`。

输入 #1

```
3
1 2 8
2 5 6
5 1 2
```

输出 #1

```
718750005 718750005 968750007
171875001 671875005 296875002
117187501 867187506 429687503
```

输入 #2

```
3
3 2 4
7 2 9
2 4 3
```

输出 #2

```
No Solution
```
对 $100 \%$ 的数据有 $N\le 400$，所有 $0 \le a_{i j} < {10}^9 + 7$。

### 算法解析：

高斯-约旦消元求逆：在 $A$ 右侧拼单位矩阵成 $[A\mid I]$，逐列选非零主元（$\bmod$ 下用逆元），把主元行归一化并消去**其他所有行**的当前列，使左侧变为单位矩阵，右侧即 $A^{-1}$。主元为 0 则不可逆。复杂度 $O(n^3)$。

![image-20251113091739495](/images/算法竞赛/G/G24-1.png)

时间复杂度：$$O(n^3)$$

### C++代码实现

```c++
#include<iostream>
#include<cstdio>
#include<cmath>
#define LL long long
using namespace std;

const int N=405,P=1e9+7;
int n;
LL a[N][N<<1];

LL quickpow(LL a, LL b){
  LL ans = 1;
  while(b){
    if(b & 1) ans = ans*a%P;
    a = a*a%P;
    b >>= 1;
  }
  return ans;
}
bool Gauss_Jordan(){    
  for(int i=1;i<=n;++i){ //枚举主元的行列
    int r = i;
    for(int k=i; k<=n; ++k) //找非0行
      if(a[k][i]) {r=k; break;}
    if(r!=i) swap(a[r],a[i]); //换行
    if(!a[i][i]) return 0;  
    
    int x=quickpow(a[i][i],P-2); //求逆元
    for(int k=1; k<=n; ++k){ //对角化
      if(k == i) continue;
      int t=a[k][i]*x%P;
      for(int j=i; j<=2*n; ++j) 
        a[k][j]=((a[k][j]-t*a[i][j])%P+P)%P;
    } 
    for(int j=1; j<=2*n; ++j) //除以主元
      a[i][j]=(a[i][j]*x%P);
  }
  return 1;
}
int main(){
  scanf("%d",&n);
  for(int i=1; i<=n; ++i)
    for(int j=1; j<=n; ++j)
      scanf("%lld",&a[i][j]),a[i][i+n]=1;
  if(Gauss_Jordan())
    for(int i=1; i<=n; ++i){
      for(int j=n+1; j<=2*n; ++j) 
        printf("%lld ",a[i][j]);
      puts("");
    }
  else puts("No Solution");
  return 0;
}
```
