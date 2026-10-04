# Numpy 常用函数速查笔记

> 收集范围：数据分析 / 数值计算里最常用的 NumPy 操作，覆盖创建、索引、变形、运算、统计、拼接与线代。
> 每条都是「**解析 ｜ 操作 ｜ 提醒**」三段：解析讲干什么（参数表 + 返回），操作是可复制运行的示例（`#` 后面是**真实输出**），提醒是易错点。
> 约定：示例里都写 `import numpy as np`，数组变量统一叫 `a` / `b`。

## 怎么用这份文件

- **先查索引**：`## 索引 · 速查表` 在最前，一行一个函数，点链接直接跳到正文。
- **章节按使用频率排**：A1 数组创建 → A2 数组属性 → A3 索引与切片 → A4 形状变换 → A5 数学运算与广播 → A6 统计函数 → A7 逻辑与条件 → A8 拼接与分割 → A9 线性代数 → A10 排序与其他。
- **允许跨板块重复**：axis 的用法、视图与副本等关键概念在相关条目里会反复出现，这是故意的——从索引直接跳，不必来回翻。
- **条目格式固定**：`### `名字` 一句话作用` → **解析**（干什么 + 参数表 + 返回）→ **操作**（可复制运行的示例）→ **提醒**（易错点，没有就不写）。

---

## 索引 · 速查表

