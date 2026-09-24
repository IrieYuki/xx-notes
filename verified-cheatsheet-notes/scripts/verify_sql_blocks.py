#!/usr/bin/env python3
"""校验 SQL 笔记：把每个 ```sql 块**重新跑一遍**，和它后面 ```text 块里写的运行结果比对。

用法:
    python3 verify_sql_blocks.py NOTE.md [...]

前提：本脚本与笔记的生成器共用同一份示例数据（schema + seed 写在脚本里的 SCHEMA / SEED），
每条都在**全新的内存 SQLite 库**里执行，所以结果与条目顺序无关。

约定:
  * ```sql 块 = 示例语句；紧跟其后的 ```text 块 = 运行结果（生成器写的，这里只负责复核）。
  * ```text 内容等于 UNVERIFIED 时跳过该条（MySQL 专有语法、本机没有 MySQL —— 如实标注，不装成已验证）。
  * 比对前把每行行尾空白去掉（对齐用的空格不该算不一致）。

局限（写清楚，别误以为验了 MySQL）：SQLite 与 MySQL 在类型精度、字符集、默认排序规则、
日期函数上有差别；本脚本只能证明「这些语句在这份数据上确实产生这样的结果」，不能替代在真 MySQL 上跑。
"""
import re
import sqlite3
import sys
from pathlib import Path

UNVERIFIED = "（MySQL 专有语法"

SCHEMA = """
CREATE TABLE students (
    id     INT PRIMARY KEY,
    name   VARCHAR(20) NOT NULL,
    age    INT,
    gender CHAR(1),
    score  INT,
    city   VARCHAR(20)
);
CREATE TABLE courses (
    id    INT PRIMARY KEY,
    cname VARCHAR(20) NOT NULL,
    teacher VARCHAR(20)
);
CREATE TABLE scores (
    student_id INT,
    course_id  INT,
    score      INT
);
"""
SEED = """
INSERT INTO students VALUES (1, '张三', 19, '男', 92, '北京');
INSERT INTO students VALUES (2, '李四', 20, '男', 78, '上海');
INSERT INTO students VALUES (3, '王五', 19, '女', 85, '北京');
INSERT INTO students VALUES (4, '赵六', 21, '女', 60, '广州');
INSERT INTO students VALUES (5, '钱七', 20, '男', 95, '上海');
INSERT INTO students VALUES (6, '孙八', NULL, '男', NULL, NULL);   -- 故意留 NULL：用来演示 IS NULL / COUNT(列)
INSERT INTO courses VALUES (1, '数据库', '王老师');
INSERT INTO courses VALUES (2, 'C语言', '李老师');
INSERT INTO scores VALUES (1, 1, 92), (1, 2, 88), (2, 1, 78), (3, 1, 85), (4, 2, 60), (5, 1, 95);
"""


def translate(sql: str) -> str:
    sql = re.sub(r"START\s+TRANSACTION", "BEGIN", sql, flags=re.I)
    for _ in range(3):
        new = re.sub(r"CONCAT\(([^()]*)\)",
                     lambda m: "(" + " || ".join(a.strip() for a in m.group(1).split(",")) + ")",
                     sql, flags=re.I)
        if new == sql:
            break
        sql = new
    return sql


def _fmt(v):
    if v is None:
        return "NULL"
    if isinstance(v, float):
        return f"{v:g}"
    return str(v)


def split_statements(sql_text: str):
    """按分号切语句，并去掉注释行（`-- 说明` 不要当语句执行）。与生成器同一规则。"""
    out = []
    for chunk in sql_text.split(";"):
        body = "\n".join(l for l in chunk.split("\n") if not l.strip().startswith("--")).strip()
        if body:
            out.append(body)
    return out


def run_sql(sql_text: str) -> str:
    con = sqlite3.connect(":memory:")
    con.executescript(SCHEMA + SEED)
    out = []
    for stmt in split_statements(sql_text):
        cur = con.execute(translate(stmt))
        if cur.description:
            cols = [d[0] for d in cur.description]
            rows = cur.fetchall()
            lines = [" | ".join(cols)] + [" | ".join(_fmt(v) for v in r) for r in rows]
            lines.append(f"（共 {len(rows)} 行）")
            out.append("\n".join(lines))
        else:
            out.append(f"（影响 {cur.rowcount} 行）" if cur.rowcount >= 0 else "（语句已执行）")
    con.commit()
    con.close()
    return "\n\n".join(out)


def extract_pairs(md_text: str):
    """返回 [(行号, sql代码, 期望结果 or None)]：```sql 后面紧跟的 ```text 块就是期望结果。"""
    lines, i, out = md_text.split("\n"), 0, []
    while i < len(lines):
        if re.match(r"^\s*```sql\s*$", lines[i]):
            start = i + 2
            i += 1
            buf = []
            while i < len(lines) and not re.match(r"^\s*```\s*$", lines[i]):
                buf.append(lines[i])
                i += 1
            sql = "\n".join(buf)
            # 跳过紧跟的 HTML 注释，再找 ```text
            j, expected = i + 1, None
            while j < len(lines) and (lines[j].strip() == "" or lines[j].strip().startswith("<!--")):
                if lines[j].strip().startswith("<!--") and not lines[j].strip().endswith("-->"):
                    while j < len(lines) and "-->" not in lines[j]:
                        j += 1
                j += 1
            if j < len(lines) and re.match(r"^\s*```text\s*$", lines[j]):
                j += 1
                ebuf = []
                while j < len(lines) and not re.match(r"^\s*```\s*$", lines[j]):
                    ebuf.append(lines[j])
                    j += 1
                expected = "\n".join(ebuf)
            out.append((start, sql, expected))
        i += 1
    return out


def norm(text: str) -> str:
    lines = [l.rstrip() for l in text.split("\n")]
    while lines and lines[0] == "":
        lines.pop(0)
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


def main() -> int:
    total = checked = skipped = bad = 0
    for f in sys.argv[1:]:
        pairs = extract_pairs(Path(f).read_text(encoding="utf-8"))
        print(f"\n== {f}｜sql 代码块 {len(pairs)} 个 ==")
        n_skip = n_bad = 0
        for start, sql, expected in pairs:
            total += 1
            if expected is None:
                n_skip += 1
                continue
            if expected.startswith(UNVERIFIED):
                skipped += 1
                n_skip += 1
                continue
            try:
                actual = run_sql(sql)
            except Exception as ex:
                n_bad += 1
                print(f"  ✗ 第 {start} 行起: 执行失败 {ex}")
                continue
            checked += 1
            if norm(actual) != norm(expected):
                n_bad += 1
                print(f"  ✗ 第 {start} 行起: 结果不一致")
                print(f"      笔记里写的:\n{expected}\n      重跑得到:\n{actual}")
        print(f"  → 复核 {len(pairs) - n_skip} 条通过 {len(pairs) - n_skip - n_bad} 条；跳过 {n_skip} 条（未实跑/无结果）")
        bad += n_bad
    print(f"\n合计：比对 {checked} 条，不一致 {bad} 条，跳过 {skipped} 条（标了未实跑的）")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
