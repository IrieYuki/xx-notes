#!/usr/bin/env python3
"""校验 Markdown 里的 bash 代码块：在 **Linux 容器**里真跑，并与紧跟其后的 ```text 结果块比对。

用法:
    python3 verify_sh_blocks.py NOTE.md [OTHER.md ...]      # 校验（默认）
    python3 verify_sh_blocks.py --fill entries.jsonl        # 生成：把真实输出写回 JSONL 的 out 字段
    python3 verify_sh_blocks.py --show-fixture              # 打印「示例环境」块（笔记里那份必须一字不差）

为什么必须在容器里跑:
    本机是 macOS，ls / sed / date 是 BSD 版，`ls -l --time-style`、`stat -c` 这些 GNU 参数直接不存在，
    输出格式也不同。Linux 笔记的示例输出要和用户以后在 Kali / 服务器上看到的一致，所以统一在
    Ubuntu 24.04 容器里跑（GNU coreutils 9.4），LC_ALL=C + TZ=UTC 固定语言与时区。
    少数工具 Ubuntu 基础镜像里没有（file / tree / less / curl / wget / ip / ss / nc / ping），
    脚本按 IMAGES 顺序换镜像找齐工具 —— 本机 apt 源不通，装不了包，只能借现成镜像。
    （Debian 镜像站不通，所以用 Ubuntu；网络工具来自 Alpine 的 netshoot，它对 file/tree/curl/ip 的
      输出与 GNU 版一致，只有 ls 之类的 BusyBox 命令不能用在 netshoot 里。）

代码块约定（与生成器共用同一套规则）:
    * 每个示例块**自包含**，默认工作目录就是示例环境 `~/linux-lab`（脚本会先造好）
    * 结果块 = 紧跟在该 ```bash 块之后的一个 ```text 块，内容为真实 stdout（`--fill` 自动写）
    * 结果块首行「（结构示例」→ 跑一遍确认命令能跑，但不比对输出（输出随机器/时间变化）
    * 结果块首行「（未实跑」  → 需要真网络/真主机/装不上的软件，本机不跑，笔记里如实标注
    * 首行是 `# [示例环境]` 的块 = 示例环境本身：脚本会核对它与本文件里 SETUP **一字不差**
判据:
    * 命令不存在（127）/ 超时 / docker 报错 → ✗ 跑不通
    * 最后一条命令非 0 退出            → ⚠ 提醒（可能是故意演示报错，人工确认）
    * 输出与结果块不一致                → ✗ 不一致
    * 有输出但后面没有结果块            → ⚠ 未记录（示例的输出没写进笔记）
"""
import argparse
import json
import re
import subprocess
import sys
import uuid
from pathlib import Path

IMAGES = ["ubuntu:24.04", "nicolaka/netshoot"]
TIMEOUT = 30
STRUCT_MARK = "（结构示例"
UNRUN_MARK = "（未实跑"

# 示例环境：笔记开头那份 ```bash 块必须与这里一字不差（脚本会核对），所以别在笔记里手改。
SETUP = """\
# [示例环境] 造一个练习目录，后面每条示例都在这个目录里跑
rm -rf ~/linux-lab && mkdir -p ~/linux-lab && cd ~/linux-lab
mkdir -p dir1 dir2
printf 'hello linux\\nsecond line\\nthird line\\n' > hello.txt
printf 'apple 3\\nbanana 5\\ncherry 7\\n' > fruit.txt
printf 'name,age\\ntom,18\\namy,20\\n' > data.csv
printf 'login ok\\nlogin failed\\nlogin ok\\n' > notes.txt
printf '#!/bin/bash\\necho "hi from script"\\n' > run.sh
: > empty.txt
chmod +x run.sh
touch -t 202601010900 hello.txt fruit.txt data.csv notes.txt run.sh empty.txt dir1 dir2"""


