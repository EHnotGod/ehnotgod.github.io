---
title: "E18 数位DP"
publishDate: 2026-08-08
description: "数位 DP：按位枚举统计满足条件的数字。"
category: algo
tags:
  - 动态规划
language: zh
---

### 题目情境

题目链接：http://ybt.ssoier.cn:8088/problem_show.php?pid=1586


**题目描述**

科协里最近很流行数字游戏。某人命名了一种不降数，这种数字必须满足从左到右各位数字成小于等于的关系，如 123，446。现在大家决定玩一个游戏，指定一个整数闭区间 [a,b]，问这个区间内有多少个不降数。

**输入格式**

有多组测试数据。每组只含两个数字 a,b，意义如题目描述。

**输出格式**

每行给出一个测试数据的答案，即 [a,b] 之间有多少不降数。

#输入1

```
1 9
1 19
```

#输出1

```
9
18
```

对于全部数据，$$1≤a≤b≤2^{31}−1$$。

### 算法解析：

数位 DP（不降数）：把数字按位处理，$f[i][j]$ 表示共 $i$ 位且最高位为 $j$ 的不降数个数（先预处理）。求 $\le n$ 的不降数个数时，从高位到低位枚举，用 $last$ 记录上一位，逐位累加符合条件的数，并处理贴住 $n$ 的边界情况；区间 $[l,r]$ 用 $f(r)-f(l-1)$。核心是“最高位 + 位数”的状态设计。复杂度 $O(位数\times 10\times 10)$。

### Python代码实现

```python
N = 12
a = [0] * N   # 把整数的每一位数字抠出来，存入数组
f = [[0] * N for _ in range(N)]  # f[i][j] 表示一共有 i 位且最高位数字是 j 的不降数个数

def init():   # 预处理不降数的个数
    for j in range(10):
        f[1][j] = 1  # 一位数
    for i in range(2, N):        # 阶段：枚举位数
        for j in range(10):      # 状态：枚举最高位
            for k in range(j, 10):  # 决策：枚举次高位
                f[i][j] += f[i - 1][k]

def dp(n):
    if not n:
        return 1   # 特判，n == 0 返回 1
    cnt = 0
    while n:
        a[cnt + 1] = n % 10
        n //= 10
        cnt += 1
    res, last = 0, 0   # last 表示上一位数字
    for i in range(cnt, 0, -1):  # 从高位到低位枚举
        now = a[i]               # now 表示当前位数字
        for j in range(last, now):   # 枚举当前位可填入的数字
            res += f[i][j]       # 累加答案
        if now < last:
            break                # 若小于上一位，则 break
        last = now               # 更新 last
        if i == 1:
            res += 1             # 特判，走到 a1 的情况
    return res

init()  # 预处理不降数的个数
while True:
    try:
        l, r = map(int, input().split())
        print(dp(r) - dp(l - 1))
    except EOFError:
        break
```

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
