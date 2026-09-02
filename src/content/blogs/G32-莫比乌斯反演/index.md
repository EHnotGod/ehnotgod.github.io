---
title: "G32 莫比乌斯反演"
publishDate: 2026-09-02
description: "莫比乌斯反演：μ 函数与反演公式。"
category: algo
tags:
  - 数学
language: zh
---
### 题目情境

**题目描述**

![题目：企鹅收集石头](/images/算法竞赛/G/G32/G32-1.png)

### 算法解析：

设 $F(k)$ 为选出的 $m$ 个数都能被 $k$ 整除的方案数，则 $F(k)=\binom{\lfloor n/k\rfloor}{m}$（从 $k,2k,\dots$ 中选 $m$ 个）。设 $G(k)$ 为选出的 $m$ 个数 $\gcd$ **恰等于** $k$ 的方案数，则 $F(k)=\sum_{k\mid d}G(d)$。

**莫比乌斯反演**：由 $F(k)=\sum_{k\mid d}G(d)$ 反演得 $G(k)=\sum_{k\mid d}\mu(d/k)F(d)$。本题要求 $\gcd\ne1$，即总数减去 $\gcd=1$：

$$
\text{ans}=\binom{n}{m}-\sum_{d=1}^{n}\mu(d)\binom{\lfloor n/d\rfloor}{m}
$$

其中用到了 $\sum_{d\mid g}\mu(d)=[g=1]$ 这一核心恒等式。复杂度瓶颈在线性筛求 $\mu$ 与预处理阶乘/逆元到 $n$（$O(n)$），再 $O(n)$ 求和，可过 $n\le4\times10^7$。

### C++代码：

```c++
/*EHnotgod————
..............#######.....#.....#..............
..............#...........#.....#..............
..............#######.....#######..............
..............#...........#.....#..............
..............#######.....#.....#..............
*/
#include <bits/stdc++.h>
using namespace std;
// debug 宏：在编译时定义 -DLOCAL 会启用打印，否则为 no-op
#ifdef LOCAL
template<class T> string ts(const T& v){
    stringstream ss; ss << v; return ss.str();
}
template<class A,class B> string ts(const pair<A,B>& p){ return "("+ts(p.first)+","+ts(p.second)+")"; }
template<class T> string ts(const vector<T>& v){ string s="{"; for (auto &x:v) s += ts(x)+","; return s+"}"; }
template<class T, class C, class A> string ts(const set<T,C,A>& v){ string s="{"; for (auto &x:v) s += ts(x)+","; return s+"}"; }
template<class T, class C, class A> string ts(const multiset<T,C,A>& v){ string s="{"; for (auto &x:v) s += ts(x)+","; return s+"}"; }
template<class K,class V,class C, class A> string ts(const map<K,V,C,A>& m){ string s="{"; for (auto &kv:m) s += ts(kv.first)+":"+ts(kv.second)+","; return s+"}"; }

void dbg_out(){ cerr << "\n"; }
template<class H, class...T> void dbg_out(const H& h, const T&...t){
    cerr << " " << ts(h);
    dbg_out(t...);
}
#define debug(...) cerr<<"["<<#__VA_ARGS__<<"]:",dbg_out(__VA_ARGS__)
#else
#define debug(...) 114514
#endif
#define endl "\n"
#define int long long
#define range(i, a, b) for (int i = (a); i < (b); ++i)
#define def(name, ...) auto name = [&](__VA_ARGS__)


const int N = 40000010;
const int mod = 1000000007;
int p[N], vis[N], cnt;
int mu[N];
int fac[N];
int inv[N];


int qpow(int a,int b,int p){ //快速幂
  int s=1LL;
  while(b){
    if(b&1) s=s*a%p;
    a=a*a%p;
    b>>=1LL;
  }
  return s;
}
void init(int n){
    fac[0] = 1;
    range(i, 1, n){
        fac[i] = i * fac[i - 1] % mod;
    }
    inv[n - 1] = qpow(fac[n - 1], mod - 2, mod);
    for (int i = n - 1; i > 0; i--){
        inv[i - 1] = inv[i] * i % mod;
    }
}
int comb(int n, int r){
    if (n < r){
        return 0;
    }
    int ans = fac[n] * inv[r] % mod * inv[n - r] % mod;
    return ans;
}
void get_mu(int n){//筛法求莫比乌斯函数
  mu[1] = 1;
  for(int i=2; i<=n; i++){
    if(!vis[i]){
      p[++cnt] = i;
      mu[i] = -1;
    }
    for(int j=1; i*p[j]<=n; j++){
      int m = i*p[j]; 
      vis[m] = 1;
      if(i%p[j] == 0){
        mu[m] = 0;
        break;
      } 
      else
        mu[m] = -mu[i];
    }
  }
}

// vector<int> a(n, 0);
// vector<vector<int>> dp(n + 1, vector<int>(n + 1, 0));
void solve() {
	int n, m; cin >> n >> m;
	get_mu(n + 1);
    init(n + 1);
    int ans = comb(n, m);
    range(i, 1, n + 1){
        ans -= (mu[i] * comb(n/i, m) % mod);
        ans %= mod;
    }
    cout << (ans + mod) % mod;
}

signed main() {
    ios::sync_with_stdio(0);
    cin.tie(0);
    cout.tie(0);
	int t;
	t = 1;
	while (t--) {
		solve();
	}
	return 0;
}
```