# NumPy 常用函数速查笔记

> 收集范围：数据分析 / 数值计算里最常用的 NumPy 操作，覆盖创建、索引、变形、运算、统计、拼接与线代。
> 每条都是「**签名 ｜ 返回 ｜ 备注**」三格 + 可直接运行的示例（`#` 后面是**真实输出**）。
> 约定：示例里都写 `import numpy as np`，数组变量统一叫 `a` / `b`。

---

## 索引 · 速查表

| 分类 | 用法（点击跳转） | 一句话作用 |
|------|------------------|-----------|
| A1 数组创建 | [`np.array(object, dtype=None)`](#nparrayobject-dtypenone-从列表元组建数组) | 从列表/元组建数组 |
| A1 数组创建 | [`np.arange(start, stop, step)`](#nparangestart-stop-step-等差序列左闭右开) | 等差序列（左闭右开） |
| A1 数组创建 | [`np.linspace(start, stop, num)`](#nplinspacestart-stop-num-等分点含右端点) | 等分点（含右端点） |
| A1 数组创建 | [`np.zeros(shape) / np.ones(shape)`](#npzerosshape--nponesshape-全-0--全-1-数组) | 全 0 / 全 1 数组 |
| A1 数组创建 | [`np.full(shape, fill_value)`](#npfullshape-fill_value-全部填成同一个值) | 全部填成同一个值 |
| A1 数组创建 | [`np.eye(n, k=0)`](#npeyen-k0-单位矩阵对角为-1) | 单位矩阵（对角为 1） |
| A1 数组创建 | [`np.empty(shape)`](#npemptyshape-只分配内存不初始化) | 只分配内存、不初始化 |
| A1 数组创建 | [`np.zeros_like(a) / ones_like / full_like`](#npzeros_likea--ones_like--full_like-照-a-的形状造新数组) | 照 a 的形状造新数组 |
| A1 数组创建 | [`np.random.default_rng(seed)`](#nprandomdefault_rngseed-新版随机数生成器) | 新版随机数生成器 |
| A2 数组属性 | [`a.shape / ndim / size / dtype / itemsize`](#ashape--ndim--size--dtype--itemsize-看数组的体检报告) | 看数组的「体检报告」 |
| A3 索引与切片 | [`a[i]、a[i, j]（基础索引切片）`](#aiai-j基础索引切片-多维用逗号分隔各维) | 多维用逗号分隔各维 |
| A3 索引与切片 | [`布尔索引 a[a > x]`](#布尔索引-aa--x-按条件筛元素) | 按条件筛元素 |
| A3 索引与切片 | [`花式索引 a[[0, 2]]`](#花式索引-a0-2-用整数数组按位置取) | 用整数数组按位置取 |
| A3 索引与切片 | [`np.where(condition, x, y)`](#npwherecondition-x-y-条件选择--找下标) | 条件选择 / 找下标 |
| A3 索引与切片 | [`a.copy()（视图 vs 副本）`](#acopy视图-vs-副本-什么时候需要复制) | 什么时候需要复制 |
| A4 形状变换 | [`a.reshape(new_shape)`](#areshapenew_shape-改形状元素总数不变) | 改形状（元素总数不变） |
| A4 形状变换 | [`a.ravel() / a.flatten()`](#aravel--aflatten-展平成一维) | 展平成一维 |
| A4 形状变换 | [`a.T / np.transpose(a)`](#at--nptransposea-转置行列互换) | 转置（行列互换） |
| A4 形状变换 | [`np.expand_dims(a, axis) / np.squeeze(a)`](#npexpand_dimsa-axis--npsqueezea-加一维--去多余的-1-维) | 加一维 / 去多余的 1 维 |
| A4 形状变换 | [`np.stack(arrays, axis=0)`](#npstackarrays-axis0-沿新轴把多个数组摞起来) | 沿**新轴**把多个数组摞起来 |
| A5 数学运算与广播 | [`逐元素算术 + - * / ** // %`](#逐元素算术---------运算符直接作用于整个数组) | 运算符直接作用于整个数组 |
| A5 数学运算与广播 | [`通用函数 ufunc（np.sqrt / exp / log ...）`](#通用函数-ufuncnpsqrt--exp--log--逐元素数学函数) | 逐元素数学函数 |
| A5 数学运算与广播 | [`广播 broadcasting`](#广播-broadcasting-形状不同也能运算) | 形状不同也能运算 |
| A5 数学运算与广播 | [`np.clip(a, a_min, a_max)`](#npclipa-a_min-a_max-把值夹到区间内) | 把值夹到区间内 |
| A6 统计函数 | [`a.sum(axis=None)`](#asumaxisnone-求和可按轴) | 求和（可按轴） |
| A6 统计函数 | [`a.mean() / a.std() / a.var()`](#amean--astd--avar-均值--标准差--方差) | 均值 / 标准差 / 方差 |
| A6 统计函数 | [`a.min() / a.max()（含 axis）`](#amin--amax含-axis-最小--最大聚合) | 最小 / 最大（聚合） |
| A6 统计函数 | [`np.median(a) / np.percentile(a, q)`](#npmediana--nppercentilea-q-中位数--分位数) | 中位数 / 分位数 |
| A6 统计函数 | [`np.prod(a, axis=None)`](#npproda-axisnone-连乘) | 连乘 |
| A6 统计函数 | [`np.argmin(a) / np.argmax(a)`](#npargmina--npargmaxa-极值所在的下标) | 极值所在的**下标** |
| A6 统计函数 | [`np.argwhere(condition)`](#npargwherecondition-所有满足条件的坐标) | 所有满足条件的坐标 |
| A6 统计函数 | [`np.cumsum / np.cumprod / np.diff`](#npcumsum--npcumprod--npdiff-累计和--累计积--相邻差分) | 累计和 / 累计积 / 相邻差分 |
| A6 统计函数 | [`np.nansum / np.nanmean`](#npnansum--npnanmean-跳过-nan-的统计) | 跳过 NaN 的统计 |
| A7 逻辑与条件 | [`(a > 5).any() / (a > 5).all()`](#a--5any--a--5all-有没有--是不是全部) | 有没有 / 是不是全部 |
| A7 逻辑与条件 | [`np.logical_and / or / not（以及 & | ~）`](#nplogical_and--or--not以及----布尔数组的与或非) | 布尔数组的与或非 |
| A7 逻辑与条件 | [`np.isnan / np.isinf / np.isfinite`](#npisnan--npisinf--npisfinite-找缺失值与无穷) | 找缺失值与无穷 |
| A7 逻辑与条件 | [`np.unique(a, return_counts=True)`](#npuniquea-return_countstrue-去重默认排序) | 去重（默认排序） |
| A7 逻辑与条件 | [`np.allclose(a, b)`](#npallclosea-b-浮点数组是否近似相等) | 浮点数组是否「近似相等」 |
| A8 拼接与分割 | [`np.concatenate / vstack / hstack`](#npconcatenate--vstack--hstack-拼接数组) | 拼接数组 |
| A8 拼接与分割 | [`np.split(a, indices_or_sections)`](#npsplita-indices_or_sections-分割数组) | 分割数组 |
| A8 拼接与分割 | [`np.tile(A, reps) / np.repeat(a, repeats)`](#nptilea-reps--nprepeata-repeats-重复数据) | 重复数据 |
| A9 线性代数 | [`a @ b / np.matmul / np.dot`](#a--b--npmatmul--npdot-矩阵乘法) | 矩阵乘法 |
| A9 线性代数 | [`np.linalg.inv / det / solve`](#nplinalginv--det--solve-逆矩阵--行列式--解方程) | 逆矩阵 / 行列式 / 解方程 |
| A9 线性代数 | [`np.linalg.eig / norm`](#nplinalgeig--norm-特征值--范数) | 特征值 / 范数 |
| A10 排序与其他 | [`np.sort(a) / np.argsort(a)`](#npsorta--npargsorta-排序--排序下标) | 排序 / 排序下标 |
| A10 排序与其他 | [`np.minimum(a, b) / np.maximum(a, b)`](#npminimuma-b--npmaximuma-b-逐元素取小--取大) | 逐元素取小 / 取大 |
| A10 排序与其他 | [`np.meshgrid(x, y)`](#npmeshgridx-y-生成二维坐标网格) | 生成二维坐标网格 |
| A10 排序与其他 | [`a.astype(dtype)`](#aastypedtype-转换元素类型) | 转换元素类型 |
| A10 排序与其他 | [`np.savetxt / np.loadtxt`](#npsavetxt--nploadtxt-数组存成文本文件--读回来) | 数组存成文本文件 / 读回来 |

---

## A1　数组创建

### `np.array(object, dtype=None)` 从列表/元组建数组

**签名** `np.array(object, dtype=None)` ｜ **返回** `ndarray` ｜ **备注** 混类型会被统一成一种 dtype

```python
import numpy as np
np.array([1, 2, 3])                # array([1, 2, 3])
np.array([[1, 2], [3, 4]])         # array([[1, 2], [3, 4]])
np.array([1, 2, 3], dtype=float)   # array([1., 2., 3.])
np.array([1, 2, 3]).dtype          # dtype('int64')
```

> ⚠️ 列表里混了字符串就会整体变成字符串数组（`np.array([1, "a"])`）；要固定类型就显式传 `dtype=`。

### `np.arange(start, stop, step)` 等差序列（左闭右开）

**签名** `np.arange(stop)`  /  `np.arange(start, stop, step)` ｜ **返回** `ndarray` ｜ **备注** **不含 stop**，和 `range` 一样

```python
import numpy as np
np.arange(5)                      # array([0, 1, 2, 3, 4])
np.arange(2, 8)                   # array([2, 3, 4, 5, 6, 7])
np.arange(0, 10, 2)               # array([0, 2, 4, 6, 8])
np.arange(0, 1, 0.25)             # array([0. , 0.25, 0.5 , 0.75])
```

> ⚠️ 浮点步长会有累计误差（`np.arange(0, 1, 0.1)` 的末位不准），要精确等分改用 `np.linspace`。

### `np.linspace(start, stop, num)` 等分点（含右端点）

**签名** `np.linspace(start, stop, num=50, endpoint=True)` ｜ **返回** `ndarray` ｜ **备注** **含 stop**，这点和 arange 相反

```python
import numpy as np
np.linspace(0, 1, 5)                    # array([0. , 0.25, 0.5 , 0.75, 1. ])
np.linspace(0, 10, 3)                   # array([ 0., 5., 10.])
np.linspace(0, 10, 3, endpoint=False)   # array([0. , 3.33333333, 6.66666667])
```

> ⚠️ `linspace(0, 1, 5)` 是「切成 5 个点、4 段」；想要步长而不是点数，用 `arange`。画图取 x 坐标几乎都用它。

### `np.zeros(shape) / np.ones(shape)` 全 0 / 全 1 数组

**签名** `np.zeros(shape, dtype=float)`  /  `np.ones(shape)` ｜ **返回** `ndarray` ｜ **备注** shape 要传**元组**

```python
import numpy as np
np.zeros(3)                       # array([0., 0., 0.])
np.zeros((2, 3))                  # array([[0., 0., 0.], [0., 0., 0.]])
np.ones((2, 2))                   # array([[1., 1.], [1., 1.]])
np.ones((2, 2), dtype=int)        # array([[1, 1], [1, 1]])
```

> ⚠️ 多维形状必须写成元组：`np.zeros(2, 3)` 会报 TypeError。默认 dtype 是浮点，要整数传 `dtype=int`。

### `np.full(shape, fill_value)` 全部填成同一个值

**签名** `np.full(shape, fill_value, dtype=None)` ｜ **返回** `ndarray` ｜ **备注** 比 `zeros(...) + 5` 更直观

```python
import numpy as np
np.full((2, 3), 7)                # array([[7, 7, 7], [7, 7, 7]])
np.full(3, 1.5)                   # array([1.5, 1.5, 1.5])
np.full(3, 9, dtype=float)        # array([9., 9., 9.])
```

### `np.eye(n, k=0)` 单位矩阵（对角为 1）

**签名** `np.eye(N, k=0)` ｜ **返回** `ndarray` ｜ **备注** `k` 控制对角线偏移

```python
import numpy as np
np.eye(3)                         # array([[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]])
np.eye(3, k=1)                    # array([[0., 1., 0.], [0., 0., 1.], [0., 0., 0.]])
np.eye(3, dtype=int)              # array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
```

> ⚠️ `eye(n)` 用于构造单位矩阵（做线代、one-hot 编码）；`np.identity(n)` 只能是对角为 1，不能偏移。

### `np.empty(shape)` 只分配内存、不初始化

**签名** `np.empty(shape, dtype=float)` ｜ **返回** `ndarray` ｜ **备注** 内容**随机**，不要依赖初值

```python
import numpy as np
e = np.empty((2, 2))
e.shape                           # (2, 2)
# 值未初始化，可能是任意数（甚至很大的数），只用于「先占位、马上整体赋值」
```

> ⚠️ 别拿 `empty` 当 `zeros` 用；它的好处只有一个：快。日常用 `zeros` 更安全。

### `np.zeros_like(a) / ones_like / full_like` 照 a 的形状造新数组

**签名** `np.zeros_like(a, dtype=None)`  /  `np.ones_like(a)`  /  `np.full_like(a, v)` ｜ **返回** `ndarray` ｜ **备注** 继承 a 的 shape 和 **dtype**

```python
import numpy as np
a = np.array([[1, 2], [3, 4]])
np.zeros_like(a)                  # array([[0, 0], [0, 0]])
np.ones_like(a)                   # array([[1, 1], [1, 1]])
np.full_like(a, 9)                # array([[9, 9], [9, 9]])
np.zeros_like(a, dtype=float)     # array([[0., 0.], [0., 0.]])
```

> ⚠️ 想得到浮点数组要显式传 `dtype=float`，否则整数数组会得到整数 0/1。

### `np.random.default_rng(seed)` 新版随机数生成器

**签名** `rng = np.random.default_rng(seed)` → `rng.random` / `integers` / `normal` / `choice` / `shuffle` ｜ **返回** `Generator` 对象 ｜ **备注** 固定 seed 结果可复现

```python
import numpy as np
rng = np.random.default_rng(42)
rng.random(3)                       # array([0.77395605, 0.43887844, 0.85859792])
rng.integers(0, 10, size=4)         # array([0, 6, 2, 0])
rng.normal(0, 1, size=3).round(3)   # array([-1.302, 0.128, -0.316])
rng.choice([1, 2, 3], size=4)       # array([2, 1, 3, 2])
x = np.arange(5)
rng.shuffle(x)
x                                   # array([4, 0, 2, 3, 1])
```

> ⚠️ 默认区间是半开 `[low, high)`；`shuffle` 是**原地**打乱。老代码里的 `np.random.seed(42)` / `rand` / `randint` 还能用，但新代码推荐 `default_rng`。

## A2　数组属性

### `a.shape / ndim / size / dtype / itemsize` 看数组的「体检报告」

**签名** `a.shape` `a.ndim` `a.size` `a.dtype` `a.itemsize` `a.nbytes` ｜ **返回** 元组 / 整数 / dtype ｜ **备注** 属性不带括号

```python
import numpy as np
a = np.array([[1, 2, 3], [4, 5, 6]])
a.shape                           # (2, 3)
a.ndim                            # 2
a.size                            # 6
a.dtype                           # dtype('int64')
a.itemsize                        # 8
a.nbytes                          # 48
```

> ⚠️ `shape` 是元组、`size` 是元素总数（各维相乘）；别用 `len(a)` 求元素数，那只是第一维的长度。属性后面**不加括号**：`a.shape` 对，`a.shape()` 错。

## A3　索引与切片

### `a[i]、a[i, j]（基础索引切片）` 多维用逗号分隔各维

**签名** `a[i]`  /  `a[i, j]`  /  `a[i:j, k:l]` ｜ **返回** 元素 / **视图** ｜ **备注** 切片返回视图，共享内存

```python
import numpy as np
a = np.arange(12).reshape(3, 4)
a[0]                              # array([0, 1, 2, 3])
a[0, 1]                           # np.int64(1)
a[:, 1]                           # array([1, 5, 9])
a[0:2, 1:3]                       # array([[1, 2], [5, 6]])
a[-1, -1]                         # np.int64(11)
```

> ⚠️ 切片是**视图**：改 `b = a[0:2]` 会改到 `a`。要独立副本写 `a[0:2].copy()`。

### `布尔索引 a[a > x]` 按条件筛元素

**签名** `a[condition]` ｜ **返回** 一维 `ndarray` ｜ **备注** 多条件要 `&` `|` 并加括号

```python
import numpy as np
a = np.arange(10)
a[a > 5]                          # array([6, 7, 8, 9])
a[a % 2 == 0]                     # array([0, 2, 4, 6, 8])
a[(a > 2) & (a < 6)]              # array([3, 4, 5])
a[a > 5].shape                    # (4,)
```

> ⚠️ 写 `a[a > 2 and a < 6]` 会报错（`and` 只能处理单个布尔值），必须 `&` + 括号。结果总是**一维**副本。

### `花式索引 a[[0, 2]]` 用整数数组按位置取

**签名** `a[[i, j, ...]]`  /  `a[[i, j], [k, l]]` ｜ **返回** **副本** `ndarray` ｜ **备注** 和切片不同，返回副本

```python
import numpy as np
a = np.array([10, 20, 30, 40])
a[[0, 2]]                         # array([10, 30])
b = np.arange(12).reshape(3, 4)
b[[0, 2]]                         # array([[ 0, 1, 2, 3], [ 8, 9, 10, 11]])
b[[0, 2], [1, 3]]                 # array([ 1, 11])
```

> ⚠️ `a[[0, 2], [1, 3]]` 取的是 `(0,1)` 和 `(2,3)` 两个**配对**元素，不是行列交叉的 2×2 子块（那要用 `np.ix_`）。

### `np.where(condition, x, y)` 条件选择 / 找下标

**签名** `np.where(cond, x, y)`  /  `np.where(cond)` ｜ **返回** `ndarray`（选择） / 下标元组（单参数） ｜ **备注** 单参数版等于 `np.nonzero`

```python
import numpy as np
a = np.array([1, 5, 8, 3])
np.where(a > 4, 1, 0)             # array([0, 1, 1, 0])
np.where(a > 4)                   # (array([1, 2]),)
np.where(a > 4)[0]                # array([1, 2])
```

> ⚠️ 只传一个参数时返回的是**下标元组**（多维也如此），要一维下标就取 `[0]`。类似 Excel 的 IF。

### `a.copy()（视图 vs 副本）` 什么时候需要复制

**签名** `a.copy()`  /  `a.base is None` ｜ **返回** `ndarray` ｜ **备注** 切片是视图、花式索引是副本

```python
import numpy as np
a = np.arange(5)
v = a[1:3]
c = a[1:3].copy()
v[0] = 99
a                                 # array([ 0, 99, 2, 3, 4])
c                                 # array([1, 2])
```

> ⚠️ 改 `v` 时 `a` 跟着变（视图），改 `c` 不影响 `a`（副本）。`a.base is None` 为 True 说明它是独立数组。

## A4　形状变换

### `a.reshape(new_shape)` 改形状（元素总数不变）

**签名** `a.reshape(shape)`  /  形状里可用 `-1` 自动推断 ｜ **返回** **视图** `ndarray` ｜ **备注** 总数不符报 `ValueError`

```python
import numpy as np
a = np.arange(12)
a.reshape(3, 4)                    # array([[ 0, 1, 2, 3], [ 4, 5, 6, 7], [ 8, 9, 10, 11]])
a.reshape(2, -1)                   # array([[ 0, 1, 2, 3, 4, 5], [ 6, 7, 8, 9, 10, 11]])
a.reshape(-1, 1).shape             # (12, 1)
a.reshape(3, 4).base is not None   # True
```

> ⚠️ `-1` 只允许出现一次，让 NumPy 算剩下的；`a.reshape(5, 5)` 会因元素数不匹配报错。原数组本身不变。

### `a.ravel() / a.flatten()` 展平成一维

**签名** `a.ravel()` 视图  /  `a.flatten()` 副本 ｜ **返回** `ndarray` ｜ **备注** ravel 改原数组，flatten 不改

```python
import numpy as np
a = np.arange(6).reshape(2, 3)
a.ravel()                         # array([0, 1, 2, 3, 4, 5])
a.flatten()                       # array([0, 1, 2, 3, 4, 5])
v = a.ravel()
v[0] = 99
a                                 # array([[99, 1, 2], [ 3, 4, 5]])
```

> ⚠️ 记法：**ravel = 视图（快、会联动）**，**flatten = 副本（安全、占内存）**。要独立数据用 `flatten()` 或 `.copy()`。

### `a.T / np.transpose(a)` 转置（行列互换）

**签名** `a.T`  /  `a.transpose(*axes)`  /  `np.transpose(a, axes=None)` ｜ **返回** **视图** `ndarray` ｜ **备注** 一维数组转置无变化

```python
import numpy as np
a = np.arange(6).reshape(2, 3)
a.T                                # array([[0, 3], [1, 4], [2, 5]])
a.T.shape                          # (3, 2)
b = np.arange(24).reshape(2, 3, 4)
b.shape                            # (2, 3, 4)
np.transpose(b, (1, 0, 2)).shape   # (3, 2, 4)
```

> ⚠️ 二维用 `a.T` 就够了；三维以上要指定轴顺序，用 `np.transpose(b, (1, 0, 2))`。转置是视图，不复制数据。

### `np.expand_dims(a, axis) / np.squeeze(a)` 加一维 / 去多余的 1 维

**签名** `np.expand_dims(a, axis)`  /  `np.squeeze(a, axis=None)` ｜ **返回** `ndarray` ｜ **备注** squeeze 只删长度为 1 的维

```python
import numpy as np
a = np.array([1, 2, 3])
np.expand_dims(a, 0).shape        # (1, 3)
np.expand_dims(a, 1).shape        # (3, 1)
b = np.ones((1, 3, 1))
np.squeeze(b).shape               # (3,)
np.squeeze(b, axis=0).shape       # (3, 1)
```

> ⚠️ `a[None, :]` 和 `np.expand_dims(a, 0)` 等价；`squeeze` 指定的 axis 长度不是 1 时会报错。

### `np.stack(arrays, axis=0)` 沿**新轴**把多个数组摞起来

**签名** `np.stack(arrays, axis=0)` ｜ **返回** `ndarray`（多一维） ｜ **备注** 和 concatenate 的区别：stack 会加维度

```python
import numpy as np
a = np.array([1, 2])
b = np.array([3, 4])
np.stack([a, b])                  # array([[1, 2], [3, 4]])
np.stack([a, b], axis=1)          # array([[1, 3], [2, 4]])
np.stack([a, b]).shape            # (2, 2)
```

> ⚠️ `np.stack([a, b])` 结果形状 `(2, 2)`，比原来多一维；`np.concatenate` 保持维度不变。形状不同的数组不能 stack。

## A5　数学运算与广播

### `逐元素算术 + - * / ** // %` 运算符直接作用于整个数组

**签名** `a + b` `a - b` `a * b` `a / b` `a ** 2` `a // 2` `a % 2` ｜ **返回** `ndarray`（**新数组**） ｜ **备注** `*` 是逐元素，不是矩阵乘

```python
import numpy as np
a = np.array([1, 2, 3])
b = np.array([10, 20, 30])
a + b                             # array([11, 22, 33])
a * b                             # array([10, 40, 90])
a * 2                             # array([2, 4, 6])
a ** 2                            # array([1, 4, 9])
a / b                             # array([0.1, 0.1, 0.1])
a // 2                            # array([0, 1, 1])
a % 2                             # array([1, 0, 1])
```

> ⚠️ **`a * b` 是逐元素相乘**，矩阵乘法是 `a @ b` / `np.matmul`。`/` 结果一定是浮点。

### `通用函数 ufunc（np.sqrt / exp / log ...）` 逐元素数学函数

**签名** `np.sqrt` `np.exp` `np.log` `np.abs` `np.round` `np.power` `np.sin` `np.cos` ｜ **返回** `ndarray` ｜ **备注** 名字和 `math` 一样，但作用在整个数组

```python
import numpy as np
a = np.array([1, 4, 9])
np.sqrt(a)                                # array([1., 2., 3.])
np.exp(np.array([0, 1]))                  # array([1. , 2.71828183])
np.round(np.array([1.2345, 2.3456]), 2)   # array([1.23, 2.35])
np.abs(np.array([-1, 2]))                 # array([1, 2])
np.power(a, 2)                            # array([ 1, 16, 81])
np.log(np.array([1, np.e])).round(6)      # array([0., 1.])
```

> ⚠️ 别对数组用 `math.sqrt`（只接受单个数字）；对负数开方/取对数会得到 `nan` 并打印 `RuntimeWarning`，不会抛异常，容易悄悄算错。

### `广播 broadcasting` 形状不同也能运算

**签名** 形状从尾向前比对：相等或其中一个是 1 即可 ｜ **返回** `ndarray` ｜ **备注** 不兼容会 `ValueError`

```python
import numpy as np
a = np.array([[1, 2, 3], [4, 5, 6]])
a + np.array([10, 20, 30])           # array([[11, 22, 33], [14, 25, 36]])
a + np.array([[1], [2]])             # array([[2, 3, 4], [6, 7, 8]])
a + 100                              # array([[101, 102, 103], [104, 105, 106]])
(a + np.array([10, 20, 30])).shape   # (2, 3)
```

> ⚠️ 行向量 `(3,)` 会加到每一行，列向量 `(2,1)` 会加到每一列；`(2,3)` 和 `(2,)` 相加**会报错**（尾巴 3 与 2 不等），需要显式 `reshape`。

### `np.clip(a, a_min, a_max)` 把值夹到区间内

**签名** `np.clip(a, a_min, a_max)`  /  `a.clip(min, max)` ｜ **返回** `ndarray` ｜ **备注** 超界值被替换成边界值

```python
import numpy as np
a = np.array([-3, 0, 5, 9])
np.clip(a, 0, 5)                  # array([0, 0, 5, 5])
a.clip(0, 5).tolist()             # [0, 0, 5, 5]
```

> ⚠️ 常用于把预测值/颜色值限制在合法范围；等价写法 `np.minimum(np.maximum(a, 0), 5)`，但 clip 更清楚。

## A6　统计函数

### `a.sum(axis=None)` 求和（可按轴）

**签名** `np.sum(a, axis=None, keepdims=False)` / `a.sum(axis)` ｜ **返回** 标量 / `ndarray` ｜ **备注** `axis` 决定沿哪一维算

```python
import numpy as np
a = np.array([[1, 2, 3], [4, 5, 6]])
a.sum()                              # np.int64(21)
a.sum(axis=0)                        # array([5, 7, 9])
a.sum(axis=1)                        # array([ 6, 15])
a.sum(axis=1, keepdims=True).shape   # (2, 1)
```

> ⚠️ `axis=0` = 把每一**列**压成一行（纵向合并），`axis=1` = 把每一**行**压成一列；不写 axis 就是全部元素。`keepdims=True` 保留维度，方便后续广播。

### `a.mean() / a.std() / a.var()` 均值 / 标准差 / 方差

**签名** `np.mean(a, axis=None)` / `np.std(a)` / `np.var(a)` ｜ **返回** `float` / `ndarray` ｜ **备注** 都是总体口径（ddof=0）

```python
import numpy as np
a = np.array([1, 2, 3, 4])
a.mean()                                      # np.float64(2.5)
a.std().round(4)                              # np.float64(1.118)
a.var()                                       # np.float64(1.25)
np.mean(np.array([[1, 2], [3, 4]]), axis=0)   # array([2., 3.])
```

> ⚠️ 方差/标准差默认除以 N（总体）；要样本口径（除以 N-1）传 `ddof=1`：`a.std(ddof=1)`。

### `a.min() / a.max()（含 axis）` 最小 / 最大（聚合）

**签名** `np.min(a, axis=None)` / `a.max(axis=)` ｜ **返回** 标量 / `ndarray` ｜ **备注** 逐元素取小用 `np.minimum`

```python
import numpy as np
a = np.array([[3, 1], [2, 5]])
a.min()                           # np.int64(1)
a.max()                           # np.int64(5)
a.max(axis=0)                     # array([3, 5])
a.min(axis=1)                     # array([1, 2])
```

> ⚠️ `a.max()` 返回**一个数**（聚合），`np.maximum(a, b)` 返回**逐元素取大的数组**，别混。

### `np.median(a) / np.percentile(a, q)` 中位数 / 分位数

**签名** `np.median(a, axis=None)` / `np.percentile(a, q)` ｜ **返回** `float` / `ndarray` ｜ **备注** 抗离群值

```python
import numpy as np
a = np.array([1, 2, 3, 4, 100])
np.median(a)                      # np.float64(3.0)
a.mean()                          # np.float64(22.0)
np.percentile(a, 50)              # np.float64(3.0)
np.percentile(a, 75)              # np.float64(4.0)
```

> ⚠️ 这份数据里 `median` 是 3、`mean` 是 22 —— 有离群值时用中位数更能代表「典型值」。

### `np.prod(a, axis=None)` 连乘

**签名** `np.prod(a, axis=None)` / `a.prod()` ｜ **返回** 标量 / `ndarray` ｜ **备注** 空数组返回 1

```python
import numpy as np
np.prod([1, 2, 3, 4])                         # np.int64(24)
np.prod(np.array([[1, 2], [3, 4]]), axis=1)   # array([ 2, 12])
```

> ⚠️ 元素多时很容易溢出成 `inf` 或 0，真要算大数乘积考虑取对数后求和。

### `np.argmin(a) / np.argmax(a)` 极值所在的**下标**

**签名** `np.argmin(a, axis=None)` / `np.argmax(a)` ｜ **返回** `int` / `ndarray` ｜ **备注** 返回展平后的下标

```python
import numpy as np
a = np.array([3, 1, 4, 1, 5])
a.argmax()                                  # np.int64(4)
a.argmin()                                  # np.int64(1)
np.array([[1, 9], [8, 2]]).argmax(axis=0)   # array([1, 0])
```

> ⚠️ 有并列时返回**第一个**；不写 axis 时按下标是按「展平（C 顺序）」算的：`np.unravel_index(idx, a.shape)` 可以还原成多维坐标。

### `np.argwhere(condition)` 所有满足条件的坐标

**签名** `np.argwhere(cond)` ｜ **返回** 形状 (n, ndim) 的 `ndarray` ｜ **备注** 比 `np.where` 单参数版更好读

```python
import numpy as np
a = np.array([[1, 6], [7, 2]])
np.argwhere(a > 5)                # array([[0, 1], [1, 0]])
np.argwhere(a > 5).tolist()       # [[0, 1], [1, 0]]
```

> ⚠️ 返回的是 `[[行, 列], ...]`；只要一维下标就用 `np.where(cond)[0]`。

### `np.cumsum / np.cumprod / np.diff` 累计和 / 累计积 / 相邻差分

**签名** `np.cumsum(a, axis=None)` / `np.cumprod(a)` / `np.diff(a, n=1)` ｜ **返回** `ndarray` ｜ **备注** `diff` 结果长度减 1

```python
import numpy as np
a = np.array([1, 2, 3, 4])
a.cumsum()                        # array([ 1, 3, 6, 10])
np.cumprod(a)                     # array([ 1, 2, 6, 24])
np.diff(a)                        # array([1, 1, 1])
np.diff(a, n=2)                   # array([0, 0])
```

> ⚠️ `cumsum` 常用于「前缀和」；`diff` 是**后一个减前一个**，所以长度比原数组少 1（求相邻变化量、算收益率）。

### `np.nansum / np.nanmean` 跳过 NaN 的统计

**签名** `np.nansum(a)` / `np.nanmean(a)` / `np.nanmax(a)` ｜ **返回** `float` / `ndarray` ｜ **备注** 普通 sum 遇到 NaN 会全变 NaN

```python
import numpy as np
a = np.array([1.0, np.nan, 3.0])
a.sum()                           # np.float64(nan)
np.nansum(a)                      # np.float64(4.0)
np.nanmean(a)                     # np.float64(2.0)
```

> ⚠️ 数据里缺值（NaN）时用 `nan*` 系列；先 `np.isnan(a).sum()` 看看有多少个缺失值。

## A7　逻辑与条件

### `(a > 5).any() / (a > 5).all()` 有没有 / 是不是全部

**签名** `np.any(a, axis=None)` / `np.all(a, axis=None)` ｜ **返回** `bool` / `ndarray` ｜ **备注** 结果是 numpy.bool_，直接用于 if 没问题

```python
import numpy as np
a = np.array([1, 6, 8])
(a > 5).any()                            # np.True_
(a > 5).all()                            # np.False_
(a > 0).all()                            # np.True_
np.array([[1, 6], [7, 2]]).any(axis=0)   # array([ True, True])
```

> ⚠️ **先做比较得到布尔数组**，再 any/all：写 `a.any() > 5` 是错的（那是「有没有非零元素」）。

### `np.logical_and / or / not（以及 & | ~）` 布尔数组的与或非

**签名** `np.logical_and(x, y)` / `np.logical_or` / `np.logical_not` / 运算符 `& | ~` ｜ **返回** 布尔 `ndarray` ｜ **备注** 条件必须加括号

```python
import numpy as np
a = np.array([1, 3, 5, 7])
np.logical_and(a > 2, a < 6)      # array([False, True, True, False])
(a > 2) & (a < 6)                 # array([False, True, True, False])
np.logical_or(a < 2, a > 6)       # array([ True, False, False, True])
np.logical_not(a > 2)             # array([ True, False, False, False])
~ (a > 2)                         # array([ True, False, False, False])
```

> ⚠️ `and`/`or`/`not` 对数组会报 `ValueError`（只能处理单个布尔值），必须用 `&`/`|`/`~` 且每个比较都要加括号。

### `np.isnan / np.isinf / np.isfinite` 找缺失值与无穷

**签名** `np.isnan(a)` / `np.isinf(a)` / `np.isfinite(a)` / `np.nan_to_num(a)` ｜ **返回** 布尔 `ndarray` ｜ **备注** 整数数组恒为 False/True（不报错）

```python
import numpy as np
a = np.array([1.0, np.nan, np.inf, 4.0])
np.isnan(a)                       # array([False, True, False, False])
np.isinf(a)                       # array([False, False, True, False])
np.isfinite(a)                    # array([ True, False, False, True])
np.isnan(a).sum()                 # np.int64(1)
np.nan_to_num(a)                  # array([1.00000000e+000, 0.00000000e+000, 1.79769313e+308, 4.00000000e+000])
```

> ⚠️ **整数数组不会出现 NaN**（本来就是整数）；Numpy 2.x 起对整数数组调 `isnan` 也不报错（全 False），旧版本会抛 `TypeError` —— 跨版本要稳就先 `.astype(float)`。清洗数据常见写法：`a[np.isnan(a)] = 0` 或 `a = np.nan_to_num(a)`。

### `np.unique(a, return_counts=True)` 去重（默认排序）

**签名** `np.unique(a, return_counts=False, return_index=False)` ｜ **返回** `ndarray` / 元组 ｜ **备注** 比 Python 的 set 多了计数

```python
import numpy as np
a = np.array([3, 1, 3, 2, 1])
np.unique(a)                      # array([1, 2, 3])
vals, counts = np.unique(a, return_counts=True)
vals                              # array([1, 2, 3])
counts                            # array([2, 1, 2])
```

> ⚠️ 结果是**排好序**的（不是原顺序）；要统计每个值出现次数还可以用 `collections.Counter`，但 `unique` 能直接给数组。

### `np.allclose(a, b)` 浮点数组是否「近似相等」

**签名** `np.allclose(a, b, rtol=1e-05, atol=1e-08)` ｜ **返回** `bool` ｜ **备注** 浮点比较不要用 ==

```python
import numpy as np
a = np.array([0.1 + 0.2, 1.0])
b = np.array([0.3, 1.0])
a == b                            # array([False, True])
np.allclose(a, b)                 # True
```

> ⚠️ 浮点运算有误差，`(0.1+0.2) == 0.3` 是 False；判断数组是否相等用 `np.allclose`。

## A8　拼接与分割

### `np.concatenate / vstack / hstack` 拼接数组

**签名** `np.concatenate([a, b], axis=0)` / `np.vstack` / `np.hstack` ｜ **返回** `ndarray` ｜ **备注** 除拼接轴外，其他维度必须一致

```python
import numpy as np
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6]])
np.concatenate([a, b], axis=0)                   # array([[1, 2], [3, 4], [5, 6]])
np.vstack([a, b])                                # array([[1, 2], [3, 4], [5, 6]])
c = np.array([[9], [9], [9]])
np.hstack([np.concatenate([a, b], axis=0), c])   # array([[1, 2, 9], [3, 4, 9], [5, 6, 9]])
```

> ⚠️ `axis=0` 上下拼（行数相加）、`axis=1` 左右拼（列数相加）；一维数组 `hstack` 就是首尾连接。形状对不上会报 `ValueError`。

### `np.split(a, indices_or_sections)` 分割数组

**签名** `np.split(a, n_or_positions, axis=0)` / `np.vsplit` / `np.hsplit` ｜ **返回** `list[ndarray]` ｜ **备注** 传整数要能整除

```python
import numpy as np
a = np.arange(6)
np.split(a, 3)                         # [array([0, 1]), array([2, 3]), array([4, 5])]
np.split(a, [2, 5])                    # [array([0, 1]), array([2, 3, 4]), array([5])]
[x.tolist() for x in np.split(a, 3)]   # [[0, 1], [2, 3], [4, 5]]
```

> ⚠️ 传整数 = 等分成几份（不能整除会报错）；传列表 = 在这些下标处切开。结果永远是**列表**，哪怕只有一份。

### `np.tile(A, reps) / np.repeat(a, repeats)` 重复数据

**签名** `np.tile(A, reps)` 整体重复 / `np.repeat(a, repeats)` 逐元素重复 ｜ **返回** `ndarray` ｜ **备注** tile 保持形状结构，repeat 会拉长

```python
import numpy as np
np.tile([1, 2], 3)                    # array([1, 2, 1, 2, 1, 2])
np.repeat([1, 2], 3)                  # array([1, 1, 1, 2, 2, 2])
np.tile(np.array([[1, 2]]), (2, 2))   # array([[1, 2, 1, 2], [1, 2, 1, 2]])
```

> ⚠️ `tile` 把整个数组当块来铺（形状会变），`repeat` 是每个元素重复 n 次（长度 ×n）；做特征扩展、构造测试数据常用。

## A9　线性代数

### `a @ b / np.matmul / np.dot` 矩阵乘法

**签名** `a @ b` / `np.matmul(a, b)` / `np.dot(a, b)` ｜ **返回** `ndarray` ｜ **备注** 不是逐元素乘法

```python
import numpy as np
A = np.array([[1, 2], [3, 4]])
B = np.array([[0, 1], [1, 0]])
A @ B                             # array([[2, 1], [4, 3]])
np.matmul(A, B)                   # array([[2, 1], [4, 3]])
A * B                             # array([[0, 2], [3, 0]])
v = np.array([1, 2])
A @ v                             # array([ 5, 11])
np.dot(v, v)                      # np.int64(5)
```

> ⚠️ **`A * B` 是逐元素相乘**，`A @ B` 才是矩阵乘法。一维数组之间 `np.dot(v, w)` 是**点积**（返回一个数），`matmul` 对一维也返回标量。

### `np.linalg.inv / det / solve` 逆矩阵 / 行列式 / 解方程

**签名** `np.linalg.inv(A)` / `np.linalg.det(A)` / `np.linalg.solve(A, b)` ｜ **返回** `ndarray` / `float` ｜ **备注** 奇异矩阵会报 `LinAlgError`

```python
import numpy as np
A = np.array([[1.0, 2.0], [3.0, 4.0]])
np.linalg.inv(A)                  # array([[-2. , 1. ], [ 1.5, -0.5]])
np.linalg.det(A).round(10)        # np.float64(-2.0)
b = np.array([5.0, 11.0])
np.linalg.solve(A, b)             # array([1., 2.])
np.linalg.inv(A) @ b              # array([1., 2.])
```

> ⚠️ 解 `Ax = b` 用 `solve`（快且稳），**别**手动 `inv(A) @ b`（后者既慢又不准，行列式接近 0 时误差会放大）。

### `np.linalg.eig / norm` 特征值 / 范数

**签名** `np.linalg.eig(A)` / `np.linalg.eigvals(A)` / `np.linalg.norm(x, ord=None)` ｜ **返回** 元组 / `ndarray` / `float` ｜ **备注** eig 可能返回复数

```python
import numpy as np
A = np.array([[2.0, 0.0], [0.0, 3.0]])
np.linalg.eigvals(A)              # array([2.+0.j, 3.+0.j])
vals, vecs = np.linalg.eig(A)
vals                              # array([2.+0.j, 3.+0.j])
v = np.array([3.0, 4.0])
np.linalg.norm(v)                 # np.float64(5.0)
np.linalg.norm(A)                 # np.float64(3.605551275463989)
```

> ⚠️ 非对称矩阵的特征值可能是**复数**（会带 `+0.j`），只要实部时用 `.real`；`norm` 不写 ord 就是常用欧氏长度。

## A10　排序与其他

### `np.sort(a) / np.argsort(a)` 排序 / 排序下标

**签名** `np.sort(a, axis=-1)` / `np.argsort(a, axis=-1)` ｜ **返回** `ndarray`（新数组） ｜ **备注** 返回副本，不改原数组

```python
import numpy as np
a = np.array([3, 1, 2])
np.sort(a)                        # array([1, 2, 3])
a                                 # array([3, 1, 2])
np.argsort(a)                     # array([1, 2, 0])
a[np.argsort(a)]                  # array([1, 2, 3])
m = np.array([[3, 1], [2, 4]])
np.sort(m, axis=0)                # array([[2, 1], [3, 4]])
```

> ⚠️ `np.sort` 返回**新数组**（原地排序用 `a.sort()`）；`argsort` 给的是下标，`a[argsort]` 就是排好序的原数组，取「前 3 大」时特别有用。

### `np.minimum(a, b) / np.maximum(a, b)` 逐元素取小 / 取大

**签名** `np.minimum(a, b)` / `np.maximum(a, b)` / `np.fmax` / `np.fmin` ｜ **返回** `ndarray` ｜ **备注** 和聚合的 min/max 不同

```python
import numpy as np
a = np.array([1, 5, 3])
b = np.array([4, 2, 3])
np.minimum(a, b)                  # array([1, 2, 3])
np.maximum(a, b)                  # array([4, 5, 3])
a.min()                           # np.int64(1)
```

> ⚠️ `np.minimum(a, b)` 是**两个数组逐元素比大小**；`a.min()` 是把 a 压成一个最小值。名字只差一个 `m`，最容易看错。

### `np.meshgrid(x, y)` 生成二维坐标网格

**签名** `np.meshgrid(x, y, indexing="xy")` ｜ **返回** 两个 `ndarray` ｜ **备注** 画 3D 曲面 / 等高线必备

```python
import numpy as np
x = np.array([0, 1, 2])
y = np.array([0, 10])
X, Y = np.meshgrid(x, y)
X                                 # array([[0, 1, 2], [0, 1, 2]])
Y                                 # array([[ 0, 0, 0], [10, 10, 10]])
X.shape                           # (2, 3)
```

> ⚠️ 返回的 `X`、`Y` 形状都是 `(len(y), len(x))`：`X` 每行相同（横坐标铺开）、`Y` 每列相同（纵坐标铺开），这样 `f(X, Y)` 就能算出整张曲面。

### `a.astype(dtype)` 转换元素类型

**签名** `a.astype(dtype)` ｜ **返回** `ndarray`（副本） ｜ **备注** 返回副本，原数组不变

```python
import numpy as np
a = np.array([1.7, 2.9])
a.astype(int)                     # array([1, 2])
a.astype(str)                     # array(['1.7', '2.9'], dtype='<U32')
a.dtype                           # dtype('float64')
a.astype(int).dtype               # dtype('int64')
```

> ⚠️ `astype(int)` 是**截断**（1.7 → 1），不是四舍五入；要四舍五入先 `np.round(a)`。转换总会复制一份新数组。

### `np.savetxt / np.loadtxt` 数组存成文本文件 / 读回来

**签名** `np.savetxt(fname, a, delimiter=",", fmt="%.2f")` / `np.loadtxt(fname, delimiter=",")` ｜ **返回** 无 / `ndarray` ｜ **备注** 二进制用 `np.save` / `np.load`

```python
import numpy as np
a = np.arange(4).reshape(2, 2)
np.savetxt("data.csv", a, delimiter=",", fmt="%d")
print(open("data.csv").read().strip())
# ↑ 屏幕输出（每行一个子数组）：0,1 与 2,3
np.loadtxt("data.csv", delimiter=",", dtype=int)   # array([[0, 1], [2, 3]])
```

> ⚠️ CSV 是**纯文本、没有 dtype 信息**，读回来要自己传 `dtype`；要连类型一起保存用 `np.save("a.npy", a)` + `np.load("a.npy")`（或 `.npz` 存多个数组）。

## 学习建议

1. **先记这 12 个**：`np.array` `np.arange` `np.linspace` `np.zeros/ones` `a.reshape` `a.T` `a.sum/mean` `axis` 用法 `a[a > x]`（布尔索引）`a @ b` `np.concatenate`。
2. **`a * b` 是逐元素，`a @ b` 才是矩阵乘法** —— 新手最容易混的一点。
3. **`axis` 方向**：`axis=0` 沿行方向（对各列算），`axis=1` 沿列方向（对各行算）；不写就是对所有元素。
4. **视图 vs 副本**：切片、`reshape`、`ravel`、`a.T` 返回**视图**（改它会动原数组）；花式索引、`flatten`、`a.copy()` 返回**副本**。
5. **能用数组运算就别写 for 循环**：NumPy 的核心价值是向量化，速度差几个数量级。
