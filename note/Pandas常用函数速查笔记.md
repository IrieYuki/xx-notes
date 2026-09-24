# Pandas 常用函数速查笔记

> 收集范围：数据分析里最常用的 Pandas 操作，覆盖创建读写、查看、选择、清洗、变换、分组、合并、统计、时间与字符串。
> 每条都是「**签名 ｜ 返回 ｜ 备注**」三格 + 可直接运行的示例（`#` 后面是**真实输出**）。
> 约定：`df` 是 DataFrame、`s` 是 Series，示例里都写 `import pandas as pd`。
> ⚠️ 版本：本笔记在 **pandas 3.0** 上逐条跑通。与旧版有关的坑都标在条目里（`applymap` 已移除 → 用 `.map()`；`fillna(method=)` 已移除 → `.ffill()`；`freq="M"` 报错 → 月末用 `"ME"`）。
> 📌 另外：pandas 3 打印单个值时会带包装，比如 `np.int64(18)`、`np.float64(99.5)` —— 那就是 18 和 99.5，想拿到普通 Python 数用 `int()` / `float()` / `.item()`。

---

## 索引 · 速查表

| 分类 | 用法（点击跳转） | 一句话作用 |
|------|------------------|-----------|
| A1 创建与读写 | [`pd.Series(data, index)`](#pdseriesdata-index-一维带标签数组) | 一维带标签数组 |
| A1 创建与读写 | [`pd.DataFrame(data, columns)`](#pddataframedata-columns-二维表格最常用的建法) | 二维表格（最常用的建法） |
| A1 创建与读写 | [`pd.read_csv(path, sep, encoding)`](#pdread_csvpath-sep-encoding-读-csv) | 读 CSV |
| A1 创建与读写 | [`pd.read_excel(path, sheet_name)`](#pdread_excelpath-sheet_name-读-excel多-sheet) | 读 Excel（多 sheet） |
| A1 创建与读写 | [`df.to_csv / df.to_excel`](#dfto_csv--dfto_excel-导出数据) | 导出数据 |
| A2 查看与基本信息 | [`df.head(n) / df.tail(n)`](#dfheadn--dftailn-看前--后-n-行) | 看前 / 后 n 行 |
| A2 查看与基本信息 | [`df.shape / index / columns / values / dtypes`](#dfshape--index--columns--values--dtypes-表的体检报告) | 表的「体检报告」 |
| A2 查看与基本信息 | [`df.info()`](#dfinfo-看列名类型非空数内存) | 看列名、类型、非空数、内存 |
| A2 查看与基本信息 | [`df.describe()`](#dfdescribe-数值列的统计汇总) | 数值列的统计汇总 |
| A2 查看与基本信息 | [`df.isnull() / df.notnull()`](#dfisnull--dfnotnull-找缺失值) | 找缺失值 |
| A2 查看与基本信息 | [`df.nunique() / s.unique()`](#dfnunique--sunique-去重后有多少--有哪些值) | 去重后有多少 / 有哪些值 |
| A2 查看与基本信息 | [`s.value_counts()`](#svalue_counts-每个值出现多少次) | 每个值出现多少次 |
| A3 选择与索引 | [`df[col] / df[[col1, col2]]`](#dfcol--dfcol1-col2-选一列--多列) | 选一列 / 多列 |
| A3 选择与索引 | [`df.loc[行标签, 列标签]`](#dfloc行标签-列标签-按标签选) | 按**标签**选 |
| A3 选择与索引 | [`df.iloc[行位置, 列位置]`](#dfiloc行位置-列位置-按整数位置选) | 按**整数位置**选 |
| A3 选择与索引 | [`df.at[label, col] / df.iat[pos, pos]`](#dfatlabel-col--dfiatpos-pos-读写单个元素) | 读写**单个**元素 |
| A3 选择与索引 | [`布尔索引 df[条件]`](#布尔索引-df条件-按条件筛行) | 按条件筛行 |
| A3 选择与索引 | [`df.query(expr)`](#dfqueryexpr-用字符串写条件更清爽) | 用字符串写条件（更清爽） |
| A3 选择与索引 | [`s.isin(values) / s.between(a, b)`](#sisinvalues--sbetweena-b-在集合里--在区间里) | 在集合里 / 在区间里 |
| A4 数据清洗 | [`df.dropna(axis, how, subset)`](#dfdropnaaxis-how-subset-删掉含缺失的行--列) | 删掉含缺失的行 / 列 |
| A4 数据清洗 | [`s.fillna(value) / df.ffill() / bfill()`](#sfillnavalue--dfffill--bfill-填缺失值) | 填缺失值 |
| A4 数据清洗 | [`df.drop_duplicates(subset, keep)`](#dfdrop_duplicatessubset-keep-去重) | 去重 |
| A4 数据清洗 | [`df.replace(to_replace, value)`](#dfreplaceto_replace-value-替换值) | 替换值 |
| A4 数据清洗 | [`astype(dtype) / pd.to_numeric(errors=)`](#astypedtype--pdto_numericerrors-类型转换) | 类型转换 |
| A4 数据清洗 | [`df.rename(columns, index)`](#dfrenamecolumns-index-改列名--行索引名) | 改列名 / 行索引名 |
| A4 数据清洗 | [`df.set_index(col) / df.reset_index(drop)`](#dfset_indexcol--dfreset_indexdrop-把列设为索引--索引还原成列) | 把列设为索引 / 索引还原成列 |
| A5 数据变换 | [`df.sort_values(by, ascending)`](#dfsort_valuesby-ascending-按列值排序) | 按列值排序 |
| A5 数据变换 | [`df.apply(func, axis)`](#dfapplyfunc-axis-按列--按行套函数) | 按列 / 按行套函数 |
| A5 数据变换 | [`s.map(func_or_dict)`](#smapfunc_or_dict-series-逐元素映射) | Series 逐元素映射 |
| A5 数据变换 | [`df.map(func)（逐元素，取代 applymap）`](#dfmapfunc逐元素取代-applymap-dataframe-逐元素映射) | DataFrame 逐元素映射 |
| A5 数据变换 | [`pd.cut(x, bins) / pd.qcut(x, q)`](#pdcutx-bins--pdqcutx-q-数值分箱) | 数值分箱 |
| A5 数据变换 | [`pd.get_dummies(df, columns)`](#pdget_dummiesdf-columns-独热编码one-hot) | 独热编码（One-Hot） |
| A6 分组聚合 | [`df.groupby(by)`](#dfgroupbyby-按列分组) | 按列分组 |
| A6 分组聚合 | [`groupby.agg(func)`](#groupbyaggfunc-分组后做多种聚合) | 分组后做多种聚合 |
| A6 分组聚合 | [`groupby.transform(func) / filter(func)`](#groupbytransformfunc--filterfunc-组内计算后广播--按组筛选) | 组内计算后广播 / 按组筛选 |
| A6 分组聚合 | [`pd.pivot_table(df, index, columns, values)`](#pdpivot_tabledf-index-columns-values-透视表) | 透视表 |
| A7 合并与连接 | [`pd.concat(objs, axis, ignore_index)`](#pdconcatobjs-axis-ignore_index-拼接表) | 拼接表 |
| A7 合并与连接 | [`pd.merge(left, right, how, on)`](#pdmergeleft-right-how-on-按键连表sql-join) | 按键连表（SQL JOIN） |
| A7 合并与连接 | [`df.join(other, how)`](#dfjoinother-how-按索引连表) | 按**索引**连表 |
| A8 统计与描述 | [`df.mean / sum / min / max / median / std / count`](#dfmean--sum--min--max--median--std--count-基础统计默认按列) | 基础统计（默认按列） |
| A8 统计与描述 | [`s.quantile / cumsum / pct_change`](#squantile--cumsum--pct_change-分位数--累计--环比) | 分位数 / 累计 / 环比 |
| A8 统计与描述 | [`df.corr() / df.cov()`](#dfcorr--dfcov-相关系数--协方差矩阵) | 相关系数 / 协方差矩阵 |
| A8 统计与描述 | [`s.idxmax / nlargest / nsmallest`](#sidxmax--nlargest--nsmallest-极值在哪一行--取前-n-行) | 极值在哪一行 / 取前 n 行 |
| A9 时间序列 | [`pd.to_datetime(arg, format, errors)`](#pdto_datetimearg-format-errors-字符串--时间类型) | 字符串 → 时间类型 |
| A9 时间序列 | [`pd.date_range(start, periods, freq)`](#pddate_rangestart-periods-freq-生成时间索引) | 生成时间索引 |
| A9 时间序列 | [`s.dt 访问器`](#sdt-访问器-从时间列取年--月--星期) | 从时间列取年 / 月 / 星期 |
| A9 时间序列 | [`df.resample(rule).agg(func)`](#dfresampleruleaggfunc-按时间频率汇总) | 按时间频率汇总 |
| A9 时间序列 | [`s.shift(periods) / s.rolling(window).mean()`](#sshiftperiods--srollingwindowmean-上期值--滑动平均) | 上期值 / 滑动平均 |
| A10 字符串处理（.str） | [`s.str.contains / startswith / endswith`](#sstrcontains--startswith--endswith-字符串包含--前后缀判断) | 字符串包含 / 前后缀判断 |
| A10 字符串处理（.str） | [`s.str.split(expand=True) / str.cat`](#sstrsplitexpandtrue--strcat-拆分--拼接字符串列) | 拆分 / 拼接字符串列 |
| A10 字符串处理（.str） | [`s.str.replace / strip / lower / upper`](#sstrreplace--strip--lower--upper-清洗文本) | 清洗文本 |
| A10 字符串处理（.str） | [`s.str.extract / str.len / str.isdigit`](#sstrextract--strlen--strisdigit-正则提取--长度--是否数字) | 正则提取 / 长度 / 是否数字 |

---

## A1　创建与读写

### `pd.Series(data, index)` 一维带标签数组

**签名** `pd.Series(data, index=None, dtype=None, name=None)` ｜ **返回** `Series` ｜ **备注** = 一维数组 + 索引

```python
import pandas as pd
pd.Series([1, 2, 3], index=["a", "b", "c"]).to_dict()   # {'a': 1, 'b': 2, 'c': 3}
pd.Series([1, 2, 3]).tolist()                           # [1, 2, 3]
pd.Series({"a": 1, "b": 2}).tolist()                    # [1, 2]
pd.Series([1, 2], name="分数").name                       # '分数'
```

> ⚠️ `Series` 就是「一维数组 + 行标签」，`.values` 拿底层数组、`.index` 拿标签；索引可以重复。

### `pd.DataFrame(data, columns)` 二维表格（最常用的建法）

**签名** `pd.DataFrame(data, columns=None, index=None)` ｜ **返回** `DataFrame` ｜ **备注** dict 的键 = 列名

```python
import pandas as pd
df = pd.DataFrame({"name": ["Tom", "Jerry", "Ann"], "age": [18, 20, 25], "city": ["北京", "上海", "北京"]})
df.shape                                                                # (3, 3)
df.columns.tolist()                                                     # ['name', 'age', 'city']
pd.DataFrame([[1, 2], [3, 4]], columns=["x", "y"]).to_dict("records")   # [{'x': 1, 'y': 2}, {'x': 3, 'y': 4}]
print(df)
#     name  age city
# 0    Tom   18   北京
# 1  Jerry   20   上海
# 2    Ann   25   北京
```

> ⚠️ 用字典建表最直观（键是列名）；每列长度必须一致，否则 `ValueError`。`print(df)` 打印的是**表格**，`df` 单独一行会打印同样的东西（Jupyter 里更好看）。

### `pd.read_csv(path, sep, encoding)` 读 CSV

**签名** `pd.read_csv(filepath, sep=",", encoding="utf-8", index_col=None, usecols=None, nrows=None)` ｜ **返回** `DataFrame` ｜ **备注** 中文乱码先查 encoding

```python
import pandas as pd
df = pd.DataFrame({"name": ["Tom", "Jerry", "Ann"], "age": [18, 20, 25], "city": ["北京", "上海", "北京"]})
df.to_csv("data.csv", index=False, encoding="utf-8")
pd.read_csv("data.csv").shape                                # (3, 3)
pd.read_csv("data.csv", usecols=["name"]).columns.tolist()   # ['name']
pd.read_csv("data.csv", index_col="name").index.tolist()     # ['Tom', 'Jerry', 'Ann']
pd.read_csv("data.csv", nrows=1)["name"].tolist()            # ['Tom']
```

> ⚠️ 乱码换 `encoding="gbk"` 试；大文件用 `usecols` 只读需要的列、`nrows` 先试读几行，或 `chunksize` 分块读。

### `pd.read_excel(path, sheet_name)` 读 Excel（多 sheet）

**签名** `pd.read_excel(io, sheet_name=0)` / `pd.read_json(path)` / `pd.read_sql(sql, con)` ｜ **返回** `DataFrame` / `dict` ｜ **备注** 依赖 openpyxl

```python
import pandas as pd
df = pd.DataFrame({"name": ["Tom", "Jerry", "Ann"], "age": [18, 20, 25], "city": ["北京", "上海", "北京"]})
df.to_excel("data.xlsx", sheet_name="Sheet1", index=False)
pd.read_excel("data.xlsx").shape                             # (3, 3)
type(pd.read_excel("data.xlsx", sheet_name=None)).__name__   # 'dict'
list(pd.read_excel("data.xlsx", sheet_name=None).keys())     # ['Sheet1']
```

> ⚠️ `sheet_name=None` 会返回 `{表名: DataFrame}`，想一次读全部分表就用它；读 Excel 需要装 `openpyxl`（旧版 .xls 用 `xlrd`）。

### `df.to_csv / df.to_excel` 导出数据

**签名** `df.to_csv(path, index=False, encoding="utf-8")` / `df.to_excel(path, index=False)` ｜ **返回** `None`（写文件） ｜ **备注** **别忘 `index=False`**

```python
import pandas as pd
df = pd.DataFrame({"name": ["Tom", "Jerry", "Ann"], "age": [18, 20, 25], "city": ["北京", "上海", "北京"]})
df.to_csv("out.csv", index=False, encoding="utf-8")
open("out.csv", encoding="utf-8").read().splitlines()[0]    # 'name,age,city'
df.to_csv("out2.csv", encoding="utf-8")
open("out2.csv", encoding="utf-8").read().splitlines()[0]   # ',name,age,city'
```

> ⚠️ 不写 `index=False` 会在文件里多出一列行号（0,1,2…），下次读回来又多一列 —— 这是新手最常见的「脏数据」来源。

## A2　查看与基本信息

### `df.head(n) / df.tail(n)` 看前 / 后 n 行

**签名** `df.head(n=5)` / `df.tail(n=5)` ｜ **返回** `DataFrame` ｜ **备注** 默认 5 行，原表不变

```python
import pandas as pd
df = pd.DataFrame({"name": ["Tom", "Jerry", "Ann"], "age": [18, 20, 25], "city": ["北京", "上海", "北京"]})
df.head(2)["name"].tolist()             # ['Tom', 'Jerry']
df.tail(1)["name"].tolist()             # ['Ann']
df.head(2).shape                        # (2, 3)
```

> ⚠️ 拿到任何新数据先 `df.head()` 看一眼长什么样，比直接 `print(df)` 干净（大数据集不会刷屏）。

### `df.shape / index / columns / values / dtypes` 表的「体检报告」

**签名** `df.shape` `df.index` `df.columns` `df.values` `df.dtypes` ｜ **返回** 元组 / Index / ndarray / Series ｜ **备注** 属性不带括号

```python
import pandas as pd
df = pd.DataFrame({"name": ["Tom", "Jerry", "Ann"], "age": [18, 20, 25], "city": ["北京", "上海", "北京"]})
df.shape                                # (3, 3)
df.columns.tolist()                     # ['name', 'age', 'city']
df.index.tolist()                       # [0, 1, 2]
df.values.shape                         # (3, 3)
df.dtypes.astype(str).to_dict()         # {'name': 'str', 'age': 'int64', 'city': 'str'}
```

> ⚠️ `shape` 是 `(行数, 列数)`；`dtypes` 看每列类型（`str` 列不能直接算数）；`values` 转成 ndarray 会**丢掉列名**，一般只在喂给 numpy/sklearn 时用。

### `df.info()` 看列名、类型、非空数、内存

**签名** `df.info(verbose=None, buf=None, memory_usage=None)` ｜ **返回** `None`（打印到屏幕） ｜ **备注** 第一眼先看它

```python
import pandas as pd
df = pd.DataFrame({"name": ["Tom", "Jerry", "Ann"], "age": [18, 20, 25], "city": ["北京", "上海", "北京"]})
df.info()
# <class 'pandas.DataFrame'>
# RangeIndex: 3 entries, 0 to 2
# Data columns (total 3 columns):
#  #   Column  Non-Null Count  Dtype
# ---  ------  --------------  -----
#  0   name    3 non-null      str
#  1   age     3 non-null      int64
#  2   city    3 non-null      str
# dtypes: int64(1), str(2)
# memory usage: 204.0 bytes
```

> ⚠️ `Non-Null Count` 比总行数少就说明那列有缺失；数据大时 `memory_usage` 能提醒你是不是读进来一个巨表。

### `df.describe()` 数值列的统计汇总

**签名** `df.describe(percentiles=None, include=None)` ｜ **返回** `DataFrame` ｜ **备注** 默认只统计**数值列**

```python
import pandas as pd
df = pd.DataFrame({"name": ["Tom", "Jerry", "Ann"], "age": [18, 20, 25], "city": ["北京", "上海", "北京"]})
df2 = pd.DataFrame({"score": [60, 75, 88, 92], "city": ["北京", "上海", "北京", "广州"]})
print(df2.describe().round(2))
#        score
# count   4.00
# mean   78.75
# std    14.45
# min    60.00
# 25%    71.25
# 50%    81.50
# 75%    89.00
# max    92.00
print(df2.describe(include="object"))
#        city
# count     4
# unique    3
# top      北京
# freq      2
```

> ⚠️ 字符串列要 `describe(include="object")` 才统计（给 count/unique/top/freq）；想多看分位就传 `percentiles=[.1, .5, .9]`。

### `df.isnull() / df.notnull()` 找缺失值

**签名** `df.isnull()` / `df.notnull()` / `df.isnull().sum()` ｜ **返回** 布尔 `DataFrame` / `Series` ｜ **备注** `sum` 数缺失数是标准组合

```python
import pandas as pd
df2 = pd.DataFrame({"a": [1.0, None, 3.0], "b": ["x", None, "z"]})
df2.isnull().to_dict()                  # {'a': {0: False, 1: True, 2: False}, 'b': {0: False, 1: True, 2: False}}
df2.isnull().sum().to_dict()            # {'a': 1, 'b': 1}
df2.isnull().any().to_dict()            # {'a': True, 'b': True}
df2.notnull().sum().to_dict()           # {'a': 2, 'b': 2}
```

> ⚠️ `isnull()` 返回同形状的布尔表，`sum()` 按列数缺失个数（布尔当 0/1 相加）；`any()` 看哪列有缺失。这是清洗数据的第一步。

### `df.nunique() / s.unique()` 去重后有多少 / 有哪些值

**签名** `df.nunique(axis=0, dropna=True)` / `s.unique()` / `s.nunique()` ｜ **返回** `Series` / 数组（字符串列是 `StringArray`） ｜ **备注** `unique` 保持原顺序

```python
import pandas as pd
df = pd.DataFrame({"name": ["Tom", "Jerry", "Ann"], "age": [18, 20, 25], "city": ["北京", "上海", "北京"]})
df.nunique().to_dict()                  # {'name': 3, 'age': 3, 'city': 2}
df["city"].unique().tolist()            # ['北京', '上海']
df["city"].nunique()                    # 2
```

> ⚠️ 看「这列是分类变量还是 ID」用它们：唯一值很少 → 分类列（可做 One-Hot）；几乎每行都不同 → ID 列。pandas 3 里字符串列的 `unique()` 返回 `StringArray`（不是 ndarray），`.tolist()` 一样能用。

### `s.value_counts()` 每个值出现多少次

**签名** `s.value_counts(normalize=False, sort=True, dropna=True)` ｜ **返回** `Series`（值=频数，索引=原值） ｜ **备注** 默认降序

```python
import pandas as pd
df = pd.DataFrame({"name": ["Tom", "Jerry", "Ann"], "age": [18, 20, 25], "city": ["北京", "上海", "北京"]})
df["city"].value_counts().to_dict()                          # {'北京': 2, '上海': 1}
df["city"].value_counts(normalize=True).round(3).to_dict()   # {'北京': 0.667, '上海': 0.333}
df["city"].value_counts().index.tolist()                     # ['北京', '上海']
```

> ⚠️ `normalize=True` 给比例；默认**不计 NaN**（要算上就 `dropna=False`）。做「类别分布」时第一选择。

## A3　选择与索引

### `df[col] / df[[col1, col2]]` 选一列 / 多列

**签名** `df[col]` → Series / `df[[col1, col2]]` → DataFrame ｜ **返回** `Series` / `DataFrame` ｜ **备注** 注意单列和多列返回类型不同

```python
import pandas as pd
df = pd.DataFrame({"name": ["Tom", "Jerry", "Ann"], "age": [18, 20, 25], "city": ["北京", "上海", "北京"]})
df["age"].tolist()                      # [18, 20, 25]
type(df["age"]).__name__                # 'Series'
df[["name", "age"]].shape               # (3, 2)
type(df[["name", "age"]]).__name__      # 'DataFrame'
```

> ⚠️ 单列 → `Series`，多列 → `DataFrame`（要写成列表 `[[...]]`）。`df[0]` 不是「第 0 列」，会 `KeyError` —— 取位置用 `iloc`。

### `df.loc[行标签, 列标签]` 按**标签**选

**签名** `df.loc[row_label, col_label]` ｜ **返回** `Series` / `DataFrame` / 标量 ｜ **备注** 切片**两端都含**

```python
import pandas as pd
df = pd.DataFrame({"name": ["Tom", "Jerry", "Ann"], "age": [18, 20, 25], "city": ["北京", "上海", "北京"]})
df.loc[0, "name"]                                            # 'Tom'
df.loc[0:1, "name"].tolist()                                 # ['Tom', 'Jerry']
df.loc[:, "age"].tolist()                                    # [18, 20, 25]
df.loc[df["age"] > 18, ["name", "age"]].to_dict("records")   # [{'name': 'Jerry', 'age': 20}, {'name': 'Ann', 'age': 25}]
```

> ⚠️ `loc` 的行切片**包含终点**（和 Python 列表切片不同）；最后一个例子是**最常用的一句**：条件 + 选列。标签不存在会 `KeyError`。

### `df.iloc[行位置, 列位置]` 按**整数位置**选

**签名** `df.iloc[row_pos, col_pos]` ｜ **返回** `Series` / `DataFrame` / 标量 ｜ **备注** 切片左闭右开

```python
import pandas as pd
df = pd.DataFrame({"name": ["Tom", "Jerry", "Ann"], "age": [18, 20, 25], "city": ["北京", "上海", "北京"]})
df.iloc[0, 0]                           # 'Tom'
df.iloc[0:2, 0].tolist()                # ['Tom', 'Jerry']
df.iloc[:, 1].tolist()                  # [18, 20, 25]
df.iloc[-1, -1]                         # '北京'
```

> ⚠️ `iloc` 只认位置、切片左闭右开（和 `loc` 相反，最容易记混）；`df.iloc[-1]` 取最后一行。

### `df.at[label, col] / df.iat[pos, pos]` 读写**单个**元素

**签名** `df.at[row_label, col_label]` / `df.iat[row_pos, col_pos]` ｜ **返回** 标量 ｜ **备注** 比 loc/iloc 快，但只能取一个

```python
import pandas as pd
df = pd.DataFrame({"name": ["Tom", "Jerry", "Ann"], "age": [18, 20, 25], "city": ["北京", "上海", "北京"]})
df.iat[0, 1]                            # np.int64(18)
d = df.copy()
d.at[0, "age"] = 21
d.at[0, "age"]                          # np.int64(21)
df.at[0, "age"]                         # np.int64(18)
```

> ⚠️ 循环里逐个改单元格用 `at`/`iat`（比 `loc` 快）；注意 `d = df.copy()` 再改才是改副本，直接 `df.at[...] = x` 会改到原表。pandas 3 打印出来的 `np.int64(21)` 就是 21，要普通 Python 数用 `int(...)` / `.item()`。

### `布尔索引 df[条件]` 按条件筛行

**签名** `df[df[col] > x]`  /  多条件 `df[(A) & (B)]` ｜ **返回** `DataFrame` ｜ **备注** 多条件必须 `&` `|` 并加括号

```python
import pandas as pd
df = pd.DataFrame({"name": ["Tom", "Jerry", "Ann"], "age": [18, 20, 25], "city": ["北京", "上海", "北京"]})
df[df["age"] > 18]["name"].tolist()                            # ['Jerry', 'Ann']
df[(df["age"] > 18) & (df["city"] == "北京")]["name"].tolist()   # ['Ann']
df[df["age"] > 12].shape                                       # (3, 3)
```

> ⚠️ 写 `df[(df.a > 1) and (df.b > 2)]` 会报 `ValueError`（`and` 不能逐元素比较），要用 `&`；每个条件都要带括号，否则运算符优先级会出错。

### `df.query(expr)` 用字符串写条件（更清爽）

**签名** `df.query(expr, inplace=False)` ｜ **返回** `DataFrame` ｜ **备注** 引用外部变量要加 `@`

```python
import pandas as pd
df = pd.DataFrame({"name": ["Tom", "Jerry", "Ann"], "age": [18, 20, 25], "city": ["北京", "上海", "北京"]})
df.query("age > 18")["name"].tolist()                    # ['Jerry', 'Ann']
df.query("age > 18 and city == '北京'")["name"].tolist()   # ['Ann']
n = 19
df.query("age > @n")["name"].tolist()                    # ['Jerry', 'Ann']
```

> ⚠️ 列名有空格或中文时用反引号：``df.query("`列 名` > 1")``；外部的 Python 变量要写成 `@变量名`。条件复杂时比一堆 `&` 好读。

### `s.isin(values) / s.between(a, b)` 在集合里 / 在区间里

**签名** `s.isin(values)` / `s.between(left, right, inclusive="both")` ｜ **返回** 布尔 `Series` ｜ **备注** `between` 两端都含

```python
import pandas as pd
df = pd.DataFrame({"name": ["Tom", "Jerry", "Ann"], "age": [18, 20, 25], "city": ["北京", "上海", "北京"]})
df[df["city"].isin(["北京", "上海"])]["name"].tolist()   # ['Tom', 'Jerry', 'Ann']
df[df["age"].between(18, 20)]["name"].tolist()       # ['Tom', 'Jerry']
df["city"].isin(["北京"]).tolist()                     # [True, False, True]
```

> ⚠️ `isin` 里可以传列表 / 集合 / Series；`between(18, 20)` 表示 `18 <= x <= 20`（含两端），只要一端就自己写比较。

## A4　数据清洗

### `df.dropna(axis, how, subset)` 删掉含缺失的行 / 列

**签名** `df.dropna(axis=0, how="any", subset=None, inplace=False)` ｜ **返回** `DataFrame`（新对象） ｜ **备注** 默认 `how="any"`

```python
import pandas as pd
df2 = pd.DataFrame({"a": [1.0, None, 3.0], "b": ["x", None, None]})
df2.dropna().shape                      # (1, 2)
df2.dropna(how="all").shape             # (2, 2)
df2.dropna(subset=["a"]).shape          # (2, 2)
df2.dropna(axis=1).shape                # (3, 0)
```

> ⚠️ `axis=0` 删行、`axis=1` 删列；`how="any"` 有一个缺失就删、`"all"` 全缺失才删；`subset` 只针对指定列判断。**默认返回新表**，想改原表要重新赋值。

### `s.fillna(value) / df.ffill() / bfill()` 填缺失值

**签名** `s.fillna(value)`  /  `df.ffill()`  /  `df.bfill()` ｜ **返回** `Series` / `DataFrame` ｜ **备注** pandas 3 已移除 `fillna(method=)`

```python
import pandas as pd
s = pd.Series([1.0, None, 3.0])
s.fillna(0).tolist()                    # [1.0, 0.0, 3.0]
s.fillna(s.mean()).tolist()             # [1.0, 2.0, 3.0]
s.ffill().tolist()                      # [1.0, 1.0, 3.0]
s.bfill().tolist()                      # [1.0, 3.0, 3.0]
```

> ⚠️ **`fillna(method="ffill")` 在 pandas 3.0 会报 `TypeError`**，改成 `.ffill()` / `.bfill()`。用均值/中位数填充要小心：会低估方差，缺失比例高时先想清楚业务含义。

### `df.drop_duplicates(subset, keep)` 去重

**签名** `df.drop_duplicates(subset=None, keep="first", inplace=False)` ｜ **返回** `DataFrame` ｜ **备注** `keep=False` 把重复的全删

```python
import pandas as pd
dd = pd.DataFrame({"id": [1, 1, 2], "v": [9, 8, 7]})
dd.drop_duplicates(subset=["id"])["v"].tolist()                # [9, 7]
dd.drop_duplicates(subset=["id"], keep="last")["v"].tolist()   # [8, 7]
dd.drop_duplicates(subset=["id"], keep=False).shape            # (1, 2)
```

> ⚠️ `subset` 指定「按哪些列判断重复」（不写就是整行完全相同才算重复）。顺序敏感：`keep="first"` 保留先出现的。

### `df.replace(to_replace, value)` 替换值

**签名** `df.replace(to_replace, value, regex=False, inplace=False)` ｜ **返回** `DataFrame` ｜ **备注** 正则要显式 `regex=True`

```python
import pandas as pd
r = pd.DataFrame({"a": [0, 1, 2], "b": ["A", "B", "C"]})
r.replace(0, 9)['a'].tolist()                                         # [9, 1, 2]
r.replace([1, 2], 0)['a'].tolist()                                    # [0, 0, 0]
r.replace({"A": "甲"})["b"].tolist()                                   # ['甲', 'B', 'C']
pd.Series([" a ", "b  c"]).replace(r"\s+", "", regex=True).tolist()   # ['a', 'bc']
```

> ⚠️ 默认是**精确/子串**替换；用正则必须 `regex=True`。`replace` 既能改一类值（`[1,2] → 0`）也能按字典映射（`{"A": "甲"}`）。

### `astype(dtype) / pd.to_numeric(errors=)` 类型转换

**签名** `s.astype(dtype)`  /  `pd.to_numeric(s, errors="coerce")` ｜ **返回** `Series` / `DataFrame` ｜ **备注** 脏数据先用 to_numeric

```python
import pandas as pd
t = pd.Series(["18", "x", "25"])
pd.to_numeric(t, errors="coerce").tolist()         # [18.0, nan, 25.0]
pd.to_numeric(t, errors="coerce").isnull().sum()   # np.int64(1)
pd.Series(["18", "25"]).astype(int).tolist()       # [18, 25]
```

> ⚠️ `astype(int)` 遇到 `"x"` 会直接报错；清洗数据先用 `pd.to_numeric(..., errors="coerce")` 把非法值变成 `NaN`，再决定删还是填。`errors="ignore"` 已被移除。

### `df.rename(columns, index)` 改列名 / 行索引名

**签名** `df.rename(columns={...}, index={...}, inplace=False)` ｜ **返回** `DataFrame` ｜ **备注** 改列名比重新赋值 `df.columns` 安全

```python
import pandas as pd
df = pd.DataFrame({"name": ["Tom", "Jerry", "Ann"], "age": [18, 20, 25], "city": ["北京", "上海", "北京"]})
df.rename(columns={"age": "年龄"}).columns.tolist()   # ['name', '年龄', 'city']
df.rename(index={0: "第一行"}).index.tolist()          # ['第一行', 1, 2]
df.columns.tolist()                                 # ['name', 'age', 'city']
```

> ⚠️ 传字典只改列出的名字，其余不动（比 `df.columns = [...]` 安全，后者列数不对就报错）；`inplace=True` 会改原表。

### `df.set_index(col) / df.reset_index(drop)` 把列设为索引 / 索引还原成列

**签名** `df.set_index(keys, drop=True)`  /  `df.reset_index(drop=False)` ｜ **返回** `DataFrame` ｜ **备注** `drop=True` 直接丢弃索引

```python
import pandas as pd
df = pd.DataFrame({"name": ["Tom", "Jerry", "Ann"], "age": [18, 20, 25], "city": ["北京", "上海", "北京"]})
df.set_index("name").index.tolist()                   # ['Tom', 'Jerry', 'Ann']
df.set_index("name").columns.tolist()                 # ['age', 'city']
df.set_index("name").reset_index().columns.tolist()   # ['name', 'age', 'city']
df.reset_index(drop=True).index.tolist()              # [0, 1, 2]
```

> ⚠️ `set_index` 之后那一列**不再出现在 columns** 里（默认 drop=True）；`reset_index(drop=True)` 是「丢掉旧索引」而不是把它变回列。时间序列重采样前常要 `set_index(时间列)`。

## A5　数据变换

### `df.sort_values(by, ascending)` 按列值排序

**签名** `df.sort_values(by, ascending=True, na_position="last", inplace=False)` ｜ **返回** `DataFrame` ｜ **备注** 不动原表

```python
import pandas as pd
df = pd.DataFrame({"name": ["Tom", "Jerry", "Ann"], "age": [18, 20, 25], "city": ["北京", "上海", "北京"]})
df.sort_values("age", ascending=False)["name"].tolist()                     # ['Ann', 'Jerry', 'Tom']
df.sort_values(["city", "age"], ascending=[True, False])["name"].tolist()   # ['Jerry', 'Ann', 'Tom']
df.sort_index(ascending=False).index.tolist()                               # [2, 1, 0]
```

> ⚠️ `by` 传列表就是多列排序，`ascending` 传列表可分别控制升降序；`sort_index()` 是按**索引**排（不是按值）。NaN 默认排最后。

### `df.apply(func, axis)` 按列 / 按行套函数

**签名** `df.apply(func, axis=0)` ｜ **返回** `Series` / `DataFrame` ｜ **备注** `axis=0` 按列、`axis=1` 按行

```python
import pandas as pd
df = pd.DataFrame({"name": ["Tom", "Jerry", "Ann"], "age": [18, 20, 25], "city": ["北京", "上海", "北京"]})
num = df[["age"]]
num.apply(lambda c: c.max() - c.min()).to_dict()        # {'age': 7}
df.apply(lambda row: row["age"] * 2, axis=1).tolist()   # [36, 40, 50]
num.apply(lambda c: c.sum()).to_dict()                  # {'age': 63}
```

> ⚠️ `apply` 比向量化慢，能用列运算（`df["a"] * 2`）就别用它；`axis=1` 才是「一行一行地算」（要访问多个列时必须用它）。

### `s.map(func_or_dict)` Series 逐元素映射

**签名** `s.map(arg, na_action=None)` ｜ **返回** `Series` ｜ **备注** 字典里没有的值 → `NaN`

```python
import pandas as pd
df = pd.DataFrame({"name": ["Tom", "Jerry", "Ann"], "age": [18, 20, 25], "city": ["北京", "上海", "北京"]})
df["city"].map({"北京": 1, "上海": 0}).tolist()   # [1, 0, 1]
df["age"].map(lambda x: x + 1).tolist()       # [19, 21, 26]
```

> ⚠️ 字典映射时**没匹配到的会变成 `NaN`**（不报错），想保留原值要 `.map(d).fillna(df["city"])`。这是做标签编码的常用手段。

### `df.map(func)（逐元素，取代 applymap）` DataFrame 逐元素映射

**签名** `df.map(func, na_action=None)` ｜ **返回** `DataFrame` ｜ **备注** **pandas 3 已移除 `applymap`**

```python
import pandas as pd
df = pd.DataFrame({"name": ["Tom", "Jerry", "Ann"], "age": [18, 20, 25], "city": ["北京", "上海", "北京"]})
df[["age"]].map(lambda x: x * 2).to_dict()   # {'age': {0: 36, 1: 40, 2: 50}}
df[["age"]].map(lambda x: x + 1).shape       # (3, 1)
```

> ⚠️ 老代码里的 `df.applymap(f)` 在 pandas 3.0 **已经不存在**，改成 `df.map(f)`。注意 `Series.map` 和 `DataFrame.map` 同名但不同物：前者逐元素、后者也逐元素，只是作用在整表上。

### `pd.cut(x, bins) / pd.qcut(x, q)` 数值分箱

**签名** `pd.cut(x, bins, labels=None)`  /  `pd.qcut(x, q, labels=None)` ｜ **返回** `Series`（category） ｜ **备注** cut 按区间、qcut 按分位

```python
import pandas as pd
age = pd.Series([15, 22, 40])
pd.cut(age, bins=[0, 18, 30, 100], labels=["未成年", "青年", "中年"]).tolist()   # ['未成年', '青年', '中年']
pd.cut(age, bins=3).astype(str).tolist()                                  # ['(14.975, 23.333]', '(14.975, 23.333]', '(31.667, 40.0]']
pd.qcut(pd.Series([1, 2, 3, 4]), q=2).astype(str).tolist()                # ['(0.999, 2.5]', '(0.999, 2.5]', '(2.5, 4.0]', '(2.5, 4.0]']
```

> ⚠️ `cut` 你自己给边界（等距或指定），`qcut` 按分位数切（每个箱里数量近似相等）；结果列是 `category`，想当字符串要 `.astype(str)`。

### `pd.get_dummies(df, columns)` 独热编码（One-Hot）

**签名** `pd.get_dummies(df, columns=None, drop_first=False)` ｜ **返回** `DataFrame` ｜ **备注** 分类变量 → 0/1 列

```python
import pandas as pd
df = pd.DataFrame({"name": ["Tom", "Jerry", "Ann"], "age": [18, 20, 25], "city": ["北京", "上海", "北京"]})
pd.get_dummies(df, columns=["city"]).columns.tolist()   # ['name', 'age', 'city_上海', 'city_北京']
pd.get_dummies(df, columns=["city"]).shape              # (3, 4)
pd.get_dummies(df, columns=["city"]).iloc[0].tolist()   # ['Tom', np.int64(18), np.False_, np.True_]
```

> ⚠️ 喂给机器学习前把分类列转成 0/1；训练集和测试集**必须对齐列**（用同一个 `categories` 或之后 `reindex`），否则特征数对不上。`drop_first=True` 可避免共线性。

## A6　分组聚合

### `df.groupby(by)` 按列分组

**签名** `df.groupby(by, as_index=True, dropna=True)` ｜ **返回** `GroupBy` 对象 ｜ **备注** 必须接聚合函数才有结果

```python
import pandas as pd
df = pd.DataFrame({"name": ["Tom", "Jerry", "Ann"], "age": [18, 20, 25], "city": ["北京", "上海", "北京"]})
df.groupby("city")["age"].mean().round(2).to_dict()                 # {'上海': 20.0, '北京': 21.5}
df.groupby("city").size().to_dict()                                 # {'上海': 1, '北京': 2}
df.groupby("city", as_index=False)["age"].mean().columns.tolist()   # ['city', 'age']
```

> ⚠️ 分组列默认变成**索引**；想让它留在列里就 `as_index=False` 或 `.reset_index()`。`groupby` 本身不是结果，后面必须跟聚合（mean/sum/size…）。

### `groupby.agg(func)` 分组后做多种聚合

**签名** `groupby.agg(func_or_dict, **named_aggs)` ｜ **返回** `DataFrame` / `Series` ｜ **备注** 一列多指标 → 多级列名

```python
import pandas as pd
df = pd.DataFrame({"name": ["Tom", "Jerry", "Ann"], "age": [18, 20, 25], "city": ["北京", "上海", "北京"]})
df.groupby("city")["age"].agg(["mean", "max", "count"]).round(2).to_dict()    # {'mean': {'上海': 20.0, '北京': 21.5}, 'max': {'上海': 20, '北京': 25}, 'count': {'上海': 1, '北京': 2}}
df.groupby("city").agg({"age": "mean"}).round(2).to_dict()                    # {'age': {'上海': 20.0, '北京': 21.5}}
df.groupby("city").agg(平均年龄=("age", "mean"), 人数=("age", "count")).to_dict()   # {'平均年龄': {'上海': 20.0, '北京': 21.5}, '人数': {'上海': 1, '北京': 2}}
```

> ⚠️ **命名聚合**（`新列名=("原列", "函数")`）最推荐：结果列名直接就是你要的名字。`agg(["mean","max"])` 会得到多级列名，取值要写 `df[("age", "mean")]`。

### `groupby.transform(func) / filter(func)` 组内计算后广播 / 按组筛选

**签名** `groupby.transform(func)`  /  `groupby.filter(func)` ｜ **返回** 同长度的 `DataFrame` / 筛过的 `DataFrame` ｜ **备注** transform 保持行数

```python
import pandas as pd
df = pd.DataFrame({"name": ["Tom", "Jerry", "Ann"], "age": [18, 20, 25], "city": ["北京", "上海", "北京"]})
df["组均值"] = df.groupby("city")["age"].transform("mean")
df["组均值"].tolist()                                                 # [21.5, 20.0, 21.5]
df.groupby("city").filter(lambda g: len(g) > 1)["name"].tolist()   # ['Tom', 'Ann']
df.groupby("city")["age"].transform("max").tolist()                # [25, 20, 25]
```

> ⚠️ `transform` 返回**和原表一样长**的结果，所以能直接 `df["新列"] = ...`（常用于「减组均值」做标准化）；`filter` 返回筛选后的行（整组保留或整组丢掉）。

### `pd.pivot_table(df, index, columns, values)` 透视表

**签名** `pd.pivot_table(df, index, columns=None, values=None, aggfunc="mean", fill_value=None)` ｜ **返回** `DataFrame` ｜ **备注** 默认 aggfunc="mean"

```python
import pandas as pd
df = pd.DataFrame({"name": ["Tom", "Jerry", "Ann"], "age": [18, 20, 25], "city": ["北京", "上海", "北京"]})
pd.pivot_table(df, index="city", values="age", aggfunc="mean").round(2).to_dict()                   # {'age': {'上海': 20.0, '北京': 21.5}}
pd.pivot_table(df, index="city", columns="name", values="age", aggfunc="max", fill_value=0).shape   # (2, 3)
```

> ⚠️ 行 = `index`、列 = `columns`、值 = `values`；没有数据的格子默认填 `NaN`（`fill_value=0` 可改）。比 `groupby` 多的是「把某个分类铺成列」。

## A7　合并与连接

### `pd.concat(objs, axis, ignore_index)` 拼接表

**签名** `pd.concat(objs, axis=0, ignore_index=False, join="outer")` ｜ **返回** `DataFrame` ｜ **备注** 按**列名**对齐

```python
import pandas as pd
a1 = pd.DataFrame({"a": [1]})
a2 = pd.DataFrame({"a": [2]})
pd.concat([a1, a2], ignore_index=True)["a"].tolist()                   # [1, 2]
pd.concat([a1, a2]).index.tolist()                                     # [0, 0]
pd.concat([a1, pd.DataFrame({"b": [9]})], axis=1).to_dict("records")   # [{'a': 1, 'b': 9}]
```

> ⚠️ `axis=0` 上下堆叠、`axis=1` 左右拼接；不写 `ignore_index=True` 索引会重复（0,0）。列名不一致的列会补 `NaN` —— 这是拼完发现一堆缺失的原因。

### `pd.merge(left, right, how, on)` 按键连表（SQL JOIN）

**签名** `pd.merge(left, right, how="inner", on=None, left_on=None, right_on=None)` ｜ **返回** `DataFrame` ｜ **备注** 默认 `how="inner"`

```python
import pandas as pd
L = pd.DataFrame({"id": [1, 2], "a": [9, 8]})
R = pd.DataFrame({"id": [1, 3], "b": [7, 6]})
pd.merge(L, R, on="id").to_dict("records")               # [{'id': 1, 'a': 9, 'b': 7}]
pd.merge(L, R, on="id", how="left").to_dict("records")   # [{'id': 1, 'a': 9, 'b': 7.0}, {'id': 2, 'a': 8, 'b': nan}]
pd.merge(L, R, on="id", how="outer").shape               # (3, 3)
pd.merge(L, R, left_on="id", right_on="id").shape        # (1, 3)
```

> ⚠️ 默认 `inner`（只留两边都有的键）最容易「莫名少数据」；想保留主表全部行用 `how="left"`（匹配不上补 NaN）。键名不同用 `left_on`/`right_on`。

### `df.join(other, how)` 按**索引**连表

**签名** `df.join(other, on=None, how="left", lsuffix="", rsuffix="")` ｜ **返回** `DataFrame` ｜ **备注** 默认按索引

```python
import pandas as pd
J1 = pd.DataFrame({"a": [1]}, index=[1])
J2 = pd.DataFrame({"b": [2]}, index=[1])
J1.join(J2).to_dict("records")                                                # [{'a': 1, 'b': 2}]
J1.join(pd.DataFrame({"b": [2]}, index=[9]), how="left").to_dict("records")   # [{'a': 1, 'b': nan}]
```

> ⚠️ `join` 默认按**索引**对齐（不是按列）；列名相同时要 `lsuffix`/`rsuffix` 区分。键在普通列上就先用 `set_index` 或直接 `merge`。

## A8　统计与描述

### `df.mean / sum / min / max / median / std / count` 基础统计（默认按列）

**签名** `df.mean(axis=0, skipna=True)` 等同族方法 ｜ **返回** `Series`（每列一个数） ｜ **备注** 默认跳过 NaN

```python
import pandas as pd
df = pd.DataFrame({"name": ["Tom", "Jerry", "Ann"], "age": [18, 20, 25], "city": ["北京", "上海", "北京"]})
num = df[["age"]]
num.mean().round(2).to_dict()           # {'age': 21.0}
num.sum().to_dict()                     # {'age': 63}
num.max().to_dict()                     # {'age': 25}
num.median().to_dict()                  # {'age': 20.0}
num.std().round(2).to_dict()            # {'age': 3.61}
num.count().to_dict()                   # {'age': 3}
```

> ⚠️ 默认 `axis=0`（对每列算一个数）；`skipna=True` 会跳过 NaN（默认），想「有 NaN 就返回 NaN」传 `skipna=False`。**pandas 3.0 起对含字符串列的表直接 `df.mean()` 会 `TypeError`**（旧版是自动忽略并给警告），只算数值列用 `df.select_dtypes("number")`。

### `s.quantile / cumsum / pct_change` 分位数 / 累计 / 环比

**签名** `s.quantile(q=0.5)`  /  `s.cumsum()`  /  `s.pct_change(periods=1)` ｜ **返回** `Series` / `float` ｜ **备注** pct_change 首行是 NaN

```python
import pandas as pd
sales = pd.Series([100, 110, 99])
sales.quantile(0.25)                    # np.float64(99.5)
sales.cumsum().tolist()                 # [100, 210, 309]
sales.pct_change().round(4).tolist()    # [nan, 0.1, -0.1]
sales.diff().tolist()                   # [nan, 10.0, -11.0]
```

> ⚠️ `pct_change()` 是「相对上一期的变化率」（第一期必为 NaN）；`quantile(0.5)` 就是中位数，`quantile(0.9)` 常用于看尾部。

### `df.corr() / df.cov()` 相关系数 / 协方差矩阵

**签名** `df.corr(method="pearson", numeric_only=False)`  / `df.cov()` ｜ **返回** `DataFrame`（方阵） ｜ **备注** 含字符串列要传 `numeric_only=True`

```python
import pandas as pd
c = pd.DataFrame({"x": [1, 2, 3], "y": [2, 4, 6]})
c.corr().round(3).to_dict()                        # {'x': {'x': 1.0, 'y': 1.0}, 'y': {'x': 1.0, 'y': 1.0}}
c.corr(method="spearman").round(3).to_dict()       # {'x': {'x': 1.0, 'y': 1.0}, 'y': {'x': 1.0, 'y': 1.0}}
c.cov().round(3).to_dict()                         # {'x': {'x': 1.0, 'y': 2.0}, 'y': {'x': 2.0, 'y': 4.0}}
mixed = pd.DataFrame({"age": [18, 20, 25], "city": ["北京", "上海", "北京"]})
mixed.corr(numeric_only=True).round(3).to_dict()   # {'age': {'age': 1.0}}
mixed.select_dtypes("number").columns.tolist()     # ['age']
```

> ⚠️ **pandas 3.0 起，表里有字符串列直接 `df.corr()` 会报 `ValueError`**（旧版是自动忽略），必须传 `numeric_only=True`；只取数值列的办法是先 `df.select_dtypes("number")`。`pearson` 看线性关系、`spearman` 看单调关系（抗离群）；**相关不等于因果**。

### `s.idxmax / nlargest / nsmallest` 极值在哪一行 / 取前 n 行

**签名** `s.idxmax()`  /  `df.nlargest(n, columns)`  /  `df.nsmallest(n, columns)` ｜ **返回** 索引标签 / `DataFrame` ｜ **备注** `idxmax` 返回索引标签

```python
import pandas as pd
df = pd.DataFrame({"name": ["Tom", "Jerry", "Ann"], "age": [18, 20, 25], "city": ["北京", "上海", "北京"]})
df["age"].idxmax()                        # 2
df["age"].idxmin()                        # 0
df.nlargest(2, "age")["name"].tolist()    # ['Ann', 'Jerry']
df.nsmallest(1, "age")["name"].tolist()   # ['Tom']
```

> ⚠️ `idxmax()` 返回的是**行索引标签**（不是位置，也不是数值）；并列时只给第一个。`nlargest(n, col)` 比 `sort_values().head(n)` 快，取排行榜用它。

## A9　时间序列

### `pd.to_datetime(arg, format, errors)` 字符串 → 时间类型

**签名** `pd.to_datetime(arg, format=None, errors="raise")` ｜ **返回** `Series` / `Timestamp` ｜ **备注** 脏值用 `errors="coerce"`

```python
import pandas as pd
pd.to_datetime(pd.Series(["2024-01-01", "2024-02-01"])).dt.month.tolist()         # [1, 2]
pd.to_datetime(pd.Series(["2024-01-01", "坏值"]), errors="coerce").isnull().sum()   # np.int64(1)
pd.to_datetime("2024-01-01").year                                                 # 2024
```

> ⚠️ 指定 `format="%Y-%m-%d"` 更快也更不容易猜错；`errors="coerce"` 把认不出的变成 `NaT`（不报错）——**注意别悄悄丢数据**，转换后先看有多少 NaT。

### `pd.date_range(start, periods, freq)` 生成时间索引

**签名** `pd.date_range(start=None, end=None, periods=None, freq="D")` ｜ **返回** `DatetimeIndex` ｜ **备注** **月末是 `"ME"` 不是 `"M"`**

```python
import pandas as pd
pd.date_range("2024-01-01", periods=3, freq="D").strftime("%Y-%m-%d").tolist()       # ['2024-01-01', '2024-01-02', '2024-01-03']
pd.date_range("2024-01-01", periods=3, freq="ME").strftime("%Y-%m-%d").tolist()      # ['2024-01-31', '2024-02-29', '2024-03-31']
pd.date_range("2024-01-01", periods=3, freq="MS").strftime("%Y-%m-%d").tolist()      # ['2024-01-01', '2024-02-01', '2024-03-01']
pd.date_range("2024-01-01", "2024-01-05", freq="2D").strftime("%Y-%m-%d").tolist()   # ['2024-01-01', '2024-01-03', '2024-01-05']
```

> ⚠️ **pandas 3.0 起 `freq="M"` 会报 `ValueError`**：月末用 `"ME"`、月初用 `"MS"`、年末 `"YE"`、年初 `"YS"`；常用还有 `D`（天）、`W`（周）、`h`（小时）。

### `s.dt 访问器` 从时间列取年 / 月 / 星期

**签名** `s.dt.year` / `s.dt.month` / `s.dt.day` / `s.dt.weekday` / `s.dt.strftime(...)` ｜ **返回** `Series` ｜ **备注** 列必须是 datetime 类型

```python
import pandas as pd
d = pd.to_datetime(pd.Series(["2024-03-05", "2024-04-06"]))
d.dt.year.tolist()                      # [2024, 2024]
d.dt.month.tolist()                     # [3, 4]
d.dt.day.tolist()                       # [5, 6]
d.dt.weekday.tolist()                   # [1, 5]
d.dt.strftime("%Y/%m").tolist()         # ['2024/03', '2024/04']
```

> ⚠️ 字符串列没有 `.dt`，要先 `pd.to_datetime`；`weekday` 是 **0=周一**、6=周日（和 `dayofweek` 一样），`day_name()` 直接给星期名。

### `df.resample(rule).agg(func)` 按时间频率汇总

**签名** `df.resample(rule, on=None).agg(func)` ｜ **返回** `Resampler` → 聚合后 `DataFrame` ｜ **备注** 需要 DatetimeIndex

```python
import pandas as pd
ts = pd.DataFrame({"sales": [10, 20, 30]}, index=pd.date_range("2024-01-01", periods=3, freq="D"))
ts.resample("ME")["sales"].sum().tolist()            # [60]
ts.resample("2D")["sales"].sum().tolist()            # [30, 30]
ts.resample("W")["sales"].mean().round(2).tolist()   # [20.0]
```

> ⚠️ 核心是「先有 DatetimeIndex」（`set_index(时间列)` 或传 `on="时间列"`），再按频率聚合；规则同 `date_range`（月末 `"ME"`）。等价于「按时间段 groupby」。

### `s.shift(periods) / s.rolling(window).mean()` 上期值 / 滑动平均

**签名** `s.shift(periods=1)`  /  `s.rolling(window, min_periods=None).mean()` ｜ **返回** `Series` ｜ **备注** 都会产生 NaN

```python
import pandas as pd
sh = pd.Series([10, 20, 30, 40])
sh.shift(1).tolist()                           # [nan, 10.0, 20.0, 30.0]
sh.shift(-1).tolist()                          # [20.0, 30.0, 40.0, nan]
sh.rolling(2).mean().tolist()                  # [nan, 15.0, 25.0, 35.0]
sh.rolling(2, min_periods=1).mean().tolist()   # [10.0, 15.0, 25.0, 35.0]
```

> ⚠️ `shift(1)` 是「取上一期的值」（首行 NaN）；`rolling(2).mean()` 前 1 个值是 NaN，想让结果不全空就 `min_periods=1`。做同比/环比、移动平均必用。

## A10　字符串处理（.str）

### `s.str.contains / startswith / endswith` 字符串包含 / 前后缀判断

**签名** `s.str.contains(pat, regex=True, na=None)`  /  `s.str.startswith(pat)`  /  `s.str.endswith(pat)` ｜ **返回** 布尔 `Series` ｜ **备注** 默认**按正则**匹配

```python
import pandas as pd
names = pd.Series(["张三", "李四", "Alice"])
names.str.contains("张").tolist()                # [True, False, False]
names.str.startswith("A").tolist()              # [False, False, True]
names.str.endswith("四").tolist()                # [False, True, False]
names.str.contains("张", regex=False).tolist()   # [True, False, False]
```

> ⚠️ `contains` 默认 `regex=True`：要找字面量里的 `.`、`*`、`(` 等符号必须加 `regex=False`，否则会被当正则；结果里 NaN 仍然是 NaN（不是 False），做筛选前先 `fillna(False)`。

### `s.str.split(expand=True) / str.cat` 拆分 / 拼接字符串列

**签名** `s.str.split(pat, expand=False)`  /  `s1.str.cat(s2, sep=None)`  /  `s.str.join(sep)` ｜ **返回** `Series` / `DataFrame` / `str` ｜ **备注** `expand=True` 直接拆成多列

```python
import pandas as pd
full = pd.Series(["张_三", "李_四"])
full.str.split("_").tolist()                                   # [['张', '三'], ['李', '四']]
full.str.split("_", expand=True).shape                         # (2, 2)
full.str.split("_", expand=True)[0].tolist()                   # ['张', '李']
pd.Series(["张"]).str.cat(pd.Series(["三"]), sep="-").tolist()   # ['张-三']
```

> ⚠️ `expand=True` 直接拆成多个列（列名是 0,1,2…，之后再 `rename`）；`str.cat` 默认不插分隔符，要 `sep=`。只想拆出第一段可以用 `str.extract`。

### `s.str.replace / strip / lower / upper` 清洗文本

**签名** `s.str.replace(pat, repl, regex=False)`  /  `s.str.strip()`  /  `s.str.lower()`  /  `s.str.upper()` ｜ **返回** `Series` ｜ **备注** 默认按**字面**替换

```python
import pandas as pd
txt = pd.Series([" Tom ", "JERRY"])
txt.str.strip().tolist()                           # ['Tom', 'JERRY']
txt.str.lower().tolist()                           # [' tom ', 'jerry']
txt.str.upper().tolist()                           # [' TOM ', 'JERRY']
pd.Series(["张 三"]).str.replace(" ", "").tolist()   # ['张三']
```

> ⚠️ `.str.replace` 默认 `regex=False`（和 Python 的 `str.replace` 一致）；要正则得显式 `regex=True`。去掉多余空格是数据清洗第一步，配合 `.str.strip()` 用。

### `s.str.extract / str.len / str.isdigit` 正则提取 / 长度 / 是否数字

**签名** `s.str.extract(pat, expand=True)`  /  `s.str.len()`  /  `s.str.isdigit()` ｜ **返回** `DataFrame`（extract） / `Series` ｜ **备注** extract 的括号 = 捕获组

```python
import pandas as pd
mix = pd.Series(["订单A123", "订单B456"])
mix.str.extract(r"(\d+)")[0].tolist()            # ['123', '456']
mix.str.len().tolist()                           # [6, 6]
pd.Series(["12", "ab"]).str.isdigit().tolist()   # [True, False]
mix.str.extract(r"([A-Z])(\d+)")[1].tolist()     # ['123', '456']
```

> ⚠️ `extract` 只提取**第一个**捕获组（多组就成了多列）；没匹配到的行是 NaN。`str.len()` 数的是**字符数**（中文算 1 个），`isdigit()` 判「全是数字」（`"1.5"`、`"-1"` 都是 False）。

## 学习建议

1. **先掌握「选择」三板斧**：`df[条件]`（布尔索引）、`df.loc`（按标签）、`df.iloc`（按位置）—— 覆盖 80% 的筛选场景。
2. **`groupby` + `agg` 是分析核心**：几乎所有「按……统计……」都能用 `df.groupby("列").agg(...)` 表达。
3. **分清 `axis`**：`axis=0` 沿行方向（对每**列**算），`axis=1` 沿列方向（对每**行**算）；默认 `axis=0`。
4. **方法几乎都返回新对象**：想改原表要重新赋值（`df = df.dropna()`），或该版本仍支持的 `inplace=True`。
5. **动手前先 `df.info()` 再 `df.describe()`**：先看清规模、类型、缺失，再决定怎么清洗。
6. **看列类型**：字符串列不能直接算数（会 `TypeError`），先 `pd.to_numeric(..., errors="coerce")` 或 `astype`。
