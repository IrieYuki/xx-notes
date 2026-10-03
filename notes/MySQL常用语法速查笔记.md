# MySQL 常用语法速查笔记

> 整理范围：MySQL 建表、增删改查、连接、分组、子查询、索引、事务里**最常用的语法**。
> 每条示例下面都有一段「运行结果」，是把语句真跑一遍得到的真实输出，不是照抄文档写的。
>
> ⚠️ 先说清楚执行环境：**本机没有装 MySQL**，所以可移植的语句（建表、增删改查、连接、分组、
> 子查询、事务、索引、视图）是用 Python 自带的 SQLite 真跑的 —— 这些语句在 MySQL 里写法完全一致；
> 少数 MySQL 独有语法（`AUTO_INCREMENT`、`SHOW`、`DATE_FORMAT`、`TRUNCATE` 等）在结果里标了
> 「未实跑」，它们照着写没问题，但结果请以你自己的 MySQL 为准。
>
> 本文用的示例数据（每条示例都从这份数据重新开始执行，所以各条结果互不影响）：
>
**students**（6 行）

| id | name | age | gender | score | city |
|---|---|---|---|---|---|
| 1 | 张三 | 19 | 男 | 92 | 北京 |
| 2 | 李四 | 20 | 男 | 78 | 上海 |
| 3 | 王五 | 19 | 女 | 85 | 北京 |
| 4 | 赵六 | 21 | 女 | 60 | 广州 |
| 5 | 钱七 | 20 | 男 | 95 | 上海 |
| 6 | 孙八 | NULL | 男 | NULL | NULL |

**courses**（2 行）

| id | cname | teacher |
|---|---|---|
| 1 | 数据库 | 王老师 |
| 2 | C语言 | 李老师 |

**scores**（6 行）

| student_id | course_id | score |
|---|---|---|
| 1 | 1 | 92 |
| 1 | 2 | 88 |
| 2 | 1 | 78 |
| 3 | 1 | 85 |
| 4 | 2 | 60 |
| 5 | 1 | 95 |


---

## 索引 · 速查表