def norm(text: str) -> str:
    """比对用归一化：逐行 rstrip（对齐/行尾空格肉眼不可见，不算错）+ 去掉首尾空行。"""
    lines = [l.rstrip() for l in text.replace("\r\n", "\n").split("\n")]
    while lines and lines[0] == "":
        lines.pop(0)
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


def extract_blocks(md_text: str):
    """返回 [(起始行号, 代码, 期望结果 or None)]：```bash 块 + 紧跟其后的 ```text 块。"""
    lines = md_text.split("\n")
    out, i = [], 0
    while i < len(lines):
        m = re.match(r"^\s*```(\S*)", lines[i])
        if m and m.group(1).lower() in {"bash", "sh", "shell", "console"}:
            start, buf, i = i + 2, [], i + 1
            while i < len(lines) and not re.match(r"^\s*```\s*$", lines[i]):
                buf.append(lines[i])
                i += 1
            code = "\n".join(buf)
            expected = None
            j = i + 1
            while j < len(lines) and lines[j].strip() == "":
                j += 1
            if j < len(lines) and re.match(r"^\s*```text\s*$", lines[j]):
                k, ebuf = j + 1, []
                while k < len(lines) and not re.match(r"^\s*```\s*$", lines[k]):
                    ebuf.append(lines[k])
                    k += 1
                expected = "\n".join(ebuf)
            out.append((start, code, expected))
        i += 1
    return out


