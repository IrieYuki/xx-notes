# Pandas 常用函数速查笔记

> 收集范围：数据分析里最常用的 Pandas 操作，覆盖创建读写、查看、选择、清洗、变换、分组、合并、统计、时间与字符串。
> 每条都是「**解析｜操作｜提醒**」三段：解析=干什么 + 参数表 + 返回，操作=可直接复制运行的示例（`#` 后面是**真实输出**），提醒=要点和易错点。
> 约定：`df` 是 DataFrame、`s` 是 Series，示例里都写 `import pandas as pd`。
> ⚠️ 版本：本笔记在 **pandas 3.0.3** 上逐条跑通。与旧版有关的坑都标在条目里（`applymap` 已移除 → 用 `.map()`；`fillna(method=)` 已移除 → `.ffill()`；`freq="M"` 报错 → 月末用 `"ME"`）。
> 📌 另外：pandas 3 打印单个值时会带包装，比如 `np.int64(18)`、`np.float64(99.5)` —— 那就是 18 和 99.5，想拿到普通 Python 数用 `int()` / `float()` / `.item()`。

## 怎么用这份文件

- **忘了就来查**：点「索引 · 速查表」里的链接直接跳到条目，不用从头读。
- **顺序按日常使用频率排**：A1 创建与读写 → A2 查看与基本信息 → A3 选择与索引 → A4 数据清洗 → A5 数据变换 → A6 分组聚合 → A7 合并与连接 → A8 统计与描述 → A9 时间序列 → A10 字符串处理（.str）。
- **示例可直接复制运行**：每段示例开头都写好了 `import pandas as pd`，`#` 后是真实输出。
- **允许重复**：相近的用法可能出现在多个分类里（比如统计方法散在 A2/A6/A8），这是故意的——读者从索引直接跳，重复省去来回翻页。

---

## 索引 · 速查表

