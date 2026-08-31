---
title: "G57 自适应辛普森积分"
publishDate: 2026-08-08
description: "自适应辛普森积分：数值积分求面积。"
category: algo
tags:
  - 数学
language: zh
---
### 题目情境

题目链接：https://www.luogu.com.cn/problem/P4525

**题目描述**

求 $\int_L^R \frac{cx+d}{ax+b}\,dx$，输出 6 位小数。

**说明/提示**

本页为算法笔记。

### 算法解析：

自适应辛普森积分：用辛普森公式 $\int_l^r f\approx\frac{r-l}{6}(f(l)+4f(m)+f(r))$ 近似积分。递归比较区间整体与左右两半辛普森值的差，误差小于 $\epsilon$ 时停止，否则递归细分。适用于无法解析积分的一般函数。

### 备注

![image-20251010102351335](/images/算法竞赛/G/G57-1.png)

P4525 【模板】自适应辛普森法 1

**题目描述**

试计算积分

$$\displaystyle{\int_L^R\frac{cx+d}{ax+b}\mathrm{d}x}$$

结果保留至小数点后 $$6$$ 位。

数据保证计算过程中分母不为 $$0$$ 且积分能够收敛。

**输入格式**

一行，包含 $$6$$ 个实数 $$a,b,c,d,L,R$$。

**输出格式**

一行，积分值，保留至小数点后 $$6$$ 位。

输入 #1

```
1 2 3 4 5 6
```

输出 #1

```
2.732937
```

$$a,b,c,d\in[-10,10]$$，$$-100\le L<R\le 100$$ 且 $$R-L\ge1$$。

时间复杂度：$${O(log(n / eps))}$$

### C++代码实现

```c++
#include <iostream>
#include <cstring>
#include <algorithm>
#include <cmath>
using namespace std;

const double eps=1e-10;
double a,b,c,d,l,r;

double f(double x){ //积分函数
  return (c*x+d)/(a*x+b);
}
double simpson(double l,double r){//辛普森公式
  return (r-l)*(f(l)+f(r)+4*f((l+r)/2))/6;
}
double asr(double l,double r,double ans){//自适应
  auto m=(l+r)/2,a=simpson(l,m),b=simpson(m,r);
  if(fabs(a+b-ans)<eps) return ans;
  return asr(l,m,a)+asr(m,r,b);
}
int main(){
  scanf("%lf%lf%lf%lf%lf%lf",&a,&b,&c,&d,&l,&r);
  printf("%.6lf",asr(l,r,simpson(l,r)));
  return 0;
}
```
