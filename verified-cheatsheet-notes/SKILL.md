---
name: verified-cheatsheet-notes
description: "Use when reworking a cheat sheet. Verify every example."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [notes, cheatsheet, markdown, verification, documentation, python]
    category: note-taking
    related_skills: [obsidian, xlsx]
---

# Verified Cheat-Sheet Notes

For beginner-facing quick-reference notes (速查笔记) whose use case is **「忘了我来查」**：
the reader jumps from an index, so the index must be topical, the links must land,
the entry format must be identical everywhere, and every `#` comment must be the
**real output** — a cheat sheet that lies is worse than none.

## When to use

- 用户说笔记「不好查 / 格式乱 / 不满意」，要求合并目录与速查表、统一格式、重排分类
- 新建或扩充速查笔记（内置函数、库 API、语法要点、命令清单）
- 任何「代码示例 + 注释写了输出」的 Markdown 文档，需要保证示例真能跑

## Workflow

1. **先确认目标路径真的存在** — 别相信上一轮 session 里的路径，目录可能被改名
   （实例：`~/python/note/` → `~/My_Python_Study/note/`）。`ls <dir>` 一下再动手。
2. **数据化，别手写正文**：每条一个 dict（`name` / `one` / `sig` / `ret` / `note` / `code` / `warn`），
   逐批 append 到工作区 JSONL（**每批 15–20 条**，脚本太长容易超时或被审批卡住）。
   最后**从同一份数据渲染**索引表和正文 —— 这才是格式一致的关键。
3. **索引放最前**，它就是合并后的「目录 + 速查表」：
   `| 分类 | 用法（点击跳转） | 一句话作用 |`，一行一个条目，链接指到正文标题。
4. **正文每条固定格式**（详见 `references/entry-format.md`）：
   `#### `名字(参数)` 一句话作用` → `**签名** … ｜ **返回** … ｜ **备注** …` → 代码块 → 可选 `> ⚠️ 要点`。
5. **锚点要对得上**：链接目标 = 标题的 GitHub slug（保留 `isalnum()` 与 `-_`、空格转 `-`、其余丢弃）。
   slug 必须唯一 → 方法名带接收者前缀（`l.append` / `d.pop` / `s.add`），否则 list/dict/set 的 `pop` 会撞车。
   渲染后断言：`](#…)` 里每个目标都存在于 slug 集合。
6. **验证两轮**（缺一不可）：
   - `python3 scripts/verify_code_blocks.py NOTE.md` —— 执行每个代码块，把注释和真实求值结果比对；
   - 手写一份**行为断言**（assert / raises）覆盖「签名 ｜ 返回 ｜ 备注」和每条 ⚠️ 里的声明：
     异常类型、原地修改 vs 返回新对象、浅拷贝共享内层、`in` 的 O(n)/O(1)、`{}` vs `set()`…
7. **整份重写前先备份**：`shutil.copy2(path, path + ".bak-旧版")`，并告诉用户备份名、可自行删除。
8. **报告要诚实**：条目数、注释比对项数、断言数、失败项。若「失败」其实是你自己断言写错，
   复查后明说（例：`insert(-1)` 与「改一行两行都变」两条我一开始断言错了，文档才是对的）。

## Publishing to a git repo

- 预检：`git status` / `git ls-files` 看清**仓库里实际跟踪的路径**（可能已是新路径），`gh auth status` 确认登录。
- `git add <path> && git commit -m "note: …" && git push origin main`。
- 推送后**必须核对远端**：`git fetch && git rev-parse origin/main:<path>` 与 `git rev-parse HEAD:<path>`
  的 blob sha 相同、`git cat-file -s` 与工作区字节数相同；必要时 `gh api repos/<o>/<r>/git/trees/main?recursive=1` 查全树。
- 用户说「删除旧文件」但仓库里只有新路径时：先 `ls` / `git ls-files` / `git log` 求证，
  **不要臆造删除对象**，直接说明「没有旧文件需要删」并列出可能意图（改写历史？别的文件名？）。

## Pitfalls

- 示例里的 `input()` 会让校验脚本永久挂住 → 脚本按代码块喂假 stdin；
  连续多次 `input()` 不能每句都喂同一行，否则 `int("Tom")` 会造出**假失败**。
- `open(...,"w")` 之类示例会往当前目录落文件 → 脚本默认在临时目录里执行代码块。
- 比较注释要按**解析后的字面量**相等比，不要字符串比：dict/set 的 repr 顺序不稳，浮点 repr 有坑。
- 生成脚本里别用反引号当字符串定界符（会 `SyntaxError: invalid character '：'`）；
  代码样本文本用 `"""` 且**首尾各留一个换行**，否则结尾的引号会和定界符撞成 4 个引号。
- 同一段示例里的注释要**统一口径**：要么都写整个容器（`# {'a': 100, 'b': 2}`），要么都写元素值；
  混着写会让读者看错，也会让校验脚本报假不一致（真实案例：`d["a"] += 1  # 100` 被脚本抓出来，
  已改成容器形式）。
- 表格单元格里写 `|` 要转义成 `\|`，或直接用全角 `｜`。
- `from hermes_tools import read_file` 在 execute_code 里返回结构不稳定 → 直接 `open()` 读。
- 分批生成 + 每批落盘，长脚本被中断也不丢进度。

## Done = 全部勾上

- [ ] 索引里每个链接都能跳到真实存在的标题（0 失效）
- [ ] 每条都有 签名 / 返回 / 备注 三格（没内容写「—」，不省略）
- [ ] 所有代码块可执行；注释与真实输出一致（0 不一致）
- [ ] 备注 / ⚠️ 里声明的异常类型都实跑验证过
- [ ] 代码围栏成对（偶数）、分类标题无重复、条目 slug 唯一
- [ ] 旧版已备份，且备份文件名已告知用户

## Supporting files

- `references/entry-format.md` — 条目格式规范、索引表设计、锚点 / slug 规则、排序与「允许重复」策略、生成方式
- `references/python-inventory.md` — Python 速查笔记的条目骨架（A1–A10 内置函数 + list/str/dict/set/tuple），可套到 Numpy/Pandas/Matplotlib/Seaborn 那几份
- `scripts/verify_code_blocks.py` — 校验脚本：执行代码块 + 注释与真实输出比对（仅标准库）
