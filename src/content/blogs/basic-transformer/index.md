---
title: "Transformer 与自注意力"
publishDate: 2026-11-28
description: "手算 Q、K、V 和因果掩码，拆解多头注意力、位置编码与残差块，写一个可训练的小型语言模型。"
category: technical
tags:
  - 基础模型算法
  - 深度学习底层
language: zh
---

[LSTM](/zh/blog/basic-lstm/)需要把早先的信息沿着状态一步步送到后面。自注意力给了另一种选择，每个位置都能在允许的范围内直接读取其他位置，并根据当前输入决定读多少。Transformer 再用前馈网络、残差连接和归一化把这些计算组成可以堆叠的层。

这是[基础模型算法](/zh/collection/basic-model-algorithms/)的第四篇。下文先讲单层在做什么，再实现一个仅解码器的因果模型。原论文使用的是编码器与解码器两套层。[Attention Is All You Need](https://arxiv.org/html/1706.03762v7)

## 1. 自注意力怎样从其他位置读信息

### 1.1 Q、K 和 V

同一条长度为 $T$ 的序列表示为矩阵 $X$，每行对应一个 token。由三组可训练的投影生成查询（query）、键（key）和值（value）。

$$
Q=XW_Q,\qquad K=XW_K,\qquad V=XW_V.
$$

第 $i$ 行的查询 $q_i$ 和第 $j$ 行的键 $k_j$ 做点积，得到位置 $i$ 给位置 $j$ 的分数。对固定的 $i$，softmax 沿着所有可见的 $j$ 做归一化。然后用这些权重加权求和读出 $V$。

$$
S=\frac{QK^{\mathsf T}}{\sqrt{d_k}},\qquad
A=\operatorname{softmax}_{\text{键维}}(S),\qquad
Y=AV.
$$

$d_k$ 是单个查询或键向量的宽度。若其各分量近似独立且方差为 1，点积的方差量级为 $d_k$。除以 $\sqrt{d_k}$ 能让分数的尺度更稳定，减少 softmax 因分数过大而过早变得尖锐。

### 1.2 手算一个输出向量

让一个查询 $q=[1,0]$ 对两个键 $[1,0]$ 和 $[0,1]$ 打分。缩放后的分数是 $[1/\sqrt{2},0]$，softmax 后的权重约为 $[0.670,0.330]$。若两个值向量为 $[2,0]$ 和 $[0,4]$，加权输出约为 $[1.340,1.320]$。换一个查询，两个键和值可以保持原样，读到的信息比例会变化。

## 2. 多头注意力里的形状

设批大小为 $B$，序列长度为 $T$，模型宽度为 $d$，头数为 $H$，每头宽度 $d_h=d/H$。常见实现先把每个位置投影成 $3d$，沿最后一维拆成三份，再给三份各自拆头。

| 中间量 | 形状 | 最后一维的含义 |
| --- | --- | --- |
| 输入表示 | `(B, T, d)` | 每个 token 的特征 |
| 每个 Q、K、V | `(B, H, T, d_h)` | 单个头的特征 |
| `Q @ K.transpose(-1, -2)` | `(B, H, T, T)` | 每个查询对所有键的打分 |
| 每个头的加权读出 | `(B, H, T, d_h)` | 当前头读取到的信息 |
| 合并各头并做输出投影 | `(B, T, d)` | 下一层接收的特征 |

每个头有自己的投影子空间和权重矩阵。算完各头后，先把头拼回特征维，再由输出投影混合。下方代码用一次线性层计算三份投影，数学上等价于先独立算三次再拼起来。

## 3. 掩码与位置信息

### 3.1 因果掩码和 padding 掩码

预测下一个 token 时，第 $i$ 个查询只能读取下标 $j\leq i$ 的键。对于四个位置，下面的矩阵用 1 表示可见。

$$
M=
\begin{bmatrix}
1&0&0&0\\
1&1&0&0\\
1&1&1&0\\
1&1&1&1
\end{bmatrix}.
$$

先把不可见位置的分数设为 $-\infty$，再对键维做 softmax。掩掉的位置权重为零，可见的位置重新归一化。如果某一行的键全被掩掉，手写 softmax 可能产生 `NaN`，需要避免该行或显式处理。

padding 掩码负责从注意力里排除补齐位置，因果掩码负责排除未来位置，二者可以同时使用。若训练标签也被补齐，应在损失计算时跳过这些目标。调用框架接口时，需要确认布尔掩码中 `True` 的语义。比如 `scaled_dot_product_attention` 用 `True` 表示允许参与，而 `nn.MultiheadAttention` 的布尔 `attn_mask` 用 `True` 表示禁止参与。[PyTorch SDPA](https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html) · [PyTorch MultiheadAttention](https://docs.pytorch.org/docs/stable/generated/torch.nn.MultiheadAttention.html)

### 3.2 怎样把位置带进模型

没有位置输入、也没有掩码的自注意力会随着输入重排而重排输出。为了让模型区分相同 token 出现的不同位置，可以在 token embedding 上加位置向量。原论文用不同频率的正弦和余弦构造固定编码。

$$
\begin{aligned}
PE(p,2i)&=\sin\bigl(p/10000^{2i/d}\bigr),\\
PE(p,2i+1)&=\cos\bigl(p/10000^{2i/d}\bigr).
\end{aligned}
$$

下方示例用可学习的位置表 `nn.Embedding(max_len, d)`，便于直接观察位置张量如何与 token 张量相加。它最多支持表中已经定义的位置。[原论文的位置编码一节](https://arxiv.org/html/1706.03762v7#S3.SS5)

## 4. 从注意力到 Transformer 层

注意力在不同位置之间混合信息。前馈网络（FFN）则在每个位置上独立做两次线性映射，中间接非线性，通常先从 $d$ 扩充到 $d_{\mathrm{ff}}$，再投影回 $d$。同一层内所有位置共享 FFN 的参数。

原论文把 LayerNorm 放到残差相加之后。下方实现采用先归一化再进入子层的 Pre-Norm 形式。

$$
\begin{aligned}
U &= X+\operatorname{Attention}(\operatorname{LN}_1(X)),\\
Y &= U+\operatorname{FFN}(\operatorname{LN}_2(U)).
\end{aligned}
$$

两个子层都返回 `(B, T, d)`，才能与输入逐元素相加。LayerNorm 在这里沿每个位置的特征维做归一化。堆多层时，上一层的输出就是下一层的输入。

常见用途可以按注意力连接方式区分。

| 结构 | 位置之间如何连接 | 常见任务 |
| --- | --- | --- |
| 仅编码器 | 输入 token 可在有效范围内相互读取 | 分类、文本表征 |
| 仅解码器 | 每个位置只能读自身和前文 | 自回归生成 |
| 编码器—解码器 | 解码器用因果自注意力，并通过交叉注意力读取编码结果 | 翻译、条件生成 |

在交叉注意力中，$Q$ 来自解码器，$K$ 和 $V$ 来自编码器，两边序列长度可以不同。得分矩阵对应目标位置与源位置之间的关系。

## 5. 手写一个可运行的因果模型

下面实现多头自注意力、一个解码器块、token 与位置 embedding，以及预测下一项的训练循环。玩具序列形如 `8, 9, 0, 1, 2`，学习目标是每个位置预测循环计数的下一项。无需下载数据。

训练前先做因果性检查。保持前两个 token 不变，替换后两个 token，前两个位置的 logits 应保持一致。这个检查能抓出常见的掩码方向错误。

```python
import torch
from torch import nn
from torch.nn import functional as F

torch.manual_seed(4)
torch.set_num_threads(1)


class CausalAttention(nn.Module):
    def __init__(self, width, heads, max_len):
        super().__init__()
        if width % heads != 0:
            raise ValueError("Model width must be divisible by the number of heads")
        self.heads = heads
        self.head_dim = width // heads
        self.qkv = nn.Linear(width, 3 * width)
        self.out = nn.Linear(width, width)
        self.register_buffer(
            "visible", torch.ones(max_len, max_len, dtype=torch.bool).tril(),
            persistent=False,
        )

    def forward(self, x):
        batch, steps, width = x.shape
        blocks = self.qkv(x).chunk(3, dim=-1)
        q, k, v = (
            part.reshape(batch, steps, self.heads, self.head_dim).transpose(1, 2)
            for part in blocks
        )
        scores = (q @ k.transpose(-1, -2)) / self.head_dim ** 0.5
        scores = scores.masked_fill(~self.visible[:steps, :steps], float("-inf"))
        weights = scores.softmax(dim=-1)
        merged = (weights @ v).transpose(1, 2).reshape(batch, steps, width)
        return self.out(merged)


class DecoderBlock(nn.Module):
    def __init__(self, width, heads, max_len):
        super().__init__()
        self.ln1 = nn.LayerNorm(width)
        self.attention = CausalAttention(width, heads, max_len)
        self.ln2 = nn.LayerNorm(width)
        self.ffn = nn.Sequential(
            nn.Linear(width, 4 * width),
            nn.GELU(),
            nn.Linear(4 * width, width),
        )

    def forward(self, x):
        x = x + self.attention(self.ln1(x))
        return x + self.ffn(self.ln2(x))


class TinyDecoder(nn.Module):
    def __init__(self, vocab, width=32, heads=4, max_len=16):
        super().__init__()
        self.token = nn.Embedding(vocab, width)
        self.position = nn.Embedding(max_len, width)
        self.layers = nn.Sequential(
            DecoderBlock(width, heads, max_len),
            DecoderBlock(width, heads, max_len),
        )
        self.norm = nn.LayerNorm(width)
        self.classifier = nn.Linear(width, vocab)

    def forward(self, tokens):
        steps = tokens.size(1)
        if not 1 <= steps <= self.position.num_embeddings:
            raise ValueError("Sequence length is outside the learned position range")
        positions = torch.arange(steps, device=tokens.device)
        x = self.token(tokens) + self.position(positions)
        return self.classifier(self.norm(self.layers(x)))


vocab = 10
model = TinyDecoder(vocab)
with torch.no_grad():
    a = model(torch.tensor([[3, 4, 5, 6]]))
    b = model(torch.tensor([[3, 4, 1, 2]]))
    assert a.shape == (1, 4, vocab)
    torch.testing.assert_close(a[:, :2], b[:, :2])

steps = 8
train_starts = torch.randint(vocab, (32, 1))
train = (train_starts + torch.arange(steps + 1)) % vocab
x, y = train[:, :-1], train[:, 1:]
optimizer = torch.optim.AdamW(model.parameters(), lr=0.01)

for _ in range(60):
    optimizer.zero_grad()
    logits = model(x)
    loss = F.cross_entropy(logits.reshape(-1, vocab), y.reshape(-1))
    loss.backward()
    optimizer.step()

model.eval()
with torch.no_grad():
    prefix = torch.tensor([[8, 9, 0, 1]])
    next_token = model(prefix)[:, -1].argmax(dim=-1)
print("next token:", next_token.item())
```

`x` 和 `y` 都是 `(B, T)`。第 $t$ 个输入的标签是原序列的第 $t+1$ 个 token。损失把所有位置展平成一批分类样本，前向仍要靠掩码阻止模型读取标签位置。训练时，模型一次算出全部位置的 logits。生成时，要先选出一个新 token，再把它加入前缀继续预测。

## 6. 计算开销和生成时的 KV Cache

全长为 $T$ 的序列会产生 $H$ 个 $T\times T$ 的分数矩阵。按总模型宽度 $d$ 计算，点积和加权求和的主要开销为 $O(T^2d)$。查询、键、值和输出投影另外需要 $O(Td^2)$ 量级的计算。直接保存分数矩阵需要 $O(HT^2)$ 空间，更高效的内核可以减少中间矩阵的显存占用。[原论文的复杂度比较](https://arxiv.org/html/1706.03762v7#S4) · [PyTorch SDPA](https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html)

自回归生成每多一个 token，上面的小模型都会重算整段前缀。因果模型中，旧位置的表示不会因追加未来 token 而改变。KV Cache 在每一层存下这些位置先前算好的键和值，下一步只为新 token 计算投影，再读取缓存与新追加的键和值。每层普通多头注意力的缓存大小随前缀长度线性增长。单步注意力仍需遍历可见前缀，生成过程也仍需要按 token 推进。

## 7. 参考资料

- 原论文包含编码器和解码器、缩放点积、多头注意力与位置编码的定义。[Vaswani 等人，Attention Is All You Need](https://arxiv.org/html/1706.03762v7)
- 对照官方接口可以检查张量布局、布尔掩码与高效实现的选项。[PyTorch SDPA](https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html)

回到[基础模型算法](/zh/collection/basic-model-algorithms/)可以从 CNN、RNN 和 LSTM 的手写例子重新对照这套计算。
