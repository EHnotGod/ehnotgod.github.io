---
title: "G41 FFT-多项式乘法"
categories:
- [算法, G 数学]
tags:
- 数学
---

### 题目情境

**题目描述**

给定一个 $n$ 次多项式 $F(x)$，和一个 $m$ 次多项式 $G(x)$。

请求出 $F(x)$ 和 $G(x)$ 的乘积。

**输入格式**

第一行两个整数 $n,m$。

接下来一行 $n+1$ 个数字，从低到高表示 $F(x)$ 的系数。

接下来一行 $m+1$ 个数字，从低到高表示 $G(x)$ 的系数。

**输出格式**

一行 $n+m+1$ 个数字，从低到高表示 $F(x) \cdot G(x)$ 的系数。

输入 #1

```
1 2
1 2
1 2 1
```

输出 #1

```
1 4 5 2
```

**说明/提示**

保证输入中的系数大于等于 $0$ 且小于等于 $9$。

对于 $100\%$ 的数据：$1 \le n, m \leq {10}^6$。

**有没有讲解？没有，会用就行了！！！！**

### C++代码实现

```c++
// 迭代版 1.5s
#include <iostream>
#include <cstring>
#include <algorithm>
#include <cmath>
using namespace std;
const int N=4e6;
const double PI=acos(-1);

struct complex{
  double x, y;
  complex operator+(const complex& t)const{
    return {x+t.x, y+t.y};}
  complex operator-(const complex& t)const{
    return {x-t.x, y-t.y};}
  complex operator*(const complex& t)const{
    return {x*t.x-y*t.y, x*t.y+y*t.x};}
}A[N], B[N];
int R[N];

void FFT(complex A[],int n,int op){
  for(int i=0; i<n; ++i)
    R[i] = R[i/2]/2 + ((i&1)?n/2:0);
  for(int i=0; i<n; ++i)
    if(i<R[i]) swap(A[i],A[R[i]]);
  for(int i=2; i<=n; i<<=1){
    complex w1({cos(2*PI/i),sin(2*PI/i)*op});
    for(int j=0; j<n; j+=i){
      complex wk({1,0});
      for(int k=j; k<j+i/2; ++k){
        complex x=A[k], y=A[k+i/2]*wk;
        A[k]=x+y; A[k+i/2]=x-y;
        wk=wk*w1;
      }
    }
  }
}
int main(){
  int n,m;
  scanf("%d%d", &n, &m);
  for(int i=0; i<=n; i++)scanf("%lf", &A[i].x);
  for(int i=0; i<=m; i++)scanf("%lf", &B[i].x);
  for(m=n+m,n=1;n<=m;n<<=1);
  FFT(A,n,1); FFT(B,n,1);
  for(int i=0;i<n;++i)A[i]=A[i]*B[i];
  FFT(A,n,-1);
  for(int i=0;i<=m;++i)
    printf("%d ",(int)(A[i].x/n+0.5));
}
```
