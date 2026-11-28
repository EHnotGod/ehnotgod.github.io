---
title: "CNN 卷积神经网络"
publishDate: 2026-11-28
description: "从滑窗手算出发，推导卷积的输出尺寸、参数量与感受野，再手写 Conv2d 并训练图像分类器。"
category: technical
tags:
  - 基础模型算法
  - 深度学习底层
language: zh
---

给一张 $12\times12$ 的灰度图，判断里面是一条横线还是竖线。横线可能出现在任何一行。我们希望模型能在不同位置用同一套规则识别它，这正是卷积擅长做的事。

这是[基础模型算法](/zh/collection/basic-model-algorithms/)的第一篇。可以先跑下面的 $2\times2$ 手算，再用相同的规则读懂 PyTorch 中的卷积层。

## 1. 滑窗与权重共享

二维卷积读入一个局部窗口，把窗口与卷积核对应的元素相乘，再把乘积加起来。同一个卷积核沿着图像滑动，得到一张特征图。设输入的左上角是

$$
\begin{bmatrix}
1 & 2 & 3\\
5 & 6 & 7\\
9 & 10 & 11
\end{bmatrix},
\qquad
K=\begin{bmatrix}
1 & -1\\
1 & -1
\end{bmatrix}.
$$

第一格的输出为 $1-2+5-6=-2$。往右移一格得到 $2-3+6-7=-2$。这个核对左右亮度差有响应。实际训练时，核里的数字由梯度更新，模型可以在不同层学出不同的局部特征。

