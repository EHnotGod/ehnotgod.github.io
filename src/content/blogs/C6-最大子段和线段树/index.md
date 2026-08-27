---
title: "C6 最大子段和线段树"
publishDate: 2026-08-08
description: "线段树进阶：维护区间最大子段和。"
category: algo
tags:
  - 数据结构
language: zh
---

### 题目情境

题目链接：https://www.luogu.com.cn/problem/P4513

**题目描述**

在小新家附近有一条“公园路”，路的一边从南到北依次排着 $$n$$ 个公园，小白早就看花了眼，自己也不清楚该去哪些公园玩了。

一开始，小白就根据公园的风景给每个公园打了分。小新为了省事，每次遛狗的时候都会事先规定一个范围，小白只可以选择第 $$a$$ 个和第 $$b$$ 个公园之间（包括 $$a, b$$ 两个公园）选择连续的一些公园玩。小白当然希望选出的公园的分数总和尽量高咯。同时，由于一些公园的景观会有所改变，所以，小白的打分也可能会有一些变化。

那么，就请你来帮小白选择公园吧。

**输入格式**

第一行，两个整数 $$n$$ 和 $$m$$，分别表示表示公园的数量和操作（遛狗或者改变打分）总数。

接下来 $$n$$ 行，每行一个整数，依次给出小白开始时对公园的打分。

接下来 $$m$$ 行，每行三个整数。其中第一个整数 $$k$$ 为 $$1$$ 或 $$2$$。

- $$k=1$$ 表示，小新要带小白出去玩，接下来的两个整数 $$a$$ 和 $$b$$ 给出了选择公园的范围 $$(1 \le a,b \le n)$$。测试数据可能会出现 $$a > b$$ 的情况，需要进行交换；
- $$k=2$$ 表示，小白改变了对某个公园的打分，接下来的两个整数 $$p$$ 和 $$s$$，表示小白对第 $$p$$ 个公园的打分变成了 $$s(1\le |s|\le 1000)$$。

**输出格式**

小白每出去玩一次，都对应输出一行，只包含一个整数，表示小白可以选出的公园得分和的最大值。

输入 #1

```
5 3
1
2
-3
4
5
1 2 3
2 2 -1
1 2 3
```

输出 #1

```
2
-1
```

对于 $$100\%$$ 的数据，$$1 \le n \le 5 \times 10^5$$，$$1 \le m \le 10^5$$，所有打分都是绝对值不超过 $$1000$$ 的整数。

### 算法解析

我们知道，求一段序列的最大子段和是O（n）的，但是这样是显然会超时的。

我们需要一个数据结构来支持修改和计算的操作，对于这种修改一个而查询区间的问题，考虑使用线段树。

在线段树中，除了左端点，右端点，左儿子指针，右儿子指针之外，新开4个域——max，maxl，maxr，sum，其中sum为该区间的和，max为该区间上的最大子段和，maxl为必须包含左端点的最大子段和，maxr为必须包含右端点的最大子段和。

可以用线段树来统计了注意求得的最大子段和中至少包含1个元素，所以出现了样例那样的输出负值。

修改时：

1、若左儿子的maxr和右儿子的maxl都为负，就从中取较大的为该节点的max（防止一个都不取），反之取二者中正的（都正就都取）。

2、将该节点的max用左右儿子的max更新。

3、该节点的maxl为左儿子的maxl与左儿子sum和右儿子maxl和的最大值。

4、该节点的maxr为右儿子的maxr与右儿子sum和左儿子maxr和的最大值。

5、该节点的sum为左右儿子的sum和。

查询时：

1、如果查询区间覆盖这一节点，将该节点信息返回。

2、如果只与一个儿子有交集，就返回在那个儿子中查找到的信息。

3、如果与两个儿子都有交集，就先分别计算出两个儿子的信息，然后按修改的方式将两个信息合并，然后返回。

4、最后返回的max值即为答案。

### py代码实现

略，再用py写这种题纯属想不开

### C++代码实现

```c++
//洛谷P4513

#include<bits/stdc++.h>
#define int long long
using namespace std;
#define endl "\n"
#define range(i, a, b) for (int i = (a); i < (b); ++i)

#define lc 2*p
#define rc 2*p+1
#define N 500005

int w[N];

struct node {
    int l, r, sum, ansl, ansr, ans;
} tr[N * 4];
void merge(int p){
    tr[p].sum = tr[lc].sum + tr[rc].sum;
    tr[p].ans = max(tr[lc].ans, max(tr[rc].ans, tr[rc].ansl + tr[lc].ansr));
    tr[p].ansl = max(tr[lc].sum + tr[rc].ansl, tr[lc].ansl);
    tr[p].ansr = max(tr[rc].sum + tr[lc].ansr, tr[rc].ansr);
}
void build(int p, int l, int r) {
    tr[p].l = l; tr[p].r = r;
    if (l == r) {
        tr[p].sum = w[l];
        tr[p].ansl = tr[p].ansr = tr[p].ans = w[l];
        return;
    }
    int m = (l + r) / 2;
    build(lc, l, m);
    build(rc, m + 1, r);
    merge(p);
}
void update(int p, int x, int k) {
    if (tr[p].l == x && tr[p].r == x) {
        tr[p].sum = k;
        tr[p].ansl = k;
        tr[p].ansr = k;
        tr[p].ans = k;
        return;
    }
    int m = (tr[p].l + tr[p].r) / 2;
    if (x <= m) update(lc, x, k);
    else update(rc, x, k);
    merge(p);
}

node query(int p, int x, int y) {
    if (x <= tr[p].l && tr[p].r <= y) return tr[p];
    int m = (tr[p].l + tr[p].r) / 2;
    if (y <= m){
        return query(lc, x, y);
    } 
    else if (x > m) {
        return query(rc, x, y);
    }
    else{
        node t, a = query(lc, x, y), b = query(rc, x, y);
        t.sum = a.sum + b.sum;
        t.ansl = max(a.ansl, a.sum + b.ansl);
        t.ansr = max(b.ansr, b.sum + a.ansr);
        t.ans = max({a.ans, b.ans, a.ansr + b.ansl});
        return t;
    }
}
signed main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    cout.tie(0);
    int n, m;
    cin >> n >> m;
    range(i, 0, n){
        cin >> w[i + 1];
    }
    build(1, 1, n);
    range(i, 0, m){
        int op; cin >> op;
        int x, y, k;
        if (op == 2){
            cin >> x >> k;
            update(1, x, k);
        }
        else{
            cin >> x >> y;
            if (x > y){
                cout << query(1, y, x).ans << endl;
            }
            else{
                cout << query(1, x, y).ans << endl;
            }
        }
    }
}
```
