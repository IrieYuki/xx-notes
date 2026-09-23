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
import tokenize
from pathlib import Path

# 假 stdin：够 input() 连着调好几次；不可依赖「同一行」重复（int("Tom") 会假失败）
STDIN_LINES = ["Tom", "18", "1 2 3", "42", "7 8 9", "5"]


def extract_blocks(md_text: str, lang: str = "python"):
    """返回 [(起始行号, 代码)]"""
    out, lines, i = [], md_text.split("\n"), 0
    while i < len(lines):
        m = re.match(r"^\s*```(\w*)", lines[i])
        if m and m.group(1) == lang:
            start, buf, i = i + 2, [], i + 1
            while i < len(lines) and not re.match(r"^\s*```\s*$", lines[i]):
                buf.append(lines[i])
                i += 1
            out.append((start, "\n".join(buf)))
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


def expected_value(comment: str):
    """从注释里解析出期望值；解析不出来（说明性文字）返回 None。"""
    c = comment.lstrip("#").strip()
    if not c or c.startswith("❌"):
        return None
    if "→" in c:
        c = c.split("→")[-1].strip()
    c = re.split(r"[（(]", c)[0].strip()
    c = re.sub(r"^(即|等于|返回|输出)\s*", "", c).strip()
    if not c:
        return None
    try:
        return ast.literal_eval(c)
    except Exception:
        return None


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
        exp = expected_value(cmts[node.end_lineno]) if node.end_lineno in cmts else None
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                if isinstance(node, ast.Expr):
                    src = ast.unparse(node)
                    value = eval(src, ns)                      # 副作用只发生一次
                    if exp is None:
                        continue
                    if value is not None:
                        n_checked += 1
                        if value != exp:
                            mismatches.append(f"{src}  → 注释 {exp!r}，实际 {value!r}")
                    else:
                        name = receiver_of(node)
                        if name and name in ns:
                            n_checked += 1
                            if ns[name] != exp:
                                mismatches.append(f"{src}  → 注释 {exp!r}，实际 {ns[name]!r}")
                else:
                    exec(compile(ast.Module([node], []), "<block>", "exec"), ns)
                    if exp is None:
                        continue
                    name = receiver_of(node)
                    if name and name in ns:
                        n_checked += 1
                        if ns[name] != exp:
                            mismatches.append(f"{head}  → 注释 {exp!r}，实际 {ns[name]!r}")
        except EOFError:
            errors.append(f"{head}  ← input() 还需要更多假 stdin（往 STDIN_LINES 里加行）")
        except Exception as ex:
            errors.append(f"{head}  ← {type(ex).__name__}: {ex}")
    return n_checked, mismatches, errors


def main() -> int:
    ap = argparse.ArgumentParser(description="校验 Markdown 代码块的注释与真实输出是否一致")
    ap.add_argument("files", nargs="+")
    ap.add_argument("--lang", default="python")
    ap.add_argument("--keep-cwd", action="store_true", help="在当前目录执行代码块（默认在临时目录）")
    args = ap.parse_args()

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
    return 1 if total_bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
