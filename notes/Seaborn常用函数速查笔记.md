# Seaborn 常用函数速查笔记

> 收集范围：统计可视化里最常用的 Seaborn 操作，覆盖主题、关系图、分布图、分类图、回归图、矩阵图与网格。
> 每条都是「**解析 ｜ 操作 ｜ 提醒**」三段 + 可直接运行的示例。绘图语句本身没有「输出」，所以示例后面跟了可检查的取值（`type(...).__name__`、`g.axes.shape`），`#` 后是**真实运行结果**。
> 约定：`import seaborn as sns`；Seaborn 基于 Matplotlib，可混用（中文乱码同样要设 `plt.rcParams`）。
> 📌 示例里的 `df` 是一张**手工小表**（列：`day` `sex` `bill` `tip` `size`，共 8 行），所以示例**离线可跑**；真实数据可以换成 `sns.load_dataset("tips")`（见 A1）。
> ⚠️ 版本：本笔记在 **seaborn 0.13.2** 上逐条跑通，过时参数标在条目里（`lineplot(ci=)`、`barplot(estimator=)` 已不推荐，改用 `errorbar=`）。

## 怎么用这份文件

1. **先看下面的《索引 · 速查表》**：一行一个函数，点「用法」列直接跳到正文对应位置；忘了名字就按分类扫一遍。
2. **正文每条统一格式**：
   - 标题：`名字(参数)` + 一句话作用
   - **解析**：先一句话说它干什么，再用表格逐个解释参数（参数名、默认值、作用），最后写返回什么
   - **操作**：能直接复制运行的示例，`#` 后是真实输出
   - `> ⚠️ 提醒`：要点和易错点（没有就不写）
3. **先分清图级 / 轴级**：图级函数（`relplot` `displot` `catplot` `lmplot` `jointplot`）自动建子图、支持 `row`/`col` 分面，返回 `FacetGrid` / `JointGrid`；轴级函数（`scatterplot` `histplot` `barplot` …）画在指定轴上，方便塞进 `plt.subplots()` 里组合。
4. **顺序**：A1 主题与数据 → A2 关系图 → A3 分布图 → A4 分类图 → A5 回归图 → A6 矩阵图 → A7 网格（按日常使用频率）。
5. 想按顺序系统复习，见文末《学习建议》。

---

## 索引 · 速查表

