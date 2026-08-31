---
title: "G20 扩展中国剩余定理"
publishDate: 2026-08-08
description: "扩展中国剩余定理：模数不互质的同余方程组。"
category: algo
tags:
  - 数学
language: zh
---
### 题目情境

题目链接：https://www.luogu.com.cn/problem/P4777

**题目描述**

给定 $n$ 组非负整数 $a_i, b_i$ ，求解关于 $x$ 的方程组的最小非负整数解。
$$\begin{cases}x\equiv b_1\pmod{a_1}\\x\equiv b_2\pmod{a_2}\\\dots\\x\equiv b_n\pmod{a_n}\end{cases}$$

**输入格式**

输入第一行包含整数 $n$。

接下来 $n$ 行，每行两个非负整数 $a_i, b_i$。

**输出格式**

输出一行，为满足条件的最小非负整数 $x$。

输入 #1

```
3
11 6
25 9
33 17

```

输出 #1

```
809
```

**说明/提示**

对于 $100 \%$ 的数据，$1 \le n \le {10}^5$，$1 \le a_i \le {10}^{12}$，$0\leq b_i \leq 10^{12}$，保证所有 $a_i$ 的最小公倍数不超过 ${10}^{18}$。

### 算法解析：

![image-20250808181543528](/images/算法竞赛/G/G20-1.png)

扩展中国剩余定理（EXCRT）：模数不互质时两两合并。对 $x\equiv r_1\pmod{m_1}$ 与 $x\equiv r_2\pmod{m_2}$，解 $m_1p+m_2q=\gcd$，若 $(r_2-r_1)\%d\ne0$ 无解；否则得特解并合并为 $x\equiv r'\pmod{\operatorname{lcm}(m_1,m_2)}$。逐对合并到只剩一个同余式。

### Python代码实现

```python
def exgcd(a, b):
    if b == 0:
        return a, 1, 0
    d, x1, y1 = exgcd(b, a % b)
    x = y1
    y = x1 - a // b * y1
    return d, x, y

def EXCRT(m, r):
    m1 = m[1]
    r1 = r[1]
    for i in range(2, n + 1):
        m2 = m[i]
        r2 = r[i]
        d, p, q = exgcd(m1, m2)
        # 不可整除则无解
        if (r2 - r1) % d != 0:
            return -1
        # 求一个特解并取模
        p = p * ((r2 - r1) // d)
        p = p % (m2 // d)
        r1 = m1 * p + r1
        m1 = m1 * (m2 // d)
    return r1 % m1

if __name__ == "__main__":
    n = int(input().strip())
    m = [0] * (n + 1)
    r = [0] * (n + 1)
    for i in range(1, n + 1):
        mi, ri = map(int, input().split())
        m[i] = mi
        r[i] = ri
    print(EXCRT(m, r))
```

### C++代码实现

```c++
#include <iostream>
#include <cstring>
#include <algorithm>
using namespace std;

typedef __int128 LL;
const int N = 100005;
LL n, m[N], r[N];

LL exgcd(LL a,LL b,LL &x,LL &y){
  if(b==0){x=1, y=0; return a;}
  LL d, x1, y1;
  d = exgcd(b, a%b, x1, y1);
  x = y1, y = x1-a/b*y1;
  return d;
}
LL EXCRT(LL m[], LL r[]){
  LL m1, m2, r1, r2, p, q;
  m1 = m[1], r1 = r[1];
  for(int i=2; i<=n; i++){
    m2 = m[i], r2 = r[i];
    LL d = exgcd(m1,m2,p,q);
    if((r2-r1)%d){return -1;}
    p=p*(r2-r1)/d; //特解
    p=(p%(m2/d)+m2/d)%(m2/d);
    r1 = m1*p+r1;
    m1 = m1*m2/d;
  }
  return (r1%m1+m1)%m1;
}
int main(){
  scanf("%lld", &n);
  for(int i = 1; i <= n; ++i)
    scanf("%lld%lld", m+i, r+i);
  printf("%lld\n",EXCRT(m,r));
  return 0;
}
```
