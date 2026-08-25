---
title: "k-means算法"
publishDate: 2026-08-08
description: "k-means 聚类：无监督学习，迭代更新簇中心。"
category: ml
tags:
  - 机器学习
language: zh
---

# k-means 算法

## 一、什么是 k-means？

**k-means** 是一种**无监督学习**中的**聚类（Clustering）**算法。它的目标很简单：

> 把一堆没有标签的数据，按照"相似程度"自动分成 $k$ 组（簇）。

比如：

- 给一堆用户画像，分成几类人群
- 把图片里的颜色聚成几种主色调
- 把文章分成几个主题

我们不需要提前告诉机器"每类长什么样"，机器自己找规律，这就是"无监督"。

---

## 二、算法步骤

假设数据是二维平面上的点，$k=3$：

1. **初始化**：随机挑 $k$ 个点作为初始中心 $C_1, C_2, \dots, C_k$
2. **分配**：对每个点 $x$，计算它到每个中心的距离（通常用欧氏距离），把它分给最近的中心
3. **更新**：对每个簇，重新计算所有点的均值，作为新的中心
4. **迭代**：重复步骤 2、3，直到中心位置几乎不变（或达到最大迭代次数）

> 距离公式（欧氏距离）：
>
> $$
> d(x, C) = \sqrt{(x_1 - C_1)^2 + (x_2 - C_2)^2}
> $$

---

## 三、Python 代码实现

用一个简单的 Python 例子，自己动手实现一遍（不依赖 sklearn）：

```python
import numpy as np
import matplotlib.pyplot as plt

def kmeans(X, k, max_iter=100):
    # 1. 随机初始化 k 个中心
    centroids = X[np.random.choice(len(X), k, replace=False)]

    for _ in range(max_iter):
        # 2. 分配：每个点归到最近的中心
        dists = np.linalg.norm(X[:, None] - centroids, axis=2)
        labels = np.argmin(dists, axis=1)

        # 3. 更新：用簇内均值作为新中心
        new_centroids = np.array([
            X[labels == i].mean(axis=0) for i in range(k)
        ])

        # 4. 中心不变则提前结束
        if np.allclose(centroids, new_centroids):
            break
        centroids = new_centroids

    return labels, centroids

# 造一点模拟数据（3 个"团"）
np.random.seed(0)
X = np.vstack([
    np.random.randn(50, 2) + [0, 0],
    np.random.randn(50, 2) + [5, 5],
    np.random.randn(50, 2) + [0, 8],
])

labels, centroids = kmeans(X, k=3)

# 画图
plt.scatter(X[:, 0], X[:, 1], c=labels, cmap="viridis")
plt.scatter(centroids[:, 0], centroids[:, 1], c="red", marker="x", s=200)
plt.title("k-means 聚类结果")
plt.show()
```

---

## 四、特点

**优点：**
- 思想简单，实现容易，速度快
- 适合大数据集

**缺点：**
- 需要**事先指定 k**（分几类）
- 对初始中心敏感，不同初始值可能得到不同结果
- 对**异常点**敏感
- 只能发现"球形"簇，对形状复杂的簇效果差
- 容易陷入局部最优

---

## 五、怎么选 k？

常用方法：

1. **肘部法则（Elbow Method）**：画出"k 和误差（SSE）"的曲线，找拐点。
   - 误差：每个点到所属中心距离的平方和
   - k 增大，误差一定下降，但到某个点后下降变缓，这个"拐点"就是合适的 k

2. **轮廓系数（Silhouette Coefficient）**：衡量簇内紧凑、簇间分离的程度，越大越好。

---