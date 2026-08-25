---
title: "A12 单调栈"
publishDate: 2026-08-08
description: "给出项数为 n 的整数数列 a 1 … n。"
category: algo
tags:
  - 基础算法
language: zh
---

### 题目情境

题目链接：https://www.luogu.com.cn/problem/P5788

**题目描述**

给出项数为 $$n$$ 的整数数列 $$a_{1 \dots n}$$。

定义函数 $$f(i)$$ 代表数列中第 $$i$$ 个元素之后第一个大于 $$a_i$$ 的元素的**下标**，即 $$f(i)=\min_{i<j\leq n, a_j > a_i} \{j\}$$。若不存在，则 $$f(i)=0$$。

试求出 $$f(1\dots n)$$。

**输入格式**

第一行一个正整数 $$n$$。

第二行 $$n$$ 个正整数 $$a_{1\dots n}$$。

**输出格式**

一行 $$n$$ 个整数表示 $$f(1), f(2), \dots, f(n)$$ 的值。

**输入输出样例**

输入 #1

```
5
1 4 2 3 5
```

输出 #1

```
2 5 4 5 0
```

对于 $$100\%$$ 的数据，$$1 \le n\leq 3\times 10^6$$，$$1\leq a_i\leq 10^9$$。
### 算法解析

**单调栈**是一种维护元素单调性的栈结构，用于高效求解"下一个更大/更小元素"类问题。

**核心思路：** 从右向左遍历数组，维护一个**单调递减栈**（栈底到栈顶递减），栈中存储下标。

对于每个位置 $$i$$：
1. 弹出栈中所有值 $$\leq a_i$$ 的元素（它们不可能成为 $$i$$ 左侧任何元素的答案）；
2. 若栈非空，则栈顶下标即为 $$f(i)$$（第一个大于 $$a_i$$ 的元素）；
3. 将 $$i$$ 压入栈中。

**复杂度：** 每个元素至多入栈、出栈各一次，时间复杂度为 $$O(n)$$，空间复杂度为 $$O(n)$$。

### Python代码实现

```python
n = int(input())
a = list(map(int, input().split()))
f = [0] * n
q = []
for i in range(n - 1, -1, -1):
    while q and a[q[-1]] < a[i]:
        q.pop()
    if q:
        f[i] = q[-1]
    q.append(i)
print(*f)
```

### C++代码实现

```cpp
#include <cstdio>
using namespace std;

const int N = 3000005;
int a[N], f[N], stk[N];

int main() {
    int n;
    scanf("%d", &n);
    for (int i = 1; i <= n; i++) scanf("%d", &a[i]);

    int top = 0;
    // 从右往左，维护单调递减栈，求每个位置右边第一个更大元素的下标
    for (int i = n; i >= 1; i--) {
        while (top && a[stk[top]] <= a[i]) top--;  // 弹出所有不大于 a[i] 的元素
        f[i] = top ? stk[top] : 0;                // 栈顶即答案，空栈则为 0
        stk[++top] = i;                            // 当前下标入栈
    }

    for (int i = 1; i <= n; i++) printf("%d ", f[i]);
    return 0;
}
```
