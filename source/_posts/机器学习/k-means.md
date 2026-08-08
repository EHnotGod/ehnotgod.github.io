---
title: "k-means算法"
categories:
- [机器学习]
tags:
- 机器学习
mathjax: true
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

## 二、核心思想

k-means 的想法非常朴素：

1. 先随便选 $k$ 个点当"中心"（centroid）
2. 每个数据点都归到离自己**最近**的中心
3. 每类里所有点的"平均位置"就是新的中心
4. 重复第 2、3 步，直到中心不再变化

名字的由来：
- **k**：要分成 k 个簇
- **means**：用"平均值"（mean）来更新中心

---

## 三、算法步骤

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

## 四、一个直观的小例子

想象桌上有几个点，想分成 2 簇：

```
初始：随机选两个中心 ★  ★
          ·
      ·       ★        ·
              ·     ·
   ★        ·       ·
```

每次迭代，点跟着最近的中心走，中心又跟着簇里的点"平均"走。来回几次后，中心和簇都不再动，聚类完成。

**收敛的标志**：所有簇的成员不再改变，中心也就不再移动。

---

## 五、Python 代码实现

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

如果想省事，直接用 scikit-learn：

```python
from sklearn.cluster import KMeans

model = KMeans(n_clusters=3, random_state=0)
labels = model.fit_predict(X)
centroids = model.cluster_centers_
```

---

## 六、优缺点

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

## 七、怎么选 k？

常用方法：

1. **肘部法则（Elbow Method）**：画出"k 和误差（SSE）"的曲线，找拐点。
   - 误差：每个点到所属中心距离的平方和
   - k 增大，误差一定下降，但到某个点后下降变缓，这个"拐点"就是合适的 k

2. **轮廓系数（Silhouette Coefficient）**：衡量簇内紧凑、簇间分离的程度，越大越好。

---

## 八、总结

一句话记住 k-means：

> **"先随便定 k 个中心，反复让点找最近的中心、中心跟点的平均，直到大家都安分下来。"**

它是聚类算法里最经典、最常用的入门算法，理解了它，再学其他聚类算法（如 DBSCAN、层次聚类）会容易很多。

