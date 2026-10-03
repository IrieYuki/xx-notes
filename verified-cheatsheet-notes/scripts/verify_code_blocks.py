#!/usr/bin/env python3
"""校验 Markdown 里的代码示例：执行 + 注释与真实输出比对。

用法:
    python3 verify_code_blocks.py NOTE.md [OTHER.md ...] [--lang python] [--keep-cwd]

做三件事:
  1. 抽出所有 ```python 代码块，逐块执行。stdin 用假数据喂，所以示例里的 input() 不会挂住；
     默认在临时目录里执行，open("x","w") 之类的示例不会污染你的工作目录。
  2. 把 `#` 注释里的期望值解析出来，和真实求值结果比对。
  3. 报告不一致与异常；有不一致时退出码 1。

注释写法约定（比对逻辑依赖它）:
    l.append(3)        # [1, 2, 3]       变异方法：比较接收者 l 执行后的值
    d.get("b")         # None            表达式：比较它的返回值
    del d["a"]         # {'b': 2}        下标删除 / 赋值：比较 d 执行后的值
    int("3.14")        # ❌ ValueError    以 ❌ 开头 = 预期报错，不做值比对
    f"{x:.2f}"         # '3.14'（两位）   括号里的中文注解会被忽略

局限：只检查顶层语句；`for`/`if`/`def` 内部的注释不比对（它们要整体执行）。
库笔记（numpy / pandas / matplotlib / seaborn）：注释写成 `# array([1, 2, 3])` / `# dtype('int64')` 也能自动比对，
但要用装了该库的解释器跑脚本（例：`~/.venv/bin/python scripts/verify_code_blocks.py ...`），
且不要依赖被 `...` 截断的长数组注释（会被跳过）。
绘图笔记：脚本默认把后端设为 Agg（不弹窗），并**在每个代码块结束后关图 + 重置 rcParams**，
否则前一个块画过的图/改过的全局样式会让后面的块出现顺序相关的假失败：
一次校验多个笔记时尤其明显（建议仍然一次只跑一个笔记，输出更好读）。
"""

from __future__ import annotations

import argparse
import ast
import contextlib
import io
import os
import re
import sys
import tempfile
import textwrap
import tokenize
from pathlib import Path

# 假 stdin：够 input() 连着调好几次；不可依赖「同一行」重复（int("Tom") 会假失败）
STDIN_LINES = ["Tom", "18", "1 2 3", "42", "7 8 9", "5"]


def extract_blocks(md_text: str, lang: str = "python"):
    """返回 [(起始行号, 代码)]。缩进在列表里的代码块会先 dedent（否则会误报 unexpected indent）。"""
    out, lines, i = [], md_text.split("\n"), 0
    while i < len(lines):
        m = re.match(r"^\s*```(\w*)", lines[i])
        if m and m.group(1) == lang:
            start, buf, i = i + 2, [], i + 1
            while i < len(lines) and not re.match(r"^\s*```\s*$", lines[i]):
                buf.append(lines[i])
                i += 1
            out.append((start, textwrap.dedent("\n".join(buf))))
        i += 1
    return out


def comments_of(code: str):
    res = {}
    try:
        for tok in tokenize.generate_tokens(io.StringIO(code).readline):
            if tok.type == tokenize.COMMENT:
                res[tok.start[0]] = tok.string
    except (tokenize.TokenError, IndentationError):
        pass
    return res


def _numpy_ns():
    """numpy 风格注释（array([...]) / dtype('int64')）的求值命名空间；没装 numpy 就返回 None。"""
    try:
        import numpy as np
    except Exception:
        return None
    return {"array": np.array, "np": np, "dtype": np.dtype, "nan": np.nan, "inf": np.inf,
            "float16": np.float16, "float32": np.float32, "float64": np.float64,
            "int32": np.int32, "int64": np.int64, "bool_": np.bool_,
            "True": True, "False": False, "None": None}


def equal(a, b) -> bool:
    """值相等判断：numpy 数组用 array_equal（忽略 dtype 差异），其余用 ==。"""
    try:
        import numpy as np
        if isinstance(a, np.ndarray) or isinstance(b, np.ndarray):
            return bool(np.array_equal(a, b))
    except Exception:
        pass
    try:
        return bool(a == b)
    except Exception:
        return False


