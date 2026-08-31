---
title: "G5 gcd及lcm问题"
publishDate: 2026-08-08
description: "gcd / lcm：欧几里得算法及相关性质。"
category: algo
tags:
  - 数学
language: zh
---
### 题目情境

题目链接：https://www.luogu.com.cn/problem/P1029

**题目描述**

给定 $x,y$，求有多少对正整数 $(p,q)$ 满足 $\gcd(p,q)=x$ 且 $\operatorname{lcm}(p,q)=y$。

**说明/提示**

本页为算法笔记。

### 算法解析：

利用性质 $\gcd(p,q)\cdot\operatorname{lcm}(p,q)=p\cdot q$：令 $t=x\cdot y$，枚举 $i$ 满足 $i\mid t$ 且 $\gcd(i,t/i)=x$，则 $(i,t/i)$ 为一组解，对称计数加 2；$x=y$ 时去掉重复的一次。复杂度 $O(\sqrt{t})$。

### Python代码实现

```python
# P1029 [NOIP 2001 普及组] 最大公约数和最小公倍数问题
import math
x, y = map(int, input().split())
t = x * y
ans = 0
for i in range(1, int(t ** 0.5) + 1):
    if t % i == 0 and math.gcd(t // i, i) == x:
        ans += 2
if x == y:
    ans -= 1
print(ans)
```

### C++代码实现

```c++
#include <iostream>
#include <cstring>
#include <algorithm>
using namespace std;

typedef long long LL;
LL x,y,ans;

LL gcd(LL a, LL b){
  return b==0 ? a : gcd(b,a%b);
}
int main(){
    cin>>x>>y;
    LL t = x*y;
    for(LL i=1; i*i<=t; i++)
        if(t%i==0 && gcd(i,t/i)==x)
          ans += 2;
    if(x==y) ans--;
    cout << ans;
    return 0;
}
```