| 分类 | 用法（点击跳转） | 一句话作用 |
|------|------------------|-----------|
| A1 主题、调色板与数据 | [`sns.set_theme(style, palette, context)`](#snsset_themestyle-palette-context-一步设定全局风格) | 一步设定全局风格 |
| A1 主题、调色板与数据 | [`sns.set_style、sns.set_context、sns.set_palette`](#snsset_stylesnsset_contextsnsset_palette-只改一项细调) | 只改一项（细调） |
| A1 主题、调色板与数据 | [`sns.color_palette(name, n_colors)`](#snscolor_palettename-n_colors-查看生成调色板) | 查看、生成调色板 |
| A1 主题、调色板与数据 | [`sns.load_dataset(name)`](#snsload_datasetname-加载内置示例数据) | 加载内置示例数据 |
| A2 关系图 | [`sns.scatterplot(data, x, y, hue, size)`](#snsscatterplotdata-x-y-hue-size-散点图最常用) | 散点图（最常用） |
| A2 关系图 | [`sns.lineplot(data, x, y, hue)`](#snslineplotdata-x-y-hue-折线图自动画均值置信区间) | 折线图（自动画均值+置信区间） |
| A2 关系图 | [`sns.relplot(data, x, y, kind, col, row)`](#snsrelplotdata-x-y-kind-col-row-图级关系图可分面) | 图级关系图（可分面） |
| A3 分布图 | [`sns.histplot(data, x, bins, kde, hue)`](#snshistplotdata-x-bins-kde-hue-直方图) | 直方图 |
| A3 分布图 | [`sns.kdeplot(data, x, y, fill, hue)`](#snskdeplotdata-x-y-fill-hue-核密度曲线二维密度) | 核密度曲线、二维密度 |
| A3 分布图 | [`sns.ecdfplot、sns.rugplot`](#snsecdfplotsnsrugplot-累积分布地毯图) | 累积分布、地毯图 |
| A3 分布图 | [`sns.boxplot、sns.violinplot`](#snsboxplotsnsviolinplot-箱线图小提琴图) | 箱线图、小提琴图 |
| A3 分布图 | [`sns.displot(data, x, kind, col)`](#snsdisplotdata-x-kind-col-图级分布图可分面) | 图级分布图（可分面） |
| A4 分类图 | [`sns.barplot(data, x, y, hue)`](#snsbarplotdata-x-y-hue-柱状图默认画均值误差棒) | 柱状图（默认画均值+误差棒） |
| A4 分类图 | [`sns.countplot(data, x, hue)`](#snscountplotdata-x-hue-计数图不用给-y) | 计数图（不用给 y） |
| A4 分类图 | [`sns.pointplot(data, x, y, hue)`](#snspointplotdata-x-y-hue-点线图趋势) | 点线图（趋势） |
| A4 分类图 | [`sns.stripplot、sns.swarmplot`](#snsstripplotsnsswarmplot-散点条带蜂群图) | 散点条带、蜂群图 |
| A4 分类图 | [`sns.boxenplot(data, x, y)`](#snsboxenplotdata-x-y-增强箱线图大数据) | 增强箱线图（大数据） |
| A4 分类图 | [`sns.catplot(data, x, y, kind, col)`](#snscatplotdata-x-y-kind-col-图级分类图可分面) | 图级分类图（可分面） |
| A5 回归图 | [`sns.regplot(data, x, y, ci)`](#snsregplotdata-x-y-ci-散点回归直线) | 散点+回归直线 |
| A5 回归图 | [`sns.lmplot(data, x, y, hue, col)`](#snslmplotdata-x-y-hue-col-图级回归图分组拟合) | 图级回归图（分组拟合） |
| A5 回归图 | [`sns.residplot(data, x, y)`](#snsresidplotdata-x-y-残差图检查拟合是否合理) | 残差图（检查拟合是否合理） |
| A6 矩阵图 | [`sns.heatmap(data, annot, cmap)`](#snsheatmapdata-annot-cmap-热力图相关性矩阵标配) | 热力图（相关性矩阵标配） |
| A6 矩阵图 | [`sns.clustermap(data, annot)`](#snsclustermapdata-annot-聚类热力图) | 聚类热力图 |
| A6 矩阵图 | [`sns.pairplot(data, hue)`](#snspairplotdata-hue-成对关系图多变量速览) | 成对关系图（多变量速览） |
| A7 网格类 | [`sns.FacetGrid(data, col, hue)+.map()`](#snsfacetgriddata-col-huemap-自定义分面网格) | 自定义分面网格 |
| A7 网格类 | [`sns.PairGrid(data, hue)+map_diag、map_offdiag`](#snspairgriddata-huemap_diagmap_offdiag-自定义成对网格) | 自定义成对网格 |
| A7 网格类 | [`sns.jointplot(data, x, y, kind)`](#snsjointplotdata-x-y-kind-联合分布图主图边缘分布) | 联合分布图（主图+边缘分布） |

---

## A1 主题、调色板与数据

### `sns.set_theme(style, palette, context)` 一步设定全局风格

**解析**　一次调用把整张统计图的外观（背景、配色、字号）设成统一风格，之后画的图都跟着变。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| context | 'notebook' | 字号缩放：可选 paper、notebook、talk、poster（演示用 talk） |
| style | 'darkgrid' | 背景网格风格：darkgrid、whitegrid、dark、white、ticks |
| palette | 'deep' | 配色方案名（deep、muted、bright、pastel、dark、colorblind） |
| font_scale | 1 | 整体字号缩放倍数 |
| rc | None | 额外传入 rcParams 字典微调 |

返回：`None`（只改全局设置，不返回任何对象）

**操作**

```python
import seaborn as sns

import matplotlib.pyplot as plt

len(sns.color_palette())                    # 10

sns.set_theme(style="darkgrid", palette="muted")

plt.rcParams["axes.grid"]                   # True

plt.rcParams["axes.facecolor"]              # '#EAEAF2'

sns.set_theme()
```

> ⚠️ 全局生效。`style` 管背景网格：`darkgrid`(默认) `whitegrid` `dark` `white` `ticks`；`palette` 管配色（`deep` `muted` `bright` `pastel` `dark` `colorblind`）；`context` 管字号缩放：`paper` `notebook` `talk` `poster`（做演示用 `talk`）。

### `sns.set_style、sns.set_context、sns.set_palette` 只改一项（细调）

**解析**　set_theme 的拆件：只换背景、只换字号、只换配色，一次只动一项，其余保持不变。

返回：`None`（都只改全局设置）

**操作**

```python
import seaborn as sns

import matplotlib.pyplot as plt

sns.set_style("whitegrid")

plt.rcParams["axes.grid"]                   # True

plt.rcParams["grid.linestyle"]              # '-'

sns.set_context("talk")

plt.rcParams["font.size"]                   # 18.0

sns.set_palette("colorblind")

len(sns.color_palette())                    # 10

sns.set_theme()
```

> ⚠️ set_theme 的拆件。`set_style` 只换背景、`set_context` 只换字号、`set_palette` 只换颜色；不想全局生效就用 `with sns.axes_style("whitegrid"):`（局部生效）。

### `sns.color_palette(name, n_colors)` 查看、生成调色板

**解析**　生成一个颜色列表：用来查看某种配色长什么样、挑几种颜色，或直接喂给 matplotlib 用。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| palette | None | 调色板名（deep 等）、色图名（viridis 等）或「blend:#7AB,#F00」自定义 |
| n_colors | None | 取几种颜色；不写返回该调色板全部颜色 |
| desat | None | 去饱和度比例（0~1） |
| as_cmap | False | True 时返回连续色图（colormap）而不是颜色列表 |

返回：颜色列表 `list[tuple]`（RGB 三元组，可直接喂给 matplotlib）

**操作**

```python
import seaborn as sns

len(sns.color_palette("muted"))                        # 10

sns.color_palette("deep", 3)                           # [(0.2980392156862745, 0.4470588235294118, 0.6901960784313725), (0.8666666666666667, 0.5176470588235295, 0.3215686274509804), (0.3333333333333333, 0.6588235294117647, 0.40784313725490196)]

[round(c, 3) for c in sns.color_palette("muted")[0]]   # [0.282, 0.471, 0.816]

sns.color_palette("blend:#7AB,#F00", 2)                # [(0.4666666666666667, 0.6666666666666666, 0.7333333333333333), (1.0, 0.0, 0.0)]
```

> ⚠️ 离散调色板名（`deep` `muted` `bright` `pastel` `dark` `colorblind`）适合分类变量；连续色图名（`viridis` `rocket` `flare`）适合数值渐变；`sns.color_palette("blend:#7AB,#F00")` 能自定义。可直接喂给 matplotlib。

### `sns.load_dataset(name)` 加载内置示例数据

**解析**　下载（或读取缓存）Seaborn 自带的示例数据集，返回 DataFrame——练手时不用自己造数据。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| name | 必填 | 数据集名：tips、iris、titanic、penguins、diamonds、mpg、fmri、flights |
| cache | True | 下载后缓存到本地，之后离线可用 |
| data_home | None | 缓存目录（默认 ~/seaborn-data） |

返回：`DataFrame`（`get_dataset_names()` 返回全部数据集名的 `list`）

**操作**

```python
import seaborn as sns

df = sns.load_dataset("tips")

df.shape                                    # (244, 7)

df.columns.tolist()                         # ['total_bill', 'tip', 'sex', 'smoker', 'day', 'time', 'size']

df["day"].unique().tolist()                 # ['Sun', 'Sat', 'Thur', 'Fri']

len(sns.get_dataset_names())                # 22
```

> ⚠️ **首次需要联网**下载并缓存到 `~/seaborn-data`，之后离线可用；下载失败就换成自己的 `pd.read_csv(...)`。

## A2 关系图

### `sns.scatterplot(data, x, y, hue, size)` 散点图（最常用）

**解析**　画散点图：每个数据点一个小点，看两个数值变量之间的关系；hue、size、style 还能再各编码一个维度。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| data | None | 数据表（DataFrame） |
| x | None | 横轴列名（数值） |
| y | None | 纵轴列名（数值） |
| hue | None | 按这一列的分类值着色 |
| size | None | 按这一列的数值调点大小 |
| style | None | 按这一列的分类值换标记形状 |

返回：`Axes`（轴级函数，画在当前轴上）

**操作**

```python
import seaborn as sns

import pandas as pd

import matplotlib.pyplot as plt

df = pd.DataFrame({"day": ["Thur", "Fri", "Sat", "Sun"] * 4,
                   "sex": ["Male"] * 8 + ["Female"] * 8,
                   "bill": [17.0, 20.5, 25.0, 30.2, 12.5, 40.1, 22.3, 18.8,
                            35.0, 27.5, 19.0, 22.4, 48.0, 15.5, 29.9, 33.2],
                   "tip": [2.0, 3.5, 4.0, 5.1, 1.5, 6.0, 3.2, 2.8,
                           5.0, 4.2, 2.4, 3.0, 7.5, 2.2, 4.4, 5.2],
                   "size": [2, 3, 4, 2, 2, 5, 3, 2, 4, 3, 2, 3, 6, 2, 4, 5]})

ax = sns.scatterplot(data=df, x="bill", y="tip", hue="sex")

type(ax).__name__                           # 'Axes'

len(ax.collections)                         # 1

ax.get_xlabel()                             # 'bill'

ax2 = sns.scatterplot(data=df, x="bill", y="tip", hue="sex", size="size", style="sex")

len(ax2.collections)                        # 2
```

> ⚠️ `hue=` 按分类着色、`size=` 按数值调点大小、`style=` 换标记形状 —— 一张图最多用它们编码 3 个额外维度（**别再多**，否则读不懂）。传 `ax=` 就能画到指定子图上。

### `sns.lineplot(data, x, y, hue)` 折线图（自动画均值+置信区间）

**解析**　画折线图；同一个 x 有多条数据时自动算均值并画出 95% 置信区间阴影，比 plt.plot 直接连线省事得多。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| data | None | 数据表（DataFrame） |
| x | None | 横轴列名 |
| y | None | 纵轴列名 |
| hue | None | 按这一列的分类值分组（每组各画一条线） |
| errorbar | ('ci', 95) | 置信区间设定；None 不画阴影 |

返回：`Axes`

**操作**

```python
import seaborn as sns

import pandas as pd

import matplotlib.pyplot as plt

df = pd.DataFrame({"day": ["Thur", "Fri", "Sat", "Sun"] * 4,
                   "sex": ["Male"] * 8 + ["Female"] * 8,
                   "bill": [17.0, 20.5, 25.0, 30.2, 12.5, 40.1, 22.3, 18.8,
                            35.0, 27.5, 19.0, 22.4, 48.0, 15.5, 29.9, 33.2],
                   "tip": [2.0, 3.5, 4.0, 5.1, 1.5, 6.0, 3.2, 2.8,
                           5.0, 4.2, 2.4, 3.0, 7.5, 2.2, 4.4, 5.2],
                   "size": [2, 3, 4, 2, 2, 5, 3, 2, 4, 3, 2, 3, 6, 2, 4, 5]})

ax = sns.lineplot(data=df, x="day", y="bill", hue="sex")

type(ax).__name__                           # 'Axes'

len(ax.lines)                               # 4

ax2 = sns.lineplot(data=df, x="day", y="bill", errorbar=None)

len(ax2.lines)                              # 5
```

> ⚠️ **同一个 x 有多条数据时，Seaborn 会自动画均值 + 置信区间阴影**（这和 `plt.plot` 直接连线完全不同）。不要阴影就传 `errorbar=None`；老教程里的 `ci=None` 还能用但**已过时**。

### `sns.relplot(data, x, y, kind, col, row)` 图级关系图（可分面）

**解析**　关系图的「图级」版本：自动建整张图，还能按 col、row 分面成多个子图，kind 切换散点或折线。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| data | None | 数据表（DataFrame） |
| x | None | 横轴列名 |
| y | None | 纵轴列名 |
| kind | 'scatter' | 图种：scatter（散点）或 line（折线） |
| col | None | 按这一列分面（一列一个子图） |
| row | None | 按这一列分面（一行一个子图） |

返回：`FacetGrid`（图级函数；子图在 `g.axes` 里）

**操作**

```python
import seaborn as sns

import pandas as pd

import matplotlib.pyplot as plt

df = pd.DataFrame({"day": ["Thur", "Fri", "Sat", "Sun"] * 4,
                   "sex": ["Male"] * 8 + ["Female"] * 8,
                   "bill": [17.0, 20.5, 25.0, 30.2, 12.5, 40.1, 22.3, 18.8,
                            35.0, 27.5, 19.0, 22.4, 48.0, 15.5, 29.9, 33.2],
                   "tip": [2.0, 3.5, 4.0, 5.1, 1.5, 6.0, 3.2, 2.8,
                           5.0, 4.2, 2.4, 3.0, 7.5, 2.2, 4.4, 5.2],
                   "size": [2, 3, 4, 2, 2, 5, 3, 2, 4, 3, 2, 3, 6, 2, 4, 5]})

g = sns.relplot(data=df, x="bill", y="tip", hue="sex", col="day")

type(g).__name__                            # 'FacetGrid'

g.axes.shape                                # (1, 4)

len(g.axes.flat)                            # 4

g2 = sns.relplot(data=df, x="day", y="bill", kind="line")

type(g2).__name__                           # 'FacetGrid'
```

> ⚠️ `col=`/`row=` 按分类**分面**成多个子图，`kind="line"` 切换成折线。**图级函数返回 `FacetGrid`**（不是 Axes），子图在 `g.axes` 里。

## A3 分布图

### `sns.histplot(data, x, bins, kde, hue)` 直方图

**解析**　画直方图：把数值按区间分组数个数，看数据的分布形态；kde=True 再叠一条密度曲线。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| data | None | 数据表（DataFrame） |
| x | None | 要统计的数值列 |
| bins | 'auto' | 箱数（也可传边界列表） |
| kde | False | True 时叠加一条核密度曲线 |
| hue | None | 按这一列分组（分组时纵轴会自动变成 count 叠加） |
| stat | 'count' | 纵轴含义：count（个数）、density（密度）等 |

返回：`Axes`

**操作**

```python
import seaborn as sns

import pandas as pd

import matplotlib.pyplot as plt

df = pd.DataFrame({"day": ["Thur", "Fri", "Sat", "Sun"] * 4,
                   "sex": ["Male"] * 8 + ["Female"] * 8,
                   "bill": [17.0, 20.5, 25.0, 30.2, 12.5, 40.1, 22.3, 18.8,
                            35.0, 27.5, 19.0, 22.4, 48.0, 15.5, 29.9, 33.2],
                   "tip": [2.0, 3.5, 4.0, 5.1, 1.5, 6.0, 3.2, 2.8,
                           5.0, 4.2, 2.4, 3.0, 7.5, 2.2, 4.4, 5.2],
                   "size": [2, 3, 4, 2, 2, 5, 3, 2, 4, 3, 2, 3, 6, 2, 4, 5]})

ax = sns.histplot(data=df, x="bill", bins=5)

type(ax).__name__                           # 'Axes'

len(ax.patches)                             # 5

ax2 = sns.histplot(data=df, x="bill", bins=5, kde=True)

len(ax2.lines)                              # 1
```

> ⚠️ `bins` 是箱数（也可传边界列表）；`kde=True` 叠一条核密度曲线（`ax.lines` 里会多出来）。`stat="density"` 换纵轴含义，`hue=` 分组（**分组时纵轴会自动变成 count 叠加**）。

### `sns.kdeplot(data, x, y, fill, hue)` 核密度曲线、二维密度

**解析**　画核密度估计曲线：一条光滑曲线近似数据的分布形状；同时给 x 和 y 就变成二维密度等高线。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| data | None | 数据表（DataFrame） |
| x | None | 横轴数值列 |
| y | None | 纵轴数值列（给了就和 x 一起画二维密度） |
| fill | None | True 时填充曲线下面积 |
| hue | None | 按这一列分组（各画一条曲线） |

返回：`Axes`

**操作**

```python
import seaborn as sns

import pandas as pd

import matplotlib.pyplot as plt

df = pd.DataFrame({"day": ["Thur", "Fri", "Sat", "Sun"] * 4,
                   "sex": ["Male"] * 8 + ["Female"] * 8,
                   "bill": [17.0, 20.5, 25.0, 30.2, 12.5, 40.1, 22.3, 18.8,
                            35.0, 27.5, 19.0, 22.4, 48.0, 15.5, 29.9, 33.2],
                   "tip": [2.0, 3.5, 4.0, 5.1, 1.5, 6.0, 3.2, 2.8,
                           5.0, 4.2, 2.4, 3.0, 7.5, 2.2, 4.4, 5.2],
                   "size": [2, 3, 4, 2, 2, 5, 3, 2, 4, 3, 2, 3, 6, 2, 4, 5]})

ax = sns.kdeplot(data=df, x="bill", fill=True)

type(ax).__name__                           # 'Axes'

len(ax.collections) > 0                     # True

ax2 = sns.kdeplot(data=df, x="bill", y="tip")

len(ax2.collections) > 0                    # True
```

> ⚠️ `fill=True` 填充曲线下面积；同时给 `x` 和 `y` 就变成**二维密度等高线**（看两个变量的联合分布）。样本很少时密度估计会不平滑，别过度解读。

### `sns.ecdfplot、sns.rugplot` 累积分布、地毯图

**解析**　ecdfplot 画经验累积分布（看「低于某值的比例」）；rugplot 在坐标轴边画小刻度展示原始数据的位置。都是轴级函数，常叠加在别的图下面。

返回：`Axes`

**操作**

```python
import seaborn as sns

import pandas as pd

import matplotlib.pyplot as plt

df = pd.DataFrame({"day": ["Thur", "Fri", "Sat", "Sun"] * 4,
                   "sex": ["Male"] * 8 + ["Female"] * 8,
                   "bill": [17.0, 20.5, 25.0, 30.2, 12.5, 40.1, 22.3, 18.8,
                            35.0, 27.5, 19.0, 22.4, 48.0, 15.5, 29.9, 33.2],
                   "tip": [2.0, 3.5, 4.0, 5.1, 1.5, 6.0, 3.2, 2.8,
                           5.0, 4.2, 2.4, 3.0, 7.5, 2.2, 4.4, 5.2],
                   "size": [2, 3, 4, 2, 2, 5, 3, 2, 4, 3, 2, 3, 6, 2, 4, 5]})

ax = sns.ecdfplot(data=df, x="bill")

type(ax).__name__                           # 'Axes'

len(ax.lines)                               # 1

ax2 = sns.rugplot(data=df, x="bill")

len(ax2.collections)                        # 1
```

> ⚠️ `ecdfplot` 画经验累积分布（看「低于某值的比例」，比直方图更客观、不受 `bins` 影响）；`rugplot` 画坐标轴上的小刻度（**是线段集合，在 `ax.collections` 里而不是 `ax.lines`**），常叠加在别的图下面展示原始数据分布。

### `sns.boxplot、sns.violinplot` 箱线图、小提琴图

**解析**　boxplot 画箱线图（中位数、四分位、离群值）；violinplot 画小提琴图 = 箱线 + 密度形状，能看出双峰、偏斜。都是轴级函数。

返回：`Axes`

**操作**

```python
import seaborn as sns

import pandas as pd

import matplotlib.pyplot as plt

df = pd.DataFrame({"day": ["Thur", "Fri", "Sat", "Sun"] * 4,
                   "sex": ["Male"] * 8 + ["Female"] * 8,
                   "bill": [17.0, 20.5, 25.0, 30.2, 12.5, 40.1, 22.3, 18.8,
                            35.0, 27.5, 19.0, 22.4, 48.0, 15.5, 29.9, 33.2],
                   "tip": [2.0, 3.5, 4.0, 5.1, 1.5, 6.0, 3.2, 2.8,
                           5.0, 4.2, 2.4, 3.0, 7.5, 2.2, 4.4, 5.2],
                   "size": [2, 3, 4, 2, 2, 5, 3, 2, 4, 3, 2, 3, 6, 2, 4, 5]})

ax = sns.boxplot(data=df, x="day", y="bill", hue="sex")

type(ax).__name__                           # 'Axes'

len(ax.patches) > 0                         # True

ax2 = sns.violinplot(data=df, x="day", y="bill")

type(ax2).__name__                          # 'Axes'
```

> ⚠️ `x` 是分类、`y` 是数值；箱线图看中位数和离群值，小提琴图还能看出**分布形状**（双峰、偏斜）。小提琴 = 箱线 + 密度形状。`hue=` 分组时每类会并排画。

### `sns.displot(data, x, kind, col)` 图级分布图（可分面）

**解析**　分布图的「图级」版本：kind 切换直方图、密度曲线或累积分布，还能按 col、row 分面。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| data | None | 数据表（DataFrame） |
| x | None | 要统计的数值列 |
| kind | 'hist' | 图种：hist（直方图）、kde、ecdf |
| col | None | 按这一列分面（一列一个子图） |
| row | None | 按这一列分面（一行一个子图） |

返回：`FacetGrid`（图级函数）

**操作**

```python
import seaborn as sns

import pandas as pd

import matplotlib.pyplot as plt

df = pd.DataFrame({"day": ["Thur", "Fri", "Sat", "Sun"] * 4,
                   "sex": ["Male"] * 8 + ["Female"] * 8,
                   "bill": [17.0, 20.5, 25.0, 30.2, 12.5, 40.1, 22.3, 18.8,
                            35.0, 27.5, 19.0, 22.4, 48.0, 15.5, 29.9, 33.2],
                   "tip": [2.0, 3.5, 4.0, 5.1, 1.5, 6.0, 3.2, 2.8,
                           5.0, 4.2, 2.4, 3.0, 7.5, 2.2, 4.4, 5.2],
                   "size": [2, 3, 4, 2, 2, 5, 3, 2, 4, 3, 2, 3, 6, 2, 4, 5]})

g = sns.displot(data=df, x="bill", col="sex", kind="hist", kde=True)

type(g).__name__                            # 'FacetGrid'

g.axes.shape                                # (1, 2)

g2 = sns.displot(data=df, x="bill", kind="kde")

type(g2).__name__                           # 'FacetGrid'
```

> ⚠️ `kind` 可选 `hist` / `kde` / `ecdf`，等价于「`histplot`/`kdeplot`/`ecdfplot` + 分面」。要和别的图拼在一起就用轴级函数。

## A4 分类图

### `sns.barplot(data, x, y, hue)` 柱状图（默认画均值+误差棒）

**解析**　画柱状图：默认算每个类别的均值来定柱高，再画 95% 置信区间误差棒——画的是聚合值，不是原始值。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| data | None | 数据表（DataFrame） |
| x | None | 横轴分类列 |
| y | None | 纵轴数值列 |
| hue | None | 按这一列再分组（并排画） |
| estimator | 'mean' | 统计量：默认均值，可换 'median'（老写法 estimator=sum 已不推荐） |
| errorbar | ('ci', 95) | 误差棒设定；None 不画 |

返回：`Axes`

**操作**

```python
import seaborn as sns

import pandas as pd

import matplotlib.pyplot as plt

df = pd.DataFrame({"day": ["Thur", "Fri", "Sat", "Sun"] * 4,
                   "sex": ["Male"] * 8 + ["Female"] * 8,
                   "bill": [17.0, 20.5, 25.0, 30.2, 12.5, 40.1, 22.3, 18.8,
                            35.0, 27.5, 19.0, 22.4, 48.0, 15.5, 29.9, 33.2],
                   "tip": [2.0, 3.5, 4.0, 5.1, 1.5, 6.0, 3.2, 2.8,
                           5.0, 4.2, 2.4, 3.0, 7.5, 2.2, 4.4, 5.2],
                   "size": [2, 3, 4, 2, 2, 5, 3, 2, 4, 3, 2, 3, 6, 2, 4, 5]})

ax = sns.barplot(data=df, x="day", y="bill")

type(ax).__name__                           # 'Axes'

[len(c) for c in ax.containers]             # [4]

ax2 = sns.barplot(data=df, x="day", y="bill", hue="sex", errorbar=None)

[len(c) for c in ax2.containers]            # [4, 4, 4]

len(ax2.patches)                            # 14
```

> ⚠️ **默认画每个类别的均值 + 95% 置信区间**（不是柱子高度 = 原始值），这点最容易误解——画的是**聚合值**不是原始值。要换统计量用 `estimator="median"`（老写法 `estimator=sum` 仍可用但**已不推荐**），去误差棒用 `errorbar=None`。看「每个 hue 层有几根柱子」用 `[len(c) for c in ax.containers]`：**`ax.patches` 里会多出给图例用的零高占位柱**，直接数它会多算。

### `sns.countplot(data, x, hue)` 计数图（不用给 y）

**解析**　画计数图：数每个类别出现多少次来定柱高，只给 x（或只给 y）就行；等价于 value_counts 后画柱。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| data | None | 数据表（DataFrame） |
| x | None | 只给 x：按这一列分类数个数（横向就只给 y） |
| y | None | 只给 y：画横向计数图 |
| hue | None | 按这一列分组（每个组各画一层柱子） |

返回：`Axes`

**操作**

```python
import seaborn as sns

import pandas as pd

import matplotlib.pyplot as plt

df = pd.DataFrame({"day": ["Thur", "Fri", "Sat", "Sun"] * 4,
                   "sex": ["Male"] * 8 + ["Female"] * 8,
                   "bill": [17.0, 20.5, 25.0, 30.2, 12.5, 40.1, 22.3, 18.8,
                            35.0, 27.5, 19.0, 22.4, 48.0, 15.5, 29.9, 33.2],
                   "tip": [2.0, 3.5, 4.0, 5.1, 1.5, 6.0, 3.2, 2.8,
                           5.0, 4.2, 2.4, 3.0, 7.5, 2.2, 4.4, 5.2],
                   "size": [2, 3, 4, 2, 2, 5, 3, 2, 4, 3, 2, 3, 6, 2, 4, 5]})

ax = sns.countplot(data=df, x="day")

type(ax).__name__                           # 'Axes'

[len(c) for c in ax.containers]             # [4]

df["day"].value_counts().to_dict()          # {'Thur': 4, 'Fri': 4, 'Sat': 4, 'Sun': 4}

ax2 = sns.countplot(data=df, x="day", hue="sex")

[len(c) for c in ax2.containers]            # [4, 4, 4]
```

> ⚠️ 只给 `x`（或只给 `y`）就看类别频数；等价于按类别 value_counts 后画柱。`hue=` 分组后**每个组各画一层柱子**（`[len(c) for c in ax.containers]` 就是每层柱子数）。类别太多时用横向（只给 `y=`）更清楚。

### `sns.pointplot(data, x, y, hue)` 点线图（趋势）

**解析**　画点线图：把每个类别的均值画成一个点再连起来，适合看随顺序变化的趋势。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| data | None | 数据表（DataFrame） |
| x | None | 横轴分类列 |
| y | None | 纵轴数值列 |
| hue | None | 按这一列分组（每组一条线） |
| errorbar | ('ci', 95) | 置信区间；None 不画 |

返回：`Axes`

**操作**

```python
import seaborn as sns

import pandas as pd

import matplotlib.pyplot as plt

df = pd.DataFrame({"day": ["Thur", "Fri", "Sat", "Sun"] * 4,
                   "sex": ["Male"] * 8 + ["Female"] * 8,
                   "bill": [17.0, 20.5, 25.0, 30.2, 12.5, 40.1, 22.3, 18.8,
                            35.0, 27.5, 19.0, 22.4, 48.0, 15.5, 29.9, 33.2],
                   "tip": [2.0, 3.5, 4.0, 5.1, 1.5, 6.0, 3.2, 2.8,
                           5.0, 4.2, 2.4, 3.0, 7.5, 2.2, 4.4, 5.2],
                   "size": [2, 3, 4, 2, 2, 5, 3, 2, 4, 3, 2, 3, 6, 2, 4, 5]})

ax = sns.pointplot(data=df, x="day", y="bill", hue="sex")

type(ax).__name__                           # 'Axes'

len(ax.lines) > 0                           # True
```

> ⚠️ 比 `barplot` 更适合看「随顺序变化的趋势」（比如不同天数的均值走势），因为它把均值点连了起来（均值点 + 连线）。同样有置信区间（`errorbar=None` 关掉）。

### `sns.stripplot、sns.swarmplot` 散点条带、蜂群图

**解析**　把每个原始数据点都画出来：stripplot 点在一条线上（jitter 抖动错开），swarmplot 把点排开不重叠。

返回：`Axes`

**操作**

```python
import seaborn as sns

import pandas as pd

import matplotlib.pyplot as plt

df = pd.DataFrame({"day": ["Thur", "Fri", "Sat", "Sun"] * 4,
                   "sex": ["Male"] * 8 + ["Female"] * 8,
                   "bill": [17.0, 20.5, 25.0, 30.2, 12.5, 40.1, 22.3, 18.8,
                            35.0, 27.5, 19.0, 22.4, 48.0, 15.5, 29.9, 33.2],
                   "tip": [2.0, 3.5, 4.0, 5.1, 1.5, 6.0, 3.2, 2.8,
                           5.0, 4.2, 2.4, 3.0, 7.5, 2.2, 4.4, 5.2],
                   "size": [2, 3, 4, 2, 2, 5, 3, 2, 4, 3, 2, 3, 6, 2, 4, 5]})

ax = sns.stripplot(data=df, x="day", y="bill", jitter=True)

type(ax).__name__                           # 'Axes'

ax2 = sns.swarmplot(data=df, x="day", y="bill")

type(ax2).__name__                          # 'Axes'
```

> ⚠️ **能直接看到每个原始数据点**（箱线图只给统计量）：`stripplot` 点会重叠（`jitter=True` 抖动错开），`swarmplot` 把点排开不重叠（**数据多时很慢**；点不重叠用 swarm）。常叠加在 `boxplot` 上看细节。

### `sns.boxenplot(data, x, y)` 增强箱线图（大数据）

**解析**　画增强箱线图：比箱线图多画若干分位数，更像分布形状，样本量大时信息更多。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| data | None | 数据表（DataFrame） |
| x | None | 横轴分类列 |
| y | None | 纵轴数值列 |

返回：`Axes`

**操作**

```python
import seaborn as sns

import pandas as pd

import matplotlib.pyplot as plt

df = pd.DataFrame({"day": ["Thur", "Fri", "Sat", "Sun"] * 4,
                   "sex": ["Male"] * 8 + ["Female"] * 8,
                   "bill": [17.0, 20.5, 25.0, 30.2, 12.5, 40.1, 22.3, 18.8,
                            35.0, 27.5, 19.0, 22.4, 48.0, 15.5, 29.9, 33.2],
                   "tip": [2.0, 3.5, 4.0, 5.1, 1.5, 6.0, 3.2, 2.8,
                           5.0, 4.2, 2.4, 3.0, 7.5, 2.2, 4.4, 5.2],
                   "size": [2, 3, 4, 2, 2, 5, 3, 2, 4, 3, 2, 3, 6, 2, 4, 5]})

ax = sns.boxenplot(data=df, x="day", y="bill")

type(ax).__name__                           # 'Axes'

len(ax.patches) > 0                         # False
```

> ⚠️ 比箱线图多画若干分位数（显示更多分位数，更像分布形状），**样本量大时**比 `boxplot` 信息更多；样本量小时两者差不多。

### `sns.catplot(data, x, y, kind, col)` 图级分类图（可分面）

**解析**　分类图的「图级」版本：kind 可选 8 种轴级分类图，支持 col、row 分面。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| data | None | 数据表（DataFrame） |
| x | None | 横轴列（分类） |
| y | None | 纵轴列（数值） |
| kind | 'strip' | 图种：strip、swarm、box、violin、boxen、point、bar、count |
| col | None | 按这一列分面 |
| row | None | 按这一列分面 |

返回：`FacetGrid`（图级函数）

**操作**

```python
import seaborn as sns

import pandas as pd

import matplotlib.pyplot as plt

df = pd.DataFrame({"day": ["Thur", "Fri", "Sat", "Sun"] * 4,
                   "sex": ["Male"] * 8 + ["Female"] * 8,
                   "bill": [17.0, 20.5, 25.0, 30.2, 12.5, 40.1, 22.3, 18.8,
                            35.0, 27.5, 19.0, 22.4, 48.0, 15.5, 29.9, 33.2],
                   "tip": [2.0, 3.5, 4.0, 5.1, 1.5, 6.0, 3.2, 2.8,
                           5.0, 4.2, 2.4, 3.0, 7.5, 2.2, 4.4, 5.2],
                   "size": [2, 3, 4, 2, 2, 5, 3, 2, 4, 3, 2, 3, 6, 2, 4, 5]})

g = sns.catplot(data=df, x="day", y="bill", kind="box", col="sex")

type(g).__name__                            # 'FacetGrid'

g.axes.shape                                # (1, 2)

g2 = sns.catplot(data=df, x="day", kind="count")

type(g2).__name__                           # 'FacetGrid'
```

> ⚠️ `kind` 可选 `strip` `swarm` `box` `violin` `boxen` `point` `bar` `count`，是各轴级分类图的「分面版」。要嵌进 `plt.subplots()` 布局就用轴级函数。**注意 `kind="count"` 不能同时给 `x` 和 `y`**（会报 `ValueError: Cannot pass values for both x and y`），只给 `x` 就行。

## A5 回归图

### `sns.regplot(data, x, y, ci)` 散点+回归直线

**解析**　画散点并拟合一条线性回归直线，默认带 95% 置信区间阴影。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| data | None | 数据表（DataFrame） |
| x | None | 横轴数值列 |
| y | None | 纵轴数值列 |
| ci | 95 | 置信区间；None 只画线不画阴影 |
| scatter_kws | None | 传给散点的微调字典（如 {"s": 10}） |
| line_kws | None | 传给回归线的微调字典（如 {"color": "red"}） |

返回：`Axes`（轴级；默认带置信区间）

**操作**

```python
import seaborn as sns

import pandas as pd

import matplotlib.pyplot as plt

df = pd.DataFrame({"day": ["Thur", "Fri", "Sat", "Sun"] * 4,
                   "sex": ["Male"] * 8 + ["Female"] * 8,
                   "bill": [17.0, 20.5, 25.0, 30.2, 12.5, 40.1, 22.3, 18.8,
                            35.0, 27.5, 19.0, 22.4, 48.0, 15.5, 29.9, 33.2],
                   "tip": [2.0, 3.5, 4.0, 5.1, 1.5, 6.0, 3.2, 2.8,
                           5.0, 4.2, 2.4, 3.0, 7.5, 2.2, 4.4, 5.2],
                   "size": [2, 3, 4, 2, 2, 5, 3, 2, 4, 3, 2, 3, 6, 2, 4, 5]})

ax = sns.regplot(data=df, x="bill", y="tip")

type(ax).__name__                           # 'Axes'

len(ax.lines)                               # 1

ax2 = sns.regplot(data=df, x="bill", y="tip", ci=None, scatter_kws={"s": 10})

type(ax2).__name__                          # 'Axes'
```

> ⚠️ 默认画**线性回归直线 + 95% 置信区间阴影**（数据少时阴影很宽，说明估计不可靠）。`ci=None` 只画线；`scatter_kws={"s": 10}` / `line_kws={"color": "red"}` 可以分别微调点和线。

### `sns.lmplot(data, x, y, hue, col)` 图级回归图（分组拟合）

**解析**　回归图的「图级」版本：按 hue、col、row 分组各自拟合回归线，方便比较不同组的趋势。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| data | 必填 | 数据表（DataFrame） |
| x | None | 横轴数值列 |
| y | None | 纵轴数值列 |
| hue | None | 按这一列分组，每组各拟合一条线 |
| col | None | 按这一列分面 |
| row | None | 按这一列分面 |

返回：`FacetGrid`（图级函数）

**操作**

```python
import seaborn as sns

import pandas as pd

import matplotlib.pyplot as plt

df = pd.DataFrame({"day": ["Thur", "Fri", "Sat", "Sun"] * 4,
                   "sex": ["Male"] * 8 + ["Female"] * 8,
                   "bill": [17.0, 20.5, 25.0, 30.2, 12.5, 40.1, 22.3, 18.8,
                            35.0, 27.5, 19.0, 22.4, 48.0, 15.5, 29.9, 33.2],
                   "tip": [2.0, 3.5, 4.0, 5.1, 1.5, 6.0, 3.2, 2.8,
                           5.0, 4.2, 2.4, 3.0, 7.5, 2.2, 4.4, 5.2],
                   "size": [2, 3, 4, 2, 2, 5, 3, 2, 4, 3, 2, 3, 6, 2, 4, 5]})

g = sns.lmplot(data=df, x="bill", y="tip", hue="sex", col="sex")

type(g).__name__                            # 'FacetGrid'

g.axes.shape                                # (1, 2)
```

> ⚠️ 按 `hue`/`col`/`row` **分别拟合**回归线（`regplot` 只画一条）。适合比较不同组的趋势是否一致。提醒：相关/回归不等于因果。

### `sns.residplot(data, x, y)` 残差图（检查拟合是否合理）

**解析**　画残差图：把真实值减预测值的差画出来，看线性拟合合不合适。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| data | None | 数据表（DataFrame） |
| x | None | 横轴数值列 |
| y | None | 纵轴数值列 |

返回：`Axes`

**操作**

```python
import seaborn as sns

import pandas as pd

import matplotlib.pyplot as plt

df = pd.DataFrame({"day": ["Thur", "Fri", "Sat", "Sun"] * 4,
                   "sex": ["Male"] * 8 + ["Female"] * 8,
                   "bill": [17.0, 20.5, 25.0, 30.2, 12.5, 40.1, 22.3, 18.8,
                            35.0, 27.5, 19.0, 22.4, 48.0, 15.5, 29.9, 33.2],
                   "tip": [2.0, 3.5, 4.0, 5.1, 1.5, 6.0, 3.2, 2.8,
                           5.0, 4.2, 2.4, 3.0, 7.5, 2.2, 4.4, 5.2],
                   "size": [2, 3, 4, 2, 2, 5, 3, 2, 4, 3, 2, 3, 6, 2, 4, 5]})

ax = sns.residplot(data=df, x="bill", y="tip")

type(ax).__name__                           # 'Axes'

len(ax.collections)                         # 1
```

> ⚠️ 残差 = 真实值 − 预测值，应随机散布在 0 两侧。**如果残差呈现 U 形/喇叭形，说明线性模型不合适**（该换非线性或加特征）；随机散布在 0 两侧才说明线性拟合可以接受。

## A6 矩阵图

### `sns.heatmap(data, annot, cmap)` 热力图（相关性矩阵标配）

**解析**　把二维矩阵画成颜色格子，常配 df.corr() 看相关性；annot 把数值写进格子里。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| data | 必填 | 二维矩阵（常配 df.corr()） |
| annot | None | True 时把数值写进格子 |
| fmt | '.2g' | 格子里数字的格式（如 ".2f"） |
| cmap | None | 色图名（如 "coolwarm"、"viridis"） |
| square | False | True 让格子变正方形 |
| vmin、vmax | None | 固定色阶上下限（比较两张热力图时必须设成一样） |

返回：`Axes`

**操作**

```python
import seaborn as sns

import pandas as pd

import matplotlib.pyplot as plt

df = pd.DataFrame({"day": ["Thur", "Fri", "Sat", "Sun"] * 4,
                   "sex": ["Male"] * 8 + ["Female"] * 8,
                   "bill": [17.0, 20.5, 25.0, 30.2, 12.5, 40.1, 22.3, 18.8,
                            35.0, 27.5, 19.0, 22.4, 48.0, 15.5, 29.9, 33.2],
                   "tip": [2.0, 3.5, 4.0, 5.1, 1.5, 6.0, 3.2, 2.8,
                           5.0, 4.2, 2.4, 3.0, 7.5, 2.2, 4.4, 5.2],
                   "size": [2, 3, 4, 2, 2, 5, 3, 2, 4, 3, 2, 3, 6, 2, 4, 5]})

corr = df[["bill", "tip", "size"]].corr()

ax = sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", square=True)

type(ax).__name__                           # 'Axes'

len(ax.texts)                               # 9

len(ax.collections)                         # 1
```

> ⚠️ `annot=True` 把数字写在格子里（`fmt` 控制小数位）；`square=True` 让格子变正方向；`vmin`/`vmax` 固定色阶范围（**比较两张热力图时必须设成一样**）。注意：`df.corr()` 在 pandas 3 里遇到字符串列要 `numeric_only=True`。常配 `df.corr()`。

### `sns.clustermap(data, annot)` 聚类热力图

**解析**　画聚类热力图：先对行/列做层次聚类把相似的排在一起，再画热力图；需要 scipy。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| data | 必填 | 二维矩阵 |
| method | 'average' | 层次聚类方法 |
| metric | 'euclidean' | 距离度量 |
| row_cluster、col_cluster | True | 是否对行/列做聚类重排 |
| z_score、standard_scale | None | 按行/列标准化后再画 |
| figsize | (10, 10) | 图的大小 |

返回：`ClusterGrid`（不是 Axes；子图用 `g.ax_heatmap` 等取）

**操作**

```python
import seaborn as sns

import pandas as pd

import matplotlib.pyplot as plt

df = pd.DataFrame({"day": ["Thur", "Fri", "Sat", "Sun"] * 4,
                   "sex": ["Male"] * 8 + ["Female"] * 8,
                   "bill": [17.0, 20.5, 25.0, 30.2, 12.5, 40.1, 22.3, 18.8,
                            35.0, 27.5, 19.0, 22.4, 48.0, 15.5, 29.9, 33.2],
                   "tip": [2.0, 3.5, 4.0, 5.1, 1.5, 6.0, 3.2, 2.8,
                           5.0, 4.2, 2.4, 3.0, 7.5, 2.2, 4.4, 5.2],
                   "size": [2, 3, 4, 2, 2, 5, 3, 2, 4, 3, 2, 3, 6, 2, 4, 5]})

corr = df[["bill", "tip", "size"]].corr()

g = sns.clustermap(corr, annot=True, cmap="viridis")

type(g).__name__                            # 'ClusterGrid'

g.ax_heatmap is not None                    # True
```

> ⚠️ 对行/列做层次聚类后重排再画（相似的变量会挨在一起），**需要装 scipy**。返回的是 `ClusterGrid`（不是 Axes），要调子图得用 `g.ax_heatmap` / `g.ax_row_dendrogram`。`annot=`/`cmap=` 这类关键字会透传给内部 heatmap。

### `sns.pairplot(data, hue)` 成对关系图（多变量速览）

**解析**　对所有数值列两两画散点、对角线画分布，一张图看完所有变量之间的关系——数据探查第一步。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| data | 必填 | 数据表（DataFrame） |
| hue | None | 按这一列的分类值着色 |
| diag_kind | 'auto' | 对角线画什么：'auto'、'hist'、'kde' |

返回：`PairGrid`

**操作**

```python
import seaborn as sns

import pandas as pd

import matplotlib.pyplot as plt

df = pd.DataFrame({"day": ["Thur", "Fri", "Sat", "Sun"] * 4,
                   "sex": ["Male"] * 8 + ["Female"] * 8,
                   "bill": [17.0, 20.5, 25.0, 30.2, 12.5, 40.1, 22.3, 18.8,
                            35.0, 27.5, 19.0, 22.4, 48.0, 15.5, 29.9, 33.2],
                   "tip": [2.0, 3.5, 4.0, 5.1, 1.5, 6.0, 3.2, 2.8,
                           5.0, 4.2, 2.4, 3.0, 7.5, 2.2, 4.4, 5.2],
                   "size": [2, 3, 4, 2, 2, 5, 3, 2, 4, 3, 2, 3, 6, 2, 4, 5]})

g = sns.pairplot(df[["bill", "tip", "size", "sex"]], hue="sex")

type(g).__name__                            # 'PairGrid'

g.axes.shape                                # (3, 3)

g.axes.shape[0]                             # 3
```

> ⚠️ 对所有数值列两两画图（对角线画分布），**一眼看完变量之间的关系** —— 数据探查第一步。列很多时很慢、图也很小，先选 4~5 个关注的列。

## A7 网格类

### `sns.FacetGrid(data, col, hue)+.map()` 自定义分面网格

**解析**　自己搭分面网格：指定按哪列分行/分列、按哪列着色，再用 .map(绘图函数, 列名...) 把任意图画进每个格子，比 relplot 灵活。

返回：`FacetGrid`

**操作**

```python
import seaborn as sns

import pandas as pd

import matplotlib.pyplot as plt

df = pd.DataFrame({"day": ["Thur", "Fri", "Sat", "Sun"] * 4,
                   "sex": ["Male"] * 8 + ["Female"] * 8,
                   "bill": [17.0, 20.5, 25.0, 30.2, 12.5, 40.1, 22.3, 18.8,
                            35.0, 27.5, 19.0, 22.4, 48.0, 15.5, 29.9, 33.2],
                   "tip": [2.0, 3.5, 4.0, 5.1, 1.5, 6.0, 3.2, 2.8,
                           5.0, 4.2, 2.4, 3.0, 7.5, 2.2, 4.4, 5.2],
                   "size": [2, 3, 4, 2, 2, 5, 3, 2, 4, 3, 2, 3, 6, 2, 4, 5]})

g = sns.FacetGrid(df, col="day", hue="sex")

g.map(sns.scatterplot, "bill", "tip")

type(g).__name__                            # 'FacetGrid'

g.axes.shape                                # (1, 4)

g.add_legend()

type(g).__name__                            # 'FacetGrid'
```

> ⚠️ `FacetGrid` 是「自己搭分面 + 想画什么就 `map` 什么」，比 `relplot` 灵活。`.map(func, *列名)` 会把列名当位置参数传给 `func`（map 里传绘图函数）；`.add_legend()` 加上图例（用 `hue` 时必须调）。

### `sns.PairGrid(data, hue)+map_diag、map_offdiag` 自定义成对网格

**解析**　pairplot 的灵活版：map_diag 指定对角线画什么（通常是分布）、map_offdiag 指定非对角线画什么（通常是散点），还能用 map_upper、map_lower 分上下三角。

返回：`PairGrid`

**操作**

```python
import seaborn as sns

import pandas as pd

import matplotlib.pyplot as plt

df = pd.DataFrame({"day": ["Thur", "Fri", "Sat", "Sun"] * 4,
                   "sex": ["Male"] * 8 + ["Female"] * 8,
                   "bill": [17.0, 20.5, 25.0, 30.2, 12.5, 40.1, 22.3, 18.8,
                            35.0, 27.5, 19.0, 22.4, 48.0, 15.5, 29.9, 33.2],
                   "tip": [2.0, 3.5, 4.0, 5.1, 1.5, 6.0, 3.2, 2.8,
                           5.0, 4.2, 2.4, 3.0, 7.5, 2.2, 4.4, 5.2],
                   "size": [2, 3, 4, 2, 2, 5, 3, 2, 4, 3, 2, 3, 6, 2, 4, 5]})

g = sns.PairGrid(df[["bill", "tip", "size", "sex"]], hue="sex")

g.map_diag(sns.histplot)

g.map_offdiag(sns.scatterplot)

type(g).__name__                            # 'PairGrid'

g.axes.shape                                # (3, 3)

g.add_legend()
```

> ⚠️ 分别指定**对角线**（通常是分布）和**非对角线**（通常是散点）画什么，比 `pairplot` 可控（pairplot 的灵活版）。想让上下三角画不同东西，还能用 `map_upper` / `map_lower`。

### `sns.jointplot(data, x, y, kind)` 联合分布图（主图+边缘分布）

**解析**　一张图里画主图（两个变量的关系）+ 旁边的边缘分布；kind 可选 scatter、kde、hist、hex、reg。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| data | None | 数据表（DataFrame） |
| x | None | 横轴数值列 |
| y | None | 纵轴数值列 |
| kind | 'scatter' | 主图图种：scatter、kde、hist、hex、reg |

返回：`JointGrid`（**没有 `.axes`**，取子图用 `g.ax_joint`、`g.ax_marg_x`、`g.ax_marg_y`）

**操作**

```python
import seaborn as sns

import pandas as pd

import matplotlib.pyplot as plt

df = pd.DataFrame({"day": ["Thur", "Fri", "Sat", "Sun"] * 4,
                   "sex": ["Male"] * 8 + ["Female"] * 8,
                   "bill": [17.0, 20.5, 25.0, 30.2, 12.5, 40.1, 22.3, 18.8,
                            35.0, 27.5, 19.0, 22.4, 48.0, 15.5, 29.9, 33.2],
                   "tip": [2.0, 3.5, 4.0, 5.1, 1.5, 6.0, 3.2, 2.8,
                           5.0, 4.2, 2.4, 3.0, 7.5, 2.2, 4.4, 5.2],
                   "size": [2, 3, 4, 2, 2, 5, 3, 2, 4, 3, 2, 3, 6, 2, 4, 5]})

g = sns.jointplot(data=df, x="bill", y="tip", kind="scatter")

type(g).__name__                            # 'JointGrid'

len(g.fig.axes)                             # 3

type(g.ax_joint).__name__                   # 'Axes'

g2 = sns.jointplot(data=df, x="bill", y="tip", kind="hex")

type(g2).__name__                           # 'JointGrid'
```

> ⚠️ 主图看两个变量的关系、旁边带各自的边缘分布。`kind` 可选 `scatter` `kde` `hist` `hex` `reg`。**返回的 `JointGrid` 没有 `.axes`**，要取子图用 `g.ax_joint`（主图）/ `g.ax_marg_x` / `g.ax_marg_y`；也可以用 `g.fig.axes` 拿到全部。

## 学习建议

1. **先分图级 / 轴级**：
   - **图级**（`relplot` `displot` `catplot` `lmplot` `jointplot`）自动建子图、支持 `row`/`col` 分面，返回 `FacetGrid` / `JointGrid`；
   - **轴级**（`scatterplot` `histplot` `barplot` …）画在指定轴上，方便塞进 `plt.subplots()` 里组合。
2. **`hue` 是灵魂参数**：几乎每个绘图函数都支持 `hue=` 按分类着色，这是 Seaborn 比 Matplotlib 省事的地方；`size=`、`style=` 还能再编码两个维度。
3. **相关性热力图三行套路**：
   ```python
   import seaborn as sns, matplotlib.pyplot as plt
   df = sns.load_dataset("tips")           # 或自己的数据（首次需联网下载）
   corr = df.select_dtypes("number").corr()
   sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", square=True)
   plt.show()
   ```
4. **统计图优先 Seaborn**：带置信区间的折线、分组箱线图、蜂群图、热力图，Seaborn 一行搞定，别在 Matplotlib 里手写。
5. **和 Matplotlib 混用**：`sns.set_theme()` 设风格，之后仍可用 `ax.set_title()` / `plt.xticks(rotation=45)` 微调；中文字体照 Matplotlib 那套设。