_MISS = object()
_SKIPPED_NUMPY: list = []


def _try_parse(s: str):
    """解析成值；解析不出来返回 _MISS。支持字面量与 numpy 写法（array([...]) / dtype('int64')）。"""
    try:
        return ast.literal_eval(s)
    except Exception:
        pass
    # numpy 形式：array(...) / dtype(...) / 以 [ { ( 开头但里面含 array(...) 的（如 split 返回的 list）
    looks_numpy = re.match(r"^(array|np\.|dtype)", s) or ("array(" in s and s[:1] in "[({}")
    if looks_numpy:
        ns = _numpy_ns()
        if ns:
            try:
                return eval(s, ns)
            except Exception:
                pass
        else:
            _SKIPPED_NUMPY.append(s)
    return _MISS


def one_line(v) -> str:
    """值的单行 repr（numpy 多维数组会换行，折成一行，便于比对与显示）。"""
    try:
        return " ".join(repr(v).split())
    except Exception:
        return "<无法repr>"


def expected_candidates(comment: str):
    """返回 (期望值, 期望文本)；文本为 None 表示这行不做比对。

    顺序很重要：先按原样试（否则 `# array([1, 2, 3])` 会被「去括号注解」那步截成 `array`），
    再去掉「→ 后面的部分」与「中文括号注解」重试。
    """
    c = comment.lstrip("#").strip()
    if not c or c.startswith("❌") or "..." in c:   # ❌ = 预期报错；... = numpy 截断值
        return None, None
    v = _try_parse(c)
    if v is not _MISS:
        return v, c
    tail = c.split("→")[-1].strip() if "→" in c else c
    tail = re.split(r"[（(]", tail)[0].strip()
    tail = re.sub(r"^(即|等于|返回|输出)\s*", "", tail).strip()
    if tail and tail != c:
        v = _try_parse(tail)
        if v is not _MISS:
            return v, tail
    return None, None


def matches(got, exp_val, exp_text: str) -> bool:
    """两级比对：
    ① 注释文本就是真实 repr（numpy 默认只显示 8 位小数，数值比对会误报）；
    ② 解析出的期望值与原值语义相等（列表/元组/集合这类用 equality）。
    """
    if one_line(got) == " ".join(exp_text.split()):
        return True
    if exp_val is not None:
        return equal(got, exp_val)
    return False


def receiver_of(node):
    """变异方法调用的接收者 / 下标赋值、删除的目标 —— 用来比较「改完之后」的值。"""
    if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
        func = node.value.func
        if isinstance(func, ast.Attribute):
            return ast.unparse(func.value)
    if isinstance(node, ast.Assign):
        for t in node.targets:
            if isinstance(t, ast.Subscript):
                return ast.unparse(t.value)
    if isinstance(node, ast.AugAssign) and isinstance(node.target, ast.Subscript):
        return ast.unparse(node.target.value)
    if isinstance(node, ast.Delete):
        for t in node.targets:
            if isinstance(t, ast.Subscript):
                return ast.unparse(t.value)
    return None


def check_block(code: str):
    """返回 (比对数, 不一致列表, 异常列表)"""
    n_checked, mismatches, errors = 0, [], []
    try:
        tree = ast.parse(code)
    except SyntaxError as ex:
        return 0, [], [f"语法错误: {ex}"]
    cmts = comments_of(code)
    ns: dict = {"__name__": "__verify__"}
    # 每个代码块重置一次 stdin，让连续多次 input() 依次取到不同的假数据
    # （若每句都重置，int(input()) 会重复拿到 "Tom"，造出假失败）
    sys.stdin = io.StringIO("\n".join(STDIN_LINES) + "\n")
    for node in tree.body:
        seg = ast.get_source_segment(code, node) or ""
        head = seg.splitlines()[0][:70] if seg else ""
        exp, exp_text = expected_candidates(cmts[node.end_lineno]) if node.end_lineno in cmts else (None, None)
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                if isinstance(node, ast.Expr):
                    src = ast.unparse(node)
                    value = eval(src, ns)                      # 副作用只发生一次
                    if exp_text is None:
                        continue
                    if value is not None:
                        n_checked += 1
                        if not matches(value, exp, exp_text):
                            mismatches.append(f"{src}  → 注释 {exp_text}，实际 {one_line(value)}")
                    elif matches(value, exp, exp_text):
                        n_checked += 1        # 表达式确实返回 None，而注释写的就是 None
                    else:
                        name = receiver_of(node)
                        if name and name in ns:
                            n_checked += 1
                            if not matches(ns[name], exp, exp_text):
                                mismatches.append(f"{src}  → 注释 {exp_text}，实际 {one_line(ns[name])}")
                else:
                    exec(compile(ast.Module([node], []), "<block>", "exec"), ns)
                    if exp_text is None:
                        continue
                    name = receiver_of(node)
                    if name and name in ns:
                        n_checked += 1
                        if not matches(ns[name], exp, exp_text):
                            mismatches.append(f"{head}  → 注释 {exp_text}，实际 {one_line(ns[name])}")
        except EOFError:
            errors.append(f"{head}  ← input() 还需要更多假 stdin（往 STDIN_LINES 里加行）")
        except Exception as ex:
            errors.append(f"{head}  ← {type(ex).__name__}: {ex}")
    return n_checked, mismatches, errors


