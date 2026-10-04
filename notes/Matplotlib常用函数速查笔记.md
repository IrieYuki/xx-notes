# Matplotlib 常用函数速查笔记

> 收集范围：画图最常用的 Matplotlib 操作，覆盖画布、基础图形、坐标轴、图例、子图、样式与保存。
> 每条都是「**解析 ｜ 操作 ｜ 提醒**」三段 + 可直接运行的示例。**画图代码本身没有「输出」**，所以示例后面都跟了可以检查的取值（如 `ax.get_title()`、`len(ax.lines)`），`#` 后面仍是**真实运行结果**。
> 约定：`import matplotlib.pyplot as plt`、`import numpy as np`；示例用**面向对象写法**（`fig, ax = plt.subplots()`，推荐），只在对比时用 pyplot 写法。
> ⚠️ 版本：本笔记在 **matplotlib 3.11.0** 上逐条跑通；有变动的地方标在条目里（`boxplot(labels=)` 已移除 → 用 `tick_labels=`）。

## 怎么用这份文件

- 先扫一遍「索引 · 速查表」，点条目名直接跳到正文；每个条目一个主题、一个可复制的示例。
- 每条固定三段：**解析**（干什么 + 参数表 + 返回什么）、**操作**（可直接运行的示例，`#` 后是真实输出）、**提醒**（要点和易错点，没有就不写）。
- 分类按日常使用频率排：画布（起手式）→ 基础图形 → 坐标轴与标题 → 图例与辅助元素 → 子图与布局 → 样式与字体 → 保存与显示。
- 允许跨板块重复：`plt.subplots()` 在 A1、A5 各写一遍（A1 讲起步、A5 讲子图网格），这是故意的——读者从索引直接跳，不用来回翻。

---

## 索引 · 速查表

