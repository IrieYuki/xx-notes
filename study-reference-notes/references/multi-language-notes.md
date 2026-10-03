# 多语言速查笔记：约定、骨架与命令

适用：正本仓库 `~/xx/xx-notes/notes/` 下的 C / C++ / MySQL 那几份（Python 那五份见
`python-quickref-inventory.md`）。新建一门语言的笔记时，**先抄现成笔记的分类顺序与条目粒度**，再逐条换内容。

## 各语言分类骨架（照这个顺序扩写）

**C（63 条）**：A1 程序结构与编译运行 → A2 数据类型与输入输出 → A3 运算符 → A4 分支与选择 →
A5 循环 → A6 数组 → A7 字符串（字符数组）→ A8 函数 → A9 指针 → A10 结构体与自定义类型 →
A11 内存管理 → A12 文件操作 → A13 常用标准库函数 → A14 预处理与多文件

**C++（55 条）**：B1 与 C 的差异与输入输出 → B2 基础类型、auto 与引用 → B3 std::string →
B4 函数进阶 → B5 类与对象 → B6 继承与多态 → B7 运算符重载与函数对象 → B8 STL 容器 →
B9 迭代器与范围 for → B10 算法库 algorithm / numeric → B11 智能指针与 RAII → B12 异常处理 →
B13 文件与流 → B14 现代特性

**MySQL（43 条）**：C1 基础语法与数据类型 → C2 建表与修改表 → C3 插入数据 → C4 查询基础 →
C5 条件与运算符 → C6 聚合函数与分组 → C7 多表连接 → C8 子查询与条件逻辑 → C9 更新与删除 →
C10 常用函数（字符串 / 数字 / 类型转换）→ C11 索引 → C12 事务与视图

**Linux（85 条，小白版）**：A1 终端与命令 → A2 目录与路径 → A3 文件操作 → A4 看文件内容 →
A5 查找与搜索 → A6 管道、重定向与文本处理 → A7 权限与用户 → A8 进程与作业 →
A9 网络与远程 → A10 压缩与打包 → A11 系统信息与软件包

顺序就是教学顺序（A1 → 末章一层层往上），不要把难点（指针、智能指针、模板）提前。

## 条目与渲染契约

- JSONL：首行 `kind="meta"`（`{title, lang, intro, tail}`，**`lang` 是围栏语言**：`c` / `cpp` / `sql` / 默认 `python`），
  其余 `kind="entry"`（`{cat, name, one, sig, ret, note, code, warn}`；SQL 另用 `out` 放结果块，`alt` 放隐藏的校验等价写法）。
- `sig` 里**不能出现全角 `｜`**（会破坏「签名 ｜ 返回 ｜ 备注」三格），用 ` / ` 分隔。
- 渲染器 / 校验器一律用正本路径：
  ```bash
  SK=~/.hermes/skills/note-taking/verified-cheatsheet-notes/scripts
  python3 $SK/render_notes.py cpp_entries.jsonl /tmp/cpp_full.md          # 索引/正文/锚点同源
  python3 $SK/verify_c_blocks.py --lang cpp /tmp/cpp_full.md               # C 用 --lang c
  python3 $SK/verify_sql_blocks.py /tmp/mysql_full.md
  python3 $SK/verify_code_blocks.py 笔记.md                                # Python 那份（库笔记用装了库的解释器）
  $SK/verify_sh_blocks.py --fill linux_entries.jsonl                       # Linux：先跑出真实输出写回 out
  python3 $SK/verify_sh_blocks.py notes/Linux常用指令速查笔记.md            # Linux：再校验（容器里跑）
  ```
- 每批 15~20 条落一次盘；生成器失败就 `sys.exit`，绝不让跑不通的示例进笔记。

## 三份笔记的示例约定

- **C / C++**：每个代码块是完整程序；顶部 `// 输入：Tom 18` 是 stdout 用的 stdin；
  尾部 `// 运行结果：…`（多行时逐行 `// `）由生成器从真实运行结果写出。
  文件读写示例在**临时目录**里跑（校验器把子进程的 cwd 设成临时目录，否则会往工作区落文件）。
  坑：数组传参 `sizeof` 的编译警告是**故意的**（正好对应「数组会退化成指针」），可以在 ⚠️ 里点明。
- **SQL**：示例下跟一个 ```text 结果块（`列 | 列` + `（共 N 行）`，DML/DDL 写 `（影响 N 行）`/`（语句已执行）`）。
  笔记开头的示例数据表（schema + seed）由 `describe_seed()` 从真正跑的那份数据生成，保证与示例一致；
  比对时逐行 rstrip（对齐用的空格不是错）。校验器识别到结果块以「（MySQL 专有语法」开头就跳过该条。
  查询结果表不要做列对齐填充（中文宽度算不准，看着更乱）。
- **Linux / bash**：每个块是可以在自己机器上直接粘的一段命令；示例下跟一个 ```text 结果块（真实 stdout）。
  脚本会先跑「示例环境」SETUP（在家目录造 `linux-lab/`，文件用 `touch -t` 固定修改时间），再在**新容器**里
  跑该块，所以块之间互不污染、输出可复现。时间 / PID / IP / 内存 / 进程列表这类输出每次都不一样：
  结果块首行写「（结构示例：…）」只跑不比对；要真网络或真主机的写「（未实跑：…）」直接跳过。
  汇报时这三类分开报数（比对通过 / 结构示例 / 未实跑），别把「跑通没比对」算成「通过」。

## 诚实标注（这条不能被省）

本机没有的服务/库，就不能声称验过：MySQL 专有语法写「未实跑」、README 里写清「复核 37 条 / 跳过 6 条」、
汇报时把「跳过」和「通过」分开报。用户明确说过要「实跑验证后的结论」——跳过就是跳过。
