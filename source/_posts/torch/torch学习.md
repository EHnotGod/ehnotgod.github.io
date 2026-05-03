---
title: "torch语法学习1"
categories:
- [语法学习]
tags:
- 深度学习底层学习 语法学习
---

建议和Dezero相关内容一起食用，效果更佳，更能理解。
eg. optimizer = optim.Adam(model.parameters(), lr=0.001)
为什么传入的是model.parameters()？以及梯度的清理optimizer.zero_grad()的理由是啥？为啥这么调用

## 1. 张量

### 1.1 基础

```python
import torch

# 设置数据类型和设备
dtype = torch.float  # 张量数据类型为浮点型
device = torch.device("cpu")  # 本次计算在 CPU 上进行

# 创建并打印两个随机张量 a 和 b
a = torch.randn(2, 3, device=device, dtype=dtype)  # 创建一个 2x3 的随机张量
b = torch.randn(2, 3, device=device, dtype=dtype)  # 创建另一个 2x3 的随机张量

print("张量 a:")
print(a)

print("张量 b:")
print(b)

# 逐元素相乘并输出结果
print("a 和 b 的逐元素乘积:")
print(a * b)

# 输出张量 a 所有元素的总和
print("张量 a 所有元素的总和:")
print(a.sum())

# 输出张量 a 中第 2 行第 3 列的元素（注意索引从 0 开始）
print("张量 a 第 2 行第 3 列的元素:")
print(a[1, 2])

# 输出张量 a 中的最大值
print("张量 a 中的最大值:")
print(a.max())
```

但是别用`max(a)`哈，这玩意儿不是torch的。
广播机制应该和numpy的是一样的：从右往左看：相等可以；有 1 可以；缺维度可以；其他不行。

numpy转tensor:

```python
import numpy as np
numpy_array = np.array([[1, 2], [3, 4]])
tensor_from_numpy = torch.from_numpy(numpy_array)
print(tensor_from_numpy)
```

数组转tensor:
```python
import torch
tensor = torch.tensor([1, 2, 3])
print(tensor)
```
tensor转numpy:
```python
x.numpy()
```
### 1.2 自动微分
一旦定义了计算图，可以通过 .backward() 方法来计算梯度。
```python
# 创建一个需要梯度的张量
tensor_requires_grad = torch.tensor([1.0], requires_grad=True)
# 进行一些操作
tensor_result = tensor_requires_grad * 2
# 计算梯度
tensor_result.backward()
print(tensor_requires_grad.grad)  # 输出梯度
```
如果你不希望某些张量的梯度被计算（例如，当你不需要反向传播时），可以使用 torch.no_grad() 或设置 requires_grad=False。
```python
with torch.no_grad():
    y = x * 2
```
### 1.3 更多操作
属性：
.shape	获取张量的形状	tensor.shape
.size()	获取张量的形状	tensor.size()
.dtype	获取张量的数据类型	tensor.dtype
.device	查看张量所在的设备 (CPU/GPU)	tensor.device
.dim()	获取张量的维度数	tensor.dim()
.requires_grad	是否启用梯度计算	tensor.requires_grad
.numel()	获取张量中的元素总数	tensor.numel()
.is_cuda	检查张量是否在 GPU 上	tensor.is_cuda
.T	获取张量的转置（适用于 2D 张量）	tensor.T
.item()	获取单元素张量的值	tensor.item()
.is_contiguous()	检查张量是否连续存储	tensor.is_contiguous()
操作：
+, -, *, /	元素级加法、减法、乘法、除法。	z = x + y
torch.matmul(x, y)	矩阵乘法。	z = torch.matmul(x, y)
torch.dot(x, y)	向量点积（仅适用于 1D 张量）。	z = torch.dot(x, y)
torch.sum(x)	求和。	z = torch.sum(x)
torch.mean(x)	求均值。	z = torch.mean(x)
torch.max(x)	求最大值。	z = torch.max(x)
torch.min(x)	求最小值。	z = torch.min(x)
torch.argmax(x, dim)	返回最大值的索引（指定维度）。	z = torch.argmax(x, dim=1)
torch.softmax(x, dim)	计算 softmax（指定维度）。	z = torch.softmax(x, dim=1)

