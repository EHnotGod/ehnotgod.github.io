---
title: "C5 加乘线段树"
publishDate: 2026-08-08
description: "线段树进阶：区间加法与乘法混合懒标记。"
category: algo
tags:
  - 数据结构
language: zh
---

### 题目情境

题目链接：https://www.luogu.com.cn/problem/P3373

**题目描述**

如题，已知一个数列 $$a$$，你需要进行下面三种操作：

- 将某区间每一个数乘上 $$x$$；
- 将某区间每一个数加上 $$x$$；
- 求出某区间每一个数的和。

**输入格式**

第一行包含三个整数 $$n,q,m$$，分别表示该数列数字的个数、操作的总个数和模数。

第二行包含 $$n$$ 个用空格分隔的整数，其中第 $$i$$ 个数字表示数列第 $$i$$ 项的初始值 $$a_i$$。

接下来 $$q$$ 行每行包含若干个整数，表示一个操作，具体如下：

操作 $$1$$： 格式：`1 x y k`  含义：将区间 $$[x,y]$$ 内每个数乘上 $$k$$。

操作 $$2$$： 格式：`2 x y k`  含义：将区间 $$[x,y]$$ 内每个数加上 $$k$$。

操作 $$3$$： 格式：`3 x y`  含义：输出区间 $$[x,y]$$ 内每个数的和对 $$m$$ 取模所得的结果。

**输出格式**

输出包含若干行整数，即为所有操作 $$3$$ 的结果。

输入 #1

```
5 5 38
1 5 4 2 3
2 1 4 1
3 2 5
1 2 4 2
2 3 5 5
3 1 4
```

输出 #1

```
17
2
```

【数据范围】对于 $$100\%$$ 的数据：$$1 \le n \le 10^5$$，$$1 \le q \le 10^5,1\le a_i,k\le 10^4$$。

### 算法解析

![](/images/算法竞赛/C/C5-1.png)

### py代码实现

有两种实现：第一种是class的，跟C++格式一样，但是常数比较大；第二种是直接全局数组接管的，快多了。

**第一种：**

```python
import sys
input = sys.stdin.readline

class Tree:
    def __init__(self):
        self.l = self.r = self.sum = self.add = 0
        self.mul = 1

class SegmentTree:
    def __init__(self, w, mod):
        self.n, self.w, self.mod = len(w) - 1, w, mod
        self.tr = [Tree() for _ in range(self.n * 4 + 5)]
        self.build(1, 1, self.n)

    def lc(self, u): return u << 1
    def rc(self, u): return u << 1 | 1
    def length(self, u): return self.tr[u].r - self.tr[u].l + 1

    def pushup(self, u):
        self.tr[u].sum = (self.tr[self.lc(u)].sum + self.tr[self.rc(u)].sum) % self.mod

    def apply(self, u, mulv, addv):
        mulv %= self.mod; addv %= self.mod
        self.tr[u].sum = (self.tr[u].sum * mulv + addv * self.length(u)) % self.mod
        self.tr[u].mul = self.tr[u].mul * mulv % self.mod
        self.tr[u].add = (self.tr[u].add * mulv + addv) % self.mod

    def pushdown(self, u):
        if self.tr[u].mul != 1 or self.tr[u].add != 0:
            self.apply(self.lc(u), self.tr[u].mul, self.tr[u].add)
            self.apply(self.rc(u), self.tr[u].mul, self.tr[u].add)
            self.tr[u].mul, self.tr[u].add = 1, 0

    def build(self, u, l, r):
        self.tr[u].l, self.tr[u].r = l, r
        if l == r:
            self.tr[u].sum = self.w[l] % self.mod
            return
        mid = (l + r) >> 1
        self.build(self.lc(u), l, mid)
        self.build(self.rc(u), mid + 1, r)
        self.pushup(u)

    def change(self, u, l, r, k):  # 区间加
        if l <= self.tr[u].l and self.tr[u].r <= r:
            self.apply(u, 1, k); return
        mid = (self.tr[u].l + self.tr[u].r) >> 1
        self.pushdown(u)
        if l <= mid: self.change(self.lc(u), l, r, k)
        if r > mid: self.change(self.rc(u), l, r, k)
        self.pushup(u)

    def change2(self, u, l, r, k):  # 区间乘
        if l <= self.tr[u].l and self.tr[u].r <= r:
            self.apply(u, k, 0); return
        mid = (self.tr[u].l + self.tr[u].r) >> 1
        self.pushdown(u)
        if l <= mid: self.change2(self.lc(u), l, r, k)
        if r > mid: self.change2(self.rc(u), l, r, k)
        self.pushup(u)

    def query(self, u, l, r):
        if l <= self.tr[u].l and self.tr[u].r <= r: return self.tr[u].sum
        mid = (self.tr[u].l + self.tr[u].r) >> 1
        self.pushdown(u)
        ans = 0
        if l <= mid: ans += self.query(self.lc(u), l, r)
        if r > mid: ans += self.query(self.rc(u), l, r)
        return ans % self.mod

n, m, mod = map(int, input().split())
w = [0] + list(map(int, input().split()))
seg = SegmentTree(w, mod)

for _ in range(m):
    op = list(map(int, input().split()))
    if op[0] == 1: seg.change2(1, op[1], op[2], op[3])
    elif op[0] == 2: seg.change(1, op[1], op[2], op[3])
    else: print(seg.query(1, op[1], op[2]))
```

