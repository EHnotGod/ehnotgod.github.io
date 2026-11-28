---
title: "RNN 循环神经网络"
publishDate: 2026-11-28
description: "把循环网络展开到时间轴上，从单步递推推到 BPTT，手写梯度并处理 PyTorch 的变长序列。"
category: technical
tags:
  - 基础模型算法
  - 深度学习底层
language: zh
---

若输入是连续订单金额、语音帧或者一句话，当前位置的含义常常取决于前面出现了什么。RNN 给每条序列维护一个隐藏状态，每读一步就用当前输入和旧状态算出新状态。顺序一变，经过的状态就可能不同。

这是[基础模型算法](/zh/collection/basic-model-algorithms/)的第二篇。前一篇讲[CNN 的权重共享](/zh/blog/basic-cnn/)，这里的权重沿时间轴共享。

## 1. 一个时间步到底算什么

一个样本在时刻 $t$ 的输入 $x_t$ 是长度为 $D$ 的行向量，隐藏状态 $h_t$ 是长度为 $H$ 的行向量。由初始状态 $h_0$ 开始，依次计算

$$
a_t=x_tW_x+h_{t-1}W_h+b,\qquad
h_t=\tanh(a_t).
$$

$W_x$ 的形状为 $(D,H)$，$W_h$ 为 $(H,H)$，$b$ 为 $(H,)$。长度为 $T$ 的序列共做 $T$ 次递推，重复使用同一组参数。若打包 $N$ 条等长序列，$x_t$ 与 $h_t$ 就分别是 $(N,D)$ 和 $(N,H)$ 的矩阵。

取标量情形 $h_0=0$、$W_x=1$、$W_h=0.5$、$b=0$。读入 $[1,0]$，$h_1=\tanh(1)\approx0.762$，$h_2=\tanh(0.5h_1)\approx0.363$。输入若变成 $[0,1]$，最终状态约为 $0.762$。单步公式相同，状态经过的路径变了。

### 1.1 从状态得到任务输出

- **整段分类**可以将最后一个有效状态 $h_T$ 接线性层，得到类别 logits。
- **逐步标注**可以将每个 $h_t$ 接同一个线性层，输出长度为 $T$ 的标签序列。
- **预测下一项**可以让 $h_t$ 输出第 $t+1$ 项的分布，训练时让输入和标签错开一格。

双向 RNN 加一条从末尾往前读的分支，可以给每个位置同时提供前后文。因果预测只能使用当前及之前的输入，应使用单向网络。

## 2. 沿时间反向传播（BPTT）

把 RNN 展成一个链式计算图，$h_t$ 会同时影响当前的任务输出和后续的 $h_{t+1}$。设 $g_t$ 是时刻 $t$ 的损失对 $h_t$ 的直接梯度，$\delta_t=\partial L/\partial a_t$。按照行向量记法，从最后一项向前递推

$$
\begin{aligned}
\delta_t
&=\bigl(g_t+\delta_{t+1}W_h^{\mathsf T}\bigr)\odot(1-h_t^2),\\
\frac{\partial L}{\partial W_x}
&=\sum_{t=1}^{T}x_t^{\mathsf T}\delta_t,\\
\frac{\partial L}{\partial W_h}
&=\sum_{t=1}^{T}h_{t-1}^{\mathsf T}\delta_t,\qquad
\frac{\partial L}{\partial b}=\sum_{t=1}^{T}\delta_t.
\end{aligned}
$$

最后一项之后的 $\delta_{T+1}$ 为零。若只在句末做分类，$g_1$ 到 $g_{T-1}$ 为零，较早的状态仍会经由递推得到梯度。参数被每一个时间步使用，所以求导时必须把所有时间步的贡献相加。

### 2.1 为什么长依赖难学

标量情形的每一步会把从未来传回的梯度乘上 $W_h(1-h_t^2)$。如果连续 30 步的乘子都是 0.8，经过这条路径后梯度只剩 $0.8^{30}\approx0.00124$。向量情形则是反复乘局部雅可比矩阵，梯度可能沿某些方向变小、沿另一些方向变大。$\tanh$ 进入饱和区时，其导数也会变小。

