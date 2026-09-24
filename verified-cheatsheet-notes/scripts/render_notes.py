#!/usr/bin/env python3
"""把 JSONL 条目渲染成速查笔记（索引前置 + 统一三格 + 可跳转锚点）。

用法:  python3 render_notes.py <entries.jsonl> <输出.md>

JSONL 格式：
  第一行 kind="meta"：{title, intro, tail}
  其余     kind="entry"：{cat, name, one, sig, ret, note, code, warn?}

设计约束（别改成手写正文，否则格式会漂）：
  * 索引表、正文、锚点全部从同一份数据生成 —— 三老永远不会不一致；
  * 锚点 = 标题的 GitHub slug（isalnum 保留、空格转 -、其余丢弃），slug 必须唯一，
    否则断言失败（用 `l.append` / `d.pop` 这种带接收者前缀的命名避免撞车）；
  * 条目里 sig 不可再出现全角 `｜`（会破坏「签名｜返回｜备注」三格），写 ` / ` 分隔。

渲染完会自查：条目数、索引链接是否全部命中、代码围栏是否成对。
生成注释（`# 真实输出`）用另一份脚本：把表达式真跑一遍、直接把 repr 写进注释。
"""
import json, re, sys
from pathlib import Path


def slug(text: str) -> str:
    out = []
    for ch in text.strip().lower():
        if ch.isalnum() or ch in "-_":
            out.append(ch)
        elif ch == " ":
            out.append("-")
    return "".join(out)


def render(jsonl_path: str, out_path: str) -> dict:
    recs = [json.loads(l) for l in Path(jsonl_path).read_text(encoding="utf-8").splitlines() if l.strip()]
    meta = next(r for r in recs if r["kind"] == "meta")
    entries = [r for r in recs if r["kind"] == "entry"]

    h_of = lambda e: f"`{e['name']}` {e['one']}"
    slugs = {}
    for e in entries:
        s = slug(h_of(e))
        assert s not in slugs, f"slug 重复：{h_of(e)} 与 {slugs[s]}"
        slugs[s] = h_of(e)

    out = [f"# {meta['title']}\n", meta["intro"] + "\n", "---\n",
           "## 索引 · 速查表\n",
           "| 分类 | 用法（点击跳转） | 一句话作用 |",
           "|------|------------------|-----------|"]
    for e in entries:
        out.append(f"| {e['cat'].replace(chr(0x3000), ' ')} | [`{e['name']}`](#{slug(h_of(e))}) | {e['one']} |")
    out.append("\n---\n")

    cur = None
    for e in entries:
        if e["cat"] != cur:
            cur = e["cat"]
            out.append(f"## {cur}\n")
        out.append(f"### {h_of(e)}\n")
        out.append(f"**签名** {e['sig']} ｜ **返回** {e['ret']} ｜ **备注** {e['note']}\n")
        out.append("```python")
        out.append(e["code"])
        out.append("```\n")
        if e.get("warn"):
            out.append(f"> ⚠️ {e['warn']}\n")

    out.append(meta["tail"])
    text = "\n".join(out)
    Path(out_path).write_text(text, encoding="utf-8")

    links = re.findall(r"\]\(#([^)]+)\)", text)
    return dict(entries=len(entries), chars=len(text), lines=text.count("\n") + 1,
                fences=text.count("```"), links=len(links),
                bad_links=[l for l in links if l not in slugs])


if __name__ == "__main__":
    info = render(sys.argv[1], sys.argv[2])
    print(f"渲染 {sys.argv[2]}")
    print(f"  条目 {info['entries']} 条｜{info['lines']} 行｜{info['chars']} 字符")
    print(f"  索引链接 {info['links']} 个，失效 {len(info['bad_links'])} 个 {info['bad_links'][:3]}")
    print(f"  代码围栏 {info['fences']} 个（应为偶数）")
    raise SystemExit(1 if info["bad_links"] or info["fences"] % 2 else 0)
