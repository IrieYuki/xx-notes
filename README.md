# assisted-learning-skills

Hermes Agent 技能（skill）仓库，放的是「辅助学习 / 整理学习资料」这类工作流。
每个子目录一份 `SKILL.md`，外加可选的 `references/`（规范与清单）、`scripts/`（可直接跑的脚本）。

| 技能 | 用途 |
|------|------|
| `verified-cheatsheet-notes/` | 把速查笔记整理成能长期查阅的形态，并用脚本验证示例注释与真实输出一致 |

## 速查笔记

| 笔记 | 内容 |
|------|------|
| `note/Python内置函数速查笔记.md` | Python 内置函数 + list / str / dict / set / tuple 常用方法，104 条用法；索引表在最前，点「用法」直接跳到正文 |

这份笔记正是用上面那个技能整理的，可以用同一个脚本验证它（注释必须和真实输出一致）：

```bash
python3 verified-cheatsheet-notes/scripts/verify_code_blocks.py note/Python内置函数速查笔记.md

# 104 个代码块｜注释比对 271/271 一致｜退出码 0
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
