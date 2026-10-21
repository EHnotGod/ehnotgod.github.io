---
title: "F3 Trie字典树"
publishDate: 2026-08-08
description: "Trie 字典树：多模式串前缀匹配。"
category: algo
tags:
  - 字符串
language: zh
---

### 题目情境

题目链接：https://www.luogu.com.cn/problem/P8306

**题目描述**

给定 $n$ 个模式串 $s_1\sim s_n$ 和 $q$ 次询问，每次询问给定一个文本串 $t$，请回答 $s_1\sim s_n$ 中有多少个字符串以 $t$ 为前缀。字符串大小写敏感。

**输入格式**

第一行是测试数据组数 $T$。对每组数据，先读入两个整数 $n,q$，分别表示模式串的个数和询问的个数。

接下来 $n$ 行，每行一个字符串，表示一个模式串。接下来 $q$ 行，每行一个字符串，表示一次询问。

**输出格式**

对于每次询问，输出一行一个整数表示答案。

输入 #1

```
1
3 3
fusufusu
fusu
anguei
fusu
anguei
kkksc
```

输出 #1

```
2
1
0
```

**说明/提示**

保证输入字符串的总长度不超过 $3\times 10^6$，只含大小写字母和数字，且不含空串。

### 算法解析：

Trie 字典树（前缀树）：每个节点用映射记录已有的字符转移，支持大小写字母和数字，插入时沿字符链走，不存在则新建节点，每经过一个字符节点，就将该节点的 $cnt$ 加一。查询时沿询问串走到底，返回末尾节点的 $cnt$，即以该询问串为前缀的模式串数量；中途断链则返回 0。节点和计数按需扩容；使用哈希映射时，插入、查询的期望时间均为 $O(|s|)$。

### Python代码实现

```python
ch = []
cnt = []

def insert(s):
    p = 0
    for c in s:
        if c not in ch[p]:
            ch[p][c] = len(ch)
            ch.append({})
            cnt.append(0)
        p = ch[p][c]
        cnt[p] += 1

def query(s):
    p = 0
    for c in s:
        if c not in ch[p]:
            return 0
        p = ch[p][c]
    return cnt[p]

T = int(input())
for _ in range(T):
    n, q = map(int, input().split())
    ch = [{}]
    cnt = [0]
    for _ in range(n):
        insert(input().strip())
    for _ in range(q):
        print(query(input().strip()))
```

### C++代码实现

```c++
#include <iostream>
#include <string>
#include <vector>
#include <unordered_map>
using namespace std;

vector<unordered_map<char,int>> ch;
vector<int> cnt;

void insert(const string& s){
  int p=0;
  for(char c:s){
    auto it=ch[p].find(c);
    if(it==ch[p].end()){
      int next=ch.size();
      ch[p][c]=next;
      ch.emplace_back();
      cnt.push_back(0);
      p=next;
    }
    else p=it->second;
    cnt[p]++;
  }
}
int query(const string& s){
  int p=0;
  for(char c:s){
    auto it=ch[p].find(c);
    if(it==ch[p].end()) return 0;
    p=it->second;
  }
  return cnt[p];
}
int main(){
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int T; cin>>T;
  while(T--){
    int n,q; cin>>n>>q;
    ch.assign(1,{}); cnt.assign(1,0); // 每组重置根节点，按需扩容
    string s;
    while(n--) cin>>s,insert(s);
    while(q--) cin>>s,cout<<query(s)<<'\n';
  }
  return 0;
}
```
