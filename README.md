# xx-notes

学习笔记 + Hermes Agent 技能（skill）仓库，放的是「辅助学习 / 整理学习资料」这类工作流。
每个子目录一份 `SKILL.md`，外加可选的 `references/`（规范与清单）、`scripts/`（可直接跑的脚本）。
速查笔记统一放在 `notes/`，这个目录同时是一个 Obsidian 库（`.obsidian/` 只提交插件与外观配置，
`workspace.json` 是窗口布局，已写进 `.gitignore`，不入库）。

| 技能 | 用途 |
|------|------|
| `verified-cheatsheet-notes/` | 把速查笔记整理成能长期查阅的形态，并用脚本验证示例注释与真实输出一致 |
| `study-reference-notes/` | 用户的学习笔记写在哪、怎么写：先定位正本（`notes/`）还是链接桩，再按固定结构写速查笔记 / 刷题笔记 |
| `packet-capture/` | 抓包与过滤器速查：dumpcap / tshark / Wireshark 命令、BPF 捕获过滤器、显示过滤器、xxd 转明文（网络安全学习用，副本在 `~/.hermes/skills/security/`） |

## 速查笔记

> 本仓库是速查笔记的**正本**；`My-Python-Study` 里的同名文件只是链接桩，改动一律在这里做。

| 笔记 | 内容 / 状态 |
|------|------|
| `notes/Python内置函数速查笔记.md` | Python 内置函数 + list / str / dict / set / tuple 常用方法，104 条用法。**已按新格式整理并校验通过**（索引表在最前，点「用法」直接跳到正文） |
| `notes/Numpy常用函数速查笔记.md` | NumPy 创建 / 索引 / 变形 / 运算 / 统计 / 拼接 / 线代，49 条用法。**已按新格式整理并校验通过** |
| `notes/Pandas常用函数速查笔记.md` | Pandas 创建读写 / 查看 / 选择 / 清洗 / 变换 / 分组 / 合并 / 统计 / 时间 / 字符串，52 条用法。**已按新格式整理并校验通过**（pandas 3.0 的 API 变动都标了） |
| `notes/Matplotlib常用函数速查笔记.md` | Matplotlib 画布 / 折线散点柱状直方饼图箱线 / 坐标轴 / 图例 / 子图 / 样式 / 保存，29 条用法。**已按新格式整理并校验通过** |
| `notes/Seaborn常用函数速查笔记.md` | Seaborn 主题 / 关系图 / 分布图 / 分类图 / 回归图 / 矩阵图 / 网格，27 条用法。**已按新格式整理并校验通过** |
| `notes/C语言常用语法速查笔记.md` | C：程序结构 / 数据类型 / 运算符 / 分支循环 / 数组 / 字符串 / 函数 / 指针 / 结构体 / 内存 / 文件 / 标准库 / 预处理，63 条用法。每条都是**完整可编译程序**，`// 运行结果：` 是真实输出 |
| `notes/C++常用语法速查笔记.md` | C++：输入输出 / auto 与引用 / std::string / 函数进阶 / 类与对象 / 继承多态 / 运算符重载 / STL 容器与算法 / 智能指针 / 异常 / 文件流 / 现代特性，55 条用法。同样每条都是完整可编译程序 |
| `notes/MySQL常用语法速查笔记.md` | **从小白到精通** MySQL：环境与连接 / 基础语法与类型 / 建表 / 插入 / 查询 / 条件 / 聚合分组 / 多表连接 / 子查询 / 更新删除 / 常用函数 / 索引 / 事务与视图 / 窗口函数与 CTE / 执行计划与优化 / **SQL 注入必备**，**62 条**。全部在**本机真 MySQL 8.4.11** 上实跑，结果原始粘贴；注入节标 🔒 |
| `notes/Linux常用指令速查笔记.md` | **小白向** Linux 指令：终端与命令 / 目录路径 / 文件操作 / 看文件 / 查找搜索 / 管道与重定向 / 权限用户 / 进程作业 / 网络远程 / 压缩打包 / 系统信息，66 条（同命令选项合并）。示例在 **Ubuntu 24.04 容器**里实跑，输出即真实输出 |
| `notes/网络安全工具速查笔记.md` | 网络安全侦察工具：**零 基础概念**（IP/端口/协议/DNS 体系，真小白入门）+ DNS 查询（dig/nslookup/host）、whois、主机发现（arping/fping）、端口扫描与指纹（nmap）、抓包（dumpcap/tshark）、过滤器、xxd、Google Hacking，26 条。示例在**用户 Mac + 自建靶场/Kali**上实跑 |
| `notes/前端设计速查笔记.md` | **小白向** 前端三件套合一（HTML → CSS → JavaScript）：HTML 结构 40 条 / CSS 样式 22 条 / JavaScript 行为 45 条，共 107 条，按「结构 → 样式 → 行为」顺序排。HTML 示例可直接打开、JS 用 Node 实跑核对；安全相关条目末尾标 🔒 |
| `notes/PHP速查笔记.md` | **从小白到精通** PHP：基础语法 / 类型与运算符 / 字符串与正则 / 数组 / 流程控制 / 函数 / 面向对象 / 错误与异常 / 文件与目录 / 表单与超全局变量 / 会话与 Cookie / 数据库（mysqli + PDO）/ 时间 JSON 加密 / **危险函数（渗透必看）**，**117 条**。示例在**本机 PHP 8.5.11 + MySQL 8.4.11** 上实跑（Web 类用 `php -S` + curl 真实请求）；安全相关条目末尾标 🔒 |
| `notes/URL速查笔记.md` | **小白向** URL：6 个组成部件 / 百分号编码对照表 / 查询字符串 / GET vs POST / 命令行 curl / **安全视角（注入点、路径穿越、%00 截断）**，18 条。示例用 urllib + 本地监听器实测 |