x.view(shape)	改变张量的形状（不改变数据）。	z = x.view(3, 4)
x.reshape(shape)	类似于 view，但更灵活。	z = x.reshape(3, 4)
x.t()	转置矩阵。	z = x.t()
x.unsqueeze(dim)	在指定维度添加一个维度。	z = x.unsqueeze(0)
x.squeeze(dim)	去掉指定维度为 1 的维度。	z = x.squeeze(0)
torch.cat((x, y), dim)	按指定维度连接多个张量。	z = torch.cat((x, y), dim=1)

## 2. 神经网络
### 2.1 网络构建
```python
import torch.nn as nn
import torch.optim as optim
# 定义一个简单的全连接神经网络
class SimpleNN(nn.Module):
    def __init__(self):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(2, 2)  # 输入层到隐藏层
        self.fc2 = nn.Linear(2, 1)  # 隐藏层到输出层
    
    def forward(self, x):
        x = torch.relu(self.fc1(x))  # ReLU 激活函数
        x = self.fc2(x)
        return x
# 创建网络实例
model = SimpleNN()
# 打印模型结构
print(model)
```
### 2.2 流程
```python
# 随机输入
x = torch.randn(1, 2)
# 前向传播
output = model(x)
print(output)
# 定义损失函数（例如均方误差 MSE）
criterion = nn.MSELoss()
# 假设目标值为 1
target = torch.randn(1, 1)
# 计算损失
loss = criterion(output, target)
# 定义优化器（使用 Adam 优化器）
optimizer = optim.Adam(model.parameters(), lr=0.001)
# 训练步骤
optimizer.zero_grad()  # 清空梯度
loss.backward()  # 反向传播
optimizer.step()  # 更新参数
```
### 2.3 完整
```python
import torch
import torch.nn as nn
import torch.optim as optim

# 1. 定义一个简单的神经网络模型
class SimpleNN(nn.Module):
    def __init__(self):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(2, 2)  # 输入层到隐藏层
        self.fc2 = nn.Linear(2, 1)  # 隐藏层到输出层
    
    def forward(self, x):
        x = torch.relu(self.fc1(x))  # ReLU 激活函数
        x = self.fc2(x)
        return x

# 2. 创建模型实例
model = SimpleNN()

# 3. 定义损失函数和优化器
criterion = nn.MSELoss()  # 均方误差损失函数
optimizer = optim.Adam(model.parameters(), lr=0.001)  # Adam 优化器

# 4. 假设我们有训练数据 X 和 Y
X = torch.randn(10, 2)  # 10 个样本，2 个特征
Y = torch.randn(10, 1)  # 10 个目标值

# 5. 训练循环
for epoch in range(100):  # 训练 100 轮
    optimizer.zero_grad()  # 清空之前的梯度
    output = model(X)  # 前向传播
    loss = criterion(output, Y)  # 计算损失
    loss.backward()  # 反向传播
    optimizer.step()  # 更新参数
    
    # 每 10 轮输出一次损失
    if (epoch+1) % 10 == 0:
        print(f'Epoch [{epoch+1}/100], Loss: {loss.item():.4f}')
```
### 2.4 更多函数

