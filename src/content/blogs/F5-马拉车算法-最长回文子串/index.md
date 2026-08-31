---
title: "F5 马拉车算法-最长回文子串"
publishDate: 2026-08-08
description: "Manacher 马拉车：O(n) 求最长回文子串。"
category: algo
tags:
  - 字符串
language: zh
---

### 题目情境

题目链接：https://www.luogu.com.cn/problem/P3805

**题目描述**

给出一个只由小写英文字符 $a,b,c,\dots,y,z$ 组成的字符串 $S$，求 $S$ 中最长回文串的长度。

**输入格式**

一行小写英文字符组成的字符串 $S$。

**输出格式**

一个整数表示答案。

输入 #1

```
aaa
```

输出 #1

```
3
```

**说明/提示**

对于 $100\%$ 的数据，$1\le |S|\le 1.1\times 10^7$。

### 算法解析：

Manacher（马拉车）O(n) 求最长回文子串：先在字符间插入 `#`（首尾加哨兵 `$`）把奇偶回文统一为奇回文，再维护当前最右回文边界 $[l,r]$ 与对应中心。$d[i]$ 为以 $i$ 为中心的回文半径，初始化用对称位置 $d[l+r-i]$ 取 min，再向两边扩展比较，最后更新 $[l,r]$。最长回文子串长度为 $\max d[i]-1$。复杂度 $O(n)$。

### Python代码实现

```python
s = input().strip()
# 改造串：插入 # 统一奇偶回文
t = ['$', '#']
for c in s:
    t.append(c)
    t.append('#')
n = len(t)
d = [0] * n
l, r = 1, 1
ans = 0
for i in range(1, n):
    if i <= r:
        d[i] = min(d[l + r - i], r - i + 1)
    while i - d[i] >= 0 and i + d[i] < n and t[i - d[i]] == t[i + d[i]]:
        d[i] += 1
    if i + d[i] - 1 > r:
        l = i - d[i] + 1
        r = i + d[i] - 1
    ans = max(ans, d[i])
print(ans - 1)
```

### C++代码实现

```c++
#include <iostream>
#include <cstring>
#include <algorithm>
using namespace std;

const int N=3e7;
char a[N],s[N];
int d[N]; //回文半径函数 

void get_d(char*s,int n){
  d[1]=1;
    for(int i=2,l,r=1;i<=n;i++){
        if(i<=r)d[i]=min(d[r-i+l],r-i+1);
        while(s[i-d[i]]==s[i+d[i]])d[i]++;
        if(i+d[i]-1>r)l=i-d[i]+1,r=i+d[i]-1;
        // printf("i=%d d=%d [%d %d]\n",i,d[i],l,r);
    }  
}
int main(){
  //改造串
  scanf("%s",a+1);
  int n=strlen(a+1),k=0;
  s[0]='$',s[++k]='#';        
  for(int i=1;i<=n;i++) 
    s[++k]=a[i],s[++k]='#';
  n=k;
  
  get_d(s,n);//计算d函数
  int ans=0;
  for(int i=1;i<=n;i++)
    ans=max(ans,d[i]);
  printf("%d\n",ans-1);
  return 0;
}
```
