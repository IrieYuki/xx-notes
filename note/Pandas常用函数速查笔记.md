# Pandas 常用函数速查笔记

> 整理范围：数据分析中最常用的 Pandas 操作，覆盖数据的读取、查看、选择、清洗、变换、分组、合并与统计。
> 每个函数都附有 **语法签名** + **作用说明** + **可运行示例**。
> 约定：`df` 表示 DataFrame，`s` 表示 Series。`import pandas as pd`。

---

## 目录

1. [创建与数据读写](#一创建与数据读写)
2. [数据查看与基本信息](#二数据查看与基本信息)
3. [数据选择与索引](#三数据选择与索引)
4. [数据清洗](#四数据清洗)
5. [数据变换与操作](#五数据变换与操作)
6. [分组聚合](#六分组聚合)
7. [合并与连接](#七合并与连接)
8. [统计与描述](#八统计与描述)
9. [时间序列](#九时间序列)
10. [字符串处理](#十字符串处理)
11. [速查表](#十一速查表)

---

## 一、创建与数据读写

### `pd.Series(data, index=...)` / `pd.DataFrame(data, columns=..., index=...)`
创建一维 Series / 二维 DataFrame。`data` 可为列表、字典、ndarray 等。
```python
import pandas as pd

s = pd.Series([1, 2, 3], index=["a", "b", "c"])   # 一维带标签数组
df = pd.DataFrame({"name": ["Tom", "Jerry"], "age": [18, 20]})
df2 = pd.DataFrame([[1, 2], [3, 4]], columns=["x", "y"])   # 二维数组 + 列名
```

### `pd.read_csv(path, sep=",", encoding="utf-8", index_col=None, ...)`
读取 CSV 文件。`sep` 分隔符、`encoding` 编码、`index_col` 指定索引列、`skiprows` 跳过行、`usecols` 只读某些列。
```python
df = pd.read_csv("data.csv", encoding="utf-8")
df = pd.read_csv("data.tsv", sep="\t")            # 制表符分隔
df = pd.read_csv("data.csv", index_col=0)          # 第 0 列作为行索引
```

### `pd.read_excel(path, sheet_name=0, ...)` / `pd.read_json(path)` / `pd.read_sql(sql, con)`
读取 Excel / JSON / 数据库。`sheet_name` 可为工作表名或序号，传 `None` 读取全部（返回字典）。
```python
df = pd.read_excel("data.xlsx", sheet_name="Sheet1")
dfs = pd.read_excel("data.xlsx", sheet_name=None)   # 所有 sheet → {名字: DataFrame}
```

### `df.to_csv(path, index=False)` / `df.to_excel(path, index=False)`
导出数据。**注意 `index=False` 避免把行索引写进文件**。
```python
df.to_csv("out.csv", index=False, encoding="utf-8")
df.to_excel("out.xlsx", sheet_name="结果", index=False)
```

---

## 二、数据查看与基本信息

### `df.head(n=5)` / `df.tail(n=5)`
查看前 / 后 n 行，快速预览数据。
```python
df.head()       # 前 5 行
df.tail(3)      # 后 3 行
```

### `df.shape` / `df.index` / `df.columns` / `df.values` / `df.dtypes`
`shape` 返回 (行数, 列数) 元组；`index` 行标签；`columns` 列名；`values` 底层 ndarray；`dtypes` 每列数据类型。
```python
df.shape        # (100, 5)
df.dtypes       # 每列的类型
```

### `df.info()` / `df.describe()`
`info` 显示列名、非空数、类型、内存占用；`describe` 生成数值列的统计汇总（count/mean/std/min/四分位/max）。
```python
df.info()
df.describe()                       # 默认只统计数值列
df.describe(include="object")       # 统计字符串列（count/unique/top/freq）
```

### `df.isnull()` / `df.notnull()`
逐元素判断是否缺失（NaN），返回同形状的布尔 DataFrame。常配合 `sum()` 统计缺失数。
```python
df.isnull()               # 布尔表
df.isnull().sum()         # 每列缺失值数量
```

### `df.nunique()` / `df.unique()`（Series 用）
`nunique` 每列不同值数量；`s.unique()` 返回 Series 中所有不重复的值。
```python
df.nunique()              # 每列去重后的数量
df["city"].unique()       # array(['北京', '上海', ...])
```

### `df.value_counts()`（Series 用，或 `df[col].value_counts()`）
统计每个值出现的次数（频数）。
```python
df["city"].value_counts()                 # 每个城市出现次数
df["city"].value_counts(normalize=True)   # 归一化为比例
```

---

## 三、数据选择与索引

### `df[col]` / `df[[col1, col2]]`
选择单列（返回 Series）或多列（返回 DataFrame）。
```python
df["age"]             # 单列 → Series
df[["age", "name"]]   # 多列 → DataFrame
```

### `df.loc[row_label, col_label]`（按标签）
基于**标签**选择。支持切片（两端都含）、列表、布尔条件。
```python
df.loc[0]                    # 第 0 行（标签为 0）
df.loc[0:5]                  # 标签 0 到 5 的行（含 5）
df.loc[:, "age"]             # age 列（所有行）
df.loc[df["age"] > 18, ["name", "age"]]   # 条件 + 指定列
```

### `df.iloc[row_pos, col_pos]`（按位置）
基于**整数位置**选择。切片遵循 Python 左闭右开。
```python
df.iloc[0]           # 第 1 行
df.iloc[0:5]         # 前 5 行（不含位置 5）
df.iloc[:, 1]        # 第 2 列
df.iloc[0, 1]        # 单个元素
```

### `df.at[label, col]` / `df.iat[pos_row, pos_col]`
访问**单个**元素，比 `loc`/`iloc` 更快，仅用于标量读写。
```python
df.at[0, "age"] = 21      # 按标签改单个值
df.iat[0, 1]              # 按位置读单个值
```

### 布尔索引 / `df.query(expr)`
用条件筛选行。`query` 用字符串表达式，写法更简洁。
```python
df[df["age"] > 18]                        # 布尔索引
df[(df["age"] > 18) & (df["city"] == "北京")]   # 多条件用 & |，记得加括号
df.query("age > 18 and city == '北京'")     # query 写法
```

### `df.isin(values)` / `s.between(a, b)`
`isin` 判断元素是否在集合中；`between` 判断是否落在区间内（含端点）。
```python
df[df["city"].isin(["北京", "上海"])]     # 在指定城市中
df[df["age"].between(18, 30)]             # 18 ≤ age ≤ 30
```

---

## 四、数据清洗

### `df.dropna(axis=0, how="any", subset=None, ...)`
删除含缺失值的行/列。`axis=0` 删行、`axis=1` 删列；`how="any"` 有缺失即删、`how="all"` 全缺失才删；`subset` 指定列。
```python
df.dropna()                       # 删除任何含 NaN 的行
df.dropna(how="all")              # 仅删除全为 NaN 的行
df.dropna(subset=["age"])         # 只对 age 列判断
df.dropna(axis=1)                 # 删除含 NaN 的列
```

### `df.fillna(value, method=None, ...)`
填充缺失值。`value` 可为标量、字典（按列填）、或前值 `method="ffill"` / 后值 `"bfill"`。
```python
df.fillna(0)                              # 全部填 0
df.fillna({"age": 0, "name": "未知"})       # 分列填充
df["age"].fillna(df["age"].mean())         # 用均值填充
df.fillna(method="ffill")                  # 用上一行的值填充
```

### `df.drop_duplicates(subset=None, keep="first", ...)`
删除重复行。`subset` 指定判断列，`keep="first"` 保留首个 / `"last"` 保留最后 / `False` 全删。
```python
df.drop_duplicates()                       # 整行去重
df.drop_duplicates(subset=["id"])          # 按 id 去重
df.drop_duplicates(subset=["id"], keep="last")
```

### `df.replace(to_replace, value, ...)`
替换值。支持标量、列表、字典、正则。
```python
df.replace(0, "无")                       # 所有 0 → '无'
df.replace([1, 2], 0)                     # 1 和 2 → 0
df.replace({"A": 1, "B": 2})              # 字典映射
df.replace(r"\s+", "", regex=True)        # 正则去掉空白
```

### `df.astype(dtype)` / `pd.to_numeric(s, errors="coerce")`
`astype` 转换列类型；`to_numeric` 把字符串安全转数字，`errors="coerce"` 遇到非法值填 NaN。
```python
df["age"] = df["age"].astype(int)
df["age"] = pd.to_numeric(df["age"], errors="coerce")   # 非法值变 NaN
```

### `df.rename(columns={...}, index={...}, inplace=False)`
重命名列或行索引。传字典映射。
```python
df.rename(columns={"age": "年龄", "city": "城市"})
df.rename(index={0: "first"})
```

### `df.set_index(col)` / `df.reset_index(drop=False)`
`set_index` 把某列设为行索引；`reset_index` 把索引还原为普通列（`drop=True` 直接丢弃索引）。
```python
df.set_index("id")
df.reset_index(drop=True)
```

---

## 五、数据变换与操作

### `df.sort_values(by, ascending=True, ...)` / `df.sort_index()`
按列值排序 / 按索引排序。`by` 可传列名或列表，`ascending` 可传布尔或列表控制多列升降序。
```python
df.sort_values("age")                          # 升序
df.sort_values("age", ascending=False)         # 降序
df.sort_values(["city", "age"], ascending=[True, False])   # 先按城市升序，再按年龄降序
df.sort_index()
```

### `df.apply(func, axis=0)` / `df.applymap(func)` / `s.map(func_or_dict)`
`apply` 沿行/列应用函数（`axis=0` 列、`axis=1` 行）；`applymap` 逐元素应用（DataFrame 用）；`map` 逐元素映射（Series 用，也支持字典）。
```python
df["age"].map(lambda x: x + 1)                 # Series 逐元素
df["sex"].map({"男": 1, "女": 0})               # 字典映射
df.apply(lambda col: col.max() - col.min())    # 每列的极差
df["总分"] = df.apply(lambda row: row["语文"] + row["数学"], axis=1)   # 行级运算
```

### `pd.cut(x, bins, labels=None)` / `pd.qcut(x, q)`
`cut` 按**数值区间**分箱；`qcut` 按**分位数**分箱（每箱数量大致相同）。
```python
pd.cut(df["age"], bins=[0, 18, 30, 100], labels=["未成年", "青年", "中年"])
pd.qcut(df["age"], q=4)                        # 四等分位
```

### `pd.get_dummies(df, columns=None)` / `pd.concat` 等
独热编码（One-Hot），把分类变量转成 0/1 列。
```python
pd.get_dummies(df, columns=["city"])
```

---

## 六、分组聚合

### `df.groupby(by, ...)`
按某列（或多列）分组，返回 GroupBy 对象，配合聚合函数使用。
```python
df.groupby("city")                 # 分组对象
df.groupby("city")["age"].mean()   # 各城市平均年龄
df.groupby(["city", "sex"]).size() # 各组合的样本数
```

### `groupby.agg(func)` / `groupby.aggregate()`
对分组后的多列做不同聚合。可传函数名、函数、或 `{列: 函数}` 字典。
```python
df.groupby("city").agg({"age": "mean", "salary": "sum"})
df.groupby("city").agg({"age": ["mean", "max"]})        # 一列多个指标
df.groupby("city").agg(平均年龄=("age", "mean"), 人数=("age", "count"))  # 重命名
```

### `groupby.transform(func)` / `groupby.filter(func)`
`transform` 返回与原始数据**同长度**的结果（常用于标准化、填充组均值）；`filter` 按条件筛选整组。
```python
df["组均值"] = df.groupby("city")["age"].transform("mean")   # 每行填所在组的均值
df.groupby("city").filter(lambda g: len(g) > 5)             # 保留人数 >5 的组
```

### `pd.pivot_table(df, index, columns, values, aggfunc="mean", ...)`
透视表：行 `index`、列 `columns`、值 `values`、聚合 `aggfunc`。
```python
pd.pivot_table(df, index="city", columns="sex", values="age", aggfunc="mean")
```

---

## 七、合并与连接

### `pd.concat(objs, axis=0, ignore_index=False, ...)`
沿行（`axis=0`，上下堆叠）或列（`axis=1`，左右拼接）拼接。`ignore_index=True` 重建索引。
```python
pd.concat([df1, df2])                    # 上下拼接
pd.concat([df1, df2], axis=1)            # 左右拼接
pd.concat([df1, df2], ignore_index=True)
```

### `pd.merge(left, right, how="inner", on=None, left_on=None, right_on=None, ...)`
按键合并两张表（类似 SQL JOIN）。`how` 可选 `inner`/`left`/`right`/`outer`；`on` 相同列名；`left_on`/`right_on` 左右键名不同。
```python
pd.merge(df1, df2, on="id")                       # 内连接
pd.merge(df1, df2, on="id", how="left")           # 左连接，保留左表所有行
pd.merge(df1, df2, left_on="user_id", right_on="id")
```

### `df.join(other, on=None, how="left", ...)`
基于**索引**连接（或用 `on` 指定键）。类似 merge 但默认按索引。
```python
df1.join(df2, on="key", how="inner")
```

---

## 八、统计与描述

### `df.mean()` / `df.sum()` / `df.min()` / `df.max()` / `df.median()` / `df.std()` / `df.var()` / `df.count()`
基础统计。默认按列计算（`axis=0`），`axis=1` 按行。`skipna=True` 默认跳过 NaN。
```python
df["age"].mean()        # 均值
df.sum(axis=1)          # 每行的和
df["age"].median()      # 中位数
df["age"].std()         # 标准差
```

### `df.quantile(q=0.5)` / `df.cumsum()` / `df.cumprod()` / `df.pct_change()`
`quantile` 分位数；`cumsum`/`cumprod` 累计和/积；`pct_change` 环比增长率。
```python
df["age"].quantile(0.25)        # 25% 分位数
df["sales"].cumsum()            # 累计求和
df["sales"].pct_change()        # 每行相对上一行的增长率
```

### `df.corr()` / `df.cov()`
相关系数矩阵 / 协方差矩阵（默认 Pearson）。
```python
df.corr()                # 各数值列两两相关
df.corr(method="spearman")
```

### `df.idxmax()` / `df.idxmin()` / `df.nlargest(n, col)` / `df.nsmallest(n, col)`
`idxmax`/`idxmin` 返回最大值/最小值所在的行标签；`nlargest`/`nsmallest` 返回某列最大/最小的 n 行。
```python
df["age"].idxmax()                    # 最大年龄所在的行索引
df.nlargest(3, "age")                 # age 最大的 3 行
```

---

## 九、时间序列

### `pd.to_datetime(arg, format=None, errors="raise", ...)`
把字符串/数字转换为 Datetime 类型。`errors="coerce"` 非法值转 NaT。
```python
df["date"] = pd.to_datetime(df["date"])
df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")   # 指定格式更快
```

### `pd.date_range(start, end, periods=None, freq="D")`
生成连续的时间索引。`freq` 频率：`D` 天、`H` 小时、`M` 月末、`MS` 月初、`W` 周、`Y` 年。
```python
pd.date_range("2024-01-01", periods=10, freq="D")
pd.date_range("2024-01-01", "2024-12-31", freq="MS")   # 每月 1 号
```

### `.dt` 访问器
对 Datetime 列提取年/月/日/周等属性。常用：`year` `month` `day` `weekday` `hour` `date` `dayofweek`。
```python
df["date"].dt.year        # 年份
df["date"].dt.month       # 月份
df["date"].dt.weekday     # 星期几（0=周一）
df["date"].dt.strftime("%Y/%m")   # 自定义格式
```

### `df.resample(rule, on=None).agg(func)` / `df.set_index(col).resample("M")`
按时间频率重采样聚合（需 DatetimeIndex 或指定 `on`）。`rule` 同 `date_range` 的 `freq`。
```python
df.set_index("date").resample("M")["sales"].sum()      # 按月汇总销售额
df.set_index("date").resample("W")["sales"].mean()     # 按周求平均
```

### `df.shift(periods=1)` / `df.rolling(window).mean()`
`shift` 把数据向下/上平移；`rolling` 滑动窗口计算（移动平均等）。
```python
df["上期"] = df["sales"].shift(1)                 # 上一期的值
df["移动平均"] = df["sales"].rolling(7).mean()     # 7 日移动平均
```

---

## 十、字符串处理（`.str` 访问器）

> 对字符串列用 `.str` 访问器，方法大多与 Python 字符串同名。

### `s.str.contains(pat, regex=True)` / `s.str.startswith()` / `s.str.endswith()`
判断是否包含/以…开头/以…结尾，返回布尔 Series。
```python
df[df["name"].str.contains("张")]        # 名字含 "张"
df["name"].str.startswith("A")
```

### `s.str.split(pat, expand=False)` / `s.str.cat()` / `s.str.join()`
`split` 按分隔符拆分（`expand=True` 拆成多列）；`cat` 拼接；`join` 用分隔符连接列表。
```python
df["name"].str.split("_")                         # 拆成列表
df["name"].str.split("_", expand=True)            # 拆成 DataFrame
df["姓"] + df["名"].str.cat(sep="")               # 拼接
```

### `s.str.replace(pat, repl, regex=True)` / `s.str.strip()` / `s.str.lower()` / `s.str.upper()`
替换 / 去空白 / 转小写 / 转大写。
```python
df["name"].str.replace("张", "李")
df["name"].str.strip()
df["name"].str.lower()
```

### `s.str.extract(pat)` / `s.str.len()` / `s.str.isdigit()`
`extract` 用正则捕获组提取子串；`len` 字符串长度；`isdigit` 是否全为数字。
```python
df["name"].str.extract(r"(\d+)")      # 提取数字部分
df["name"].str.len()
```

---

## 十一、速查表

| 分类 | 函数 | 一句话作用 |
|------|------|-----------|
| 创建 | `Series` `DataFrame` | 创建一维 / 二维数据 |
| 读写 | `read_csv` `read_excel` `to_csv` `to_excel` | 读取 / 写出 CSV、Excel |
| 查看 | `head` `tail` `info` `describe` `shape` `dtypes` | 预览与基本信息 |
| 查看 | `isnull` `value_counts` `unique` `nunique` | 缺失 / 频数 / 去重 |
| 选择 | `loc` `iloc` `at` `iat` | 按标签 / 位置选择 |
| 选择 | `query` `isin` `between` | 条件筛选 |
| 清洗 | `dropna` `fillna` `drop_duplicates` `replace` | 缺失 / 去重 / 替换 |
| 清洗 | `astype` `to_numeric` `rename` | 类型转换 / 重命名 |
| 变换 | `sort_values` `apply` `map` `applymap` | 排序 / 逐元素 / 行列应用 |
| 变换 | `cut` `qcut` `get_dummies` | 分箱 / 独热编码 |
| 分组 | `groupby` `agg` `transform` `filter` `pivot_table` | 分组聚合 / 透视 |
| 合并 | `concat` `merge` `join` | 拼接 / 连接 |
| 统计 | `mean` `sum` `min` `max` `median` `std` `quantile` `corr` | 描述统计 |
| 时间 | `to_datetime` `date_range` `resample` `.dt` | 时间转换 / 重采样 |
| 字符串 | `.str.contains` `.str.split` `.str.replace` `.str.extract` | 字符串处理 |

---

## 学习建议

1. **先掌握「选择」三板斧**：`loc`（标签）、`iloc`（位置）、布尔索引，这三者覆盖 80% 的数据筛选场景。
   ```python
   df.loc[df["age"] > 18, ["name", "age"]]     # 最常用的组合：条件 + 选列
   ```
2. **`groupby` + `agg` 是分析核心**：先分组，再聚合，几乎所有的「按…统计…」都能用它表达。
   ```python
   df.groupby("city")["age"].agg(["mean", "max", "count"])
   ```
3. **注意 `axis` 的含义**：`axis=0` 沿行方向操作（即按列计算），`axis=1` 沿列方向（按行计算）。很多报错都源于搞混了它。
4. **链式 vs inplace**：大多数方法默认返回新对象（不修改原数据），要原地修改需传 `inplace=True` 或重新赋值。
5. **养成先 `df.info()` 后 `df.describe()` 的习惯**：动手分析前先看清数据规模、类型和缺失情况，避免后面踩坑。
