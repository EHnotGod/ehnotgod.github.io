---
title: "F2 马拉车算法-最长回文子串"
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
#include <string>
#include <vector>
#include <algorithm>
using namespace std;

void get_d(const string& s,vector<int>& d){
  int n=s.size()-2;
  for(int i=1,l=0,r=0;i<=n;i++){
    d[i]=i<=r ? min(d[l+r-i],r-i+1) : 1;
    while(s[i-d[i]]==s[i+d[i]]) d[i]++;
    if(i+d[i]-1>r) l=i-d[i]+1,r=i+d[i]-1;
  }
}
int main(){
  string a; cin>>a;
  // 改造串，并在两端放置不同的哨兵。
  string s="^#";
  s.reserve(2*a.size()+3);
  for(char c:a) s+=c,s+='#';
  s+='$';
  vector<int> d(s.size()); // 按改造后的串长分配回文半径
  get_d(s,d);
  int ans=0;
  for(int i=1;i+1<(int)s.size();i++) ans=max(ans,d[i]-1);
  cout<<ans<<'\n';
  return 0;
}
```
