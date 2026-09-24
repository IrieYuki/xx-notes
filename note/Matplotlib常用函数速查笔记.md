# Matplotlib 常用函数速查笔记

> 整理范围：数据可视化中最常用的 Matplotlib 操作，覆盖基础图形、坐标轴设置、图例、子图与样式。
> 每个函数都附有 **语法签名** + **作用说明** + **可运行示例**。
> 约定：`import matplotlib.pyplot as plt`。示例基于 `fig, ax = plt.subplots()` 的**面向对象**写法（推荐）。

---

## 目录

1. [基础概念](#一基础概念)
2. [基础图形](#二基础图形)
3. [坐标轴与标题](#三坐标轴与标题)
4. [图例与网格](#四图例与网格)
5. [子图](#五子图)
6. [样式](#六样式)
7. [保存与显示](#七保存与显示)
8. [速查表](#八速查表)

---

## 一、基础概念

### 两种画图方式
- **pyplot 式**（快速、脚本用）：`plt.plot(x, y)` 直接作用于当前图。
- **面向对象式**（推荐、清晰）：先 `fig, ax = plt.subplots()`，再用 `ax.plot(...)`。

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x)

# pyplot 式
plt.plot(x, y)
plt.show()

# 面向对象式（推荐，可精细控制）
fig, ax = plt.subplots()
ax.plot(x, y)
plt.show()
```

### `plt.figure(figsize=(w, h), dpi=...)` / `plt.subplots()`
`figure` 创建画布（`figsize` 宽高英寸、`dpi` 分辨率）；`subplots` 创建画布 + 子图轴（见第五节）。
```python
fig = plt.figure(figsize=(8, 6), dpi=100)
fig, ax = plt.subplots(figsize=(8, 6))     # 一步到位
```

---

## 二、基础图形

### `ax.plot(x, y, ...)` — 折线图
最基础的绘图。常用参数：`color`/`c` 颜色、`linestyle`/`ls` 线型、`linewidth`/`lw` 线宽、`marker` 标记、`label` 图例标签。
```python
ax.plot(x, y, color="red", linestyle="--", linewidth=2, marker="o", label="sin")
```

### `ax.scatter(x, y, ...)` — 散点图
参数：`s` 点大小、`c` 颜色、`marker` 形状、`alpha` 透明度、`cmap` 色图（配合数值用）。
```python
ax.scatter(x, y, s=50, c="blue", alpha=0.6, label="数据点")
ax.scatter(x, y, c=z, cmap="viridis")   # 按 z 的值着色
```

### `ax.bar(x, height, ...)` / `ax.barh(y, width)` — 柱状图 / 水平柱状图
参数：`width` 柱宽、`color`、`align`、`edgecolor` 边框色。
```python
names = ["A", "B", "C"]
values = [3, 7, 5]
ax.bar(names, values, color="skyblue", edgecolor="black", width=0.6)
ax.barh(names, values, color="orange")      # 水平方向
```

### `ax.hist(x, bins=..., ...)` — 直方图
参数：`bins` 分箱数（或边界列表）、`density` 是否归一化为概率密度、`alpha`、`color`、`edgecolor`。
```python
data = np.random.normal(0, 1, 1000)
ax.hist(data, bins=30, color="green", alpha=0.7, edgecolor="black", density=True)
```

### `ax.pie(x, labels=None, autopct=..., ...)` — 饼图
参数：`labels` 标签、`autopct` 百分比格式（如 `"%1.1f%%"`）、`explode` 分离某块、`startangle` 起始角度。
```python
ax.pie(values, labels=names, autopct="%1.1f%%", startangle=90, explode=[0, 0.1, 0])
```

### `ax.boxplot(data)` — 箱线图
显示中位数、四分位、异常值。
```python
ax.boxplot([data1, data2, data3], labels=["A", "B", "C"])
```

---

## 三、坐标轴与标题

### `ax.set_title(label)` / `ax.set_xlabel(xlabel)` / `ax.set_ylabel(ylabel)`
设置标题、X 轴标签、Y 轴标签。可用 `fontsize` 调字号。
```python
ax.set_title("正弦曲线", fontsize=14)
ax.set_xlabel("时间")
ax.set_ylabel("幅值")
```

### `ax.set_xlim(left, right)` / `ax.set_ylim(bottom, top)`
设置坐标轴范围。
```python
ax.set_xlim(0, 10)
ax.set_ylim(-1.5, 1.5)
```

### `ax.set_xticks(ticks, labels=None)` / `ax.set_yticks(...)`
自定义刻度位置与标签。常配合 `rotation` 旋转刻度文字。
```python
ax.set_xticks([0, 5, 10])
ax.set_xticks([0, 5, 10], labels=["零", "五", "十"])
plt.xticks(rotation=45)        # 刻度文字旋转 45°，防重叠
```

### `ax.set_xscale("log")` / `ax.set_yscale("log")`
把坐标轴改为对数刻度。
```python
ax.set_yscale("log")
```

### `ax.grid(True, ...)` / `ax.axhline(y, ...)` / `ax.axvline(x, ...)`
`grid` 显示网格；`axhline`/`axvline` 画水平/垂直参考线。
```python
ax.grid(True, linestyle="--", alpha=0.5)
ax.axhline(0, color="red", linestyle="--")    # y=0 参考线
ax.axvline(5, color="gray", linestyle=":")    # x=5 参考线
```

### `ax.text(x, y, s)` / `ax.annotate(text, xy, xytext, arrowprops=...)`
`text` 在指定坐标写文字；`annotate` 带箭头的标注。
```python
ax.text(5, 1, "峰值", fontsize=12)
ax.annotate("最高点", xy=(5, 1), xytext=(3, 1.2),
            arrowprops=dict(arrowstyle="->"))
```

---

## 四、图例与网格

### `ax.legend(loc=..., ...)`
显示图例（需在绘图时传 `label` 参数）。`loc` 位置：`"upper right"` `"best"` `"lower left"` 等，或传 `frameon=False` 去边框。
```python
ax.plot(x, y1, label="sin")
ax.plot(x, y2, label="cos")
ax.legend(loc="upper right")
# 或绘图后手动指定
ax.legend(loc="best", frameon=False)
```

### `ax.twinx()` — 双 Y 轴
在同一 X 轴上叠加两个不同量纲的 Y 轴。
```python
ax2 = ax.twinx()
ax.plot(x, y1, color="blue")
ax2.plot(x, y2, color="red")     # 共用 X 轴，独立 Y 轴
```

### `ax.fill_between(x, y1, y2, ...)` — 区域填充
填充两条曲线之间的区域，常用 `alpha` 透明度。
```python
ax.fill_between(x, y1, y2, color="gray", alpha=0.3)
ax.fill_between(x, 0, y, alpha=0.2)     # 填充到 y=0
```

### `ax.errorbar(x, y, yerr=None, ...)` — 误差棒
```python
ax.errorbar(x, y, yerr=err, fmt="o", capsize=3)
```

---

## 五、子图

### `plt.subplot(nrows, ncols, index)` — pyplot 式子图
```python
plt.subplot(2, 2, 1)     # 2×2 网格中的第 1 个
plt.plot(x, y1)
plt.subplot(2, 2, 2)     # 第 2 个
plt.plot(x, y2)
```

### `fig, axes = plt.subplots(nrows, ncols, figsize=..., sharex=False, sharey=False)` — 面向对象式子图（推荐）
返回轴对象（单个轴或数组），逐个绘制。`sharex`/`sharey` 共享坐标轴。
```python
fig, axes = plt.subplots(2, 2, figsize=(10, 8), sharex=True)
axes[0, 0].plot(x, y1)     # 用索引访问每个子图
axes[0, 1].scatter(x, y2)
axes[1, 0].bar(names, values)
axes[1, 1].hist(data)
```

### `fig.tight_layout()` / `plt.tight_layout()`
自动调整子图间距，避免标签重叠（画完后调用）。
```python
fig.tight_layout()
```

### `plt.subplots_adjust(left, bottom, right, top, wspace, hspace)`
手动调整边距与子图间距。
```python
plt.subplots_adjust(wspace=0.3, hspace=0.4)
```

---

## 六、样式

### `plt.style.use(style)` / `plt.style.available`
切换整体风格主题。`available` 列出所有可用样式（如 `"ggplot"` `"seaborn-v0_8"` `"dark_background"` `"fivethirtyeight"`）。
```python
print(plt.style.available)          # 查看可选样式
plt.style.use("ggplot")             # 应用样式
```

### 颜色 / 线型 / 标记速查
- **颜色**：`"r"` `"g"` `"b"` `"k"` `"w"` `"c"` `"m"` `"y"`，或十六进制 `"#FF0000"`、色名 `"tomato"`。
- **线型**：`"-"` 实线、`"--"` 虚线、`":"` 点线、`"-."` 点划线、`""` 无线。
- **标记**：`"o"` 圆点、`"s"` 方块、`"^"` 三角、`"*"` 星、`"x"` 叉、`"."` 小点。

```python
ax.plot(x, y, color="tomato", linestyle="--", marker="o")
```

### `plt.rcParams` / `plt.rc("font", family=...)` — 中文字体
默认不支持中文，需手动设置字体（macOS 用 `"Arial Unicode MS"` 或 `"PingFang SC"`）。
```python
plt.rcParams["font.sans-serif"] = ["Arial Unicode MS", "PingFang SC"]  # 中文字体
plt.rcParams["axes.unicode_minus"] = False     # 解决负号显示为方框的问题
```

### `plt.xscale` / `plt.yscale`（见第三节）

---

## 七、保存与显示

### `plt.show()`
显示图形（交互窗口中）。
```python
plt.show()
```

### `fig.savefig(fname, dpi=..., bbox_inches="tight")`
保存图片。`dpi` 分辨率、`bbox_inches="tight"` 裁掉多余白边。格式由扩展名决定（png/pdf/svg）。
```python
fig.savefig("plot.png", dpi=150, bbox_inches="tight")
fig.savefig("plot.pdf")            # 矢量图，适合论文
```

### `plt.close(fig)` / `plt.clf()` / `plt.cla()`
`close` 关闭图；`clf` 清空整张图；`cla` 清空当前坐标轴。循环画多图时常用，避免内存堆积。
```python
plt.clf()       # 清空，准备画下一张
plt.close("all")
```

### `ax.imshow(data, cmap=...)` — 显示图像/矩阵
```python
ax.imshow(matrix, cmap="viridis")
plt.colorbar(ax.images[0])     # 加颜色条
```

---

## 八、速查表

| 分类 | 函数 | 一句话作用 |
|------|------|-----------|
| 画布 | `figure` `subplots` | 创建画布 / 画布+子图 |
| 折线 | `plot` | 折线图 |
| 散点 | `scatter` | 散点图 |
| 柱状 | `bar` `barh` | 柱状图 / 水平柱状图 |
| 分布 | `hist` `boxplot` `pie` | 直方图 / 箱线图 / 饼图 |
| 标题 | `set_title` `set_xlabel` `set_ylabel` | 标题 / 轴标签 |
| 范围 | `set_xlim` `set_ylim` `set_xticks` `set_yticks` | 轴范围 / 刻度 |
| 参考线 | `grid` `axhline` `axvline` | 网格 / 水平线 / 垂直线 |
| 标注 | `text` `annotate` | 文字 / 带箭头标注 |
| 图例 | `legend` `twinx` | 图例 / 双 Y 轴 |
| 区域 | `fill_between` `errorbar` | 填充 / 误差棒 |
| 子图 | `subplot` `subplots` `tight_layout` `subplots_adjust` | 子图布局 |
| 样式 | `style.use` `rcParams` | 主题 / 全局设置（含中文字体） |
| 输出 | `show` `savefig` `close` `clf` | 显示 / 保存 / 关闭 / 清空 |

---

## 学习建议

1. **用面向对象写法**：`fig, ax = plt.subplots()` 再 `ax.plot(...)`，比 `plt.plot` 更清晰、更易扩展（尤其画子图时）。
2. **先 `subplots` 后逐个设置**：一张完整的图 = 数据（plot/scatter/bar…）+ 标题 + 轴标签 + 图例 + 保存，缺一不可。
   ```python
   fig, ax = plt.subplots(figsize=(8, 5))
   ax.plot(x, y, label="y")
   ax.set_title("标题")
   ax.set_xlabel("X")
   ax.set_ylabel("Y")
   ax.legend()
   fig.tight_layout()
   fig.savefig("out.png", dpi=150)
   ```
3. **中文乱码两个步骤**：设置 `font.sans-serif` 字体，再关掉 `axes.unicode_minus`（否则负号变方框）。
4. **记不住参数就查**：颜色/线型/标记种类多，用 `help(plt.plot)` 或文档随时查，不必死背。
5. **Seaborn 能少写很多代码**：统计图（如带置信区间的折线、分类箱线图）优先用 Seaborn，它基于 Matplotlib，风格也更好看。
