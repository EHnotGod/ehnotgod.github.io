---
title: "G9 欧拉函数"
publishDate: 2026-08-08
description: "欧拉函数：1~n 中与 n 互质的数个数。"
category: algo
tags:
  - 数学
language: zh
---
### 题目情境

**题目描述**

题目链接：https://www.luogu.com.cn/problem/U629802

欧拉函数就是小于 $x$ 的正整数中与 $x$ 互质的数的个数，一般用 $φ(x)$ 表示。特殊的，$φ(1)=1$。

现在需要你求出 $1-n$ 的欧拉函数。

**输入格式**

输入一行一个整数 $n$。

**输出格式**

输出一行 $n$ 个整数表示 $1-n$ 的欧拉函数，用空格分隔。

输入 #1

```
10
```

输出 #1

```
1 1 2 2 4 2 6 4 6 4
```

对于 $100\%$ 的数据，保证 $1≤n≤2×10^6$。

### 算法解析：

线性筛求欧拉函数：$\varphi(1)=1$；质数 $p$ 的 $\varphi(p)=p-1$；对合数 $m=i\cdot p$：若 $p\mid i$ 则 $\varphi(m)=p\cdot\varphi(i)$，否则 $\varphi(m)=(p-1)\cdot\varphi(i)$。用数组 $\varphi$ 记录并输出。复杂度 $O(n)$。

### Python代码实现

```python
import sys

def get_phi(n):
    phi = [0] * (n + 1)
    vis = [False] * (n + 1)
    primes = []
    phi[1] = 1
    for i in range(2, n + 1):
        if not vis[i]:
            primes.append(i)
            phi[i] = i - 1
        for p in primes:
            m = i * p
            if m > n:
                break
            vis[m] = True
            if i % p == 0:
                # p | i
                phi[m] = p * phi[i]
                break
            else:
                phi[m] = (p - 1) * phi[i]
    return phi

data = sys.stdin.read().split()
n = int(data[0])
phi = get_phi(n)
# 输出 1..n
out = ' '.join(str(phi[i]) for i in range(1, n + 1))
sys.stdout.write(out)
```

### C++代码实现

```c++
#include <iostream>
using namespace std;

const int N = 1000010;
int p[N], vis[N], cnt;
int phi[N];

void get_phi(int n){//筛法求欧拉函数
  phi[1] = 1;
  for(int i=2; i<=n; i++){
    if(!vis[i]){
      p[cnt++] = i;
      phi[i] = i-1;
    }
    for(int j=0; i*p[j]<=n; j++){
      int m = i*p[j];
      vis[m] = 1;
      if(i%p[j] == 0){
        phi[m] = p[j]*phi[i];
        break;
      }
      else
        phi[m]=(p[j]-1)*phi[i];
    }
  }
}
int main(){
  int n;
  cin >> n;
  get_phi(n);
  for(int i=1; i<=n; i++)
    printf("%d ", phi[i]);
  return 0;
}
```
