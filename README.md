# assisted-learning-skills

Hermes Agent 技能（skill）仓库，放的是「辅助学习 / 整理学习资料」这类工作流。
每个子目录一份 `SKILL.md`，外加可选的 `references/`（规范与清单）、`scripts/`（可直接跑的脚本）。

| 技能 | 用途 |
|------|------|
| `verified-cheatsheet-notes/` | 把速查笔记整理成能长期查阅的形态，并用脚本验证示例注释与真实输出一致 |

## 速查笔记

> 本仓库是速查笔记的**正本**；`My-Python-Study` 里的同名文件只是链接桩，改动一律在这里做。

| 笔记 | 内容 / 状态 |
|------|------|
| `note/Python内置函数速查笔记.md` | Python 内置函数 + list / str / dict / set / tuple 常用方法，104 条用法。**已按新格式整理并校验通过**（索引表在最前，点「用法」直接跳到正文） |
| `note/Numpy常用函数速查笔记.md` | NumPy 创建 / 索引 / 变形 / 运算 / 统计 / 拼接 / 线代，49 条用法。**已按新格式整理并校验通过** |
| `note/Pandas常用函数速查笔记.md` | Pandas 创建读写 / 查看 / 选择 / 清洗 / 变换 / 分组 / 合并 / 统计 / 时间 / 字符串，52 条用法。**已按新格式整理并校验通过**（pandas 3.0 的 API 变动都标了） |
| `note/Matplotlib常用函数速查笔记.md` | Matplotlib 画布 / 折线散点柱状直方饼图箱线 / 坐标轴 / 图例 / 子图 / 样式 / 保存，29 条用法。**已按新格式整理并校验通过** |
| `note/Seaborn常用函数速查笔记.md` | Seaborn 常用函数。**待按新格式整理** |

「新格式」＝ 索引前置（目录与速查表合并、每行可跳转）+ 每条统一 `签名 ｜ 返回 ｜ 备注` 三格 +
代码示例注释必须是真实输出。整理完一份就把状态改成「已整理并校验通过」，并补上它的校验命令与输出。

校验已整理的笔记（以下命令针对 Python 那份，可直接跑）：

```bash
# Python 那份（只依赖标准库，任何解释器都行）
python3 verified-cheatsheet-notes/scripts/verify_code_blocks.py note/Python内置函数速查笔记.md
# 104 个代码块｜注释比对 284/284 一致｜退出码 0

# Numpy 那份（示例里有 np.array(...)，要用装了 numpy 的解释器跑）
~/.venv/bin/python verified-cheatsheet-notes/scripts/verify_code_blocks.py note/Numpy常用函数速查笔记.md
# 49 个代码块｜注释比对 178/178 一致｜退出码 0

# Pandas 那份（用装了 pandas 的解释器）
~/.venv/bin/python verified-cheatsheet-notes/scripts/verify_code_blocks.py note/Pandas常用函数速查笔记.md
# 52 个代码块｜注释比对 164/164 一致｜退出码 0

# Matplotlib 那份（绘图示例：脚本会把后端设成 Agg，不会弹窗）
~/.venv/bin/python verified-cheatsheet-notes/scripts/verify_code_blocks.py note/Matplotlib常用函数速查笔记.md
# 30 个代码块｜注释比对 76/76 一致（其余是纯绘图语句，编译执行无异常即可）｜退出码 0
```

## verified-cheatsheet-notes

把「速查笔记」整理成能长期查阅的形态：

- **索引表放最前**，同时充当目录和速查表；每行一个函数/方法，点「用法」直接跳到正文对应位置；
- 正文每条格式统一：`#### 名字 一句话` → `**签名** ｜ **返回** ｜ **备注**` → 可运行示例 → 可选 `> ⚠️`；
- 代码示例里的 `#` 注释必须是**真实输出**，写完用脚本验，不靠肉眼。

校验脚本（只用标准库，不需要 pip 安装）：

```bash
python3 verified-cheatsheet-notes/scripts/verify_code_blocks.py /path/to/笔记.md

# 实例：对 My-Python-Study 仓库的 Python 速查笔记
#   104 个代码块｜注释比对 271/271 一致｜退出码 0
```

它逐块执行 Markdown 里的 python 代码块，把 `#` 注释解析成期望值再和真实求值结果比对：
`input()` 用假 stdin 喂（不会卡住），代码块在临时目录里跑（不污染工作目录），
`# ❌ ValueError` 这类注释表示「这行预期报错」，自动跳过比对。

## 装回本地

```bash
mkdir -p ~/.hermes/skills/note-taking
cp -R verified-cheatsheet-notes ~/.hermes/skills/note-taking/
```

本地实际安装位置：`~/.hermes/skills/note-taking/verified-cheatsheet-notes/`。
