---
title: "E20 Windy数"
publishDate: 2026-08-08
description: "数位 DP：相邻数字差不小于 2 的数。"
category: algo
tags:
  - 动态规划
language: zh
---

### 题目情境

题目链接：https://www.luogu.com.cn/problem/P2657

### 算法解析：

Windy 数（相邻数字差 $\ge 2$）数位 DP：预处理 $f[i][j]$ 表示共 $i$ 位、最高位为 $j$ 的 Windy 数个数（$f[i][j]=\sum f[i-1][k]$，其中 $|j-k|\ge 2$）。求 $\le x$ 的个数时按位枚举，$last$ 记录上一位保证相邻差 $\ge 2$，同时处理前导零（位数不足的单独统计）。区间 $[l,r]$ 用 $f(r)-f(l-1)$。复杂度 $O(位数\times 10\times 10)$。

### Python代码实现

```python
f = [[0] * 20 for i in range(20)]
def init():
    for i in range(10):
        f[1][i] = 1
    for i in range(2, 20):
        for j in range(10):
            for k in range(10):
                if abs(j - k) >= 2:
                    f[i][j] += f[i - 1][k]
def dp(x):
    if x == 0:
        return 0
    xlis = []
    while x > 0:
        xlis.append(x % 10)
        x = x // 10
    m = len(xlis)
    res = 0
    last = -2
    for i in range(m - 1, -1, -1):
        new = xlis[i]
        if i == m - 1:
            for j in range(1, new):
                if abs(j - last) >= 2:
                    res += f[i + 1][j]
        else:
            for j in range(new):
                if abs(j - last) >= 2:
                    res += f[i + 1][j]
        if abs(new - last) < 2:
            break
        last = new
        if i == 0:
            res += 1
    for i in range(m - 1):
        for j in range(1, 10):
            res += f[i + 1][j]
    return res
init()
a, b = map(int, input().split())
print(dp(b) - dp(a - 1))
```

### C++代码实现

```c++
#include <bits/stdc++.h>
using namespace std;

const int N = 20;
int a[N];     //把整数的每一位数字抠出来，存入数组 
int f[N][10]; //f[i][j]表示一共有i位，且最高位数字为j的Windy数的个数 

void init(){  //预处理Windy数的个数 
  for(int i=0; i<=9; i++) f[1][i]=1;  //一位数 
  for(int i=2; i<N; i++)        //阶段：枚举位数 
    for(int j=0; j<=9; j++)     //状态：枚举第i位 
      for(int k=0; k<=9; k++)   //决策：枚举第i-1位 
        if(abs(k-j)>=2) f[i][j]+=f[i-1][k];    
}
int dp(int x){
  if(!x) return 0;                //特判，x==0返回0 
  int cnt = 0; 
  while(x) a[++cnt]=x%10, x/=10;  //把每一位抠出来存入数组

  int res=0, last=-2;             //last表示上一位数字 
  for(int i=cnt; i>=1; --i){      //从高位到低位枚举 
    int now = a[i];               //now表示当前位数字 
    for(int j=(i==cnt); j<now; ++j)     //最高位从1开始 
      if(abs(j-last)>=2) res+=f[i][j];  //累加答案 
       
    if(abs(now-last)<2) break;  //不满足定义，break 
    last = now;                 //更新last 
    if(i==1) res++;             //特判，走到a1的情况 
  }
  
  for(int i=1; i<cnt; i++)      //答案小于cnt位的 
    for(int j=1; j<=9; j++) 
      res += f[i][j]; 
  return res; 
}
int main(){
  init();   //预处理Windy数的个数 
  int l,r;
  cin>>l>>r;
  cout<<dp(r)-dp(l-1);
  return 0;
}
```
