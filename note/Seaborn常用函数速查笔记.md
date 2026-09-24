# Seaborn 常用函数速查笔记

> 整理范围：统计可视化中最常用的 Seaborn 操作，覆盖关系图、分布图、分类图、回归图、矩阵图与多子图网格。
> 每个函数都附有 **语法签名** + **作用说明** + **可运行示例**。
> 约定：`import seaborn as sns`。Seaborn 基于 Matplotlib，二者可混用。数据常用 `sns.load_dataset()` 加载。

---

## 目录

1. [主题与样式](#一主题与样式)
2. [关系图](#二关系图)
3. [分布图](#三分布图)
4. [分类图](#四分类图)
5. [回归图](#五回归图)
6. [矩阵图](#六矩阵图)
7. [多子图网格](#七多子图网格)
8. [速查表](#八速查表)

---

## 一、主题与样式

### `sns.set_theme(style=..., palette=..., context=...)` / `sns.set_style()` / `sns.set_palette()` / `sns.set_context()`
全局设置主题。`style` 背景（`"darkgrid"` `"whitegrid"` `"dark"` `"white"` `"ticks"`）；`palette` 配色；`context` 缩放（`"paper"` `"notebook"` `"talk"` `"poster"`）。
```python
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="darkgrid", palette="muted")   # 一步到位
sns.set_style("whitegrid")       # 只设背景
sns.set_context("talk")          # 放大字体（做演示用）
```

### `sns.color_palette(name, n_colors=None)` / `sns.set_palette(name)`
查看/生成调色板。常用：`"deep"` `"muted"` `"bright"` `"pastel"` `"dark"` `"colorblind"`，或色图名如 `"viridis"`。
```python
sns.color_palette("muted")               # 返回颜色列表
sns.set_palette("colorblind")            # 全局设置
```

### `sns.load_dataset(name)` / `sns.get_dataset_names()`
加载内置示例数据集（如 `"tips"` `"iris"` `"titanic"` `"penguins"` `"diamonds"` `"mpg"` `"fmri"`）。
```python
df = sns.load_dataset("tips")
print(sns.get_dataset_names())           # 列出所有内置数据集
```

---

## 二、关系图

### `sns.scatterplot(data, x, y, hue=None, size=None, style=None, ...)`
散点图。`hue` 按分类着色、`size` 按数值调大小、`style` 按分类调标记形状。
```python
sns.scatterplot(data=df, x="total_bill", y="tip", hue="sex", size="size")
```

### `sns.lineplot(data, x, y, hue=None, ...)`
折线图。自动计算并画出**均值 + 置信区间阴影**（`ci` 参数控制）。
```python
sns.lineplot(data=df, x="time", y="total_bill", hue="smoker")
sns.lineplot(data=df, x="time", y="total_bill", ci=None)   # 关闭置信区间
```

### `sns.relplot(data, x, y, kind="scatter", row=None, col=None, ...)`
关系图的**图级**函数，用 `row`/`col` 按分类分面成多个子图。`kind` 可选 `"scatter"`（默认）或 `"line"`。
```python
g = sns.relplot(data=df, x="total_bill", y="tip", hue="sex",
                col="time", kind="scatter")     # 按 time 分成多列子图
```

> **图级 vs 轴级**：`relplot`/`displot`/`catplot`/`lmplot` 是**图级**函数（自动创建子图网格，返回 FacetGrid）；`scatterplot`/`lineplot`/`histplot` 等是**轴级**函数（画在指定轴上）。分面用图级，单图用轴级。

---

## 三、分布图

### `sns.histplot(data, x, bins=None, kde=False, hue=None, ...)`
直方图。`kde=True` 叠加核密度估计曲线，`hue` 分组着色，`stat` 控制纵轴（`"count"`/`"density"`/`"probability"`）。
```python
sns.histplot(data=df, x="total_bill", bins=30, kde=True)
sns.histplot(data=df, x="total_bill", hue="sex", kde=True)   # 分组
```

### `sns.kdeplot(data, x=None, y=None, hue=None, ...)`
核密度估计曲线（概率密度）。传 `x` 与 `y` 可画二维密度等高线。
```python
sns.kdeplot(data=df, x="total_bill", hue="sex", fill=True)   # fill 填充面积
sns.kdeplot(data=df, x="total_bill", y="tip")                 # 二维密度
```

### `sns.ecdfplot(data, x, ...)` / `sns.rugplot(data, x, ...)`
`ecdfplot` 经验累积分布函数；`rugplot` 地毯图（坐标轴上的小刻度线）。
```python
sns.ecdfplot(data=df, x="total_bill")
sns.rugplot(data=df, x="total_bill")
```

### `sns.boxplot(data, x, y, ...)` / `sns.violinplot(data, x, y, ...)`
箱线图 / 小提琴图（箱线图 + 密度曲线）。
```python
sns.boxplot(data=df, x="day", y="total_bill", hue="sex")
sns.violinplot(data=df, x="day", y="total_bill", hue="sex")
```

### `sns.displot(data, x, kind="hist", ...)` — 图级分布图
`kind` 可选 `"hist"`（直方）、`"kde"`（密度）、`"ecdf"`（累积分布）。支持 `row`/`col` 分面。
```python
sns.displot(data=df, x="total_bill", kind="hist", kde=True)
sns.displot(data=df, x="total_bill", col="sex", kind="kde")
```

---

## 四、分类图

### `sns.barplot(data, x, y, hue=None, ...)`
柱状图（默认画**均值 + 误差棒**）。`estimator` 可改统计量（如 `sum`、`median`）。
```python
sns.barplot(data=df, x="day", y="total_bill", hue="sex")
sns.barplot(data=df, x="day", y="total_bill", estimator=sum)   # 改成求和
```

### `sns.countplot(data, x=None, y=None, hue=None, ...)`
计数图（统计各类别出现次数，无需 y 值）。
```python
sns.countplot(data=df, x="day", hue="sex")
```

### `sns.pointplot(data, x, y, hue=None, ...)`
点线图：画各分类的均值点并连线，适合比较趋势。
```python
sns.pointplot(data=df, x="day", y="total_bill", hue="sex")
```

### `sns.stripplot(data, x, y, ...)` / `sns.swarmplot(data, x, y, ...)`
`stripplot` 散点条带图（点会重叠）；`swarmplot` 蜂群图（点不重叠）。
```python
sns.stripplot(data=df, x="day", y="total_bill", jitter=True)
sns.swarmplot(data=df, x="day", y="total_bill", hue="sex")
```

### `sns.boxenplot(data, x, y, ...)`
增强箱线图（显示更多分位数，适合大数据）。
```python
sns.boxenplot(data=df, x="day", y="total_bill")
```

### `sns.catplot(data, x, y, kind=..., row=None, col=None, ...)` — 图级分类图
`kind` 可选 `"strip"` `"swarm"` `"box"` `"violin"` `"boxen"` `"point"` `"bar"` `"count"`。
```python
sns.catplot(data=df, x="day", y="total_bill", kind="box", col="sex")
```

---

## 五、回归图

### `sns.regplot(data, x, y, ...)`
轴级线性回归图：散点 + 回归直线（默认带 95% 置信区间）。`ci=None` 关闭置信区间。
```python
sns.regplot(data=df, x="total_bill", y="tip")
sns.regplot(data=df, x="total_bill", y="tip", ci=None, scatter_kws={"s": 10})
```

### `sns.lmplot(data, x, y, hue=None, col=None, row=None, ...)`
图级回归图：按 `hue`/`col`/`row` 分组分别拟合回归线。
```python
sns.lmplot(data=df, x="total_bill", y="tip", hue="smoker", col="sex")
```

### `sns.residplot(data, x, y, ...)`
残差图：检查线性回归拟合是否合理（残差应随机分布在 0 两侧）。
```python
sns.residplot(data=df, x="total_bill", y="tip")
```

---

## 六、矩阵图

### `sns.heatmap(data, annot=None, cmap=None, fmt=..., ...)`
热力图（常用于相关性矩阵）。`annot=True` 显示数值、`fmt` 数值格式、`cmap` 色图、`vmin`/`vmax` 固定色阶范围。
```python
corr = df.corr()
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", square=True)
```

### `sns.clustermap(data, ...)`
聚类热力图：对行列做层次聚类并排序后画热力图。
```python
sns.clustermap(corr, annot=True, cmap="viridis")
```

### `sns.pairplot(data, hue=None, ...)`
成对关系图：对所有数值列两两画散点图，对角线画直方图/密度。
```python
sns.pairplot(df, hue="species")
```

---

## 七、多子图网格

### `sns.FacetGrid(data, row, col, hue=...)` + `.map(func, ...)`
通用分面网格：按 `row`/`col` 分组生成子图，再用 `.map` 把任意绘图函数套上去。
```python
g = sns.FacetGrid(df, col="sex", hue="smoker")
g.map(sns.scatterplot, "total_bill", "tip")      # 每个分面画散点图
g.add_legend()
```

### `sns.PairGrid(data, hue=...)` + `.map_diag()` / `.map_offdiag()`
成对网格：分别控制对角线与非对角线的绘图函数（比 `pairplot` 更灵活）。
```python
g = sns.PairGrid(df, hue="sex")
g.map_diag(sns.histplot)
g.map_offdiag(sns.scatterplot)
g.add_legend()
```

### `sns.JointGrid(data, x, y)` / `sns.jointplot(data, x, y, kind=...)`
联合分布图：主图 + 两边的边缘分布。`jointplot` 是一步到位的图级函数。
```python
sns.jointplot(data=df, x="total_bill", y="tip", kind="scatter")  # 或 "kde"、"hist"、"hex"
```

---

## 八、速查表

| 分类 | 函数 | 一句话作用 |
|------|------|-----------|
| 样式 | `set_theme` `set_style` `set_palette` `set_context` `color_palette` | 全局主题 / 配色 |
| 数据 | `load_dataset` `get_dataset_names` | 加载 / 列出内置数据集 |
| 关系 | `scatterplot` `lineplot` `relplot` | 散点 / 折线（含置信区间）/ 分面关系图 |
| 分布 | `histplot` `kdeplot` `ecdfplot` `rugplot` | 直方 / 密度 / 累积分布 / 地毯图 |
| 分布 | `boxplot` `violinplot` `displot` | 箱线 / 小提琴 / 图级分布图 |
| 分类 | `barplot` `countplot` `pointplot` | 柱状 / 计数 / 点线图 |
| 分类 | `stripplot` `swarmplot` `boxenplot` `catplot` | 散点条带 / 蜂群 / 增强箱线 / 图级分类图 |
| 回归 | `regplot` `lmplot` `residplot` | 线性回归 / 分组回归 / 残差图 |
| 矩阵 | `heatmap` `clustermap` `pairplot` | 热力图 / 聚类热力图 / 成对关系图 |
| 网格 | `FacetGrid` `PairGrid` `JointGrid` `jointplot` | 分面 / 成对 / 联合分布 |

---

## 学习建议

1. **分清图级与轴级**：图级函数（`relplot` `displot` `catplot` `lmplot`）自动建子图、支持 `row`/`col` 分面，返回 FacetGrid；轴级函数（`scatterplot` `histplot` `barplot`…）画在指定坐标轴上，适合放进 `plt.subplots()` 里组合。分面选图级，单图选轴级。
2. **`hue` 是灵魂参数**：几乎所有绘图函数都支持 `hue` 按分类着色分组，这是 Seaborn 对比 Matplotlib 最省事的地方。
3. **画相关性热力图的三行套路**：
   ```python
   corr = df.corr()
   sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", square=True)
   plt.show()
   ```
4. **统计图优先 Seaborn**：带置信区间的折线、分组箱线图、蜂群图、热力图等，用 Seaborn 一行搞定，别在 Matplotlib 里手写。
5. **样式与 Matplotlib 混用**：Seaborn 用 `sns.set_theme()` 设风格，之后仍可用 `plt.title()`、`plt.xticks(rotation=45)` 等 Matplotlib 命令微调；中文乱码同样要设 `plt.rcParams["font.sans-serif"]`。