「新格式」＝ 索引前置（目录与速查表合并、每行可跳转）+ 每条统一「**解析 ｜ 操作 ｜ 提醒**」三段（解析 = 干什么 + 参数表 + 返回；操作 = 可复制示例；提醒 = 要点易错点）+
代码示例注释必须是真实输出。整理完一份就把状态改成「已整理并校验通过」，并补上它的校验命令与输出。

校验已整理的笔记（以下命令针对 Python 那份，可直接跑）：

```bash
# Python 那份（只依赖标准库，任何解释器都行）
python3 verified-cheatsheet-notes/scripts/verify_code_blocks.py notes/Python内置函数速查笔记.md
# 104 个代码块｜注释比对 284/284 一致｜退出码 0

# Numpy 那份（示例里有 np.array(...)，要用装了 numpy 的解释器跑）
~/.venv/bin/python verified-cheatsheet-notes/scripts/verify_code_blocks.py notes/Numpy常用函数速查笔记.md
# 49 个代码块｜注释比对 178/178 一致｜退出码 0

# Pandas 那份（用装了 pandas 的解释器）
~/.venv/bin/python verified-cheatsheet-notes/scripts/verify_code_blocks.py notes/Pandas常用函数速查笔记.md
# 52 个代码块｜注释比对 164/164 一致｜退出码 0

# Matplotlib 那份（绘图示例：脚本会把后端设成 Agg，不会弹窗）
~/.venv/bin/python verified-cheatsheet-notes/scripts/verify_code_blocks.py notes/Matplotlib常用函数速查笔记.md
# 30 个代码块｜注释比对 76/76 一致（其余是纯绘图语句，编译执行无异常即可）｜退出码 0

# Seaborn 那份（示例用手工小表，离线可跑；load_dataset 那条首次需联网）
~/.venv/bin/python verified-cheatsheet-notes/scripts/verify_code_blocks.py notes/Seaborn常用函数速查笔记.md
# 28 个代码块｜注释比对 82/82 一致｜退出码 0

# C 那份（编译 + 运行，需要 cc / clang；不需要第三方库）
python3 verified-cheatsheet-notes/scripts/verify_c_blocks.py --lang c notes/C语言常用语法速查笔记.md
# 63 个 c 代码块｜全部编译运行通过｜退出码 0

# C++ 那份（同上，编译器换成 c++ -std=c++17）
python3 verified-cheatsheet-notes/scripts/verify_c_blocks.py --lang cpp notes/C++常用语法速查笔记.md
# 55 个 cpp 代码块｜全部编译运行通过｜退出码 0

# MySQL 那份（可移植语句重新跑一遍并与笔记里的结果表比对；用标准库 sqlite3，不需要 mysql 服务）
python3 verified-cheatsheet-notes/scripts/verify_sql_blocks.py notes/MySQL常用语法速查笔记.md
# 复核 37 条通过 37 条；跳过 6 条（标了未实跑的 MySQL 专有语法）

# Linux 那份（命令笔记：在 Ubuntu 24.04 容器里真跑每个 bash 块，再和笔记里的结果块比对；
# 少数网络工具只有 nicolaka/netshoot 镜像里有，脚本会自己换镜像找工具。需要本机跑着 docker/colima）
python3 verified-cheatsheet-notes/scripts/verify_sh_blocks.py notes/Linux常用指令速查笔记.md
# 比对 78 个块｜不一致 0 个｜结构示例 8 个（时间/PID/IP 这类每次都不一样）｜未实跑 7 个（要真网络/真主机）
```

