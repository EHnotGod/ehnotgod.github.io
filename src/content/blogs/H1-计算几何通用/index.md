---
title: "H1 计算几何通用"
publishDate: 2026-09-01
updatedDate: 2026-11-09
description: "计算几何专题讲解：精度建模、二维几何模板、凸包切线、闵可夫斯基和、旋转卡壳、半平面交、最小覆盖圆与竞赛题单，附章节索引和 C++ 代码。"
category: algo
tags:
  - 其他
language: zh
---

本页收录《计算几何专题讲解》完整 132 页课件，以及最新的计算几何 C++ 模板。

[查看或下载完整 PDF](/downloads/computational-geometry/main.pdf) · <a href="/downloads/computational-geometry/ji.cpp" download>下载完整 C++ 源码</a> · [代码模板](#代码模板)

## 目录索引

目录按“章节 → 小节”展示，页码与 PDF 一致，点击标题即可跳转；桌面端也可使用右侧目录。

- **[课件封面与原文目录](#课件封面与原文目录)**（第 1–3 页）

- **[1 引言](#1-引言)**（第 4–18 页）

<details>
<summary>展开“1 引言”的小节索引</summary>

- [1.1 精度建模](#11-精度建模)（第 5–8 页）
- [1.2 案例研究：Keeping the Dogs Apart](#12-案例研究keeping-the-dogs-apart)（第 9–13 页）
- [1.3 浮点数求和](#13-浮点数求和)（第 14–15 页）
- [1.4 常用数学函数](#14-常用数学函数)（第 16–18 页）

</details>

- **[2 二维计算几何模板](#2-二维计算几何模板)**（第 19–76 页）

<details>
<summary>展开“2 二维计算几何模板”的小节索引</summary>

- [2.1 点](#21-点)（第 20–36 页）
- [2.2 直线](#22-直线)（第 37–50 页）
- [2.3 线段](#23-线段)（第 51–58 页）
- [2.4 多边形](#24-多边形)（第 59–69 页）
- [2.5 圆](#25-圆)（第 70–76 页）

</details>

- **[3 更多高级算法](#3-更多高级算法)**（第 77–93 页）

<details>
<summary>展开“3 更多高级算法”的小节索引</summary>

- [3.1 凸包切线与凸包外点距离](#31-凸包切线与凸包外点距离)（第 78–80 页）
- [3.2 闵可夫斯基和](#32-闵可夫斯基和)（第 81–82 页）
- [3.3 旋转卡壳](#33-旋转卡壳)（第 83–84 页）
- [3.4 半平面交](#34-半平面交)（第 85–89 页）
- [3.5 欧拉公式与皮克定理](#35-欧拉公式与皮克定理)（第 90 页）
- [3.6 随机增量法与最小覆盖圆](#36-随机增量法与最小覆盖圆)（第 91–93 页）

</details>

- **[4 杂题选讲](#4-杂题选讲)**（第 94–113 页）

<details>
<summary>展开“4 杂题选讲”的小节索引</summary>

- [4.1 雷达安装](#41-雷达安装)（第 95–96 页）
- [4.2 意大利美食](#42-意大利美食)（第 97–98 页）
- [4.3 行对](#43-行对)（第 99–100 页）
- [4.4 Dazzling stars](#44-dazzling-stars)（第 101–102 页）
- [4.5 我将如潮水般归来](#45-我将如潮水般归来)（第 103–104 页）
- [4.7 碰撞伤害](#47-碰撞伤害)（第 105–106 页）
- [4.8 楼观楼观楼楼时间到了](#48-楼观楼观楼楼时间到了)（第 107–109 页）
- [4.9 Parallel Lines](#49-parallel-lines)（第 110–111 页）
- [4.10 博物馆奇妙夜 2](#410-博物馆奇妙夜-2)（第 112–113 页）

</details>

- **[5 后记](#5-后记)**（第 114–131 页）

<details>
<summary>展开“5 后记”的小节索引</summary>

- [5.1 总结](#51-总结)（第 115 页）
- [5.2 比赛建议](#52-比赛建议)（第 116–117 页）
- [5.3 计算几何综合题单](#53-计算几何综合题单)（第 118–124 页）
- [5.4 题单难度与标签](#54-题单难度与标签)（第 125–131 页）

</details>

- **[参考资料](#参考资料)**（第 132 页）

- **[代码模板](#代码模板)**

<details>
<summary>展开 C++ 模板模块索引</summary>

- [代码 1：头文件与配置](#代码-1头文件与配置)
- [代码 2：点与向量](#代码-2点与向量)
- [代码 3：直线](#代码-3直线)
- [代码 4：线段](#代码-4线段)
- [代码 5：多边形与凸包](#代码-5多边形与凸包)
- [代码 6：圆与交点](#代码-6圆与交点)
- [代码 7：凸包切线](#代码-7凸包切线)
- [代码 8：半平面交](#代码-8半平面交)
- [代码 9：闵可夫斯基和](#代码-9闵可夫斯基和)
- [代码 10：最小覆盖圆](#代码-10最小覆盖圆)
- [代码 11：主程序](#代码-11主程序)

</details>

## 课件封面与原文目录

*第 1–3 页*

![计算几何专题讲解，第 1 页：课件封面与原文目录](images/H1-001.webp)

![计算几何专题讲解，第 2 页：课件封面与原文目录](images/H1-002.webp)

![计算几何专题讲解，第 3 页：课件封面与原文目录](images/H1-003.webp)

[↑ 返回目录索引](#目录索引)

## 1 引言

*第 4 页*

![计算几何专题讲解，第 4 页：1 引言](images/H1-004.webp)

[↑ 返回目录索引](#目录索引)

### 1.1 精度建模

*第 5–8 页*

![计算几何专题讲解，第 5 页：1.1 精度建模](images/H1-005.webp)

![计算几何专题讲解，第 6 页：1.1 精度建模](images/H1-006.webp)

![计算几何专题讲解，第 7 页：1.1 精度建模](images/H1-007.webp)

![计算几何专题讲解，第 8 页：1.1 精度建模](images/H1-008.webp)

[↑ 返回目录索引](#目录索引)

### 1.2 案例研究：Keeping the Dogs Apart

*第 9 页*

![计算几何专题讲解，第 9 页：1.2 案例研究：Keeping the Dogs Apart](images/H1-009.webp)

**1.2.1 看起来很对但过不去的代码**

*第 10–11 页*

![计算几何专题讲解，第 10 页：1.2.1 看起来很对但过不去的代码](images/H1-010.webp)

![计算几何专题讲解，第 11 页：1.2.1 看起来很对但过不去的代码](images/H1-011.webp)

**1.2.2 误差分析**

*第 12 页*

![计算几何专题讲解，第 12 页：1.2.2 误差分析](images/H1-012.webp)

**1.2.3 巧解**

*第 13 页*

![计算几何专题讲解，第 13 页：1.2.3 巧解](images/H1-013.webp)

[↑ 返回目录索引](#目录索引)

### 1.3 浮点数求和

**1.3.1 更精确的浮点数求和**

*第 14 页*

![计算几何专题讲解，第 14 页：1.3.1 更精确的浮点数求和](images/H1-014.webp)

**1.3.2 stableSum 模板**

*第 15 页*

![计算几何专题讲解，第 15 页：1.3.2 stableSum 模板](images/H1-015.webp)

[↑ 返回目录索引](#目录索引)

### 1.4 常用数学函数

**1.4.1 三角函数与反三角函数**

*第 16 页*

![计算几何专题讲解，第 16 页：1.4.1 三角函数与反三角函数](images/H1-016.webp)

**1.4.2 数值处理与精度控制**

*第 17 页*

![计算几何专题讲解，第 17 页：1.4.2 数值处理与精度控制](images/H1-017.webp)

**1.4.3 Python 高精度数值与整数上限**

*第 18 页*

![计算几何专题讲解，第 18 页：1.4.3 Python 高精度数值与整数上限](images/H1-018.webp)

[↑ 返回目录索引](#目录索引)

## 2 二维计算几何模板

*第 19 页*

![计算几何专题讲解，第 19 页：2 二维计算几何模板](images/H1-019.webp)

[↑ 返回目录索引](#目录索引)

### 2.1 点

**2.1.1 基本定义**

*第 20 页*

![计算几何专题讲解，第 20 页：2.1.1 基本定义](images/H1-020.webp)

**2.1.2 辅助函数**

*第 21 页*

![计算几何专题讲解，第 21 页：2.1.2 辅助函数](images/H1-021.webp)

**2.1.3 平移**

*第 22 页*

![计算几何专题讲解，第 22 页：2.1.3 平移](images/H1-022.webp)

**2.1.4 缩放**

*第 23 页*

![计算几何专题讲解，第 23 页：2.1.4 缩放](images/H1-023.webp)

**2.1.5 旋转与复数**

*第 24–25 页*

![计算几何专题讲解，第 24 页：2.1.5 旋转与复数](images/H1-024.webp)

![计算几何专题讲解，第 25 页：2.1.5 旋转与复数](images/H1-025.webp)

**2.1.6 点积**

*第 26 页*

![计算几何专题讲解，第 26 页：2.1.6 点积](images/H1-026.webp)

**2.1.7 叉积、夹角与方向判断**

*第 27–33 页*

![计算几何专题讲解，第 27 页：2.1.7 叉积、夹角与方向判断](images/H1-027.webp)

![计算几何专题讲解，第 28 页：2.1.7 叉积、夹角与方向判断](images/H1-028.webp)

![计算几何专题讲解，第 29 页：2.1.7 叉积、夹角与方向判断](images/H1-029.webp)

![计算几何专题讲解，第 30 页：2.1.7 叉积、夹角与方向判断](images/H1-030.webp)

![计算几何专题讲解，第 31 页：2.1.7 叉积、夹角与方向判断](images/H1-031.webp)

![计算几何专题讲解，第 32 页：2.1.7 叉积、夹角与方向判断](images/H1-032.webp)

![计算几何专题讲解，第 33 页：2.1.7 叉积、夹角与方向判断](images/H1-033.webp)

**2.1.8 极角排序**

*第 34–36 页*

![计算几何专题讲解，第 34 页：2.1.8 极角排序](images/H1-034.webp)

![计算几何专题讲解，第 35 页：2.1.8 极角排序](images/H1-035.webp)

![计算几何专题讲解，第 36 页：2.1.8 极角排序](images/H1-036.webp)

[↑ 返回目录索引](#目录索引)

### 2.2 直线

**2.2.1 基本定义与表示方式**

*第 37–40 页*

![计算几何专题讲解，第 37 页：2.2.1 基本定义与表示方式](images/H1-037.webp)

![计算几何专题讲解，第 38 页：2.2.1 基本定义与表示方式](images/H1-038.webp)

![计算几何专题讲解，第 39 页：2.2.1 基本定义与表示方式](images/H1-039.webp)

![计算几何专题讲解，第 40 页：2.2.1 基本定义与表示方式](images/H1-040.webp)

**2.2.2 点与直线的位置关系**

*第 41 页*

![计算几何专题讲解，第 41 页：2.2.2 点与直线的位置关系](images/H1-041.webp)

**2.2.3 点到直线的距离与平方距离**

*第 42–43 页*

![计算几何专题讲解，第 42 页：2.2.3 点到直线的距离与平方距离](images/H1-042.webp)

![计算几何专题讲解，第 43 页：2.2.3 点到直线的距离与平方距离](images/H1-043.webp)

**2.2.4 过一点的垂线**

*第 44 页*

![计算几何专题讲解，第 44 页：2.2.4 过一点的垂线](images/H1-044.webp)

**2.2.5 沿直线排序**

*第 45 页*

![计算几何专题讲解，第 45 页：2.2.5 沿直线排序](images/H1-045.webp)

**2.2.6 沿指定方向平移**

*第 46 页*

![计算几何专题讲解，第 46 页：2.2.6 沿指定方向平移](images/H1-046.webp)

**2.2.7 直线交点**

*第 47–48 页*

![计算几何专题讲解，第 47 页：2.2.7 直线交点](images/H1-047.webp)

![计算几何专题讲解，第 48 页：2.2.7 直线交点](images/H1-048.webp)

**2.2.8 正交投影与反射**

*第 49–50 页*

![计算几何专题讲解，第 49 页：2.2.8 正交投影与反射](images/H1-049.webp)

![计算几何专题讲解，第 50 页：2.2.8 正交投影与反射](images/H1-050.webp)

[↑ 返回目录索引](#目录索引)

### 2.3 线段

**2.3.1 点在线段为直径的圆内**

*第 51 页*

![计算几何专题讲解，第 51 页：2.3.1 点在线段为直径的圆内](images/H1-051.webp)

**2.3.2 点在线段上**

*第 52 页*

![计算几何专题讲解，第 52 页：2.3.2 点在线段上](images/H1-052.webp)

**2.3.3 线段与线段交点**

*第 53–55 页*

![计算几何专题讲解，第 53 页：2.3.3 线段与线段交点](images/H1-053.webp)

![计算几何专题讲解，第 54 页：2.3.3 线段与线段交点](images/H1-054.webp)

![计算几何专题讲解，第 55 页：2.3.3 线段与线段交点](images/H1-055.webp)

**2.3.4 点到线段的距离**

*第 56–57 页*

![计算几何专题讲解，第 56 页：2.3.4 点到线段的距离](images/H1-056.webp)

![计算几何专题讲解，第 57 页：2.3.4 点到线段的距离](images/H1-057.webp)

**2.3.5 线段到线段的距离**

*第 58 页*

![计算几何专题讲解，第 58 页：2.3.5 线段到线段的距离](images/H1-058.webp)

[↑ 返回目录索引](#目录索引)

### 2.4 多边形

**2.4.1 多边形面积**

*第 59 页*

![计算几何专题讲解，第 59 页：2.4.1 多边形面积](images/H1-059.webp)

**2.4.2 射线法判点**

*第 60–63 页*

![计算几何专题讲解，第 60 页：2.4.2 射线法判点](images/H1-060.webp)

![计算几何专题讲解，第 61 页：2.4.2 射线法判点](images/H1-061.webp)

![计算几何专题讲解，第 62 页：2.4.2 射线法判点](images/H1-062.webp)

![计算几何专题讲解，第 63 页：2.4.2 射线法判点](images/H1-063.webp)

**凸多边形内严格判点**

*第 64 页*

![计算几何专题讲解，第 64 页：凸多边形内严格判点](images/H1-064.webp)

**2.4.3 凸包**

*第 65–69 页*

![计算几何专题讲解，第 65 页：2.4.3 凸包](images/H1-065.webp)

![计算几何专题讲解，第 66 页：2.4.3 凸包](images/H1-066.webp)

![计算几何专题讲解，第 67 页：2.4.3 凸包](images/H1-067.webp)

![计算几何专题讲解，第 68 页：2.4.3 凸包](images/H1-068.webp)

![计算几何专题讲解，第 69 页：2.4.3 凸包](images/H1-069.webp)

[↑ 返回目录索引](#目录索引)

### 2.5 圆

**2.5.1 外接圆**

*第 70–71 页*

![计算几何专题讲解，第 70 页：2.5.1 外接圆](images/H1-070.webp)

![计算几何专题讲解，第 71 页：2.5.1 外接圆](images/H1-071.webp)

**2.5.2 圆与直线的交点**

*第 72–73 页*

![计算几何专题讲解，第 72 页：2.5.2 圆与直线的交点](images/H1-072.webp)

![计算几何专题讲解，第 73 页：2.5.2 圆与直线的交点](images/H1-073.webp)

**2.5.3 圆与圆的交点**

*第 74–76 页*

![计算几何专题讲解，第 74 页：2.5.3 圆与圆的交点](images/H1-074.webp)

![计算几何专题讲解，第 75 页：2.5.3 圆与圆的交点](images/H1-075.webp)

![计算几何专题讲解，第 76 页：2.5.3 圆与圆的交点](images/H1-076.webp)

[↑ 返回目录索引](#目录索引)

## 3 更多高级算法

*第 77 页*

![计算几何专题讲解，第 77 页：3 更多高级算法](images/H1-077.webp)

[↑ 返回目录索引](#目录索引)

### 3.1 凸包切线与凸包外点距离

*第 78–80 页*

![计算几何专题讲解，第 78 页：3.1 凸包切线与凸包外点距离](images/H1-078.webp)

![计算几何专题讲解，第 79 页：3.1 凸包切线与凸包外点距离](images/H1-079.webp)

![计算几何专题讲解，第 80 页：3.1 凸包切线与凸包外点距离](images/H1-080.webp)

[↑ 返回目录索引](#目录索引)

### 3.2 闵可夫斯基和

*第 81–82 页*

![计算几何专题讲解，第 81 页：3.2 闵可夫斯基和](images/H1-081.webp)

![计算几何专题讲解，第 82 页：3.2 闵可夫斯基和](images/H1-082.webp)

[↑ 返回目录索引](#目录索引)

### 3.3 旋转卡壳

*第 83–84 页*

![计算几何专题讲解，第 83 页：3.3 旋转卡壳](images/H1-083.webp)

![计算几何专题讲解，第 84 页：3.3 旋转卡壳](images/H1-084.webp)

[↑ 返回目录索引](#目录索引)

### 3.4 半平面交

*第 85–89 页*

![计算几何专题讲解，第 85 页：3.4 半平面交](images/H1-085.webp)

![计算几何专题讲解，第 86 页：3.4 半平面交](images/H1-086.webp)

![计算几何专题讲解，第 87 页：3.4 半平面交](images/H1-087.webp)

![计算几何专题讲解，第 88 页：3.4 半平面交](images/H1-088.webp)

![计算几何专题讲解，第 89 页：3.4 半平面交](images/H1-089.webp)

[↑ 返回目录索引](#目录索引)

### 3.5 欧拉公式与皮克定理

*第 90 页*

![计算几何专题讲解，第 90 页：3.5 欧拉公式与皮克定理](images/H1-090.webp)

[↑ 返回目录索引](#目录索引)

### 3.6 随机增量法与最小覆盖圆

*第 91–93 页*

![计算几何专题讲解，第 91 页：3.6 随机增量法与最小覆盖圆](images/H1-091.webp)

![计算几何专题讲解，第 92 页：3.6 随机增量法与最小覆盖圆](images/H1-092.webp)

![计算几何专题讲解，第 93 页：3.6 随机增量法与最小覆盖圆](images/H1-093.webp)

[↑ 返回目录索引](#目录索引)

## 4 杂题选讲

*第 94 页*

![计算几何专题讲解，第 94 页：4 杂题选讲](images/H1-094.webp)

[↑ 返回目录索引](#目录索引)

### 4.1 雷达安装

*第 95–96 页*

![计算几何专题讲解，第 95 页：4.1 雷达安装](images/H1-095.webp)

![计算几何专题讲解，第 96 页：4.1 雷达安装](images/H1-096.webp)

[↑ 返回目录索引](#目录索引)

### 4.2 意大利美食

*第 97–98 页*

![计算几何专题讲解，第 97 页：4.2 意大利美食](images/H1-097.webp)

![计算几何专题讲解，第 98 页：4.2 意大利美食](images/H1-098.webp)

[↑ 返回目录索引](#目录索引)

### 4.3 行对

*第 99–100 页*

![计算几何专题讲解，第 99 页：4.3 行对](images/H1-099.webp)

![计算几何专题讲解，第 100 页：4.3 行对](images/H1-100.webp)

[↑ 返回目录索引](#目录索引)

### 4.4 Dazzling stars

*第 101–102 页*

![计算几何专题讲解，第 101 页：4.4 Dazzling stars](images/H1-101.webp)

![计算几何专题讲解，第 102 页：4.4 Dazzling stars](images/H1-102.webp)

[↑ 返回目录索引](#目录索引)

### 4.5 我将如潮水般归来

*第 103–104 页*

![计算几何专题讲解，第 103 页：4.5 我将如潮水般归来](images/H1-103.webp)

![计算几何专题讲解，第 104 页：4.5 我将如潮水般归来](images/H1-104.webp)

[↑ 返回目录索引](#目录索引)

### 4.7 碰撞伤害

*第 105–106 页*

![计算几何专题讲解，第 105 页：4.7 碰撞伤害](images/H1-105.webp)

![计算几何专题讲解，第 106 页：4.7 碰撞伤害](images/H1-106.webp)

[↑ 返回目录索引](#目录索引)

### 4.8 楼观楼观楼楼时间到了

*第 107–109 页*

![计算几何专题讲解，第 107 页：4.8 楼观楼观楼楼时间到了](images/H1-107.webp)

![计算几何专题讲解，第 108 页：4.8 楼观楼观楼楼时间到了](images/H1-108.webp)

![计算几何专题讲解，第 109 页：4.8 楼观楼观楼楼时间到了](images/H1-109.webp)

[↑ 返回目录索引](#目录索引)

### 4.9 Parallel Lines

*第 110–111 页*

![计算几何专题讲解，第 110 页：4.9 Parallel Lines](images/H1-110.webp)

![计算几何专题讲解，第 111 页：4.9 Parallel Lines](images/H1-111.webp)

[↑ 返回目录索引](#目录索引)

### 4.10 博物馆奇妙夜 2

*第 112–113 页*

![计算几何专题讲解，第 112 页：4.10 博物馆奇妙夜 2](images/H1-112.webp)

![计算几何专题讲解，第 113 页：4.10 博物馆奇妙夜 2](images/H1-113.webp)

[↑ 返回目录索引](#目录索引)

## 5 后记

*第 114 页*

![计算几何专题讲解，第 114 页：5 后记](images/H1-114.webp)

[↑ 返回目录索引](#目录索引)

### 5.1 总结

*第 115 页*

![计算几何专题讲解，第 115 页：5.1 总结](images/H1-115.webp)

[↑ 返回目录索引](#目录索引)

### 5.2 比赛建议

*第 116–117 页*

![计算几何专题讲解，第 116 页：5.2 比赛建议](images/H1-116.webp)

![计算几何专题讲解，第 117 页：5.2 比赛建议](images/H1-117.webp)

[↑ 返回目录索引](#目录索引)

### 5.3 计算几何综合题单

**综合题单：2024 省赛与邀请赛**

*第 118 页*

![计算几何专题讲解，第 118 页：综合题单：2024 省赛与邀请赛](images/H1-118.webp)

**综合题单：2024 区域赛**

*第 119 页*

![计算几何专题讲解，第 119 页：综合题单：2024 区域赛](images/H1-119.webp)

**综合题单：2025 省赛与邀请赛**

*第 120–121 页*

![计算几何专题讲解，第 120 页：综合题单：2025 省赛与邀请赛](images/H1-120.webp)

![计算几何专题讲解，第 121 页：综合题单：2025 省赛与邀请赛](images/H1-121.webp)

**综合题单：2025 区域赛**

*第 122–123 页*

![计算几何专题讲解，第 122 页：综合题单：2025 区域赛](images/H1-122.webp)

![计算几何专题讲解，第 123 页：综合题单：2025 区域赛](images/H1-123.webp)

**综合题单：2026 省赛与邀请赛**

*第 124 页*

![计算几何专题讲解，第 124 页：综合题单：2026 省赛与邀请赛](images/H1-124.webp)

[↑ 返回目录索引](#目录索引)

### 5.4 题单难度与标签

**难度与标签：2024 省赛与邀请赛**

*第 125 页*

![计算几何专题讲解，第 125 页：难度与标签：2024 省赛与邀请赛](images/H1-125.webp)

**难度与标签：2024 区域赛**

*第 126 页*

![计算几何专题讲解，第 126 页：难度与标签：2024 区域赛](images/H1-126.webp)

**难度与标签：2025 省赛与邀请赛**

*第 127–128 页*

![计算几何专题讲解，第 127 页：难度与标签：2025 省赛与邀请赛](images/H1-127.webp)

![计算几何专题讲解，第 128 页：难度与标签：2025 省赛与邀请赛](images/H1-128.webp)

**难度与标签：2025 区域赛**

*第 129–130 页*

![计算几何专题讲解，第 129 页：难度与标签：2025 区域赛](images/H1-129.webp)

![计算几何专题讲解，第 130 页：难度与标签：2025 区域赛](images/H1-130.webp)

**难度与标签：2026 省赛与邀请赛**

*第 131 页*

![计算几何专题讲解，第 131 页：难度与标签：2026 省赛与邀请赛](images/H1-131.webp)

[↑ 返回目录索引](#目录索引)

## 参考资料

*第 132 页*

![计算几何专题讲解，第 132 页：参考资料](images/H1-132.webp)

[↑ 返回目录索引](#目录索引)

## 代码模板

以下代码按原文件顺序分块展示；需要整份复制时，可<a href="/downloads/computational-geometry/ji.cpp" download>下载完整 ji.cpp</a>。

### 代码 1：头文件与配置

```cpp
/*EHnotgod————
..............#######.....#.....#..............
..............#...........#.....#..............
..............#######.....#######..............
..............#...........#.....#..............
..............#######.....#.....#..............
*/

// 1.头文件(EH:?这也能算第一点?)
#include <bits/stdc++.h>
using namespace std;
#define endl "\n"
#define int long long
#define M_PI acos(-1)
#define range(i, a, b) for (int i = (a); i < (b); ++i)
typedef long double T;
#define debug(args...) println(cerr, "{} = {}", #args, tuple(args))
```

[↑ 返回目录索引](#目录索引)

### 代码 2：点与向量

```cpp
// 2.1 点
// 2.1.1基本定义
struct pt{
    T x, y;
    pt operator+(pt p){return{x+p.x, y+p.y};}
    pt operator-(pt p){return{x-p.x, y-p.y};}
    pt operator*(T d){return{x*d, y*d};}
    pt operator/(T d){return{x/d, y/d};} //注意不能除以0
    bool operator<(const pt& a) const {
    if (x != a.x) return x < a.x;
        return y < a.y;
    }
    bool operator==(const pt& other) const { return x == other.x && y == other.y; }
    bool operator!=(const pt& other) const { return !(*this == other); }
};
template<>
struct std::formatter<pt> {
    constexpr auto parse(auto& c) { return c.begin(); }
    auto format(const pt& p, auto& c) const {
        return std::format_to(c.out(), "({}, {})", p.x, p.y);
    }
};
T sq(pt p) {return p.x*p.x+ p.y*p.y;}
T absv(pt p){return sqrtl(sq(p));}

int sgn(T x){return(T(0)< x)-(x <T(0));}
// 2.1.3基本变换：平移
pt translate(pt v, pt p){
    return p + v;
}
// 2.1.4基本变换：缩放
pt scale(pt c,T factor, pt p){
    return c +(p - c)* factor;
}
// 2.1.5基本变换：旋转（逆时针）
pt rot(pt p,T a){
    return{p.x*cosl(a)- p.y*sinl(a), p.x*sinl(a)+ p.y*cosl(a)};}
pt perp(pt p){
    return{-p.y, p.x};
}
// 2.1.6 点积
T dot(pt v, pt w){
    return v.x* w.x+ v.y* w.y;
}
bool isPerp(pt v, pt w){
    return dot(v, w)==0;
}
// 2.1.7 叉积
T cross(pt v, pt w){return v.x* w.y- v.y* w.x;}
T angle(pt v, pt w){
    return abs(atan2(cross(v, w), dot(v, w)));
}
T orient(pt a, pt b, pt c){return cross(b - a, c - a);}
bool inAngle(pt a, pt b, pt c, pt p){
	if(orient(a, b, c)<0)swap(b, c);
	return orient(a, b, p)>=0&&orient(a, c, p)<=0;
}
T orientedAngle(pt a, pt b, pt c){
    if(orient(a, b, c)>=0){return angle(b - a, c - a);}
	else{return 2* M_PI -angle(b - a, c - a);
}
}
// 2.1.8 极角排序
bool half(pt p){
	return p.y>0||(p.y==0&& p.x<0);
}
void polarSort(vector<pt>&v){
    sort(v.begin(), v.end(),[](pt v, pt w){
        return make_tuple(half(v),0,sq(v))<
            make_tuple(half(w),cross(v,w),sq(w));
    });
}
```

[↑ 返回目录索引](#目录索引)

### 代码 3：直线

```cpp
// 2.2 直线
// 2.2.1 基本定义
struct line{
    pt v; T c;
    line(pt v, T c):v(v),c(c){} // 点斜式
    line(T a, T b, T c):v({b,-a}),c(c){} // 标准式(ax+by+c=0)
    line(pt p, pt q):v(q-p),c(cross(v,p)){} // 两点式
};
// 2.2.2点与直线的位置关系
T side(line ln, pt p){
    return cross(ln.v, p)- ln.c;}
// 2.2.3点到直线的距离
T dist(line ln, pt p){return abs(side(ln, p))/absv(ln.v);}
// 2.2.4过一点的垂线
line perpThrough(line ln, pt p){return{p, p +perp(ln.v)};}  
// 2.2.5沿直线排序   
bool cmpProj(line ln, pt p, pt q){return dot(ln.v, p)<dot(ln.v, q);}   
// 2.2.6沿指定方向平移    
line translate(line ln, pt t){return{ln.v, ln.c +cross(ln.v, t)};} 
// 2.2.7直线交点  
bool inter(line l1, line l2, pt &out){
    T d =cross(l1.v, l2.v); if(d == 0)return false;
    out =(l2.v* l1.c- l1.v* l2.c)/ d;
    return true;
}
// 2.2.8正交投影与反射
pt proj(line ln, pt p){return p -perp(ln.v)*side(ln, p)/sq(ln.v);}
pt refl(line ln, pt p){return p -perp(ln.v)*2*side(ln, p)/sq(ln.v);}
// 2.2.9点到直线的平方距离
T sqDist(line ln, pt p) {
    return side(ln, p) * side(ln, p) / sq(ln.v); 
}
```

[↑ 返回目录索引](#目录索引)

### 代码 4：线段

```cpp
// 2.3 线段
// 2.3.0 定义?没有定义，线段不TM就两个点吗
// 2.3.1点在线段为直径的圆上    
bool inDisk(pt a, pt b, pt p){return dot(a - p, b - p)<=0;}
// 2.3.2点在线段上    
bool onSegment(pt a, pt b, pt p){
    return orient(a, b, p)==0 && inDisk(a, b, p);
}
// 2.3.3线段与线段交点    
bool properInter(pt a, pt b, pt c, pt d, pt &out){    
    T oa =orient(c, d, a), ob =orient(c, d, b),         
      oc =orient(a, b, c), od =orient(a, b, d);
	if(oa * ob <0&& oc * od <0){
    	out =(a * ob - b * oa)/(ob - oa);
    	return true;
    }
	return false;
}
set<pt>inters(pt a, pt b, pt c, pt d){
  pt out;        
  if(properInter(a, b, c, d, out))return{out};  
  set<pt> s;      
  if(onSegment(c, d, a)) s.insert(a);
  if(onSegment(c, d, b)) s.insert(b);
  if(onSegment(a, b, c)) s.insert(c);
  if(onSegment(a, b, d)) s.insert(d);
  return s;
}// 如果|s|=1则只有一个交点；如果|s|=2则说明相交的区域是一条线段，并且中存的是其他两个端点

// 2.3.4点到线段的距离
T segPoint(pt a, pt b, pt p){
    if(a != b){
    	line l(a, b);
    	if(cmpProj(l, a, p)&& cmpProj(l, p, b))
            return dist(l, p);
		return min(absv(p - a),absv(p - b));
    }
	return absv(p - a);
}

// 2.3.5线段到线段的距离  
T segSeg(pt a, pt b, pt c, pt d){
  pt dummy;    
  if(properInter(a, b, c, d, dummy))return 0;
  return min({segPoint(a, b, c),segPoint(a, b, d), 
              segPoint(c, d, a),segPoint(c, d, b)});
}
```

[↑ 返回目录索引](#目录索引)

### 代码 5：多边形与凸包

```cpp
// 2.4 多边形
// 2.4.1多边形面积
T areaPolygon(vector<pt>p){
    T area =0.0;
	for(int i =0, n = p.size(); i < n; i++){
    	area +=cross(p[i], p[(i +1)% n]);
    }
	return abs(area)/2.0;
}
// 2.4.2 射线法：判断点是否在多边形内部
bool above(pt a, pt p){
    return p.y>= a.y;
}
bool crossesRay(pt a, pt p, pt q){
    return(above(a, q)-above(a, p))*
    	orient(a, p, q)>0;
}
// 这个strict可以自己调控，如果 strict=true（默认值），点在边上返回 false。如果 strict=false，点在边上返回 true。
bool inPolygon(vector<pt>p, pt a, bool strict=true){
    int numCrossings =0;
	for(int i =0, n = p.size(); i < n; i++){
        if(onSegment(p[i], p[(i +1)% n], a))return!strict;
            numCrossings +=crossesRay(a, p[i], p[(i +1)% n]);
    }
    return numCrossings & 1;
}
// 2.4.3凸包
bool turn_left(pt a, pt b, pt c) { 
    return sgn(cross(b - a, c - a)) > 0; 
}
vector<pt> convex_hull(vector<pt> a) {
    if (a.size() <= 2) return a;
    pt base = *min_element(a.begin(), a.end());
    sort(a.begin(), a.end(), [&](auto u, auto v) {
        return make_tuple(half(u - base), 0, sq(u- base)) < make_tuple(half(u - base), cross(u - base, v - base), sq(v - base));
    });
    vector<pt> ret;
    for (auto i : a) {
        while (ret.size() > 1 && !turn_left(ret[ret.size() - 2], ret[ret.size() - 1], i)) 
            ret.pop_back();
        ret.push_back(i);
    }
    return ret;
}

// 2.4.4 CCW判点-严格判断点 p 是否在凸多边形 A（CCW）内部，但是A必须逆时针排列
bool pointInConvexStrict(const vector<pt>& A, const pt& p) {
    int n = (int)A.size();
    if (n < 3) return false;
    if (sgn(orient(A[0], A[1], p)) <= 0) return false;
    if (sgn(orient(A[0], A[n-1], p)) >= 0) return false;

    int l = 1, r = n - 1;
    while (r - l > 1) {
        int mid = (l + r) >> 1;
        if (sgn(orient(A[0], A[mid], p)) > 0) l = mid;
        else r = mid;
    }
    return sgn(orient(A[l], A[l+1], p)) > 0;
}
```

[↑ 返回目录索引](#目录索引)

### 代码 6：圆与交点

```cpp
// 2.5圆
// 2.5.1 外接圆，返回的是外心！别问我为啥不返回半径，要算的话，自己逮个点算不就得了
pt circumCenter(pt a, pt b, pt c){
  b = b - a, c = c - a;
  return a +perp(b *sq(c)- c *sq(b))/cross(b, c)/2;
}

// 2.5.2圆与直线的交点
int circleLine(pt o,T r, line ln,pair<pt, pt>&out){
    T h2 = r * r - sqDist(ln, o);
	if(h2 >= 0){
    	pt p = proj(ln, o);
    	pt h = ln.v*sqrt(h2)/absv(ln.v);
        out = {p - h, p + h};
    }
	return 1+sgn(h2);
}

// 2.5.3圆与圆的交点
int circleCircle(pt o1,T r1, pt o2,T r2, pair<pt, pt>&out){
    pt d = o2 - o1;    
    T d2 =sq(d);
    if(d2 == 0){
		return 0;
    }
	T pd =(d2 + r1 * r1 - r2 * r2)/2;
    T h2 = r1 * r1 - pd * pd / d2;
    if(h2 >=0){ pt p = o1 + d * pd / d2, h =perp(d)*sqrt(h2 / d2); out = {p - h, p + h};}
    return 1 + sgn(h2);
}
```

[↑ 返回目录索引](#目录索引)

### 代码 7：凸包切线

```cpp
T getSum2(pt a, pt b, int flag){
    if (flag) return cross(a, b);
    else return cross(b, a);
}

T getSum(pt a, pt b, int flag){
    T x = dot(a, b);
    T y = flag ? cross(a, b) : cross(b, a);
    T z = y / (fabsl(x) + fabsl(y));
    return x >= 0 ? z : (y >= 0 ? 2 - z : -2 - z);
}
pt san(vector<pt>& con, pt st, pt q, int flag){
    int n = con.size(); // flag = 1：逆时针侧切线
    pt b = q + con[1] + con[n-1] - st * 3;
    auto f = [&](int i){return getSum(con[i] - st, b, flag);};
    int k = f(1) < f(n-1) ? 1 : -1;
    auto g = [&](int i){return f((i*k%n+n)%n);};
    int R = n-1, l = 1, r = R;
    if (g(R) >= g(0)){
        while (l < r){
            int m = (l+r)>>1;
            if (g(m) >= g(0)) r = m;
            else l = m+1;
        }
        R = l;
    }
    l = 0, r = R;
    while (l < r){
        int m = (l+r)>>1;
        if (g(m) <= g(m+1)) r = m;
        else l = m+1;
    }
    return con[(l*k%n+n)%n];
}
```

[↑ 返回目录索引](#目录索引)

### 代码 8：半平面交

```cpp
vector<pt> half_plane(vector<line> a) {
    const T eps = 1e-12L;
    for (auto &l : a) { T k = absv(l.v); l.v = l.v/k; l.c /= k; }
    sort(a.begin(), a.end(), [](line x, line y) {
        return half(x.v) != half(y.v) ? half(x.v) < half(y.v) : cross(x.v,y.v) > 0;
    });
    auto out = [&](line l, line x, line y) {
        pt p; return inter(x,y,p) && side(l,p) < -eps;
    };
    deque<line> q;
    for (line l : a) {
        while (q.size()>1 && out(l,q.back(),q[q.size()-2])) q.pop_back();
        while (q.size()>1 && out(l,q[0],q[1])) q.pop_front();
        if (!q.empty() && abs(cross(q.back().v,l.v)) < eps) {
            if (dot(q.back().v,l.v) < 0) return {};
            if (l.c <= q.back().c) continue;
            q.pop_back();
        }
        q.push_back(l);
    }
    while (q.size()>2 && out(q.front(),q.back(),q[q.size()-2])) q.pop_back();
    while (q.size()>2 && out(q.back(),q[0],q[1])) q.pop_front();
    vector<pt> res;
    if (q.size()<3) return res;
    for (int i=0; i<(int)q.size(); i++) {
        pt p; if (!inter(q[i],q[(i+1)%q.size()],p)) return {};
        res.push_back(p);
    }
    return res;
}
```

[↑ 返回目录索引](#目录索引)

### 代码 9：闵可夫斯基和

```cpp
vector<pt> minkowski(vector<pt> a, vector<pt> b){
    auto init = [](vector<pt>& p){
        rotate(p.begin(), min_element(p.begin(), p.end(),
            [](pt a, pt b){return tie(a.y,a.x)<tie(b.y,b.x);}), p.end());
    };
    init(a); init(b);
    int n=a.size(), m=b.size(), i=0, j=0;
    vector<pt> res;
    while(i<n || j<m){
        res.push_back(a[i%n]+b[j%m]);
        T c=i==n?-1:j==m?1:cross(a[(i+1)%n]-a[i%n],b[(j+1)%m]-b[j%m]);
        if(c>=0) i++;
        if(c<=0) j++;
    }
    return res;
}
```

[↑ 返回目录索引](#目录索引)

### 代码 10：最小覆盖圆

```cpp
// 2.5.4 最小覆盖圆，返回 {圆心, 半径}
pair<pt,T> minCircle(vector<pt> a){
    if(a.empty()) return {{0,0},0};
    shuffle(a.begin(),a.end(),mt19937(114514));
    pt o=a[0]; T r=0;
    auto out=[&](pt p){return sq(p-o)>r;};
    for(int i=0;i<a.size();i++) if(out(a[i])){
        o=a[i]; r=0;
        for(int j=0;j<i;j++) if(out(a[j])){
            o=(a[i]+a[j])/2; r=sq(a[i]-o);
            for(int k=0;k<j;k++) if(out(a[k])){
                if(orient(a[i],a[j],a[k]))
                    o=circumCenter(a[i],a[j],a[k]);
                else o=sq(a[i]-a[k])>sq(a[j]-a[k])
                    ?(a[i]+a[k])/2:(a[j]+a[k])/2;
                r=max({sq(a[i]-o),sq(a[j]-o),sq(a[k]-o)});
            }
        }
    }
    return {o,sqrtl(r)};
}
```

[↑ 返回目录索引](#目录索引)

### 代码 11：主程序

```cpp
// 快捷CV处
// vector<int> a(n, 0);
// vector<vector<int>> dp(n + 1, vector<int>(n + 1, 0));
void solve() {
	int n, m, a; cin >> n >> m >> a;

}

signed main() {
    ios::sync_with_stdio(0);
    cin.tie(0);
    cout.tie(0);
	int T; T = 1;
	// cin >> T;
	while (T--) {
		solve();
	}
	return 0;
}
```

[↑ 返回目录索引](#目录索引)
