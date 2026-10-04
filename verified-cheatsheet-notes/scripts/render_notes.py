#!/usr/bin/env python3
"""把 JSONL 条目渲染成速查笔记 v2（解析 + 操作 + 提醒，双端兼容锚点）。

用法:  python3 render_notes.py <entries.jsonl> <输出.md>

JSONL 格式：
  第一行 kind="meta"：{title, intro, tail, lang?}
          intro = 「怎么用这份文件」等正文前的完整文本（含 --- 分隔）
          tail  = 文末「学习建议」等文本
  其余     kind="entry"：{cat, name, one, desc, params?, ret, code, warn?, out?}
          params = [[参数名, 默认值, 作用], ...]，可省略（没有参数表的条目）
          out    = 可选「运行结果」文本，渲染成紧随代码块之后的 ```text 块

v2 格式（用户定稿）：
  ### `name` one
  **解析**　desc
  （参数表）
  返回：ret
  **操作**
  ```lang
  code
  ```
  > ⚠️ warn

锚点规则（双端兼容）：
  * 锚点 = 标题的 GitHub slug（isalnum 保留、每个空格转 -、其余丢弃）
  * 标题里禁止「空格包标点」（` → `、` / `、` -x` 这类），否则 GitHub 会算出 `--`
    而 Obsidian 的 gfm-heading-links 插件会压成 `-`，链接就跳不过去；
  * 渲染时断言：每个标题的 GitHub slug == 插件 slug（\\s+ 与 -+ 都压成一个 -），
    不相等直接报错退出 —— 死链永远进不了笔记。

渲染完自查：条目数、索引链接全部命中、双端 slug 一致、代码围栏成对。
"""
import json, re, sys
from pathlib import Path


def slug(text: str) -> str:
    """GitHub 锚点算法（与 github-slugger 实测一致）。"""
    out = []
    for ch in text.strip().lower():
        if ch.isalnum() or ch in "-_":
            out.append(ch)
        elif ch == " ":
            out.append("-")
    return "".join(out)


def plugin_slug(text: str) -> str:
    """gfm-heading-links 插件（Obsidian）的算法：标点删除后把连续空白/连字符压成一个 -。"""
    s = re.sub(r"[^\w\s\-_]", "", text.strip().lower(), flags=re.UNICODE)
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s.strip("-")


def render(jsonl_path: str, out_path: str) -> dict:
    recs = [json.loads(l) for l in Path(jsonl_path).read_text(encoding="utf-8").splitlines() if l.strip()]
    meta = next(r for r in recs if r["kind"] == "meta")
    entries = [r for r in recs if r["kind"] == "entry"]

    h_of = lambda e: f"`{e['name']}` {e['one']}".strip()
    slugs = {}
    for e in entries:
        h = h_of(e)
        s = slug(h)
        assert s not in slugs, f"slug 重复：{h} 与 {slugs[s]}"
        p = plugin_slug(h)
        assert s == p, (
            f"双端锚点不一致（Obsidian 里会死链）：{h}\n"
            f"  GitHub slug: {s}\n  插件 slug:   {p}\n"
            f"  改法：标题里去掉「空格包标点」（→ / ↔ 贴字写，命令选项并进正文）"
        )
        slugs[s] = h

    out = [f"# {meta['title']}\n", meta["intro"] + "\n", "---\n",
           "## 索引 · 速查表\n",
           "| 分类 | 用法（点击跳转） | 一句话作用 |",
           "|------|------------------|-----------|"]
    for e in entries:
        out.append(f"| {e['cat'].replace(chr(0x3000), ' ')} | [`{e['name']}`](#{slug(h_of(e))}) | {e['one']} |")
    out.append("\n---\n")

    fence = meta.get("lang", "python")
    cur = None
    for e in entries:
        if e["cat"] != cur:
            cur = e["cat"]
            out.append(f"## {cur.replace(chr(0x3000), ' ')}\n")
        out.append(f"### {h_of(e)}\n")
        out.append(f"**解析**　{e['desc']}\n")
        params = e.get("params") or []
        if params:
            out.append("| 参数 | 默认值 | 作用 |")
            out.append("|------|--------|------|")
            for p in params:
                out.append(f"| {p[0]} | {p[1]} | {p[2]} |")
            out.append("")
        out.append(f"返回：{e['ret']}\n")
        out.append("**操作**")
        out.append("")
        ops = e.get("ops")
        if ops:
            for k, op in enumerate(ops):
                out.append(f"```{fence}")
                out.append(op["code"].strip("\n"))
                out.append("```")
                if op.get("out"):
                    out.append("```text")
                    out.append(op["out"].strip("\n"))
                    out.append("```")
                out.append("")
        else:
            out.append(f"```{fence}")
            out.append(e["code"].strip("\n"))
            out.append("```")
            if e.get("out"):
                out.append("```text")
                out.append(e["out"].strip("\n"))
                out.append("```")
            out.append("")
        if e.get("warn"):
            out.append(f"> ⚠️ {e['warn']}\n")

    out.append(meta["tail"])
    text = "\n".join(out).rstrip("\n") + "\n"
    Path(out_path).write_text(text, encoding="utf-8")

    links = re.findall(r"\]\(#([^)#]+)\)", text)
    bad = [l for l in links if l not in slugs]
    assert not bad, f"索引死链：{bad[:5]}"
    return dict(entries=len(entries), chars=len(text), lines=text.count("\n") + 1,
                fences=text.count("```"), links=len(links))


if __name__ == "__main__":
    info = render(sys.argv[1], sys.argv[2])
    print(f"渲染 {sys.argv[2]}")
    print(f"  条目 {info['entries']} 条｜{info['lines']} 行｜{info['chars']} 字符")
    print(f"  索引链接 {info['links']} 个，全部命中")
    print(f"  代码围栏 {info['fences']} 个（应为偶数）")
    raise SystemExit(1 if info["fences"] % 2 else 0)
