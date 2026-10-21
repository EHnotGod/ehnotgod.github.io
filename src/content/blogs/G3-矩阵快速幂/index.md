---
title: "G3 矩阵快速幂"
publishDate: 2026-08-08
description: "矩阵快速幂：加速线性递推。"
category: algo
tags:
  - 数学
language: zh
---
### 题目情境

题目链接：https://www.luogu.com.cn/problem/P3390

**题目描述**

给定 $$n\times n$$ 的矩阵 $$A$$，求 $$A^k$$。

**输入格式**

第一行两个整数 $$n,k$$。  
接下来 $$n$$ 行，每行 $$n$$ 个整数，第 $$i$$ 行的第 $$j$$ 的数表示 $$A_{i,j}$$。

**输出格式**

输出 $$A^k$$

共 $$n$$ 行，每行 $$n$$ 个数，第 $$i$$ 行第 $$j$$ 个数表示 $$(A^k)_{i,j}$$，每个元素对 $$10^9+7$$ 取模。

输入 #1

```
2 1
1 1
1 1
```

输出 #1

```
1 1
1 1
```

输入 #2

```
3 5
1 2 3
4 5 6
7 8 9
```

输出 #2

```
121824 149688 177552
275886 338985 402084
429948 528282 626616
```

对于 $$100\%$$ 的数据，$$1\le n \le 100$$，$$0 \le k \le 10^{12}$$，$$|A_{i,j}| \le 1000$$。

### 算法解析：

矩阵快速幂：把标量快速幂推广到矩阵。初始为单位矩阵，转移矩阵自乘平方，指数 $k$ 按二进制拆分，当前位为 1 则乘上对应矩阵。矩阵乘法三重循环 $O(n^3)$，总复杂度 $O(n^3\log k)$，模 $10^9+7$。

### Python代码实现

```python
import sys
MOD = 10**9 + 7
def mat_mult(X, Y, n):  # 矩阵乘法：返回 X * Y
    Z = [[0] * n for _ in range(n)]
    for i in range(n):
        for k in range(n):
            if X[i][k]:  # 跳过零元，加快运算
                xik = X[i][k]
                for j in range(n):
                    Z[i][j] = (Z[i][j] + xik * Y[k][j]) % MOD
    return Z

def mat_pow(A, exp, n):  # 快速幂：A^exp
    # 初始化为单位矩阵
    res = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    base = A
    while exp:
        if exp & 1:
            res = mat_mult(res, base, n)
        base = mat_mult(base, base, n)
        exp >>= 1
    return res
n, k = map(int, input().split())
# 读取矩阵，转换为 0-index 列表
A = []
for i in range(n):
    A.append(list(map(int, input().split())))
# 计算 A^k 模 MOD
result = mat_pow(A, k, n)
# 输出结果矩阵
out = []
for row in result:
    out.append(' '.join(str(v) for v in row))
sys.stdout.write('\n'.join(out))
```

### C++代码实现

```c++
#include <iostream>
#include <vector>
using namespace std;

using LL = long long;
using Matrix = vector<vector<LL>>;
const LL mod=1000000007;

Matrix mul(const Matrix& a,const Matrix& b){
  int n=static_cast<int>(a.size());
  Matrix res(n,vector<LL>(n,0));
  for(int i=0;i<n;i++)
    for(int k=0;k<n;k++)
      for(int j=0;j<n;j++)
        res[i][j]=(res[i][j]+a[i][k]*b[k][j])%mod;
  return res;
}
Matrix quickpow(Matrix a,LL k){
  int n=static_cast<int>(a.size());
  Matrix res(n,vector<LL>(n,0));
  for(int i=0;i<n;i++) res[i][i]=1;
  while(k){
    if(k&1) res=mul(res,a);
    a=mul(a,a);
    k>>=1;
  }
  return res;
}
int main(){
  ios::sync_with_stdio(false); cin.tie(nullptr);
  int n; LL k; cin>>n>>k;
  Matrix a;
  a.assign(n,vector<LL>(n,0));
  for(auto& row:a)
    for(LL& value:row){
      cin>>value;
      value=(value%mod+mod)%mod;
    }
  Matrix res=quickpow(a,k);
  for(const auto& row:res){
    for(LL value:row) cout<<value<<' ';
    cout<<'\n';
  }
}
```
