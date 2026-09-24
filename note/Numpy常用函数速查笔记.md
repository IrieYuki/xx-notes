# NumPy 常用函数速查笔记

> 整理范围：数据分析与数值计算中最常用的 NumPy 操作，覆盖数组创建、索引、变形、运算、统计与线性代数。
> 每个函数都附有 **语法签名** + **作用说明** + **可运行示例**。
> 约定：`import numpy as np`，`a`、`b` 表示 ndarray 数组。

---

## 目录

1. [数组创建](#一数组创建)
2. [数组属性](#二数组属性)
3. [索引与切片](#三索引与切片)
4. [形状变换](#四形状变换)
5. [数学运算与广播](#五数学运算与广播)
6. [统计函数](#六统计函数)
7. [逻辑与条件](#七逻辑与条件)
8. [拼接与分割](#八拼接与分割)
9. [线性代数](#九线性代数)
10. [其他常用](#十其他常用)
11. [速查表](#十一速查表)

---

## 一、数组创建

### `np.array(object, dtype=None)`
从列表/元组等创建数组，可指定 `dtype`。
```python
import numpy as np

np.array([1, 2, 3])                      # array([1, 2, 3])
np.array([[1, 2], [3, 4]])               # 二维数组
np.array([1, 2, 3], dtype=float)         # 指定类型 array([1., 2., 3.])
```

### `np.arange(start, stop, step)` / `np.linspace(start, stop, num)`
`arange` 等差序列（**左闭右开**，类似 range）；`linspace` 在闭区间内生成 `num` 个等分点（**含端点**）。
```python
np.arange(5)                 # array([0, 1, 2, 3, 4])
np.arange(0, 1, 0.25)        # array([0.  , 0.25, 0.5 , 0.75])
np.linspace(0, 1, 5)         # array([0.  , 0.25, 0.5 , 0.75, 1.  ])
```

### `np.zeros(shape)` / `np.ones(shape)` / `np.full(shape, fill_value)` / `np.eye(n)`
全 0 / 全 1 / 指定填充值 / 单位矩阵。
```python
np.zeros((2, 3))             # 2×3 全 0
np.ones((2, 3))              # 2×3 全 1
np.full((2, 3), 7)           # 2×3 全 7
np.eye(3)                    # 3×3 单位矩阵
```

### `np.empty(shape)` / `np.ones_like(a)` / `np.zeros_like(a)`
`empty` 分配未初始化内存（值随机，快）；`ones_like`/`zeros_like` 生成与 `a` 同形状的全 1/0 数组。
```python
np.empty((2, 2))             # 内容未初始化，别依赖初值
np.ones_like(a)
np.zeros_like(a)
```

### 随机数组
```python
rng = np.random.default_rng(seed=42)   # 推荐：新版生成器（可复现）
rng.random((2, 3))           # [0,1) 均匀分布
rng.integers(0, 10, size=5)  # [0,10) 随机整数
rng.normal(0, 1, size=5)     # 均值 0 标准差 1 的正态分布
rng.choice([1, 2, 3], size=4)          # 从给定值中随机抽取
rng.shuffle(a)               # 原地打乱
```
> 旧版 `np.random.seed(42)`、`np.random.rand`、`np.random.randint` 仍常见，可了解。

---

## 二、数组属性

### `a.shape` / `a.ndim` / `a.size` / `a.dtype` / `a.itemsize`
`shape` 形状元组；`ndim` 维度数；`size` 元素总数；`dtype` 数据类型；`itemsize` 每个元素的字节数。
```python
a = np.array([[1, 2, 3], [4, 5, 6]])
a.shape        # (2, 3)
a.ndim         # 2
a.size         # 6
a.dtype        # dtype('int64')
```

---

## 三、索引与切片

### 基础索引 / 切片
与 Python 列表类似，但多维用逗号分隔各维度。切片返回**视图**（view，共享内存），改视图会影响原数组。
```python
a = np.arange(12).reshape(3, 4)
a[0]           # 第 1 行 array([0, 1, 2, 3])
a[0, 1]        # 第 0 行第 1 列元素 = 1
a[:, 1]        # 第 2 列（所有行）
a[0:2, 1:3]    # 前两行、第 2~3 列的子块
```

### 布尔索引
用布尔数组筛选元素。
```python
a[a > 5]                      # 所有 >5 的元素
a[a % 2 == 0]                 # 所有偶数
a[(a > 2) & (a < 8)]          # 多条件用 & |，记得加括号
```

### 花式索引（fancy indexing）
用整数数组/列表按位置选取。
```python
a[[0, 2]]                     # 第 0、2 行
a[[0, 2], [1, 3]]             # (0,1) 和 (2,3) 两个元素
```

### `np.where(condition, x, y)`
三元选择：满足条件取 `x`，否则取 `y`。也用于返回满足条件的**索引**（只传一个参数）。
```python
np.where(a > 5, 1, 0)         # 大于 5 的变 1，否则 0
np.where(a > 5)               # 返回满足条件元素的索引（多个数组）
```

---

## 四、形状变换

### `a.reshape(new_shape)` / `a.ravel()` / `a.flatten()`
`reshape` 改变形状（元素总数不变）；`ravel` 展平为**视图**（共享内存）；`flatten` 展平为**副本**（独立内存）。
```python
a = np.arange(12)
a.reshape(3, 4)               # 3 行 4 列
a.reshape(-1, 1)              # 变列向量（-1 自动推断）
a.ravel()                     # 展平
```

### `a.T` / `np.transpose(a)` / `a.transpose()`
转置。`a.T` 是最简写法。
```python
a.T                          # 转置
np.transpose(a)
```

### `np.expand_dims(a, axis)` / `np.squeeze(a, axis=None)`
`expand_dims` 在指定位置增加一个维度；`squeeze` 去掉长度为 1 的维度。
```python
np.expand_dims(a, axis=0)     # (n,) → (1, n)
np.squeeze(np.ones((1, 3, 1)))  # → (3,)
```

### `np.stack(arrays, axis=0)` / `np.concatenate`（见第八节）
`stack` 沿新轴堆叠多个数组。
```python
np.stack([a, b], axis=0)      # 在行方向新增一维
```

---

## 五、数学运算与广播

### 向量化算术
NumPy 支持**逐元素**运算，无需循环：`+ - * / ** // %` 等运算符直接作用于整个数组。
```python
a + b        # 对应元素相加
a * b        # 对应元素相乘（注意：不是矩阵乘法！）
a * 2        # 标量广播
a ** 2       # 逐元素平方
a / b        # 对应元素相除
```

### 通用函数（ufunc）
`np.add` `np.subtract` `np.multiply` `np.divide` `np.power` `np.sqrt` `np.exp` `np.log` `np.abs` `np.sin` `np.cos` 等。
```python
np.add(a, b)         # 等价于 a + b
np.sqrt(a)           # 逐元素开方
np.exp(a)            # e 的 a 次方
np.log(a)            # 自然对数
np.abs(a)            # 绝对值
np.round(a, 2)       # 保留两位小数
```

### 广播（broadcasting）
形状不同的数组运算时，NumPy 会自动「复制」小数组对齐形状。规则：从尾向前比对维度，相等或其一为 1 才兼容。
```python
a = np.array([[1, 2, 3], [4, 5, 6]])   # (2, 3)
a + np.array([10, 20, 30])             # (3,) 广播到每行
a + np.array([[1], [2]])               # (2, 1) 广播到每列
```

### `np.clip(a, a_min, a_max)`
把值限制在 `[a_min, a_max]` 区间内。
```python
np.clip(a, 0, 5)          # 小于 0 变 0，大于 5 变 5
```

---

## 六、统计函数

### `np.sum` / `np.mean` / `np.min` / `np.max` / `np.std` / `np.var` / `np.median` / `np.prod`
基本统计。`axis` 指定沿哪一维计算，不指定则对**所有元素**计算。
```python
a.sum()               # 所有元素和
a.sum(axis=0)         # 每列和（沿行方向）
a.sum(axis=1)         # 每行和（沿列方向）
a.mean()              # 均值
a.std()               # 标准差
a.var()               # 方差
a.max()               # 最大值
np.median(a)          # 中位数
```

### `np.argmin(a, axis)` / `np.argmax(a, axis)` / `np.argwhere(cond)`
`argmin`/`argmax` 返回最小值/最大值的**索引**；`argwhere` 返回所有满足条件的元素的坐标。
```python
a.argmax()            # 最大值在展平数组中的索引
a.argmax(axis=0)      # 每列最大值的行索引
np.argwhere(a > 5)    # 所有 >5 元素的坐标
```

### `np.cumsum(a, axis)` / `np.cumprod(a, axis)` / `np.diff(a)`
`cumsum`/`cumprod` 累计和/积；`diff` 相邻元素之差（后一个减前一个）。
```python
a.cumsum()            # 累计和
np.diff(a)            # 相邻差，结果长度减 1
```

---

## 七、逻辑与条件

### `np.any(a, axis)` / `np.all(a, axis)`
`any` 任一为真返回 True；`all` 全部为真返回 True。
```python
(a > 5).any()         # 是否存在 >5 的元素
(a > 5).all()         # 是否所有元素都 >5
(a > 5).any(axis=0)   # 每列是否存在 >5 的元素
```

### `np.logical_and` / `np.logical_or` / `np.logical_not`
逐元素逻辑运算（布尔数组的 `& | ~` 的底层实现）。
```python
np.logical_and(a > 1, a < 5)
np.logical_or(a < 1, a > 5)
np.logical_not(a > 5)
```

### `np.isnan` / `np.isinf` / `np.isfinite`
判断是否为 NaN / 无穷 / 有限值。常用于检测缺失值。
```python
np.isnan(a)           # 是否为 NaN
np.isfinite(a)        # 是否有限
np.nan_to_num(a)      # NaN/Inf 替换为 0 或大数
```

### `np.unique(a, return_counts=False)`
返回去重后的值（默认排序）。`return_counts=True` 同时返回每个值的出现次数。
```python
np.unique(a)                         # 去重排序
np.unique(a, return_counts=True)     # (值, 次数)
```

---

## 八、拼接与分割

### `np.concatenate(arrays, axis=0)` / `np.vstack(tup)` / `np.hstack(tup)`
沿指定轴拼接。`vstack` 垂直（沿行）堆叠，`hstack` 水平（沿列）堆叠。
```python
np.concatenate([a, b], axis=0)      # 沿行拼接（上下）
np.concatenate([a, b], axis=1)      # 沿列拼接（左右）
np.vstack([a, b])                   # 垂直堆叠，同 axis=0
np.hstack([a, b])                   # 水平堆叠，同 axis=1
```

### `np.split(ary, indices, axis=0)` / `np.vsplit` / `np.hsplit`
分割数组。`indices` 可传整数（等分份数）或列表（分割位置）。
```python
np.split(a, 2)             # 沿 axis=0 等分成 2 份
np.split(a, [2, 3], axis=1)  # 在第 2、3 列处切
np.vsplit(a, 2)            # 垂直分割
np.hsplit(a, 2)            # 水平分割
```

### `np.tile(A, reps)` / `np.repeat(a, repeats, axis=None)`
`tile` 把数组作为一个整体重复；`repeat` 逐元素重复。
```python
np.tile([1, 2], 3)          # array([1, 2, 1, 2, 1, 2])
np.repeat([1, 2], 3)        # array([1, 1, 1, 2, 2, 2])
```

---

## 九、线性代数

### `np.dot(a, b)` / `np.matmul(a, b)` / `@`
矩阵乘法。`dot` 兼容一维（点积）与高维；`matmul` 和 `@` 更规范地处理二维及以上矩阵乘法。
```python
A @ B               # 推荐写法
np.matmul(A, B)     # 等价
np.dot(A, B)        # 经典写法
np.dot(v1, v2)      # 向量点积
```

### `np.linalg.inv(A)` / `np.linalg.det(A)` / `np.linalg.eig(A)` / `np.linalg.solve(A, b)` / `np.linalg.norm(v)`
`inv` 逆矩阵；`det` 行列式；`eig` 特征值与特征向量；`solve` 解线性方程组 `Ax = b`；`norm` 范数。
```python
np.linalg.inv(A)             # 逆矩阵
np.linalg.det(A)             # 行列式
vals, vecs = np.linalg.eig(A)  # 特征值、特征向量
np.linalg.solve(A, b)        # 解 Ax = b
np.linalg.norm(v)            # 向量 2-范数（长度）
```

---

## 十、其他常用

### `np.sort(a, axis=-1)` / `np.argsort(a)`
`sort` 排序（默认沿最后一维）；`argsort` 返回排序后元素在原数组中的索引。
```python
np.sort(a)             # 每行各自排序
np.sort(a, axis=0)     # 每列排序
np.argsort(a)          # 排序索引
```

### `np.meshgrid(x, y)`
生成网格坐标，常用于画 3D 曲面、等高线图。
```python
x = np.linspace(-1, 1, 5)
y = np.linspace(-1, 1, 5)
X, Y = np.meshgrid(x, y)     # 二维坐标网格
```

### `np.minimum(a, b)` / `np.maximum(a, b)`
逐元素取两者中的较小 / 较大值（区别于 `min`/`max` 聚合）。
```python
np.minimum(a, b)       # 逐元素取小
np.maximum(a, b)       # 逐元素取大
```

### `a.astype(dtype)` / `np.savetxt(fname, a, delimiter=",")` / `np.loadtxt(fname, delimiter=",")`
类型转换 / 保存到文本文件 / 从文本文件读取。
```python
a.astype(float)                        # 转浮点
np.savetxt("data.csv", a, delimiter=",")   # 写出
np.loadtxt("data.csv", delimiter=",")      # 读入
```

---

## 十一、速查表

| 分类 | 函数 | 一句话作用 |
|------|------|-----------|
| 创建 | `array` `arange` `linspace` `zeros` `ones` `full` `eye` | 创建数组 |
| 随机 | `random.default_rng` `normal` `integers` `choice` | 随机数 |
| 属性 | `shape` `ndim` `size` `dtype` | 形状 / 维度 / 元素数 / 类型 |
| 索引 | 切片 / 布尔索引 / 花式索引 / `where` | 选取元素 |
| 变形 | `reshape` `ravel` `flatten` `T` `expand_dims` `squeeze` | 改变形状 |
| 运算 | `+ - * / **` `sqrt` `exp` `log` `abs` `clip` | 逐元素运算 |
| 统计 | `sum` `mean` `std` `var` `min` `max` `median` | 描述统计 |
| 统计 | `argmax` `argmin` `cumsum` `cumprod` `diff` | 索引 / 累计 / 差分 |
| 逻辑 | `any` `all` `logical_and` `isnan` `unique` | 逻辑判断 / 去重 |
| 拼接 | `concatenate` `vstack` `hstack` `stack` `tile` `repeat` | 拼接 / 重复 |
| 分割 | `split` `vsplit` `hsplit` | 分割 |
| 线代 | `dot` `matmul` `@` `linalg.inv` `det` `solve` `norm` | 矩阵运算 |
| 其他 | `sort` `argsort` `meshgrid` `minimum` `maximum` `savetxt` `loadtxt` | 排序 / 网格 / 读写 |

---

## 学习建议

1. **分清「逐元素乘法」与「矩阵乘法」**：`a * b` 是逐元素，`a @ b`（或 `np.dot`）才是矩阵乘法。这是新手最容易混淆的点。
   ```python
   A * B      # 对应元素相乘
   A @ B      # 矩阵乘法
   ```
2. **善用广播，少写循环**：NumPy 的精髓是向量化，能用数组运算就不要写 for 循环，速度差几个数量级。
3. **牢记 `axis` 方向**：`axis=0` 沿行方向（作用于每列），`axis=1` 沿列方向（作用于每行）；不指定 axis 则对所有元素。
4. **`reshape` 的 `-1`**：让 NumPy 自动推断该维度大小，非常实用。
   ```python
   a.reshape(-1, 1)     # 变 n 行 1 列
   ```
5. **注意视图 vs 副本**：`ravel`、切片返回视图（改它会动原数组），`flatten` 返回副本。要独立数据时用 `.copy()`。
