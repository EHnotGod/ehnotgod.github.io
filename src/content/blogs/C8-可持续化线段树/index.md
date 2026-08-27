---
title: "C8 可持续化线段树"
publishDate: 2026-08-08
description: "可持久化线段树（主席树）：静态区间第 k 小。"
category: algo
tags:
  - 数据结构
language: zh
---

### 题目情境

**题目背景**

这是个非常经典的可持久化权值线段树入门题——静态区间第 $$k$$ 小。

**题目描述**

如题，给定 $$n$$ 个整数构成的序列 $$a$$，将对于指定的闭区间 $$[l, r]$$ 查询其区间内的第 $$k$$ 小值。

**输入格式**

第一行包含两个整数，分别表示序列的长度 $$n$$ 和查询的个数 $$m$$。  
第二行包含 $$n$$ 个整数，第 $$i$$ 个整数表示序列的第 $$i$$ 个元素 $$a_i$$。   
接下来 $$m$$ 行每行包含三个整数 $$ l, r, k$$ , 表示查询区间 $$[l, r]$$ 内的第 $$k$$ 小值。

**输出格式**

对于每次询问，输出一行一个整数表示答案。

输入 #1

```
5 5
25957 6405 15770 26287 26465 
2 2 1
3 4 1
4 5 1
1 2 2
4 4 1
```

输出 #1

```
6405
15770
26287
25957
26287
```

- 对于 $$100\%$$ 的数据，满足 $$1 \leq n,m \leq 2\times 10^5$$，$$0\le a_i \leq 10^9$$，$$1 \leq l \leq r \leq n$$，$$1 \leq k \leq r - l + 1$$。

### 算法解析

**1. 每棵树维护什么？**

普通线段树一般维护数组下标区间，而主席树这里维护的是**值域**。

```cpp
struct node{
    int l,r,s;
};
```

其中：

- `l`：左儿子编号
- `r`：右儿子编号
- `s`：当前值域内有多少个数

例如：

```text
          [1,4] s=4
         /          \
    [1,2] s=2    [3,4] s=2
```

也就是说，它本质上是一棵**统计每个值出现次数的线段树**。

**2. `root[i]` 是什么？**

```cpp
root[i]
```

表示：

> 前 $i$ 个数形成的值域线段树。

例如：

```text
a = [3,1,4,2]

root[0] = []
root[1] = [3]
root[2] = [3,1]
root[3] = [3,1,4]
root[4] = [3,1,4,2]
```

**3. 怎么查询第 k 小？**

查询：

```cpp
query(root[l-1],root[r],1,bn,k);
```

核心代码：

```cpp
int s=tr[lc(y)].s-tr[lc(x)].s;
```

这里：

```text
x = root[l-1]
y = root[r]
```

所以 `s` 表示：

> `[l,r]` 中有多少个数落在当前值域的左半边。

不断对值域二分，直到找到答案。

**4. 为什么要有很多版本？**

每加入一个新数，就产生一个新版本：

```cpp
insert(root[i-1],root[i],1,bn,id);
```

也就是：

```text
root[0]
   ↓ 插入 a1
root[1]
   ↓ 插入 a2
root[2]
   ↓ 插入 a3
root[3]
...
```

但是不会把整棵树复制一遍。

**5. 新版本是怎么产生的？**

核心：

```cpp
void insert(int x,int &y,int l,int r,int pos){
    y=++idx;
    tr[y]=tr[x];
    tr[y].s++;
    ...
}
```

其中：

```text
x = 旧版本节点
y = 新版本节点
```

最重要的是：

```cpp
y=++idx;      // 新建节点
tr[y]=tr[x];  // 复制旧节点
tr[y].s++;    // 只修改新节点
```

也就是说：

> **旧节点不修改，先复制一份，再修改副本。**

因此一次插入只增加：

```text
O(log n)
```

个节点，而不是复制整棵树。

复杂度：

```text
建树：O(n log n)
单次查询：O(log n)
空间：O(n log n)
```

### Python代码实现

```python
import bisect

class Node:
    def __init__(self, l=0, r=0, s=0):
        self.l = l
        self.r = r
        self.s = s


n, m = map(int, input().split())
a = list(map(int, input().split()))
a = [0] + a  # 转换为1-based索引

# 离散化处理
sorted_b = sorted(a[1:])
unique_b = []
prev = None
for num in sorted_b:
    if num != prev:
        unique_b.append(num)
        prev = num
bn = len(unique_b)

# 初始化主席树
tr = [Node(0, 0, 0)]  # 空节点，索引0
idx = 1
root = [0] * (n + 1)
root[0] = 0

def insert(x, l, r, pos):
    global idx
    y = Node(tr[x].l, tr[x].r, tr[x].s + 1)
    tr.append(y)
    y_idx = idx
    idx += 1
    if l == r:
        return y_idx
    mid = (l + r) // 2
    if pos <= mid:
        new_l = insert(tr[x].l, l, mid, pos)
        y.l = new_l
    else:
        new_r = insert(tr[x].r, mid + 1, r, pos)
        y.r = new_r
    return y_idx

# 构建主席树的每个版本
for i in range(1, n + 1):
    num = a[i]
    pos = bisect.bisect_left(unique_b, num) + 1  # 转换为1-based的id
    root[i] = insert(root[i-1], 1, bn, pos)

# 查询函数
def query(x, y, l, r, k):
    if l == r:
        return l
    mid = (l + r) // 2
    left_x = tr[x].l
    left_y = tr[y].l
    s = tr[left_y].s - tr[left_x].s
    if k <= s:
        return query(left_x, left_y, l, mid, k)
    else:
        return query(tr[x].r, tr[y].r, mid + 1, r, k - s)

# 处理每个查询并输出结果
output = []
for _ in range(m):
    l, r, k = map(int, input().split())
    id = query(root[l-1], root[r], 1, bn, k)
    output.append(str(unique_b[id-1]))  # id转换为0-based索引
print('\n'.join(output))
```

### C++代码实现

```c++
// 主席树 O(nlognlogn)
#include <iostream>
#include <cstring>
#include <algorithm>
using namespace std;

#define N 200005
#define lc(x) tr[x].l
#define rc(x) tr[x].r
struct node{
  int l,r,s; //s:节点值域中有多少个数
}tr[N*20];
int root[N],idx;
int n,m,a[N],b[N];

void insert(int x,int &y,int l,int r,int pos){
  y=++idx; //开点
  tr[y]=tr[x]; tr[y].s++;
  if(l==r) return;
  int m=l+r>>1;
  if(pos<=m) insert(lc(x),lc(y),l,m,pos);
  else insert(rc(x),rc(y),m+1,r,pos);
}
int query(int x,int y,int l,int r,int k){
  if(l==r) return l;
  int m=l+r>>1;
  int s=tr[lc(y)].s-tr[lc(x)].s;
  if(k<=s) return query(lc(x),lc(y),l,m,k);
  else return query(rc(x),rc(y),m+1,r,k-s);
}
int main(){
  scanf("%d%d",&n,&m);
  for(int i=1; i<=n; i++){
    scanf("%d",&a[i]); b[i]=a[i];
  }
  sort(b+1,b+n+1);
  int bn=unique(b+1,b+n+1)-b-1; //去重后的个数

  for(int i=1; i<=n; i++){
    int id=lower_bound(b+1,b+bn+1,a[i])-b;//下标
    insert(root[i-1],root[i],1,bn,id);
  }
  while(m--){
    int l,r,k; scanf("%d%d%d",&l,&r,&k);
    int id=query(root[l-1],root[r],1,bn,k);
    printf("%d\n",b[id]);
  }
}
```