| 分类 | 用法（点击跳转） | 一句话作用 |
|------|------------------|-----------|
| C1 基础语法与数据类型 | [`第一条 SQL 与注释`](#第一条-sql-与注释-最小可执行的查询--两种注释写法) | 最小可执行的查询 / 两种注释写法 |
| C1 基础语法与数据类型 | [`常用数据类型`](#常用数据类型-建表时字段该选什么类型) | 建表时字段该选什么类型 |
| C1 基础语法与数据类型 | [`建库 / 切库 / 看库`](#建库--切库--看库-库是表的容器) | 库是表的容器 |
| C2 建表与修改表 | [`CREATE TABLE 与常用约束`](#create-table-与常用约束-建表主键--非空--默认值--唯一) | 建表：主键 / 非空 / 默认值 / 唯一 |
| C2 建表与修改表 | [`自增主键 AUTO_INCREMENT`](#自增主键-auto_increment-插入时不用操心-id) | 插入时不用操心 id |
| C2 建表与修改表 | [`ALTER TABLE 加列 / 改名 / 删列`](#alter-table-加列--改名--删列-表建好之后改结构) | 表建好之后改结构 |
| C2 建表与修改表 | [`外键 FOREIGN KEY`](#外键-foreign-key-让两张表的数据对得上) | 让两张表的数据对得上 |
| C2 建表与修改表 | [`DROP TABLE 删表`](#drop-table-删表-把表连数据一起删掉) | 把表连数据一起删掉 |
| C3 插入数据 | [`INSERT 插入数据`](#insert-插入数据-插一行--插多行--只给部分列) | 插一行 / 插多行 / 只给部分列 |
| C3 插入数据 | [`INSERT INTO ... SELECT 从查询结果插入`](#insert-into--select-从查询结果插入-把-a-表的数据搬进-b-表) | 把 A 表的数据搬进 B 表 |
| C3 插入数据 | [`事务里批量插入`](#事务里批量插入-要么全成功要么全不生效) | 要么全成功，要么全不生效 |
| C4 查询基础 | [`SELECT 查询列与别名`](#select-查询列与别名-查什么怎么起名字能不能算) | 查什么、怎么起名字、能不能算 |
| C4 查询基础 | [`DISTINCT 去重`](#distinct-去重-看一列里有哪些不同的值) | 看一列里有哪些不同的值 |
| C4 查询基础 | [`WHERE 与 ORDER BY`](#where-与-order-by-筛选--排序升序--降序--多字段) | 筛选 + 排序（升序 / 降序 / 多字段） |
| C4 查询基础 | [`LIMIT 限制条数与分页`](#limit-限制条数与分页-只要前几条--分页取数据) | 只要前几条 / 分页取数据 |
| C5 条件与运算符 | [`AND / OR / NOT 与括号`](#and--or--not-与括号-多个条件一起用) | 多个条件一起用 |
| C5 条件与运算符 | [`BETWEEN 与 IN`](#between-与-in-区间--若干个候选值) | 区间 / 若干个候选值 |
| C5 条件与运算符 | [`LIKE 模糊查询`](#like-模糊查询-按模式匹配文字) | 按模式匹配文字 |
| C5 条件与运算符 | [`IS NULL / IS NOT NULL 与 COUNT 的区别`](#is-null--is-not-null-与-count-的区别-空值判断和数数的两种口径) | 空值判断和数数的两种口径 |
| C6 聚合函数与分组 | [`五个常用聚合函数`](#五个常用聚合函数-数数求和平均最大最小) | 数数、求和、平均、最大最小 |
| C6 聚合函数与分组 | [`GROUP BY 分组统计`](#group-by-分组统计-按某个字段分组每组各算一份) | 按某个字段分组，每组各算一份 |
| C6 聚合函数与分组 | [`HAVING 过滤分组`](#having-过滤分组-分组之后再筛选) | 分组之后再筛选 |
| C6 聚合函数与分组 | [`GROUP BY 多个字段`](#group-by-多个字段-按两个维度交叉统计) | 按两个维度交叉统计 |
| C7 多表连接 | [`INNER JOIN 内连接`](#inner-join-内连接-只留下两边都能对上的行) | 只留下两边都能对上的行 |
| C7 多表连接 | [`LEFT JOIN 左连接`](#left-join-左连接-左表全保留右表没数据就是-null) | 左表全保留，右表没数据就是 NULL |
| C7 多表连接 | [`UNION 合并两个查询结果`](#union-合并两个查询结果-上下拼起来可去重) | 上下拼起来（可去重） |
| C8 子查询与条件逻辑 | [`子查询（放在 WHERE 里）`](#子查询放在-where-里-把一次查询的结果当条件) | 把一次查询的结果当条件 |
| C8 子查询与条件逻辑 | [`EXISTS 子查询`](#exists-子查询-只判断有没有) | 只判断「有没有」 |
| C8 子查询与条件逻辑 | [`CASE WHEN 条件分支`](#case-when-条件分支-在-sql-里写-if-else) | 在 SQL 里写 if-else |
| C8 子查询与条件逻辑 | [`IFNULL 与 COALESCE`](#ifnull-与-coalesce-把-null-换成想要的默认值) | 把 NULL 换成想要的默认值 |
| C9 更新与删除 | [`UPDATE 更新数据`](#update-更新数据-改已有数据的值) | 改已有数据的值 |
| C9 更新与删除 | [`DELETE 删除数据`](#delete-删除数据-删掉符合条件的行) | 删掉符合条件的行 |
| C9 更新与删除 | [`TRUNCATE 与 DELETE 的区别`](#truncate-与-delete-的区别-清空全表更快的方式) | 清空全表更快的方式 |
| C10 常用函数（字符串 / 数字 / 类型转换） | [`字符串函数`](#字符串函数-拼接--截取--大小写--去空格--替换) | 拼接 / 截取 / 大小写 / 去空格 / 替换 |
| C10 常用函数（字符串 / 数字 / 类型转换） | [`日期与时间函数`](#日期与时间函数-取当前时间--格式化--算天数差) | 取当前时间 / 格式化 / 算天数差 |
| C10 常用函数（字符串 / 数字 / 类型转换） | [`数学函数`](#数学函数-四舍五入--取整--绝对值--余数) | 四舍五入 / 取整 / 绝对值 / 余数 |
| C10 常用函数（字符串 / 数字 / 类型转换） | [`类型转换 CAST`](#类型转换-cast-字符串和数字互转) | 字符串和数字互转 |
| C11 索引 | [`建索引 CREATE INDEX`](#建索引-create-index-让查询变快) | 让查询变快 |
| C11 索引 | [`复合索引与最左前缀`](#复合索引与最左前缀-多个列一起建索引) | 多个列一起建索引 |
| C11 索引 | [`查看表结构 / 索引 / 建表语句`](#查看表结构--索引--建表语句-接手一个库先看有什么) | 接手一个库先看有什么 |
| C12 事务与视图 | [`事务 COMMIT 与 ROLLBACK`](#事务-commit-与-rollback-要么全成功要么全撤销) | 要么全成功、要么全撤销 |
| C12 事务与视图 | [`CREATE VIEW 视图`](#create-view-视图-把常用查询存成一个虚拟表) | 把常用查询存成一个「虚拟表」 |
| C12 事务与视图 | [`用户与权限`](#用户与权限-给程序建一个专用账号) | 给程序建一个专用账号 |

---

## C1 基础语法与数据类型

### `第一条 SQL 与注释` 最小可执行的查询 / 两种注释写法

**签名** SELECT 表达式 AS 别名; ｜ **返回** 一张结果表（几行几列） ｜ **备注** 语句末尾要有分号；`AS` 起别名让结果表更好读

```sql
SELECT 1 + 1 AS result, '你好' AS greeting;
```

```text
result | greeting
2 | 你好
（共 1 行）
```

### `常用数据类型` 建表时字段该选什么类型

**签名** INT ､ VARCHAR(n) ､ CHAR(n) ､ DECIMAL(m,d) ､ TEXT ､ DATE ､ FLOAT ｜ **返回** — ｜ **备注** 金额用 `DECIMAL`（精确），科学计算用 `FLOAT/DOUBLE`（近似）；`VARCHAR` 变长、`CHAR` 定长

```sql
CREATE TABLE demo_types (
    id    INT,              -- 整数
    name  VARCHAR(20),      -- 变长字符串（最多 20 个字符）
    code  CHAR(4),          -- 定长字符串（固定 4 位，如 'A001'）
    price DECIMAL(6, 2),    -- 精确小数：总共 6 位、其中小数 2 位 → 最大 9999.99
    intro TEXT,             -- 长文本（几百字以上用它）
    born  DATE,             -- 日期 '2026-09-24'
    score FLOAT             -- 近似小数
);
```

```text
（语句已执行）
```

> ⚠️ `VARCHAR` 存的是「实际长度」，`CHAR` 不足长度会补空格；主键一般用 `INT`（够快够省）。

### `建库 / 切库 / 看库` 库是表的容器

**签名** CREATE DATABASE 库名;   /   USE 库名;   /   SHOW DATABASES; ｜ **返回** — ｜ **备注** MySQL 里表都属于某个库；一条语句只能操作当前库里的表，除非写全名 `库名.表名`

```sql
CREATE DATABASE school DEFAULT CHARSET utf8mb4;   -- 建库，推荐 utf8mb4（能存 emoji）
USE school;                                       -- 切到 / 进入这个库
SHOW DATABASES;                                   -- 列出所有库
SELECT DATABASE();                                -- 看现在在哪个库
SHOW TABLES;                                      -- 看当前库有哪些表
```

```text
（MySQL 专有语法，本机没有装 MySQL，这条未实跑 —— 以官方文档为准）
```

> ⚠️ 这几条是 MySQL 服务端/客户端专有命令，本机没装 MySQL 所以**未实跑**；`DROP DATABASE 库名;` 会连库带表全删，慎用。

## C2 建表与修改表

### `CREATE TABLE 与常用约束` 建表：主键 / 非空 / 默认值 / 唯一

**签名** CREATE TABLE 表名 (字段 类型 约束, ...); ｜ **返回** —（建表语句没有结果集） ｜ **备注** 四个最常用约束：`PRIMARY KEY` 主键、`NOT NULL` 非空、`DEFAULT` 默认值、`UNIQUE` 唯一

```sql
CREATE TABLE classes (                  -- 示例数据里已经有 students，这里另建一张 classes 演示
    id    INT PRIMARY KEY,              -- 主键：唯一且不能为空
    name  VARCHAR(20) NOT NULL,         -- 不允许存 NULL
    age   INT,
    city  VARCHAR(20) DEFAULT '未知',   -- 不写这一列时自动用默认值
    email VARCHAR(50) UNIQUE            -- 该列的值不能重复
);
INSERT INTO classes (id, name) VALUES (1, '张三');
INSERT INTO classes (id, name, city, email) VALUES (2, '李四', '北京', 'lisi@example.com');
SELECT * FROM classes;
```

```text
（语句已执行）

（影响 1 行）

（影响 1 行）

id | name | age | city | email
1 | 张三 | NULL | 未知 | NULL
2 | 李四 | NULL | 北京 | lisi@example.com
（共 2 行）
```

### `自增主键 AUTO_INCREMENT` 插入时不用操心 id

**签名** id INT AUTO_INCREMENT PRIMARY KEY ｜ **返回** — ｜ **备注** 自增列**必须**是键；插入时不给它值，数据库自动填 1、2、3…

```sql
CREATE TABLE students2 (
    id   INT AUTO_INCREMENT PRIMARY KEY,     -- 不用手写 id
    name VARCHAR(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;     -- 常用引擎 + 字符集

INSERT INTO students2 (name) VALUES ('张三'), ('李四');
SELECT * FROM students2;
SELECT LAST_INSERT_ID();                     -- 刚插入那行的自增 id
```

```text
（MySQL 专有语法，本机没有装 MySQL，这条未实跑 —— 以官方文档为准）
```

> ⚠️ `AUTO_INCREMENT`、`ENGINE=InnoDB`、`LAST_INSERT_ID()` 都是 MySQL 专有，本机没装 MySQL 所以**未实跑**；效果是 id 自动变成 1、2。删掉的行不会把号让出来。

### `ALTER TABLE 加列 / 改名 / 删列` 表建好之后改结构

**签名** ALTER TABLE 表名 ADD / RENAME COLUMN / DROP COLUMN ...; ｜ **返回** — ｜ **备注** 已经存了数据的表也能改；加 `NOT NULL` 列时要给默认值，否则老数据没法填

```sql
ALTER TABLE students ADD COLUMN phone VARCHAR(20);       -- 加一列
ALTER TABLE students RENAME COLUMN city TO hometown;     -- 改列名
ALTER TABLE students DROP COLUMN phone;                  -- 删一列
SELECT id, name, hometown FROM students LIMIT 3;         -- 看看结果
```

```text
（语句已执行）

（语句已执行）

（语句已执行）

id | name | hometown
1 | 张三 | 北京
2 | 李四 | 上海
3 | 王五 | 北京
（共 3 行）
```

> ⚠️ MySQL 里改**类型**用 `ALTER TABLE students MODIFY COLUMN age TINYINT;`（TINYINT 只占 1 字节），加索引用 `ADD INDEX`——这两种写法和 SQLite 不同，本机未实跑。

### `外键 FOREIGN KEY` 让两张表的数据对得上

**签名** FOREIGN KEY (本表字段) REFERENCES 另一张表(它的主键) ｜ **返回** — ｜ **备注** 外键保证「引用的那条记录真的存在」；`ON DELETE CASCADE` 表示主表删了，子表跟着删

```sql
CREATE TABLE scores2 (
    id         INT PRIMARY KEY,
    student_id INT,
    score      INT,
    FOREIGN KEY (student_id) REFERENCES students(id)   -- 学号必须存在于 students
);
INSERT INTO scores2 VALUES (1, 1, 92);
SELECT * FROM scores2;
```

```text
（语句已执行）

（影响 1 行）

id | student_id | score
1 | 1 | 92
（共 1 行）
```

> ⚠️ MySQL 中外键要求两张表都用 InnoDB 引擎（8.0 默认就是）；有了外键，删主表里被引用的行会被拦住（除非写了级联规则）。

### `DROP TABLE 删表` 把表连数据一起删掉

**签名** DROP TABLE 表名;   /   DROP TABLE IF EXISTS 表名; ｜ **返回** — ｜ **备注** `DROP TABLE` 是**结构 + 数据**全删，不可恢复；加 `IF EXISTS` 可以避免表不存在时报错

```sql
CREATE TABLE tmp (id INT, note VARCHAR(20));
INSERT INTO tmp VALUES (1, 'a'), (2, 'b');
SELECT COUNT(*) AS 行数 FROM tmp;
DROP TABLE tmp;
```

```text
（语句已执行）

（影响 2 行）

行数
2
（共 1 行）

（语句已执行）
```

> ⚠️ 只清数据、保留表结构要用 `TRUNCATE TABLE 表名;`（MySQL 专有，见「更新与删除」一节）。

## C3 插入数据

### `INSERT 插入数据` 插一行 / 插多行 / 只给部分列

**签名** INSERT INTO 表名 (列, ...) VALUES (值, ...), (...); ｜ **返回** int（影响的行数） ｜ **备注** 指定列时可以省略的列要有默认值或允许 NULL；一次插多行比分多次快得多

```sql
INSERT INTO students VALUES (7, '周九', 22, '男', 88, '深圳');            -- 按顺序给全部列
INSERT INTO students (id, name, city) VALUES (8, '吴十', '杭州');          -- 只给部分列
INSERT INTO students (id, name, score) VALUES (9, '郑十一', 70), (10, '王十二', 66);  -- 一次插多行
SELECT * FROM students WHERE id >= 7;
```

```text
（影响 1 行）

（影响 1 行）

（影响 2 行）

id | name | age | gender | score | city
7 | 周九 | 22 | 男 | 88 | 深圳
8 | 吴十 | NULL | NULL | NULL | 杭州
9 | 郑十一 | NULL | NULL | 70 | NULL
10 | 王十二 | NULL | NULL | 66 | NULL
（共 4 行）
```

### `INSERT INTO ... SELECT 从查询结果插入` 把 A 表的数据搬进 B 表

**签名** INSERT INTO 目标表 (列, ...) SELECT 列, ... FROM 源表 WHERE ...; ｜ **返回** int（影响的行数） ｜ **备注** 列的顺序和个数要一一对应；常用于备份、汇总、把中间结果落到表里

```sql
CREATE TABLE good_students (id INT, name VARCHAR(20), score INT);
INSERT INTO good_students
SELECT id, name, score FROM students WHERE score >= 85;
SELECT * FROM good_students ORDER BY score DESC;
```

```text
（语句已执行）

（影响 3 行）

id | name | score
5 | 钱七 | 95
1 | 张三 | 92
3 | 王五 | 85
（共 3 行）
```

### `事务里批量插入` 要么全成功，要么全不生效

**签名** START TRANSACTION; ... COMMIT;   /   ROLLBACK; ｜ **返回** int（各语句影响的行数） ｜ **备注** 多条 INSERT/UPDATE 放在一起，中途出错就 `ROLLBACK` 回滚，不会插一半

```sql
START TRANSACTION;                                  -- MySQL 的写法（SQLite 里是 BEGIN）
INSERT INTO students (id, name) VALUES (11, '甲同学');
INSERT INTO students (id, name) VALUES (12, '乙同学');
COMMIT;                                             -- 确认提交
SELECT COUNT(*) AS 学生总数 FROM students;
```

```text
（语句已执行）

（影响 1 行）

（影响 1 行）

（语句已执行）

学生总数
8
（共 1 行）
```

> ⚠️ 忘记 `COMMIT` 时连接一断就会回滚；`DROP TABLE` / `CREATE TABLE` 这类 DDL 在 MySQL 里会**隐式提交**，没法回滚。

## C4 查询基础

### `SELECT 查询列与别名` 查什么、怎么起名字、能不能算

**签名** SELECT 列 [AS 别名], ... FROM 表; ｜ **返回** 一张结果表 ｜ **备注** `*` 是「所有列」，正式代码里建议写清楚列名；列名后可以跟表达式做计算

```sql
SELECT name, score FROM students;
SELECT name AS 姓名, score AS 分数, score + 5 AS 加分后 FROM students WHERE id = 1;
SELECT name, ROUND(score * 0.6, 1) AS 折后分 FROM students WHERE score IS NOT NULL;
```

```text
name | score
张三 | 92
李四 | 78
王五 | 85
赵六 | 60
钱七 | 95
孙八 | NULL
（共 6 行）

姓名 | 分数 | 加分后
张三 | 92 | 97
（共 1 行）

name | 折后分
张三 | 55.2
李四 | 46.8
王五 | 51
赵六 | 36
钱七 | 57
（共 5 行）
```

### `DISTINCT 去重` 看一列里有哪些不同的值

**签名** SELECT DISTINCT 列 FROM 表; ｜ **返回** 去重后的结果表 ｜ **备注** `DISTINCT` 管的是**整行组合**都相同才算重复；`COUNT(DISTINCT 列)` 可以数不同值有几个

```sql
SELECT DISTINCT city FROM students;
SELECT COUNT(DISTINCT city) AS 城市种类 FROM students;
```

```text
city
北京
上海
广州
NULL
（共 4 行）

城市种类
3
（共 1 行）
```

### `WHERE 与 ORDER BY` 筛选 + 排序（升序 / 降序 / 多字段）

**签名** SELECT ... FROM 表 WHERE 条件 ORDER BY 列 [ASC|DESC], ...; ｜ **返回** 排好序的结果表 ｜ **备注** `ASC` 升序（默认）、`DESC` 降序；多字段排序按顺序比较（前一个相同才看后一个）

```sql
SELECT name, score FROM students WHERE score IS NOT NULL ORDER BY score DESC;
SELECT name, age, score FROM students ORDER BY age DESC, score DESC;
```

```text
name | score
钱七 | 95
张三 | 92
王五 | 85
李四 | 78
赵六 | 60
（共 5 行）

name | age | score
赵六 | 21 | 60
钱七 | 20 | 95
李四 | 20 | 78
张三 | 19 | 92
王五 | 19 | 85
孙八 | NULL | NULL
（共 6 行）
```

> ⚠️ 排序时 NULL 会被当成「最小值」：升序时排最前，降序时排最后。

### `LIMIT 限制条数与分页` 只要前几条 / 分页取数据

**签名** LIMIT 条数 OFFSET 跳过条数; ｜ **返回** 前 N 条的结果表 ｜ **备注** 分页公式：第 p 页、每页 n 条 → `LIMIT n OFFSET (p-1)*n`

```sql
SELECT name, score FROM students WHERE score IS NOT NULL ORDER BY score DESC LIMIT 3;
SELECT name, score FROM students WHERE score IS NOT NULL ORDER BY score DESC LIMIT 2 OFFSET 2;
```

```text
name | score
钱七 | 95
张三 | 92
王五 | 85
（共 3 行）

name | score
王五 | 85
李四 | 78
（共 2 行）
```

> ⚠️ MySQL 也支持简写 `LIMIT 2, 3`（跳过 2 条、取 3 条），但 `LIMIT 3 OFFSET 2` 更清楚；排序不写时顺序不保证，分页一定要配 `ORDER BY`。

## C5 条件与运算符

### `AND / OR / NOT 与括号` 多个条件一起用

**签名** WHERE 条件1 AND 条件2   /   OR   /   NOT   /   ( ) ｜ **返回** 符合条件的结果表 ｜ **备注** `AND` 比 `OR` 优先级高，混用时**一定要加括号**说清意图

```sql
SELECT name, city, score FROM students
WHERE (city = '北京' OR city = '上海') AND score >= 85;

SELECT name, score FROM students WHERE NOT (score < 85) AND score IS NOT NULL;
```

```text
name | city | score
张三 | 北京 | 92
王五 | 北京 | 85
钱七 | 上海 | 95
（共 3 行）

name | score
张三 | 92
王五 | 85
钱七 | 95
（共 3 行）
```

> ⚠️ `score >= 85 AND score <= 95` 等价于 `score BETWEEN 85 AND 95`；写反括号是新手最常见的逻辑错误。

### `BETWEEN 与 IN` 区间 / 若干个候选值

**签名** BETWEEN 小 AND 大   /   IN (值1, 值2, ...) ｜ **返回** 符合条件的结果表 ｜ **备注** `BETWEEN` 是**闭区间**（含两头）；`NOT IN` 遇到 NULL 会翻车，慎用

```sql
SELECT name, score FROM students WHERE score BETWEEN 85 AND 95 ORDER BY score;
SELECT name, city FROM students WHERE city IN ('北京', '广州');
```

```text
name | score
王五 | 85
张三 | 92
钱七 | 95
（共 3 行）

name | city
张三 | 北京
王五 | 北京
赵六 | 广州
（共 3 行）
```

> ⚠️ `IN` 里可以放子查询：`WHERE id IN (SELECT student_id FROM scores)`。

### `LIKE 模糊查询` 按模式匹配文字

**签名** LIKE '模式'   其中 % 代表任意多个字符，_ 代表一个字符 ｜ **返回** 符合模式的结果表 ｜ **备注** `%张%` 任意位置含「张」、`张%` 以「张」开头、`%张` 以「张」结尾

```sql
SELECT name FROM students WHERE name LIKE '张%';      -- 张开头
SELECT name, city FROM students WHERE city LIKE '%海'; -- 海结尾
SELECT name FROM students WHERE name LIKE '__';        -- 恰好两个字的姓名
```

```text
name
张三
（共 1 行）

name | city
李四 | 上海
钱七 | 上海
（共 2 行）

name
张三
李四
王五
赵六
钱七
孙八
（共 6 行）
```

> ⚠️ `LIKE '%张%'` 用不上索引（前面有通配符），数据量大时会慢；需要全文搜索应该用专门的方案。

### `IS NULL / IS NOT NULL 与 COUNT 的区别` 空值判断和数数的两种口径

**签名** 列 IS NULL   /   COUNT(*)   /   COUNT(列) ｜ **返回** 条件判断是真假；COUNT 是一个数字 ｜ **备注** NULL 表示「没有值」，不能用 `= NULL` 比较；`COUNT(*)` 数行数、`COUNT(列)` 只数该列非 NULL 的行

```sql
SELECT name, age FROM students WHERE age IS NULL;
SELECT COUNT(*) AS 总人数,
       COUNT(score) AS 有成绩人数,
       COUNT(*) - COUNT(score) AS 没成绩人数
FROM students;
```

```text
name | age
孙八 | NULL
（共 1 行）

总人数 | 有成绩人数 | 没成绩人数
6 | 5 | 1
（共 1 行）
```

> ⚠️ 聚合函数（SUM/AVG/MAX/MIN）会自动**跳过 NULL**：`AVG(score)` 算的是「有成绩的人」的平均分。

## C6 聚合函数与分组

### `五个常用聚合函数` 数数、求和、平均、最大最小

**签名** COUNT(*) ､ SUM(列) ､ AVG(列) ､ MAX(列) ､ MIN(列) ｜ **返回** 一行一列（汇总值） ｜ **备注** 它们把「很多行」压成「一个数」；`COUNT(*)` 数行数、`COUNT(列)` 只数非 NULL 的行

```sql
SELECT COUNT(*)          AS 总人数,
       COUNT(score)      AS 有成绩人数,
       SUM(score)        AS 总分,
       ROUND(AVG(score), 2) AS 平均分,
       MAX(score)        AS 最高分,
       MIN(score)        AS 最低分
FROM students;
```

```text
总人数 | 有成绩人数 | 总分 | 平均分 | 最高分 | 最低分
6 | 5 | 410 | 82 | 95 | 60
（共 1 行）
```

### `GROUP BY 分组统计` 按某个字段分组，每组各算一份

**签名** SELECT 分组列, 聚合函数 FROM 表 GROUP BY 分组列; ｜ **返回** 每组一行 ｜ **备注** `SELECT` 里只能出现「分组列」和「聚合函数」（MySQL 8 默认强制这条规则）

```sql
SELECT city, COUNT(*) AS 人数, ROUND(AVG(score), 1) AS 平均分
FROM students
GROUP BY city
ORDER BY 人数 DESC;
```

```text
city | 人数 | 平均分
北京 | 2 | 88.5
上海 | 2 | 86.5
广州 | 1 | 60
NULL | 1 | NULL
（共 4 行）
```

> ⚠️ `city` 为 NULL 的那些行会单独变成一组；想给这组取个名字用 `IFNULL(city, '未填写')` 当分组列。

### `HAVING 过滤分组` 分组之后再筛选

**签名** GROUP BY ... HAVING 聚合条件 ｜ **返回** 留下来的组 ｜ **备注** `WHERE` 在分组**前**过滤行，`HAVING` 在分组**后**过滤组；聚合结果的条件只能写在 `HAVING` 里

```sql
SELECT gender, COUNT(*) AS 人数, ROUND(AVG(score), 1) AS 平均分
FROM students
GROUP BY gender
HAVING AVG(score) > 80;
```

```text
gender | 人数 | 平均分
男 | 4 | 88.3
（共 1 行）
```

### `GROUP BY 多个字段` 按两个维度交叉统计

**签名** GROUP BY 列1, 列2 ｜ **返回** 每个「组合」一行 ｜ **备注** 组合的先后顺序影响结果顺序，用 `ORDER BY` 明确排一下更稳

```sql
SELECT city, gender, COUNT(*) AS 人数
FROM students
GROUP BY city, gender
ORDER BY city, gender;
```

```text
city | gender | 人数
NULL | 男 | 1
上海 | 男 | 2
北京 | 女 | 1
北京 | 男 | 1
广州 | 女 | 1
（共 5 行）
```

## C7 多表连接

### `INNER JOIN 内连接` 只留下两边都能对上的行

**签名** SELECT ... FROM A JOIN B ON A.字段 = B.字段; ｜ **返回** 连接后的结果表 ｜ **备注** `JOIN` 默认就是 `INNER JOIN`；`ON` 写「两张表的哪两个字段相等」

```sql
SELECT s.name AS 姓名, c.cname AS 课程, sc.score AS 分数
FROM scores sc
JOIN students s ON sc.student_id = s.id
JOIN courses  c ON sc.course_id  = c.id
ORDER BY s.name, c.cname;
```

```text
姓名 | 课程 | 分数
张三 | C语言 | 88
张三 | 数据库 | 92
李四 | 数据库 | 78
王五 | 数据库 | 85
赵六 | C语言 | 60
钱七 | 数据库 | 95
（共 6 行）
```

> ⚠️ 三张表连接就是再写一个 `JOIN ... ON ...`；表名太长时用别名（`students s`）能让语句短很多。

### `LEFT JOIN 左连接` 左表全保留，右表没数据就是 NULL

**签名** A LEFT JOIN B ON 条件 ｜ **返回** 左表每一行至少一行，右表缺失处为 NULL ｜ **备注** 用来找「没有对应数据」的行（右表字段 IS NULL 就是没配对上的）

```sql
SELECT s.name AS 姓名, sc.score AS 分数
FROM students s
LEFT JOIN scores sc ON s.id = sc.student_id
ORDER BY 姓名;

-- 右连接的写法：把两张表换个位置即可（结果等价）
SELECT c.cname AS 课程, COUNT(sc.student_id) AS 选课人数
FROM scores sc RIGHT JOIN courses c ON sc.course_id = c.id
GROUP BY c.cname;
```

```text
姓名 | 分数
孙八 | NULL
张三 | 88
张三 | 92
李四 | 78
王五 | 85
赵六 | 60
钱七 | 95
（共 7 行）

课程 | 选课人数
C语言 | 2
数据库 | 4
（共 2 行）
```

### `UNION 合并两个查询结果` 上下拼起来（可去重）

**签名** 查询1 UNION 查询2   /   UNION ALL ｜ **返回** 合并后的结果表 ｜ **备注** 列的个数和类型要一致；`UNION` 自动去重（较慢），`UNION ALL` 全留着（更快）

```sql
SELECT name FROM students WHERE score >= 90
UNION
SELECT name FROM students WHERE city = '北京';

SELECT name FROM students WHERE score >= 90
UNION ALL
SELECT name FROM students WHERE city = '北京';
```

```text
name
张三
王五
钱七
（共 3 行）

name
张三
钱七
张三
王五
（共 4 行）
```

> ⚠️ 注意两个结果的行数不同：`UNION` 把重名的合并了，`UNION ALL` 一条不落。

## C8 子查询与条件逻辑

### `子查询（放在 WHERE 里）` 把一次查询的结果当条件

**签名** WHERE 列 IN (SELECT ...)   /   WHERE 列 > (SELECT ...) ｜ **返回** 符合条件的外层结果表 ｜ **备注** 子查询先算，结果再交给外层；`IN` 用于「一列值」，比较运算符用于「一个值」

```sql
SELECT name, score FROM students
WHERE id IN (SELECT student_id FROM scores WHERE score >= 90);

SELECT name, score FROM students
WHERE score > (SELECT AVG(score) FROM students)
ORDER BY score DESC;
```

```text
name | score
张三 | 92
钱七 | 95
（共 2 行）

name | score
钱七 | 95
张三 | 92
王五 | 85
（共 3 行）
```

> ⚠️ 第二句的含义是「谁高于全班平均分」—— 这是子查询最实用的用法之一。

### `EXISTS 子查询` 只判断「有没有」

**签名** WHERE EXISTS (SELECT 1 FROM ... WHERE 关联条件) ｜ **返回** 外层符合条件的行 ｜ **备注** `EXISTS` 只关心子查询有没有结果，不关心内容，所以写 `SELECT 1` 就行

```sql
SELECT name FROM students s
WHERE EXISTS (SELECT 1 FROM scores sc WHERE sc.student_id = s.id);

SELECT name FROM students s
WHERE NOT EXISTS (SELECT 1 FROM scores sc WHERE sc.student_id = s.id);
```

```text
name
张三
李四
王五
赵六
钱七
（共 5 行）

name
孙八
（共 1 行）
```

> ⚠️ 第二句就是「一节课都没选的学生」——`NOT EXISTS` 找「没有对应记录」很好用。

### `CASE WHEN 条件分支` 在 SQL 里写 if-else

**签名** CASE WHEN 条件 THEN 值 ... ELSE 值 END ｜ **返回** 一个值（可起别名当新列） ｜ **备注** 从上往下判断，命中一个就停；`ELSE` 不写时返回 NULL

```sql
SELECT name, score,
       CASE
           WHEN score IS NULL THEN '没成绩'
           WHEN score >= 90 THEN '优秀'
           WHEN score >= 80 THEN '良好'
           WHEN score >= 60 THEN '及格'
           ELSE '不及格'
       END AS 等级
FROM students
ORDER BY score DESC;
```

```text
name | score | 等级
钱七 | 95 | 优秀
张三 | 92 | 优秀
王五 | 85 | 良好
李四 | 78 | 及格
赵六 | 60 | 及格
孙八 | NULL | 没成绩
（共 6 行）
```

> ⚠️ 把 `IS NULL` 放在第一个 `WHEN`，否则 NULL 会一路掉到 `ELSE`（NULL 和任何值比较都不成立）。

### `IFNULL 与 COALESCE` 把 NULL 换成想要的默认值

**签名** IFNULL(值, 默认值)   /   COALESCE(值1, 值2, ...) ｜ **返回** 第一个不为 NULL 的值 ｜ **备注** `IFNULL` 只处理两个参数（MySQL 常用）；`COALESCE` 可以给一串候选值，更通用

```sql
SELECT name,
       IFNULL(score, 0)            AS 分数,
       COALESCE(city, '未填写')     AS 城市,
       COALESCE(score, age, 0)      AS 有值优先
FROM students;
```

```text
name | 分数 | 城市 | 有值优先
张三 | 92 | 北京 | 92
李四 | 78 | 上海 | 78
王五 | 85 | 北京 | 85
赵六 | 60 | 广州 | 60
钱七 | 95 | 上海 | 95
孙八 | 0 | 未填写 | 0
（共 6 行）
```

## C9 更新与删除

### `UPDATE 更新数据` 改已有数据的值

**签名** UPDATE 表 SET 列 = 新值, ... WHERE 条件; ｜ **返回** int（影响的行数） ｜ **备注** **不写 WHERE 就是全表更新**；`SET score = score + 2` 这种「基于原值」的写法很常用

```sql
UPDATE students SET score = score + 2 WHERE city = '北京';
SELECT name, city, score FROM students WHERE city = '北京';
```

```text
（影响 2 行）

name | city | score
张三 | 北京 | 94
王五 | 北京 | 87
（共 2 行）
```

> ⚠️ 先跑一遍 `SELECT ... WHERE 同样的条件`，确认影响的就是你想改的那些行，再改成 `UPDATE`。

### `DELETE 删除数据` 删掉符合条件的行

**签名** DELETE FROM 表 WHERE 条件; ｜ **返回** int（影响的行数） ｜ **备注** **不写 WHERE 会删光全表**；想留后路就先 `START TRANSACTION`，删完确认再 `COMMIT`

```sql
DELETE FROM students WHERE score < 65;
SELECT COUNT(*) AS 剩下人数 FROM students;
SELECT name FROM students ORDER BY id;
```

```text
（影响 1 行）

剩下人数
5
（共 1 行）

name
张三
李四
王五
钱七
孙八
（共 5 行）
```

> ⚠️ 被删行里的 NULL 比较也是不成立的（`score < 65` 对 NULL 行返回 NULL），所以没成绩的孙八没被删掉。

### `TRUNCATE 与 DELETE 的区别` 清空全表更快的方式

**签名** TRUNCATE TABLE 表名; ｜ **返回** — ｜ **备注** `TRUNCATE` 直接重建空表：快、自增 id 归零、**不能回滚**；`DELETE` 逐行删、能回滚

```sql
DELETE FROM students;              -- 逐行删：能回滚、能触发行级触发器
SELECT COUNT(*) AS 剩下人数 FROM students;

TRUNCATE TABLE students;           -- MySQL 专有：整体清空，更快
```

```text
（MySQL 专有语法，本机没有装 MySQL，这条未实跑 —— 以官方文档为准）
```

> ⚠️ `TRUNCATE` 是 MySQL 专有语法（本机未实跑）；它属于 DDL，一执行就会**隐式提交**，所以别指望 `ROLLBACK` 救回来。

## C10 常用函数（字符串 / 数字 / 类型转换）

### `字符串函数` 拼接 / 截取 / 大小写 / 去空格 / 替换

**签名** CONCAT ､ SUBSTRING(s, 起点, 长度) ､ UPPER ､ LOWER ､ TRIM ､ REPLACE ､ LENGTH ｜ **返回** 处理后的字符串（起点从 1 开始！） ｜ **备注** SQL 的字符串下标**从 1 开始**，不是 0；任何参数是 NULL，`CONCAT` 的结果就是 NULL

```sql
SELECT CONCAT(name, ' 来自 ', city) AS 介绍,
       UPPER('abc')                AS 转大写,
       LOWER('ABC')                AS 转小写,
       TRIM('  hi  ')              AS 去首尾空格,
       REPLACE('a-b-c', '-', '/')  AS 替换,
       SUBSTRING('2026-09-24', 1, 4) AS 取年份,
       LENGTH('abc')               AS 字节长度
FROM students
LIMIT 2;
```

```text
介绍 | 转大写 | 转小写 | 去首尾空格 | 替换 | 取年份 | 字节长度
张三 来自 北京 | ABC | abc | hi | a/b/c | 2026 | 3
李四 来自 上海 | ABC | abc | hi | a/b/c | 2026 | 3
（共 2 行）
```

> ⚠️ `LENGTH` 数的是**字节**（中文一个字 3 字节），要数字符数用 `CHAR_LENGTH`。`city` 是 NULL 的行拼出来也是 NULL，需要 `IFNULL(city, '')` 兜一下。

### `日期与时间函数` 取当前时间 / 格式化 / 算天数差

**签名** NOW() ､ CURDATE() ､ DATE_FORMAT(d, 格式) ､ DATEDIFF(d1, d2) ｜ **返回** 日期时间值或字符串 ｜ **备注** `%Y` 四位年、`%m` 月、`%d` 日；`DATEDIFF` 算的是**天数差**

```sql
SELECT NOW()                       AS 现在几点;
SELECT CURDATE()                   AS 今天;
SELECT DATE_FORMAT(NOW(), '%Y-%m-%d %H:%i:%s') AS 格式化;
SELECT DATE_FORMAT(born, '%Y年%m月') AS 出生年月 FROM students WHERE id = 1;
SELECT DATEDIFF('2026-12-31', CURDATE()) AS 距年底还有几天;
SELECT YEAR(NOW()) AS 年, MONTH(NOW()) AS 月, DAY(NOW()) AS 日;
```

```text
（MySQL 专有语法，本机没有装 MySQL，这条未实跑 —— 以官方文档为准）
```

> ⚠️ 这些都是 MySQL 专有函数（本机没装 MySQL 所以未实跑）；注意 MySQL 的日期格式符是 `%i` 表示分钟（不是 `%M`），和别的语言不一样。

### `数学函数` 四舍五入 / 取整 / 绝对值 / 余数

**签名** ROUND(x, n) ､ CEIL(x) ､ FLOOR(x) ､ ABS(x) ､ MOD(x, y) ｜ **返回** 数字 ｜ **备注** `ROUND(x)` 不写位数就是取整（四舍五入）；`MOD(10, 3)` 等于 `10 % 3`

```sql
SELECT ROUND(3.567, 1) AS 保留一位,
       ROUND(3.5)      AS 四舍五入,
       CEIL(2.1)       AS 向上取整,
       FLOOR(2.9)      AS 向下取整,
       ABS(-7)         AS 绝对值,
       MOD(10, 3)      AS 余数;
```

```text
保留一位 | 四舍五入 | 向上取整 | 向下取整 | 绝对值 | 余数
3.6 | 4 | 3 | 2 | 7 | 1
（共 1 行）
```

### `类型转换 CAST` 字符串和数字互转

**签名** CAST(值 AS 类型)   /   CONVERT(值, 类型) ｜ **返回** 转换后的值 ｜ **备注** MySQL 用 `SIGNED` 表示整数、`CHAR` 表示字符串；转换失败会得到 0 或警告，不会报错

```sql
SELECT CAST('123' AS SIGNED) + 1     AS 字符串转数字,
       CAST('3.9' AS SIGNED)         AS 截断成整数,
       CAST(88 AS CHAR)              AS 整数转字符串,
       CONCAT('编号-', CAST(7 AS CHAR)) AS 拼起来;
```

```text
字符串转数字 | 截断成整数 | 整数转字符串 | 拼起来
124 | 3.9 | 88 | 编号-7
（共 1 行）
```

> ⚠️ `CONVERT(值, CHAR)` 是 MySQL 的另一种写法；把字符串当数字用时 SQL 会自动转换，但显式 `CAST` 更清楚（也避免索引失效）。

## C11 索引

### `建索引 CREATE INDEX` 让查询变快

**签名** CREATE INDEX 索引名 ON 表名 (列);   /   CREATE UNIQUE INDEX ... ｜ **返回** — ｜ **备注** 索引像书的目录：`WHERE` / `JOIN` / `ORDER BY` 用到的列建了索引会快很多，代价是插入变慢、占空间

```sql
CREATE INDEX idx_students_city ON students (city);
CREATE UNIQUE INDEX idx_courses_cname ON courses (cname);   -- 唯一索引：该列不许重复
SELECT name, city FROM students WHERE city = '北京';
```

```text
（语句已执行）

（语句已执行）

name | city
张三 | 北京
王五 | 北京
（共 2 行）
```

> ⚠️ 索引名习惯写成 `idx_表_列`；`PRIMARY KEY` 本身就是索引，`UNIQUE` 约束也会自动建唯一索引。

### `复合索引与最左前缀` 多个列一起建索引

**签名** CREATE INDEX 索引名 ON 表名 (列1, 列2); ｜ **返回** — ｜ **备注** 复合索引 `(city, gender)` 能用上 `WHERE city=?` 和 `WHERE city=? AND gender=?`，但**用不上** `WHERE gender=?` —— 这就是「最左前缀」

```sql
CREATE INDEX idx_students_cg ON students (city, gender);
SELECT name, city, gender FROM students WHERE city = '北京' AND gender = '男';
SELECT name, city FROM students WHERE city = '北京';
```

```text
（语句已执行）

name | city | gender
张三 | 北京 | 男
（共 1 行）

name | city
王五 | 北京
张三 | 北京
（共 2 行）
```

> ⚠️ 想知道语句到底走没走索引，在 MySQL 里语句前面加 `EXPLAIN`（`EXPLAIN SELECT ...`）看 `key` 列 —— 这条本机未实跑。

### `查看表结构 / 索引 / 建表语句` 接手一个库先看有什么

**签名** DESCRIBE 表名;   /   SHOW INDEX FROM 表名;   /   SHOW CREATE TABLE 表名; ｜ **返回** 一张描述表结构的结果表 ｜ **备注** `DESC 表名` 是 `DESCRIBE` 的简写；这些是排查问题的第一步

```sql
SHOW TABLES;                          -- 当前库有哪些表
DESCRIBE students;                    -- 表结构（字段、类型、是否可空、键）
SHOW INDEX FROM students;             -- 有哪些索引
SHOW CREATE TABLE students\G          -- 建表语句原文（\G 是竖排显示）
DROP INDEX idx_students_city ON students;   -- 删索引
```

```text
（MySQL 专有语法，本机没有装 MySQL，这条未实跑 —— 以官方文档为准）
```

> ⚠️ 这些 `SHOW` / `DESCRIBE` 是 MySQL 客户端专有命令，本机没装 MySQL 所以**未实跑**；`DROP INDEX ... ON 表名` 是通用的删索引写法。

## C12 事务与视图

### `事务 COMMIT 与 ROLLBACK` 要么全成功、要么全撤销

**签名** START TRANSACTION; 业务语句; COMMIT;   /   ROLLBACK; ｜ **返回** — ｜ **备注** 事务里的改动在 `COMMIT` 之前只有自己看得到；`ROLLBACK` 直接撤销

```sql
START TRANSACTION;
UPDATE students SET score = 0 WHERE id = 1;
SELECT score AS 事务内看到的分 FROM students WHERE id = 1;
ROLLBACK;                                       -- 撤销
SELECT score AS 回滚后的分 FROM students WHERE id = 1;
```

```text
（语句已执行）

（影响 1 行）

事务内看到的分
0
（共 1 行）

（语句已执行）

回滚后的分
92
（共 1 行）
```

> ⚠️ 转账就是典型场景：扣钱和加钱必须在同一个事务里。MySQL 里表的引擎要是 InnoDB 才能用事务（8.0 默认 InnoDB）。

### `CREATE VIEW 视图` 把常用查询存成一个「虚拟表」

**签名** CREATE VIEW 视图名 AS SELECT ...; ｜ **返回** —（之后可以像表一样查询这个视图） ｜ **备注** 视图不存数据，只存 SQL；好处是复杂查询写一次、到处用，还能给不同的人看不同的列

```sql
CREATE VIEW v_good AS
SELECT id, name, score FROM students WHERE score >= 85;

SELECT * FROM v_good ORDER BY score DESC;
SELECT COUNT(*) AS 优秀人数 FROM v_good;
```

```text
（语句已执行）

id | name | score
5 | 钱七 | 95
1 | 张三 | 92
3 | 王五 | 85
（共 3 行）

优秀人数
3
（共 1 行）
```

> ⚠️ 视图里的数据是**实时算的**（底层表一变，视图结果就变）；改视图用 `CREATE OR REPLACE VIEW ...`，删视图用 `DROP VIEW 名字;`。

### `用户与权限` 给程序建一个专用账号

**签名** CREATE USER ... IDENTIFIED BY ...;   /   GRANT 权限 ON 库.表 TO ...; ｜ **返回** — ｜ **备注** **最小权限原则**：程序账号只给需要的权限，不要用 root；权限改完 `FLUSH PRIVILEGES` 生效

```sql
CREATE USER 'app'@'localhost' IDENTIFIED BY '强密码';
GRANT SELECT, INSERT, UPDATE ON school.* TO 'app'@'localhost';
FLUSH PRIVILEGES;
SHOW GRANTS FOR 'app'@'localhost';
```

```text
（MySQL 专有语法，本机没有装 MySQL，这条未实跑 —— 以官方文档为准）
```

> ⚠️ 这些是 MySQL 专有的账号管理语句，本机没装 MySQL 所以**未实跑**；`'app'@'localhost'` 表示只允许本机登录。

---

## 学习建议

1. **先背这一句模板**：`SELECT 要看的列 FROM 表 WHERE 条件 ORDER BY 排序 LIMIT 条数;` —— 日常查询有一大半是它的变形。
2. **SQL 语句以分号结尾**，可以写多行；`-- 两个减号是注释`（`#` 也行，但 `--` 更通用）。
3. **改数据前先 SELECT 一遍同样的 WHERE**：把 `DELETE FROM students WHERE id > 3;` 先写成 `SELECT * FROM students WHERE id > 3;` 看看影响哪些行。
4. **NULL 不是 0 也不是空字符串**：判断只能用 `IS NULL` / `IS NOT NULL`，`= NULL` 永远不成立；聚合函数会自动跳过 NULL。
5. **多表查询先想清楚「连哪两个表、用哪个字段连」**，JOIN 的 `ON` 就是这两个字段相等。
6. **练手环境**：本机装 MySQL（macOS 可 `brew install mysql` 或官网下载 DMG），或用 `phpstudy`、Navicat / DBeaver 这类带图形界面的客户端；命令行客户端用 `mysql -u root -p` 登录后就能逐条试。
