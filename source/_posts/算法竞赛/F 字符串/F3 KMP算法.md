---
title: "F3 KMP算法"
categories:
- [算法, F 字符串]
tags:
- 字符串
---

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
