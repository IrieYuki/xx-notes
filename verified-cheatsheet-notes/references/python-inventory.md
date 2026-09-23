# Python 速查笔记条目骨架

来源：`~/My_Python_Study/note/Python内置函数速查笔记.md`（104 条）。
抄到 Numpy / Pandas / Matplotlib / Seaborn 那几份时，保持同样的分区与条目粒度。

## 第一部分　内置函数（## 一级分区，### 分类，#### 条目）

| 分类 | 条目 |
|------|------|
| A1 类型转换 | `int` `float` `str` `bool` `list()/tuple()/set()/dict()` `chr/ord` `hex/oct/bin` |
| A2 数学与数值 | `abs` `round` `pow` `divmod` |
| A3 聚合与判断 | `len` `sum` `min/max` `all/any` |
| A4 序列生成与迭代 | `range` `enumerate` `zip` `iter/next` |
| A5 排序与筛选 | `sorted` `reversed` `filter` `map` `slice` |
| A6 类型与属性 | `type` `isinstance/issubclass` `callable` `hasattr/getattr/setattr/delattr` `id/dir/vars` `super` |
| A7 类与装饰器 | `@staticmethod/@classmethod/@property` |
| A8 字符串表示与编码 | `repr` `hash` `bytes/bytearray` |
| A9 输入输出与格式化 | `print` `input` `open` `format/f-string` |
| A10 动态执行与反射 | `eval/exec` `compile` `globals/locals` |

## 第二部分　容器方法

| 分类 | 条目 |
|------|------|
| B1 list | 切片读取、切片赋值、`append`、`extend/+=`、`insert`、`remove`、`pop`、`clear`、`del`、`index`、`count`、`in`、`reverse`、`sort`、`copy/deepcopy`、列表推导式、5 个常用组合 |
| B2 str | 切片、`split`、`join`、`strip/lstrip/rstrip`、`replace`、`find/index`、`startswith/endswith`、`upper/lower/title/capitalize`、`count`、`in`、`zfill/ljust/rjust/center`、`isdigit/isalpha/isalnum/isspace`、f-string 格式化、3 个常用套路 |
| B3 dict | 创建、`d[k]`、`d.get`、`d[k]=v`、`update`、`setdefault`、`\|` 合并、`keys/values/items`、`in`、`pop`、`popitem`、`del/clear`、遍历、`copy`、推导式与 `Counter` |
| B4 set | 创建、`add`、`update`、`remove/discard`、`pop/clear`、`in`、交并差 `\| & - ^`、`issubset/issuperset/isdisjoint`、`sorted`、去重的 3 种写法 |
| B5 tuple | 创建（`(5,)` 陷阱）、读取/切片、`count/index`、解包、重建元组、当 dict 的 key、tuple vs list |

## 每个库笔记的取舍（做 Numpy/Pandas 时）

- 保留：高频 API + 每个 API 的**参数陷阱**（axis、inplace、dtype、copy 语义）。
- 保留：`.copy()` 类「视图 vs 副本」声明，这类最容易被注释写错，必须实跑验证。
- 砍掉：一次性配置项、需要画图才能看的数据，示例尽量用几行字面对量，别依赖外部文件。
- 示例里的外部数据（csv/图片）要写清路径与生成方式，否则校验脚本跑不过。