模型定义基础：
nn.Module	所有神经网络模块的基类	class Net(nn.Module): ...
nn.Sequential	顺序容器，按顺序执行各层	nn.Sequential(conv, relu, pool)
nn.ModuleList	将子模块存储在列表中	self.layers = nn.ModuleList([...])
nn.Parameter	创建可学习的参数张量	self.w = nn.Parameter(torch.randn(n))
卷积层：
nn.Conv1d	一维卷积（文本、音频）	nn.Conv1d(3, 64, 3)
nn.Conv2d	二维卷积（图像）	nn.Conv2d(3, 64, 3, padding=1)
nn.Conv3d	三维卷积（视频）	nn.Conv3d(3, 64, 3)
nn.ConvTranspose2d	转置卷积（解码器、上采样）	nn.ConvTranspose2d(64, 3, 2, stride=2)
池化层：
nn.MaxPool2d	二维最大池化	nn.MaxPool2d(2, 2)
nn.AvgPool2d	二维平均池化	nn.AvgPool2d(2, 2)
nn.AdaptiveAvgPool2d	自适应平均池化（固定输出尺寸）	nn.AdaptiveAvgPool2d((1, 1))
nn.AdaptiveMaxPool2d	自适应最大池化（固定输出尺寸）	nn.AdaptiveMaxPool2d((1, 1))
线性层：
nn.ReLU	ReLU 激活函数，f(x) = max(0, x)	nn.ReLU()
nn.GELU	高斯误差线性单元（Transformer 默认）	nn.GELU()
nn.SiLU	Swish 激活函数	nn.SiLU()
nn.Tanh	双曲正切	nn.Tanh()
nn.Sigmoid	Sigmoid 激活函数	nn.Sigmoid()
nn.Softmax	Softmax 激活函数	nn.Softmax(dim=1)
nn.LogSoftmax	Log Softmax（数值稳定）	nn.LogSoftmax(dim=1)
nn.LeakyReLU	LeakyReLU，允许负值有小幅梯度	nn.LeakyReLU(0.01)
nn.ELU	指数线性单元	nn.ELU()
归一化层：
nn.BatchNorm2d	二维批归一化（卷积网络常用）	nn.BatchNorm2d(64)
nn.LayerNorm	层归一化（Transformer 常用）	nn.LayerNorm(512)
nn.GroupNorm	组归一化（ResNet 等常用）	nn.GroupNorm(4, 64)
nn.InstanceNorm2d	实例归一化（风格迁移常用）	nn.InstanceNorm2d(64)
Transformer 层：
nn.Transformer	完整 Transformer 模型	nn.Transformer(d_model=512, nhead=8)
nn.TransformerEncoder	Transformer 编码器	nn.TransformerEncoder(layer, num_layers=6)
nn.TransformerDecoder	Transformer 解码器	nn.TransformerDecoder(layer, num_layers=6)
nn.TransformerEncoderLayer	Transformer 编码器层	nn.TransformerEncoderLayer(512, 8)
nn.MultiheadAttention	多头注意力机制	nn.MultiheadAttention(512, 8)
嵌入层：
nn.Embedding	嵌入层（词汇映射到向量）	nn.Embedding(10000, 256)
nn.EmbeddingBag	嵌入袋（聚合多个嵌入）	nn.EmbeddingBag(10000, 256)
Dropout 层：
nn.Dropout	随机丢弃（防止过拟合）	nn.Dropout(0.5)
nn.Dropout2d	2D Dropout（按特征图丢弃）	nn.Dropout2d(0.5)
损失函数：
nn.CrossEntropyLoss	交叉熵损失（多分类）	nn.CrossEntropyLoss()
nn.MSELoss	均方误差损失（回归）	nn.MSELoss()
nn.L1Loss	L1 损失（MAE）	nn.L1Loss()
nn.BCEWithLogitsLoss	带 Sigmoid 的二元交叉熵	nn.BCEWithLogitsLoss()
nn.HuberLoss	Huber 损失（鲁棒回归）	nn.HuberLoss()
nn.NLLLoss	负对数似然损失	nn.NLLLoss()

### 2.5 更大的示例

```python
# 导入PyTorch库
import torch
import torch.nn as nn

# 定义输入层大小、隐藏层大小、输出层大小和批量大小
n_in, n_h, n_out, batch_size = 10, 5, 1, 10

# 创建虚拟输入数据和目标数据
x = torch.randn(batch_size, n_in)  # 随机生成输入数据
y = torch.tensor([[1.0], [0.0], [0.0], 
                 [1.0], [1.0], [1.0], [0.0], [0.0], [1.0], [1.0]])  # 目标输出数据

# 创建顺序模型，包含线性层、ReLU激活函数和Sigmoid激活函数
model = nn.Sequential(
   nn.Linear(n_in, n_h),  # 输入层到隐藏层的线性变换
   nn.ReLU(),            # 隐藏层的ReLU激活函数
   nn.Linear(n_h, n_out),  # 隐藏层到输出层的线性变换
   nn.Sigmoid()           # 输出层的Sigmoid激活函数
)

# 定义均方误差损失函数和随机梯度下降优化器
criterion = torch.nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)  # 学习率为0.01

# 执行梯度下降算法进行模型训练
for epoch in range(50):  # 迭代50次
   y_pred = model(x)  # 前向传播，计算预测值
   loss = criterion(y_pred, y)  # 计算损失
   print('epoch: ', epoch, 'loss: ', loss.item())  # 打印损失值

   optimizer.zero_grad()  # 清零梯度
   loss.backward()  # 反向传播，计算梯度
   optimizer.step()  # 更新模型参数
```

