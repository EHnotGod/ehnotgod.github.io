---
title: "LSTM 长短期记忆网络"
publishDate: 2026-11-28
description: "用手算理解遗忘门、输入门和输出门，分析细胞状态的梯度路径，再实现单步 LSTM 与延迟记忆任务。"
category: technical
tags:
  - 基础模型算法
  - 深度学习底层
language: zh
---

在[RNN](/zh/blog/basic-rnn/)里，隐藏状态既负责记录历史，又要产生当前输出。每读一个输入，这个状态就得穿过一次矩阵乘法和非线性。LSTM 给状态分出两条路径。细胞状态 $c_t$ 可以按元素保留或写入，隐藏状态 $h_t$ 提供当下的输出以及下一步的门控信息。

这是[基础模型算法](/zh/collection/basic-model-algorithms/)的第三篇。正文使用 PyTorch 实现的常见变体，它包含遗忘门。可以结合原论文了解最早的结构与动机。[LSTM 原论文](https://doi.org/10.1162/neco.1997.9.8.1735) · [PyTorch LSTM 文档](https://docs.pytorch.org/docs/stable/generated/torch.nn.LSTM.html)

## 1. 四个向量怎样更新两份状态

输入 $x_t$ 的维度为 $D$，上一步的 $h_{t-1}$ 与 $c_{t-1}$ 的维度都为 $H$。先对输入和旧隐藏状态做两次线性变换，得到一份长为 $4H$ 的向量，切成四段

$$
[z_i,z_f,z_g,z_o]=x_tW_x+h_{t-1}W_h+b.
$$

这四段分别负责输入门、遗忘门、候选内容和输出门。门用 sigmoid 转到 $[0,1]$，候选内容用 $\tanh$ 转到 $[-1,1]$。完整更新是

$$
\begin{aligned}
i_t &= \sigma(z_i), & f_t &= \sigma(z_f),\\
g_t &= \tanh(z_g), & o_t &= \sigma(z_o),\\
c_t &= f_t\odot c_{t-1}+i_t\odot g_t,\\
h_t &= o_t\odot\tanh(c_t).
\end{aligned}
$$

| 向量 | 参与的计算 | 接近 0 时会怎样 |
| --- | --- | --- |
| 遗忘门 $f_t$ | 从旧细胞状态保留多少 | 旧记忆在该维几乎被清空 |
| 输入门 $i_t$ | 写入多少候选内容 | 候选内容在该维几乎写不进去 |
| 候选 $g_t$ | 提供有正有负的新内容 | 该维写入的内容很少 |
| 输出门 $o_t$ | 从细胞状态暴露多少到 $h_t$ | 该维的隐藏输出很小，细胞状态可以继续保留 |

例如某个维度上，原来的 $c_{t-1}=0.8$，遗忘门为 $0.9$，输入门为 $0.2$，候选值为 $-0.5$。新记忆为 $0.9\times0.8+0.2\times(-0.5)=0.62$。若输出门是 $0.4$，对应的隐藏状态为 $0.4\tanh(0.62)\approx0.220$。隐藏状态读出来的数值可以比内部记忆小得多。

## 2. 梯度为什么能走得更远

把门值和经过 $h$ 的支路单独看，细胞状态的直接传递项是 $f_t\odot c_{t-1}$。沿着这条直接边，$c_t$ 对 $c_{t-1}$ 的局部导数是

$$
\left.\frac{\partial c_t}{\partial c_{t-1}}\right|_{\text{直接路径}}
=\operatorname{diag}(f_t).
$$

连续 $k$ 步沿这条路径传递时，对应维度的梯度会乘上这 $k$ 个遗忘门值。门在需要记住的阶段能学到接近 1，梯度就能在这些阶段保留得更多。门持续偏小，或者梯度走进其他饱和的分支时，梯度依然可能变小。

完整反传还要算其他路径。比如时刻 $t$ 的隐藏状态读出了 $c_t$，自己的损失和未来门控传回来的 $h_t$ 梯度都会贡献到 $c_t$。设已有上游梯度 $\bar h_t$ 和来自未来的 $\bar c_t^{\mathrm{future}}$，先合并

$$
\bar c_t=\bar c_t^{\mathrm{future}}
+\bar h_t\odot o_t\odot\bigl(1-\tanh^2(c_t)\bigr).
$$

然后，$\bar c_t\odot f_t$ 传回旧细胞状态，$\bar c_t\odot c_{t-1}$ 传给遗忘门。输入门、候选内容和输出门也各自用乘积法则和激活函数导数往回传。用自动微分库时，这些分支会合并到同一棵计算图里。

## 3. 合并矩阵与参数量

单向、单层、无投影时，PyTorch 的 `weight_ih_l0` 是 `(4H, D)`，`weight_hh_l0` 是 `(4H, H)`，顺序为 `i, f, g, o`。框架按 `x @ weight.T` 做乘法，所以存储形状与前文使用的 $W_x$、$W_h$ 互为转置。

PyTorch 还为这两组线性变换各存了一份偏置，前向会把它们相加。参数量因此为 $4HD+4H^2+8H$。例如 $D=3$、$H=5$ 时总量为 $200$。若自己只存一份合并偏置，等式中的最后一项就变成 $4H$。[PyTorch LSTM 参数布局](https://docs.pytorch.org/docs/stable/generated/torch.nn.LSTM.html)

### 3.1 用 NumPy 重算一个 LSTMCell

本例直接取 PyTorch 初始化的权重，在 NumPy 中重算同一组批次的两个状态。这样可以同时验证矩阵转置、切片顺序和偏置相加。

```python
import numpy as np
import torch
from torch import nn


def sigmoid(x):
    return np.exp(-np.logaddexp(0, -x))


def lstm_step(x, h, c, wx, wh, bias):
    gates = x @ wx + h @ wh + bias
    zi, zf, zg, zo = np.split(gates, 4, axis=-1)
    i = sigmoid(zi)
    f = sigmoid(zf)
    g = np.tanh(zg)
    o = sigmoid(zo)
    c_next = f * c + i * g
    h_next = o * np.tanh(c_next)
    return h_next, c_next


torch.manual_seed(2)
cell = nn.LSTMCell(3, 5).double()
x = torch.randn(2, 3, dtype=torch.float64)
h = torch.randn(2, 5, dtype=torch.float64)
c = torch.randn(2, 5, dtype=torch.float64)

with torch.no_grad():
    expected_h, expected_c = cell(x, (h, c))
    bias = (cell.bias_ih + cell.bias_hh).numpy()
    actual_h, actual_c = lstm_step(
        x.numpy(), h.numpy(), c.numpy(),
        cell.weight_ih.numpy().T, cell.weight_hh.numpy().T, bias,
    )

np.testing.assert_allclose(actual_h, expected_h.numpy())
np.testing.assert_allclose(actual_c, expected_c.numpy())
assert sum(p.numel() for p in cell.parameters()) == 200
print(actual_h.shape, actual_c.shape)
```

## 4. 用最后一个时间步读取第一步的信息

这里用长度为 16 的单变量序列。第一步写入 $+1$ 或 $-1$，其余位置只有少量独立噪声，标签由第一步的符号决定。模型直到最后一个时间步才输出类别。测试集用另一个随机种子生成，评估的是同样长度和规则下的记忆能力。

```python
import torch
from torch import nn

torch.manual_seed(0)
torch.set_num_threads(1)


def memory_batch(count, steps, seed):
    rng = torch.Generator().manual_seed(seed)
    labels = torch.randint(0, 2, (count,), generator=rng)
    x = 0.05 * torch.randn(count, steps, 1, generator=rng)
    x[:, 0, 0] = 2 * labels.float() - 1
    return x, labels


lstm = nn.LSTM(input_size=1, hidden_size=12, batch_first=True)
readout = nn.Linear(12, 2)
x_train, y_train = memory_batch(128, steps=16, seed=1)
x_test, y_test = memory_batch(96, steps=16, seed=2)

# The combined forget bias starts at 1.
with torch.no_grad():
    hidden = lstm.hidden_size
    lstm.bias_ih_l0[hidden:2 * hidden].fill_(1)
    lstm.bias_hh_l0[hidden:2 * hidden].zero_()


def classify(x):
    output, (h_n, c_n) = lstm(x)
    assert output.shape[:2] == x.shape[:2]
    assert h_n.shape == c_n.shape == (1, x.size(0), 12)
    return readout(h_n[-1])


optimizer = torch.optim.Adam([*lstm.parameters(), *readout.parameters()], lr=0.02)
loss_fn = nn.CrossEntropyLoss()
for _ in range(80):
    optimizer.zero_grad()
    loss = loss_fn(classify(x_train), y_train)
    loss.backward()
    optimizer.step()

lstm.eval()
readout.eval()
with torch.no_grad():
    test_accuracy = (classify(x_test).argmax(dim=-1) == y_test).float().mean()
print(f"test accuracy = {test_accuracy.item():.3f}")
```

`output` 是最后一层所有时间步的隐藏状态，`h_n` 与 `c_n` 是各层及方向在序列结束时的状态。即使 `batch_first=True`，最终状态的批次维仍在第二维。用单层单向等长批次时，`output[:, -1]` 与 `h_n[-1]` 相同。若数据经过 padding，应像[RNN 的变长示例](/zh/blog/basic-rnn/)一样传真实长度或正确取有效位置。

### 4.1 LSTM 与 GRU

LSTM 把 $h_t$ 与 $c_t$ 分开，用三道门控制读写。GRU 只传一份隐藏状态，通过更新门混合旧状态与新候选，并用重置门控制旧状态怎样参与候选计算。相同输入和隐藏维度下，GRU 通常有较少的门控参数，实际速度和效果还要看任务、序列长度及实现。[PyTorch GRU](https://docs.pytorch.org/docs/stable/generated/torch.nn.GRU.html)

## 5. 参考资料与下一篇

- 最初的 LSTM 论文从长期梯度问题出发，引入了更稳定的误差信号路径。[Hochreiter 与 Schmidhuber，Long Short-Term Memory](https://doi.org/10.1162/neco.1997.9.8.1735)
- 现代实现的门、状态、参数及双向接口以官方文档为准。[PyTorch LSTM](https://docs.pytorch.org/docs/stable/generated/torch.nn.LSTM.html)

下一篇看[Transformer](/zh/blog/basic-transformer/)，用自注意力直接混合多个位置的信息。
