---
title: "机器学习与深度学习笔记"
title_en: "Machine Learning & Deep Learning Notes"
description: "从决策树、随机森林、k-means 到自动微分与反向传播，记录模型原理与从零实现时踩过的坑。"
description_en: "From decision trees, random forests and k-means to autodiff and backpropagation — notes on the maths and the from-scratch implementations."
bloglist:
  - 决策树算法
  - 随机森林
  - k-means算法
  - 自动微分与反向传播
  - torch语法学习1
---

这几篇是同一个思路下的产物：先用 numpy 把模型手写一遍（决策树的分裂准则、随机森林的袋外估计、
k-means 的收敛条件），再顺着 Dezero 的思路把自动微分和反向传播也拆开看。

手写一遍之后再回头看框架里的 `backward()`，很多东西才真正接上。
