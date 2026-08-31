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

（题目链接待补充：Trie 字典树——统计每个字符串出现的次数）

**题目描述**

给定 $n$ 个模式串 $s_1\sim s_n$ 和 $q$ 次询问，每次询问给定一个文本串 $t$，请回答 $t$ 在 $s_1\sim s_n$ 中作为完整字符串出现的次数。

**输入格式**

第一行是两个整数，分别表示模式串的个数 $n$ 和询问的个数 $q$。

接下来 $n$ 行，每行一个字符串，表示一个模式串。接下来 $q$ 行，每行一个字符串，表示一次询问。

**输出格式**

对于每次询问，输出一行一个整数表示答案。

输入 #1

```
3 3
fusufusu
fusu
fusu
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

Trie 字典树（前缀树）：每个节点有 26 个儿子指针（小写字母），插入时沿字符链走，不存在则新建节点，末尾节点 $cnt$ 加一。查询时沿询问串走到底，返回末尾节点的 $cnt$ 即该串作为完整串出现的次数；中途断链则返回 0。插入、查询均 $O(|s|)$。

### Python代码实现

```python
N = 100010
ch = [[0 for _ in range(26)] for _ in range(N)]
cnt = [0] * N
idx = 0

def insert(s):
    global idx
    p = 0
    for c in s:
        j = ord(c) - ord('a')
        if not ch[p][j]:
            idx += 1
            ch[p][j] = idx
        p = ch[p][j]
    cnt[p] += 1

def query(s):
    p = 0
    for c in s:
        j = ord(c) - ord('a')
        if not ch[p][j]:
            return 0
        p = ch[p][j]
    return cnt[p]

n, q = map(int, input().split())
for _ in range(n):
    s = input().strip()
    insert(s)
for _ in range(q):
    s = input().strip()
    print(query(s))
```

### C++代码实现

```c++
// O(n)#include <iostream>
#include <cstring>
#include <algorithm>
using namespace std;

const int N=100010;
int n;
char s[N];
int ch[N][26],cnt[N],idx;

void insert(char *s){
  int p=0;
  for(int i=0; s[i]; i ++){
    int j=s[i]-'a';//字母映射
    if(!ch[p][j])ch[p][j]=++idx;
    p=ch[p][j];
  }
  cnt[p]++;//插入次数
}
int query(char *s){
  int p=0;
  for(int i=0; s[i]; i ++){
    int j=s[i]-'a';
    if(!ch[p][j]) return 0;
    p=ch[p][j];
  }
  return cnt[p];
}
int main(){
  scanf("%d",&n);
  while(n--){
    char op;
    scanf("%s%s",&op,s);
    if(op=='I')insert(s);
    else printf("%d\n",query(s));
  }
  return 0;
}
```