## 3. 数据处理与预加载

### 3.1 Dataset
```python
import torch
from torch.utils.data import Dataset

# 自定义数据集类
class MyDataset(Dataset):
    def __init__(self, X_data, Y_data):
        """
        初始化数据集，X_data 和 Y_data 是两个列表或数组
        X_data: 输入特征
        Y_data: 目标标签
        """
        self.X_data = X_data
        self.Y_data = Y_data

    def __len__(self):
        """返回数据集的大小"""
        return len(self.X_data)

    def __getitem__(self, idx):
        """返回指定索引的数据"""
        x = torch.tensor(self.X_data[idx], dtype=torch.float32)  # 转换为 Tensor
        y = torch.tensor(self.Y_data[idx], dtype=torch.float32)
        return x, y

# 示例数据
X_data = [[1, 2], [3, 4], [5, 6], [7, 8]]  # 输入特征
Y_data = [1, 0, 1, 0]  # 目标标签

# 创建数据集实例
dataset = MyDataset(X_data, Y_data)
```
### 3.2 Dataloader
DataLoader 是 PyTorch 提供的一个重要工具，用于从 Dataset 中按批次（batch）加载数据。
DataLoader 允许我们批量读取数据并进行多线程加载，从而提高训练效率。
```python
from torch.utils.data import DataLoader

# 创建 DataLoader 实例，batch_size 设置每次加载的样本数量
dataloader = DataLoader(dataset, batch_size=2, shuffle=True)

# 打印加载的数据
for epoch in range(1):
    for batch_idx, (inputs, labels) in enumerate(dataloader):
        print(f'Batch {batch_idx + 1}:')
        print(f'Inputs: {inputs}')
        print(f'Labels: {labels}')
```

### 3.3 预处理
transforms.Compose()：将多个变换操作组合在一起。
transforms.Resize()：调整图像大小。
transforms.ToTensor()：将图像转换为 PyTorch 张量，值会被归一化到 [0, 1] 范围。
transforms.Normalize()：标准化图像数据，通常使用预训练模型时需要进行标准化处理。

```python
import torchvision.datasets as datasets
import torchvision.transforms as transforms

# 定义预处理操作
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))  # 对灰度图像进行标准化
])

# 下载并加载 MNIST 数据集
train_dataset = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
test_dataset = datasets.MNIST(root='./data', train=False, download=True, transform=transform)

# 创建 DataLoader
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)

# 迭代训练数据
for inputs, labels in train_loader:
    print(inputs.shape)  # 每个批次的输入数据形状
    print(labels.shape)  # 每个批次的标签形状
```

## 4. 一些例子

### 4.1 卷积神经网络

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms


# 1. 数据加载与预处理
transform = transforms.Compose([
    transforms.ToTensor(),  # 转为张量
    transforms.Normalize((0.5,), (0.5,))  # 归一化到 [-1, 1]
])

# 加载 MNIST 数据集
train_dataset = datasets.MNIST(root='./data', train=True, transform=transform, download=True)
test_dataset = datasets.MNIST(root='./data', train=False, transform=transform, download=True)

train_loader = torch.utils.data.DataLoader(dataset=train_dataset, batch_size=64, shuffle=True)
test_loader = torch.utils.data.DataLoader(dataset=test_dataset, batch_size=64, shuffle=False)

