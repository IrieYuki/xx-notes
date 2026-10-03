# Python 速查笔记：现有结构清单与候选缺口

## 文件

`~/My_Python_Study/note/`（git 仓库 `IrieYuki/My-Python-Study`）：

- `Python内置函数速查笔记.md` —— 唯一一份讲语法 / 内置函数与容器方法的笔记（用户最常要求扩充的就是这份），已按 §2 的定稿结构重排：104 条用法
- `Numpy常用函数速查笔记.md`、`Pandas常用函数速查笔记.md`、`Matplotlib常用函数速查笔记.md`、`Seaborn常用函数速查笔记.md`
- 同目录还有 `titanic.ipynb` / `titanic.xlsx`（练习数据，与笔记无关）

## 先拿真实清单，别信本文件

笔记会被持续追加，动手前重新生成清单：

```bash
grep -n '^#\{2,4\} ' ~/My_Python_Study/note/Python内置函数速查笔记.md
```

上次重排后的骨架（每条含「签名 ｜ 返回 ｜ 备注」三格 + 示例 + 可选 ⚠️）：

```
# Python 常用函数与方法速查笔记
## 怎么用这份文件
## 索引 · 速查表                     （一行一个用法，链接到正文条目）
## 第一部分　内置函数（直接写名字调用）
### A1　类型转换(7)          A2 数学与数值(4)       A3 聚合与判断(4)
### A4　序列生成与迭代(4)     A5 排序与筛选(5)       A6 类型与属性(6)
### A7　类与装饰器(1)         A8 字符串表示与编码(3)  A9 输入输出与格式化(4)
### A10　动态执行与反射(3)
## 第二部分　各类型常用方法（点号调用）
### B1　list 列表(17)   B2　str 字符串(14)   B3　dict 字典(15)
### B4　set 集合(10)     B5　tuple 元组(7)
## 学习建议
```

## 候选缺口（用户可能接着要点）

- **推导式与生成器表达式**：`[x for x in ...]`、`{k: v for ...}`、`(x for x in ...)`（B1 里点过列表推导式，但没有独立条目）
- **异常处理**：`try/except/else/finally`、`raise`、`assert`、常见内置异常（KeyError / ValueError / TypeError / RuntimeError）
- **文件与序列化**：`json.load/loads/dump/dumps`、`csv`、`pathlib.Path`（`open` 已在 A9）
- **collections / itertools**：`Counter`（B3 里提过）、`defaultdict`、`deque`、`chain/combinations`
- **正则 re**：`search/match/findall/sub/split`
- **类与面向对象**：`self`、继承、`__init__`/`__repr__` 等魔术方法
- 其余四份 Numpy / Pandas / Matplotlib / Seaborn 笔记目前以「函数签名」为主，若要补「对象方法」可按同一结构（A/B 分类 + 索引前置）处理

## 扩充时的检查项

- 新条目插到对应分类末尾，同时在**索引表**同分类末尾加一行（顺序与正文一致）；新增分类要同步开头「怎么用这份文件」的顺序说明。
- 条目名字带接收者前缀保证唯一（`l.` `s.` `d.` `t.`），标题里的名字会被索引行镜像。
- 三个加粗字段（签名 ｜ 返回 ｜ 备注）永远都在；跨板块重复是有意的，别去重。
- 示例跑 `scripts/verify_notes_examples.py <文件>`，坑点用 ❌/✅ 对照。