| 分类 | 用法（点击跳转） | 一句话作用 |
|------|------------------|-----------|
| A1 画布与两种写法 | [`plt.subplots(nrows, ncols)`](#pltsubplotsnrows-ncols-画布轴推荐起点) | 画布+轴（推荐起点） |
| A1 画布与两种写法 | [`plt.figure(figsize, dpi)`](#pltfigurefigsize-dpi-只创建画布) | 只创建画布 |
| A1 画布与两种写法 | [`pyplot 式 vs 面向对象式`](#pyplot-式-vs-面向对象式-两种写法对比) | 两种写法对比 |
| A2 基础图形 | [`ax.plot(x, y)`](#axplotx-y-折线图最基础) | 折线图（最基础） |
| A2 基础图形 | [`ax.scatter(x, y)`](#axscatterx-y-散点图) | 散点图 |
| A2 基础图形 | [`ax.bar(x, height)、ax.barh(y, width)`](#axbarx-heightaxbarhy-width-柱状图水平柱状图) | 柱状图、水平柱状图 |
| A2 基础图形 | [`ax.hist(x, bins)`](#axhistx-bins-直方图看分布) | 直方图（看分布） |
| A2 基础图形 | [`ax.pie(x, labels, autopct)`](#axpiex-labels-autopct-饼图) | 饼图 |
| A2 基础图形 | [`ax.boxplot(data, tick_labels=)`](#axboxplotdata-tick_labels-箱线图看中位数与离群点) | 箱线图（看中位数与离群点） |
| A2 基础图形 | [`ax.imshow(data, cmap)+colorbar`](#aximshowdata-cmapcolorbar-显示矩阵图片) | 显示矩阵、图片 |
| A3 坐标轴与标题 | [`ax.set_title、set_xlabel、set_ylabel`](#axset_titleset_xlabelset_ylabel-标题与轴标签) | 标题与轴标签 |
| A3 坐标轴与标题 | [`ax.set_xlim(left, right)`](#axset_xlimleft-right-设置坐标轴范围) | 设置坐标轴范围 |
| A3 坐标轴与标题 | [`ax.set_xticks(ticks, labels)`](#axset_xticksticks-labels-自定义刻度位置与文字) | 自定义刻度位置与文字 |
| A3 坐标轴与标题 | [`ax.set_xscale("log")`](#axset_xscalelog-对数坐标轴) | 对数坐标轴 |
| A3 坐标轴与标题 | [`ax.grid、axhline、axvline`](#axgridaxhlineaxvline-网格与参考线) | 网格与参考线 |
| A3 坐标轴与标题 | [`ax.text(x, y, s)、ax.annotate(...)`](#axtextx-y-saxannotate-文字与带箭头标注) | 文字与带箭头标注 |
| A4 图例与辅助元素 | [`ax.legend(loc, frameon)`](#axlegendloc-frameon-图例) | 图例 |
| A4 图例与辅助元素 | [`ax.twinx()`](#axtwinx-双-y-轴) | 双 Y 轴 |
| A4 图例与辅助元素 | [`ax.fill_between(x, y1, y2)`](#axfill_betweenx-y1-y2-区域填充) | 区域填充 |
| A4 图例与辅助元素 | [`ax.errorbar(x, y, yerr)`](#axerrorbarx-y-yerr-误差棒) | 误差棒 |
| A5 子图与布局 | [`plt.subplot(nrows, ncols, index)`](#pltsubplotnrows-ncols-index-pyplot-式子图) | pyplot 式子图 |
| A5 子图与布局 | [`fig, axes=plt.subplots(2, 2)`](#fig-axespltsubplots2-2-面向对象式子图推荐) | 面向对象式子图（推荐） |
| A5 子图与布局 | [`fig.tight_layout()、plt.subplots_adjust()`](#figtight_layoutpltsubplots_adjust-子图间距) | 子图间距 |
| A6 样式与字体 | [`plt.style.use(style)`](#pltstyleusestyle-切换整体风格) | 切换整体风格 |
| A6 样式与字体 | [`颜色、线型、标记速查`](#颜色线型标记速查-参数速记) | 参数速记 |
| A6 样式与字体 | [`plt.rcParams 中文字体`](#pltrcparams-中文字体-让中文和负号正常显示) | 让中文和负号正常显示 |
| A7 保存与显示 | [`fig.savefig(fname, dpi)`](#figsavefigfname-dpi-保存图片) | 保存图片 |
| A7 保存与显示 | [`plt.show()`](#pltshow-显示图形) | 显示图形 |
| A7 保存与显示 | [`plt.close(fig)、plt.clf()、plt.cla()`](#pltclosefigpltclfpltcla-关闭与清空) | 关闭与清空 |

---

## A1 画布与两种写法

### `plt.subplots(nrows, ncols)` 画布+轴（推荐起点）

**解析**　建好「画布 fig + 坐标轴 ax」两个对象，是画一张图的标准第一行。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| nrows | 1 | 子图行数 |
| ncols | 1 | 子图列数 |
| figsize | None | 画布宽高（英寸），不写默认 6.4×4.8 |
| sharex | False | 子图是否共享 X 轴（去重复刻度） |

返回：元组 `(Figure, Axes)`：整张画布 + 坐标轴。

**操作**

```python
import numpy as np

import matplotlib.pyplot as plt

x = np.linspace(0, 10, 100)

y = np.sin(x)

fig, ax = plt.subplots()

type(fig).__name__                            # 'Figure'

type(ax).__name__                             # 'Axes'

fig.get_size_inches().tolist()                # [6.4, 4.8]
```

> ⚠️ 一条线画图的标配第一行。`fig` 是整张画布、`ax` 是坐标轴（画图都画在 ax 上）。不传 `figsize` 默认 `(6.4, 4.8)` 英寸。一个 fig 可以装多个 ax（子图）。

### `plt.figure(figsize, dpi)` 只创建画布

**解析**　只创建一张空白画布（还没有坐标轴）；想自己定尺寸和清晰度时用它。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| num | None | 画布编号（一般不传） |
| figsize | None | 画布宽高（英寸） |
| dpi | None | 分辨率，不写默认 100（越大越清晰、文件越大） |

返回：`Figure` 画布对象。

**操作**

```python
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 6), dpi=100).get_size_inches().tolist()   # [8.0, 6.0]

plt.gcf().dpi                                                    # 100

plt.close("all")
```

> ⚠️ 画布 ≠ 坐标轴：`figure` 只有画布，没有坐标轴，要画图还得 `fig.add_subplot()`；日常直接用 `plt.subplots()` 更省事。`figsize` 是宽高（英寸），`dpi` 越大越清晰、文件越大。

### `pyplot 式 vs 面向对象式` 两种写法对比

**解析**　两种画图写法的对比：`plt.plot` 画到「当前」图（状态机，图一多容易乱），`ax.plot` 画到指定的轴（永远明确）。

返回：两种写法都返回 `list[Line2D]`（线对象列表）。

**操作**

```python
import numpy as np

import matplotlib.pyplot as plt

x = np.linspace(0, 10, 100)

plt.plot(x, np.sin(x))

len(plt.gca().lines)                          # 1

plt.close("all")

fig, ax = plt.subplots()

ax.plot(x, np.sin(x))

len(ax.lines)                                 # 1
```

> ⚠️ 推荐 OO 写法：pyplot 式靠「当前图/当前轴」的状态机，图一多就容易画错对象；`ax` 写法永远明确，画子图时只有这一种选择。`plt.gca()` = get current axes。

## A2 基础图形

### `ax.plot(x, y)` 折线图（最基础）

**解析**　画折线图：把一对对 (x, y) 点连成线，是最基础的画图方法。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| x | 必填 | 横坐标数组 |
| y | 必填 | 纵坐标数组 |
| color/c | None | 颜色（"red"、"blue"…） |
| linestyle/ls | None | 线型（- 实线、-- 虚线、: 点线、-. 点划线） |
| linewidth/lw | None | 线宽 |
| marker | None | 数据点标记（o 圆、s 方块、^ 三角） |
| label | None | 图例名字（配合 ax.legend） |

返回：`list[Line2D]`（习惯写法 `line, = ax.plot(...)` 解包出那一条线）。

**操作**

```python
import numpy as np

import matplotlib.pyplot as plt

x = np.linspace(0, 10, 100)

y = np.sin(x)

fig, ax = plt.subplots()

line, = ax.plot(x, y, color="red", linestyle="--", linewidth=2, label="sin")

type(line).__name__                           # 'Line2D'

line.get_color()                              # 'red'

line.get_linestyle()                          # '--'

line.get_linewidth()                          # 2.0

line.get_label()                              # 'sin'
```

> ⚠️ 返回的是**列表**，所以习惯写法是 `line, = ax.plot(...)`（解包一条线）。参数常用缩写：`c`=color、`ls`=linestyle、`lw`=linewidth、`ms`=markersize。

### `ax.scatter(x, y)` 散点图

**解析**　画散点图：每个数据点画一个圆点，不连线；还能按数值大小给点上色。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| x | 必填 | 横坐标数组 |
| y | 必填 | 纵坐标数组 |
| s | None | 点的大小（是**面积**不是直径） |
| c | None | 颜色（单色或数值数组） |
| marker | None | 点形状（不写默认圆点 o） |
| alpha | None | 透明度（0~1） |
| cmap | None | 色带（c 传数值数组时用，如 "viridis"） |

返回：`PathCollection`（想改样式用 `sc.set_*()`）。

**操作**

```python
import numpy as np

import matplotlib.pyplot as plt

x = np.linspace(0, 10, 100)

y = np.sin(x)

fig, ax = plt.subplots()

sc = ax.scatter(x, y, s=50, c="blue", alpha=0.6, label="数据点")

type(sc).__name__                             # 'PathCollection'

sc.get_sizes().tolist()                       # [50]

z = np.abs(y)

sc2 = ax.scatter(x, y, s=30, c=z, cmap="viridis", alpha=0.8)

len(ax.collections)                           # 2
```

> ⚠️ `s` 是点**面积**不是直径。`scatter` 返回 `PathCollection`（不是 Line2D），想改样式用 `sc.set_*()`。`c` 传数组 + `cmap` 就能按数值着色（比 `plot` 只能一种颜色灵活）。

### `ax.bar(x, height)、ax.barh(y, width)` 柱状图、水平柱状图

**解析**　画柱状图：每个类别一根柱子，柱高代表数值；barh 是横着的版本，类别名长时更好看。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| x | 必填 | 类别位置（字符串也行，自动编号） |
| height | 必填 | 每根柱子的高度 |
| width | 0.8 | 柱子宽度（占一个格子的比例） |
| color | None | 柱子颜色 |
| edgecolor | None | 柱子描边颜色 |

返回：`BarContainer`，每根柱子是一个 `Rectangle`，可以 `for b in bars` 逐个改。

**操作**

```python
import matplotlib.pyplot as plt

names = ["A", "B", "C"]

values = [3, 7, 5]

fig, ax = plt.subplots()

bars = ax.bar(names, values, color="skyblue", edgecolor="black", width=0.6)

type(bars).__name__                              # 'BarContainer'

[int(b.get_height()) for b in bars]              # [3, 7, 5]

[round(float(b.get_width()), 2) for b in bars]   # [0.6, 0.6, 0.6]

[t.get_text() for t in ax.bar_label(bars)]       # ['3', '7', '5']
```

> ⚠️ 每根柱子一个 `Rectangle`。**给柱子标数值用 `ax.bar_label(bars)`**（一行搞定，不用手写 text）。横向柱状图用 `barh`，类别名长的时候更好看。

### `ax.hist(x, bins)` 直方图（看分布）

**解析**　画直方图：把数据切成若干「箱子」，数每个箱子里有多少个值，看数据分布。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| x | 必填 | 数据数组 |
| bins | None | 箱子个数（不写默认 10） |
| density | False | 改成 True 变概率密度（整个面积=1） |
| alpha | None | 透明度 |
| edgecolor | None | 箱子描边颜色 |

返回：元组 `(counts, bins, patches)`：每个箱的计数、箱边界、图元。

**操作**

```python
import numpy as np

import matplotlib.pyplot as plt

data = np.random.default_rng(0).normal(0, 1, 1000)

fig, ax = plt.subplots()

counts, bins, patches = ax.hist(data, bins=30, color="green", alpha=0.7, edgecolor="black", density=True)

len(counts)                                           # 30

len(bins)                                             # 31

round(float(counts.sum() * (bins[1] - bins[0])), 6)   # 1.0

int(ax.hist(data, bins=30)[0].sum())                  # 1000
```

> ⚠️ `density=True` 才是概率密度。返回值是 `(每个箱的计数, 箱边界, 图元)`，`len(bins) == len(counts) + 1`。默认是**频数**；`density=True` 变成概率密度（整个面积为 1）——比较两个不同样本量的分布要用它。

### `ax.pie(x, labels, autopct)` 饼图

**解析**　画饼图：把一组数值画成按比例切块的圆饼，每块标上名字和百分比。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| x | 必填 | 各部分的数值（自动算百分比） |
| labels | None | 每块的名字 |
| autopct | None | 百分比文字格式（如 "%1.1f%%"） |
| explode | None | 把某几块往外推（强调） |
| startangle | 0 | 起始角度 |

返回：元组 `(wedges, texts, autotexts)`：饼块、标签、百分比文字。

**操作**

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

wedges, texts, autotexts = ax.pie([3, 7, 5], labels=["A", "B", "C"], autopct="%1.1f%%", startangle=90)

len(wedges)                                   # 3

[t.get_text() for t in texts]                 # ['A', 'B', 'C']

[t.get_text() for t in autotexts]             # ['20.0%', '46.7%', '33.3%']
```

> ⚠️ 类别多时别用饼图。`autopct` 里要写 `%%`（百分号转义），常用 `"%1.1f%%"`。**统计上不推荐饼图**（人眼比较角度不准），类别超过 4~5 个就换 `bar`。

### `ax.boxplot(data, tick_labels=)` 箱线图（看中位数与离群点）

**解析**　画箱线图：一张图同时看中位数、四分位范围和离群点（异常值）。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| x | 必填 | 数据（一组或 [组1, 组2, ...]） |
| tick_labels | None | 每组数据的名字 |
| patch_artist | None | 改成 True 给箱子填色 |

返回：`dict`：boxes（箱子）、medians（中位线）、whiskers（须）、fliers（离群点）…

**操作**

```python
import numpy as np

import matplotlib.pyplot as plt

data = np.random.default_rng(0).normal(0, 1, 200)

fig, ax = plt.subplots()

res = ax.boxplot([data, data * 2], tick_labels=["A", "B"])

sorted(res.keys())                                            # ['boxes', 'caps', 'fliers', 'means', 'medians', 'whiskers']

len(res['boxes'])                                             # 2

[round(float(m.get_ydata()[0]), 2) for m in res['medians']]   # [0.05, 0.1]
```

> ⚠️ **matplotlib 3.9 起 `labels=` 已移除**，必须写 `tick_labels=`（老代码会 `TypeError`）。箱子 = 四分位范围，红线 = 中位数，外面的点是离群值。

### `ax.imshow(data, cmap)+colorbar` 显示矩阵、图片

**解析**　把二维数组/矩阵画成彩色格子图（热力图），值越大颜色越深；要配 `fig.colorbar` 加颜色条才知道数值大小。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| X | 必填 | 二维数组或图片 |
| cmap | None | 色带（常用 "viridis"） |
| origin | None | 数据第 0 行在图的哪边（不写默认左上） |
| aspect | None | 格子宽高比（"auto" 取消正方形拉伸） |

返回：`AxesImage`；`fig.colorbar(im, ax=ax)` 返回 `Colorbar`。

**操作**

```python
import numpy as np

import matplotlib.pyplot as plt

fig, ax = plt.subplots()

m = np.arange(9).reshape(3, 3)

im = ax.imshow(m, cmap="viridis")

type(im).__name__                             # 'AxesImage'

im.get_array().tolist()                       # [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

cb = fig.colorbar(im, ax=ax)

type(cb).__name__                             # 'Colorbar'
```

> ⚠️ 默认 origin 在左上：`origin="lower"` 能让 y 轴从下往上（画坐标系时常用），`aspect="auto"` 可取消正方形拉伸。别忘 `fig.colorbar(im, ax=ax)`，否则数值范围看不懂。

## A3 坐标轴与标题

### `ax.set_title、set_xlabel、set_ylabel` 标题与轴标签

**解析**　给图加标题、X 轴名字、Y 轴名字——没有轴标签，读者不知道单位。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| label | 必填 | 标题/轴标签的文字内容 |
| fontsize | None | 字号 |

返回：`Text` 对象。

**操作**

```python
import numpy as np

import matplotlib.pyplot as plt

x = np.linspace(0, 10, 100)

y = np.sin(x)

fig, ax = plt.subplots()

ax.set_title("正弦曲线", fontsize=14)

ax.set_xlabel("时间")

ax.set_ylabel("幅值")

ax.get_title()                                # '正弦曲线'

(ax.get_xlabel(), ax.get_ylabel())            # ('时间', '幅值')
```

> ⚠️ 中文乱码看 A6 的字体设置。少了轴标签的图基本等于没信息（读者不知道单位）。中文显示成方框**不是 bug**，是没设中文字体（见 A6「rcParams 中文字体」）。

### `ax.set_xlim(left, right)` 设置坐标轴范围

**解析**　手动设定坐标轴显示范围；左右写反还能得到「反转轴」。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| left | None | X 轴左端（最小值） |
| right | None | X 轴右端（最大值）；set_ylim 对应 bottom、top |

返回：元组 `(left, right)`，两个浮点数。

**操作**

```python
import numpy as np

import matplotlib.pyplot as plt

x = np.linspace(0, 10, 100)

y = np.sin(x)

fig, ax = plt.subplots()

ax.set_xlim(0, 10)

ax.set_ylim(-1.5, 1.5)

[float(v) for v in ax.get_xlim()]             # [0.0, 10.0]

[float(v) for v in ax.get_ylim()]             # [-1.5, 1.5]

ax.set_xlim(10, 0)

[float(v) for v in ax.get_xlim()]             # [10.0, 0.0]
```

> ⚠️ 传反了就得到反转轴。顺序是 `(小, 大)`；**故意写反**（`set_xlim(10, 0)`）就能把轴翻转（画排名、时间倒序时有用）。也可以只传一个值或 `None` 自动缩放。

### `ax.set_xticks(ticks, labels)` 自定义刻度位置与文字

**解析**　自定义刻度画在哪些位置、刻度下面显示什么文字。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| ticks | 必填 | 刻度位置列表 |
| labels | None | 刻度下显示的文字（个数和 ticks 一致） |

返回：`None`（改的是当前轴的样子）。

**操作**

```python
import numpy as np

import matplotlib.pyplot as plt

x = np.linspace(0, 10, 100)

y = np.sin(x)

fig, ax = plt.subplots()

ax.set_xticks([0, 5, 10])

ax.get_xticks().tolist()                       # [0, 5, 10]

ax.set_xticks([0, 5, 10], labels=["零", "五", "十"])

[t.get_text() for t in ax.get_xticklabels()]   # ['零', '五', '十']

plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

ax.get_xticklabels()[0].get_rotation()         # 45.0
```

> ⚠️ 标签名长或重叠用 rotation。刻度文字重叠时用 `rotation=45`（配合 `ha="right"` 更整齐）。别单独调 `set_xticklabels`（会有警告），推荐直接给 `set_xticks` 传 `labels=`。

### `ax.set_xscale("log")` 对数坐标轴

**解析**　把坐标轴改成对数刻度——数据跨好几个数量级时才能看清。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| value | 必填 | 刻度类型："log" 对数、"linear" 线性；set_yscale 同理 |

返回：`None`（改的是当前轴）。

**操作**

```python
import numpy as np

import matplotlib.pyplot as plt

x = np.linspace(0.1, 100, 50)

fig, ax = plt.subplots()

ax.plot(x, x ** 2)

ax.set_xscale("log")

ax.set_yscale("log")

(ax.get_xscale(), ax.get_yscale())            # ('log', 'log')
```

> ⚠️ 数据有 0 或负数会出问题：跨好几个数量级的数据（收入、人口、频率）用对数轴才看得清变化率。**数据里有 0 或负数时会报错或丢点**，先确认取值范围。

### `ax.grid、axhline、axvline` 网格与参考线

**解析**　grid 画背景网格线；axhline/axvline 画一条水平/垂直参考线（阈值线、均值线）。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| visible | True | grid 是否显示网格（False 关闭） |
| y | 0 | axhline 参考线的 Y 位置 |
| x | 0 | axvline 参考线的 X 位置 |

返回：`grid` 返回 `None`；`axhline`/`axvline` 返回 `Line2D`。

**操作**

```python
import numpy as np

import matplotlib.pyplot as plt

x = np.linspace(0, 10, 100)

y = np.sin(x)

fig, ax = plt.subplots()

ax.grid(True, linestyle="--", alpha=0.5)

any(l.get_visible() for l in ax.get_xgridlines())   # True

ax.axhline(0, color="red", linestyle="--")

ax.axvline(5, color="gray", linestyle=":")

len(ax.lines)                                       # 2

ax.lines[0].get_ydata()                             # [0, 0]
```

> ⚠️ 参考线也算 `ax.lines`：`grid` 网格、`axhline`/`axvline` 画参考线（阈值线、均值线）；它们都画在**当前 ax** 上，子图要对每个 ax 单独调用。注意参考线也会出现在 `ax.lines` 里（所以这里是 2 条）。

### `ax.text(x, y, s)、ax.annotate(...)` 文字与带箭头标注

**解析**　text 在指定坐标放一段文字；annotate 放文字的同时画箭头指向数据点。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| x、y、s | 必填 | text 的坐标和文字内容 |
| xy | 必填 | annotate 箭头指向的数据点 |
| xytext | None | 文字放的位置（不写=xy） |
| arrowprops | None | 箭头样式，dict(arrowstyle="->") |

返回：`Text` / `Annotation` 对象。

**操作**

```python
import numpy as np

import matplotlib.pyplot as plt

x = np.linspace(0, 10, 100)

y = np.sin(x)

fig, ax = plt.subplots()

ax.text(5, 1, "峰值", fontsize=12)

ax.annotate("最高点", xy=(5, 1), xytext=(3, 1.2), arrowprops=dict(arrowstyle="->"))

[t.get_text() for t in ax.texts]              # ['峰值', '最高点']

ax.texts[1].xy                                # (5, 1)
```

> ⚠️ `xy` 是被指的点：`annotate` 的 `xy` 是**被指的点**、`xytext` 是**文字位置**、`arrowprops=dict(arrowstyle="->")` 画箭头。坐标是数据坐标（跟着轴缩放走）。

## A4 图例与辅助元素

### `ax.legend(loc, frameon)` 图例

**解析**　给每条线画图例框，标出「哪条线叫什么」；前提是画线时给了 `label=`。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| loc | None | 图例放哪（不写默认 "best" 自动找空位） |
| frameon | True | 是否画边框（False 去掉） |
| ncol | 1 | 图例排成几列 |

返回：`Legend` 图例对象。

**操作**

```python
import numpy as np

import matplotlib.pyplot as plt

x = np.linspace(0, 10, 100)

y = np.sin(x)

fig, ax = plt.subplots()

ax.plot(x, y, label="sin")

ax.plot(x, np.cos(x), label="cos")

ax.legend(loc="upper right")

[t.get_text() for t in ax.get_legend().get_texts()]   # ['sin', 'cos']

ax.get_legend().get_frame_on()                        # True
```

> ⚠️ 要先有 `label=`：绘图时没写 `label=` 就会出现 `_child0` 这种占位名（或没有图例项）。`loc` 常用 `best`/`upper right`/`lower left`；`frameon=False` 去边框、`ncol=2` 排两列。

### `ax.twinx()` 双 Y 轴

**解析**　复制一个叠在同一位置、共享 X 轴的新坐标轴——用来画量纲不同的两组数据（如温度+降雨量）。

返回：新的 `Axes`（与原来的共享 X 轴）。

**操作**

```python
import numpy as np

import matplotlib.pyplot as plt

x = np.linspace(0, 10, 100)

y = np.sin(x)

fig, ax = plt.subplots()

ax.plot(x, y, color="blue")

ax2 = ax.twinx()

ax2.plot(x, 10 * y, color="red")

(len(ax.lines), len(ax2.lines))               # (1, 1)

ax2 is not ax                                 # True
```

> ⚠️ 两轴量纲不同时用：两个 Y 轴共享同一条 X 轴，适合「温度 + 降雨量」这类量纲不同的数据。**务必分别标注**（给每条线 `label` + 两个轴各自 `set_ylabel` 并上色），否则读者不知道哪条对哪轴。

### `ax.fill_between(x, y1, y2)` 区域填充

**解析**　把两条曲线之间（或曲线和 0 之间）的区域填上颜色，画置信区间、误差带。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| x | 必填 | 横坐标数组 |
| y1 | 必填 | 区域上边界 |
| y2 | 0 | 区域下边界（不写填到 0） |
| alpha | None | 透明度（一定给个值） |
| color | None | 填充颜色 |

返回：`FillBetweenPolyCollection`。

**操作**

```python
import numpy as np

import matplotlib.pyplot as plt

x = np.linspace(0, 10, 100)

y = np.sin(x)

fig, ax = plt.subplots()

ax.plot(x, y, color="black", linewidth=1)

ax.fill_between(x, 0, y, alpha=0.3, color="gray")

type(ax.collections[0]).__name__              # 'FillBetweenPolyCollection'

len(ax.collections)                           # 1
```

> ⚠️ 一定给 `alpha`：填两条曲线之间（或到 0）的区域，画置信区间、误差带、面积图用它。`alpha` 一定要给（半透明），否则会把线和网格盖住。

### `ax.errorbar(x, y, yerr)` 误差棒

**解析**　画带误差棒的线/点：每个数据点带一条「不确定范围」竖线，实验数据标配。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| x、y | 必填 | 数据点的坐标 |
| yerr | None | Y 方向误差（标量或数组） |
| xerr | None | X 方向误差 |
| fmt | "" | 数据点样式（"o"=只画点不连线） |
| capsize | None | 误差棒两端横帽长度 |

返回：`ErrorbarContainer`（真正的数据线在 `eb.lines[0]`）。

**操作**

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

eb = ax.errorbar([1, 2, 3], [2, 3, 5], yerr=[0.2, 0.3, 0.4], fmt="o", capsize=3)

type(eb).__name__                                       # 'ErrorbarContainer'

len(eb.lines)                                           # 3

[round(float(v), 2) for v in eb.lines[0].get_ydata()]   # [2.0, 3.0, 5.0]
```

> ⚠️ 实验数据标配：`yerr` 给标准差/标准误（可以是标量或数组）；`fmt="o"` 表示只画点不连线。返回值是容器对象，取真正的数据线用 `eb.lines[0]`。

## A5 子图与布局

### `plt.subplot(nrows, ncols, index)` pyplot 式子图

**解析**　pyplot 式子图：反复调用，把画布切成 nrows×ncols 的格子，每次画一格。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| nrows | 必填 | 子图行数 |
| ncols | 必填 | 子图列数 |
| index | 必填 | 这次画第几格（**从 1 开始**） |

返回：`Axes`（当前要画的轴）。

**操作**

```python
import numpy as np

import matplotlib.pyplot as plt

x = np.linspace(0, 10, 100)

plt.subplot(2, 2, 1)

plt.plot(x, np.sin(x))

plt.subplot(2, 2, 2)

plt.plot(x, np.cos(x))

len(plt.gcf().axes)                           # 2

plt.close("all")
```

> ⚠️ index 从 1 开始：**从 1 开始**的编号（1~4），和 `axes.ravel()` 的 0 起始不一样，容易混。写法靠状态机，多个子图建议直接用 `plt.subplots()`。

### `fig, axes=plt.subplots(2, 2)` 面向对象式子图（推荐）

**解析**　一次性建好 nrows×ncols 个子图，返回的 axes 是数组，按坐标逐个画——画子图的推荐写法。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| nrows | 必填 | 子图行数 |
| ncols | 必填 | 子图列数 |
| figsize | None | 画布宽高（英寸） |
| sharex | False | 各子图共享 X 轴 |
| sharey | False | 各子图共享 Y 轴 |

返回：元组 `(Figure, ndarray)`，数组里每个元素是一个 `Axes`。

**操作**

```python
import numpy as np

import matplotlib.pyplot as plt

x = np.linspace(0, 10, 100)

y = np.sin(x)

fig, axes = plt.subplots(2, 2, figsize=(10, 8), sharex=True)

axes.shape                                                      # (2, 2)

type(axes[0, 0]).__name__                                       # 'Axes'

axes[0, 0].plot(x, y)

axes[0, 1].scatter(x, y, s=5)

axes[1, 0].bar(["A", "B"], [3, 7])

len(axes[0, 0].lines)                                           # 1

len(axes[0, 1].collections)                                     # 1

axes[0, 0].get_shared_x_axes().joined(axes[0, 0], axes[1, 1])   # True
```

> ⚠️ 1×N 时 axes 是**一维**：`axes` 是个 **ndarray**——2×2 用 `axes[0, 1]`，但 **1×3 或 3×1 会得到一维数组**（要写 `axes[1]`），所以常用 `for a in axes.ravel():` 统一遍历。`sharex=True` 让子图共享 X 轴（去掉重复标签）。

### `fig.tight_layout()、plt.subplots_adjust()` 子图间距

**解析**　修子图间距：标签被压住先用 tight_layout 自动算，要精确控制用 subplots_adjust 手调。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| wspace | None | 子图间水平间距（subplots_adjust） |
| hspace | None | 子图间垂直间距（subplots_adjust） |

返回：`None`。

**操作**

```python
import numpy as np

import matplotlib.pyplot as plt

x = np.linspace(0, 10, 100)

y = np.sin(x)

fig, axes = plt.subplots(1, 2, figsize=(8, 3))

axes[0].set_title("很长的标题需要空间")

axes[0].set_xlabel("时间")

fig.tight_layout()

type(fig.tight_layout()).__name__             # 'NoneType'

plt.subplots_adjust(wspace=0.4, hspace=0.4)
```

> ⚠️ 画完再调：标签被裁掉/压住时先 `tight_layout()`（自动算间距）；要精确控制用 `subplots_adjust(wspace=, hspace=)`。**两者别混用在同一个 fig 上**，后调的会覆盖前一个的效果。最好在画完标题、轴标签之后再调。

## A6 样式与字体

### `plt.style.use(style)` 切换整体风格

**解析**　一键切换整个绘图风格（配色、背景、网格），全局生效。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| style | 必填 | 样式名，如 "ggplot"、"seaborn-v0_8"、"dark_background" |

返回：`None`（改的是全局配置）。

**操作**

```python
import matplotlib.pyplot as plt

len(plt.style.available)                      # 28

plt.style.available[:3]                       # ['Solarize_Light2', 'bmh', 'classic']

plt.style.use("ggplot")

plt.rcParams["axes.grid"]                     # True

plt.style.use("default")

plt.rcParams["axes.grid"]                     # False
```

> ⚠️ 全局生效：样式是**全局**的，影响后面所有图；只想局部生效用 `with plt.style.context("ggplot"):`。常用：`"ggplot"`、`"seaborn-v0_8"`、`"dark_background"`、`"fivethirtyeight"`。

### `颜色、线型、标记速查` 参数速记

**解析**　颜色、线型、标记三类样式参数的可选值速查；缩写和全名都能用。

返回：无（它们只是传给 `ax.plot` 的样式参数，plot 返回 `Line2D`）。

**操作**

```python
import numpy as np

import matplotlib.pyplot as plt

x = np.linspace(0, 10, 100)

y = np.sin(x)

fig, ax = plt.subplots()

line, = ax.plot(x, y, color="tomato", linestyle="--", marker="o", markersize=4)

(line.get_color(), line.get_marker(), line.get_markersize())                      # ('tomato', 'o', 4.0)

[plt.plot([0], [0], c=c)[0].get_color() for c in ["r", "g", "b", "k"]]            # ['r', 'g', 'b', 'k']

[plt.plot([0], [0], ls=ls)[0].get_linestyle() for ls in ["-", "--", ":", "-."]]   # ['-', '--', ':', '-.']
```

> ⚠️ 缩写和全名都能用：颜色 `r g b k w c m y`、色名 `"tomato"`、十六进制 `"#FF0000"` 都行。线型：`-` 实线、`--` 虚线、`:` 点线、`-.` 点划线。标记：`o` 圆、`s` 方块、`^` 三角、`*` 星、`x` 叉。

### `plt.rcParams 中文字体` 让中文和负号正常显示

**解析**　两句配置让中文和负号正常显示（否则中文变方框、负号也变方框）。

返回：`None`（改的是全局配置）。

**操作**

```python
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Arial Unicode MS", "PingFang SC"]

plt.rcParams["axes.unicode_minus"] = False

"PingFang SC" in plt.rcParams["font.sans-serif"]   # True

plt.rcParams["axes.unicode_minus"]                 # False
```

> ⚠️ 两句都要设：**两句都要设**——字体解决中文方块，`unicode_minus=False` 解决负号变方框。放在画图**最前面**（rcParams 是全局配置）。macOS 常用 `"PingFang SC"` / `"Arial Unicode MS"`，Windows 用 `"SimHei"`。

## A7 保存与显示

### `fig.savefig(fname, dpi)` 保存图片

**解析**　把当前画布存成图片文件；扩展名决定格式（png 位图、pdf/svg 矢量）。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| fname | 必填 | 文件名（扩展名决定格式） |
| dpi | None | 分辨率（不写用画布默认 100） |
| bbox_inches | None | 传 "tight" 裁掉多余白边 |

返回：`None`（写文件）。

**操作**

```python
import os

import matplotlib.pyplot as plt

fig, ax = plt.subplots()

ax.plot([1, 2, 3], [2, 1, 4])

fig.savefig("plot.png", dpi=150, bbox_inches="tight")

fig.savefig("plot.pdf")

os.path.getsize("plot.png") > 0               # True

os.path.exists("plot.pdf")                    # True
```

> ⚠️ 扩展名决定格式：`png`（位图、报告用）、`pdf`/`svg`（矢量、论文用）。`bbox_inches="tight"` 裁掉多余白边。**要在 `plt.show()` 之前保存**（有的后端 show 之后会清空画布），文件名尽量用英文。

### `plt.show()` 显示图形

**解析**　把画好的图显示出来（弹窗）；交互窗口会阻塞脚本，直到你关掉窗口。

返回：`None`。

**操作**

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

ax.plot([1, 2], [1, 2])

plt.show()
# 交互后端：弹出窗口并阻塞，关掉窗口才继续；
# Agg 等无界面后端：什么都不做，只打印一句警告
```

> ⚠️ 脚本里会阻塞：脚本里 `show()` 会**阻塞**在窗口上；Jupyter/Notebook 里不用写 `show()`，最后一行写 `fig` 或 `ax` 就会显示。批量画图脚本建议不 show，只 `savefig`。

### `plt.close(fig)、plt.clf()、plt.cla()` 关闭与清空

**解析**　三个清理动作：close 关掉整张图（释放内存）、clf 清空画布内容、cla 清空当前坐标轴。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| fig | None | close 要关的图："all" 全部、None 当前图、或 fig 对象 |

返回：`None`。

**操作**

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

plt.fignum_exists(fig.number)                 # True

plt.close(fig)

plt.fignum_exists(fig.number)                 # False

plt.close("all")

plt.get_fignums()                             # []
```

> ⚠️ 循环画图必须关：`close` 关掉整个图（释放内存）、`clf` 清空画布但保留窗口、`cla` 只清空当前坐标轴。循环里画很多图不关，会出现 `More than 20 figures have been opened` 警告并吃内存。

## 学习建议

1. **用面向对象写法**：`fig, ax = plt.subplots()` 再 `ax.plot(...)`。比 `plt.plot` 清晰，画子图时更是必需。
2. **一张完整的图 = 4 步**：画数据 → 标题轴标签 → 图例 → 保存（`fig.savefig`）。
   ```python
   import matplotlib.pyplot as plt
   x, y = [1, 2, 3], [1, 4, 9]
   fig, ax = plt.subplots(figsize=(8, 5))
   ax.plot(x, y, label="y")
   ax.set_title("标题"); ax.set_xlabel("X"); ax.set_ylabel("Y")
   ax.legend()
   fig.tight_layout()
   fig.savefig("out.png", dpi=150, bbox_inches="tight")
   ```
3. **中文乱码两步走**：`plt.rcParams["font.sans-serif"] = [...]` + `plt.rcParams["axes.unicode_minus"] = False`（放在画图最前面）。
4. **记得关图**：循环里画很多图要 `plt.close(fig)`，否则内存堆积（会出现 "More than 20 figures" 警告）。
5. **统计图优先看 Seaborn**：箱线图、分布图、带置信区间的折线，Seaborn 几行就能画，风格也更好。