| 分类 | 用法（点击跳转） | 一句话作用 |
|------|------------------|-----------|
| A1 创建与读写 | [`pd.Series(data, index)`](#pdseriesdata-index-一维带标签数组) | 一维带标签数组 |
| A1 创建与读写 | [`pd.DataFrame(data, columns)`](#pddataframedata-columns-二维表格最常用的建法) | 二维表格（最常用的建法） |
| A1 创建与读写 | [`pd.read_csv(path, sep, encoding)`](#pdread_csvpath-sep-encoding-读-csv) | 读 CSV |
| A1 创建与读写 | [`pd.read_excel(path, sheet_name)`](#pdread_excelpath-sheet_name-读-excel多-sheet) | 读 Excel（多 sheet） |
| A1 创建与读写 | [`df.to_csv、df.to_excel`](#dfto_csvdfto_excel-导出数据) | 导出数据 |
| A2 查看与基本信息 | [`df.head(n)、df.tail(n)`](#dfheadndftailn-看前后-n-行) | 看前、后 n 行 |
| A2 查看与基本信息 | [`df.shape、df.index、df.columns、df.values、df.dtypes`](#dfshapedfindexdfcolumnsdfvaluesdfdtypes-表的体检报告) | 表的「体检报告」 |
| A2 查看与基本信息 | [`df.info()`](#dfinfo-看列名类型非空数内存) | 看列名、类型、非空数、内存 |
| A2 查看与基本信息 | [`df.describe()`](#dfdescribe-数值列的统计汇总) | 数值列的统计汇总 |
| A2 查看与基本信息 | [`df.isnull()、df.notnull()`](#dfisnulldfnotnull-找缺失值) | 找缺失值 |
| A2 查看与基本信息 | [`df.nunique()、s.unique()`](#dfnuniquesunique-去重后有多少有哪些值) | 去重后有多少、有哪些值 |
| A2 查看与基本信息 | [`s.value_counts()`](#svalue_counts-每个值出现多少次) | 每个值出现多少次 |
| A3 选择与索引 | [`df[col]、df[[col1, col2]]`](#dfcoldfcol1-col2-选一列多列) | 选一列、多列 |
| A3 选择与索引 | [`df.loc[行标签, 列标签]`](#dfloc行标签-列标签-按标签选) | 按标签选 |
| A3 选择与索引 | [`df.iloc[行位置, 列位置]`](#dfiloc行位置-列位置-按整数位置选) | 按整数位置选 |
| A3 选择与索引 | [`df.at[label, col]、df.iat[pos, pos]`](#dfatlabel-coldfiatpos-pos-读写单个元素) | 读写单个元素 |
| A3 选择与索引 | [`布尔索引 df[条件]`](#布尔索引-df条件-按条件筛行) | 按条件筛行 |
| A3 选择与索引 | [`df.query(expr)`](#dfqueryexpr-用字符串写条件更清爽) | 用字符串写条件（更清爽） |
| A3 选择与索引 | [`s.isin(values)、s.between(a, b)`](#sisinvaluessbetweena-b-在集合里在区间里) | 在集合里、在区间里 |
| A4 数据清洗 | [`df.dropna(axis, how, subset)`](#dfdropnaaxis-how-subset-删掉含缺失的行列) | 删掉含缺失的行、列 |
| A4 数据清洗 | [`s.fillna(value)、df.ffill()、df.bfill()`](#sfillnavaluedfffilldfbfill-填缺失值) | 填缺失值 |
| A4 数据清洗 | [`df.drop_duplicates(subset, keep)`](#dfdrop_duplicatessubset-keep-去重) | 去重 |
| A4 数据清洗 | [`df.replace(to_replace, value)`](#dfreplaceto_replace-value-替换值) | 替换值 |
| A4 数据清洗 | [`s.astype(dtype)、pd.to_numeric(errors=)`](#sastypedtypepdto_numericerrors-类型转换) | 类型转换 |
| A4 数据清洗 | [`df.rename(columns, index)`](#dfrenamecolumns-index-改列名行索引名) | 改列名、行索引名 |
| A4 数据清洗 | [`df.set_index(col)、df.reset_index(drop)`](#dfset_indexcoldfreset_indexdrop-把列设为索引索引还原成列) | 把列设为索引、索引还原成列 |
| A5 数据变换 | [`df.sort_values(by, ascending)`](#dfsort_valuesby-ascending-按列值排序) | 按列值排序 |
| A5 数据变换 | [`df.apply(func, axis)`](#dfapplyfunc-axis-按列按行套函数) | 按列、按行套函数 |
| A5 数据变换 | [`s.map(func_or_dict)`](#smapfunc_or_dict-series-逐元素映射) | Series 逐元素映射 |
| A5 数据变换 | [`df.map(func)（逐元素，取代 applymap）`](#dfmapfunc逐元素取代-applymap-dataframe-逐元素映射) | DataFrame 逐元素映射 |
| A5 数据变换 | [`pd.cut(x, bins)、pd.qcut(x, q)`](#pdcutx-binspdqcutx-q-数值分箱) | 数值分箱 |
| A5 数据变换 | [`pd.get_dummies(df, columns)`](#pdget_dummiesdf-columns-独热编码one-hot) | 独热编码（One-Hot） |
| A6 分组聚合 | [`df.groupby(by)`](#dfgroupbyby-按列分组) | 按列分组 |
| A6 分组聚合 | [`groupby.agg(func)`](#groupbyaggfunc-分组后做多种聚合) | 分组后做多种聚合 |
| A6 分组聚合 | [`groupby.transform(func)、groupby.filter(func)`](#groupbytransformfuncgroupbyfilterfunc-组内计算后广播按组筛选) | 组内计算后广播、按组筛选 |
| A6 分组聚合 | [`pd.pivot_table(df, index, columns, values)`](#pdpivot_tabledf-index-columns-values-透视表) | 透视表 |
| A7 合并与连接 | [`pd.concat(objs, axis, ignore_index)`](#pdconcatobjs-axis-ignore_index-拼接表) | 拼接表 |
| A7 合并与连接 | [`pd.merge(left, right, how, on)`](#pdmergeleft-right-how-on-按键连表sql-join) | 按键连表（SQL JOIN） |
| A7 合并与连接 | [`df.join(other, how)`](#dfjoinother-how-按索引连表) | 按索引连表 |
| A8 统计与描述 | [`df.mean、df.sum、df.min、df.max、df.median、df.std、df.count`](#dfmeandfsumdfmindfmaxdfmediandfstddfcount-基础统计默认按列) | 基础统计（默认按列） |
| A8 统计与描述 | [`s.quantile、s.cumsum、s.pct_change`](#squantilescumsumspct_change-分位数累计环比) | 分位数、累计、环比 |
| A8 统计与描述 | [`df.corr()、df.cov()`](#dfcorrdfcov-相关系数协方差矩阵) | 相关系数、协方差矩阵 |
| A8 统计与描述 | [`s.idxmax、df.nlargest、df.nsmallest`](#sidxmaxdfnlargestdfnsmallest-极值在哪一行取前-n-行) | 极值在哪一行、取前 n 行 |
| A9 时间序列 | [`pd.to_datetime(arg, format, errors)`](#pdto_datetimearg-format-errors-字符串时间类型) | 字符串→时间类型 |
| A9 时间序列 | [`pd.date_range(start, periods, freq)`](#pddate_rangestart-periods-freq-生成时间索引) | 生成时间索引 |
| A9 时间序列 | [`s.dt 访问器`](#sdt-访问器-从时间列取年月星期) | 从时间列取年、月、星期 |
| A9 时间序列 | [`df.resample(rule).agg(func)`](#dfresampleruleaggfunc-按时间频率汇总) | 按时间频率汇总 |
| A9 时间序列 | [`s.shift(periods)、s.rolling(window).mean()`](#sshiftperiodssrollingwindowmean-上期值滑动平均) | 上期值、滑动平均 |
| A10 字符串处理（.str） | [`s.str.contains、s.str.startswith、s.str.endswith`](#sstrcontainssstrstartswithsstrendswith-字符串包含前后缀判断) | 字符串包含、前后缀判断 |
| A10 字符串处理（.str） | [`s.str.split(expand=True)、s.str.cat`](#sstrsplitexpandtruesstrcat-拆分拼接字符串列) | 拆分、拼接字符串列 |
| A10 字符串处理（.str） | [`s.str.replace、s.str.strip、s.str.lower、s.str.upper`](#sstrreplacesstrstripsstrlowersstrupper-清洗文本) | 清洗文本 |
| A10 字符串处理（.str） | [`s.str.extract、s.str.len、s.str.isdigit`](#sstrextractsstrlensstrisdigit-正则提取长度是否数字) | 正则提取、长度、是否数字 |

---

## A1 创建与读写

### `pd.Series(data, index)` 一维带标签数组

**解析**　把一组数据变成带行标签的一维数组，每行有个名字。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| data | 必填 | 要装进 Series 的数据：列表、元组、字典都可以 |
| index | None | 行标签；长度要和数据一致，不写就是 0,1,2… |
| dtype | None | 元素类型，不写自动推断 |
| name | None | 给这列起个名字 |

返回：`Series`（一维数组 + 行标签）

**操作**

```python
import pandas as pd

pd.Series([1, 2, 3], index=["a", "b", "c"]).to_dict()   # {'a': 1, 'b': 2, 'c': 3}

pd.Series([1, 2, 3]).tolist()                           # [1, 2, 3]

pd.Series({"a": 1, "b": 2}).tolist()                    # [1, 2]

pd.Series([1, 2], name="分数").name                       # '分数'
```

> ⚠️ `Series` 就是「一维数组 + 行标签」：`.values` 拿底层数组、`.index` 拿标签；索引可以重复。

### `pd.DataFrame(data, columns)` 二维表格（最常用的建法）

**解析**　把数据变成二维表格；用字典建最直观，键就是列名。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| data | 必填 | 字典（键=列名）或二维列表、数组 |
| columns | None | 列名列表；用字典建时键就是列名，可不写 |
| index | None | 行标签，不写就是 0,1,2… |

返回：`DataFrame`（二维表格）

**操作**

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

**解析**　把 CSV 文件读成表格。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| path | 必填 | CSV 文件路径 |
| sep | "," | 列分隔符（有些文件用 ; 或制表符） |
| encoding | "utf-8" | 文件编码，中文乱码换 "gbk" 试 |
| index_col | None | 用哪一列当行索引 |
| usecols | None | 只读哪些列（大文件省内存） |
| nrows | None | 只读前几行（先试读） |

返回：`DataFrame`

**操作**

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

**解析**　把 Excel 文件读成表格；一个文件多个 sheet 也能一次读完。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| path | 必填 | Excel 文件路径 |
| sheet_name | 0 | 表名或第几张表；None 表示读全部表（返回字典） |

返回：`DataFrame`；`sheet_name=None` 时是 `{表名: DataFrame}` 字典

**操作**

```python
import pandas as pd

df = pd.DataFrame({"name": ["Tom", "Jerry", "Ann"], "age": [18, 20, 25], "city": ["北京", "上海", "北京"]})

df.to_excel("data.xlsx", sheet_name="Sheet1", index=False)

pd.read_excel("data.xlsx").shape                             # (3, 3)

type(pd.read_excel("data.xlsx", sheet_name=None)).__name__   # 'dict'

list(pd.read_excel("data.xlsx", sheet_name=None).keys())     # ['Sheet1']
```

> ⚠️ `sheet_name=None` 会返回 `{表名: DataFrame}`，想一次读全部分表就用它；读 Excel 需要装 `openpyxl`（旧版 .xls 用 `xlrd`）。读 JSON 用 `pd.read_json(path)`、读数据库用 `pd.read_sql(sql, con)`。

### `df.to_csv、df.to_excel` 导出数据

**解析**　把表导出成 CSV 或 Excel 文件。

返回：`None`（表写进文件）

**操作**

```python
import pandas as pd

df = pd.DataFrame({"name": ["Tom", "Jerry", "Ann"], "age": [18, 20, 25], "city": ["北京", "上海", "北京"]})

df.to_csv("out.csv", index=False, encoding="utf-8")

open("out.csv", encoding="utf-8").read().splitlines()[0]    # 'name,age,city'

df.to_csv("out2.csv", encoding="utf-8")

open("out2.csv", encoding="utf-8").read().splitlines()[0]   # ',name,age,city'
```

> ⚠️ 不写 `index=False` 会在文件里多出一列行号（0,1,2…），下次读回来又多一列 —— 这是新手最常见的「脏数据」来源。

## A2 查看与基本信息

### `df.head(n)、df.tail(n)` 看前、后 n 行

**解析**　看表的前几行或后几行，不写参数默认 5 行。

返回：`DataFrame`（原表不变）

**操作**

```python
import pandas as pd

df = pd.DataFrame({"name": ["Tom", "Jerry", "Ann"], "age": [18, 20, 25], "city": ["北京", "上海", "北京"]})

df.head(2)["name"].tolist()             # ['Tom', 'Jerry']

df.tail(1)["name"].tolist()             # ['Ann']

df.head(2).shape                        # (2, 3)
```

> ⚠️ 拿到任何新数据先 `df.head()` 看一眼长什么样，比直接 `print(df)` 干净（大数据集不会刷屏）。

### `df.shape、df.index、df.columns、df.values、df.dtypes` 表的「体检报告」

**解析**　一口气看表的行数×列数、行标签、列名、底层数据、每列类型。

返回：元组（shape）／`Index`／ndarray／`Series`（都是属性，不带括号）

**操作**

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

**解析**　把表的列名、类型、非空数量、内存用量打印出来，拿到数据第一眼看它。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| verbose | None | True 时显示全部列（列多时默认折叠） |
| buf | None | 把信息写进文件而不是打印到屏幕 |

返回：`None`（信息打印到屏幕）

**操作**

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

**解析**　一键出数值列的统计汇总：个数、均值、标准差、最值、分位数。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| percentiles | None | 想看更多分位就传列表，如 [.1, .5, .9] |
| include | None | 默认只统计数值列；字符串列写 "object" |

返回：`DataFrame`（每列的 count/mean/std/min/分位/max）

**操作**

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

### `df.isnull()、df.notnull()` 找缺失值

**解析**　找出表里哪些位置是缺失值；isnull 缺失=True，notnull 相反。

返回：和原表同形状的布尔 `DataFrame`；`.sum()` 后是每列缺失数的 `Series`

**操作**

```python
import pandas as pd

df2 = pd.DataFrame({"a": [1.0, None, 3.0], "b": ["x", None, "z"]})

df2.isnull().to_dict()                  # {'a': {0: False, 1: True, 2: False}, 'b': {0: False, 1: True, 2: False}}

df2.isnull().sum().to_dict()            # {'a': 1, 'b': 1}

df2.isnull().any().to_dict()            # {'a': True, 'b': True}

df2.notnull().sum().to_dict()           # {'a': 2, 'b': 2}
```

> ⚠️ `isnull()` 返回同形状的布尔表，`sum()` 按列数缺失个数（布尔当 0/1 相加）；`any()` 看哪列有缺失。这是清洗数据的第一步。`isnull().sum()` 是数缺失的标准组合。

### `df.nunique()、s.unique()` 去重后有多少、有哪些值

**解析**　nunique 数每列去重后有几个不同值；unique 列出这列有哪些值。

返回：`Series`（每列去重个数）／数组（字符串列是 `StringArray`，保持原顺序）

**操作**

```python
import pandas as pd

df = pd.DataFrame({"name": ["Tom", "Jerry", "Ann"], "age": [18, 20, 25], "city": ["北京", "上海", "北京"]})

df.nunique().to_dict()                  # {'name': 3, 'age': 3, 'city': 2}

df["city"].unique().tolist()            # ['北京', '上海']

df["city"].nunique()                    # 2
```

> ⚠️ 看「这列是分类变量还是 ID」用它们：唯一值很少 → 分类列（可做 One-Hot）；几乎每行都不同 → ID 列。pandas 3 里字符串列的 `unique()` 返回 `StringArray`（不是 ndarray），`.tolist()` 一样能用。

### `s.value_counts()` 每个值出现多少次

**解析**　数一列里每个值出现多少次，看类别分布。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| normalize | False | True 时返回比例（加起来=1） |
| sort | True | 按频数降序（默认） |
| dropna | True | False 时 NaN 也算一种值 |

返回：`Series`（索引=原值，值=出现次数，默认降序）

**操作**

```python
import pandas as pd

df = pd.DataFrame({"name": ["Tom", "Jerry", "Ann"], "age": [18, 20, 25], "city": ["北京", "上海", "北京"]})

df["city"].value_counts().to_dict()                          # {'北京': 2, '上海': 1}

df["city"].value_counts(normalize=True).round(3).to_dict()   # {'北京': 0.667, '上海': 0.333}

df["city"].value_counts().index.tolist()                     # ['北京', '上海']
```

> ⚠️ `normalize=True` 给比例；默认**不计 NaN**（要算上就 `dropna=False`）。做「类别分布」时第一选择。

## A3 选择与索引

### `df[col]、df[[col1, col2]]` 选一列、多列

**解析**　从表里挑出一列（得到 Series）或多列（双层中括号，得到 DataFrame）。

返回：`Series`（单列）／`DataFrame`（多列）

**操作**

```python
import pandas as pd

df = pd.DataFrame({"name": ["Tom", "Jerry", "Ann"], "age": [18, 20, 25], "city": ["北京", "上海", "北京"]})

df["age"].tolist()                      # [18, 20, 25]

type(df["age"]).__name__                # 'Series'

df[["name", "age"]].shape               # (3, 2)

type(df[["name", "age"]]).__name__      # 'DataFrame'
```

> ⚠️ 单列 → `Series`，多列 → `DataFrame`（要写成列表 `[[...]]`）。`df[0]` 不是「第 0 列」，会 `KeyError` —— 取位置用 `iloc`。

### `df.loc[行标签, 列标签]` 按标签选

**解析**　按标签（行名、列名）选数据；条件 + 选列最常用。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| 行标签 | 必填 | 行的标签，切片时两端都含 |
| 列标签 | 必填 | 列的标签，用 : 表示全部 |

返回：标量／`Series`／`DataFrame`（按选的行列数而定）

**操作**

```python
import pandas as pd

df = pd.DataFrame({"name": ["Tom", "Jerry", "Ann"], "age": [18, 20, 25], "city": ["北京", "上海", "北京"]})

df.loc[0, "name"]                                            # 'Tom'

df.loc[0:1, "name"].tolist()                                 # ['Tom', 'Jerry']

df.loc[:, "age"].tolist()                                    # [18, 20, 25]

df.loc[df["age"] > 18, ["name", "age"]].to_dict("records")   # [{'name': 'Jerry', 'age': 20}, {'name': 'Ann', 'age': 25}]
```

> ⚠️ `loc` 的行切片**包含终点**（和 Python 列表切片不同）；最后一个例子是**最常用的一句**：条件 + 选列。标签不存在会 `KeyError`。

### `df.iloc[行位置, 列位置]` 按整数位置选

**解析**　按整数位置（第几行第几列）选数据，不管标签是什么。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| 行位置 | 必填 | 行的整数位置（从 0 数，-1 表示最后一行） |
| 列位置 | 必填 | 列的整数位置；切片左闭右开 |

返回：标量／`Series`／`DataFrame`

**操作**

```python
import pandas as pd

df = pd.DataFrame({"name": ["Tom", "Jerry", "Ann"], "age": [18, 20, 25], "city": ["北京", "上海", "北京"]})

df.iloc[0, 0]                           # 'Tom'

df.iloc[0:2, 0].tolist()                # ['Tom', 'Jerry']

df.iloc[:, 1].tolist()                  # [18, 20, 25]

df.iloc[-1, -1]                         # '北京'
```

> ⚠️ `iloc` 只认位置、切片左闭右开（和 `loc` 相反，最容易记混）；`df.iloc[-1]` 取最后一行。

### `df.at[label, col]、df.iat[pos, pos]` 读写单个元素

**解析**　读写某一个单元格：at 按标签、iat 按位置，比 loc/iloc 快。

返回：标量（单个值，可读可写）

**操作**

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

**解析**　用条件筛行，返回条件为 True 的那些行。

返回：`DataFrame`（满足条件的行）

**操作**

```python
import pandas as pd

df = pd.DataFrame({"name": ["Tom", "Jerry", "Ann"], "age": [18, 20, 25], "city": ["北京", "上海", "北京"]})

df[df["age"] > 18]["name"].tolist()                            # ['Jerry', 'Ann']

df[(df["age"] > 18) & (df["city"] == "北京")]["name"].tolist()   # ['Ann']

df[df["age"] > 12].shape                                       # (3, 3)
```

> ⚠️ 写 `df[(df.a > 1) and (df.b > 2)]` 会报 `ValueError`（`and` 不能逐元素比较），要用 `&`；每个条件都要带括号，否则运算符优先级会出错。

### `df.query(expr)` 用字符串写条件（更清爽）

**解析**　把筛选条件写成字符串，列名直接写、外部变量加 @。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| expr | 必填 | 条件字符串，直接写列名，如 "age > 18" |
| inplace | False | True 时直接筛原表（一般不用） |

返回：`DataFrame`（满足条件的行）

**操作**

```python
import pandas as pd

df = pd.DataFrame({"name": ["Tom", "Jerry", "Ann"], "age": [18, 20, 25], "city": ["北京", "上海", "北京"]})

df.query("age > 18")["name"].tolist()                    # ['Jerry', 'Ann']

df.query("age > 18 and city == '北京'")["name"].tolist()   # ['Ann']

n = 19

df.query("age > @n")["name"].tolist()                    # ['Jerry', 'Ann']
```

> ⚠️ 列名有空格或中文时用反引号：``df.query("`列 名` > 1")``；外部的 Python 变量要写成 `@变量名`。条件复杂时比一堆 `&` 好读。

### `s.isin(values)、s.between(a, b)` 在集合里、在区间里

**解析**　判断每个值在不在给定的集合里（isin），或在不在区间内（between）。

返回：布尔 `Series`

**操作**

```python
import pandas as pd

df = pd.DataFrame({"name": ["Tom", "Jerry", "Ann"], "age": [18, 20, 25], "city": ["北京", "上海", "北京"]})

df[df["city"].isin(["北京", "上海"])]["name"].tolist()   # ['Tom', 'Jerry', 'Ann']

df[df["age"].between(18, 20)]["name"].tolist()       # ['Tom', 'Jerry']

df["city"].isin(["北京"]).tolist()                     # [True, False, True]
```

> ⚠️ `isin` 里可以传列表 / 集合 / Series；`between(18, 20)` 表示 `18 <= x <= 20`（含两端），只要一端就自己写比较。

## A4 数据清洗

### `df.dropna(axis, how, subset)` 删掉含缺失的行、列

**解析**　把含有缺失值的行或列删掉，怎么算「含缺失」由 how 决定。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| axis | 0 | 0=删行、1=删列 |
| how | "any" | any=有一个缺失就删、all=全缺失才删 |
| subset | None | 只针对这些列判断缺失 |

返回：`DataFrame`（新对象，原表不变）

**操作**

```python
import pandas as pd

df2 = pd.DataFrame({"a": [1.0, None, 3.0], "b": ["x", None, None]})

df2.dropna().shape                      # (1, 2)

df2.dropna(how="all").shape             # (2, 2)

df2.dropna(subset=["a"]).shape          # (2, 2)

df2.dropna(axis=1).shape                # (3, 0)
```

> ⚠️ `axis=0` 删行、`axis=1` 删列；`how="any"` 有一个缺失就删、`"all"` 全缺失才删；`subset` 只针对指定列判断。**默认返回新表**，想改原表要重新赋值。

### `s.fillna(value)、df.ffill()、df.bfill()` 填缺失值

**解析**　填缺失值：fillna 填成指定值（或均值），ffill 用上一行填、bfill 用下一行填。

返回：`Series`／`DataFrame`

**操作**

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

**解析**　删掉重复行，按 subset 指定的列判断「重不重」。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| subset | None | 按哪些列判断重复；不写=整行完全相同才算 |
| keep | "first" | 保留哪一条：first=先出现、last=后出现、False=全删 |

返回：`DataFrame`（去重后）

**操作**

```python
import pandas as pd

dd = pd.DataFrame({"id": [1, 1, 2], "v": [9, 8, 7]})

dd.drop_duplicates(subset=["id"])["v"].tolist()                # [9, 7]

dd.drop_duplicates(subset=["id"], keep="last")["v"].tolist()   # [8, 7]

dd.drop_duplicates(subset=["id"], keep=False).shape            # (1, 2)
```

> ⚠️ `subset` 指定「按哪些列判断重复」（不写就是整行完全相同才算重复）。顺序敏感：`keep="first"` 保留先出现的；`keep=False` 把重复的全删。

### `df.replace(to_replace, value)` 替换值

**解析**　把表里的某些值换成别的值：单个换、批量换、按字典映射都可以。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| to_replace | 必填 | 要替换的值：单个、列表或映射字典 |
| value | 必填 | 替换成什么（to_replace 是字典时不用写） |
| regex | False | True 时把 to_replace 当正则 |

返回：`DataFrame`

**操作**

```python
import pandas as pd

r = pd.DataFrame({"a": [0, 1, 2], "b": ["A", "B", "C"]})

r.replace(0, 9)['a'].tolist()                                         # [9, 1, 2]

r.replace([1, 2], 0)['a'].tolist()                                    # [0, 0, 0]

r.replace({"A": "甲"})["b"].tolist()                                   # ['甲', 'B', 'C']

pd.Series([" a ", "b  c"]).replace(r"\s+", "", regex=True).tolist()   # ['a', 'bc']
```

> ⚠️ 默认是**精确/子串**替换；用正则必须 `regex=True`。`replace` 既能改一类值（`[1,2] → 0`）也能按字典映射（`{"A": "甲"}`）。

### `s.astype(dtype)、pd.to_numeric(errors=)` 类型转换

**解析**　把列转成指定类型；astype 强制转、遇到坏值报错，to_numeric(errors="coerce") 把坏值变成 NaN 不报错。

返回：`Series`／`DataFrame`（类型转换后）

**操作**

```python
import pandas as pd

t = pd.Series(["18", "x", "25"])

pd.to_numeric(t, errors="coerce").tolist()         # [18.0, nan, 25.0]

pd.to_numeric(t, errors="coerce").isnull().sum()   # np.int64(1)

pd.Series(["18", "25"]).astype(int).tolist()       # [18, 25]
```

> ⚠️ `astype(int)` 遇到 `"x"` 会直接报错；清洗数据先用 `pd.to_numeric(..., errors="coerce")` 把非法值变成 `NaN`，再决定删还是填。`errors="ignore"` 已被移除。

### `df.rename(columns, index)` 改列名、行索引名

**解析**　按字典把列名、行索引名改掉，只改列出的、其余不动。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| columns | None | 旧列名→新列名字典，如 {"age": "年龄"} |
| index | None | 旧行标签→新行标签字典 |
| inplace | False | True 时直接改原表 |

返回：`DataFrame`（改名后）

**操作**

```python
import pandas as pd

df = pd.DataFrame({"name": ["Tom", "Jerry", "Ann"], "age": [18, 20, 25], "city": ["北京", "上海", "北京"]})

df.rename(columns={"age": "年龄"}).columns.tolist()   # ['name', '年龄', 'city']

df.rename(index={0: "第一行"}).index.tolist()          # ['第一行', 1, 2]

df.columns.tolist()                                 # ['name', 'age', 'city']
```

> ⚠️ 传字典只改列出的名字，其余不动（比 `df.columns = [...]` 安全，后者列数不对就报错）；`inplace=True` 会改原表。

### `df.set_index(col)、df.reset_index(drop)` 把列设为索引、索引还原成列

**解析**　set_index 把某列提成行索引，reset_index 再把索引变回普通列。

返回：`DataFrame`

**操作**

```python
import pandas as pd

df = pd.DataFrame({"name": ["Tom", "Jerry", "Ann"], "age": [18, 20, 25], "city": ["北京", "上海", "北京"]})

df.set_index("name").index.tolist()                   # ['Tom', 'Jerry', 'Ann']

df.set_index("name").columns.tolist()                 # ['age', 'city']

df.set_index("name").reset_index().columns.tolist()   # ['name', 'age', 'city']

df.reset_index(drop=True).index.tolist()              # [0, 1, 2]
```

> ⚠️ `set_index` 之后那一列**不再出现在 columns** 里（默认 drop=True）；`reset_index(drop=True)` 是「丢掉旧索引」而不是把它变回列。时间序列重采样前常要 `set_index(时间列)`。

## A5 数据变换

### `df.sort_values(by, ascending)` 按列值排序

**解析**　按某一列（或多列）的值给行排序。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| by | 必填 | 按哪一列（或哪几列）排序 |
| ascending | True | 升序；传列表可每列分别控制 |
| na_position | "last" | NaN 排最后(last)还是最前 |

返回：`DataFrame`（排序后，原表不变）

**操作**

```python
import pandas as pd

df = pd.DataFrame({"name": ["Tom", "Jerry", "Ann"], "age": [18, 20, 25], "city": ["北京", "上海", "北京"]})

df.sort_values("age", ascending=False)["name"].tolist()                     # ['Ann', 'Jerry', 'Tom']

df.sort_values(["city", "age"], ascending=[True, False])["name"].tolist()   # ['Jerry', 'Ann', 'Tom']

df.sort_index(ascending=False).index.tolist()                               # [2, 1, 0]
```

> ⚠️ `by` 传列表就是多列排序，`ascending` 传列表可分别控制升降序；`sort_index()` 是按**索引**排（不是按值）。NaN 默认排最后。

### `df.apply(func, axis)` 按列、按行套函数

**解析**　把同一个函数套到每一列（axis=0）或每一行（axis=1）上。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| func | 必填 | 要套的函数（常用 lambda） |
| axis | 0 | 0=一列一列算、1=一行一行算 |

返回：`Series`／`DataFrame`（取决于函数返回什么）

**操作**

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

**解析**　把 Series 里每个元素换成另一个值：传函数逐个算，传字典按表查。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| func | 必填 | 函数（逐个套）或映射字典 |
| na_action | None | "ignore" 时跳过 NaN 不调函数 |

返回：`Series`（逐元素映射后）

**操作**

```python
import pandas as pd

df = pd.DataFrame({"name": ["Tom", "Jerry", "Ann"], "age": [18, 20, 25], "city": ["北京", "上海", "北京"]})

df["city"].map({"北京": 1, "上海": 0}).tolist()   # [1, 0, 1]

df["age"].map(lambda x: x + 1).tolist()       # [19, 21, 26]
```

> ⚠️ 字典映射时**没匹配到的会变成 `NaN`**（不报错），想保留原值要 `.map(d).fillna(df["city"])`。这是做标签编码的常用手段。

### `df.map(func)（逐元素，取代 applymap）` DataFrame 逐元素映射

**解析**　把 DataFrame 里每个格子都套一遍函数（旧版叫 applymap，pandas 3 已移除）。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| func | 必填 | 逐元素套的函数 |
| na_action | None | "ignore" 时跳过 NaN |

返回：`DataFrame`

**操作**

```python
import pandas as pd

df = pd.DataFrame({"name": ["Tom", "Jerry", "Ann"], "age": [18, 20, 25], "city": ["北京", "上海", "北京"]})

df[["age"]].map(lambda x: x * 2).to_dict()   # {'age': {0: 36, 1: 40, 2: 50}}

df[["age"]].map(lambda x: x + 1).shape       # (3, 1)
```

> ⚠️ 老代码里的 `df.applymap(f)` 在 pandas 3.0 **已经不存在**，改成 `df.map(f)`。注意 `Series.map` 和 `DataFrame.map` 同名但不同物：前者逐元素、后者也逐元素，只是作用在整表上。

### `pd.cut(x, bins)、pd.qcut(x, q)` 数值分箱

**解析**　把数值切成一个个区间（箱）：cut 自己定边界，qcut 按分位数切。

返回：`Series`（category 类型）

**操作**

```python
import pandas as pd

age = pd.Series([15, 22, 40])

pd.cut(age, bins=[0, 18, 30, 100], labels=["未成年", "青年", "中年"]).tolist()   # ['未成年', '青年', '中年']

pd.cut(age, bins=3).astype(str).tolist()                                  # ['(14.975, 23.333]', '(14.975, 23.333]', '(31.667, 40.0]']

pd.qcut(pd.Series([1, 2, 3, 4]), q=2).astype(str).tolist()                # ['(0.999, 2.5]', '(0.999, 2.5]', '(2.5, 4.0]', '(2.5, 4.0]']
```

> ⚠️ `cut` 你自己给边界（等距或指定），`qcut` 按分位数切（每个箱里数量近似相等）；结果列是 `category`，想当字符串要 `.astype(str)`。

### `pd.get_dummies(df, columns)` 独热编码（One-Hot）

**解析**　把分类列展开成一堆 0/1 列（独热编码），喂给机器学习前常用。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| data | 必填 | 要编码的表 |
| columns | None | 要转成 0/1 的分类列 |
| drop_first | False | True 时丢掉每个分类的第一列（避免共线性） |

返回：`DataFrame`（原表 + 0/1 列）

**操作**

```python
import pandas as pd

df = pd.DataFrame({"name": ["Tom", "Jerry", "Ann"], "age": [18, 20, 25], "city": ["北京", "上海", "北京"]})

pd.get_dummies(df, columns=["city"]).columns.tolist()   # ['name', 'age', 'city_上海', 'city_北京']

pd.get_dummies(df, columns=["city"]).shape              # (3, 4)

pd.get_dummies(df, columns=["city"]).iloc[0].tolist()   # ['Tom', np.int64(18), np.False_, np.True_]
```

> ⚠️ 喂给机器学习前把分类列转成 0/1；训练集和测试集**必须对齐列**（用同一个 `categories` 或之后 `reindex`），否则特征数对不上。`drop_first=True` 可避免共线性。

## A6 分组聚合

### `df.groupby(by)` 按列分组

**解析**　按某列的值把表分成一组一组，后面跟 mean/sum/size 等聚合才能出结果。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| by | 必填 | 按哪一列（或几列）分组 |
| as_index | True | 分组列默认变索引；False 让它留在列里 |
| dropna | True | 是否忽略 NaN 组 |

返回：`GroupBy` 对象（必须接聚合函数才有结果）

**操作**

```python
import pandas as pd

df = pd.DataFrame({"name": ["Tom", "Jerry", "Ann"], "age": [18, 20, 25], "city": ["北京", "上海", "北京"]})

df.groupby("city")["age"].mean().round(2).to_dict()                 # {'上海': 20.0, '北京': 21.5}

df.groupby("city").size().to_dict()                                 # {'上海': 1, '北京': 2}

df.groupby("city", as_index=False)["age"].mean().columns.tolist()   # ['city', 'age']
```

> ⚠️ 分组列默认变成**索引**；想让它留在列里就 `as_index=False` 或 `.reset_index()`。`groupby` 本身不是结果，后面必须跟聚合（mean/sum/size…）。

### `groupby.agg(func)` 分组后做多种聚合

**解析**　分组之后做聚合：一个函数、多个函数、给每列指定不同函数都行。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| func | 必填 | 聚合函数：字符串（"mean"）或列表（["mean","max"]）；命名聚合 新列名=("原列","函数") |

返回：`DataFrame`／`Series`（一列多指标 → 多级列名）

**操作**

```python
import pandas as pd

df = pd.DataFrame({"name": ["Tom", "Jerry", "Ann"], "age": [18, 20, 25], "city": ["北京", "上海", "北京"]})

df.groupby("city")["age"].agg(["mean", "max", "count"]).round(2).to_dict()    # {'mean': {'上海': 20.0, '北京': 21.5}, 'max': {'上海': 20, '北京': 25}, 'count': {'上海': 1, '北京': 2}}

df.groupby("city").agg({"age": "mean"}).round(2).to_dict()                    # {'age': {'上海': 20.0, '北京': 21.5}}

df.groupby("city").agg(平均年龄=("age", "mean"), 人数=("age", "count")).to_dict()   # {'平均年龄': {'上海': 20.0, '北京': 21.5}, '人数': {'上海': 1, '北京': 2}}
```

> ⚠️ **命名聚合**（`新列名=("原列", "函数")`）最推荐：结果列名直接就是你要的名字。`agg(["mean","max"])` 会得到多级列名，取值要写 `df[("age", "mean")]`。

### `groupby.transform(func)、groupby.filter(func)` 组内计算后广播、按组筛选

**解析**　transform 组内算完把结果广播回每一行；filter 按条件整组保留或丢掉。

返回：transform：和原表等长的 `DataFrame`；filter：筛过的 `DataFrame`

**操作**

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

**解析**　把表「旋转」成透视表：行、列、值三样指定好，自动聚合。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| data | 必填 | 数据表 |
| index | None | 行分组键（透视后的行） |
| columns | None | 列分组键（透视后的列） |
| values | None | 要聚合的数值列 |
| aggfunc | "mean" | 聚合函数，默认平均 |
| fill_value | None | 空格子填什么（默认 NaN） |

返回：`DataFrame`（透视表）

**操作**

```python
import pandas as pd

df = pd.DataFrame({"name": ["Tom", "Jerry", "Ann"], "age": [18, 20, 25], "city": ["北京", "上海", "北京"]})

pd.pivot_table(df, index="city", values="age", aggfunc="mean").round(2).to_dict()                   # {'age': {'上海': 20.0, '北京': 21.5}}

pd.pivot_table(df, index="city", columns="name", values="age", aggfunc="max", fill_value=0).shape   # (2, 3)
```

> ⚠️ 行 = `index`、列 = `columns`、值 = `values`；没有数据的格子默认填 `NaN`（`fill_value=0` 可改）。比 `groupby` 多的是「把某个分类铺成列」。

## A7 合并与连接

### `pd.concat(objs, axis, ignore_index)` 拼接表

**解析**　把多张表拼成一张：上下堆或者左右拼。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| objs | 必填 | 要拼的表列表 [df1, df2, …] |
| axis | 0 | 0=上下堆叠、1=左右拼接 |
| ignore_index | False | True 时重新编号（0,1,2…） |

返回：`DataFrame`（拼接后，按列名对齐）

**操作**

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

**解析**　像 SQL JOIN 一样把两张表按键连起来。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| left | 必填 | 左表 |
| right | 必填 | 右表 |
| how | "inner" | inner=只留都有的键、left=保留左表全部、outer=并集 |
| on | None | 按键连（两边键名相同） |
| left_on | None | 两边键名不同时分别指定 |
| right_on | None | 两边键名不同时分别指定 |

返回：`DataFrame`

**操作**

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

### `df.join(other, how)` 按索引连表

**解析**　把另一张表按索引连过来（不是按键）。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| other | 必填 | 要连过来的另一张表 |
| how | "left" | 连接方式（同 merge） |
| lsuffix | "" | 两边列名相同时加后缀区分 |
| rsuffix | "" | 两边列名相同时加后缀区分 |

返回：`DataFrame`（按索引对齐）

**操作**

```python
import pandas as pd

J1 = pd.DataFrame({"a": [1]}, index=[1])

J2 = pd.DataFrame({"b": [2]}, index=[1])

J1.join(J2).to_dict("records")                                                # [{'a': 1, 'b': 2}]

J1.join(pd.DataFrame({"b": [2]}, index=[9]), how="left").to_dict("records")   # [{'a': 1, 'b': nan}]
```

> ⚠️ `join` 默认按**索引**对齐（不是按列）；列名相同时要 `lsuffix`/`rsuffix` 区分。键在普通列上就先用 `set_index` 或直接 `merge`。

## A8 统计与描述

### `df.mean、df.sum、df.min、df.max、df.median、df.std、df.count` 基础统计（默认按列）

**解析**　基础统计：对每列算均值、总和、最小、最大、中位数、标准差、非空个数，默认跳过 NaN。

返回：`Series`（每列一个数）

**操作**

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

### `s.quantile、s.cumsum、s.pct_change` 分位数、累计、环比

**解析**　分位数（默认中位数）、累计和、环比变化率三件套。

返回：`Series`；`pct_change` 首行是 NaN

**操作**

```python
import pandas as pd

sales = pd.Series([100, 110, 99])

sales.quantile(0.25)                    # np.float64(99.5)

sales.cumsum().tolist()                 # [100, 210, 309]

sales.pct_change().round(4).tolist()    # [nan, 0.1, -0.1]

sales.diff().tolist()                   # [nan, 10.0, -11.0]
```

> ⚠️ `pct_change()` 是「相对上一期的变化率」（第一期必为 NaN）；`quantile(0.5)` 就是中位数，`quantile(0.9)` 常用于看尾部。

### `df.corr()、df.cov()` 相关系数、协方差矩阵

**解析**　算列与列之间的相关系数（pearson 线性、spearman 单调）或协方差。

返回：`DataFrame`（相关系数／协方差方阵）

**操作**

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

### `s.idxmax、df.nlargest、df.nsmallest` 极值在哪一行、取前 n 行

**解析**　找最大值在哪一行（idxmax），或直接取最大/最小的前 n 行。

返回：索引标签／`DataFrame`（前 n 行）

**操作**

```python
import pandas as pd

df = pd.DataFrame({"name": ["Tom", "Jerry", "Ann"], "age": [18, 20, 25], "city": ["北京", "上海", "北京"]})

df["age"].idxmax()                        # 2

df["age"].idxmin()                        # 0

df.nlargest(2, "age")["name"].tolist()    # ['Ann', 'Jerry']

df.nsmallest(1, "age")["name"].tolist()   # ['Tom']
```

> ⚠️ `idxmax()` 返回的是**行索引标签**（不是位置，也不是数值）；并列时只给第一个。`nlargest(n, col)` 比 `sort_values().head(n)` 快，取排行榜用它。

## A9 时间序列

### `pd.to_datetime(arg, format, errors)` 字符串→时间类型

**解析**　把字符串变成真正的时间类型，之后才能用 .dt 和日期运算。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| arg | 必填 | 要转换的字符串或字符串列 |
| format | None | 日期格式，如 "%Y-%m-%d"（指定更快更准） |
| errors | "raise" | 认不出的值：raise=报错、coerce=变 NaT、ignore=跳过 |

返回：`Series`（datetime 类型）／`Timestamp`

**操作**

```python
import pandas as pd

pd.to_datetime(pd.Series(["2024-01-01", "2024-02-01"])).dt.month.tolist()         # [1, 2]

pd.to_datetime(pd.Series(["2024-01-01", "坏值"]), errors="coerce").isnull().sum()   # np.int64(1)

pd.to_datetime("2024-01-01").year                                                 # 2024
```

> ⚠️ 指定 `format="%Y-%m-%d"` 更快也更不容易猜错；`errors="coerce"` 把认不出的变成 `NaT`（不报错）——**注意别悄悄丢数据**，转换后先看有多少 NaT。

### `pd.date_range(start, periods, freq)` 生成时间索引

**解析**　生成一串等间隔的时间点，常用来当时间索引。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| start | None | 起始时间 |
| end | None | 结束时间（和 start 配合用） |
| periods | None | 生成几个时间点（和 freq 配合用） |
| freq | "D" | 频率：D=天、W=周、h=小时、ME=月末、MS=月初 |

返回：`DatetimeIndex`（一串时间点）

**操作**

```python
import pandas as pd

pd.date_range("2024-01-01", periods=3, freq="D").strftime("%Y-%m-%d").tolist()       # ['2024-01-01', '2024-01-02', '2024-01-03']

pd.date_range("2024-01-01", periods=3, freq="ME").strftime("%Y-%m-%d").tolist()      # ['2024-01-31', '2024-02-29', '2024-03-31']

pd.date_range("2024-01-01", periods=3, freq="MS").strftime("%Y-%m-%d").tolist()      # ['2024-01-01', '2024-02-01', '2024-03-01']

pd.date_range("2024-01-01", "2024-01-05", freq="2D").strftime("%Y-%m-%d").tolist()   # ['2024-01-01', '2024-01-03', '2024-01-05']
```

> ⚠️ **pandas 3.0 起 `freq="M"` 会报 `ValueError`**：月末用 `"ME"`、月初用 `"MS"`、年末 `"YE"`、年初 `"YS"`；常用还有 `D`（天）、`W`（周）、`h`（小时）。

### `s.dt 访问器` 从时间列取年、月、星期

**解析**　时间列专属的 .dt 访问器：取年、月、星期等。

返回：`Series`（year/month/day/weekday 的结果）

**操作**

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

**解析**　把时间序列按频率重采样再聚合，等价于「按时间段 groupby」。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| rule | 必填 | 时间频率："ME" 按月、"2D" 每两天、"W" 每周 |
| on | None | 时间在普通列里时指定列名（否则先 set_index） |

返回：`Resampler` → 接聚合后是 `DataFrame`（按时间段汇总）

**操作**

```python
import pandas as pd

ts = pd.DataFrame({"sales": [10, 20, 30]}, index=pd.date_range("2024-01-01", periods=3, freq="D"))

ts.resample("ME")["sales"].sum().tolist()            # [60]

ts.resample("2D")["sales"].sum().tolist()            # [30, 30]

ts.resample("W")["sales"].mean().round(2).tolist()   # [20.0]
```

> ⚠️ 核心是「先有 DatetimeIndex」（`set_index(时间列)` 或传 `on="时间列"`），再按频率聚合；规则同 `date_range`（月末 `"ME"`）。等价于「按时间段 groupby」。

### `s.shift(periods)、s.rolling(window).mean()` 上期值、滑动平均

**解析**　shift 取上期/下期的值，rolling 做滑动窗口统计（如移动平均）。

返回：`Series`（会产生 NaN）

**操作**

```python
import pandas as pd

sh = pd.Series([10, 20, 30, 40])

sh.shift(1).tolist()                           # [nan, 10.0, 20.0, 30.0]

sh.shift(-1).tolist()                          # [20.0, 30.0, 40.0, nan]

sh.rolling(2).mean().tolist()                  # [nan, 15.0, 25.0, 35.0]

sh.rolling(2, min_periods=1).mean().tolist()   # [10.0, 15.0, 25.0, 35.0]
```

> ⚠️ `shift(1)` 是「取上一期的值」（首行 NaN）；`rolling(2).mean()` 前 1 个值是 NaN，想让结果不全空就 `min_periods=1`。做同比/环比、移动平均必用。

## A10 字符串处理（.str）

### `s.str.contains、s.str.startswith、s.str.endswith` 字符串包含、前后缀判断

**解析**　判断字符串列里每个值包含什么、以什么开头、以什么结尾。

返回：布尔 `Series`

**操作**

```python
import pandas as pd

names = pd.Series(["张三", "李四", "Alice"])

names.str.contains("张").tolist()                # [True, False, False]

names.str.startswith("A").tolist()              # [False, False, True]

names.str.endswith("四").tolist()                # [False, True, False]

names.str.contains("张", regex=False).tolist()   # [True, False, False]
```

> ⚠️ `contains` 默认 `regex=True`：要找字面量里的 `.`、`*`、`(` 等符号必须加 `regex=False`，否则会被当正则；结果里 NaN 仍然是 NaN（不是 False），做筛选前先 `fillna(False)`。

### `s.str.split(expand=True)、s.str.cat` 拆分、拼接字符串列

**解析**　按分隔符拆开字符串（expand=True 直接拆成多列），或把两列字符串拼起来。

返回：`Series`／`DataFrame`（expand=True 拆成多列）

**操作**

```python
import pandas as pd

full = pd.Series(["张_三", "李_四"])

full.str.split("_").tolist()                                   # [['张', '三'], ['李', '四']]

full.str.split("_", expand=True).shape                         # (2, 2)

full.str.split("_", expand=True)[0].tolist()                   # ['张', '李']

pd.Series(["张"]).str.cat(pd.Series(["三"]), sep="-").tolist()   # ['张-三']
```

> ⚠️ `expand=True` 直接拆成多个列（列名是 0,1,2…，之后再 `rename`）；`str.cat` 默认不插分隔符，要 `sep=`。只想拆出第一段可以用 `str.extract`。

### `s.str.replace、s.str.strip、s.str.lower、s.str.upper` 清洗文本

**解析**　文本清洗四件套：替换、去首尾空格、转小写、转大写。

返回：`Series`

**操作**

```python
import pandas as pd

txt = pd.Series([" Tom ", "JERRY"])

txt.str.strip().tolist()                           # ['Tom', 'JERRY']

txt.str.lower().tolist()                           # [' tom ', 'jerry']

txt.str.upper().tolist()                           # [' TOM ', 'JERRY']

pd.Series(["张 三"]).str.replace(" ", "").tolist()   # ['张三']
```

> ⚠️ `.str.replace` 默认 `regex=False`（和 Python 的 `str.replace` 一致）；要正则得显式 `regex=True`。去掉多余空格是数据清洗第一步，配合 `.str.strip()` 用。

### `s.str.extract、s.str.len、s.str.isdigit` 正则提取、长度、是否数字

**解析**　用正则从字符串里抠出片段、数长度、判断是否全是数字。

返回：`DataFrame`（extract，一列一个捕获组）／`Series`（len、isdigit）

**操作**

```python
import pandas as pd

mix = pd.Series(["订单A123", "订单B456"])

mix.str.extract(r"(\d+)")[0].tolist()            # ['123', '456']

mix.str.len().tolist()                           # [6, 6]

pd.Series(["12", "ab"]).str.isdigit().tolist()   # [True, False]

mix.str.extract(r"([A-Z])(\d+)")[1].tolist()     # ['123', '456']
```

> ⚠️ `extract` 只提取**第一个**捕获组（多组就成了多列）；没匹配到的行是 NaN。`str.len()` 数的是**字符数**（中文算 1 个），`isdigit()` 判「全是数字」（`"1.5"`、`"-1"` 都是 False）。



1. **先掌握「选择」三板斧**：`df[条件]`（布尔索引）、`df.loc`（按标签）、`df.iloc`（按位置）—— 覆盖 80% 的筛选场景。
2. **`groupby` + `agg` 是分析核心**：几乎所有「按……统计……」都能用 `df.groupby("列").agg(...)` 表达。
3. **分清 `axis`**：`axis=0` 沿行方向（对每**列**算），`axis=1` 沿列方向（对每**行**算）；默认 `axis=0`。
4. **方法几乎都返回新对象**：想改原表要重新赋值（`df = df.dropna()`），或该版本仍支持的 `inplace=True`。
5. **动手前先 `df.info()` 再 `df.describe()`**：先看清规模、类型、缺失，再决定怎么清洗。
6. **看列类型**：字符串列不能直接算数（会 `TypeError`），先 `pd.to_numeric(..., errors="coerce")` 或 `astype`。
