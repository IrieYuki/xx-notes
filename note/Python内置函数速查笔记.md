# Python 常用函数与方法速查笔记

> 收集范围：日常写代码、做作业、刷题时最常忘、最高频的内置函数与容器方法。
> 每条都是「**签名 ｜ 返回 ｜ 备注**」三格 + 可直接运行的示例（`#` 后面是**真实输出**）。

## 怎么用这份文件

1. **先看下面的《索引 · 速查表》**：一行一个函数/方法，点「用法」列直接跳到正文对应位置；忘了名字就按分类扫一遍。
2. **正文每条统一格式**：
   - 标题：`名字(参数)` + 一句话作用
   - **签名 ｜ 返回 ｜ 备注**：三格看清「怎么调用、得到什么、什么时候报错」
   - 代码块：可直接复制运行，`#` 后是真实输出，`❌` 标的是会报错的写法
   - `> ⚠️`：要点 / 陷阱提醒（没有就不写）
3. **内容在不同板块会重复**（比如 `in` 在 list / set / str 里各写一遍）—— 故意这么做的：从索引直接跳过去就行，不用来回翻页。
4. **顺序**：内置函数 A1→A10（基础 → 进阶）；容器方法 list → str → dict → set → tuple（按日常使用频率）。
5. 想按顺序系统复习，见文末《学习建议》。

---

## 索引 · 速查表

