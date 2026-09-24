#!/usr/bin/env python3
"""校验 Markdown 里的 C / C++ 代码块：**编译 + 运行**，并把输出和注释里写的「运行结果」比对。

用法:
    python3 verify_c_blocks.py --lang c  NOTE.md [OTHER.md ...]
    python3 verify_c_blocks.py --lang cpp NOTE.md [OTHER.md ...]

可选: --cc cc --cxx c++    指定编译器（默认 cc / c++，即本机 clang）
      --std c17 / --std c++17
      --stdin-file f         把文件内容当假 stdin 喂（默认内置几行假数据，scanf 不会挂）
      --keep-files           保留临时目录（默认删）

代码块里两种特殊注释（生成器会自动写第二种）:
    // 输入：Tom 18                   ← 该块运行时的 stdin（省略则不喂任何输入）
    // 运行结果：Hello                 ← 期望输出，单行

    // 运行结果：                     ← 期望输出，多行
    // 第一行
    // 第二行

判据:
  * 编译失败   → ✗（报错信息前几行）
  * 运行崩溃   → ✗（信号/退出码）
  * 输出不一致 → ✗（期望 vs 实际）
  * 只有警告   → 算通过，但报 ⚠ 提醒
  * 程序设了超时（默认 10s），避免示例卡在死循环/scanf 上
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

STDIN_FEED = ""
TIMEOUT = 10


def feed_from_code(code: str, default: str):
    """代码块里的 `// 输入：Tom 18` 就是该块的 stdin（与生成器同一规则）。"""
    m = re.search(r"^\s*//\s*输入[：:]\s*(.*)$", code, re.M)
    return (m.group(1).strip() + "\n") if m else default


def extract_blocks(md_text: str, lang: str):
    """返回 [(起始行号, 代码)]；支持 ```c / ```cpp / ```c++ 三种围栏标记。"""
    aliases = {"c": {"c"}, "cpp": {"cpp", "c++", "cc"}}[lang]
    out, lines, i = [], md_text.split("\n"), 0
    while i < len(lines):
        m = re.match(r"^\s*```(\S*)", lines[i])
        if m and m.group(1).lower() in aliases:
            start, buf, i = i + 2, [], i + 1
            while i < len(lines) and not re.match(r"^\s*```\s*$", lines[i]):
                buf.append(lines[i])
                i += 1
            out.append((start, textwrap.dedent("\n".join(buf))))
        i += 1
    return out


def split_expected(code: str):
    """从代码尾部抽出「运行结果」注释，返回 (纯代码, 期望输出 or None)。

    只认**尾部**连续的 `// 运行结果：` / `// 后续行` （或 `/* 运行结果：...*/`）注释。
    """
    lines = code.split("\n")
    # 从后往前收集尾部注释行
    tail = []
    idx = len(lines) - 1
    while idx >= 0 and (lines[idx].strip() == "" or lines[idx].lstrip().startswith("//")):
        if lines[idx].strip():
            tail.insert(0, lines[idx].strip())
        idx -= 1
    if not tail:
        return code, None
    # 在尾部注释里找**最后一条**「运行结果：」——它之前可能是代码自带的注释
    pos = None
    for k, t in enumerate(tail):
        if re.match(r"^//\s*运行结果[：:]", t):
            pos = k
    if pos is None:
        return code, None
    m = re.match(r"^//\s*运行结果[：:]\s*(.*)$", tail[pos])
    first = m.group(1).strip()
    rest = [re.sub(r"^//\s?", "", t) for t in tail[pos + 1:]]
    expected = "\n".join(([first] if first else []) + rest)
    pure = "\n".join(lines[: idx + 1])
    return pure, (expected if (first or rest) else "")


def norm(text: str) -> str:
    """比对用归一化：去掉每行行尾空白与首尾空行（行尾空格肉眼不可见，不该算不一致）。"""
    lines = [l.rstrip() for l in text.split("\n")]
    while lines and lines[0] == "":
        lines.pop(0)
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


