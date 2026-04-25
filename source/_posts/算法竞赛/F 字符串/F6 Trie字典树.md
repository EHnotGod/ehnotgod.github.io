---
title: "F6 Trie字典树"
categories:
- [算法, F 字符串]
tags:
- 字符串
---

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
