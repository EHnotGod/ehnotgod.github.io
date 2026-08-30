---
title: "E43 单调队列优化dp"
publishDate: 2026-08-08
description: "单调队列优化 DP：维护滑动窗口最值转移。"
category: algo
tags:
  - 动态规划
language: zh
---

### 题目情境

题目链接：https://www.luogu.com.cn/problem/P1725

### 算法解析：

单调队列优化 DP：当转移式是 $f[i]=\max/\min(f[j])+w$ 且 $j$ 落在长度固定的滑动窗口内时，用单调队列维护候选 $j$ 的最值。本题从 $[i-m, i-1]$ 转移：队头弹出滑出窗口的下标，队尾保持 $f$ 单调，$f[i]=f[q[h]]+a[i]$，最后取能到达末尾的最小值。复杂度 $O(n)$。

### C++代码实现

```c++
// 单调队列+DP O(n)
#include<bits/stdc++.h>
using namespace std;

const int N=200010;
int n,m,a[N];
int q[N],f[N];

int main(){
  cin>>n>>m;
  for(int i=1; i<=n; i++) cin>>a[i];
  
  int ans=2e9;
  for(int i=1,h=1,t=0; i<=n; i++){
    while(h<=t && q[h]<i-m) h++;
    while(h<=t && f[q[t]]>=f[i-1]) t--;
    q[++t]=i-1;
    f[i]=f[q[h]]+a[i];
    if(i>=n-m+1) ans=min(ans,f[i]);
  }
  cout<<ans;
}
```
