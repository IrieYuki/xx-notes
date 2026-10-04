# Linux 常用指令速查笔记（小白版）

## 怎么用这份文件

这份笔记写给**完全没用过 Linux 的人**。每条命令都配能直接复制的示例，示例下面那段输出是
**真的跑出来的**（在 Ubuntu 24.04 的容器里跑，GNU coreutils 9.4），不是凭记忆写的。

### 先把这几个词记住

| 词 | 白话解释 |
|----|----------|
| 终端（terminal） | 一个能打字、看输出的窗口 |
| shell | 终端里真正读懂你打的字、去执行的程序，最常见的是 `bash` |
| 命令 | 一个程序名（比如 `ls`），后面可以跟**选项**（`-l`、`--all`）和**参数**（文件名、目录） |
| 提示符（prompt） | 行首那串东西，比如 `kali@kali:~$` —— `$` 后面才是你打字的地方。笔记里的示例**不写提示符**，直接给能复制的命令 |
| 路径 | `/` 是根目录（整个文件系统的顶）、`~` 是你的家目录（比如 `/home/kali`）、`.` 是当前目录、`..` 是上一级目录 |
| 标准输出 / 标准错误 | 命令正常打印的内容 / 报错信息。屏幕上都是字，但它们是两条不同的「管子」（A6 讲怎么分开接） |
| root（根用户） | 权限最大的用户，能改系统里任何东西，破坏力也最大。平时用 `sudo` 临时借它的权限（A7） |

两个新手最常被绊倒的地方：

1. **很多命令成功时什么都不打印** —— Linux 的老规矩是「没有消息就是好消息」。`rm a.txt` 没有输出 ≠ 没执行。
2. **命令和文件名都区分大小写**：`ls` 能跑，`LS` 会说 `command not found`。

### 示例环境（先跑这块）

下面这块在你自己机器上跑也行：它会在家目录下造一个 `linux-lab` 目录，后面每条示例都在这个目录里跑，
这样你看到的文件名、大小和笔记里一模一样。

```bash
# [示例环境] 造一个练习目录，后面每条示例都在这个目录里跑
rm -rf ~/linux-lab && mkdir -p ~/linux-lab && cd ~/linux-lab
mkdir -p dir1 dir2
printf 'hello linux\nsecond line\nthird line\n' > hello.txt
printf 'apple 3\nbanana 5\ncherry 7\n' > fruit.txt
printf 'name,age\ntom,18\namy,20\n' > data.csv
printf 'login ok\nlogin failed\nlogin ok\n' > notes.txt
printf '#!/bin/bash\necho "hi from script"\n' > run.sh
: > empty.txt
chmod +x run.sh
touch -t 202601010900 hello.txt fruit.txt data.csv notes.txt run.sh empty.txt dir1 dir2
```

```text
（运行完屏幕上没有任何输出 —— 没消息就是好消息，目录已经建好了）
```

示例是在容器里**以 root 用户**跑的，所以 `ls -l` 的属主列显示 `root root`；
你在自己的 Kali 上用普通用户跑，那一列会变成你的用户名，其余列一样。

### 怎么查

- 最前面那张**索引表**既是目录也是速查表：一行一条命令，点「用法」直接跳到正文那一条。
- 正文每条格式一样：
  - **解析**：先一句话说这条命令是干嘛的，再用表格逐个解释**选项和参数**的作用，最后写会得到什么
  - **操作**：能直接复制的示例，下面紧跟真的运行结果；一个选项一组，组之间空行隔开
  - `> ⚠️ 提醒`：讲坑和易错点，尤其是带删除、带权限、带 `rm` 的那些，值得多看两眼
- 同一命令的多个选项**合并成一条**（比如 `ls` 的 -a -l -h -t 都在 `ls` 那一条里），
  一个命令一行索引，不再占十几行。

### 章节顺序

A1 终端与命令 → A2 目录与路径 → A3 文件操作 → A4 看文件内容 → A5 查找与搜索 →
A6 管道、重定向与文本处理 → A7 权限与用户 → A8 进程与作业 → A9 网络与远程 →
A10 压缩与打包 → A11 系统信息与软件包

顺序就是上手顺序：A1 到 A4 会了，日常在服务器上活下来没问题；A5、A6 开始是效率工具，
也是后面做安全、看日志的基础。

---

## 索引 · 速查表