梯度裁剪会限制单次更新前的梯度范数，主要应对梯度爆炸。截断 BPTT 会在片段交界处断开旧计算图，前向状态仍继续传递，梯度只在当前窗口内传播。需要跨批延续状态时，应确认这些批次真的是同一条序列的连续片段。[Pascanu 等人对梯度消失和爆炸的分析](https://proceedings.mlr.press/v28/pascanu13.html)

## 3. 用 NumPy 手写前向和 BPTT

下面先用一条序列对全部时刻计算平均平方损失，再对 $W_h$ 做中心有限差分。改动一个共享权重后重跑整个前向，数值梯度会包含这个权重在所有时刻的影响。

```python
import numpy as np


def rnn_forward(xs, wx, wh, bias):
    states = np.zeros((len(xs) + 1, len(bias)), dtype=xs.dtype)
    for t, x in enumerate(xs):
        states[t + 1] = np.tanh(x @ wx + states[t] @ wh + bias)
    return states


def loss_and_grads(xs, target, wx, wh, bias):
    states = rnn_forward(xs, wx, wh, bias)
    diff = states[1:] - target
    loss = 0.5 * np.sum(diff ** 2) / len(xs)

    dwx, dwh, db = np.zeros_like(wx), np.zeros_like(wh), np.zeros_like(bias)
    dh_next = np.zeros_like(bias)
    for t in reversed(range(len(xs))):
        h_prev, h = states[t], states[t + 1]
        dh = diff[t] / len(xs) + dh_next
        dz = dh * (1 - h ** 2)
        dwx += np.outer(xs[t], dz)
        dwh += np.outer(h_prev, dz)
        db += dz
        dh_next = dz @ wh.T
    return loss, (dwx, dwh, db)


rng = np.random.default_rng(0)
xs = rng.normal(size=(5, 3))
target = rng.normal(size=(5, 2))
wx = rng.normal(scale=0.2, size=(3, 2))
wh = rng.normal(scale=0.2, size=(2, 2))
bias = np.zeros(2)
loss, (_, dwh, _) = loss_and_grads(xs, target, wx, wh, bias)

eps = 1e-5
numerical = np.empty_like(wh)
for index in np.ndindex(wh.shape):
    delta = np.zeros_like(wh)
    delta[index] = eps
    plus, _ = loss_and_grads(xs, target, wx, wh + delta, bias)
    minus, _ = loss_and_grads(xs, target, wx, wh - delta, bias)
    numerical[index] = (plus - minus) / (2 * eps)
np.testing.assert_allclose(dwh, numerical, rtol=1e-6, atol=1e-8)
print(f"loss = {loss:.4f}, max gradient error = {abs(dwh - numerical).max():.2e}")
```

## 4. PyTorch 中的形状和变长批次

给 `nn.RNN` 设置 `batch_first=True`，输入与输出的头两维分别是批次和时间。最后的隐藏状态依然将层数与方向放在第一维。[PyTorch RNN 文档](https://docs.pytorch.org/docs/stable/generated/torch.nn.RNN.html)

| 张量 | 单层单向的形状 | 含义 |
| --- | --- | --- |
| `x` | `(N, T, D)` | 每个时间步的输入 |
| `output` | `(N, T, H)` | 最后一层各时刻的状态 |
| `h_n` | `(1, N, H)` | 每条序列的最终隐藏状态 |

把不同长度的样本补零后直接送入 RNN，短序列在补齐的位置依然会更新状态。可以用 `pack_padded_sequence` 提供真实长度，再从 `h_n[-1]` 取每个样本的最后有效状态。下面先用打包批次算一次，再把每条序列单独送进同一个网络验证。

```python
import torch
from torch import nn
from torch.nn.utils.rnn import pack_padded_sequence

torch.manual_seed(1)

lengths = torch.tensor([5, 2, 4])
x = torch.randn(3, 5, 3)
for i, length in enumerate(lengths.tolist()):
    x[i, length:] = 0

rnn = nn.RNN(input_size=3, hidden_size=4, batch_first=True)
classifier = nn.Linear(4, 2)
packed = pack_padded_sequence(x, lengths, batch_first=True, enforce_sorted=False)
_, h_n = rnn(packed)
logits = classifier(h_n[-1])
assert logits.shape == (3, 2)

for i, length in enumerate(lengths.tolist()):
    _, separate_state = rnn(x[i:i + 1, :length])
    torch.testing.assert_close(h_n[:, i:i + 1], separate_state)
print(logits.shape)
```

多层结构会把下层每个时刻的输出送给上层。双向时 `output` 的最后一维会拼接两个方向，`h_n` 的第一维则是 `num_layers * num_directions`。用双向模型做整句分类时，可以显式把最后一层两个方向的最终状态拼接起来。

## 5. 参考资料与下一篇

- 官方文档列出了循环层、批次维和隐藏状态的接口。[PyTorch RNN](https://docs.pytorch.org/docs/stable/generated/torch.nn.RNN.html)
- 关于梯度范数、裁剪和长期依赖的分析见原论文。[On the difficulty of training recurrent neural networks](https://proceedings.mlr.press/v28/pascanu13.html)

下一篇是[LSTM 长短期记忆网络](/zh/blog/basic-lstm/)。它保留了时间递推，并给记忆和梯度增加一条更直接的路径。
