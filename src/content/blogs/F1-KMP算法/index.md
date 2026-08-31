---
title: "F1 KMP算法"
publishDate: 2026-08-08
description: "KMP 字符串匹配：next 数组加速匹配。"
category: algo
tags:
  - 字符串
language: zh
---

### 题目情境

题目链接：https://www.luogu.com.cn/problem/P3375

**题目描述**

给出两个字符串 $s_1$ 和 $s_2$，若 $s_1$ 的区间 $[l,r]$ 子串与 $s_2$ 完全相同，则称 $s_2$ 在 $s_1$ 中出现了，其出现位置为 $l$。现在请你求出 $s_2$ 在 $s_1$ 中所有出现的位置。

定义一个字符串 $s$ 的 border 为 $s$ 的一个非 $s$ 本身的子串 $t$，满足 $t$ 既是 $s$ 的前缀，又是 $s$ 的后缀。对于 $s_2$，你还需要求出对于其每个前缀 $s_2$ 的最长 border 的长度。

**输入格式**

第一行为一个字符串，即为 $s_1$。第二行为一个字符串，即为 $s_2$。

**输出格式**

首先输出若干行，每行一个整数，按从小到大的顺序输出 $s_2$ 在 $s_1$ 中出现的位置。最后一行输出 $|s_2|$ 个整数，第 $i$ 个整数表示 $s_2$ 的长度为 $i$ 的前缀的最长 border 长度。

输入 #1

```
ABABABC
ABA
```

输出 #1

```
1
3
0 0 1
```

**说明/提示**

对于全部的测试点，$1\le |s_1|,|s_2|\le 10^6$，$s_1,s_2$ 中均只含大写英文字母。

### 算法解析：

KMP 字符串匹配：预处理模式串的 $nxt$ 数组，$nxt[i]$ 表示 $P$ 的前缀 $i$ 的最长 border 长度。匹配时主串指针不回退，失配时 $j=nxt[j]$ 跳跃，$j==n$ 即匹配成功并输出位置 $i-n+1$。最后按题目要求输出 $nxt[1..n]$。复杂度 $O(n+m)$。

### Python代码实现

```python
N = 1000010
S = list(input().strip())
S = [""] + S
P = list(input().strip())
P = [""] + P
nxt = [0] * N
m = len(S) - 1
n = len(P) - 1
S.append("")
P.append("")
nxt[1] = 0
j = 0
for i in range(2, n + 1):
    while j and P[i] != P[j + 1]:
        j = nxt[j]
    if P[i] == P[j + 1]:
        j += 1
    nxt[i] = j
j = 0
for i in range(1, m + 1):
    while j and S[i] != P[j + 1]:
        j = nxt[j]
    if S[i] == P[j + 1]:
        j += 1
    if j == n:
        print(i - n + 1)
print(*nxt[1:n + 1])
```

### C++代码实现

```c++
#include <cstring>
#include <iostream>
#include <algorithm>
using namespace std;

const int N=1000010;
int m,n;
char S[N],P[N];
int nxt[N];

int main(){
  cin>>S+1>>P+1;
  m=strlen(S+1),n=strlen(P+1);

  nxt[1]=0;
  for(int i=2,j=0;i<=n;i++){
    while(j && P[i]!=P[j+1]) j=nxt[j];
    if(P[i]==P[j+1]) j++;
    nxt[i]=j;
  }

  for(int i=1,j=0;i<=m;i++){
    while(j && S[i]!=P[j+1]) j=nxt[j];
    if(S[i]==P[j+1]) j++;
    if(j==n) printf("%d\n",i-n+1);
  }

  for(int i=1;i<=n;i++)printf("%d ",nxt[i]);
  return 0;
}
```
