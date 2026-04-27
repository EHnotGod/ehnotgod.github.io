---
title: "G99 超级gcd"
categories:
- [算法, G 数学]
tags:
- 数学
---

### 题目情境

![image-20250808230643738](/images/算法竞赛/G/G99-1.png)

## H 邪教

### Python代码实现

```python
import sys
import threading
import math

MOD = 998244353
PHI = MOD - 1  # 欧拉函数 phi(998244353)

def qmi(a, k):
    res = 1
    a %= MOD
    while k:
        if k & 1:
            res = res * a % MOD
        a = a * a % MOD
        k >>= 1
    return res

def dfs(a, b, c, d):
    g = math.gcd(a, c)
    if g == 1:
        return 1
    minv = min(b, d)
    if b <= d:
        exp = b if b < PHI else b % PHI + PHI
        return qmi(g, exp) * dfs(a // g, b, g, d - b) % MOD
    else:
        exp = d if d < PHI else d % PHI + PHI
        return qmi(g, exp) * dfs(g, b - d, c // g, d) % MOD

def main():
    T = int(sys.stdin.readline())
    for _ in range(T):
        a, b, c, d = map(int, sys.stdin.readline().split())
        print(dfs(a, b, c, d))

threading.Thread(target=main).start()
```

### C++代码实现

```c++
#include "bits/stdc++.h"
using namespace std;
using ll = long long;
using lll = __int128;
#define all(x) (x).begin(),(x).end()
const ll p = 998244353;
ll ksm(ll x, lll Y)
{
	ll r = 1;
	x %= p;
	if (!Y) return 1;
	if (!x) return 0;
	ll y = Y % (p - 1);
	while (y)
	{
		if (y & 1) r = r * x % p;
		x = x * x % p; y >>= 1;
	}
	return r;
}
ll f(ll a, lll b, ll c, lll d)
{
	ll x = gcd(a, c);
	if (x == 1 || b == 0 || d == 0) return 1;
	lll ka = 0, kc = 0;
	while (a % x == 0) a /= x, ++ka;
	while (c % x == 0) c /= x, ++kc;
	ka *= b, kc *= d;
	if (ka > kc) swap(a, c), swap(b, d), swap(ka, kc);
	return ksm(x, ka) * f(a, b, x, kc - ka) % p;
}
int main()
{
	ios::sync_with_stdio(0);
	cin.tie(0);
	int T;
	cin >> T;
	while (T--)
	{
		ll a, b, c, d;
		cin >> a >> b >> c >> d;
		cout << f(a, b, c, d) << '\n';
	}
}
```
