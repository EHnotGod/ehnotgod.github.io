---
title: "H4 超绝浮点精度"
publishDate: 2026-09-02
description: "高精度浮点：用 Decimal 处理精度极限。"
category: algo
tags:
  - 其他
language: zh
---

### 题目情境

题目链接：待补充

**题目描述**

"荒泷卡牌天下第一斗"酷爱卡牌，尤其是最近马上要上线的"七圣召唤"，荒泷一斗想在 2.3 版本前集齐全部种类的卡牌，但他不精于计算，所以他找来了你、战力第一的旅行者帮忙。

已知"七圣召唤"共有 $K$ 张不同的卡牌，荒泷一斗的资金够买 $N$ 个卡包。每个卡包能随机从 $K$ 种卡牌中抽到一张。现给出 $N$ 和 $K$，他想问你要集齐全部种类的卡牌所需的期望卡包数，以及 $N$ 个卡包能开出的期望卡牌种类数。

**输入格式**

第一行输入两个整数 $N$ 和 $K$。$N$ 表示卡包数，$K$ 表示卡牌种类数（$1\le N\le 10^6,\ 1\le K\le 10^6$）。

**输出格式**

第一行输出两个浮点数，分别是集齐全部种类的卡牌所需的期望卡包数，和 $N$ 个卡包能开出的期望卡牌种类数，中间用空格间隔（答案与标准答案相差 $10^{-6}$ 以内就算正确）。

输入 #1

```
3 3
```

输出 #1

```
5.50000000 2.11111111
```

输入 #2

```
4 3
```

输出 #2

```
5.50000000 2.40740741
```

**说明/提示**

本邪教为 py 邪教，方法是使用 Python 的 Decimal 提升精度，在 WA 与 T 之间徘徊。

### 算法解析：

两问本质都是期望计算：

1. **集齐全部 $K$ 种所需的期望卡包数**：经典优惠券收集问题。当已集齐 $i$ 种时，抽到新种类的概率为 $\frac{K-i}{K}$，期望还需 $\frac{K}{K-i}$ 包。故总期望 $=\sum_{i=0}^{K-1}\frac{K}{K-i}=K\sum_{j=1}^{K}\frac1j$。直接浮点累加 $K$ 项在 $K$ 大时误差累积，用高精度 `Decimal` 提升精度。

2. **$N$ 个卡包能开出的期望种类数**：对每种卡牌，$N$ 包都没开到的概率为 $\left(1-\frac1K\right)^N$，故至少开到一次的概率为 $1-\left(1-\frac1K\right)^N$，期望种类数 $=K\left(1-\left(1-\frac1K\right)^N\right)$。幂运算 `**` 在 Decimal 下同样高精度。

### Python代码实现

```python
from decimal import Decimal, getcontext

getcontext().prec = 200

n, k = map(int, input().split())
n = Decimal(n)
k = Decimal(k)

ans1 = Decimal(0)
for i in range(int(k)):
    ans1 += k / Decimal(i + 1)

ans2 = k * (Decimal(1) - (Decimal(1) - Decimal(1) / k) ** n)

print(ans1, ans2)
```