def run_block(code: str, lang: str, args, workdir: str):
    """编译并运行一个代码块，返回 (ok, expected, actual, message)。"""
    pure, expected = split_expected(code)
    stdin_data = feed_from_code(code, args.stdin_data)
    ext = ".c" if lang == "c" else ".cpp"
    src = os.path.join(workdir, "main" + ext)
    exe = os.path.join(workdir, "prog")
    Path(src).write_text(pure + "\n", encoding="utf-8")
    compiler = args.cc if lang == "c" else args.cxx
    cmd = [compiler, f"-std={args.std}", "-O0", "-Wall", "-o", exe, src, "-lm"]
    cp = subprocess.run(cmd, capture_output=True, text=True)
    if cp.returncode != 0:
        err = "\n".join([l for l in cp.stderr.splitlines() if "error" in l.lower()][:3]) or cp.stderr[:300]
        return False, expected, None, f"编译失败: {err}"
    warnings = [l for l in cp.stderr.splitlines() if "warning" in l.lower()]
    try:
        rp = subprocess.run([exe], capture_output=True, text=True, input=stdin_data,
                            timeout=TIMEOUT, cwd=os.path.dirname(exe))   # cwd=临时目录：文件读写示例不污染工作目录
    except subprocess.TimeoutExpired:
        return False, expected, None, f"运行超时（>{TIMEOUT}s）：是不是在等输入（scanf）或死循环？"
    if rp.returncode != 0:
        return False, expected, rp.stdout, f"运行退出码 {rp.returncode}（崩溃/异常退出）"
    actual = rp.stdout.rstrip("\n")
    msg = f"[{len(warnings)} 条编译警告]" if warnings else ""
    if expected is None:
        return True, None, actual, msg
    ok = norm(actual) == norm(expected)      # 逐行 rstrip 再比：行尾空格不可见，不算错
    return ok, expected, actual, msg


def main() -> int:
    ap = argparse.ArgumentParser(description="编译+运行 C/C++ 代码块，并比对「运行结果」注释")
    ap.add_argument("files", nargs="+")
    ap.add_argument("--lang", choices=["c", "cpp"], default="c")
    ap.add_argument("--cc", default=os.environ.get("CC", "cc"))
    ap.add_argument("--cxx", default=os.environ.get("CXX", "c++"))
    ap.add_argument("--std", default=None)
    ap.add_argument("--stdin-file", default=None)
    ap.add_argument("--keep-files", action="store_true")
    args = ap.parse_args()
    args.std = args.std or ("c17" if args.lang == "c" else "c++17")
    args.stdin_data = Path(args.stdin_file).read_text(encoding="utf-8") if args.stdin_file else STDIN_FEED

    tmp = tempfile.mkdtemp(prefix="verify-c-")
    total = bad = 0
    try:
        for f in args.files:
            text = Path(f).read_text(encoding="utf-8")
            blocks = extract_blocks(text, args.lang)
            n_bad = 0
            print(f"\n== {f}｜{args.lang} 代码块 {len(blocks)} 个｜编译器 {args.cc if args.lang=='c' else args.cxx} -std={args.std} ==")
            for start, code in blocks:
                ok, expected, actual, msg = run_block(code, args.lang, args, tmp)
                total += 1
                if not ok:
                    n_bad += 1
                    print(f"  ✗ 第 {start} 行起: {msg}")
                    if expected is not None and actual is not None:
                        print(f"      期望: {expected!r}")
                        print(f"      实际: {actual!r}")
                elif msg:
                    print(f"  ⚠ 第 {start} 行起: {msg}")
            print(f"  → 通过 {len(blocks) - n_bad}/{len(blocks)}")
            bad += n_bad
    finally:
        if not args.keep_files:
            shutil.rmtree(tmp, ignore_errors=True)
    print(f"\n合计：{total - bad}/{total} 个代码块编译运行通过")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
