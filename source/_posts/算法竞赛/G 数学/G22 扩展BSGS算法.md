---
title: "G22 扩展BSGS算法"
categories:
- [算法, G 数学]
tags:
- 数学
---

### 题目情境

![image-20250808181703985](/images/算法竞赛/G/G22-1.png)

时间复杂度：${O(\sqrt{p})}$

### Python代码实现

```python
import math

def gcd(a, b):
    return a if b == 0 else gcd(b, a % b)

def exbsgs(a, b, p):
    a %= p
    b %= p
    if b == 1 or p == 1:
        return 0  # x = 0

    # 处理 gcd 除掉公共因子
    k = 0
    A = 1 % p
    while True:
        d = gcd(a, p)
        if d == 1:
            break
        if b % d != 0:
            return -1
        k += 1
        b //= d
        p //= d
        A = (A * (a // d)) % p
        if A == b:
            return k

    # baby-step giant-step
    m = math.isqrt(p)
    if m * m < p:
        m += 1

    t = b % p
    table = {t: 0}
    for j in range(1, m):
        t = (t * a) % p
        table[t] = j

    mi = pow(a, m, p)  # a^m % p
    t = A % p
    for i in range(1, m + 1):
        t = (t * mi) % p
        if t in table:
            return i * m - table[t] + k

    return -1

# 使用 input() 逐个 token 读取（可处理不同换行/空格的输入格式）
def tokens():
    while True:
        try:
            for tok in input().split():
                yield tok
        except EOFError:
            return

if __name__ == "__main__":
    it = tokens()
    while True:
        try:
            a = int(next(it))
            p = int(next(it))
            b = int(next(it))
        except StopIteration:
            break
        if a == 0:
            break
        res = exbsgs(a, b, p)
        if res == -1:
            print("No Solution")
        else:
            print(res)
```

### C++代码实现

```c++
#include <iostream>
#include <cstring>
#include <algorithm>
#include <cmath>
#include <unordered_map>
using namespace std;

typedef long long LL;

LL gcd(LL a, LL b){
  return b==0?a:gcd(b,a%b);
}
LL exbsgs(LL a, LL b, LL p){
  a %= p; b %= p;
  if(b==1||p==1)return 0;//x=0

  LL d, k=0, A=1;
  while(true){
    d = gcd(a,p);
    if(d==1) break;
    if(b%d) return -1; //无解
    k++; b/=d; p/=d;
    A = A*(a/d)%p; //求a^k/D
    if(A==b) return k;
  }

  LL m=ceil(sqrt(p));
  LL t = b;
  unordered_map<int,int> hash;
  hash[b] = 0;
  for(int j = 1; j < m; j++){
    t = t*a%p; //求b*a^j
    hash[t] = j;
  }
  LL mi = 1;
  for(int i = 1; i <= m; i++)
    mi = mi*a%p; //求a^m
  t = A;
  for(int i=1; i <= m; i++){
    t = t*mi%p; //求(a^m)^i
    if(hash.count(t))
      return i*m-hash[t]+k;
  }
  return -1; //无解
}
int main(){
  LL a, p, b;
  while((scanf("%lld%lld%lld",&a,&p,&b)!=EOF)&&a){
    LL res = exbsgs(a, b, p);
    if(res == -1) puts("No Solution");
    else printf("%lld\n",res);
  }
  return 0;
}
```
