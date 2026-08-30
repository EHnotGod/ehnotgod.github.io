---
title: "E36 数位DP"
publishDate: 2026-08-08
description: "数位 DP：按位枚举统计满足条件的数字。"
category: algo
tags:
  - 动态规划
language: zh
---

### 题目情境

（题目链接待补充：数位 DP——不降数）

### 算法解析：

数位 DP（不降数）：把数字按位处理，$f[i][j]$ 表示共 $i$ 位且最高位为 $j$ 的不降数个数（先预处理）。求 $\le n$ 的不降数个数时，从高位到低位枚举，用 $last$ 记录上一位，逐位累加符合条件的数，并处理贴住 $n$ 的边界情况；区间 $[l,r]$ 用 $f(r)-f(l-1)$。核心是“最高位 + 位数”的状态设计。复杂度 $O(位数\times 10\times 10)$。

### C++代码实现

```c++
#include <iostream>
#include <cstring>
#include <algorithm>
using namespace std;

const int N=12;
int a[N];     //把整数的每一位数字抠出来，存入数组 
int f[N][N];  //f[i][j]表示一共有i位，且最高位数字是j的不降数的个数 

void init(){  //预处理不降数的个数  
  for(int i=0; i<=9; i++) f[1][i]=1;  //一位数
  for(int i=2; i<N; i++)        //阶段：枚举位数 
    for(int j=0; j<=9; j++)     //状态：枚举最高位 
      for(int k=j; k<=9; k++)   //决策：枚举次高位 
        f[i][j]+=f[i-1][k];
}
int dp(int n){
  if(!n) return 1;              //特判，n==0返回1 
  int cnt=0;
  while(n) a[++cnt]=n%10, n/=10;//把每一位抠出来存入数组a      
  
  int res=0, last=0;            //last表示上一位数字
  for(int i=cnt; i>=1; --i){    //从高位到低位枚举 
    int now=a[i];               //now表示当前位数字           
    for(int j=last; j<now; j++) //枚举当前位可填入的数字  
      res += f[i][j];           //累加答案
    if(now<last) break;         //若小，则break                          
    last=now;                   //更新last
    if(i==1) res++;             //特判，走到a1的情况 
  } 
  return res;
}
int main(){
  init();     //预处理不降数的个数 
  int l,r;
  while(cin>>l>>r) cout<<dp(r)-dp(l-1)<<endl;
  return 0;
}
```