# 2. 定义 CNN 模型
class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        # 定义卷积层
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, stride=1, padding=1)  # 输入1通道，输出32通道
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)  # 输入32通道，输出64通道
        # 定义全连接层
        self.fc1 = nn.Linear(64 * 7 * 7, 128)  # 展平后输入到全连接层
        self.fc2 = nn.Linear(128, 10)  # 10 个类别

    def forward(self, x):
        x = F.relu(self.conv1(x))  # 第一层卷积 + ReLU
        x = F.max_pool2d(x, 2)     # 最大池化
        x = F.relu(self.conv2(x))  # 第二层卷积 + ReLU
        x = F.max_pool2d(x, 2)     # 最大池化
        x = x.view(-1, 64 * 7 * 7) # 展平
        x = F.relu(self.fc1(x))    # 全连接层 + ReLU
        x = self.fc2(x)            # 最后一层输出
        return x

# 创建模型实例
model = SimpleCNN()

# 3. 定义损失函数与优化器
criterion = nn.CrossEntropyLoss()  # 多分类交叉熵损失
optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.9)

# 4. 模型训练
num_epochs = 5
model.train()  # 设置模型为训练模式

for epoch in range(num_epochs):
    total_loss = 0
    for images, labels in train_loader:
        outputs = model(images)  # 前向传播
        loss = criterion(outputs, labels)  # 计算损失

        optimizer.zero_grad()  # 清空梯度
        loss.backward()  # 反向传播
        optimizer.step()  # 更新参数

        total_loss += loss.item()

    print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {total_loss / len(train_loader):.4f}")

# 5. 模型测试
model.eval()  # 设置模型为评估模式
correct = 0
total = 0

with torch.no_grad():  # 关闭梯度计算
    for images, labels in test_loader:
        outputs = model(images)
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

accuracy = 100 * correct / total
print(f"Test Accuracy: {accuracy:.2f}%")
```

### 4.2 循环神经网络

```python
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
import numpy as np

# 数据集：字符序列预测（Hello -> Elloh）
char_set = list("hello")
char_to_idx = {c: i for i, c in enumerate(char_set)}
idx_to_char = {i: c for i, c in enumerate(char_set)}

# 数据准备
input_str = "hello"
target_str = "elloh"
input_data = [char_to_idx[c] for c in input_str]
target_data = [char_to_idx[c] for c in target_str]

# 转换为独热编码
input_one_hot = np.eye(len(char_set))[input_data]

# 转换为 PyTorch Tensor
inputs = torch.tensor(input_one_hot, dtype=torch.float32)
targets = torch.tensor(target_data, dtype=torch.long)

# 模型超参数
input_size = len(char_set)
hidden_size = 8
output_size = len(char_set)
num_epochs = 200
learning_rate = 0.1

# 定义 RNN 模型
class RNNModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(RNNModel, self).__init__()
        self.rnn = nn.RNN(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x, hidden):
        out, hidden = self.rnn(x, hidden)
        out = self.fc(out)  # 应用全连接层
        return out, hidden

model = RNNModel(input_size, hidden_size, output_size)

# 定义损失函数和优化器
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

# 训练 RNN
losses = []
hidden = None  # 初始隐藏状态为 None
for epoch in range(num_epochs):
    optimizer.zero_grad()

    # 前向传播
    outputs, hidden = model(inputs.unsqueeze(0), hidden)
    hidden = hidden.detach()  # 防止梯度爆炸

    # 计算损失
    loss = criterion(outputs.view(-1, output_size), targets)
    loss.backward()
    optimizer.step()
    losses.append(loss.item())

    if (epoch + 1) % 20 == 0:
        print(f"Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}")

# 测试 RNN
with torch.no_grad():
    test_hidden = None
    test_output, _ = model(inputs.unsqueeze(0), test_hidden)
    predicted = torch.argmax(test_output, dim=2).squeeze().numpy()

    print("Input sequence: ", ''.join([idx_to_char[i] for i in input_data]))
    print("Predicted sequence: ", ''.join([idx_to_char[i] for i in predicted]))

# 可视化损失
plt.plot(losses, label="Training Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.title("RNN Training Loss Over Epochs")
plt.legend()
plt.show()
```
