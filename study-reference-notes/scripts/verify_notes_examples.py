#!/usr/bin/env python3
"""校验速查笔记：示例能不能跑 + `#` 注释里写的输出是不是真的。

用法:
    python3 verify_notes_examples.py <笔记.md> [--stdin "Tom\n18\n1 2\n"]

做三件事:
1. 逐条 exec 每个 ```python 代码块（顶层语句逐句执行；stdin 用 StringIO 顶掉，
   否则示例里的 input() 会真的等键盘、把调用方卡住）；
2. 用 tokenize 找每行 `#` 注释，对「顶层简单语句」把注释里的字面量和真实结果比对
   （`→` 取右边、`（…）` 注解剥掉；prose 注释与 ❌ 行跳过）；
3. 结构检查：``` 围栏是否成对、`#### ` 条目数是否等于索引链接数、每条 `](#slug)`
   是否都能在条目标题算出的锚点集合里找到。

退出码 0 = 全部通过。
"""
from __future__ import annotations

import ast
import contextlib
import io
import re
import sys
import tokenize

DEFAULT_STDIN = "Tom\n18\n1 2 3\n"


def slug(text: str) -> str:
    """GitHub 锚点算法：小写，保留字母/数字/汉字/`-`/`_`，空格转 `-`，其余标点丢弃。"""
    out = []
    for ch in text.strip().lower():
        if ch.isalnum() or ch in "-_":
            out.append(ch)
        elif ch == " ":
            out.append("-")
    return "".join(out)


def fences(text: str):
    """产出 (info, code, 起始行号)。"""
    info = buf = None
    start = 0
    for i, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("```"):
            if buf is None:
                info, buf, start = line.lstrip()[3:].strip(), [], i
            else:
                yield info, "\n".join(buf), start
                info = buf = None
        elif buf is not None:
            buf.append(line)


def comments_of(code: str) -> dict:
    out = {}
    try:
        for tok in tokenize.generate_tokens(io.StringIO(code).readline):
            if tok.type == tokenize.COMMENT:
                out[tok.start[0]] = tok.string
    except (tokenize.TokenError, IndentationError):
        pass
    return out


def expected_from(comment: str):
    """从注释里提取「期望值」；是说明性文字就返回 None。"""
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


def base_name(node):
    """`l.append(3)` → 'l'；`d['a'] = 1` / `del d['a']` → 'd'（注释通常写操作后的容器样子）。"""
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
        return ast.unparse(node.func.value)
    if isinstance(node, ast.Assign) and node.targets and isinstance(node.targets[0], ast.Subscript):
        return ast.unparse(node.targets[0].value)
    if isinstance(node, ast.Delete) and node.targets and isinstance(node.targets[0], ast.Subscript):
        return ast.unparse(node.targets[0].value)
    return None


def check_block(code: str, stdin_payload: str):
    try:
        tree = ast.parse(code)
    except SyntaxError as ex:
        return 0, 0, [], [f"语法错误: {ex}"]
    cmts = comments_of(code)
    ns = {"__name__": "__verify__"}
    sink = io.StringIO()
    checked = skipped = 0
    mism, errs = [], []
    for node in tree.body:
        head = (ast.get_source_segment(code, node) or "").splitlines()[0][:70]
        exp = expected_from(cmts.get(node.end_lineno, "")) if node.end_lineno in cmts else None
        try:
            with contextlib.redirect_stdout(sink):
                sys.stdin = io.StringIO(stdin_payload)  # 每句重喂，避免 input() 卡死
                if isinstance(node, ast.Expr):
                    src = ast.unparse(node)
                    res = eval(src, ns)
                    if exp is None:
                        skipped += 1
                    elif res is not None:
                        checked += 1
                        if res != exp:
                            mism.append((src, exp, res))
                    else:
                        base = base_name(node)
                        if base and base in ns:
                            checked += 1
                            if ns[base] != exp:
                                mism.append((src, exp, ns[base]))
                        else:
                            skipped += 1
                else:
                    exec(compile(ast.Module([node], []), "<verify>", "exec"), ns)
                    base = base_name(node)
                    if exp is None or not base or base not in ns:
                        skipped += 1
                    else:
                        checked += 1
                        if ns[base] != exp:
                            mism.append((head, exp, ns[base]))
        except Exception as ex:  # 示例里的报错都写成注释行，这里出现异常就是真问题
            errs.append(f"{type(ex).__name__}: {ex} | {head}")
    return checked, skipped, mism, errs


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    path = argv[1]
    payload = DEFAULT_STDIN
    if "--stdin" in argv:
        payload = argv[argv.index("--stdin") + 1].encode().decode("unicode_escape")
    text = open(path, encoding="utf-8").read()

    # --- 结构 ---
    entries = [l[5:].strip() for l in text.splitlines() if l.startswith("#### ")]
    links = re.findall(r"\]\(#([^)]+)\)", text)
    slugs = {slug(e) for e in entries}
    dead = [l for l in links if l not in slugs]
    n_fences = sum(1 for l in text.splitlines() if l.lstrip().startswith("```"))
    print(f"文件: {path}")
    print(f"条目(####) {len(entries)}｜索引链接 {len(links)}｜失效链接 {len(dead)}"
          f"｜围栏 {n_fences}（{'成对' if n_fences % 2 == 0 else '奇数 ⚠️'}）")
    if dead:
        print("  失效链接:", dead[:5])

    # --- 示例 ---
    checked = skipped = 0
    all_mism, all_err = [], []
    for info, code, line in fences(text):
        if info not in ("", "python"):
            continue
        c, s, mism, errs = check_block(code, payload)
        checked += c
        skipped += s
        all_mism += [(line,) + m for m in mism]
        all_err += [(line, e) for e in errs]
    print(f"示例比对 {checked - len(all_mism)}/{checked} 一致｜执行异常 {len(all_err)}"
          f"｜跳过（prose 注释）{skipped}")
    for line, src, exp, got in all_mism:
        print(f"  ✗ L{line} {src}\n      注释写 {exp!r} ≠ 实际 {got!r}")
    for line, err in all_err:
        print(f"  ⚠ L{line} {err}")

    ok = not (all_mism or all_err or dead or n_fences % 2)
    print("结论:", "通过 ✅" if ok else "有问题 ❌")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