PyTorch 的 `Conv2d` 直接用核做乘加，因此严格说实现的是互相关。信号处理中的卷积会先翻转核。对可学习的核，两种记号的区别可以由权重的排列吸收。以下都采用 PyTorch 的约定。[PyTorch Conv2d 文档](https://docs.pytorch.org/docs/stable/generated/torch.nn.Conv2d.html)

### 1.1 多输入通道与多输出通道

输入用 `(N, C_in, H, W)` 表示。对 RGB 图像，$C_{\mathrm{in}}=3$。普通卷积中，每个输出通道拥有一个跨越所有输入通道的核，三个颜色通道各有一片权重，乘加结果汇总到同一个输出值。$C_{\mathrm{out}}$ 个核会得到 $C_{\mathrm{out}}$ 张特征图。

令 $\widetilde X$ 表示填充后的输入，省略批次下标。输出通道 $o$ 在位置 $(i,j)$ 的值是

$$
Y_{o,i,j}=b_o+\sum_{c,u,v}
W_{o,c,u,v}\,\widetilde X_{c,\,i s_h+u d_h,\,j s_w+v d_w}.
$$

求和遍历输入通道 $c$ 和核的坐标 $(u,v)$，$s$ 是步幅，$d$ 是膨胀率。反传时，同一个核元素在多个窗口里都被使用，所以它的梯度是各位置贡献的和。单个贡献等于上游梯度乘以该窗口对应的输入值。这正是[自动微分与反向传播](/zh/blog/自动微分与反向传播/)里梯度累加的同一个规则。

## 2. 输出尺寸、参数量与感受野

### 2.1 用公式检查形状

单看高度这一维。大小为 $K$、膨胀率为 $D$ 的核，覆盖的实际跨度是 $K_{\mathrm{eff}}=D(K-1)+1$。左右各补 $P$ 格、每次跨 $S$ 格，可放下的完整窗口数为

$$
H_{\mathrm{out}}=
\left\lfloor\frac{H_{\mathrm{in}}+2P-K_{\mathrm{eff}}}{S}\right\rfloor+1.
$$

宽度用相同公式单独计算。以 `Conv2d(3, 16, kernel_size=3, stride=2, padding=1)` 为例，`(8, 3, 32, 32)` 会变成 `(8, 16, 16, 16)`。如果步幅为 1、核为奇数且 $D=1$，每侧填充 $(K-1)/2$ 格可以保持尺寸。

### 2.2 参数有多少

普通卷积的权重形状为 `(C_out, C_in, K_h, K_w)`，每个输出通道还可以有一个偏置。上面的例子参数量为 $16(3\cdot3\cdot3+1)=448$，图像宽高变动也沿用这组权重。

分组卷积把输入和输出通道分成 $g$ 组，各组独立计算。权重形状变为 `(C_out, C_in / groups, K_h, K_w)`，两个通道数都必须能被 $g$ 整除。取 $g=C_{\mathrm{in}}$ 时就是逐通道卷积，常再接一个普通的 $1\times1$ 卷积混合通道。

### 2.3 堆叠后一个输出能看到多大范围

站在原图坐标上，记相邻两个特征点相隔 $j$ 格，单个特征点的理论感受野宽度为 $r$。初始为 $j=r=1$，经过核跨度 $K_{\mathrm{eff}}$、步幅 $S$ 的层后

$$
r_{\mathrm{new}}=r+(K_{\mathrm{eff}}-1)j,\qquad
j_{\mathrm{new}}=jS.
$$

依次通过 `3×3 Conv, stride=1`、`2×2 MaxPool, stride=2`、`3×3 Conv, stride=1`，感受野从 $1$ 变为 $3$、$4$、$8$。padding 会影响边上的有效输入范围，感受野公式描述的是理论跨度。

## 3. 用 NumPy 手写卷积前向

下面实现 `groups=1` 的版本，步幅、填充、膨胀率在两个空间维度上共用。循环只走输出位置，`tensordot` 同时完成批次和通道的乘加。最后用手算例子和 PyTorch 检查结果。

```python
import numpy as np
import torch
from torch.nn.functional import conv2d


def conv2d_numpy(x, weight, bias, stride=1, padding=0, dilation=1):
    if stride < 1 or padding < 0 or dilation < 1:
        raise ValueError("Invalid stride, padding, or dilation")
    n, channels, height, width = x.shape
    out_channels, kernel_channels, kh, kw = weight.shape
    if channels != kernel_channels or bias.shape != (out_channels,):
        raise ValueError("Input, weight, and bias shapes do not match")

    effective_h = dilation * (kh - 1) + 1
    effective_w = dilation * (kw - 1) + 1
    h_out = (height + 2 * padding - effective_h) // stride + 1
    w_out = (width + 2 * padding - effective_w) // stride + 1
    if h_out < 1 or w_out < 1:
        raise ValueError("Kernel does not fit the padded input")

    x = np.pad(x, ((0, 0), (0, 0), (padding, padding), (padding, padding)))
    result = np.empty(
        (n, out_channels, h_out, w_out), dtype=np.result_type(x, weight, bias)
    )
    for i in range(h_out):
        for j in range(w_out):
            row, col = i * stride, j * stride
            region = x[:, :, row:row + effective_h:dilation, col:col + effective_w:dilation]
            result[:, :, i, j] = (
                np.tensordot(region, weight, axes=((1, 2, 3), (1, 2, 3))) + bias
            )
    return result


image = np.arange(1.0, 17.0).reshape(1, 1, 4, 4)
edge = np.array([[[[1., -1.], [1., -1.]]]])
assert conv2d_numpy(image, edge, np.zeros(1))[0, 0, 0, 0] == -2

rng = np.random.default_rng(4)
x = rng.normal(size=(2, 3, 9, 8))
w = rng.normal(size=(4, 3, 3, 2))
b = rng.normal(size=(4,))
options = dict(stride=2, padding=1, dilation=2)
actual = conv2d_numpy(x, w, b, **options)
expected = conv2d(*(torch.from_numpy(a) for a in (x, w, b)), **options)
np.testing.assert_allclose(actual, expected.numpy())
print(actual.shape)
```

这个版本便于验证索引。实际框架可以重新组织窗口、使用矩阵乘法或选用专门的硬件内核，保持上述张量接口。

## 4. 训练一个最小的图像分类器

卷积后接 ReLU，让堆叠的层具有非线性。最大池化从每个窗口选出最大的响应并缩小特征图。这个例子关心线的方向，不关心线移动到了哪一行或哪一列，所以在分类前用全局平均池化，把每张特征图压成一个值。最后由全连接层把 16 个描述值映射到两个类别的 logits。

| 层 | 输出形状 |
| --- | --- |
| 输入 | `(N, 1, 12, 12)` |
| Conv + ReLU | `(N, 8, 12, 12)` |
| MaxPool | `(N, 8, 6, 6)` |
| Conv + ReLU | `(N, 16, 6, 6)` |
| AdaptiveAvgPool + Flatten | `(N, 16)` |
| Linear | `(N, 2)` |

下面的脚本会独立生成训练集和测试集，可直接运行，无需下载数据。

```python
import torch
from torch import nn

torch.manual_seed(0)
torch.set_num_threads(1)


def lines(count, seed):
    rng = torch.Generator().manual_seed(seed)
    images = 0.15 * torch.randn(count, 1, 12, 12, generator=rng)
    labels = torch.randint(0, 2, (count,), generator=rng)
    starts = torch.randint(0, 11, (count,), generator=rng)
    for i, (label, start) in enumerate(zip(labels.tolist(), starts.tolist())):
        if label == 0:
            images[i, 0, start:start + 2, :] += 1
        else:
            images[i, 0, :, start:start + 2] += 1
    return images, labels


model = nn.Sequential(
    nn.Conv2d(1, 8, 3, padding=1),
    nn.ReLU(),
    nn.MaxPool2d(2),
    nn.Conv2d(8, 16, 3, padding=1),
    nn.ReLU(),
    nn.AdaptiveAvgPool2d(1),
    nn.Flatten(1),
    nn.Linear(16, 2),
)
x_train, y_train = lines(192, seed=1)
x_test, y_test = lines(96, seed=2)
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

for _ in range(40):
    optimizer.zero_grad()
    loss = loss_fn(model(x_train), y_train)
    loss.backward()
    optimizer.step()

model.eval()
with torch.no_grad():
    logits = model(x_test)
    assert logits.shape == (96, 2)
    accuracy = (logits.argmax(dim=1) == y_test).float().mean().item()
print(f"test accuracy = {accuracy:.3f}")
```

`CrossEntropyLoss` 接收未归一化的 logits 和整型类别索引，两类任务的目标形状为 `(N,)`。如果换成自己的图片，先检查通道维是否在第二维，标签是否是 `torch.long`，卷积后的高宽是否符合预期。池化和带步幅的卷积都会丢掉空间细节，做定位或分割时要保留更高分辨率的特征。

## 5. 参考资料与下一篇

- LeCun 等人的文档识别论文展示了卷积网络如何在字符识别任务中组织卷积、下采样与分类。[Gradient-Based Learning Applied to Document Recognition](https://doi.org/10.1109/5.726791)
- 官方文档给出了分组卷积、膨胀率与输出尺寸的精确定义。[PyTorch Conv2d](https://docs.pytorch.org/docs/stable/generated/torch.nn.Conv2d.html)

下一篇看[RNN 循环神经网络](/zh/blog/basic-rnn/)，把计算从二维空间移到有先后顺序的序列上。