def reset_plot_state():
    """清掉绘图库的**全局状态**。

    matplotlib / seaborn 把 rcParams、当前 figure 放在模块级全局里，一个代码块画的图会影响下一个块：
    例如某块 set_xlabel("X") 后，下一个没建 figure 的 seaborn 块会画到那个轴上，
    导致「注释 vs 实际」出现与顺序相关的**假失败**。每块结束后关图 + 恢复 rcParams 默认值。
    """
    plt = sys.modules.get("matplotlib.pyplot")
    if plt is None:
        return
    try:
        plt.close("all")
        import matplotlib
        matplotlib.rcdefaults()
    except Exception:
        pass


def main() -> int:
    ap = argparse.ArgumentParser(description="校验 Markdown 代码块的注释与真实输出是否一致")
    ap.add_argument("files", nargs="+")
    ap.add_argument("--lang", default="python")
    ap.add_argument("--keep-cwd", action="store_true", help="在当前目录执行代码块（默认在临时目录）")
    args = ap.parse_args()

    # 先把笔记路径解析成绝对路径：下面会 chdir 到临时目录，相对路径就找不到了
    args.files = [str(Path(f).resolve()) for f in args.files]

    # 绘图类笔记：强制无界面后端，避免 plt.show() 弹窗/阻塞校验
    os.environ.setdefault("MPLBACKEND", "Agg")

    origin = os.getcwd()
    tmp = None
    if not args.keep_cwd:
        tmp = tempfile.mkdtemp(prefix="verify-blocks-")
        os.chdir(tmp)

    total_checked = total_bad = 0
    bad_files = 0
    try:
        for f in args.files:
            text = Path(f).read_text(encoding="utf-8")
            bl = extract_blocks(text, args.lang)
            n_checked = n_bad = 0
            print(f"\n== {f}｜{args.lang} 代码块 {len(bl)} 个 ==")
            for start, code in bl:
                checked, mismatches, errors = check_block(code)
                reset_plot_state()          # 防止绘图全局状态跨块污染（假失败）
                n_checked += checked
                n_bad += len(mismatches)
                for mm in mismatches:
                    print(f"  ✗ 第 {start} 行起: {mm}")
                for er in errors:
                    print(f"  ⚠ 第 {start} 行起: {er}")
            print(f"  注释比对：{n_checked - n_bad}/{n_checked} 一致，不一致 {n_bad}")
            total_checked += n_checked
            total_bad += n_bad
            if n_bad:
                bad_files += 1
    finally:
        os.chdir(origin)
        if tmp and os.path.isdir(tmp):
            contextlib.suppress(OSError) and __import__("shutil").rmtree(tmp, ignore_errors=True)

    print(f"\n合计：比对 {total_checked} 项，不一致 {total_bad} 项，有问题的文件 {bad_files} 个")
    if _SKIPPED_NUMPY:
        print(f"提示：{len(_SKIPPED_NUMPY)} 条 numpy 形式注释被跳过 —— 当前解释器没装 numpy。"
              f"换装了库的解释器重跑，例如 ~/.venv/bin/python {__file__} <笔记.md>")
    return 1 if total_bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