> 笔记全部按新格式整理完毕（2026-09）；除 Python 那份外，其余都要用装了对应工具的解释器跑校验：
> `~/.venv/bin/python`（numpy / pandas / matplotlib / seaborn 都在里面）。
> C / C++ 那份用系统自带的 `cc` / `c++`；MySQL 那份用 Python 标准库的 sqlite3（本机没有 MySQL 服务，
> 所以只复核可移植语句，专有语法在笔记里如实标注「未实跑」，不假装验证过）。

## verified-cheatsheet-notes

把「速查笔记」整理成能长期查阅的形态：

- **索引表放最前**，同时充当目录和速查表；每行一个函数/方法，点「用法」直接跳到正文对应位置；
- 正文每条格式统一：`### 名字 一句话` → `**解析**`（干什么 + 参数表 + 返回）→ `**操作**`（示例，Linux 命令一行代码紧跟其输出）→ 可选 `> ⚠️ 提醒`；
- 代码示例里的 `#` 注释必须是**真实输出**，写完用脚本验，不靠肉眼。

校验脚本（只用标准库，不需要 pip 安装）：

```bash
python3 verified-cheatsheet-notes/scripts/verify_code_blocks.py /path/to/笔记.md

# 实例：本仓库的 Python 速查笔记
python3 verified-cheatsheet-notes/scripts/verify_code_blocks.py notes/Python内置函数速查笔记.md
#   104 个代码块｜注释比对 284/284 一致｜退出码 0
```

命令类笔记（Linux）用另一个脚本：`verify_sh_blocks.py` **在 Linux 容器里**跑每个 bash 块
（macOS 的 BSD 工具输出和 Linux 不一样，不能拿 macOS 当参照），支持 `--fill` 把真实输出写回 JSONL。
校验环境：`ubuntu:24.04`（coreutils/ps）+ `nicolaka/netshoot`（`file`/`tree`/`curl`/`ip`/`ss`/`nc`/`ping`），
脚本会按顺序换镜像找工具；想自带一个镜像就用 `scripts/Dockerfile.linux-note` build，再用 `--images` 指定。

它逐块执行 Markdown 里的 python 代码块，把 `#` 注释解析成期望值再和真实求值结果比对：
`input()` 用假 stdin 喂（不会卡住），代码块在临时目录里跑（不污染工作目录），
`# ❌ ValueError` 这类注释表示「这行预期报错」，自动跳过比对。

## study-reference-notes

「笔记写在哪、怎么写」的定位与模板：先判断该改正本（本仓库 `notes/`）还是链接桩
（`~/My_Python_Study/note/*.md` 只有几百字节、指向正本的指针），再按固定结构写
速查笔记（索引前置 + 每条「解析 ｜ 操作 ｜ 提醒」+ 真实输出注释）或 LeetCode 刷题笔记。
`references/` 里是三份骨架与清单（条目规范、多语言分类骨架、Python 清单），
`scripts/verify_notes_examples.py` 单独校验笔记里的示例。

## 装回本地

```bash
mkdir -p ~/.hermes/skills/note-taking ~/.hermes/skills/security
cp -R verified-cheatsheet-notes study-reference-notes ~/.hermes/skills/note-taking/
cp -R packet-capture ~/.hermes/skills/security/
```

本地实际安装位置：`~/.hermes/skills/note-taking/verified-cheatsheet-notes/`、
`~/.hermes/skills/note-taking/study-reference-notes/`、`~/.hermes/skills/security/packet-capture/`（两边内容保持一致）。