```python
import sys
input = sys.stdin.readline

n, m, mod = map(int, input().split())
w = [0] + list(map(int, input().split()))
N = 4 * n + 5
L = [0] * N
R = [0] * N
SUM = [0] * N
ADD = [0] * N
MUL = [1] * N

def length(u):
    return R[u] - L[u] + 1

def pushup(u):
    SUM[u] = (SUM[u << 1] + SUM[u << 1 | 1]) % mod

def apply(u, mulv, addv):
    mulv %= mod; addv %= mod
    SUM[u] = (SUM[u] * mulv + addv * length(u)) % mod
    MUL[u] = MUL[u] * mulv % mod
    ADD[u] = (ADD[u] * mulv + addv) % mod

def pushdown(u):
    if MUL[u] == 1 and ADD[u] == 0: return
    apply(u << 1, MUL[u], ADD[u])
    apply(u << 1 | 1, MUL[u], ADD[u])
    MUL[u] = 1; ADD[u] = 0

def build(u, l, r):
    L[u] = l; R[u] = r
    if l == r:
        SUM[u] = w[l] % mod
        return
    mid = (l + r) >> 1
    build(u << 1, l, mid); build(u << 1 | 1, mid + 1, r)
    pushup(u)

def change(u, l, r, k):
    if l <= L[u] and R[u] <= r:
        apply(u, 1, k)
        return
    pushdown(u); mid = (L[u] + R[u]) >> 1
    if l <= mid: change(u << 1, l, r, k)
    if r > mid: change(u << 1 | 1, l, r, k)
    pushup(u)

def change2(u, l, r, k):
    if l <= L[u] and R[u] <= r:
        apply(u, k, 0)
        return
    pushdown(u); mid = (L[u] + R[u]) >> 1
    if l <= mid: change2(u << 1, l, r, k)
    if r > mid: change2(u << 1 | 1, l, r, k)
    pushup(u)

def query(u, l, r):
    if l <= L[u] and R[u] <= r: return SUM[u]
    pushdown(u); mid = (L[u] + R[u]) >> 1; ans = 0
    if l <= mid: ans += query(u << 1, l, r)
    if r > mid: ans += query(u << 1 | 1, l, r)
    return ans % mod

build(1, 1, n)

for _ in range(m):
    op = list(map(int, input().split()))
    if op[0] == 1: change2(1, op[1], op[2], op[3])
    elif op[0] == 2: change(1, op[1], op[2], op[3])
    else: print(query(1, op[1], op[2]))
```

### C++代码实现

```c++
// 洛谷P3373
#include <cstring>
#include <iostream>
#include <algorithm>
using namespace std;

#define N 100005
#define LL long long
#define int long long
#define lc u<<1
#define rc u<<1|1
LL w[N];
LL n,m,op,x,y,k,mod;
struct Tree{ //线段树
  LL l,r,sum,add,mul;
}tr[N*4];

inline LL len(int u) { return tr[u].r - tr[u].l + 1; }

void pushup(int u) {
  tr[u].sum = (tr[lc].sum + tr[rc].sum) % mod;
}

void apply_mul_add_to_node(int u, LL mulv, LL addv) {
  mulv %= mod; if (mulv < 0) mulv += mod;
  addv %= mod; if (addv < 0) addv += mod;
  tr[u].sum = ( (tr[u].sum * mulv) % mod + (addv * (len(u) % mod)) % mod ) % mod;
  tr[u].mul = (tr[u].mul * mulv) % mod;
  tr[u].add = (tr[u].add * mulv + addv) % mod;
}

void pushdown(int u) {
  if (tr[u].mul != 1 || tr[u].add != 0) {
    apply_mul_add_to_node(lc, tr[u].mul, tr[u].add);
    apply_mul_add_to_node(rc, tr[u].mul, tr[u].add);
    tr[u].mul = 1;
    tr[u].add = 0;
  }
}
void build(LL u,LL l,LL r){ //建树
  tr[u]={l,r,w[l],0,1};
  if(l==r) return;
  LL m=l+r>>1;
  build(lc,l,m);
  build(rc,m+1,r);
  pushup(u);
}
void change(LL u,LL l,LL r,LL k){ //区修
  if(l<=tr[u].l&&tr[u].r<=r){
    apply_mul_add_to_node(u, 1, k);
    return;
  }
  LL m=tr[u].l+tr[u].r>>1;
  pushdown(u);
  if(l<=m) change(lc,l,r,k);
  if(r>m) change(rc,l,r,k);
  pushup(u);
}
void change2(LL u,LL l,LL r,LL k){ //区修
  if(l<=tr[u].l&&tr[u].r<=r){
    apply_mul_add_to_node(u, k, 0);
    return;
  }
  LL m=tr[u].l+tr[u].r>>1;
  pushdown(u);
  if(l<=m) change2(lc,l,r,k);
  if(r>m) change2(rc,l,r,k);
  pushup(u);
}
LL query(LL u,LL l,LL r){ //区查
  if(l<=tr[u].l && tr[u].r<=r) return tr[u].sum % mod;
  LL m=tr[u].l+tr[u].r>>1;
  pushdown(u);
  LL sum=0;
  if(l<=m) {
    sum+=query(lc,l,r);
    sum %= mod;
  }
  if(r>m) {
    sum+=query(rc,l,r);
    sum %= mod;
  }
  return sum;
}
signed main(){
  cin>>n>>m>>mod;
  for(int i=1; i<=n; i ++) cin>>w[i];
  build(1,1,n);
  while(m--){
    cin>>op>>x>>y;
    if(op==3)cout<<query(1,x,y)<<endl;
    else if (op == 2){
      cin>>k;change(1,x,y,k);
    }
    else{
      cin>>k;change2(1,x,y,k);
    }
  }
  return 0;
}
```