def run_in(image: str, code: str, timeout: int):
    """在一个全新容器里跑 SETUP + code，返回 (returncode, stdout, stderr, 说明)。"""
    script = SETUP + "\n\n" + code + "\n"
    name = "verify-sh-" + uuid.uuid4().hex[:10]
    cmd = ["docker", "run", "--rm", "-i", "--name", name,
           "-e", "LC_ALL=C", "-e", "TZ=UTC", "-e", "HOME=/root",
           image, "bash"]
    try:
        cp = subprocess.run(cmd, input=script, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        subprocess.run(["docker", "rm", "-f", name], capture_output=True)
        return None, None, None, f"超时（>{timeout}s）：是不是有命令在等输入 / 死循环？"
    except FileNotFoundError:
        return None, None, None, "找不到 docker（先启动 colima / Docker Desktop）"
    return cp.returncode, cp.stdout, cp.stderr, ""


def run_block(code: str, timeout: int = TIMEOUT, images=None):
    """按 IMAGES 顺序换镜像跑；返回 (ok, stdout, stderr, 说明, 用到的镜像)。"""
    cand = list(images or IMAGES)
    last = ""
    for image in cand:
        rc, out, err, msg = run_in(image, code, timeout)
        if rc is None:
            return False, out, err, msg, image
        if rc == 127 or "command not found" in (err or ""):
            tail = (err or "").strip().splitlines()
            last = f"{image} 里没有这个命令：{tail[-1] if tail else '退出码 127'}"
            continue
        warn = "" if rc == 0 else f"最后一条命令退出码 {rc}（非 0，确认是不是故意演示报错）"
        return True, out, err, warn, image
    return False, None, None, last or "所有镜像都跑不通", cand[-1]


def cmd_verify(files, args):
    total = bad = struct = unrun = unrecorded = warned = 0
    images_used = {}
    for f in files:
        text = Path(f).read_text(encoding="utf-8")
        blocks = extract_blocks(text)
        n_bad = 0
        print(f"\n== {f}｜bash 代码块 {len(blocks)} 个｜镜像 {', '.join(args.images)}（LC_ALL=C, TZ=UTC）==")
        for start, code, expected in blocks:
            if code.lstrip().startswith("# [示例环境]"):
                if norm(code) != norm(SETUP):
                    n_bad += 1
                    print(f"  ✗ 第 {start} 行起: 「示例环境」块与校验脚本里的 SETUP 不一致（两边要一模一样）")
                continue
            if expected and expected.strip().startswith(UNRUN_MARK):
                unrun += 1
                continue
            total += 1
            ok, out, err, msg, image = run_block(code, args.timeout, args.images)
            actual = norm(out or "")
            if not ok:
                n_bad += 1
                print(f"  ✗ 第 {start} 行起: {msg}")
                continue
            images_used[image] = images_used.get(image, 0) + 1
            if msg:
                warned += 1
                print(f"  ⚠ 第 {start} 行起: {msg}")
            if expected and expected.strip().startswith(STRUCT_MARK):
                struct += 1
                continue
            if expected is None:
                if actual:
                    unrecorded += 1
                    print(f"  ⚠ 第 {start} 行起: 有输出但笔记里没写结果块（缺 {len(actual.splitlines())} 行）")
                continue
            if norm(expected) != actual:
                n_bad += 1
                print(f"  ✗ 第 {start} 行起: 输出不一致")
                print(f"      期望: {norm(expected)!r}")
                print(f"      实际: {actual!r}")
        print(f"  → 该文件不一致 {n_bad} 处")
        bad += n_bad
    print(f"\n合计：比对 {total} 个块｜不一致 {bad} 个｜结构示例 {struct} 个｜未实跑 {unrun} 个"
          f"｜有输出未记录 {unrecorded} 个｜非 0 退出提醒 {warned} 个")
    if images_used:
        print("镜像使用：" + "｜".join(f"{k} {v} 块" for k, v in images_used.items()))
    if bad:
        print("不一致必须改到 0 才算通过。")
    return 1 if bad else 0


def cmd_fill(path: str, args):
    """把每个 entry 的 code 真跑一遍，把真实 stdout 写回 out 字段。"""
    src = Path(path)
    recs = [json.loads(l) for l in src.read_text(encoding="utf-8").splitlines() if l.strip()]
    filled = kept = failed = 0
    for r in recs:
        if r.get("kind") != "entry":
            continue
        out = r.get("out")
        if out and out.strip().startswith(UNRUN_MARK):
            kept += 1
            print(f"  跳过（未实跑）{r['name']}")
            continue
        ok, stdout, stderr, msg, image = run_block(r["code"], args.timeout, args.images)
        if not ok:
            failed += 1
            print(f"  ✗ {r['name']}: {msg}")
            continue
        if msg:
            print(f"  ⚠ {r['name']}: {msg}")
        actual = norm(stdout or "")
        if out and out.strip().startswith(STRUCT_MARK):
            kept += 1
            print(f"  ✓ 跑通（结构示例，保留手写结果块）{r['name']}｜{image}")
            continue
        if not actual:
            r.pop("out", None)
            print(f"  ✓ {r['name']}（无输出）｜{image}")
        else:
            r["out"] = actual
            print(f"  ✓ {r['name']}（{len(actual.splitlines())} 行输出）｜{image}")
        filled += 1
    src.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in recs) + "\n", encoding="utf-8")
    print(f"\n写入 {src}：填了 {filled} 条｜结构示例/未实跑 {kept} 条｜跑不通 {failed} 条")
    return 1 if failed else 0


def main() -> int:
    ap = argparse.ArgumentParser(description="在 Linux 容器里跑 bash 代码块并比对真实输出")
    ap.add_argument("files", nargs="*")
    ap.add_argument("--fill", metavar="ENTRIES.jsonl", help="生成模式：把真实输出写回 JSONL 的 out 字段")
    ap.add_argument("--show-fixture", action="store_true")
    ap.add_argument("--images", default=",".join(IMAGES), help="镜像候选，逗号分隔（按顺序找工具）")
    ap.add_argument("--timeout", type=int, default=TIMEOUT)
    args = ap.parse_args()
    args.images = [x for x in args.images.split(",") if x]

    if args.show_fixture:
        print("```bash")
        print(SETUP)
        print("```")
        return 0
    if args.fill:
        return cmd_fill(args.fill, args)
    if not args.files:
        ap.error("给个笔记文件，或 --fill entries.jsonl")
    return cmd_verify(args.files, args)


if __name__ == "__main__":
    raise SystemExit(main())