| 分类 | 用法（点击跳转） | 一句话作用 |
|------|------------------|-----------|
| A1 类型转换 | [`int(x, base=10)`](#intx-base10-字符串数字--整数可指定进制) | 字符串/数字 → 整数，可指定进制 |
| A1 类型转换 | [`float(x)`](#floatx-字符串数字--浮点数) | 字符串/数字 → 浮点数 |
| A1 类型转换 | [`str(object)`](#strobject-任意对象--字符串) | 任意对象 → 字符串 |
| A1 类型转换 | [`bool(x)`](#boolx-任意值--true--false) | 任意值 → True / False |
| A1 类型转换 | [`list()、tuple()、set()、dict()`](#listtuplesetdict-四种容器互转) | 四种容器互转 |
| A1 类型转换 | [`chr(i)、ord(c)`](#chriordc-整数--字符unicode-码点) | 整数 ↔ 字符（Unicode 码点） |
| A1 类型转换 | [`hex(x)、oct(x)、bin(x)`](#hexxoctxbinx-整数--带前缀的进制字符串) | 整数 → 带前缀的进制字符串 |
| A2 数学与数值 | [`abs(x)`](#absx-绝对值复数是模长) | 绝对值（复数是模长） |
| A2 数学与数值 | [`round(x, ndigits=0)`](#roundx-ndigits0-四舍五入银行家舍入) | 四舍五入（银行家舍入） |
| A2 数学与数值 | [`pow(x, y, mod=None)`](#powx-y-modnone-幂运算可带取模) | 幂运算，可带取模 |
| A2 数学与数值 | [`divmod(a, b)`](#divmoda-b-一次拿到商和余数) | 一次拿到商和余数 |
| A3 聚合与判断 | [`len(s)`](#lens-长度元素个数) | 长度：元素个数 |
| A3 聚合与判断 | [`sum(iterable, start=0)`](#sumiterable-start0-求和可指定起始值) | 求和，可指定起始值 |
| A3 聚合与判断 | [`min() / max()`](#min--max-最小值--最大值) | 最小值 / 最大值 |
| A3 聚合与判断 | [`all() / any()`](#all--any-全为真--存在真值) | 全为真 / 存在真值 |
| A4 序列生成与迭代 | [`range(start, stop, step=1)`](#rangestart-stop-step1-生成整数序列惰性求值) | 生成整数序列（惰性求值） |
| A4 序列生成与迭代 | [`enumerate(iterable, start=0)`](#enumerateiterable-start0-遍历时同时拿到下标和元素) | 遍历时同时拿到下标和元素 |
| A4 序列生成与迭代 | [`zip(*iterables)`](#zipiterables-按位置把多个序列打包) | 按位置把多个序列打包 |
| A4 序列生成与迭代 | [`iter(obj) / next(it, default)`](#iterobj--nextit-default-取迭代器逐个取值) | 取迭代器、逐个取值 |
| A5 排序与筛选 | [`sorted(iterable, key=None, reverse=False)`](#sortediterable-keynone-reversefalse-排序返回新列表) | 排序，返回**新**列表 |
| A5 排序与筛选 | [`reversed(seq)`](#reversedseq-反向迭代器不改原序列) | 反向迭代器（不改原序列） |
| A5 排序与筛选 | [`filter(function, iterable)`](#filterfunction-iterable-按条件筛选元素) | 按条件筛选元素 |
| A5 排序与筛选 | [`map(function, iterable, ...)`](#mapfunction-iterable--对每个元素做转换) | 对每个元素做转换 |
| A5 排序与筛选 | [`slice(start, stop, step)`](#slicestart-stop-step-切片对象很少直接用) | 切片对象（很少直接用） |
| A6 类型与属性 | [`type(obj)`](#typeobj-查看对象的类型) | 查看对象的类型 |
| A6 类型与属性 | [`isinstance(obj, cls) / issubclass(cls, cls2)`](#isinstanceobj-cls--issubclasscls-cls2-类型判断--继承判断) | 类型判断 / 继承判断 |
| A6 类型与属性 | [`callable(obj)`](#callableobj-判断能不能当函数调用) | 判断能不能当函数调用 |
| A6 类型与属性 | [`hasattr / getattr / setattr / delattr`](#hasattr--getattr--setattr--delattr-属性的动态检查与读写) | 属性的动态检查与读写 |
| A6 类型与属性 | [`id(obj) / dir(obj) / vars(obj)`](#idobj--dirobj--varsobj-内存地址--属性名--命名空间) | 内存地址 / 属性名 / 命名空间 |
| A6 类型与属性 | [`super()`](#super-调用父类的方法) | 调用父类的方法 |
| A7 类与装饰器 | [`@staticmethod / @classmethod / @property`](#staticmethod--classmethod--property-三种常用装饰器的用法) | 三种常用装饰器的用法 |
| A8 字符串表示与编码 | [`repr(obj)`](#reprobj-给开发者看的可还原表示) | 给开发者看的「可还原」表示 |
| A8 字符串表示与编码 | [`hash(obj)`](#hashobj-取哈希值dictset-的底层) | 取哈希值（dict/set 的底层） |
| A8 字符串表示与编码 | [`bytes() / bytearray()`](#bytes--bytearray-二进制数据不可变--可变) | 二进制数据（不可变 / 可变） |
| A9 输入输出与格式化 | [`print(*objects, sep, end)`](#printobjects-sep-end-打印输出) | 打印输出 |
| A9 输入输出与格式化 | [`input(prompt)`](#inputprompt-读取一行输入) | 读取一行输入 |
| A9 输入输出与格式化 | [`open(file, mode, encoding)`](#openfile-mode-encoding-打开文件配-with-自动关闭) | 打开文件（配 `with` 自动关闭） |
| A9 输入输出与格式化 | [`format(value, spec) / f-string`](#formatvalue-spec--f-string-格式化数值和字符串) | 格式化数值和字符串 |
| A10 动态执行与反射 | [`eval(expression) / exec(code)`](#evalexpression--execcode-把字符串当代码执行) | 把字符串当代码执行 |
| A10 动态执行与反射 | [`compile(source, filename, mode)`](#compilesource-filename-mode-把源码编译成可执行对象) | 把源码编译成可执行对象 |
| A10 动态执行与反射 | [`globals() / locals()`](#globals--locals-取全局--局部命名空间字典) | 取全局 / 局部命名空间字典 |
| B1 list 列表 | [`l[i]、l[i:j]（读取与切片）`](#lilij读取与切片-按下标取值--切出一段) | 按下标取值 / 切出一段 |
| B1 list 列表 | [`l[i] = x、l[i:j] = [...]`](#li--xlij---改单个元素--用切片批量改) | 改单个元素 / 用切片批量改 |
| B1 list 列表 | [`l.append(x)`](#lappendx-末尾追加一个元素) | 末尾追加一个元素 |
| B1 list 列表 | [`l.extend(it)、l += [...]`](#lextenditl---末尾批量追加拆开加) | 末尾批量追加（拆开加） |
| B1 list 列表 | [`l.insert(i, x)`](#linserti-x-在指定位置插入元素) | 在指定位置插入元素 |
| B1 list 列表 | [`l.remove(x)`](#lremovex-按值删除第一个匹配项) | 按**值**删除第一个匹配项 |
| B1 list 列表 | [`l.pop(i=-1)`](#lpopi-1-按下标弹出元素并返回) | 按下标弹出元素并返回 |
| B1 list 列表 | [`l.clear()`](#lclear-清空列表) | 清空列表 |
| B1 list 列表 | [`del l[i]、del l[i:j]、del l`](#del-lidel-lijdel-l-按下标--切片--变量删除) | 按下标 / 切片 / 变量删除 |
| B1 list 列表 | [`l.index(x, start, end)`](#lindexx-start-end-查值对应的下标) | 查值对应的下标 |
| B1 list 列表 | [`l.count(x)`](#lcountx-统计值出现次数) | 统计值出现次数 |
| B1 list 列表 | [`x in l`](#x-in-l-判断元素是否存在) | 判断元素是否存在 |
| B1 list 列表 | [`l.reverse()`](#lreverse-原地反转) | 原地反转 |
| B1 list 列表 | [`l.sort(key, reverse)`](#lsortkey-reverse-原地排序) | 原地排序 |
| B1 list 列表 | [`l.copy()、l[:]、copy.deepcopy()`](#lcopylcopydeepcopy-拷贝列表浅--深) | 拷贝列表（浅 / 深） |
| B1 list 列表 | [`列表推导式`](#列表推导式-一行生成新列表推荐写法) | 一行生成新列表（推荐写法） |
| B1 list 列表 | [`列表的 5 个常用组合`](#列表的-5-个常用组合-去重--扁平化--反转--求和--建二维) | 去重 / 扁平化 / 反转 / 求和 / 建二维 |
| B2 str 字符串 | [`s[i]、s[i:j]、s[::-1]`](#sisijs-1-下标与切片字符串不可改) | 下标与切片（字符串不可改） |
| B2 str 字符串 | [`s.split(sep=None, maxsplit=-1)`](#ssplitsepnone-maxsplit-1-按分隔符切成列表) | 按分隔符切成列表 |
| B2 str 字符串 | [`sep.join(iterable)`](#sepjoiniterable-把列表拼成字符串) | 把列表拼成字符串 |
| B2 str 字符串 | [`s.strip() / lstrip() / rstrip()`](#sstrip--lstrip--rstrip-去掉两端空白或指定字符) | 去掉两端空白或指定字符 |
| B2 str 字符串 | [`s.replace(old, new, count=-1)`](#sreplaceold-new-count-1-替换子串默认全部替换) | 替换子串（默认全部替换） |
| B2 str 字符串 | [`s.find(sub) / s.index(sub)`](#sfindsub--sindexsub-找子串的位置) | 找子串的位置 |
| B2 str 字符串 | [`s.startswith() / s.endswith()`](#sstartswith--sendswith-判断开头--结尾) | 判断开头 / 结尾 |
| B2 str 字符串 | [`s.upper() / lower() / title() / capitalize()`](#supper--lower--title--capitalize-大小写转换) | 大小写转换 |
| B2 str 字符串 | [`s.count(sub)`](#scountsub-统计子串出现次数) | 统计子串出现次数 |
| B2 str 字符串 | [`sub in s`](#sub-in-s-子串判断) | 子串判断 |
| B2 str 字符串 | [`s.zfill(n) / ljust / rjust / center`](#szfilln--ljust--rjust--center-补位对齐补零补空格) | 补位对齐（补零、补空格） |
| B2 str 字符串 | [`s.isdigit() / isalpha() / isalnum() / isspace()`](#sisdigit--isalpha--isalnum--isspace-判断字符串内容类型) | 判断字符串内容类型 |
| B2 str 字符串 | [`f-string 格式化`](#f-string-格式化-拼接与格式化36-首选) | 拼接与格式化（3.6+ 首选） |
| B2 str 字符串 | [`字符串的 3 个常见套路`](#字符串的-3-个常见套路-判空--忽略大小写--处理一行输入) | 判空 / 忽略大小写 / 处理一行输入 |
| B3 dict 字典 | [`d = {} 创建字典`](#d---创建字典-键值对的-5-种建法) | 键值对的 5 种建法 |
| B3 dict 字典 | [`d[key] 取值`](#dkey-取值-按键取-value) | 按键取 value |
| B3 dict 字典 | [`d.get(key, default=None)`](#dgetkey-defaultnone-安全取值推荐) | 安全取值（推荐） |
| B3 dict 字典 | [`d[key] = value`](#dkey--value-新增或覆盖) | 新增或覆盖 |
| B3 dict 字典 | [`d.update(other)`](#dupdateother-批量新增--覆盖) | 批量新增 / 覆盖 |
| B3 dict 字典 | [`d.setdefault(key, default=None)`](#dsetdefaultkey-defaultnone-不存在才初始化分组神器) | 不存在才初始化（分组神器） |
| B3 dict 字典 | [`d1 | d2（3.9+）`](#d1--d239-合并两个字典生成新对象) | 合并两个字典（生成新对象） |
| B3 dict 字典 | [`d.keys() / d.values() / d.items()`](#dkeys--dvalues--ditems-取键--值--键值对) | 取键 / 值 / 键值对 |
| B3 dict 字典 | [`key in d`](#key-in-d-判断键是否存在) | 判断键是否存在 |
| B3 dict 字典 | [`d.pop(key, default)`](#dpopkey-default-弹出键并返回值) | 弹出键并返回值 |
| B3 dict 字典 | [`d.popitem()`](#dpopitem-删掉并返回最后一个键值对) | 删掉并返回最后一个键值对 |
| B3 dict 字典 | [`del d[k] / d.clear()`](#del-dk--dclear-删除一个键--清空字典) | 删除一个键 / 清空字典 |
| B3 dict 字典 | [`遍历字典`](#遍历字典-3-种遍历方式--改值的正确姿势) | 3 种遍历方式 + 改值的正确姿势 |
| B3 dict 字典 | [`d.copy() / copy.deepcopy()`](#dcopy--copydeepcopy-拷贝字典浅--深) | 拷贝字典（浅 / 深） |
| B3 dict 字典 | [`字典推导式与 Counter`](#字典推导式与-counter-计数排行反转筛选一行搞定) | 计数、排行、反转、筛选一行搞定 |
| B4 set 集合 | [`set() 创建集合`](#set-创建集合-去重容器无序不重复) | 去重容器：无序、不重复 |
| B4 set 集合 | [`s.add(x)`](#saddx-加一个元素) | 加一个元素 |
| B4 set 集合 | [`s.update(iterable)`](#supdateiterable-批量加元素) | 批量加元素 |
| B4 set 集合 | [`s.remove(x) / s.discard(x)`](#sremovex--sdiscardx-删除元素报错--不报错) | 删除元素（报错 / 不报错） |
| B4 set 集合 | [`s.pop() / s.clear()`](#spop--sclear-随机删一个--清空) | 随机删一个 / 清空 |
| B4 set 集合 | [`x in s`](#x-in-s-判断元素是否存在o1) | 判断元素是否存在（O(1)） |
| B4 set 集合 | [`a | b、a & b、a - b、a ^ b`](#a--ba--ba---ba--b-交并差集合的杀手锏) | 交并差（集合的杀手锏） |
| B4 set 集合 | [`a.issubset / issuperset / isdisjoint`](#aissubset--issuperset--isdisjoint-包含关系判断) | 包含关系判断 |
| B4 set 集合 | [`sorted(s)`](#sorteds-集合要按顺序看先转-list) | 集合要按顺序看：先转 list |
| B4 set 集合 | [`去重的 3 种写法`](#去重的-3-种写法-set--dictfromkeys--嵌套去重) | set / dict.fromkeys / 嵌套去重 |
| B5 tuple 元组 | [`t = (1, 2) 创建元组`](#t--1-2-创建元组-不可变序列方法只有-2-个) | 不可变序列，方法只有 2 个 |
| B5 tuple 元组 | [`t[i]、t[i:j]（读取）`](#titij读取-下标与切片不能改) | 下标与切片（不能改） |
| B5 tuple 元组 | [`t.count(x) / t.index(x)`](#tcountx--tindexx-元组只有这两个方法) | 元组只有这两个方法 |
| B5 tuple 元组 | [`解包：a, b = t`](#解包a-b--t-把元组拆成多个变量最常用) | 把元组拆成多个变量（最常用） |
| B5 tuple 元组 | [`重建元组（因为不可变）`](#重建元组因为不可变-要改就得造个新的) | 要「改」就得造个新的 |
| B5 tuple 元组 | [`元组当 dict 的键 / 进 set`](#元组当-dict-的键--进-set-坐标组合键的好帮手) | 坐标、组合键的好帮手 |
| B5 tuple 元组 | [`tuple 还是 list？`](#tuple-还是-list-一句话选择标准) | 一句话选择标准 |

---

## 第一部分　内置函数（直接写名字调用）

### A1　类型转换

#### `int(x, base=10)` 字符串/数字 → 整数，可指定进制

**签名** `int(x, base=10)` ｜ **返回** `int` ｜ **备注** 无法转换时抛 `ValueError`

```python
int("42")        # 42
int("1010", 2)   # 10（二进制字符串）
int("ff", 16)    # 255（十六进制字符串）
int(3.9)         # 3（直接截断小数，不四舍五入）
```

> ⚠️ `int("3.14")` 会 `ValueError`：字符串里带小数点得先用 `float()` 再转。想四舍五入用 `round()`。

#### `float(x)` 字符串/数字 → 浮点数

**签名** `float(x)` ｜ **返回** `float` ｜ **备注** 不能转时抛 `ValueError`

```python
float("3.14")    # 3.14
float(7)         # 7.0
float("1e3")     # 1000.0
0.1 + 0.2        # 0.30000000000000004（浮点精度误差）
```

> ⚠️ 小数有精度误差：`0.1 + 0.2 == 0.3` 是 `False`。比较小数用 `round()` 或 `math.isclose()`；要精确计算用 `decimal.Decimal`。

#### `str(object)` 任意对象 → 字符串

**签名** `str(object)` ｜ **返回** `str` ｜ **备注** 任何对象都能转，不会报错

```python
str(123)         # '123'
str([1, 2])      # '[1, 2]'
str(3.0)         # '3.0'
str(None)        # 'None'
```

#### `bool(x)` 任意值 → True / False

**签名** `bool(x)` ｜ **返回** `bool` ｜ **备注** 判断真假时直接写 `if x:`，不必写 `if bool(x):`

```python
bool(1)          # True
bool(0)          # False
bool("hello")    # True
bool("")         # False
bool([])         # False
bool(None)       # False
```

> ⚠️ **假值清单**（记住这些，`if` 判断就不会踩坑）：`0`、`0.0`、`""`、`None`、空容器 `[]` `()` `{}` `set()`、`False`；其他都是真值。

#### `list()、tuple()、set()、dict()` 四种容器互转

**签名** `list(it)` `tuple(it)` `set(it)` `dict(it)` ｜ **返回** 对应容器对象 ｜ **备注** 无参数调用得到空容器

```python
list("abc")                # ['a', 'b', 'c']
tuple([1, 2, 3])           # (1, 2, 3)
set([1, 2, 2, 3])          # {1, 2, 3}（自动去重）
dict([("a", 1), ("b", 2)]) # {'a': 1, 'b': 2}
list(range(3))             # [0, 1, 2]
```

> ⚠️ `set()` 会打乱顺序；想「保序去重」用 `list(dict.fromkeys(x))`。`list(d)` 只拿到键，要键值对得 `list(d.items())`。

#### `chr(i)、ord(c)` 整数 ↔ 字符（Unicode 码点）

**签名** `ord(c)` 字符→码点 ｜ `chr(i)` 码点→字符 ｜ **返回** `int` / `str` ｜ **备注** 只能传单个字符，传多个会 `TypeError`

```python
ord("A")     # 65
chr(65)      # 'A'
chr(20013)   # '中'
ord("中")    # 20013
```

#### `hex(x)、oct(x)、bin(x)` 整数 → 带前缀的进制字符串

**签名** `hex(x)` `oct(x)` `bin(x)` ｜ **返回** `str` ｜ **备注** 只接整数，不能传字符串

```python
hex(255)          # '0xff'
oct(8)            # '0o10'
bin(5)            # '0b101'
int("0xff", 16)   # 255（反向：int + 进制）
```

> ⚠️ 不要前缀 `0x`/`0o`/`0b` 时用 `format(255, "x")` → `'ff'`。

### A2　数学与数值

#### `abs(x)` 绝对值（复数是模长）

**签名** `abs(x)` ｜ **返回** 同类型数值 ｜ **备注** 字符串会 `TypeError`

```python
abs(-5)        # 5
abs(3.14)      # 3.14
abs(-3 + 4j)   # 5.0（复数的模）
```

#### `round(x, ndigits=0)` 四舍五入（银行家舍入）

**签名** `round(x, ndigits=None)` ｜ **返回** 指定小数位的数值 ｜ **备注** `.5` 会舍到最近的**偶数**

```python
round(3.14159, 2)   # 3.14
round(2.5)          # 2（银行家舍入：.5 舍到偶数）
round(3.5)          # 4
round(2.675, 2)     # 2.67（2.675 在二进制里存不下，本身就略小于 2.675）
```

> ⚠️ 要求「严格四舍五入」或精确结果时别用 `round`：用 `decimal.Decimal("2.675").quantize(...)`，或 `math.floor(x + 0.5)`。

#### `pow(x, y, mod=None)` 幂运算，可带取模

**签名** `pow(x, y, mod=None)` ｜ **返回** 数值（`mod` 为空时等同 `x ** y`） ｜ **备注** 大数连乘时比 `x**y % mod` 快得多

```python
pow(2, 3)         # 8
2 ** 3            # 8（等价写法）
pow(2, 10, 1000)  # 24（即 2**10 % 1000，且中间结果不会爆）
```

#### `divmod(a, b)` 一次拿到商和余数

**签名** `divmod(a, b)` ｜ **返回** `(a // b, a % b)` 元组 ｜ **备注** 除数为 0 时 `ZeroDivisionError`

```python
divmod(10, 3)    # (3, 1)
divmod(7, 2)     # (3, 1)
divmod(-7, 2)    # (-4, 1)   ← Python 的 // 向下取整，不是截断
```

### A3　聚合与判断

#### `len(s)` 长度：元素个数

**签名** `len(s)` ｜ **返回** `int` ｜ **备注** 内置容器是 O(1)，不会真去数一遍

```python
len("hello")           # 5
len([1, 2, 3])         # 3
len({"a": 1, "b": 2})  # 2（字典数的是键值对个数）
len(range(10))         # 10
```

> ⚠️ 数字没有长度：`len(123)` 会 `TypeError`。判空用 `if not l:`，比 `if len(l) == 0:` 更地道。

#### `sum(iterable, start=0)` 求和，可指定起始值

**签名** `sum(iterable, start=0)` ｜ **返回** 数值 ｜ **备注** 字符串不能求和

```python
sum([1, 2, 3, 4])        # 10
sum([1, 2, 3], 100)      # 106（从 100 开始加）
sum(x * x for x in range(3))   # 5（0+1+4，配合生成器省内存）
sum([])                  # 0（空序列得到起始值）
```

> ⚠️ 拼字符串用 `"".join(list)`，`sum` 会报错；浮点求和有误差，要精确用 `math.fsum()`。

#### `min() / max()` 最小值 / 最大值

**签名** `min(iterable, key=...)` ｜ `max(iterable, key=...)` ｜ **返回** 序列中的某个元素 ｜ **备注** 空序列报 `ValueError`

```python
min([3, 1, 4, 1, 5])                       # 1
min(3, 1, 4)                               # 1（也可以直接传多个参数）
max(["apple", "pear", "banana"], key=len)  # 'banana'（按长度比）
students = [{"name": "Tom", "score": 85}, {"name": "Jerry", "score": 92}]
max(students, key=lambda s: s["score"])    # {'name': 'Jerry', 'score': 92}
```

> ⚠️ `key=` 只决定「怎么比」，返回的仍是整个元素。默认按字符串字典序，注意 `"Z" < "a"`。

#### `all() / any()` 全为真 / 存在真值

**签名** `all(iterable)` ｜ `any(iterable)` ｜ **返回** `bool` ｜ **备注** 空序列：`all([])` 为 True，`any([])` 为 False

```python
all([True, 1, "a"])   # True（都真）
all([True, 0])        # False（有假值）
any([0, "", False])   # False（全假）
any([0, "", 3])       # True
all([])               # True   ← 空序列算「全部满足」
any([])               # False
```

> ⚠️ 它们接受生成器且会**短路**：`any(x > 100 for x in nums)` 一遇到满足就停，比先建列表省内存。

### A4　序列生成与迭代

#### `range(start, stop, step=1)` 生成整数序列（惰性求值）

**签名** `range(stop)` ｜ `range(start, stop)` ｜ `range(start, stop, step)` ｜ **返回** `range` 对象（可迭代、可索引） ｜ **备注** **左闭右开**：不含 stop

```python
list(range(5))         # [0, 1, 2, 3, 4]
list(range(2, 8))      # [2, 3, 4, 5, 6, 7]
list(range(0, 10, 2))  # [0, 2, 4, 6, 8]
list(range(5, 0, -1))  # [5, 4, 3, 2, 1]（倒着数必须写负 step）
range(5)[-1]           # 4
len(range(0, 10, 2))   # 5
```

> ⚠️ 要「序号」用 range，要「元素」就直接遍历，别写 `for i in range(len(l))`；要下标+元素用 `enumerate`。

#### `enumerate(iterable, start=0)` 遍历时同时拿到下标和元素

**签名** `enumerate(iterable, start=0)` ｜ **返回** `(下标, 元素)` 迭代器 ｜ **备注** `start` 只改编号起点，不动原数据

```python
for i, fruit in enumerate(["apple", "banana"], start=1):
    print(i, fruit)
# 1 apple
# 2 banana

list(enumerate("ab"))    # [(0, 'a'), (1, 'b')]
```

> ⚠️ 这是 `for i in range(len(l))` 的标准替代写法。

#### `zip(*iterables)` 按位置把多个序列打包

**签名** `zip(it1, it2, ...)` ｜ **返回** 元组迭代器 ｜ **备注** 长度不同时**取最短**，多出来的被丢掉

```python
list(zip([1, 2, 3], ["a", "b", "c"]))   # [(1, 'a'), (2, 'b'), (3, 'c')]
list(zip([1, 2, 3], ["a", "b"]))        # [(1, 'a'), (2, 'b')]（按短的截断）
names, ages = ["Tom", "Jerry"], [5, 6]
dict(zip(names, ages))                  # {'Tom': 5, 'Jerry': 6}

pairs = [(1, "a"), (2, "b")]
a, b = zip(*pairs)     # 反操作（解压）：a=(1, 2), b=('a', 'b')
```

> ⚠️ `zip` 返回迭代器，只能消费一次，想留着就 `list(zip(...))`；要保留最长序列用 `itertools.zip_longest`。

#### `iter(obj) / next(it, default)` 取迭代器、逐个取值

**签名** `iter(obj)` ｜ `next(it, default)` ｜ **返回** 迭代器 / 下一个元素 ｜ **备注** 取完再 `next` 会 `StopIteration`

```python
it = iter([1, 2, 3])
next(it)         # 1
next(it)         # 2
next(it)         # 3
next(it, "end")  # 'end'（耗尽后给默认值，不报错）

for x in iter([1, 2]):   # for 循环底层就是 iter + next
    print(x)
```

> ⚠️ 迭代器是「一次性」的，消费过就没了。`for` 循环已自动处理 `StopIteration`，不用手写。

### A5　排序与筛选

#### `sorted(iterable, key=None, reverse=False)` 排序，返回**新**列表

**签名** `sorted(iterable, key=None, reverse=False)` ｜ **返回** 排序后的 `list` ｜ **备注** 原数据不动（想原地排用 `l.sort()`）

```python
sorted([3, 1, 2])                    # [1, 2, 3]
sorted([3, 1, 2], reverse=True)      # [3, 2, 1]
sorted(["aa", "b", "ccc"], key=len)  # ['b', 'aa', 'ccc']

students = [{"name": "Tom", "score": 85}, {"name": "Jerry", "score": 92}]
sorted(students, key=lambda s: s["score"], reverse=True)
# [{'name': 'Jerry', 'score': 92}, {'name': 'Tom', 'score': 85}]

sorted(["b1", "a2", "a1"], key=lambda s: (s[0], s[1]))   # 多级排序：先比第 1 位再比第 2 位
# ['a1', 'a2', 'b1']
```

> ⚠️ `key` 返回什么就按什么比。字符串默认按字典序（大写字母 `<` 小写字母）；要忽略大小写加 `key=str.lower`。

#### `reversed(seq)` 反向迭代器（不改原序列）

**签名** `reversed(seq)` ｜ **返回** 反向迭代器 ｜ **备注** 要**原地**反转列表用 `l.reverse()`

```python
list(reversed([1, 2, 3]))   # [3, 2, 1]
"".join(reversed("abc"))    # 'cba'
[1, 2, 3][::-1]             # [3, 2, 1]（切片写法，直接得到新列表）
```

#### `filter(function, iterable)` 按条件筛选元素

**签名** `filter(function, iterable)` ｜ **返回** 迭代器 ｜ **备注** `function` 传 `None` 时保留所有真值元素

```python
list(filter(lambda x: x % 2 == 0, [1, 2, 3, 4, 5]))   # [2, 4]
list(filter(None, [0, 1, "", "a", None]))             # [1, 'a']
```

> ⚠️ 新手更推荐列表推导式：`[x for x in l if x % 2 == 0]` 一样简洁，还不用记 `filter`。

#### `map(function, iterable, ...)` 对每个元素做转换

**签名** `map(function, *iterables)` ｜ **返回** 迭代器 ｜ **备注** 多个序列时会按位传给 function

```python
list(map(str, [1, 2, 3]))              # ['1', '2', '3']
list(map(lambda x: x * 2, [1, 2, 3]))  # [2, 4, 6]
list(map(pow, [2, 3], [4, 5]))         # [16, 243]（2**4, 3**5）
```

> ⚠️ 等价写法 `[x * 2 for x in [1, 2, 3]]`。要同时用索引就 `enumerate`，`map` 没有下标。

#### `slice(start, stop, step)` 切片对象（很少直接用）

**签名** `slice(start, stop, step)` ｜ **返回** `slice` 对象 ｜ **备注** 平时直接写 `l[1:5:2]` 就行

```python
s = slice(1, 5, 2)
[0, 1, 2, 3, 4, 5][s]      # [1, 3]
"abcdef"[s]                # 'bd'
```

> ⚠️ 它的用处：把切片参数存成变量复用，或传给自定义类的 `__getitem__`。

### A6　类型与属性

#### `type(obj)` 查看对象的类型

**签名** `type(obj)` ｜ **返回** 类型对象 ｜ **备注** `type(x) is int` 不认子类

```python
type(1)           # <class 'int'>
type("a")         # <class 'str'>
type(1) is int    # True
type(True) is int # False  ← bool 是 int 的子类，但 type 只认「正好是」某个类
```

> ⚠️ 判断类型请用 `isinstance`，`type` 主要用来调试打印。

#### `isinstance(obj, cls) / issubclass(cls, cls2)` 类型判断 / 继承判断

**签名** `isinstance(obj, cls_or_tuple)` ｜ `issubclass(cls, cls_or_tuple)` ｜ **返回** `bool` ｜ **备注** **官方推荐的类型判断方式**（支持继承）

```python
isinstance(1, int)             # True
isinstance(True, int)          # True（bool 是 int 子类）
isinstance(1, (int, float))    # True（是其中任一类型即可）
issubclass(bool, int)          # True
```

#### `callable(obj)` 判断能不能当函数调用

**签名** `callable(obj)` ｜ **返回** `bool` ｜ **备注** 类本身、实现了 `__call__` 的对象都算可调用

```python
callable(print)      # True
callable(len)        # True
callable("abc")      # False
class A:
    def __call__(self): return 1
callable(A())        # True
```

#### `hasattr / getattr / setattr / delattr` 属性的动态检查与读写

**签名** `hasattr(obj, name)` ｜ `getattr(obj, name, default)` ｜ `setattr(obj, name, value)` ｜ `delattr(obj, name)` ｜ **返回** 属性值 / `bool` / `None` ｜ **备注** `getattr` 给了默认值就不会报错

```python
class Person:
    name = "Tom"

hasattr(Person, "name")      # True
getattr(Person, "name")      # 'Tom'
getattr(Person, "age", 0)    # 0（不存在则返回默认值）
setattr(Person, "age", 18)   # 动态添加属性 -> Person.age 变成 18
delattr(Person, "age")       # 删掉该属性
```

> ⚠️ 属性名是「字符串」时才需要这一套；平时直接 `obj.name` 读、`obj.name = x` 写就行。

#### `id(obj) / dir(obj) / vars(obj)` 内存地址 / 属性名 / 命名空间

**签名** `id(obj)` ｜ `dir(obj)` ｜ `vars(obj)` ｜ **返回** `int` / `list` / `dict` ｜ **备注** `id` 只在对象存活期间有效

```python
class Person:
    name = "Tom"

id(123)                          # 一串内存地址整数
"name" in dir(Person)            # True（dir 列出所有属性名，含大量双下划线）
vars(Person)["name"]             # 'Tom'（vars 返回对象的 __dict__）
```

> ⚠️ 别用 `id` 判断两个东西是否相等，用 `==`；`is` 比 `id(a) == id(b)` 更直观。`dir(obj)` 配合 `help(obj)` 是查方法的利器。

#### `super()` 调用父类的方法

**签名** `super()` ｜ **返回** 父类代理对象 ｜ **备注** 子类 `__init__` 里必须先调它

```python
class Animal:
    def __init__(self, name):
        self.name = name

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)   # 调用父类构造，别忘了
        self.breed = breed

d = Dog("旺财", "金毛")
d.name, d.breed   # ('旺财', '金毛')
```

> ⚠️ 漏掉 `super().__init__()` 时父类的属性不会被初始化，会在后面报 `AttributeError`。

### A7　类与装饰器

#### `@staticmethod / @classmethod / @property` 三种常用装饰器的用法

**签名** `@staticmethod` ｜ `@classmethod` ｜ `@property` ｜ **返回** 函数 / 属性值 ｜ **备注** 平时直接用 `@` 写法，不必手写 `staticmethod(fn)`

```python
class Circle:
    def __init__(self, r):
        self._r = r

    @property              # 把方法当属性用：circle.area（不加括号）
    def area(self):
        return 3.14 * self._r ** 2

    @classmethod           # 第一个参数是类本身 cls，常用于另类构造器
    def unit(cls):
        return cls(1)

    @staticmethod          # 不需要 self / cls 的工具函数
    def info():
        return "Circle 类"

Circle.unit().area   # 3.14
Circle.info()        # 'Circle 类'
```

> ⚠️ `@property` 让 `area` 像属性一样访问（写成 `area()` 会报 `'float' object is not callable`）；`@classmethod` 里第一个参数永远是 `cls`。

### A8　字符串表示与编码

#### `repr(obj)` 给开发者看的「可还原」表示

**签名** `repr(obj)` ｜ **返回** `str` ｜ **备注** 字符串会带引号；容器内部用的是元素的 repr

```python
repr("hello")    # "'hello'"（带引号）
str("hello")     # 'hello'
repr([1, 2])     # '[1, 2]'
print("a")       # 屏幕上是 a，因为 print 用的是 str
```

> ⚠️ 调试时用 `repr`（能看出空字符串、多余空格），给用户看用 `str`/`print`。

#### `hash(obj)` 取哈希值（dict/set 的底层）

**签名** `hash(obj)` ｜ **返回** `int` ｜ **备注** 只有不可变对象能哈希

```python
hash("abc")      # 一串整数
hash((1, 2))     # 元组可哈希
# hash([1, 2])   # ❌ TypeError: unhashable type: 'list'
```

> ⚠️ 所以 dict 的 key、set 的元素只能用不可变类型（str、int、tuple…）。同一个值在同一进程里哈希值稳定，**跨进程不保证**。

#### `bytes() / bytearray()` 二进制数据（不可变 / 可变）

**签名** `bytes(x, encoding=...)` ｜ `bytearray(x)` ｜ **返回** `bytes` / `bytearray` ｜ **备注** 文本用 `str`，二进制用 `bytes`

```python
bytes("中文", encoding="utf-8")      # b'\xe4\xb8\xad\xe6\x96\x87'
b"abc".decode("utf-8")               # 'abc'
"abc".encode("utf-8")                # b'abc'
bytearray(b"abc")[0] = 100           # 可变，能改
```

> ⚠️ 文件/网络里遇到乱码，多半是 `encoding` 没写对；读写二进制文件用 `"rb"`/`"wb"`，不传 `encoding`。

### A9　输入输出与格式化

#### `print(*objects, sep, end)` 打印输出

**签名** `print(*objects, sep=" ", end="\n", file=..., flush=False)` ｜ **返回** `None` ｜ **备注** 多值自动加空格，结尾自动换行

```python
print("a", "b", "c")        # a b c
print("a", "b", sep="-")    # a-b
print("hello", end=" ")     # 不换行
print("world")              # hello world
f = 3.14159
print(f"{f:.2f}")           # 3.14（格式化交给 f-string）
```

> ⚠️ `end=""` 可以不换行；要写文件用 `file=f`。多个值连在一起不想加空格就 `print("a" + "b")` 或改 `sep=""`。

#### `input(prompt)` 读取一行输入

**签名** `input(prompt)` ｜ **返回** `str`（**永远是字符串**） ｜ **备注** 参与计算前必须转类型

```python
name = input("请输入名字: ")
age = int(input("请输入年龄: "))   # 记得转 int
nums = list(map(int, input().split()))   # 一行读多个整数
```

> ⚠️ `input()` 拿到的是 `'18'` 不是 `18`：`"18" + 1` 会 `TypeError`。做算法题时用 `sys.stdin.readline()` 更快。

#### `open(file, mode, encoding)` 打开文件（配 `with` 自动关闭）

**签名** `open(file, mode="r", encoding=None)` ｜ **返回** 文件对象 ｜ **备注** 模式：`r` 读 / `w` 覆盖写 / `a` 追加 / `rb`·`wb` 二进制

```python
with open("test.txt", "w", encoding="utf-8") as f:
    f.write("你好\n")

with open("test.txt", "r", encoding="utf-8") as f:
    content = f.read()        # 一次读全部
    # for line in f:          # 大文件改成逐行读，省内存
    #     print(line, end="")
```

> ⚠️ `w` 会**直接清空**原文件，想追加用 `a`；中文乱码就检查 `encoding="utf-8"`；打开文件务必用 `with`，否则忘了 `close()` 可能丢数据。

#### `format(value, spec) / f-string` 格式化数值和字符串

**签名** `format(value, format_spec)` ｜ `f"{value:format_spec}"` ｜ **返回** `str` ｜ **备注** f-string 是最常用写法

```python
format(3.14159, ".2f")     # '3.14'（保留 2 位小数）
f"{3.14159:.2f}"           # '3.14'（等价写法）
format(255, "x")           # 'ff'（十六进制）
format(0.1, ".2%")         # '10.00%'（百分比）
format(1234567, ",")       # '1,234,567'（千分位）
f"{3:03d}"                 # '003'（补零到 3 位）
f"{'Tom':<5}|"             # 'Tom  |'（左对齐补空格，> 右对齐，^ 居中）
```

> ⚠️ `format_spec` 顺序记法：`[[填充]对齐][宽度][,][.精度][类型]`，比如 `{:>8.2f}`、`{:,}`。

### A10　动态执行与反射

#### `eval(expression) / exec(code)` 把字符串当代码执行

**签名** `eval(expr)` 返回表达式的值 ｜ `exec(code)` 执行语句、无返回值 ｜ **返回** 表达式结果 / `None` ｜ **备注** **危险**：别对用户输入用

```python
eval("1 + 2 * 3")               # 7
exec("x = 10\nprint(x * 2)")    # 输出 20
eval("[x * 2 for x in range(3)]")   # [0, 2, 4]
```

> ⚠️ `eval`/`exec` 能执行任意代码，用户能输入的地方用它们等于把电脑交出去。能用 `int()`、`float()`、`ast.literal_eval()` 就别用 `eval`。

#### `compile(source, filename, mode)` 把源码编译成可执行对象

**签名** `compile(source, filename, mode)` ｜ **返回** 代码对象 ｜ **备注** `mode`：`'eval'` / `'exec'` / `'single'`

```python
code = compile("1 + 1", "<string>", "eval")
eval(code)      # 2

code2 = compile("y = 5", "<string>", "exec")
exec(code2)
y               # 5
```

> ⚠️ 日常几乎用不到，只有写表达式引擎、模板、插件时才需要。

#### `globals() / locals()` 取全局 / 局部命名空间字典

**签名** `globals()` ｜ `locals()` ｜ **返回** `dict`（可读） ｜ **备注** 函数里改 `locals()` 通常**不会**真的改变量

```python
x = 1
globals()["x"]        # 1
globals()["x"] = 99   # 真的能改全局变量（不推荐这么写）

def f():
    a = 1
    return locals()   # {'a': 1}（快照）
f()
```

> ⚠️ 调试时打印 `locals()` 看当前有哪些变量很好用；但**不要**靠它修改变量，代码会很难维护。

## 第二部分　各类型常用方法（点号调用）

### B1　list 列表

#### `l[i]、l[i:j]（读取与切片）` 按下标取值 / 切出一段

**签名** `l[i]` ｜ `l[i:j]` ｜ `l[i:j:step]` ｜ **返回** 元素 / 新的 `list` ｜ **备注** 切片**左闭右开**，越界不报错

```python
l = [10, 20, 30, 40, 50]
l[0], l[-1]     # 10, 50（-1 是最后一个）
l[1:3]          # [20, 30]
l[:3]           # [10, 20, 30]
l[3:]           # [40, 50]
l[::-1]         # [50, 40, 30, 20, 10]（反转的新列表，原列表不动）
l[100:200]      # []（切片越界不报错）
# l[100]        # ❌ IndexError：索引越界会报错
```

> ⚠️ 切片永远返回**新列表**：`b = a[:]` 就是一份拷贝，而 `b = a` 只是起别名（改一个两个都变）。

#### `l[i] = x、l[i:j] = [...]` 改单个元素 / 用切片批量改

**签名** `l[i] = x` ｜ `l[i:j] = iterable` ｜ **返回** `None`（原地修改） ｜ **备注** 切片赋值长度可以和原来不同

```python
l = [1, 2, 3]
l[0] = 100                  # [100, 2, 3]
l[1:3] = ["a", "b", "c"]    # [100, 'a', 'b', 'c']（长度不一样也没关系）
l[1:1] = ["插"]             # 在位置 1 插入：[100, '插', 'a', 'b', 'c']
l[1:3] = []                 # 用空列表删除这一段
l[:] = [7, 8]               # 换掉全部内容（列表对象还是同一个）
```

> ⚠️ `l[i:j] = "ab"` 会把字符串拆成字符加进去；`l[:] = ...` 是「原地替换」，别的引用也能看到。

#### `l.append(x)` 末尾追加一个元素

**签名** `l.append(x) -> None` ｜ **返回** `None`（原地修改） ｜ **备注** 把 x 当成**一个整体**加进去

```python
l = [1, 2]
l.append(3)          # [1, 2, 3]
l.append([4, 5])     # [1, 2, 3, [4, 5]]   ← 整个列表变成 1 个元素
l.append("ab")       # [1, 2, 3, [4, 5], 'ab']
len(l)               # 5
```

> ⚠️ **返回 None**！写成 `l = l.append(3)` 会让 `l` 变成 `None`。想一次加多个元素用 `extend`。

#### `l.extend(it)、l += [...]` 末尾批量追加（拆开加）

**签名** `l.extend(iterable)` ｜ `l += iterable` ｜ **返回** `None`（原地修改） ｜ **备注** 把可迭代对象里的元素**逐个**加入

```python
l = [1, 2]
l.extend([3, 4])     # [1, 2, 3, 4]
l.extend("ab")       # [1, 2, 3, 4, 'a', 'b']（字符串被拆成字符）
l += [5]             # [1, 2, 3, 4, 'a', 'b', 5]（等价于 extend，原地改）
l + [6]              # 返回新列表，l 本身不变
```

> ⚠️ `append` 加整体、`extend` 拆开加。`l += [...]` 原地修改（`id` 不变），`l = l + [...]` 是新列表 —— 传参给函数时这个区别很关键。

#### `l.insert(i, x)` 在指定位置插入元素

**签名** `l.insert(i, x) -> None` ｜ **返回** `None`（原地修改） ｜ **备注** 后面的元素整体后移

```python
l = [1, 2, 3]
l.insert(1, "a")     # [1, 'a', 2, 3]
l.insert(0, "头")    # ['头', 1, 'a', 2, 3]
l.insert(99, "尾")   # 下标超出范围 → 插到末尾
l.insert(-1, "x")    # 插到最后一个元素之前
```

> ⚠️ `insert` 是 O(n)：后面的元素都要挪位置。频繁在头部插入用 `collections.deque` 或先 append 再反转。

#### `l.remove(x)` 按**值**删除第一个匹配项

**签名** `l.remove(x) -> None` ｜ **返回** `None`（原地修改） ｜ **备注** 值不存在抛 `ValueError`

```python
l = [1, 2, 3, 2]
l.remove(2)          # [1, 3, 2]（只删第一个匹配的）
# l.remove(9)        # ❌ ValueError: list.remove(x): x not in list
if 3 in l:           # 不确定就先判断
    l.remove(3)
```

> ⚠️ 按**值**删，不是按下标删；想按下标删用 `pop(i)` 或 `del l[i]`。

#### `l.pop(i=-1)` 按下标弹出元素并返回

**签名** `l.pop(i=-1) -> 元素` ｜ **返回** 被删掉的元素 ｜ **备注** 空列表报 `IndexError`

```python
l = [1, 2, 3]
last = l.pop()       # last = 3，l 变成 [1, 2]
first = l.pop(0)     # first = 1，l 变成 [2]
l2 = [1, 2]
# l2.pop(9)          # ❌ IndexError: pop index out of range
# [].pop()           # ❌ IndexError: pop from empty list
```

> ⚠️ **栈**（后进先出）的标准写法就是 `append` 入栈 + `pop()` 出栈。`pop` 有返回值，`remove`/`del` 没有。

#### `l.clear()` 清空列表

**签名** `l.clear() -> None` ｜ **返回** `None`（原地修改） ｜ **备注** 列表对象本身还在

```python
l = [1, 2, 3]
l.clear()            # []
a = [1, 2]
b = a
a.clear()            # b 也变成 []（指向同一个列表）
```

> ⚠️ `clear()` 改的是列表**本身**，所有引用它的变量都会看到变空；想换一个全新空列表用 `l = []`。

#### `del l[i]、del l[i:j]、del l` 按下标 / 切片 / 变量删除

**签名** `del l[i]` ｜ `del l[i:j]` ｜ `del l` ｜ **返回** 无返回值 ｜ **备注** `del l` 删的是**变量名**

```python
l = [1, 2, 3, 4, 5]
del l[0]             # [2, 3, 4, 5]
del l[1:3]           # [2, 5]（按下标删一段）
del l[-1]            # [2]
l2 = [1, 2]
del l2               # 变量和列表一起消失，再引用会 NameError
```

> ⚠️ `del` 是**语句**不是函数（别写 `del(l)` 以为是函数调用）。想按值删用 `remove`。

#### `l.index(x, start, end)` 查值对应的下标

**签名** `l.index(x, start=0, end=len(l))` ｜ **返回** `int` ｜ **备注** 找不到抛 `ValueError`

```python
l = ["a", "b", "c", "b"]
l.index("b")          # 1
l.index("b", 2)       # 3（从下标 2 开始找）
# l.index("z")        # ❌ ValueError: 'z' is not in list
"z" in l              # False（安全的存在性判断）
```

> ⚠️ 只返回**第一个**匹配的下标；不确定是否存在先用 `in`。要所有位置用 `[i for i, v in enumerate(l) if v == x]`。

#### `l.count(x)` 统计值出现次数

**签名** `l.count(x) -> int` ｜ **返回** `int` ｜ **备注** 不存在返回 `0`，不报错

```python
[1, 2, 2, 3].count(2)         # 2
["a", "b", "a"].count("a")    # 2
[1, 2].count(9)               # 0
```

> ⚠️ 是 O(n) 遍历；循环里反复统计同一个列表要考虑先做一次计数（`collections.Counter`）。

#### `x in l` 判断元素是否存在

**签名** `x in l` ｜ `x not in l` ｜ **返回** `bool` ｜ **备注** 列表的 `in` 是 O(n)

```python
l = [1, 2, 3]
3 in l            # True
9 not in l        # True
if 2 in [1, 2]:
    print("有")   # 有
```

> ⚠️ 大数据量里反复判断「在不在」，先转成 `set`（O(1)），能快几个数量级。

#### `l.reverse()` 原地反转

**签名** `l.reverse() -> None` ｜ **返回** `None`（原地修改） ｜ **备注** 想保留原列表用 `reversed()` / `l[::-1]`

```python
l = [1, 2, 3]
l.reverse()               # l 变成 [3, 2, 1]
list(reversed([1, 2, 3])) # [3, 2, 1]（原列表不动）
[1, 2, 3][::-1]           # [3, 2, 1]（切片写法）
```

> ⚠️ `l = l.reverse()` 会让 `l` 变成 `None`（返回 None），这是新手最常见的 bug 之一。

#### `l.sort(key, reverse)` 原地排序

**签名** `l.sort(key=None, reverse=False) -> None` ｜ **返回** `None`（原地修改） ｜ **备注** 想保留原列表用 `sorted(l)`

```python
l = [3, 1, 2]
l.sort()                          # [1, 2, 3]
l.sort(reverse=True)              # [3, 2, 1]

words = ["ccc", "a", "bb"]
words.sort(key=len)               # ['a', 'bb', 'ccc']（按长度排）

students = [{"name": "Tom", "score": 85}, {"name": "Jerry", "score": 92}]
students.sort(key=lambda s: s["score"], reverse=True)   # 按分数降序
sorted(l)                         # 返回新列表，l 不变
```

> ⚠️ `sort()` 原地改、返回 `None`；`sorted()` 返回新列表。排序后如果又改了元素的值，顺序不会自动更新。

#### `l.copy()、l[:]、copy.deepcopy()` 拷贝列表（浅 / 深）

**签名** `l.copy()` ｜ `l[:]` ｜ `list(l)` ｜ `copy.deepcopy(l)` ｜ **返回** 新的 `list` ｜ **备注** 嵌套结构要深拷贝

```python
a = [1, 2, [3, 4]]
b = a                  # 别名：同一个列表，改一个另一个也变
b.append(9)            # a 也变成 [1, 2, [3, 4], 9]

c = a.copy()           # 浅拷贝：外层独立，内层共享
d = a[:]               # 同样效果
e = list(a)            # 同样效果

import copy
f = copy.deepcopy(a)   # 深拷贝：连嵌套内容一起复制

c[2].append(99)        # 内层共享 → a[2] 也变成 [3, 4, 99]
f[2].append(7)         # 深拷贝不受影响，f[2] 是 [3, 4, 7]
```

> ⚠️ 只有一维列表时浅拷贝就够；列表里套列表/字典并且要改内层，必须 `deepcopy`。

#### `列表推导式` 一行生成新列表（推荐写法）

**签名** `[表达式 for x in 可迭代对象 if 条件]` ｜ **返回** 新的 `list` ｜ **备注** 可读性通常优于 `map`/`filter`

```python
[x * 2 for x in range(5)]                      # [0, 2, 4, 6, 8]
[x for x in range(10) if x % 2 == 0]           # [0, 2, 4, 6, 8]（只留偶数）
[x.upper() for x in ["a", "b"]]                # ['A', 'B']
[[r, c] for r in range(2) for c in range(2)]   # [[0, 0], [0, 1], [1, 0], [1, 1]]
```

> ⚠️ 别在推导式里写副作用（比如 append）；嵌套超过两层就改普通 `for` 循环，否则没人读得懂。

#### `列表的 5 个常用组合` 去重 / 扁平化 / 反转 / 求和 / 建二维

**签名** 组合写法速记 ｜ **返回** 新的 `list` / 数值 ｜ **备注** 记住 `[[0]*2]*2` 是错的

```python
nums = [1, 2, 2, 3]
list(dict.fromkeys(nums))                 # [1, 2, 3]（保序去重）
matrix = [[1, 2], [3, 4]]
[col for row in matrix for col in row]    # [1, 2, 3, 4]（扁平化）
sum(nums)                                 # 8
nums[::-1]                                # [3, 2, 2, 1]
[0] * 3                                   # [0, 0, 0]
[[0] * 2 for _ in range(2)]               # [[0, 0], [0, 0]]（二维要这样建）
```

> ⚠️ 建二维列表千万别写 `[[0] * 2] * 2`：里面两行是**同一个列表**，改一行两行都变。

### B2　str 字符串

#### `s[i]、s[i:j]、s[::-1]` 下标与切片（字符串不可改）

**签名** `s[i]` ｜ `s[i:j]` ｜ `s[::-1]` ｜ **返回** 单个字符 / 新字符串 ｜ **备注** 字符串**不可变**，没有 append 之类的方法

```python
s = "python"
s[0], s[-1]     # 'p', 'n'
s[1:4]          # 'yth'
s[:3]           # 'pyt'
s[::-1]         # 'nohtyp'（反转）
len(s)          # 6
# s[0] = "P"    # ❌ TypeError: 'str' object does not support item assignment
s = "P" + s[1:] # ✅ 拼出新字符串：'Python'
```

> ⚠️ 所有字符串方法都**返回新字符串**，原串不变。循环里用 `+=` 拼字符串很慢，先收集到列表最后 `"".join(...)`。

#### `s.split(sep=None, maxsplit=-1)` 按分隔符切成列表

**签名** `s.split(sep=None, maxsplit=-1) -> list` ｜ **返回** `list[str]` ｜ **备注** 不传参数＝按任意空白切，并去掉首尾空白

```python
"a,b,c".split(",")      # ['a', 'b', 'c']
"a b  c".split()        # ['a', 'b', 'c']（多个空格算一个）
"a,b,c".split(",", 1)   # ['a', 'b,c']（最多切 1 次）
"abc".split("x")        # ['abc']（分隔符不存在时返回含原串的列表）
"  a b ".split()        # ['a', 'b']
```

> ⚠️ 切出来的是**字符串列表**，要数字得 `list(map(int, s.split()))`。只想按单个字符拆用 `list("abc")`。

#### `sep.join(iterable)` 把列表拼成字符串

**签名** `sep.join(iterable) -> str` ｜ **返回** `str` ｜ **备注** 顺序是「分隔符.join(列表)」

```python
",".join(["a", "b", "c"])       # 'a,b,c'
"".join(["a", "b"])             # 'ab'
"-".join("abc")                 # 'a-b-c'
",".join(map(str, [1, 2, 3]))   # '1,2,3'（数字要先转字符串）
# ",".join([1, 2, 3])           # ❌ TypeError: sequence item 0: expected str
```

> ⚠️ 别写反成 `list.join(sep)`。列表里混有数字时先 `map(str, ...)`，这是最常见的报错来源。

#### `s.strip() / lstrip() / rstrip()` 去掉两端空白或指定字符

**签名** `s.strip(chars=None)` ｜ `lstrip()` ｜ `rstrip()` ｜ **返回** `str` ｜ **备注** 只处理**两端**，中间不动

```python
"  hi  ".strip()        # 'hi'
"\n hi \n".strip()      # 'hi'（换行、制表符也算空白）
"xxhixx".strip("x")     # 'hi'（去掉两端指定的字符）
"  hi".lstrip()         # 'hi'
"hi  ".rstrip()         # 'hi'
```

> ⚠️ `input()` 读进来的内容常带 `\n`，记得 `strip()`；想把中间空格也去掉用 `replace(" ", "")`。

#### `s.replace(old, new, count=-1)` 替换子串（默认全部替换）

**签名** `s.replace(old, new, count=-1) -> str` ｜ **返回** 新字符串 ｜ **备注** 原字符串不变

```python
"a-b-c".replace("-", "_")      # 'a_b_c'
"aaa".replace("a", "b", 1)     # 'baa'（只替换 1 次）
"a b".replace(" ", "")         # 'ab'（去掉所有空格）
```

> ⚠️ 要「替换一次」必须给 `count`；想按正则替换用 `re.sub()`（`replace` 只认普通子串）。

#### `s.find(sub) / s.index(sub)` 找子串的位置

**签名** `s.find(sub, start)` 找不到返回 `-1` ｜ `s.index(sub, start)` 找不到报 `ValueError` ｜ **返回** `int` ｜ **备注** 只判断在不在用 `in` 最快

```python
s = "hello world"
s.find("o")        # 4
s.find("o", 5)     # 7（从下标 5 开始往后找）
s.find("z")        # -1（找不到返回 -1，不报错）
# s.index("z")     # ❌ ValueError: substring not found
"z" in s           # False
```

> ⚠️ `find` 安全、`index` 会炸，写代码建议用 `find` + 判断 `!= -1`，或者干脆 `if sub in s:`。

#### `s.startswith() / s.endswith()` 判断开头 / 结尾

**签名** `s.startswith(prefix)` ｜ `s.endswith(suffix)` ｜ **返回** `bool` ｜ **备注** 可以同时传多个候选（放在元组里）

```python
"test.py".endswith(".py")         # True
"http://x".startswith("http")     # True
"a.txt".startswith(("a", "b"))    # True（任一匹配即可）
"test.py".endswith((".py", ".md"))  # True
```

> ⚠️ 比 `s[:4] == "http"` 或 `s[-3:] == ".py"` 清楚得多，判断文件类型/协议时用它。

#### `s.upper() / lower() / title() / capitalize()` 大小写转换

**签名** `s.upper()` ｜ `s.lower()` ｜ `s.title()` ｜ `s.capitalize()` ｜ **返回** 新字符串 ｜ **备注** 比较字符串前常先 `lower()`

```python
"Hello".upper()              # 'HELLO'
"Hello".lower()              # 'hello'
"hello world".title()        # 'Hello World'（每个单词首字母大写）
"hello".capitalize()         # 'Hello'（只有首字母大写）
"Hello".lower() == "hello"   # True（忽略大小写比较）
```

> ⚠️ 判断用户输入 `y/n` 时要先 `input().strip().lower()`，否则 `"Y"` 和 `"y"` 匹配不上。

#### `s.count(sub)` 统计子串出现次数

**签名** `s.count(sub, start, end) -> int` ｜ **返回** `int` ｜ **备注** 不存在返回 `0`

```python
"banana".count("a")     # 3
"banana".count("na")    # 2
"banana".count("z")     # 0
```

> ⚠️ 统计**每个**字符出现次数用 `collections.Counter(s)`，一步到位。

#### `sub in s` 子串判断

**签名** `sub in s` ｜ `sub not in s` ｜ **返回** `bool` ｜ **备注** 字符串的 `in` 是子串匹配（比列表的 in 更实用）

```python
"py" in "python"      # True
"z" not in "python"   # True
"" in "python"        # True（空串永远算存在）
```

> ⚠️ 要忽略大小写：`"Py".lower() in s.lower()`。字符串 `in` 是 O(n·m)，超长文本反复查要用正则或 KMP。

#### `s.zfill(n) / ljust / rjust / center` 补位对齐（补零、补空格）

**签名** `s.zfill(width)` ｜ `s.ljust(w, fill)` ｜ `s.rjust(w, fill)` ｜ `s.center(w, fill)` ｜ **返回** 新字符串 ｜ **备注** 只在长度不足时补，够长原样返回

```python
"5".zfill(3)            # '005'（前面补 0）
"5".rjust(3, "0")       # '005'（右对齐补 0）
"5".ljust(3, "-")       # '5--'（左对齐）
"hi".center(6, "*")     # '**hi**'（居中）
"-42".zfill(5)          # '-0042'（负号也算一位）
"12345".zfill(3)        # '12345'（够长不裁剪）
```

> ⚠️ 编号、日期补零常用它，f-string 写法 `f"{5:03d}"` 更常见；对齐输出用 `:<10`、`:>10`、`:^10`。

#### `s.isdigit() / isalpha() / isalnum() / isspace()` 判断字符串内容类型

**签名** `s.isdigit()` ｜ `s.isalpha()` ｜ `s.isalnum()` ｜ `s.isspace()` ｜ **返回** `bool` ｜ **备注** **空字符串**一律返回 `False`

```python
"123".isdigit()      # True
"abc".isalpha()      # True
"a1".isalnum()       # True
"  ".isspace()       # True
"3.14".isdigit()     # False（小数点不算数字）
"".isdigit()         # False（空串）
"-1".isdigit()       # False（负号也不是数字）
```

> ⚠️ `isdigit` **不能**用来校验整数（`"-1"`、`"+1"`、空串都会失败），老老实实 `try: int(s) except ValueError:`。

#### `f-string 格式化` 拼接与格式化（3.6+ 首选）

**签名** `f"{变量:格式}"` ｜ `format(value, spec)` ｜ **返回** `str` ｜ **备注** 比 `%` 和 `.format()` 更好读

```python
name, score = "Tom", 92.5
f"{name} 考了 {score} 分"       # 'Tom 考了 92.5 分'
f"{score:.1f}"                 # '92.5'（1 位小数）
f"{score:.2%}"                 # '9250.00%'（百分比）
f"{1234567:,}"                 # '1,234,567'（千分位）
f"{'左':<5}|{'右':>5}"          # '左    |    右'
print(f"debug: {score=}")      # debug: score=92.5（3.8+ 直接打印变量名和值）
```

> ⚠️ 格式串顺序：`[[填充]对齐][宽度][,][.精度][类型]`，例如 `{x:>8.2f}`。f-string 里的引号别和外面撞。

#### `字符串的 3 个常见套路` 判空 / 忽略大小写 / 处理一行输入

**签名** 组合写法速记 ｜ **返回** `bool` / 新字符串 ｜ **备注** 空串判空直接用 `if not s:`

```python
s = "  Hello World  "
if not s:                      # 判空（空串是假值）
    print("空")
s.strip().lower()              # 'hello world'（清洗输入的标准两步）
out = [x for x in s.split()]   # ['Hello', 'World']
"-".join(out)                  # 'Hello-World'
line = "1 2 3\n".strip().split()   # ['1', '2', '3']（处理一行输入）
```

> ⚠️ 处理输入几乎永远逃不掉 `strip().split()`；反过来输出用 `join`。

### B3　dict 字典

#### `d = {} 创建字典` 键值对的 5 种建法

**签名** `{}` ｜ `dict(...)` ｜ `dict(zip(k, v))` ｜ 字典推导式 ｜ **返回** `dict` ｜ **备注** 键必须可哈希且唯一，值随意

```python
d = {"name": "Tom", "age": 18}
d = dict(name="Tom", age=18)            # 键都是字符串时可这样写
d = dict([("a", 1), ("b", 2)])          # 由键值对序列创建
d = dict(zip(["a", "b"], [1, 2]))       # {'a': 1, 'b': 2}（和 zip 搭配最常用）
d = {k: 0 for k in ["a", "b"]}          # 字典推导式 {'a': 0, 'b': 0}
empty = {}                              # 空字典（空集合是 set()）
```

> ⚠️ Python 3.7+ 字典**保留插入顺序**（遍历顺序 = 插入顺序），但别指望它自动排序，要顺序自己 `sorted(d)`。

#### `d[key] 取值` 按键取 value

**签名** `d[key]` ｜ **返回** 对应的值 ｜ **备注** 键不存在抛 `KeyError`

```python
d = {"a": 1, "b": 2}
d["a"]           # 1
# d["c"]         # ❌ KeyError: 'c'
d["c"] = 3       # 先赋值就有了
```

> ⚠️ 不确定键在不在，一律用 `d.get(key, 默认值)`，别让程序因为 KeyError 崩掉。

#### `d.get(key, default=None)` 安全取值（推荐）

**签名** `d.get(key, default=None)` ｜ **返回** 值 或 `default` ｜ **备注** 找不到**不报错**，返回默认值

```python
d = {"a": 1}
d.get("a")           # 1
d.get("b")           # None（默认返回 None）
d.get("b", 0)        # 0
d.get("b", [])       # []（也可以给列表/字典做默认值）
```

> ⚠️ `get` 和 `d[k]` 只差「键不存在时是否报错」。注意 `d.get(k) or 默认值` 有坑：值本身是 `0` 或 `""` 时会被当成假值替换掉。

#### `d[key] = value` 新增或覆盖

**签名** `d[key] = value` ｜ **返回** `None`（原地修改） ｜ **备注** 键存在就覆盖，不存在就新增

```python
d = {"a": 1}
d["b"] = 2         # 新增 → {'a': 1, 'b': 2}
d["a"] = 99        # 覆盖 → {'a': 99, 'b': 2}
d["a"] += 1        # {'a': 100, 'b': 2}（键存在时可以直接自增）
counts = {}
counts["x"] = counts.get("x", 0) + 1   # 计数惯用法
```

> ⚠️ `d["k"] += 1` 在键**不存在**时会 KeyError，计数必须写成 `d[k] = d.get(k, 0) + 1`。

#### `d.update(other)` 批量新增 / 覆盖

**签名** `d.update(other)` ｜ **返回** `None`（原地修改） ｜ **备注** 同名的键会被覆盖

```python
d = {"a": 1}
d.update({"b": 2, "a": 9})     # {'a': 9, 'b': 2}（a 被覆盖）
d.update([("c", 3)])           # 也可以传键值对序列
d.update(zip(["d"], [4]))      # 也可以传 zip
```

> ⚠️ `update` 是「就地合并」；想得到新字典用 `d1 | d2` 或 `{**d1, **d2}`，原字典不动。

#### `d.setdefault(key, default=None)` 不存在才初始化（分组神器）

**签名** `d.setdefault(key, default=None)` ｜ **返回** 该键的值 ｜ **备注** 存在则原值不动；不存在则插入并返回默认值

```python
d = {"a": 1}
d.setdefault("a", 100)     # 返回 1，d 不变
d.setdefault("b", 0)       # 返回 0，d 变成 {'a': 1, 'b': 0}

groups = {}                # 按城市分组（很常用的套路）
for name, city in [("Tom", "北京"), ("Jerry", "上海"), ("Bob", "北京")]:
    groups.setdefault(city, []).append(name)
groups     # {'北京': ['Tom', 'Bob'], '上海': ['Jerry']}
```

> ⚠️ 和 `get` 的区别：`get` 只取值，`setdefault` 缺失时会**写回**字典。`groups.setdefault(city, []).append(x)` 是分组的标准一行写法。

#### `d1 | d2（3.9+）` 合并两个字典（生成新对象）

**签名** `d1 | d2` ｜ `d1 |= d2` ｜ **返回** 新 `dict` / `None` ｜ **备注** 右边的同名键覆盖左边

```python
{"a": 1} | {"b": 2}     # {'a': 1, 'b': 2}
{"a": 1} | {"a": 9}     # {'a': 9}（右边赢）
d = {"a": 1}
d |= {"c": 3}           # 就地合并：d 变成 {'a': 1, 'c': 3}
{**{"a": 1}, **{"b": 2}}   # 兼容老版本（3.5+）的写法
```

> ⚠️ `|` 需要 Python 3.9+；字典**不能**用 `+` 合并（会 TypeError）。

#### `d.keys() / d.values() / d.items()` 取键 / 值 / 键值对

**签名** `d.keys()` ｜ `d.values()` ｜ `d.items()` ｜ **返回** 视图对象（可迭代） ｜ **备注** 要按顺序用就 `list(...)` 包一层

```python
d = {"a": 1, "b": 2}
list(d.keys())       # ['a', 'b']
list(d.values())     # [1, 2]
list(d.items())      # [('a', 1), ('b', 2)]
sorted(d.items())    # [('a', 1), ('b', 2)]（按键排序）
"a" in d.keys()      # True（等价于 "a" in d）
sorted(d)            # ['a', 'b']（对字典用 sorted 默认排键）
```

> ⚠️ 视图是「活的」：拿到之后再改字典，视图内容也会跟着变。想固定住就 `list(...)` 转出来。

#### `key in d` 判断键是否存在

**签名** `key in d` ｜ `key not in d` ｜ **返回** `bool` ｜ **备注** 判断的是**键**，不是值

```python
d = {"a": 1, "b": 2}
"a" in d            # True
1 in d              # False（1 是值不是键）
"x" not in d        # True
1 in d.values()     # True（判断值要显式写 values，O(n) 慢）
```

> ⚠️ `if k in d:` 比 `d.get(k)` 更快、也没有默认值歧义，是判断键存在的标准写法。

#### `d.pop(key, default)` 弹出键并返回值

**签名** `d.pop(key, default)` ｜ **返回** 被删掉的值 ｜ **备注** 没给 default 且键不存在时 `KeyError`

```python
d = {"a": 1, "b": 2}
d.pop("a")           # 1，d 变成 {'b': 2}
d.pop("z", None)     # None（给了默认值就不报错）
d.pop("z", 0)        # 0
```

> ⚠️ 和 `del d[k]` 的区别：`pop` **有返回值**、能带默认值；`del` 没有返回值、键不存在直接报错。

#### `d.popitem()` 删掉并返回最后一个键值对

**签名** `d.popitem()` ｜ **返回** `(key, value)` 元组 ｜ **备注** 空字典报 `KeyError`；3.7+ 是后进先出（LIFO）

```python
d = {"a": 1, "b": 2}
d.popitem()          # ('b', 2)（最后插入的那个），d 变成 {'a': 1}
d.popitem()          # ('a', 1)
# {}.popitem()       # ❌ KeyError: 'popitem(): dictionary is empty'
```

> ⚠️ 写缓存淘汰（LRU）之类场景会用到；日常删某个键还是用 `pop` 或 `del`。

#### `del d[k] / d.clear()` 删除一个键 / 清空字典

**签名** `del d[key]` ｜ `d.clear()` ｜ **返回** 无返回值 / `None` ｜ **备注** `del` 键不存在报 `KeyError`

```python
d = {"a": 1, "b": 2}
del d["a"]           # {'b': 2}
# del d["z"]         # ❌ KeyError: 'z'
d.clear()            # {}
```

> ⚠️ `clear()` 清空的是字典**本身**，其他指向它的变量也会变空；想换新字典用 `d = {}`。

#### `遍历字典` 3 种遍历方式 + 改值的正确姿势

**签名** `for k in d` ｜ `for k, v in d.items()` ｜ **返回** 键 / 键值对 ｜ **备注** 遍历中增删键会 `RuntimeError`

```python
d = {"a": 1, "b": 2}
for k in d:                 # 只遍历键
    print(k)                # a   b

for k, v in d.items():      # 最常用：同时拿键和值
    print(k, v)             # a 1    b 2

for v in d.values():        # 只遍历值
    print(v)                # 1   2

for k in list(d.keys()):    # 边遍历边改：先取 list 快照
    d[k] = d[k] * 10        # {'a': 10, 'b': 20}
```

> ⚠️ 遍历时直接 `d["c"] = 3` 或 `del d[k]` 会报 `RuntimeError: dictionary changed size during iteration`，要先取快照或先收集要改的键。

#### `d.copy() / copy.deepcopy()` 拷贝字典（浅 / 深）

**签名** `d.copy()` ｜ `dict(d)` ｜ `copy.deepcopy(d)` ｜ **返回** 新 `dict` ｜ **备注** 嵌套的值要深拷贝

```python
d = {"a": [1, 2]}
e = d                # 别名：改 e 就是改 d
e["b"] = 3           # d 也多了 'b'

f = d.copy()         # 浅拷贝：外层独立
f["c"] = 4           # d 没有 'c'
f["a"].append(9)     # ⚠️ 内层共享 → d["a"] 也变成 [1, 2, 9]

import copy
g = copy.deepcopy(d) # 深拷贝：彻底独立
```

> ⚠️ 只改「键」用浅拷贝就够；要改「值里面的可变对象」必须 `deepcopy`。

#### `字典推导式与 Counter` 计数、排行、反转、筛选一行搞定

**签名** `{k: v for ...}` ｜ `collections.Counter` ｜ **返回** 新 `dict` ｜ **备注** 统计场景优先用 `Counter`

```python
# 1) 计数（词频）
import collections
collections.Counter("a b a c a".split())   # Counter({'a': 3, 'b': 1, 'c': 1})
counts = {}
for w in "a b a c a".split():
    counts[w] = counts.get(w, 0) + 1       # 不用 Counter 的等价写法

# 2) 按值排序取前 2 名
scores = {"Tom": 85, "Jerry": 92, "Bob": 78}
sorted(scores.items(), key=lambda kv: kv[1], reverse=True)[:2]
# [('Jerry', 92), ('Tom', 85)]

# 3) 反转键值（前提：值唯一）
{v: k for k, v in {"a": 1, "b": 2}.items()}    # {1: 'a', 2: 'b'}

# 4) 筛出分数 >= 90 的
{k: v for k, v in scores.items() if v >= 90}   # {'Jerry': 92}
```

> ⚠️ `Counter` 是 dict 的子类，`most_common(n)` 直接给排行榜；统计场景优先用它。

### B4　set 集合

#### `set() 创建集合` 去重容器：无序、不重复

**签名** `{1, 2}` ｜ `set(iterable)` ｜ 集合推导式 ｜ **返回** `set` ｜ **备注** 空集合只能写 `set()`，`{}` 是空字典

```python
s = {1, 2, 3}
s = set([1, 2, 2, 3])    # {1, 2, 3}（自动去重）
s = set("hello")         # {'h', 'e', 'l', 'o'}（重复的 l 只留一个）
empty = set()            # ✅ 空集合
empty = {}               # ❌ 这是空字典！
s = {x for x in range(5) if x % 2 == 0}   # {0, 2, 4}
```

> ⚠️ 元素必须**可哈希**（不可变）：`{1, [2]}` 会 `TypeError`，要放组合值就用元组 `{(1, 2), (3, 4)}`。

#### `s.add(x)` 加一个元素

**签名** `s.add(x) -> None` ｜ **返回** `None`（原地修改） ｜ **备注** 已存在时不报错、只是不重复加

```python
s = {1, 2}
s.add(3)          # {1, 2, 3}
s.add(1)          # 还是 {1, 2, 3}
# s.add([4])      # ❌ TypeError: unhashable type: 'list'
```

> ⚠️ `add` 没有返回值（和 list 的 append 一样）；要一次加多个用 `update`。

#### `s.update(iterable)` 批量加元素

**签名** `s.update(*iterables)` ｜ **返回** `None`（原地修改） ｜ **备注** 相当于「并集」后原地更新

```python
s = {1, 2}
s.update([3, 4])      # {1, 2, 3, 4}
s.update("ab")        # {1, 2, 3, 4, 'a', 'b'}（字符串被拆成字符）
s |= {9}              # 等价写法（并集赋值）
```

> ⚠️ 带 `update` 的是「批量」，`add` 是单个 —— 和 list 的 append / extend 一个道理。

#### `s.remove(x) / s.discard(x)` 删除元素（报错 / 不报错）

**签名** `s.remove(x)` 不存在报 `KeyError` ｜ `s.discard(x)` 不存在不报错 ｜ **返回** `None`（原地修改） ｜ **备注** 不确定在不在就用 `discard`

```python
s = {1, 2, 3}
s.remove(1)      # {2, 3}
# s.remove(9)    # ❌ KeyError: 9
s.discard(9)     # ✅ 什么都不发生，也不报错
s.discard(2)     # {3}
```

> ⚠️ 这是 set 最常被问的一对：**remove 会炸、discard 不会**。处理来源不确定的数据时统一用 `discard`。

#### `s.pop() / s.clear()` 随机删一个 / 清空

**签名** `s.pop()` ｜ `s.clear()` ｜ **返回** 被删的元素 / `None` ｜ **备注** 空集合 `pop` 报 `KeyError`

```python
s = {1, 2, 3}
x = s.pop()      # 随机删掉一个并返回它（set 没有「第几个」的概念）
s.clear()        # set()
# set().pop()    # ❌ KeyError: 'pop from an empty set'
```

> ⚠️ `s.pop()` 删的是「任意一个」，别指望顺序；要按顺序处理先 `sorted(s)` 转成 list。

#### `x in s` 判断元素是否存在（O(1)）

**签名** `x in s` ｜ `x not in s` ｜ **返回** `bool` ｜ **备注** 比 list 的 in 快几个数量级

```python
s = {1, 2, 3}
3 in s            # True
9 not in s        # True

seen = set()      # 经典用法：记录见过的元素
for x in [1, 2, 3, 2]:
    if x in seen:
        print("重复:", x)   # 重复: 2
    seen.add(x)
```

> ⚠️ 「是否见过 / 是否重复」的判断，先把容器换成 set：列表 O(n)、集合 O(1)，数据量大时差的就是秒和分钟。

#### `a | b、a & b、a - b、a ^ b` 交并差（集合的杀手锏）

**签名** `a | b` 并集 ｜ `a & b` 交集 ｜ `a - b` 差集 ｜ `a ^ b` 对称差 ｜ **返回** 新 `set` ｜ **备注** 运算符生成新集合；`|=` `&=` `-=` `^=` 是就地修改

```python
a = {1, 2, 3}
b = {3, 4}

a | b    # {1, 2, 3, 4}    并集：两边都要        等价 a.union(b)
a & b    # {3}             交集：两边都有        等价 a.intersection(b)
a - b    # {1, 2}          差集：在 a 不在 b     等价 a.difference(b)
a ^ b    # {1, 2, 4}       对称差：只在其中一边   等价 a.symmetric_difference(b)

a |= b   # a 变成 {1, 2, 3, 4}（就地并集）
```

> ⚠️ 找「两个列表的共同元素」用 `set(A) & set(B)` 一行搞定，比双重循环快得多。

#### `a.issubset / issuperset / isdisjoint` 包含关系判断

**签名** `a.issubset(b)` ｜ `a.issuperset(b)` ｜ `a.isdisjoint(b)` ｜ **返回** `bool` ｜ **备注** 也可写 `a <= b`、`a >= b`

```python
a = {1, 2, 3}
b = {3, 4}
c = {3}

a.issubset(b)      # False：a 是 b 的子集吗？   也可写 a <= b
a.issuperset(b)    # False：a 包含 b 吗？       也可写 a >= b
c.issubset(a)      # True
c <= a             # True
a.isdisjoint(b)    # False：两个集合完全没有交集吗？
a.isdisjoint({9})  # True
```

> ⚠️ `<=` 表示「包含或不相等」，严格子集用 `<`；`isdisjoint` 用来看两组数据是否有冲突。

#### `sorted(s)` 集合要按顺序看：先转 list

**签名** `sorted(s)` ｜ `list(s)` ｜ **返回** `list` ｜ **备注** set 无序无下标，不能 `s[0]`

```python
s = {3, 1, 2}
sorted(s)        # [1, 2, 3]（排序后是 list）
sorted(s)[0]     # 1
list(s)          # [1, 2, 3]（顺序不保证，只是转类型）
# s[0]           # ❌ TypeError: 'set' object is not subscriptable
```

> ⚠️ set 不能索引、切片、用 `+` 拼接；要「有序的集合」就存成 list，只在判断存在时临时转 set。

#### `去重的 3 种写法` set / dict.fromkeys / 嵌套去重

**签名** 组合写法速记 ｜ **返回** `list` / `set` ｜ **备注** set 去重会**打乱顺序**

```python
nums = [1, 2, 2, 3, 1]
list(set(nums))              # [1, 2, 3]（最快，但顺序不保证）
list(dict.fromkeys(nums))    # [1, 2, 3]（保序去重，推荐）

A, B = ["a", "b", "c"], ["b", "c", "d"]
set(A) & set(B)              # {'b', 'c'}（共同元素）
set(A) - set(B)              # {'a'}（A 独有）
set(A) | set(B)              # {'a', 'b', 'c', 'd'}（合并去重）

matrix = [[1, 2], [2, 3], [1, 2]]
seen = {tuple(row) for row in matrix}   # 嵌套列表去重：先转元组
```

> ⚠️ 要保序用 `dict.fromkeys`；嵌套结构（列表套列表）不能直接进 set，先 `tuple()` 转换。

### B5　tuple 元组

#### `t = (1, 2) 创建元组` 不可变序列，方法只有 2 个

**签名** `t = 1, 2` ｜ `t = (1,)` ｜ `tuple(iterable)` ｜ **返回** `tuple` ｜ **备注** 单元素**必须**带逗号

```python
t = (1, 2, 3)
t = 1, 2, 3          # 括号可以省略，用逗号隔开就是元组
one = (5)            # ❌ 这是 int 5，不是元组
one = (5,)           # ✅ 单元素元组必须带逗号
empty = ()           # 空元组
tuple([1, 2])        # (1, 2)（由其他可迭代对象转换）
tuple("ab")          # ('a', 'b')
list((1, 2, 3))      # [1, 2, 3]（反向转换）
```

> ⚠️ 忘了逗号的 `(5)` 是整数，这种 bug 很隐蔽 —— 不确定就用 `type(x)` 确认一下。

#### `t[i]、t[i:j]（读取）` 下标与切片（不能改）

**签名** `t[i]` ｜ `t[i:j]` ｜ **返回** 元素 / 新 `tuple` ｜ **备注** 赋值改元素会 `TypeError`

```python
t = (10, 20, 30, 40)
t[0], t[-1]    # 10, 40
t[1:3]         # (20, 30)   ← 切出来还是元组
t[::-1]        # (40, 30, 20, 10)
len(t)         # 4
# t[0] = 5     # ❌ TypeError: 'tuple' object does not support item assignment
```

> ⚠️ 元组切片仍返回元组（列表切片返回列表）；要改内容只能整体重建，见下面「重建」那条。

#### `t.count(x) / t.index(x)` 元组只有这两个方法

**签名** `t.count(x)` ｜ `t.index(x)` ｜ **返回** `int` ｜ **备注** 统计和查找，其他功能都得靠内置函数

```python
t = (10, 20, 30, 20)
t.count(20)              # 2
t.index(20)              # 1（第一个匹配的下标）
20 in t                  # True
len(t)                   # 4
min(t), max(t), sum(t)   # 10, 30, 80（这些是内置函数，不是方法）
sorted(t)                # [10, 20, 20, 30]（注意返回 list）
```

> ⚠️ 元组没有 append / remove / sort；要这些功能就先 `list(t)` 转成列表，处理完再 `tuple(...)`。

#### `解包：a, b = t` 把元组拆成多个变量（最常用）

**签名** `a, b = t` ｜ `a, *rest = t` ｜ **返回** 各自的变量 ｜ **备注** 变量个数和元素个数必须匹配

```python
a, b = (1, 2)             # a=1, b=2
a, b = b, a               # 交换两个变量，不用临时变量
x, y = (3, 5)             # 坐标拆开

first, *rest = (1, 2, 3, 4)   # first=1, rest=[2, 3, 4]（* 收集剩余，得到 list）
*init, last = (1, 2, 3, 4)    # init=[1, 2, 3], last=4

def min_max(nums):
    return min(nums), max(nums)   # 返回的其实是元组
lo, hi = min_max([3, 1, 4])       # lo=1, hi=4

for name, age in [("Tom", 5), ("Jerry", 6)]:
    print(name, age)
```

> ⚠️ 个数不匹配会 `ValueError: too many values to unpack`；`for k, v in d.items()` 也是解包。

#### `重建元组（因为不可变）` 要「改」就得造个新的

**签名** `t = t[:i] + (x,) + t[i+1:]` ｜ `t += (x,)` ｜ **返回** 新的 `tuple` ｜ **备注** `+=` 是生成新对象，不是原地改

```python
t = (1, 2)
t = (9,) + t[1:]     # 拼出新元组 (9, 2)，原来那个没变

t2 = t
t += (3,)            # 生成新对象，t2 仍指向旧元组
print(t, t2)         # (9, 2, 3) (9, 2)

# ⚠️ 「不可变」只到第一层：里面装 list 时照样能改
t3 = (1, [2, 3])
t3[1].append(4)      # 合法！t3 变成 (1, [2, 3, 4])
```

> ⚠️ `t += (...)` 和列表的 `l += [...]` 行为**不同**：列表是原地改，元组是造新对象 —— 别的变量还看着旧值。

#### `元组当 dict 的键 / 进 set` 坐标、组合键的好帮手

**签名** `{(1, 2): "起点"}` ｜ `{(1, 2), (3, 4)}` ｜ **返回** 可哈希，能做键和集合元素 ｜ **备注** 列表、字典都不能当键

```python
location = {(1, 2): "起点", (3, 4): "终点"}   # 元组做 dict 的键
location[(1, 2)]        # '起点'
{(1, 2), (3, 4)}        # 可以放进 set
hash((1, 2))            # 可哈希
# {[1, 2]}              # ❌ TypeError: unhashable type: 'list'
list({"a": 1}.items())  # [('a', 1)]（键值对本身就是元组）
```

> ⚠️ 需要「多维坐标」「(行, 列) 组合键」时就用元组；这也是嵌套列表要去重时先 `tuple()` 的原因。

#### `tuple 还是 list？` 一句话选择标准

**签名** `tuple` 不可变 ｜ `list` 可变 ｜ **返回** 容器 ｜ **备注** 拿不准就用 list

```python
t = (1, 2, 3)
l = [1, 2, 3]
# 元组：不可变 → 更安全、可哈希、省内存；方法只有 count / index
# 列表：可变   → 能增删改；有 append / pop / sort 等一大堆方法
tuple(l)    # (1, 2, 3)   列表 → 元组
list(t)     # [1, 2, 3]   元组 → 列表
sorted(t)   # [1, 2, 3]   要排序就先转成 list
```

> ⚠️ 数据固定不变（坐标、RGB、配置项、函数返回多个值）用元组；需要增删改、要排序就用列表。

## 学习建议

1. **先记高频 15 个**：`len` `range` `enumerate` `zip` `sorted` `map` `filter` `min` `max` `sum` `any` `all` `print` `input` `open` —— 覆盖 80% 日常场景。
2. **方法先记两条规律**：容器方法多数**原地修改、返回 `None`**（`append` / `sort` / `add` / `update`…）；`sorted()`、`reversed()` 这类**内置函数**返回新对象、不动原数据。
3. **选容器先问 3 句话**：要顺序、要增删 → `list`；要按键取值 → `dict`；要去重 / 判重 / 交并差 → `set`；固定不变或要当 key → `tuple`。
4. **类型判断用 `isinstance`**，别用 `type`（前者支持继承，官方推荐）。
5. **多写推导式**：`[x * 2 for x in l]` 比 `map` / `filter` 好读；但别为了短而堆两层以上嵌套。
6. **别背签名**：`help(len)`、`len.__doc__`，或者直接查这份文件的索引。