| 分类 | 用法（点击跳转） | 一句话作用 |
|------|------------------|-----------|
| A1 终端与命令 | [`echo`](#echo-打印一行字最简单的命令) | 打印一行字（最简单的命令） |
| A1 终端与命令 | [`man`](#man-查命令用法看帮助看手册看版本) | 查命令用法：看帮助、看手册、看版本 |
| A2 目录与路径 | [`pwd`](#pwd-我现在在哪个目录) | 我现在在哪个目录 |
| A2 目录与路径 | [`ls`](#ls-看这个目录里有什么) | 看这个目录里有什么 |
| A2 目录与路径 | [`cd`](#cd-进到某个目录里和三个跳回去的写法) | 进到某个目录里（和三个跳回去的写法） |
| A2 目录与路径 | [`mkdir`](#mkdir-新建目录) | 新建目录 |
| A2 目录与路径 | [`tree`](#tree-树形看目录结构一眼看懂层级) | 树形看目录结构（一眼看懂层级） |
| A3 文件操作 | [`touch`](#touch-建一个空文件或只更新它的时间) | 建一个空文件（或只更新它的时间） |
| A3 文件操作 | [`cp`](#cp-复制文件-r-复制整个目录) | 复制文件（-r 复制整个目录） |
| A3 文件操作 | [`mv`](#mv-移动文件或给文件改名) | 移动文件或给文件改名 |
| A3 文件操作 | [`rm`](#rm-删文件-r-删目录危险命令) | 删文件（-r 删目录，危险命令） |
| A3 文件操作 | [`ln`](#ln-建软链接快捷方式) | 建软链接（快捷方式） |
| A3 文件操作 | [`stat`](#stat-看文件的各种详细信息) | 看文件的各种详细信息 |
| A4 看文件内容 | [`cat`](#cat-把文件内容整个打印出来) | 把文件内容整个打印出来 |
| A4 看文件内容 | [`less`](#less-分页看大文件可以上下翻搜索) | 分页看大文件（可以上下翻、搜索） |
| A4 看文件内容 | [`head`](#head-只看开头几行) | 只看开头几行 |
| A4 看文件内容 | [`tail`](#tail-只看结尾几行盯日志常用) | 只看结尾几行（盯日志常用） |
| A4 看文件内容 | [`wc`](#wc-数行数单词数字节数) | 数行数、单词数、字节数 |
| A4 看文件内容 | [`nl`](#nl-带行号打印方便讨论第几行) | 带行号打印（方便讨论「第几行」） |
| A4 看文件内容 | [`diff`](#diff-比较两个文件哪里不一样) | 比较两个文件哪里不一样 |
| A5 查找与搜索 | [`find`](#find-按名字按类型找文件会钻进所有子目录) | 按名字、按类型找文件（会钻进所有子目录） |
| A5 查找与搜索 | [`grep`](#grep-在文件里找包含某个词的行) | 在文件里找包含某个词的行 |
| A5 查找与搜索 | [`which`](#which-这个命令到底是哪个程序) | 这个命令到底是哪个程序 |
| A6 管道、重定向与文本处理 | [`命令>文件`](#命令文件-把输出写进文件覆盖) | 把输出写进文件（覆盖） |
| A6 管道、重定向与文本处理 | [`命令>>文件`](#命令文件-把输出追加到文件末尾) | 把输出追加到文件末尾 |
| A6 管道、重定向与文本处理 | [`命令2>文件`](#命令2文件-只把报错信息接进文件) | 只把报错信息接进文件 |
| A6 管道、重定向与文本处理 | [`命令>文件2>&1`](#命令文件21-正常输出和报错都接进同一个文件) | 正常输出和报错都接进同一个文件 |
| A6 管道、重定向与文本处理 | [`命令1｜命令2`](#命令1命令2-管道把上一条的输出当输入) | 管道：把上一条的输出当输入 |
| A6 管道、重定向与文本处理 | [`tee`](#tee-又打印到屏幕又存进文件) | 又打印到屏幕、又存进文件 |
| A6 管道、重定向与文本处理 | [`sort`](#sort-排序) | 排序 |
| A6 管道、重定向与文本处理 | [`uniq`](#uniq-数一数每行重复出现了几次) | 数一数每行重复出现了几次 |
| A6 管道、重定向与文本处理 | [`cut`](#cut-按分隔符取某一列) | 按分隔符取某一列 |
| A6 管道、重定向与文本处理 | [`sed 's/旧/新/'`](#sed-s旧新-替换文本默认只改输出不改文件) | 替换文本（默认只改输出，不改文件） |
| A6 管道、重定向与文本处理 | [`awk '{print $2}'`](#awk-print-2-取列做简单计算文本处理万能工具) | 取列、做简单计算（文本处理万能工具） |
| A6 管道、重定向与文本处理 | [`xargs`](#xargs-把上一条的输出变成下一条的参数) | 把上一条的输出变成下一条的参数 |
| A7 权限与用户 | [`chmod`](#chmod-改文件权限符号写法和数字写法) | 改文件权限（符号写法和数字写法） |
| A7 权限与用户 | [`chown、chgrp`](#chownchgrp-改文件的属主属组) | 改文件的属主、属组 |
| A7 权限与用户 | [`umask`](#umask-看或改新建文件的默认权限) | 看或改新建文件的默认权限 |
| A7 权限与用户 | [`whoami、id`](#whoamiid-我是谁我的-uid-和组) | 我是谁、我的 uid 和组 |
| A7 权限与用户 | [`sudo`](#sudo-用-root-权限跑一条命令) | 用 root 权限跑一条命令 |
| A8 进程与作业 | [`ps`](#ps-看进程这个终端的或整台机器的) | 看进程（这个终端的或整台机器的） |
| A8 进程与作业 | [`pgrep`](#pgrep-按名字查进程的-pid) | 按名字查进程的 PID |
| A8 进程与作业 | [`top`](#top-动态看谁在吃-cpu内存) | 动态看谁在吃 CPU、内存 |
| A8 进程与作业 | [`kill`](#kill-结束一个进程) | 结束一个进程 |
| A8 进程与作业 | [`sleep`](#sleep-等一会儿暂停-n-秒) | 等一会儿（暂停 N 秒） |
| A8 进程与作业 | [`&、jobs、fg`](#jobsfg-放到后台跑把后台作业拉回来) | 放到后台跑、把后台作业拉回来 |
| A8 进程与作业 | [`nohup`](#nohup-关掉终端也别停后台长任务) | 关掉终端也别停（后台长任务） |
| A9 网络与远程 | [`ip`](#ip-看网卡和-ip-地址) | 看网卡和 IP 地址 |
| A9 网络与远程 | [`ss`](#ss-看谁在监听端口本机开了哪些服务) | 看谁在监听端口（本机开了哪些服务） |
| A9 网络与远程 | [`ping`](#ping-测通不通发-icmp-包) | 测「通不通」（发 ICMP 包） |
| A9 网络与远程 | [`curl`](#curl-抓网页调接口发-http-请求) | 抓网页、调接口（发 HTTP 请求） |
| A9 网络与远程 | [`wget`](#wget-下载文件到当前目录) | 下载文件到当前目录 |
| A9 网络与远程 | [`nc`](#nc-测某个端口开没开) | 测某个端口开没开 |
| A9 网络与远程 | [`ssh`](#ssh-登录远程主机) | 登录远程主机 |
| A9 网络与远程 | [`scp`](#scp-在本地和远程之间复制文件) | 在本地和远程之间复制文件 |
| A10 压缩与打包 | [`tar`](#tar-打包压缩-czf-打包-tzf-看包-xzf-解包) | 打包压缩（-czf 打包、-tzf 看包、-xzf 解包） |
| A10 压缩与打包 | [`gzip、gunzip`](#gzipgunzip-压缩单个文件不是打包目录) | 压缩单个文件（不是打包目录） |
| A10 压缩与打包 | [`zip、unzip`](#zipunzip-跨平台压缩包给-windows-用) | 跨平台压缩包（给 Windows 用） |
| A11 系统信息与软件包 | [`cat /etc/os-release`](#cat-etcos-release-我在什么系统上发行版与版本) | 我在什么系统上（发行版与版本） |
| A11 系统信息与软件包 | [`uname`](#uname-看内核版本和机器架构) | 看内核版本和机器架构 |
| A11 系统信息与软件包 | [`df`](#df-看磁盘还剩多少空间) | 看磁盘还剩多少空间 |
| A11 系统信息与软件包 | [`du`](#du-看某个目录占了多少空间) | 看某个目录占了多少空间 |
| A11 系统信息与软件包 | [`free`](#free-看内存和-swap-使用情况) | 看内存和 swap 使用情况 |
| A11 系统信息与软件包 | [`echo $PATH`](#echo-path-命令是从哪些目录里找的path-环境变量) | 命令是从哪些目录里找的（PATH 环境变量） |
| A11 系统信息与软件包 | [`export、alias`](#exportalias-临时设环境变量造命令别名) | 临时设环境变量、造命令别名 |
| A11 系统信息与软件包 | [`apt`](#apt-装卸软件debianubuntukali-系) | 装、卸软件（Debian、Ubuntu、Kali 系） |

---

## A1 终端与命令

### `echo` 打印一行字（最简单的命令）

**解析**　把字原样打印到屏幕（标准输出）。用来试终端是否正常、在脚本里输出提示；`echo $变量` 能直接看变量的值。（记：echo = 回声，你说什么它就回什么）

| 参数 | 默认值 | 作用 |
|------|--------|------|
| 内容 | 必填 | 要打印的字，可以多个，用空格隔开；不含空格时引号可以省略 |
| -n | 不写 | 结尾不换行 |
| -e | 不写 | 把 \n、\t 这类转义符解释出来（不加就原样打印） |

返回：屏幕上出现你写的内容

**操作**

```bash
echo hello linux
```
```text
hello linux
```

```bash
echo "引号里的    多个空格也会保留"
```
```text
引号里的    多个空格也会保留
```

```bash
echo $HOME
```
```text
/root
```

> ⚠️ 不加引号时多个空格会被压成一个；`$HOME` 这种 `$` 开头的会被**先替换成变量的值**再打印（这叫变量展开）。

### `man` 查命令用法：看帮助、看手册、看版本

**解析**　忘了一个命令怎么用，有三条路：命令自带的 --help（快）、man 手册（全）、--version（看版本）。（记：man = manual，手册）

| 参数 | 默认值 | 作用 |
|------|--------|------|
| 命令 --help | — | 打印用法和所有选项；少数命令只认 -h，shell 内建命令（cd、echo）没有 |
| man 命令 | — | 完整手册：空格翻页、/关键词 搜索、q 退出 |
| 命令 --version | — | 打印版本号；出错求助时先贴版本，不同版本行为可能不同 |

返回：对应命令的说明文字

**操作**

```bash
ls --help | head -n 5
```
```text
Usage: ls [OPTION]... [FILE]...
List information about the FILEs (the current directory by default).
Sort entries alphabetically if none of -cftuvSUX nor --sort is specified.

Mandatory arguments to long options are mandatory for short options too.
```

```bash
man ls
```
```text
（未实跑：man 需要交互式终端，校验容器里也没装 man-db。先记住三个键：空格翻页、`/` 搜索、`q` 退出）
```

```bash
ls --version | head -n 1
```
```text
ls (GNU coreutils) 9.4
```

> ⚠️ 少数命令只认 `-h`；`echo`、`cd` 这种是 shell 内建命令，没有 `--help`。两种都试一下。；多数 Linux 命令来自 GNU 项目，macOS 用的是 BSD 版：**同名命令、选项和行为可能不同**（本笔记会在 ⚠️ 里点出来）。

## A2 目录与路径

### `pwd` 我现在在哪个目录

**解析**　打印当前目录的完整路径（以 / 开头的是绝对路径）。迷路时的第一条命令。（记：pwd = print working directory，打印当前工作目录）

返回：当前目录的绝对路径

**操作**

```bash
pwd
```
```text
/root/linux-lab
```

```bash
cd dir1 && pwd
```
```text
/root/linux-lab/dir1
```

> ⚠️ 你机器上显示的是你自己的家目录，比如 `/home/kali/linux-lab`；示例里是容器里的 `/root/linux-lab`。

### `ls` 看这个目录里有什么

**解析**　列出目录里的文件和子目录。最常用的命令，不修改任何东西。（记：ls = list，列出）

| 参数 | 默认值 | 作用 |
|------|--------|------|
| （不写选项） | — | 只显示文件名（不含 . 开头的隐藏文件），按字母序排成一列 |
| -a | — | 连隐藏文件一起列（含 . 和 .. 这两个特殊条目） |
| -l | — | 长格式：一行一个，7 列 = 权限、硬链接数、属主、属组、大小、修改时间、名字 |
| -h | — | 配合 -l：大小变成 4.0K 这种好读写法 |
| -t | — | 按修改时间排，最新的在最上面（-ltr 反过来） |
| 目录 | 可选 | 看哪个目录；不写就是当前目录 |

返回：目录内容的列表

**操作**

```bash
ls
```
```text
data.csv
dir1
dir2
empty.txt
fruit.txt
hello.txt
notes.txt
run.sh
```

```bash
ls dir1
```

```bash
touch .secret.txt && ls
```
```text
data.csv
dir1
dir2
empty.txt
fruit.txt
hello.txt
notes.txt
run.sh
```

```bash
touch .secret.txt && ls -a
```
```text
.
..
.secret.txt
data.csv
dir1
dir2
empty.txt
fruit.txt
hello.txt
notes.txt
run.sh
```

```bash
ls -l
```
```text
total 28
-rw-r--r-- 1 root root   23 Jan  1  2026 data.csv
drwxr-xr-x 2 root root 4096 Jan  1  2026 dir1
drwxr-xr-x 2 root root 4096 Jan  1  2026 dir2
-rw-r--r-- 1 root root    0 Jan  1  2026 empty.txt
-rw-r--r-- 1 root root   26 Jan  1  2026 fruit.txt
-rw-r--r-- 1 root root   35 Jan  1  2026 hello.txt
-rw-r--r-- 1 root root   31 Jan  1  2026 notes.txt
-rwxr-xr-x 1 root root   34 Jan  1  2026 run.sh
```

```bash
ls -lh
```
```text
total 28K
-rw-r--r-- 1 root root   23 Jan  1  2026 data.csv
drwxr-xr-x 2 root root 4.0K Jan  1  2026 dir1
drwxr-xr-x 2 root root 4.0K Jan  1  2026 dir2
-rw-r--r-- 1 root root    0 Jan  1  2026 empty.txt
-rw-r--r-- 1 root root   26 Jan  1  2026 fruit.txt
-rw-r--r-- 1 root root   35 Jan  1  2026 hello.txt
-rw-r--r-- 1 root root   31 Jan  1  2026 notes.txt
-rwxr-xr-x 1 root root   34 Jan  1  2026 run.sh
```

```bash
touch -t 202602020900 newer.txt && ls -lt
```
```text
total 28
-rw-r--r-- 1 root root    0 Feb  2  2026 newer.txt
-rw-r--r-- 1 root root   23 Jan  1  2026 data.csv
drwxr-xr-x 2 root root 4096 Jan  1  2026 dir1
drwxr-xr-x 2 root root 4096 Jan  1  2026 dir2
-rw-r--r-- 1 root root    0 Jan  1  2026 empty.txt
-rw-r--r-- 1 root root   26 Jan  1  2026 fruit.txt
-rw-r--r-- 1 root root   35 Jan  1  2026 hello.txt
-rw-r--r-- 1 root root   31 Jan  1  2026 notes.txt
-rwxr-xr-x 1 root root   34 Jan  1  2026 run.sh
```

> ⚠️ 目录为空时 `ls` **什么都不打印**，这不代表出错（`dir1` 就是空的）。；别被输出里的 `.` 和 `..` 弄晕：每个目录里都有这两个特殊条目，它们就是「当前目录」和「上一级目录」。；时间列是**修改时间**；示例里被固定成 2026-01-01（为了让输出稳定、可校验），你机器上是真实时间。；选项可以叠着写：`-lh` 就是 `-l -h`（Linux 命令的通用习惯，如 `tar -xzf`、`ls -la`）。；修改时间完全相同时，`ls` 会按名字排序，所以输出是稳定的。

### `cd` 进到某个目录里（和三个跳回去的写法）

**解析**　切换当前目录。成功时什么都不打印；`..` 上一级、`~` 家目录、`-` 回上一个待过的目录。（记：cd = change directory，切换目录）

| 参数 | 默认值 | 作用 |
|------|--------|------|
| 目录 | 必填 | 要去的目录；不存在会报 No such file or directory，写成了文件报 Not a directory |
| .. | — | 上一级目录 |
| ~ | — | 家目录 |
| - | — | 回上一个待过的目录（只有这个形式会打印目标路径） |

返回：没有输出，但「当前位置」变了

**操作**

```bash
pwd
```
```text
/root/linux-lab
```

```bash
cd dir1 && pwd
```
```text
/root/linux-lab/dir1
```

```bash
cd /etc && pwd
```
```text
/etc
```

```bash
cd dir1 && cd .. && pwd
```
```text
/root/linux-lab
```

```bash
cd /etc && cd -
```
```text
/root/linux-lab
```

```bash
cd && pwd
```
```text
/root
```

> ⚠️ `cd` 写错的两种报错：目录不存在 → `No such file or directory`；写成了文件 → `Not a directory`。；只有 `cd -` 会打印路径，其他形式都是安静的 —— 在脚本里要注意这一点。

### `mkdir` 新建目录

**解析**　创建目录；-p 可以把不存在的父目录一起建出来。（记：mkdir = make directory，创建目录）

| 参数 | 默认值 | 作用 |
|------|--------|------|
| 目录名 | 必填 | 要建的目录 |
| -p | 不写 | 父目录不存在时一起建（mkdir -p a/b/c）；不加 -p 父目录不存在会报错 |

返回：没有输出，目录直接出现

**操作**

```bash
mkdir newdir && ls -1d newdir
```
```text
newdir
```

```bash
mkdir -p a/b/c && find . -type d | sort
```
```text
.
./a
./a/b
./a/b/c
./dir1
./dir2
```

> ⚠️ 目录已存在时会报 `File exists`；这不是错，通常忽略即可。

### `tree` 树形看目录结构（一眼看懂层级）

**解析**　把目录画成一棵树，最后一行给出目录数和文件数。项目层级多时特别好用。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| 目录 | 可选 | 看哪个目录；不写是当前目录 |
| -L 2 | 不写 | 只看前两层 |

返回：画成树的目录结构

**操作**

```bash
tree
```
```text
.
|-- data.csv
|-- dir1
|-- dir2
|-- empty.txt
|-- fruit.txt
|-- hello.txt
|-- notes.txt
`-- run.sh

2 directories, 6 files
```

> ⚠️ 输出里的 `│ ├ └` 只是画线的字符，没有别的含义。

## A3 文件操作

### `touch` 建一个空文件（或只更新它的时间）

**解析**　文件不存在就创建一个 0 字节的空文件；已存在就把修改时间刷成现在。（记：touch = 碰一下——把文件「碰」出来，或更新时间）

| 参数 | 默认值 | 作用 |
|------|--------|------|
| 文件名 | 必填 | 要建/要刷的文件，可以写多个；支持通配符（touch *.txt） |

返回：没有输出；文件出现或时间更新

**操作**

```bash
touch newfile.txt && ls -1 *.txt
```
```text
empty.txt
fruit.txt
hello.txt
newfile.txt
notes.txt
```

> ⚠️ 它不检查文件内容，也不报「文件已存在」；改的是时间戳，不是内容。

### `cp` 复制文件（-r 复制整个目录）

**解析**　复制文件；复制目录必须加 -r。目标已存在会直接覆盖。（记：cp = copy，复制）

| 参数 | 默认值 | 作用 |
|------|--------|------|
| 源 | 必填 | 要复制的文件或目录 |
| 目标 | 必填 | 复制到哪；已存在会静默覆盖 |
| -r | 必填（复制目录时） | 递归复制整个目录；不加 -r 复制目录会报 omitting directory |
| -i | 不写 | 覆盖前问一次 |
| -a | 不写 | 连权限、时间一起保留（归档式复制） |

返回：没有输出；目标处出现副本

**操作**

```bash
cp hello.txt copy.txt && ls -1 *.txt
```
```text
copy.txt
empty.txt
fruit.txt
hello.txt
notes.txt
```

```bash
cp hello.txt copy.txt && cat copy.txt
```
```text
hello linux
second line
third line
```

```bash
cp -r dir1 dir1-copy && find . -maxdepth 1 -type d | sort
```
```text
.
./dir1
./dir1-copy
./dir2
```

> ⚠️ 不加 `-r` 复制目录会报 `omitting directory 'dir1'`（它默认不递归）。；`cp -r 源 目标`：目标不存在就新建，目标已存在会把源目录**塞进目标里面**（变成 `目标/源/...`），这点很容易搞错。

### `mv` 移动文件或给文件改名

**解析**　同一个目录里是改名，跨目录是移动；目标已存在会静默覆盖。（记：mv = move，移动）

| 参数 | 默认值 | 作用 |
|------|--------|------|
| 源 | 必填 | 要移动/改名的文件 |
| 目标 | 必填 | 新位置或新名字 |
| -i | 不写 | 覆盖前问一次 |
| -n | 不写 | 不覆盖已存在的文件 |

返回：没有输出

**操作**

```bash
mv empty.txt renamed.txt && ls -1 *.txt
```
```text
fruit.txt
hello.txt
notes.txt
renamed.txt
```

> ⚠️ `mv` 覆盖目标文件时**不提示、不备份**（要提示加 `-i`，要防覆盖加 `-n`）—— 这是最常见的误伤之一。

### `rm` 删文件（-r 删目录，危险命令）

**解析**　删除文件；删目录要加 -r。没有回收站，删了就是删了。（记：rm = remove，移除）

| 参数 | 默认值 | 作用 |
|------|--------|------|
| 文件名 | 必填 | 要删的文件，可以写多个 |
| -r | 必填（删目录时） | 递归删除目录及里面所有东西 |
| -f | 不写 | 强制：不提示，不存在也不报错 |
| -i | 不写 | 删之前问一次 |

返回：没有输出（成功时）

**操作**

```bash
rm empty.txt && ls -1 *.txt
```
```text
fruit.txt
hello.txt
notes.txt
```

```bash
cp -r dir1 dir1-copy && rm -r dir1-copy && find . -maxdepth 1 -type d | sort
```
```text
.
./dir1
./dir2
```

> ⚠️ **没有回收站**：删了就是删了。养成习惯：删之前先 `ls` 看一眼要删的东西。；`rm -rf /`、`rm -rf ~` 能直接毁掉系统，**永远不要**复制来路不明的这种命令。脚本里删变量路径要加保护：`rm -rf "${DIR:?}"/`，变量为空时 `${DIR:?}` 会直接报错退出，避免变成 `rm -rf /`。

### `ln` 建软链接（快捷方式）

**解析**　给文件建一个「快捷方式」：链接只是个指针，改链接内容就是改原文件。（记：ln = link，链接）

| 参数 | 默认值 | 作用 |
|------|--------|------|
| -s | 必填 | 建软链接；不加 -s 建的是硬链接（另一种东西，日常别碰） |
| 真实文件 | 必填 | 指向的原文件 |
| 链接名 | 必填 | 快捷方式的名字 |

返回：没有输出；多出一个链接

**操作**

```bash
ln -s hello.txt link.txt && stat -c '%N' link.txt
```
```text
'link.txt' -> 'hello.txt'
```

```bash
ln -s hello.txt link.txt && cat link.txt
```
```text
hello linux
second line
third line
```

```bash
ln -s hello.txt link.txt && readlink link.txt
```
```text
hello.txt
```

> ⚠️ 原文件被删掉后链接会「断」：`cat` 会报 `No such file or directory`，但链接本身还在（`ls -l` 里会显示成红色）。

### `stat` 看文件的各种详细信息

**解析**　看文件的元数据：权限、大小、三个时间戳。想知道权限的数字写法（644）用它。（记：stat = status，状态）

| 参数 | 默认值 | 作用 |
|------|--------|------|
| 文件 | 必填 | 要看哪个文件 |
| -c '格式' | 不写 | 自定义输出：%a 权限数字、%s 大小、%U 属主、%y 修改时间 |

返回：一大段元数据

**操作**

```bash
stat -c '%a %U %G %s %n' hello.txt
```
```text
644 root root 35 hello.txt
```

> ⚠️ `-c` 是 GNU 的写法；macOS 的 `stat` 要用 `-f`，格式字母也不同（`%Sp %Su %z`）。

## A4 看文件内容

### `cat` 把文件内容整个打印出来

**解析**　按顺序打印文件内容；给多个文件就前后拼起来打印。只适合小文本文件。（记：cat = concatenate，把多个文件连接起来打印）

| 参数 | 默认值 | 作用 |
|------|--------|------|
| 文件 | 必填 | 要看的文件，可以写多个 |
| -n | 不写 | 每行前面加行号 |

返回：文件内容原样出现在屏幕

**操作**

```bash
cat hello.txt
```
```text
hello linux
second line
third line
```

```bash
cat hello.txt notes.txt
```
```text
hello linux
second line
third line
login ok
login failed
login ok
```

> ⚠️ `cat` 只能看**文本**文件，看二进制（图片、可执行文件）会刷出乱七八糟的乱码，还可能弄坏终端（这时敲 `reset`）。

### `less` 分页看大文件（可以上下翻、搜索）

**解析**　进入分页阅读器看大文件：不一次读进内存，多大都能开。（记：less 是「more 的加强版」——more 是更早的分页器，「less is more」是个梗）

| 参数 | 默认值 | 作用 |
|------|--------|------|
| 文件 | 必填 | 要看的文件 |
| （阅读器内按键） | — | 空格/PgDn 下翻、b 上翻、/词 搜索、n 下一个、q 退出 |

返回：分页的文件内容

**操作**

```bash
less hello.txt
```
```text
（未实跑：less 需要交互式终端。三个必记键：空格翻页、`/` 搜索、`q` 退出）
```

### `head` 只看开头几行

**解析**　打印文件前 N 行（默认前 10 行）。看文件格式、看表头用。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| -n 行数 | 10 | 打印前几行 |
| -c 字节数 | 不写 | 打印前几个字节 |
| 文件 | 必填 | 要看哪个文件 |

返回：文件开头的几行

**操作**

```bash
head -n 2 notes.txt
```
```text
login ok
login failed
```

> ⚠️ `head -n -2 f` 是 GNU 的玩法（除最后两行都打印），换到 macOS 的 BSD `head` 就用不了。

### `tail` 只看结尾几行（盯日志常用）

**解析**　打印文件最后 N 行；加 -f 就一直盯着文件，新写入的行实时显示。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| -n 行数 | 10 | 打印最后几行 |
| -f | 不写 | 持续盯文件，新内容实时滚出来（Ctrl+C 停） |
| 文件 | 必填 | 要看哪个文件 |

返回：文件结尾的几行

**操作**

```bash
tail -n 2 notes.txt
```
```text
login failed
login ok
```

> ⚠️ `tail -f` 会**一直挂着不退出**，这是正常现象，用 `Ctrl+C` 停；想边看边过滤就 `tail -f 日志 | grep 关键词`（A6）。

### `wc` 数行数、单词数、字节数

**解析**　统计文件有多少行、多少单词、多少字节。wc -l 是数「有几条」的日常工具。（记：wc = word count，统计字数）

| 参数 | 默认值 | 作用 |
|------|--------|------|
| -l | 不写 | 只要行数（最常用） |
| -w | 不写 | 只要单词数 |
| -c | 不写 | 只要字节数 |
| 文件 | 可选 | 要统计的文件；不写就从管道读 |

返回：数字（默认顺序：行数 单词数 字节数 文件名）

**操作**

```bash
wc -l notes.txt
```
```text
3 notes.txt
```

```bash
wc -l -w -c hello.txt
```
```text
 3  6 35 hello.txt
```

```bash
ls | wc -l
```
```text
8
```

> ⚠️ 最后一行没有换行符时 `wc -l` 会**少算一行**（它数的是换行符个数）：`printf 'a' | wc -l` 得 0。

### `nl` 带行号打印（方便讨论「第几行」）

**解析**　每行前面加上行号再打印，和报错信息里的「第几行」对位置用。（记：nl = number lines，给行编号）

| 参数 | 默认值 | 作用 |
|------|--------|------|
| 文件 | 必填 | 要看哪个文件 |
| -ba | 不写 | 空行也编号（默认空行不编号；cat -n 会给空行编号） |

返回：带行号的内容

**操作**

```bash
nl hello.txt
```
```text
     1	hello linux
     2	second line
     3	third line
```

```bash
cat -n hello.txt
```
```text
     1	hello linux
     2	second line
     3	third line
```

> ⚠️ 行号是**打印出来的装饰**，文件内容里并没有；不要拿行号去写进文件。

### `diff` 比较两个文件哪里不一样

**解析**　找出两个文件的差异：`<` 是左边文件的行、`>` 是右边文件的行。完全相同则什么都不打印。（记：diff = difference，差异）

| 参数 | 默认值 | 作用 |
|------|--------|------|
| 文件1 | 必填 | 旧文件（左边） |
| 文件2 | 必填 | 新文件（右边） |
| -q | 不写 | 只回答「有没有差异」 |
| -r | 不写 | 比较两个目录 |

返回：差异清单（无差异时无输出）

**操作**

```bash
cp hello.txt same.txt && diff hello.txt same.txt
```

```bash
cp hello.txt same.txt && printf 'hello linux\nsecond line\nCHANGED\n' > other.txt && diff hello.txt other.txt
```
```text
3c3
< third line
---
> CHANGED
```

> ⚠️ `diff` 有差异时**退出码是 1**（相同是 0），在脚本里常写 `diff a b || echo 有差异`；想只看「有没有差异」用 `diff -q`。

## A5 查找与搜索

### `find` 按名字、按类型找文件（会钻进所有子目录）

**解析**　从某个目录出发，把所有子目录翻一遍，找出符合条件的文件。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| 起点目录 | 必填 | 从哪开始找（. 表示当前目录） |
| -name '模式' | 二选一 | 按名字找；* 任意多个字符、? 一个字符；模式必须加引号 |
| -type f/d/l | 二选一 | 按类型找：f 普通文件、d 目录、l 软链接 |
| -size +1M | 可选 | 按大小找 |
| -mtime -1 | 可选 | 按修改时间找（1 天内改过） |
| -maxdepth 1 | 可选 | 只看本层，不钻进子目录（要写在其他条件之前） |

返回：所有匹配的文件路径（没找到就无输出）

**操作**

```bash
find . -name '*.csv'
```
```text
./data.csv
```

```bash
find . -type d | sort
```
```text
.
./dir1
./dir2
```

```bash
find . -type f -name '*.csv'
```
```text
./data.csv
```

> ⚠️ 模式**必须加引号**：写成 `find . -name *.txt`，shell 会先把 `*.txt` 展开成一堆文件名再交给 find，直接报 `find: paths must precede expression`。；`-maxdepth` 要写在**其他条件之前**，放后面 GNU 会警告（位置写错是 find 最常见的坑）。

### `grep` 在文件里找包含某个词的行

**解析**　最常用的文本搜索：打印匹配到的整行；一行都没有就什么都不打印。（记：grep = g/re/p，来自 ed 编辑器的「全局正则打印」）

| 参数 | 默认值 | 作用 |
|------|--------|------|
| '模式' | 必填 | 要找的词或正则（^词 行首、词$ 行尾） |
| 文件 | 必填 | 在哪找，可以写多个 |
| -n | 不写 | 每行前面加它在文件里的行号 |
| -i | 不写 | 不区分大小写 |
| -c | 不写 | 只打印匹配的行数 |
| -v | 不写 | 反过来：打印不匹配的行 |
| -r | 不写 | 递归搜整个目录（输出形如 路径:行号:内容） |
| -l | 不写 | 只列文件名不列内容 |

返回：匹配到的整行

**操作**

```bash
grep ok notes.txt
```
```text
login ok
login ok
```

```bash
grep -n failed notes.txt
```
```text
2:login failed
```

```bash
grep -i LOGIN notes.txt
```
```text
login ok
login failed
login ok
```

```bash
grep -c ok notes.txt
```
```text
2
```

```bash
grep -v ok notes.txt
```
```text
login failed
```

```bash
grep -r login .
```
```text
./notes.txt:login ok
./notes.txt:login failed
./notes.txt:login ok
```

> ⚠️ 退出码有意义：0 = 找到了、1 = 一行都没匹配、2 = 出错（比如文件不存在）。脚本里用 `grep -q 词 文件` 只看成败、不要输出。；递归会连 `.git`、`node_modules`、日志一起搜，又慢又乱：用 `--include='*.py'` 限定文件、`--exclude-dir=.git` 排除目录。

### `which` 这个命令到底是哪个程序

**解析**　查出命令对应哪个可执行文件，或它是内建命令/别名。命令「找不到」时用它排查。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| 命令 | 必填 | 要查的命令名 |

返回：程序路径（which 对内建命令会查无此人，command -v 更标准）

**操作**

```bash
which ls
```
```text
/usr/bin/ls
```

```bash
command -v bash
```
```text
/usr/bin/bash
```

```bash
type ls
```
```text
ls is /usr/bin/ls
```

```bash
type cd
```
```text
cd is a shell builtin
```

> ⚠️ `which` 只找外部程序，对内建命令（`cd`、`echo`）会「查无此人」；`command -v` 是更标准的写法。

## A6 管道、重定向与文本处理

### `命令>文件` 把输出写进文件（覆盖）

**解析**　把命令的屏幕输出接进文件，文件原内容全部清掉。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| 命令 | 必填 | 任何会打印东西的命令 |
| 文件 | 必填 | 目标文件；不存在就新建 |

返回：屏幕上看不到输出，内容进了文件

**操作**

```bash
echo "第一行" > out.txt && cat out.txt
```
```text
第一行
```

> ⚠️ `> 文件` 哪怕命令最后什么都没输出，也会先把文件清空 —— 这是常见的数据丢失原因（想追加用 `>>`）。

### `命令>>文件` 把输出追加到文件末尾

**解析**　把输出接进文件末尾，原内容保留。写日志、往配置末尾加一行用它。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| 命令 | 必填 | 任何会打印东西的命令 |
| 文件 | 必填 | 目标文件 |

返回：屏幕无输出，内容追加进文件

**操作**

```bash
echo "第一行" > out.txt && echo "第二行" >> out.txt && cat out.txt
```
```text
第一行
第二行
```

### `命令2>文件` 只把报错信息接进文件

**解析**　正常输出还在屏幕，只有报错（标准错误，编号 2）被写进文件。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| 命令 | 必填 | 会报错或可能报错的命令 |
| 文件 | 必填 | 存报错的文件 |

返回：报错进了文件，正常输出仍在屏幕

**操作**

```bash
ls no-such-file 2> err.txt; cat err.txt
```
```text
ls: cannot access 'no-such-file': No such file or directory
```

> ⚠️ `ls` 报错后退出码是 2（非 0）—— 这是「命令失败」的正常表现，不是你写错了。

### `命令>文件2>&1` 正常输出和报错都接进同一个文件

**解析**　两类输出一起进文件，屏幕一片安静。写日志、排查问题时最常用。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| 命令 | 必填 | 任意命令 |
| 文件 | 必填 | 目标文件 |

返回：屏幕无输出，两类输出都在文件里

**操作**

```bash
ls no-such-file > all.txt 2>&1; cat all.txt
```
```text
ls: cannot access 'no-such-file': No such file or directory
```

> ⚠️ **顺序不能反**：`2>&1 > 文件` 里的 `2>&1` 在 `>` 之前生效，那时 1 还指着屏幕，结果只有正常输出进文件、报错依旧打印在屏幕上。

### `命令1｜命令2` 管道：把上一条的输出当输入

**解析**　Linux 的招牌玩法：命令1 的输出变成命令2 的输入，屏幕上只出现命令2 的输出。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| 命令1 | 必填 | 上游命令 |
| 命令2 | 必填 | 下游命令；可以继续 ｜ 命令3 往下接 |

返回：只有最后一条命令的输出

**操作**

```bash
ls -1 | wc -l
```
```text
8
```

```bash
grep ok notes.txt | wc -l
```
```text
2
```

```bash
sort fruit.txt | head -n 2
```
```text
apple 3
banana 5
```

> ⚠️ 管道只接标准输出（1），**报错不走管道**（还在屏幕）；要让报错也进管道就写 `命令 2>&1 | 下一条`。

### `tee` 又打印到屏幕、又存进文件

**解析**　管道中间的分流器：屏幕上照常显示，同时写一份进文件。调试管道时用它。（记：tee = T 形三通管——一边进、两边出）

| 参数 | 默认值 | 作用 |
|------|--------|------|
| 文件 | 必填 | 要写进哪个文件 |
| -a | 不写 | 追加（不加就覆盖） |

返回：屏幕照常显示 + 文件里有存档

**操作**

```bash
echo "第四行" | tee -a hello.txt && tail -n 1 hello.txt
```
```text
第四行
第四行
```

### `sort` 排序

**解析**　把输入按行排序后打印（不改原文件）。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| 文件 | 可选 | 要排序的文件；不写就从管道读 |
| -n | 不写 | 按数字大小排（默认是字典序，10 会排在 9 前面） |
| -r | 不写 | 倒序 |
| -k2 | 不写 | 按第 2 列排 |
| -u | 不写 | 去重 |

返回：排好序的行

**操作**

```bash
sort fruit.txt
```
```text
apple 3
banana 5
cherry 7
```

```bash
sort -k2 -n fruit.txt
```
```text
apple 3
banana 5
cherry 7
```

```bash
printf '9\n10\n' | sort
```
```text
10
9
```

> ⚠️ 默认字典序会把 `10` 排在 `9` 前面；带数字的列要加 `-n`（或 `-h` 处理 1K/2M 这种）。

### `uniq` 数一数每行重复出现了几次

**解析**　把相邻的重复行合并，打印「次数 内容」。统计日志里谁出现最多就靠它。（记：uniq = unique，去重）

| 参数 | 默认值 | 作用 |
|------|--------|------|
| -c | 常用 | 每行前面加上出现次数 |
| （管道上游） | 必填 | 几乎总要先 sort 再 uniq（uniq 只合并相邻重复行） |

返回：去重后的行（带 -c 是 次数+内容）

**操作**

```bash
sort notes.txt | uniq -c
```
```text
      1 login failed
      2 login ok
```

> ⚠️ `uniq` 只合并**相邻**的重复行，所以几乎总要先 `sort`；不排序直接用 `uniq` 会得到「没去重」的假象。

### `cut` 按分隔符取某一列

**解析**　把每行按分隔符切开，只打印你要的列。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| -d'分隔符' | Tab | 按什么切：-d, 逗号（CSV）、-d: 冒号（/etc/passwd） |
| -f列号 | 必填 | 要第几列：-f1 第 1 列、-f1,3 两列、-f2- 第 2 列到末尾 |
| 文件 | 可选 | 处理哪个文件 |

返回：指定列的内容

**操作**

```bash
cut -d, -f1 data.csv
```
```text
name
tom
amy
```

```bash
cut -d, -f2 data.csv
```
```text
age
18
20
```

> ⚠️ `cut` 只能按**单个字符**分隔，多空格对齐的（比如 `ps` 的输出）用 `awk` 更好。

### `sed 's/旧/新/'` 替换文本（默认只改输出，不改文件）

**解析**　把文本里的「旧」换成「新」打印出来；不加 -i 原文件一点都不变。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| s/旧/新/ | 必填 | 替换规则 |
| g | 不写 | 一行里所有出现都换（不加只换每行第一个） |
| -i | 不写 | 真改文件（没有撤销，改前先备份） |
| 文件 | 必填 | 处理哪个文件 |

返回：替换后的内容（不加 -i 时文件不变）

**操作**

```bash
sed 's/ok/OK/g' notes.txt
```
```text
login OK
login failed
login OK
```

> ⚠️ `-i` 是真改文件、没有撤销：先用不带 `-i` 的版本看一眼结果，确认无误再加 `-i`（macOS 的 `sed -i` 还要求跟一个备份后缀，如 `sed -i '' 's/a/b/'`）。

### `awk '{print $2}'` 取列、做简单计算（文本处理万能工具）

**解析**　按列处理每一行再打印：默认按空格/Tab 分列，$1 第一列、$0 整行。cut 搞不定的交给它。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| '{print $2}' | 必填 | 对每一行做什么：print $2 打第 2 列、s+=$2 累加、END 块打印最终结果 |
| -F'分隔符' | 空格/Tab | 按什么分列（CSV 写 -F,） |
| 文件 | 可选 | 处理哪个文件 |

返回：按列处理后的输出

**操作**

```bash
awk -F, '{print $2}' data.csv
```
```text
age
18
20
```

```bash
awk '{s+=$2} END{print s}' fruit.txt
```
```text
15
```

> ⚠️ `cut` 搞不定的（多个空格、条件判断、求和）交给他。它是「一门小语言」，不用全学，先会用 `print $n` 和求和。

### `xargs` 把上一条的输出变成下一条的参数

**解析**　很多命令不读管道、只认参数（rm、cp、wc）：把上游输出的每个「词」接到下游命令后面执行。（记：xargs = extended arguments，扩展参数）

| 参数 | 默认值 | 作用 |
|------|--------|------|
| 命令2 | 必填 | 下游命令（不读管道输入的那种） |
| -0 | 不写 | 上游用 -print0 输出、文件里有空格时的安全写法 |

返回：下游命令的执行结果

**操作**

```bash
printf 'hello.txt\nempty.txt\n' | xargs wc -l
```
```text
 3 hello.txt
 0 empty.txt
 3 total
```

> ⚠️ 文件名里有空格时 `xargs` 会拆错：用 `find ... -print0 | xargs -0 命令` 这种零分隔写法才安全。

## A7 权限与用户

### `chmod` 改文件权限（符号写法和数字写法）

**解析**　修改文件/目录的权限：谁能读、谁能写、谁能执行。（记：chmod = change mode，改权限模式）

| 参数 | 默认值 | 作用 |
|------|--------|------|
| u/g/o/a | — | 给谁改：u 自己、g 同组、o 其他人、a 所有人 |
| +/-/= | — | 加权限 / 减权限 / 设成（符号写法） |
| r/w/x | — | 读 / 写 / 执行 |
| 数字 | — | 数字写法：r=4、w=2、x=1 加起来；644 = rw-r--r--、755 = rwxr-xr-x |
| -R | 不写 | 递归改整个目录（更稳的做法是 find 区分文件和目录分开设） |
| 文件 | 必填 | 要改权限的对象 |

返回：没有输出；权限位被改掉

**操作**

```bash
chmod -x run.sh && ls -l run.sh
```
```text
-rw-r--r-- 1 root root 34 Jan  1  2026 run.sh
```

```bash
chmod +x run.sh && ls -l run.sh
```
```text
-rwxr-xr-x 1 root root 34 Jan  1  2026 run.sh
```

```bash
chmod 644 hello.txt && chmod 755 run.sh && stat -c '%a %n' hello.txt run.sh
```
```text
644 hello.txt
755 run.sh
```

```bash
mkdir -p perm/sub && printf 'x\n' > perm/sub/file.txt && chmod -R 700 perm && stat -c '%a %n' perm perm/sub perm/sub/file.txt
```
```text
700 perm
700 perm/sub
700 perm/sub/file.txt
```

> ⚠️ 脚本报 `Permission denied` 但文件明明在，八成是少了 `x`：`chmod +x 脚本.sh` 就好。；`chmod 777`（所有人都能读改删）是最糟的权限，安全上别用；日常：普通文件 644、要执行的脚本和目录 755。；文件和目录需要的权限不一样，一把梭的 `-R` 常出问题：更稳的写法是 `find 目录 -type d -exec chmod 755 {} +`、`find 目录 -type f -exec chmod 644 {} +` 分开设。

### `chown、chgrp` 改文件的属主、属组

**解析**　改一个文件「归谁」：chown 改属主、chgrp 改组。要 root 权限（前面加 sudo）。（记：chown = change owner 改属主；chgrp = change group 改属组）

| 参数 | 默认值 | 作用 |
|------|--------|------|
| 用户 | 必填 | chown 的新属主（可以写 用户:组 一起改） |
| 组 | 必填 | chgrp 的新属组 |
| 文件 | 必填 | 要改的文件 |
| -R | 不写 | 递归改整个目录 |

返回：没有输出；ls -l 第 3、4 列会变

**操作**

```bash
chown 1000 hello.txt && stat -c '%u %g %n' hello.txt
```
```text
1000 0 hello.txt
```

```bash
chown 1000:1000 hello.txt && stat -c '%u %g %n' hello.txt
```
```text
1000 1000 hello.txt
```

> ⚠️ 网站报 403、服务读不到文件，很常见的原因就是属主不对（比如 root 建的文件，服务以 www-data 跑）。

### `umask` 看或改新建文件的默认权限

**解析**　umask 是「新建时不给哪些权限」的掩码：022 → 新文件 644、新目录 755。（记：umask = user file-creation mask，新建文件的权限掩码）

| 参数 | 默认值 | 作用 |
|------|--------|------|
| （不写参数） | — | 查看当前掩码（如 0022） |
| 三位数字 | — | 设置新掩码（如 077 → 新文件只有自己能看） |

返回：当前掩码（改的时候无输出）

**操作**

```bash
umask
```
```text
0022
```

```bash
touch newfile.txt && stat -c '%a %n' newfile.txt
```
```text
644 newfile.txt
```

```bash
umask 077 && touch private.txt && stat -c '%a %n' private.txt
```
```text
600 private.txt
```

> ⚠️ umask 只影响**之后新建**的文件，已存在的文件不受影响；想长期生效得写进 `~/.bashrc`。

### `whoami、id` 我是谁、我的 uid 和组

**解析**　在别人机器上先搞清楚自己是谁：很多命令能不能跑、文件能不能读，全看这个。（记：whoami = who am I；id = identity，身份）

返回：用户名 / uid、gid、所属组

**操作**

```bash
whoami
```
```text
root
```

```bash
id
```
```text
uid=0(root) gid=0(root) groups=0(root)
```

> ⚠️ 示例在容器里所以是 `root`；你自己机器上会是你的普通用户名。加了 `sudo` 之后 `whoami` 就变成 root。

### `sudo` 用 root 权限跑一条命令

**解析**　以 root 身份执行一条命令（root 是权限最大的用户）。第一次会问你自己账户的密码。（记：sudo = superuser do，以超级用户身份做）

| 参数 | 默认值 | 作用 |
|------|--------|------|
| 命令 | 必填 | 要以 root 跑的完整命令 |
| -i | 不写 | 直接进 root 的 shell |
| !! | — | sudo !! 用 root 重跑上一条（忘了加 sudo 时用） |
| -l | 不写 | 看你能 sudo 哪些命令 |

返回：命令正常执行（以 root 身份）

**操作**

```bash
sudo apt update
```
```text
（未实跑：需要真实系统装了 sudo 并知道密码。别习惯性给所有命令加 sudo —— 它的破坏力也是 root 级的，先问自己「这条命令真的需要 root 吗」）
```

## A8 进程与作业

### `ps` 看进程（这个终端的或整台机器的）

**解析**　列出进程：PID（进程号）、TTY、TIME、CMD 几列。排查「什么在跑、什么在占资源」的第一步。（记：ps = process status，进程状态）

| 参数 | 默认值 | 作用 |
|------|--------|------|
| （不写参数） | — | 只看当前终端里的进程 |
| -e | 不写 | 所有进程 |
| -ef | 不写 | 所有进程 + 全格式（最常用；| grep 关键词 过滤） |
| aux | 不写 | BSD 风格的另一种全量写法 |

返回：一行一个进程的表格

**操作**

```bash
sleep 300 & ps
```
```text
（结构示例：PID 每次都不同）
    PID TTY          TIME CMD
      1 pts/0    00:00:00 bash
     42 pts/0    00:00:00 sleep
    123 pts/0    00:00:00 ps
```

```bash
ps -ef | head -n 3
```
```text
（结构示例：每台机器的进程都不一样，这里只看列的含义）
UID        PID  PPID  C STIME TTY          TIME CMD
root         1     0  0 08:00 ?        00:00:00 bash
root        42     1  0 08:00 pts/0    00:00:00 sleep 300
```

### `pgrep` 按名字查进程的 PID

**解析**　按名字找进程，直接打印 PID（比 ps | grep 省事，自动跳过 grep 自己）。（记：pgrep = process grep，按名字找进程）

| 参数 | 默认值 | 作用 |
|------|--------|------|
| 名字 | 必填 | 进程名（模糊匹配：pgrep ssh 会连 sshd 一起匹配） |
| -a | 不写 | 连命令行一起显示 |
| -c | 不写 | 只给个数 |

返回：PID（一行一个）

**操作**

```bash
sleep 300 & sleep 300 & pgrep -c sleep
```
```text
2
```

> ⚠️ 名字是**模糊匹配**：`pgrep ssh` 会连 sshd、ssh-agent 一起匹配到。杀之前先 `pgrep -a` 看清楚。

### `top` 动态看谁在吃 CPU、内存

**解析**　交互式界面实时看系统负载和进程排行；q 退出、M 按内存排、P 按 CPU 排。（记：top = Table of Processes，按资源占用排的进程表）

| 参数 | 默认值 | 作用 |
|------|--------|------|
| （交互按键） | — | q 退出、M 按内存、P 按 CPU |
| -b -n 1 | 不写 | 拍一张快照就退出（适合丢进管道或文件） |

返回：实时刷新的进程界面

**操作**

```bash
top -b -n 1 | head -n 5
```
```text
（结构示例：每台机器的进程和负载都不一样，只列格式）
top - 08:00:00 up  1:23,  1 user,  load average: 0.00, 0.01, 0.05
Tasks:   3 total,   1 running,   2 sleeping,   0 stopped,   0 zombie
%Cpu(s):  0.3 us,  0.2 sy,  0.0 ni, 99.5 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
MiB Mem :   7931.0 total,   6021.4 free,    406.0 used,   1503.6 buff/cache
```

### `kill` 结束一个进程

**解析**　给进程发信号让它退出：默认 TERM（15）请它自己退；-9 是强杀。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| PID | 必填 | 要结束的进程号（从 ps/pgrep 拿） |
| -9 | 不写 | 强制杀死，程序拦不住（先普通 kill、不行再 -9） |

返回：没有输出；进程结束

**操作**

```bash
sleep 300 & kill $!; wait $! 2>/dev/null; echo "退出码 $?"
```
```text
退出码 143
```

> ⚠️ 顺序是**先 `kill`、不行再 `kill -9`**：`-9` 不给程序收尾机会，可能留下写坏的文件。上面那个 `143` = 128 + 15（被 TERM 结束）。

### `sleep` 等一会儿（暂停 N 秒）

**解析**　什么都不干，等够时间再继续。脚本里等服务起来时用。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| 秒数 | 必填 | 睡多久；支持 1m（分钟）、2h（小时） |

返回：没有输出（时间到了才继续）

**操作**

```bash
sleep 2 && echo "睡完了"
```
```text
睡完了
```

> ⚠️ 前台 `sleep` 会占住终端，等得不耐烦就 `Ctrl+C`；想让它后台睡就写 `sleep 300 &`。

### `&、jobs、fg` 放到后台跑、把后台作业拉回来

**解析**　命令末尾加 & 立刻回到提示符（命令继续跑）；jobs 看后台清单；fg 把作业拉回前台。（记：fg = foreground 前台；bg = background 后台）

| 参数 | 默认值 | 作用 |
|------|--------|------|
| 命令 & | — | 放后台跑 |
| jobs | — | 列出后台作业（%1、%2 是编号） |
| fg %1 | — | 把作业拉回前台；bg %1 把挂起的作业推到后台继续跑 |
| Ctrl+Z | — | 把正在跑的命令挂起（暂停） |

返回：提示符立刻回来；jobs 打印作业清单

**操作**

```bash
sleep 300 & sleep 300 & jobs
```
```text
（结构示例：作业号和 PID 每次都不同）
[1]-  Running                 sleep 300 &
[2]+  Running                 sleep 300 &
```

> ⚠️ 后台进程的输出还是会打到你这个屏幕上（把终端搅乱）：一般配 `> 文件 2>&1` 或 `> /dev/null` 把输出接走。

### `nohup` 关掉终端也别停（后台长任务）

**解析**　让命令忽略「终端挂断」信号：退出 SSH 后它还继续跑。跑长任务（扫描、爬虫）时用。（记：nohup = no hangup，终端挂断也不停）

| 参数 | 默认值 | 作用 |
|------|--------|------|
| 命令 | 必填 | 要跑的长任务 |
| & | 必填 | 配合 nohup 使用，否则还是占着终端 |
| > 日志文件 2>&1 | 推荐 | 把输出接走，默认是追加到 nohup.out |

返回：命令在后台继续跑

**操作**

```bash
nohup sleep 300 > nohup.out 2>&1 & jobs && cat nohup.out
```
```text
（结构示例：作业号和 PID 每次都不同）
[1]+  Running                 nohup sleep 300 > nohup.out 2>&1 &
```

> ⚠️ 不带 `&` 的 `nohup 命令` 还是占着终端（只是不怕挂断）；要真后台，`nohup ... &` 两个一起写。

## A9 网络与远程

### `ip` 看网卡和 IP 地址

**解析**　查看每张网卡的状态、MAC、IP。找 inet 那一行就是 IPv4 地址。（记：ip = Internet Protocol，网际协议）

| 参数 | 默认值 | 作用 |
|------|--------|------|
| a | — | 所有网卡详情（= ip addr） |
| -o -4 addr show | — | 一行一个 IPv4 地址（脚本里取 IP 用这个） |
| r | — | 看默认网关和路由 |

返回：网卡信息表

**操作**

```bash
ip a
```
```text
（结构示例：网卡名、IP、MAC 每台机器都不同，这里只看格式）
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:42:ac:11:00:02 brd ff:ff:ff:ff:ff:ff
    inet 172.17.0.2/16 brd 172.17.255.255 scope global eth0
```

```bash
ip -o -4 addr show lo
```
```text
1: lo    inet 127.0.0.1/8 scope host lo\       valid_lft forever preferred_lft forever
```

> ⚠️ 输出里的空格数量会随 iproute2 版本略有差别，取字段用 `awk '{print $4}'` 比按位置切字符串稳。

### `ss` 看谁在监听端口（本机开了哪些服务）

**解析**　列出处于 LISTEN 状态的 TCP 端口，看本机开了哪些服务。（记：ss = socket statistics，套接字统计）

| 参数 | 默认值 | 作用 |
|------|--------|------|
| -t | — | TCP（-u 是 UDP） |
| -l | — | 只听着的（LISTEN 状态） |
| -n | — | 不解析域名：显示端口号，输出快 |
| -p | — | 多一列：是哪个进程在听（要 root） |

返回：监听端口清单

**操作**

```bash
ss -tln
```
```text
State Recv-Q Send-Q Local Address:Port Peer Address:Port
```

> ⚠️ 加 `-p` 需要 root 权限；老教程里的 `netstat -tlnp` 要装 `net-tools`，`ss` 才是现在的标准工具。

### `ping` 测「通不通」（发 ICMP 包）

**解析**　每秒发一个包测主机通不通，打印往返时间。排网络问题的第一步。（记：ping 是声呐的拟声词——发个脉冲、听回声测距离）

| 参数 | 默认值 | 作用 |
|------|--------|------|
| 主机或IP | 必填 | 要测的目标（ping 域名顺便验证 DNS 通不通） |
| -c 3 | 不写 | 只发 3 个就停（不加会一直 ping，Ctrl+C 停） |

返回：每秒一行的往返时间

**操作**

```bash
ping -c 3 127.0.0.1
```
```text
（结构示例：每次的耗时（time=）都不同，只看格式）
PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.031 ms
64 bytes from 127.0.0.1: icmp_seq=2 ttl=64 time=0.028 ms

--- 127.0.0.1 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2028ms
```

### `curl` 抓网页、调接口（发 HTTP 请求）

**解析**　把 HTTP 响应的正文打到屏幕上。测试 Web 服务、看接口返回、确认状态码都用它。（记：curl = client for URLs，URL 客户端）

| 参数 | 默认值 | 作用 |
|------|--------|------|
| URL | 必填 | 要请求的地址 |
| -s | 不写 | 安静模式（不显示进度） |
| -i | 不写 | 连响应头一起看 |
| -I | 不写 | 只看响应头（HEAD 请求） |
| -o 文件 | 不写 | 把正文存进文件（默认打到屏幕） |
| -X 方法 -d 数据 | 不写 | 发 POST 等请求（curl -X POST -d 'a=1' URL） |

返回：响应正文

**操作**

```bash
(python3 -m http.server 8000 --directory . > /dev/null 2>&1 &) && sleep 1 && curl -s http://127.0.0.1:8000/hello.txt
```
```text
hello linux
second line
third line
```

> ⚠️ 示例为了不依赖外网，先在本地起了一个测试服务器（第一行那句 `python3 -m http.server`）—— 真实使用时你直接写 `curl https://example.com` 就行。

### `wget` 下载文件到当前目录

**解析**　把 URL 指向的文件下载到当前目录（curl 默认打到屏幕，wget 默认存文件）。（记：wget = Web get，从网上拿）

| 参数 | 默认值 | 作用 |
|------|--------|------|
| URL | 必填 | 要下载的地址 |
| -O 名字 | 不写 | 另存为指定文件名 |
| -c | 不写 | 断点续传（大文件下到一半断了接着下） |
| -q | 不写 | 安静模式 |

返回：文件出现在当前目录

**操作**

```bash
(python3 -m http.server 8000 --directory . > /dev/null 2>&1 &) && sleep 1 && wget -q -O - http://127.0.0.1:8000/fruit.txt
```
```text
apple 3
banana 5
cherry 7
```

> ⚠️ macOS **没有自带 wget**（只有 curl），要用得先 `brew install wget`；示例同样是在本地测试服务器上跑的。

### `nc` 测某个端口开没开

**解析**　只连不发数据（-z），看端口通不通。比 ping 更有用：很多服务器禁 ICMP，但服务其实是好的。（记：nc = netcat，网络版的 cat，瑞士军刀）

| 参数 | 默认值 | 作用 |
|------|--------|------|
| -z | — | 只连不发数据 |
| -v | — | 显示结果（succeeded 或报错） |
| 主机 | 必填 | 目标主机 |
| 端口 | 必填 | 目标端口 |

返回：succeeded 或报错（refused = 端口没人听；timed out = 根本没连上）

**操作**

```bash
nc -zv 127.0.0.1 22 2>&1
```
```text
nc: connect to 127.0.0.1 port 22 (tcp) failed: Connection refused
```

> ⚠️ 两种报错要分清：`Connection refused` = 连到了主机但这个端口没人听；`timed out` = 根本没连上（网络不通或被防火墙丢包）。

### `ssh` 登录远程主机

**解析**　连上远程主机，之后就在对方的 shell 里操作。exit 退出。（记：ssh = secure shell，安全的 shell）

| 参数 | 默认值 | 作用 |
|------|--------|------|
| 用户@主机 | 必填 | 用什么账号登哪台机器（如 kali@192.168.64.2） |
| -p 端口 | 22 | 换端口 |
| -i 私钥文件 | 不写 | 指定密钥登录 |
| 命令 | 可选 | ssh 主机 命令 = 跑一条命令就断开 |

返回：进入远程 shell（或单条命令的输出）

**操作**

```bash
ssh user@example.com
```
```text
（未实跑：需要一台真实的远程主机。三种常见报错：`Permission denied (publickey)` = 密钥/用户名不对；`Connection refused` = 对方没开 sshd 或端口不对；`Host key verification failed` = 主机指纹变了）
```

### `scp` 在本地和远程之间复制文件

**解析**　把文件传过去或拉回来。写法是「谁在前谁就是源」。（记：scp = secure copy，安全的复制）

| 参数 | 默认值 | 作用 |
|------|--------|------|
| 源 | 必填 | 本地文件 或 用户@主机:远程路径 |
| 目标 | 必填 | 另一个位置（. 表示当前本地目录） |
| -r | 不写 | 传整个目录 |
| -P 端口 | 22 | 换端口（大写 P，和 ssh 的小写 -p 不同） |

返回：传输进度和结果

**操作**

```bash
scp report.txt kali@192.168.1.10:/tmp/
```
```text
（未实跑：需要真实主机。OpenSSH 官方现在更推荐 `sftp` 或 `rsync -av`，但简单传文件 `scp` 还是最顺手）
```

## A10 压缩与打包

### `tar` 打包压缩（-czf 打包、-tzf 看包、-xzf 解包）

**解析**　Linux 最常用的打包工具：把目录/文件打成 .tar.gz，或解开。字母记法：c 创建、t 查看、x 解开、z 用 gzip、f 指定包名。（记：tar = tape archive，磁带归档，老传统）

| 参数 | 默认值 | 作用 |
|------|--------|------|
| -czf 包名 东西... | — | 打包压缩（f 后面必须紧跟包名，一般放最后） |
| -tzf 包名 | — | 看包里有什么（不解开，解压前先跑一遍） |
| -xzf 包名 | — | 解包到当前目录（-C 目录 可指定解到哪） |
| -v | 不写 | 边做边列出文件 |

返回：-czf/-xzf 无输出；-tzf 打印包内文件清单

**操作**

```bash
tar -czf bak.tar.gz dir1 hello.txt && stat -c '%s %n' bak.tar.gz
```
```text
168 bak.tar.gz
```

```bash
tar -czf bak.tar.gz dir1 hello.txt && tar -tzf bak.tar.gz
```
```text
dir1/
hello.txt
```

```bash
tar -czf bak.tar.gz dir1 hello.txt && mkdir restore && tar -xzf bak.tar.gz -C restore && find restore -type f | sort
```
```text
restore/hello.txt
```

> ⚠️ `tar -czf 包 目录` 是把整个目录（连路径）放进去；打包大量重复文件时 `-z` 很慢，可以先去 `-v` 看是不是包错东西了。；解压来路不明的包有风险：包里可能带 `../` 或绝对路径，解到你的重要目录会覆盖文件（GNU tar 会自动去掉开头的 `/` 和 `../` 并报 `Member name contains '..'` 退出，但别指望所有解压工具都这么乖）。先 `-tzf` 看文件列表最稳。；解之前先 `ls` 看当前在哪、最好新建一个空目录再解 —— 否则一堆文件会散在你当前的目录里。

### `gzip、gunzip` 压缩单个文件（不是打包目录）

**解析**　gzip 只能压单个文件：gzip 会把原文件替换成 文件.gz，gunzip 反向还原。压目录要用 tar -czf。（记：gzip = GNU zip；gunzip 反过来解开）

| 参数 | 默认值 | 作用 |
|------|--------|------|
| 文件 | 必填 | gzip 的压缩对象（单个文件） |
| 文件.gz | 必填 | gunzip 的还原对象 |
| -k | 不写 | gzip 时保留原文件 |
| -d | 不写 | 等于 gunzip |

返回：压缩后原文件消失（变成 .gz）；gunzip 还原

**操作**

```bash
cp hello.txt gz-demo.txt && gzip gz-demo.txt && ls -1 gz-demo.txt.gz
```
```text
gz-demo.txt.gz
```

```bash
cp hello.txt gz-demo.txt && gzip gz-demo.txt && gunzip gz-demo.txt.gz && ls -1 gz-demo.txt
```
```text
gz-demo.txt
```

> ⚠️ gzip 只能压**单个文件**，压目录要用 `tar -czf`（所以才有 `.tar.gz` 这种双后缀）。

### `zip、unzip` 跨平台压缩包（给 Windows 用）

**解析**　Windows 不认 .tar.gz：和 Windows 交换文件用 zip。需要先装：sudo apt install zip unzip。（记：zip = 拉链——拉上压缩、拉开解压）

| 参数 | 默认值 | 作用 |
|------|--------|------|
| -r 包名.zip 目录 | — | zip 打包目录（-r 递归） |
| 包名.zip | — | unzip 解压对象 |
| -l 包名.zip | — | 只看内容清单不解压 |

返回：压缩包出现 / 文件解出

**操作**

```bash
zip -r bak.zip dir1
```
```text
（未实跑：校验容器里没有 zip / unzip。跨系统传 zip 时中文文件名容易乱码，收下后先 `unzip -l` 看一眼名字对不对）
```

## A11 系统信息与软件包

### `cat /etc/os-release` 我在什么系统上（发行版与版本）

**解析**　看当前系统的发行版名字和版本号（PRETTY_NAME 那一行最有用）。

返回：发行版信息（PRETTY_NAME = 名字+版本）

**操作**

```bash
head -n 3 /etc/os-release
```
```text
PRETTY_NAME="Ubuntu 24.04.5 LTS"
NAME="Ubuntu"
VERSION_ID="24.04"
```

> ⚠️ 你在容器里看到的这个文件是**容器自己的**，和宿主机（你的 macOS）无关。

### `uname` 看内核版本和机器架构

**解析**　打印内核名、主机名、内核版本、CPU 架构。装软件包前先看一眼架构，下载错架构是最常见的低级错误。（记：uname = Unix name，Unix 系统信息）

| 参数 | 默认值 | 作用 |
|------|--------|------|
| -a | — | 全部信息 |
| -r | — | 只要内核版本 |
| -m | — | 只要架构（x86_64 或 aarch64） |

返回：系统信息一行

**操作**

```bash
uname -a
```
```text
（结构示例：主机名、内核版本、架构每台机器都不同，只看格式）
Linux hostname 6.8.0-117-generic #117-Ubuntu SMP PREEMPT_DYNAMIC aarch64 GNU/Linux
```

### `df` 看磁盘还剩多少空间

**解析**　一行一个分区：容量、已用、可用、使用率、挂载点。「磁盘满了」靠它定位。（记：df = disk free，磁盘剩余空间）

| 参数 | 默认值 | 作用 |
|------|--------|------|
| -h | 常用 | 大小用 G/M 显示 |
| 路径 | 可选 | 只看这个路径所在的分区（df -h .） |

返回：分区使用情况表

**操作**

```bash
df -h
```
```text
（结构示例：每台机器的容量和挂载点都不同，只看格式）
Filesystem      Size  Used Avail Use% Mounted on
overlay          59G  4.8G   51G   9% /
tmpfs            64M     0   64M   0% /dev
```

### `du` 看某个目录占了多少空间

**解析**　统计目录占用的磁盘空间。磁盘满了想知道是谁占的：du -sh * | sort -h（最大的在最后）。（记：du = disk usage，磁盘用量）

| 参数 | 默认值 | 作用 |
|------|--------|------|
| -s | 常用 | 只给总计，不列子目录 |
| -h | 常用 | 人类可读（K/M/G） |
| 目录 | 必填 | 要统计的目录（* 表示当前目录下每个条目） |

返回：占用空间数字

**操作**

```bash
du -sh .
```
```text
32K	.
```

```bash
du -sh dir1
```
```text
4.0K	dir1
```

> ⚠️ `du` 算的是**占用块**（4K 起跳），和 `ls -l` 显示的字节数不完全一样；软链接默认不跟着算进去。

### `free` 看内存和 swap 使用情况

**解析**　打印总内存、已用、空闲、缓存以及 swap 用量；重点看 available 列。

| 参数 | 默认值 | 作用 |
|------|--------|------|
| -h | 常用 | 人类可读 |
| -s 2 | 不写 | 每 2 秒刷新一次（Ctrl+C 停） |

返回：内存使用表

**操作**

```bash
free -h
```
```text
（结构示例：内存大小和用量每台机器都不同，只看格式）
               total        used        free      shared  buff/cache   available
Mem:           7.7Gi       406Mi       5.9Gi       1.0Mi       1.5Gi       7.0Gi
Swap:          2.0Gi          0B       2.0Gi
```

### `echo $PATH` 命令是从哪些目录里找的（PATH 环境变量）

**解析**　打印 PATH 变量：一串用冒号分隔的目录，你敲命令时 shell 从左到右在这些目录里找同名程序。

返回：一串冒号分隔的目录

**操作**

```bash
echo $PATH
```
```text
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
```

```bash
echo "$PATH" | tr ':' '\n'
```
```text
/usr/local/sbin
/usr/local/bin
/usr/sbin
/usr/bin
/sbin
/bin
```

> ⚠️ 改 PATH 必须带上 `$PATH`：写成 `export PATH="$HOME/bin"` 会把系统目录全丢掉，之后 `ls`、`head` 全都 `command not found`（只能关掉这个终端重开）。

### `export、alias` 临时设环境变量、造命令别名

**解析**　export 设环境变量（子进程能看见）；alias 造命令快捷写法。都只对当前终端有效，长期生效写进 ~/.bashrc。（记：export = 导出，把变量传给子进程；alias = 别名）

| 参数 | 默认值 | 作用 |
|------|--------|------|
| 名字=值 | 必填 | export 的变量（echo $名字 查看，env 里也在） |
| 别名='命令' | 必填 | alias 的快捷写法（alias 只在交互式 shell 生效，脚本里不展开） |

返回：无输出；变量或别名即刻可用

**操作**

```bash
export SITE=dvwa && echo $SITE
```
```text
dvwa
```

```bash
alias ll='ls -l' && alias ll
```
```text
alias ll='ls -l'
```

```bash
export SITE=dvwa && env | grep '^SITE='
```
```text
SITE=dvwa
```

> ⚠️ `alias` 只在**交互式** shell 里展开，脚本里不生效（脚本里请用函数或者写完整命令）；别把 `ls` 之类的常用命令覆盖成危险别名。

### `apt` 装、卸软件（Debian、Ubuntu、Kali 系）

**解析**　Debian 系的软件包管理器：update 刷新清单、install 安装、search 搜索、remove 卸载。（记：apt = advanced package tool，高级软件包工具）

| 参数 | 默认值 | 作用 |
|------|--------|------|
| update | — | 刷新软件清单（安装前先跑） |
| install 包名 | — | 安装软件 |
| search 关键词 | — | 搜索包名 |
| remove 包名 | — | 卸载 |

返回：一堆过程输出和结果

**操作**

```bash
sudo apt update
```
```text
（未实跑：需要 root + 网络；在 Kali/Ubuntu 上直接敲就行）
```

```bash
sudo apt install -y tree
```
```text
（未实跑：需要 root + 网络）
```

## 学习建议

1. **别背，练**：这份笔记是「忘了来查」的，不是「背下来再上机」的。真想记住一条命令，去 `~/linux-lab` 里亲手敲三遍。
2. **键盘上的保命操作**（比命令还常用）：`Ctrl+C` 停掉正在跑的命令、`Ctrl+L` 清屏、`Ctrl+R` 搜索敲过的历史、`Tab` 补全、`↑` 翻上一条。
3. **三个新手最常踩的坑**：成功时没输出（正常）；大小写写错（`LS` 不是 `ls`）；路径写错（`~`、`.`、`..`、`/` 先分清）。
4. **下一步（往安全方向走）**：这些是网安工具的地基——`ss`、`nc`、`grep`、`awk`、`tail -f` 之后都会天天用。配套的《网络安全工具速查笔记》从 `dig`、`nmap` 讲起。