| 分类 | 用法（点击跳转） | 一句话作用 |
|------|------------------|-----------|
| A1 数组创建 | [`np.array(object, dtype=None)`](#nparrayobject-dtypenone-从列表元组建数组) | 从列表/元组建数组 |
| A1 数组创建 | [`np.arange(start, stop, step)`](#nparangestart-stop-step-等差序列左闭右开) | 等差序列（左闭右开） |
| A1 数组创建 | [`np.linspace(start, stop, num)`](#nplinspacestart-stop-num-等分点含右端点) | 等分点（含右端点） |
| A1 数组创建 | [`np.zeros(shape)、np.ones(shape)`](#npzerosshapenponesshape-全-0全-1-数组) | 全 0、全 1 数组 |
| A1 数组创建 | [`np.full(shape, fill_value)`](#npfullshape-fill_value-全部填成同一个值) | 全部填成同一个值 |
| A1 数组创建 | [`np.eye(n, k=0)`](#npeyen-k0-单位矩阵对角为-1) | 单位矩阵（对角为 1） |
| A1 数组创建 | [`np.empty(shape)`](#npemptyshape-只分配内存不初始化) | 只分配内存、不初始化 |
| A1 数组创建 | [`np.zeros_like(a)、np.ones_like(a)、np.full_like(a, v)`](#npzeros_likeanpones_likeanpfull_likea-v-照-a-的形状造新数组) | 照 a 的形状造新数组 |
| A1 数组创建 | [`np.random.default_rng(seed)`](#nprandomdefault_rngseed-新版随机数生成器) | 新版随机数生成器 |
| A2 数组属性 | [`a.shape、a.ndim、a.size、a.dtype、a.itemsize`](#ashapeandimasizeadtypeaitemsize-看数组的体检报告) | 看数组的「体检报告」 |
| A3 索引与切片 | [`a[i]、a[i, j]（基础索引切片）`](#aiai-j基础索引切片-多维用逗号分隔各维) | 多维用逗号分隔各维 |
| A3 索引与切片 | [`布尔索引 a[a>x]`](#布尔索引-aax-按条件筛元素) | 按条件筛元素 |
| A3 索引与切片 | [`花式索引 a[[0, 2]]`](#花式索引-a0-2-用整数数组按位置取) | 用整数数组按位置取 |
| A3 索引与切片 | [`np.where(condition, x, y)`](#npwherecondition-x-y-条件选择找下标) | 条件选择、找下标 |
| A3 索引与切片 | [`a.copy()（视图 vs 副本）`](#acopy视图-vs-副本-什么时候需要复制) | 什么时候需要复制 |
| A4 形状变换 | [`a.reshape(new_shape)`](#areshapenew_shape-改形状元素总数不变) | 改形状（元素总数不变） |
| A4 形状变换 | [`a.ravel()、a.flatten()`](#aravelaflatten-展平成一维) | 展平成一维 |
| A4 形状变换 | [`a.T、np.transpose(a)`](#atnptransposea-转置行列互换) | 转置（行列互换） |
| A4 形状变换 | [`np.expand_dims(a, axis)、np.squeeze(a)`](#npexpand_dimsa-axisnpsqueezea-加一维去多余的-1-维) | 加一维、去多余的 1 维 |
| A4 形状变换 | [`np.stack(arrays, axis=0)`](#npstackarrays-axis0-沿新轴把多个数组摞起来) | 沿**新轴**把多个数组摞起来 |
| A5 数学运算与广播 | [`逐元素算术`](#逐元素算术-运算符-作用于整个数组) | 运算符+、-、*、/、**、//、%作用于整个数组 |
| A5 数学运算与广播 | [`通用函数 ufunc（np.sqrt、exp、log…）`](#通用函数-ufuncnpsqrtexplog-逐元素数学函数) | 逐元素数学函数 |
| A5 数学运算与广播 | [`广播 broadcasting`](#广播-broadcasting-形状不同也能运算) | 形状不同也能运算 |
| A5 数学运算与广播 | [`np.clip(a, a_min, a_max)`](#npclipa-a_min-a_max-把值夹到区间内) | 把值夹到区间内 |
| A6 统计函数 | [`a.sum(axis=None)`](#asumaxisnone-求和可按轴) | 求和（可按轴） |
| A6 统计函数 | [`a.mean()、a.std()、a.var()`](#ameanastdavar-均值标准差方差) | 均值、标准差、方差 |
| A6 统计函数 | [`a.min()、a.max()（含 axis）`](#aminamax含-axis-最小最大聚合) | 最小、最大（聚合） |
| A6 统计函数 | [`np.median(a)、np.percentile(a, q)`](#npmediananppercentilea-q-中位数分位数) | 中位数、分位数 |
| A6 统计函数 | [`np.prod(a, axis=None)`](#npproda-axisnone-连乘) | 连乘 |
| A6 统计函数 | [`np.argmin(a)、np.argmax(a)`](#npargminanpargmaxa-极值所在的下标) | 极值所在的**下标** |
| A6 统计函数 | [`np.argwhere(condition)`](#npargwherecondition-所有满足条件的坐标) | 所有满足条件的坐标 |
| A6 统计函数 | [`np.cumsum、np.cumprod、np.diff`](#npcumsumnpcumprodnpdiff-累计和累计积相邻差分) | 累计和、累计积、相邻差分 |
| A6 统计函数 | [`np.nansum、np.nanmean`](#npnansumnpnanmean-跳过-nan-的统计) | 跳过 NaN 的统计 |
| A7 逻辑与条件 | [`(a>5).any()、(a>5).all()`](#a5anya5all-有没有是不是全部) | 有没有、是不是全部 |
| A7 逻辑与条件 | [`np.logical_and、np.logical_or、np.logical_not（&、｜、~）`](#nplogical_andnplogical_ornplogical_not-布尔数组的与或非) | 布尔数组的与或非 |
| A7 逻辑与条件 | [`np.isnan、np.isinf、np.isfinite`](#npisnannpisinfnpisfinite-找缺失值与无穷) | 找缺失值与无穷 |
| A7 逻辑与条件 | [`np.unique(a, return_counts=True)`](#npuniquea-return_countstrue-去重默认排序) | 去重（默认排序） |
| A7 逻辑与条件 | [`np.allclose(a, b)`](#npallclosea-b-浮点数组是否近似相等) | 浮点数组是否「近似相等」 |
| A8 拼接与分割 | [`np.concatenate、np.vstack、np.hstack`](#npconcatenatenpvstacknphstack-拼接数组) | 拼接数组 |
| A8 拼接与分割 | [`np.split(a, indices_or_sections)`](#npsplita-indices_or_sections-分割数组) | 分割数组 |
| A8 拼接与分割 | [`np.tile(A, reps)、np.repeat(a, repeats)`](#nptilea-repsnprepeata-repeats-重复数据) | 重复数据 |
| A9 线性代数 | [`a@b、np.matmul、np.dot`](#abnpmatmulnpdot-矩阵乘法) | 矩阵乘法 |
| A9 线性代数 | [`np.linalg.inv、np.linalg.det、np.linalg.solve`](#nplinalginvnplinalgdetnplinalgsolve-逆矩阵行列式解方程) | 逆矩阵、行列式、解方程 |
| A9 线性代数 | [`np.linalg.eig、np.linalg.norm`](#nplinalgeignplinalgnorm-特征值范数) | 特征值、范数 |
| A10 排序与其他 | [`np.sort(a)、np.argsort(a)`](#npsortanpargsorta-排序排序下标) | 排序、排序下标 |
| A10 排序与其他 | [`np.minimum(a, b)、np.maximum(a, b)`](#npminimuma-bnpmaximuma-b-逐元素取小取大) | 逐元素取小、取大 |
| A10 排序与其他 | [`np.meshgrid(x, y)`](#npmeshgridx-y-生成二维坐标网格) | 生成二维坐标网格 |
| A10 排序与其他 | [`a.astype(dtype)`](#aastypedtype-转换元素类型) | 转换元素类型 |
| A10 排序与其他 | [`np.savetxt、np.loadtxt`](#npsavetxtnploadtxt-数组存成文本文件读回来) | 数组存成文本文件、读回来 |

---

## A1 数组创建

### `np.array(object, dtype=None)` 从列表/元组建数组

**解析**　把列表或元组（可嵌套）变成 NumPy 数组，是最常用的建数组方法。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| object | 必填 | 列表、元组等序列；嵌套的表示多维数组 |
| dtype | None | 元素类型；不写就自动推断 |

返回：ndarray 数组；混类型会被统一成一种 dtype

**操作**

```python
import numpy as np

np.array([1, 2, 3])                # array([1, 2, 3])

np.array([[1, 2], [3, 4]])         # array([[1, 2], [3, 4]])

np.array([1, 2, 3], dtype=float)   # array([1., 2., 3.])

np.array([1, 2, 3]).dtype          # dtype('int64')
```

> ⚠️ 列表里混了字符串就会整体变成字符串数组（`np.array([1, "a"])`）；要固定类型就显式传 `dtype=`。

### `np.arange(start, stop, step)` 等差序列（左闭右开）

**解析**　生成等差数列（整数、小数都行），和 `range` 一样**不含终点**。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| start_or_stop | 必填 | 只传一个数时它是终点（从 0 开始）；传多个时它是起点 |
| stop | None | 终点（不含本身） |
| step | 1 | 步长（可为小数） |

返回：ndarray 等差数组；**不含 stop**，和 `range` 一样

**操作**

```python
import numpy as np

np.arange(5)                      # array([0, 1, 2, 3, 4])

np.arange(2, 8)                   # array([2, 3, 4, 5, 6, 7])

np.arange(0, 10, 2)               # array([0, 2, 4, 6, 8])

np.arange(0, 1, 0.25)             # array([0. , 0.25, 0.5 , 0.75])
```

> ⚠️ 浮点步长会有累计误差（`np.arange(0, 1, 0.1)` 的末位不准），要精确等分改用 `np.linspace`。

### `np.linspace(start, stop, num)` 等分点（含右端点）

**解析**　在 start 和 stop 之间等距取 num 个点，**包含 stop**（这点和 arange 相反）。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| start | 必填 | 起点 |
| stop | 必填 | 终点（包含在内） |
| num | 50 | 一共取几个点 |
| endpoint | True | 是否包含右端点；写 False 就不含 stop |

返回：ndarray；**含 stop**，这点和 arange 相反

**操作**

```python
import numpy as np

np.linspace(0, 1, 5)                    # array([0. , 0.25, 0.5 , 0.75, 1. ])

np.linspace(0, 10, 3)                   # array([ 0., 5., 10.])

np.linspace(0, 10, 3, endpoint=False)   # array([0. , 3.33333333, 6.66666667])
```

> ⚠️ `linspace(0, 1, 5)` 是「切成 5 个点、4 段」；想要步长而不是点数，用 `arange`。画图取 x 坐标几乎都用它。

### `np.zeros(shape)、np.ones(shape)` 全 0、全 1 数组

**解析**　造一个全 0（或全 1）的数组；形状用元组给，比如 (2, 3) 是 2 行 3 列。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| shape | 必填 | 形状元组，如 (2, 3)；一维可只写数字 |
| dtype | None | 元素类型；不写就是浮点，要整数传 dtype=int |

返回：ndarray 全 0、全 1 数组；shape 要传**元组**

**操作**

```python
import numpy as np

np.zeros(3)                       # array([0., 0., 0.])

np.zeros((2, 3))                  # array([[0., 0., 0.], [0., 0., 0.]])

np.ones((2, 2))                   # array([[1., 1.], [1., 1.]])

np.ones((2, 2), dtype=int)        # array([[1, 1], [1, 1]])
```

> ⚠️ 多维形状必须写成元组：`np.zeros(2, 3)` 会报 TypeError。默认 dtype 是浮点，要整数传 `dtype=int`。

### `np.full(shape, fill_value)` 全部填成同一个值

**解析**　造一个所有元素都是同一个值的数组，比 zeros 完再加更直接。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| shape | 必填 | 形状元组 |
| fill_value | 必填 | 要填的值 |
| dtype | None | 元素类型；不写就按 fill_value 推断 |

返回：ndarray；比 `zeros(...) + 5` 更直观

**操作**

```python
import numpy as np

np.full((2, 3), 7)                # array([[7, 7, 7], [7, 7, 7]])

np.full(3, 1.5)                   # array([1.5, 1.5, 1.5])

np.full(3, 9, dtype=float)        # array([9., 9., 9.])
```

### `np.eye(n, k=0)` 单位矩阵（对角为 1）

**解析**　造单位矩阵：对角线全是 1、其余是 0；`k` 可以让对角线偏移。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| N | 必填 | 行数（默认列数同 N） |
| k | 0 | 对角线偏移：1 = 对角线上移一行，-1 = 下移 |

返回：ndarray 单位矩阵；`k` 控制对角线偏移

**操作**

```python
import numpy as np

np.eye(3)                         # array([[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]])

np.eye(3, k=1)                    # array([[0., 1., 0.], [0., 0., 1.], [0., 0., 0.]])

np.eye(3, dtype=int)              # array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
```

> ⚠️ `eye(n)` 用于构造单位矩阵（做线代、one-hot 编码）；`np.identity(n)` 只能是对角为 1，不能偏移。

### `np.empty(shape)` 只分配内存、不初始化

**解析**　只分配一块内存但不初始化，里面的数是随机垃圾值，只适合「先占位、马上整体赋值」。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| shape | 必填 | 形状元组 |
| dtype | None | 元素类型 |

返回：ndarray；内容**随机**，不要依赖初值

**操作**

```python
import numpy as np

e = np.empty((2, 2))

e.shape                           # (2, 2)
# 值未初始化，可能是任意数（甚至很大的数），只用于「先占位、马上整体赋值」
```

> ⚠️ 别拿 `empty` 当 `zeros` 用；它的好处只有一个：快。日常用 `zeros` 更安全。

### `np.zeros_like(a)、np.ones_like(a)、np.full_like(a, v)` 照 a 的形状造新数组

**解析**　照着数组 a 的形状（和类型）造一个同样大小的全 0 / 全 1 / 全 v 数组。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| a | 必填 | 参照数组：形状和 dtype 都照它来 |
| fill_value | 必填 | （仅 full_like）要填的值 |
| dtype | None | 元素类型；不写 = 照 a 的来 |

返回：ndarray；继承 a 的 shape 和 **dtype**

**操作**

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

**解析**　造一个随机数生成器 rng，再用 rng.random / integers / normal / choice / shuffle 取随机数；固定 seed 结果可复现。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| seed | None | 随机种子；固定一个整数，每次运行结果都一样 |

返回：`Generator` 对象（后面接 `.random` / `.integers` / `.normal` / `.choice` / `.shuffle`）；固定 seed 结果可复现

**操作**

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

## A2 数组属性

### `a.shape、a.ndim、a.size、a.dtype、a.itemsize` 看数组的「体检报告」

**解析**　用属性查看数组的基本情况：形状、几维、元素总数、元素类型、每个元素占几字节。

返回：shape 是元组、ndim / size / itemsize / nbytes 是整数、dtype 是类型对象；属性不带括号

**操作**

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

## A3 索引与切片

### `a[i]、a[i, j]（基础索引切片）` 多维用逗号分隔各维

**解析**　用下标或切片取元素；多维数组用逗号分隔各维（`a[i, j]`），行列也能一起切 `a[i:j, k:l]`。

返回：单个元素 / **视图** ndarray；切片返回视图，共享内存

**操作**

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

### `布尔索引 a[a>x]` 按条件筛元素

**解析**　把「哪些元素满足条件」的布尔数组放进方括号，筛出所有满足条件的元素。

返回：一维 `ndarray`（副本）；多条件要 `&` `|` 并加括号

**操作**

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

**解析**　用整数数组（或列表）当「点名册」，按位置把对应的元素挑出来。

返回：**副本** `ndarray`（和切片不同，返回副本）

**操作**

```python
import numpy as np

a = np.array([10, 20, 30, 40])

a[[0, 2]]                         # array([10, 30])

b = np.arange(12).reshape(3, 4)

b[[0, 2]]                         # array([[ 0, 1, 2, 3], [ 8, 9, 10, 11]])

b[[0, 2], [1, 3]]                 # array([ 1, 11])
```

> ⚠️ `a[[0, 2], [1, 3]]` 取的是 `(0,1)` 和 `(2,3)` 两个**配对**元素，不是行列交叉的 2×2 子块（那要用 `np.ix_`）。

### `np.where(condition, x, y)` 条件选择、找下标

**解析**　像 Excel 的 IF：条件为真的位置取 x、为假的位置取 y；只传条件时返回满足条件的下标。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| condition | 必填 | 布尔条件（数组） |
| x | None | 条件为真的位置填 x |
| y | None | 条件为假的位置填 y |

返回：`ndarray`（选择结果）/ 下标元组（单参数）；单参数版等于 `np.nonzero`

**操作**

```python
import numpy as np

a = np.array([1, 5, 8, 3])

np.where(a > 4, 1, 0)             # array([0, 1, 1, 0])

np.where(a > 4)                   # (array([1, 2]),)

np.where(a > 4)[0]                # array([1, 2])
```

> ⚠️ 只传一个参数时返回的是**下标元组**（多维也如此），要一维下标就取 `[0]`。类似 Excel 的 IF。

### `a.copy()（视图 vs 副本）` 什么时候需要复制

**解析**　把数组完整复制一份，和原数组彻底脱钩；切片只是「视图」（共用数据），要独立就 copy。

返回：`ndarray` 副本；切片是视图、花式索引是副本

**操作**

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

## A4 形状变换

### `a.reshape(new_shape)` 改形状（元素总数不变）

**解析**　给数组换个形状（元素总数必须不变）；某维写 -1 表示让 NumPy 自己算。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| new_shape | 必填 | 新形状（元素总数必须不变）；其中一维可写 -1 自动推断 |

返回：**视图** `ndarray`（多数情况）；总数不符报 `ValueError`

**操作**

```python
import numpy as np

a = np.arange(12)

a.reshape(3, 4)                    # array([[ 0, 1, 2, 3], [ 4, 5, 6, 7], [ 8, 9, 10, 11]])

a.reshape(2, -1)                   # array([[ 0, 1, 2, 3, 4, 5], [ 6, 7, 8, 9, 10, 11]])

a.reshape(-1, 1).shape             # (12, 1)

a.reshape(3, 4).base is not None   # True
```

> ⚠️ `-1` 只允许出现一次，让 NumPy 算剩下的；`a.reshape(5, 5)` 会因元素数不匹配报错。原数组本身不变。

### `a.ravel()、a.flatten()` 展平成一维

**解析**　把多维数组摊成一维；ravel 返回视图（快、改了会动原数组），flatten 返回副本（安全、占内存）。

返回：`ndarray`；ravel 是视图（改它会动原数组），flatten 是副本

**操作**

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

### `a.T、np.transpose(a)` 转置（行列互换）

**解析**　把行列互换；一维数组转置没有变化。三维以上用 np.transpose 指定轴顺序。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| axes | None | （transpose 用）新的轴顺序，如 (1, 0, 2) |

返回：**视图** `ndarray`；一维数组转置无变化

**操作**

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

### `np.expand_dims(a, axis)、np.squeeze(a)` 加一维、去多余的 1 维

**解析**　expand_dims 在指定位置加一个长度为 1 的维；squeeze 把长度为 1 的维删掉。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| a | 必填 | 数组 |
| axis | 必填 / None | expand_dims：新维插在哪个位置；squeeze：要删的维（不写 = 删所有长度为 1 的维） |

返回：`ndarray`；squeeze 只删长度为 1 的维

**操作**

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

**解析**　把形状相同的多个数组沿一条**新轴**摞起来，结果比原来多一维；concatenate 沿已有轴拼、不加维。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| arrays | 必填 | 形状相同的数组序列 |
| axis | 0 | 新轴插在哪个位置 |

返回：`ndarray`（比原来多一维）；和 concatenate 的区别：stack 会加维度

**操作**

```python
import numpy as np

a = np.array([1, 2])

b = np.array([3, 4])

np.stack([a, b])                  # array([[1, 2], [3, 4]])

np.stack([a, b], axis=1)          # array([[1, 3], [2, 4]])

np.stack([a, b]).shape            # (2, 2)
```

> ⚠️ `np.stack([a, b])` 结果形状 `(2, 2)`，比原来多一维；`np.concatenate` 保持维度不变。形状不同的数组不能 stack。

## A5 数学运算与广播

### `逐元素算术` 运算符+、-、*、/、**、//、%作用于整个数组

**解析**　加减乘除等运算符直接对整个数组逐元素计算，返回新数组；`*` 是逐元素乘，不是矩阵乘。

返回：`ndarray`（**新数组**）；`*` 是逐元素，不是矩阵乘

**操作**

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

### `通用函数 ufunc（np.sqrt、exp、log…）` 逐元素数学函数

**解析**　开方、指数、对数这些数学函数（名字和 math 库一样），对整个数组逐元素计算。

返回：`ndarray`；名字和 `math` 一样，但作用在整个数组

**操作**

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

**解析**　两个形状不同的数组也能直接运算：NumPy 从尾巴往前对形状，相等或其中一个是 1 就兼容，自动「复制补齐」。

返回：`ndarray`；不兼容会 `ValueError`

**操作**

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

**解析**　把数组里的值限制在区间内：小于下限的换成下限，大于上限的换成上限。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| a | 必填 | 要处理的数组 |
| a_min | 必填 | 下限：小于它的都换成它 |
| a_max | 必填 | 上限：大于它的都换成它 |

返回：`ndarray`；超界值被替换成边界值

**操作**

```python
import numpy as np

a = np.array([-3, 0, 5, 9])

np.clip(a, 0, 5)                  # array([0, 0, 5, 5])

a.clip(0, 5).tolist()             # [0, 0, 5, 5]
```

> ⚠️ 常用于把预测值/颜色值限制在合法范围；等价写法 `np.minimum(np.maximum(a, 0), 5)`，但 clip 更清楚。

## A6 统计函数

### `a.sum(axis=None)` 求和（可按轴）

**解析**　求和；不写 axis 是对全部元素，写 axis=0 按列、axis=1 按行。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| axis | None | 沿哪一维算：0 按列、1 按行；不写 = 全部元素 |
| keepdims | False | 是否保留被压缩的那一维（True 便于后续广播） |

返回：标量 / `ndarray`；`axis` 决定沿哪一维算

**操作**

```python
import numpy as np

a = np.array([[1, 2, 3], [4, 5, 6]])

a.sum()                              # np.int64(21)

a.sum(axis=0)                        # array([5, 7, 9])

a.sum(axis=1)                        # array([ 6, 15])

a.sum(axis=1, keepdims=True).shape   # (2, 1)
```

> ⚠️ `axis=0` = 把每一**列**压成一行（纵向合并），`axis=1` = 把每一**行**压成一列；不写 axis 就是全部元素。`keepdims=True` 保留维度，方便后续广播。

### `a.mean()、a.std()、a.var()` 均值、标准差、方差

**解析**　求均值、标准差、方差；不写 axis 是对全部元素，写 axis 可按行/列。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| axis | None | 沿哪一维算；不写 = 全部元素 |
| ddof | 0 | 方差/标准差的自由度修正：样本口径写 ddof=1 |

返回：`float` / `ndarray`；都是总体口径（ddof=0）

**操作**

```python
import numpy as np

a = np.array([1, 2, 3, 4])

a.mean()                                      # np.float64(2.5)

a.std().round(4)                              # np.float64(1.118)

a.var()                                       # np.float64(1.25)

np.mean(np.array([[1, 2], [3, 4]]), axis=0)   # array([2., 3.])
```

> ⚠️ 方差/标准差默认除以 N（总体）；要样本口径（除以 N-1）传 `ddof=1`：`a.std(ddof=1)`。

### `a.min()、a.max()（含 axis）` 最小、最大（聚合）

**解析**　求最小 / 最大值（把数组压成一个数）；写 axis 就是沿某方向各自求。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| axis | None | 沿哪一维算；不写 = 全部元素 |

返回：标量 / `ndarray`；逐元素取小用 `np.minimum`

**操作**

```python
import numpy as np

a = np.array([[3, 1], [2, 5]])

a.min()                           # np.int64(1)

a.max()                           # np.int64(5)

a.max(axis=0)                     # array([3, 5])

a.min(axis=1)                     # array([1, 2])
```

> ⚠️ `a.max()` 返回**一个数**（聚合），`np.maximum(a, b)` 返回**逐元素取大的数组**，别混。

### `np.median(a)、np.percentile(a, q)` 中位数、分位数

**解析**　求中位数（50 分位）和任意分位数；数据里有离群值时比均值更能代表典型值。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| a | 必填 | 数组 |
| q | 必填 | （percentile）分位点（0~100 的百分数），如 75 = 75 分位 |
| axis | None | 沿哪一维算 |

返回：`float` / `ndarray`；抗离群值

**操作**

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

**解析**　把所有元素连乘求积；空数组返回 1。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| a | 必填 | 数组 |
| axis | None | 沿哪一维算 |

返回：标量 / `ndarray`；空数组返回 1

**操作**

```python
import numpy as np

np.prod([1, 2, 3, 4])                         # np.int64(24)

np.prod(np.array([[1, 2], [3, 4]]), axis=1)   # array([ 2, 12])
```

> ⚠️ 元素多时很容易溢出成 `inf` 或 0，真要算大数乘积考虑取对数后求和。

### `np.argmin(a)、np.argmax(a)` 极值所在的**下标**

**解析**　找最大值 / 最小值所在的**下标**（注意是下标不是值）；不写 axis 时下标按展平顺序算。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| a | 必填 | 数组 |
| axis | None | 沿哪一维找；不写 = 展平后找 |

返回：`int` / `ndarray`；返回展平后的下标

**操作**

```python
import numpy as np

a = np.array([3, 1, 4, 1, 5])

a.argmax()                                  # np.int64(4)

a.argmin()                                  # np.int64(1)

np.array([[1, 9], [8, 2]]).argmax(axis=0)   # array([1, 0])
```

> ⚠️ 有并列时返回**第一个**；不写 axis 时按下标是按「展平（C 顺序）」算的：`np.unravel_index(idx, a.shape)` 可以还原成多维坐标。

### `np.argwhere(condition)` 所有满足条件的坐标

**解析**　找出所有满足条件的元素的坐标（行、列都给出），比 where 单参数版更好读。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| condition | 必填 | 布尔条件 |

返回：形状 (n, ndim) 的 `ndarray`；比 `np.where` 单参数版更好读

**操作**

```python
import numpy as np

a = np.array([[1, 6], [7, 2]])

np.argwhere(a > 5)                # array([[0, 1], [1, 0]])

np.argwhere(a > 5).tolist()       # [[0, 1], [1, 0]]
```

> ⚠️ 返回的是 `[[行, 列], ...]`；只要一维下标就用 `np.where(cond)[0]`。

### `np.cumsum、np.cumprod、np.diff` 累计和、累计积、相邻差分

**解析**　cumsum 逐位累加（前缀和）、cumprod 逐位累乘、diff 算相邻两个元素的差（后减前）。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| axis | None | 沿哪一维算 |
| n | 1 | （diff）做几次差分 |

返回：`ndarray`；`diff` 结果长度减 1

**操作**

```python
import numpy as np

a = np.array([1, 2, 3, 4])

a.cumsum()                        # array([ 1, 3, 6, 10])

np.cumprod(a)                     # array([ 1, 2, 6, 24])

np.diff(a)                        # array([1, 1, 1])

np.diff(a, n=2)                   # array([0, 0])
```

> ⚠️ `cumsum` 常用于「前缀和」；`diff` 是**后一个减前一个**，所以长度比原数组少 1（求相邻变化量、算收益率）。

### `np.nansum、np.nanmean` 跳过 NaN 的统计

**解析**　求和 / 求均值时自动跳过 NaN；普通 sum 碰到 NaN 会整个变 NaN。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| a | 必填 | 数组（可能含 NaN） |
| axis | None | 沿哪一维算 |

返回：`float` / `ndarray`；普通 sum 遇到 NaN 会全变 NaN

**操作**

```python
import numpy as np

a = np.array([1.0, np.nan, 3.0])

a.sum()                           # np.float64(nan)

np.nansum(a)                      # np.float64(4.0)

np.nanmean(a)                     # np.float64(2.0)
```

> ⚠️ 数据里缺值（NaN）时用 `nan*` 系列；先 `np.isnan(a).sum()` 看看有多少个缺失值。

## A7 逻辑与条件

### `(a>5).any()、(a>5).all()` 有没有、是不是全部

**解析**　any 问「有没有为真的」，all 问「是不是全为真」；一般先做比较得到布尔数组再问。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| axis | None | 沿哪一维判断；不写 = 整个数组 |

返回：`bool` / `ndarray`；结果是 numpy.bool_，直接用于 if 没问题

**操作**

```python
import numpy as np

a = np.array([1, 6, 8])

(a > 5).any()                            # np.True_

(a > 5).all()                            # np.False_

(a > 0).all()                            # np.True_

np.array([[1, 6], [7, 2]]).any(axis=0)   # array([ True, True])
```

> ⚠️ **先做比较得到布尔数组**，再 any/all：写 `a.any() > 5` 是错的（那是「有没有非零元素」）。

### `np.logical_and、np.logical_or、np.logical_not（&、｜、~）` 布尔数组的与或非

**解析**　对布尔数组做与 / 或 / 非；`&`、`|`、`~` 是运算符写法，每个比较都要加括号。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| x1、x2 | 必填 | 两个布尔数组 |

返回：布尔 `ndarray`；条件必须加括号

**操作**

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

### `np.isnan、np.isinf、np.isfinite` 找缺失值与无穷

**解析**　逐个判断数组里的元素是不是 NaN / 无穷 / 有限数，返回布尔数组，常用来清洗数据。

返回：布尔 `ndarray`；整数数组恒为 False/True（不报错）

**操作**

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

**解析**　去重并**排序**；return_counts=True 时顺带返回每个值出现几次。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| ar | 必填 | 数组 |
| return_counts | False | True 时额外返回每个值出现的次数 |
| return_index | False | True 时额外返回每个值第一次出现的下标 |

返回：`ndarray` / 元组；比 Python 的 set 多了计数

**操作**

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

**解析**　判断两个数组是否「近似相等」（允许一点点浮点误差）；浮点比较不要用 ==。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| a、b | 必填 | 两个数组 |
| rtol | 1e-05 | 相对误差上限 |
| atol | 1e-08 | 绝对误差上限 |

返回：`bool`；浮点比较不要用 ==

**操作**

```python
import numpy as np

a = np.array([0.1 + 0.2, 1.0])

b = np.array([0.3, 1.0])

a == b                            # array([False, True])

np.allclose(a, b)                 # True
```

> ⚠️ 浮点运算有误差，`(0.1+0.2) == 0.3` 是 False；判断数组是否相等用 `np.allclose`。

## A8 拼接与分割

### `np.concatenate、np.vstack、np.hstack` 拼接数组

**解析**　把几个数组拼到一起：concatenate 沿指定轴拼，vstack 上下拼，hstack 左右拼。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| arrays | 必填 | 要拼的数组序列 |
| axis | 0 | 沿哪一维拼：0 上下、1 左右 |

返回：`ndarray`；除拼接轴外，其他维度必须一致

**操作**

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

**解析**　把一个数组切成几段：传整数 = 等分几份，传列表 = 在这些下标处切开。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| ary | 必填 | 要切的数组 |
| indices_or_sections | 必填 | 整数（等分几份）或下标列表（切点） |
| axis | 0 | 沿哪一维切 |

返回：`list[ndarray]`；传整数要能整除

**操作**

```python
import numpy as np

a = np.arange(6)

np.split(a, 3)                         # [array([0, 1]), array([2, 3]), array([4, 5])]

np.split(a, [2, 5])                    # [array([0, 1]), array([2, 3, 4]), array([5])]

[x.tolist() for x in np.split(a, 3)]   # [[0, 1], [2, 3], [4, 5]]
```

> ⚠️ 传整数 = 等分成几份（不能整除会报错）；传列表 = 在这些下标处切开。结果永远是**列表**，哪怕只有一份。

### `np.tile(A, reps)、np.repeat(a, repeats)` 重复数据

**解析**　tile 把整个数组当块铺多遍（像贴瓷砖）；repeat 把每个元素重复 n 次。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| A、a | 必填 | 数组 |
| reps | 必填 | （tile）沿各维重复几遍，可为元组 |
| repeats | 必填 | （repeat）每个元素重复几次 |

返回：`ndarray`；tile 保持形状结构，repeat 会拉长

**操作**

```python
import numpy as np

np.tile([1, 2], 3)                    # array([1, 2, 1, 2, 1, 2])

np.repeat([1, 2], 3)                  # array([1, 1, 1, 2, 2, 2])

np.tile(np.array([[1, 2]]), (2, 2))   # array([[1, 2, 1, 2], [1, 2, 1, 2]])
```

> ⚠️ `tile` 把整个数组当块来铺（形状会变），`repeat` 是每个元素重复 n 次（长度 ×n）；做特征扩展、构造测试数据常用。

## A9 线性代数

### `a@b、np.matmul、np.dot` 矩阵乘法

**解析**　做矩阵乘法（注意不是逐元素乘）：`@` 最好写；两个一维数组用 np.dot 得到点积（一个数）。

返回：`ndarray` / 标量；不是逐元素乘法

**操作**

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

### `np.linalg.inv、np.linalg.det、np.linalg.solve` 逆矩阵、行列式、解方程

**解析**　求逆矩阵、行列式、解线性方程组 Ax=b；矩阵奇异（不可逆）会报 LinAlgError。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| A | 必填 | 方阵（inv/det）或系数矩阵（solve） |
| b | 必填 | （solve）等号右边的向量 |

返回：`ndarray` / `float`；奇异矩阵会报 `LinAlgError`

**操作**

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

### `np.linalg.eig、np.linalg.norm` 特征值、范数

**解析**　eig 求特征值和特征向量；norm 求向量 / 矩阵的长度（范数）。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| a、x | 必填 | 方阵（eig）或向量/矩阵（norm） |
| ord | None | （norm）范数类型；不写 = 欧氏长度（2 范数） |

返回：元组 / `ndarray` / `float`；eig 可能返回复数

**操作**

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

## A10 排序与其他

### `np.sort(a)、np.argsort(a)` 排序、排序下标

**解析**　sort 返回排好序的新数组（原数组不动）；argsort 返回「第几小的数原来在哪个位置」的下标。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| a | 必填 | 数组 |
| axis | -1 | 沿哪一维排（默认最后一维） |

返回：`ndarray`（新数组）；返回副本，不改原数组

**操作**

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

### `np.minimum(a, b)、np.maximum(a, b)` 逐元素取小、取大

**解析**　两个数组（或数组和数字）逐元素比大小，取小的 / 大的那个，返回同样形状的数组。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| x1、x2 | 必填 | 两个数组（形状可广播） |

返回：`ndarray`；和聚合的 min/max 不同

**操作**

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

**解析**　用两个一维坐标轴生成二维坐标网格 X、Y，画 3D 曲面、等高线时都要先做这一步。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| x、y | 必填 | 两个一维坐标轴 |
| indexing | xy | xy = 笛卡尔坐标（默认）；ij = 矩阵下标顺序 |

返回：两个 `ndarray`（X、Y）；画 3D 曲面 / 等高线必备

**操作**

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

**解析**　把数组的元素整体换成另一种类型（比如 int 换 float、数字换字符串），返回副本。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| dtype | 必填 | 目标类型，如 int、float、str |

返回：`ndarray`（副本），原数组不变

**操作**

```python
import numpy as np

a = np.array([1.7, 2.9])

a.astype(int)                     # array([1, 2])

a.astype(str)                     # array(['1.7', '2.9'], dtype='<U32')

a.dtype                           # dtype('float64')

a.astype(int).dtype               # dtype('int64')
```

> ⚠️ `astype(int)` 是**截断**（1.7 → 1），不是四舍五入；要四舍五入先 `np.round(a)`。转换总会复制一份新数组。

### `np.savetxt、np.loadtxt` 数组存成文本文件、读回来

**解析**　把数组存成文本文件（CSV 等）或从文本文件读回来；要连类型一起存用 np.save / np.load。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| fname | 必填 | 文件名 |
| delimiter | 空格 / None | 分隔符；CSV 写 ','（loadtxt 不传则按空白分列） |
| fmt | %.18e | （savetxt）每个数的格式，整数可写 '%d' |
| dtype | float | （loadtxt）读回来转成什么类型 |

返回：savetxt 无返回 / loadtxt 返回 `ndarray`；二进制用 `np.save` / `np.load`

**操作**

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
