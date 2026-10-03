# Linux 常用指令速查笔记（小白版）

## 怎么用这份文件

这份笔记写给**完全没用过 Linux 的人**。每条命令都配一个能直接复制的示例，示例下面那段输出是
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
- 正文每条格式一样：**签名**（怎么敲）｜**返回**（你会得到什么）｜**备注**（什么时候用、等价写法），下面接示例。
- `> ⚠️` 开头的行专门讲坑，尤其是带删除、带权限、带 `rm` 的那些，值得多看两眼。
- 命令会**跨章节重复**（`ls`、`grep` 这些），这是故意的：你的用法是「从索引跳过来查一条」，重复比来回翻页省事。

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
| A1 终端与命令 | [`命令 --help`](#命令---help-看命令自带的用法说明) | 看命令自带的用法说明 |
| A1 终端与命令 | [`man`](#man-看完整的手册页比---help-详细) | 看完整的手册页（比 --help 详细） |
| A1 终端与命令 | [`命令 --version`](#命令---version-看这个命令的版本) | 看这个命令的版本 |
| A2 目录与路径 | [`pwd`](#pwd-我现在在哪个目录) | 我现在在哪个目录 |
| A2 目录与路径 | [`ls`](#ls-看这个目录里有什么) | 看这个目录里有什么 |
| A2 目录与路径 | [`ls -a`](#ls--a-连隐藏文件一起列出来) | 连隐藏文件一起列出来 |
| A2 目录与路径 | [`ls -l`](#ls--l-长格式看权限属主大小时间) | 长格式：看权限、属主、大小、时间 |
| A2 目录与路径 | [`ls -lh`](#ls--lh-大小变成-40k-这种好读的写法) | 大小变成 4.0K 这种好读的写法 |
| A2 目录与路径 | [`ls -lt`](#ls--lt-按修改时间排最新的在最上面) | 按修改时间排，最新的在最上面 |
| A2 目录与路径 | [`cd`](#cd-进到某个目录里) | 进到某个目录里 |
| A2 目录与路径 | [`cd .. / cd ~ / cd -`](#cd---cd---cd---三个最常用的跳回去) | 三个最常用的「跳回去」 |
| A2 目录与路径 | [`mkdir`](#mkdir-新建目录) | 新建目录 |
| A2 目录与路径 | [`tree`](#tree-树形看目录结构一眼看懂层级) | 树形看目录结构（一眼看懂层级） |
| A3 文件操作 | [`touch`](#touch-建一个空文件或只更新它的时间) | 建一个空文件（或只更新它的时间） |
| A3 文件操作 | [`cp`](#cp-复制文件) | 复制文件 |
| A3 文件操作 | [`cp -r`](#cp--r-复制整个目录含里面的东西) | 复制整个目录（含里面的东西） |
| A3 文件操作 | [`mv`](#mv-移动文件--给文件改名) | 移动文件 / 给文件改名 |
| A3 文件操作 | [`rm`](#rm-删文件) | 删文件 |
| A3 文件操作 | [`rm -r / rm -rf`](#rm--r--rm--rf-删目录危险命令) | 删目录（危险命令） |
| A3 文件操作 | [`ln -s`](#ln--s-建软链接快捷方式) | 建软链接（快捷方式） |
| A3 文件操作 | [`stat`](#stat-看文件的各种详细信息) | 看文件的各种详细信息 |
| A4 看文件内容 | [`cat`](#cat-把文件内容整个打印出来) | 把文件内容整个打印出来 |
| A4 看文件内容 | [`less`](#less-分页看大文件可以上下翻搜索) | 分页看大文件（可以上下翻、搜索） |
| A4 看文件内容 | [`head`](#head-只看开头几行) | 只看开头几行 |
| A4 看文件内容 | [`tail`](#tail-只看结尾几行盯日志常用) | 只看结尾几行（盯日志常用） |
| A4 看文件内容 | [`wc`](#wc-数行数--单词数--字节数) | 数行数 / 单词数 / 字节数 |
| A4 看文件内容 | [`nl / cat -n`](#nl--cat--n-带行号打印方便讨论第几行) | 带行号打印（方便讨论“第几行”） |
| A4 看文件内容 | [`diff`](#diff-比较两个文件哪里不一样) | 比较两个文件哪里不一样 |
| A5 查找与搜索 | [`find . -name`](#find---name-按名字找文件会钻进所有子目录) | 按名字找文件（会钻进所有子目录） |
| A5 查找与搜索 | [`find . -type`](#find---type-按类型找只要文件--只要目录) | 按类型找（只要文件 / 只要目录） |
| A5 查找与搜索 | [`grep`](#grep-在文件里找包含某个词的行) | 在文件里找包含某个词的行 |
| A5 查找与搜索 | [`grep -n / -i`](#grep--n---i-显示行号--忽略大小写) | 显示行号 / 忽略大小写 |
| A5 查找与搜索 | [`grep -c / -v`](#grep--c---v-只数数量--看没匹配上的行) | 只数数量 / 看没匹配上的行 |
| A5 查找与搜索 | [`grep -r`](#grep--r-在整个目录里递归搜索) | 在整个目录里递归搜索 |
| A5 查找与搜索 | [`which / command -v / type`](#which--command--v--type-这个命令到底是哪个程序) | 这个命令到底是哪个程序 |
| A6 管道、重定向与文本处理 | [`命令 > 文件`](#命令--文件-把输出写进文件覆盖) | 把输出写进文件（覆盖） |
| A6 管道、重定向与文本处理 | [`命令 >> 文件`](#命令--文件-把输出追加到文件末尾) | 把输出追加到文件末尾 |
| A6 管道、重定向与文本处理 | [`命令 2> 文件`](#命令-2-文件-只把报错信息接进文件) | 只把报错信息接进文件 |
| A6 管道、重定向与文本处理 | [`命令 > 文件 2>&1`](#命令--文件-21-正常输出和报错都接进同一个文件) | 正常输出和报错都接进同一个文件 |
| A6 管道、重定向与文本处理 | [`命令1 ｜ 命令2`](#命令1--命令2-管道把上一条的输出当输入) | 管道：把上一条的输出当输入 |
| A6 管道、重定向与文本处理 | [`tee`](#tee-又打印到屏幕又存进文件) | 又打印到屏幕、又存进文件 |
| A6 管道、重定向与文本处理 | [`sort`](#sort-排序) | 排序 |
| A6 管道、重定向与文本处理 | [`uniq -c`](#uniq--c-数一数每行重复出现了几次) | 数一数每行重复出现了几次 |
| A6 管道、重定向与文本处理 | [`cut`](#cut-按分隔符取某一列) | 按分隔符取某一列 |
| A6 管道、重定向与文本处理 | [`sed 's/旧/新/'`](#sed-s旧新-替换文本默认只改输出不改文件) | 替换文本（默认只改输出，不改文件） |
| A6 管道、重定向与文本处理 | [`awk '{print $2}'`](#awk-print-2-取列--做简单计算文本处理万能工具) | 取列 / 做简单计算（文本处理万能工具） |
| A6 管道、重定向与文本处理 | [`xargs`](#xargs-把上一条的输出变成下一条的参数) | 把上一条的输出变成下一条的参数 |
| A7 权限与用户 | [`chmod +x`](#chmod-x-给文件加减权限符号写法) | 给文件加/减权限（符号写法） |
| A7 权限与用户 | [`chmod 644 / 755`](#chmod-644--755-给文件设权限数字写法最常见) | 给文件设权限（数字写法，最常见） |
| A7 权限与用户 | [`chmod -R`](#chmod--r-递归改一个目录里所有东西的权限) | 递归改一个目录里所有东西的权限 |
| A7 权限与用户 | [`chown / chgrp`](#chown--chgrp-改文件的属主--属组) | 改文件的属主 / 属组 |
| A7 权限与用户 | [`umask`](#umask-看改新建文件的默认权限) | 看/改新建文件的默认权限 |
| A7 权限与用户 | [`whoami / id`](#whoami--id-我是谁--我的-uid-和组) | 我是谁 / 我的 uid 和组 |
| A7 权限与用户 | [`sudo`](#sudo-用-root-权限跑一条命令) | 用 root 权限跑一条命令 |
| A8 进程与作业 | [`ps`](#ps-看这个终端里在跑什么) | 看这个终端里在跑什么 |
| A8 进程与作业 | [`ps -ef / ps aux`](#ps--ef--ps-aux-看整台机器上的所有进程) | 看整台机器上的所有进程 |
| A8 进程与作业 | [`pgrep`](#pgrep-按名字查进程的-pid) | 按名字查进程的 PID |
| A8 进程与作业 | [`top`](#top-动态看谁在吃-cpu--内存) | 动态看谁在吃 CPU / 内存 |
| A8 进程与作业 | [`kill`](#kill-结束一个进程) | 结束一个进程 |
| A8 进程与作业 | [`sleep`](#sleep-等一会儿暂停-n-秒) | 等一会儿（暂停 N 秒） |
| A8 进程与作业 | [`命令 &  ｜  jobs / fg`](#命令-----jobs--fg-放到后台跑--把后台作业拉回来) | 放到后台跑 / 把后台作业拉回来 |
| A8 进程与作业 | [`nohup`](#nohup-关掉终端也别停后台长任务) | 关掉终端也别停（后台长任务） |
| A9 网络与远程 | [`ip a`](#ip-a-看网卡和-ip-地址) | 看网卡和 IP 地址 |
| A9 网络与远程 | [`ip -o -4 addr show`](#ip--o--4-addr-show-一行一个地址机器好读的格式) | 一行一个地址（机器好读的格式） |
| A9 网络与远程 | [`ss -tln`](#ss--tln-看谁在监听端口本机开了哪些服务) | 看谁在监听端口（本机开了哪些服务） |
| A9 网络与远程 | [`ping`](#ping-测通不通发-icmp-包) | 测「通不通」（发 ICMP 包） |
| A9 网络与远程 | [`curl`](#curl-抓网页--调接口发-http-请求) | 抓网页 / 调接口（发 HTTP 请求） |
| A9 网络与远程 | [`wget`](#wget-下载文件到当前目录) | 下载文件到当前目录 |
| A9 网络与远程 | [`nc -zv`](#nc--zv-测某个端口开没开) | 测某个端口开没开 |
| A9 网络与远程 | [`ssh`](#ssh-登录远程主机) | 登录远程主机 |
| A9 网络与远程 | [`scp`](#scp-在本地和远程之间复制文件) | 在本地和远程之间复制文件 |
| A10 压缩与打包 | [`tar -czf`](#tar--czf-把目录文件打包成-targz) | 把目录/文件打包成 .tar.gz |
| A10 压缩与打包 | [`tar -tzf`](#tar--tzf-看一眼压缩包里有什么不解开) | 看一眼压缩包里有什么（不解开） |
| A10 压缩与打包 | [`tar -xzf`](#tar--xzf-解包解开-targz) | 解包（解开 .tar.gz） |
| A10 压缩与打包 | [`gzip / gunzip`](#gzip--gunzip-压缩单个文件不是打包目录) | 压缩单个文件（不是打包目录） |
| A10 压缩与打包 | [`zip / unzip`](#zip--unzip-跨平台压缩包给-windows-用) | 跨平台压缩包（给 Windows 用） |
| A11 系统信息与软件包 | [`cat /etc/os-release`](#cat-etcos-release-我在什么系统上发行版与版本) | 我在什么系统上（发行版与版本） |
| A11 系统信息与软件包 | [`uname -a`](#uname--a-看内核版本和机器架构) | 看内核版本和机器架构 |
| A11 系统信息与软件包 | [`df -h`](#df--h-看磁盘还剩多少空间) | 看磁盘还剩多少空间 |
| A11 系统信息与软件包 | [`du -sh`](#du--sh-看某个目录占了多少空间) | 看某个目录占了多少空间 |
| A11 系统信息与软件包 | [`free -h`](#free--h-看内存和-swap-使用情况) | 看内存和 swap 使用情况 |
| A11 系统信息与软件包 | [`echo $PATH`](#echo-path-命令是从哪些目录里找的) | 命令是从哪些目录里找的 |
| A11 系统信息与软件包 | [`export / alias`](#export--alias-临时设环境变量--造命令别名) | 临时设环境变量 / 造命令别名 |
| A11 系统信息与软件包 | [`apt`](#apt-装--卸软件debianubuntukali-系) | 装 / 卸软件（Debian、Ubuntu、Kali 系） |

---

## A1 终端与命令

### `echo` 打印一行字（最简单的命令）

**签名** `echo 内容...` ｜ **返回** 把内容原样打印到屏幕（标准输出） ｜ **备注** 用来试终端是否正常、在脚本里输出提示；`echo $变量` 可以直接看变量的值

```bash
echo hello linux
echo "引号里的    多个空格也会保留"
echo $HOME
```

```text
hello linux
引号里的    多个空格也会保留
/root
```

> ⚠️ 不加引号时多个空格会被压成一个；`$HOME` 这种 `$` 开头的会被**先替换成变量的值**再打印（这叫变量展开）。

### `命令 --help` 看命令自带的用法说明

**签名** `<命令> --help` ｜ **返回** 把该命令的用法和所有选项打印出来（很长，可配 `| head` 只看开头，见 A6） ｜ **备注** 新手最有用的一条规则：忘了怎么用就 `命令 --help`，比背笔记靠谱 —— 版本一变选项也会变

```bash
ls --help | head -n 5
```

```text
Usage: ls [OPTION]... [FILE]...
List information about the FILEs (the current directory by default).
Sort entries alphabetically if none of -cftuvSUX nor --sort is specified.

Mandatory arguments to long options are mandatory for short options too.
```

> ⚠️ 少数命令只认 `-h`；`echo`、`cd` 这种是 shell 内建命令，没有 `--help`。两种都试一下。

### `man` 看完整的手册页（比 --help 详细）

**签名** `man <命令>` ｜ **返回** 进入分页阅读器：`↑↓` / 空格翻页、`/关键词` 搜索、`q` 退出 ｜ **备注** 选项的完整解释、返回值、相关文件都在这里；`man man` 是 man 自己的说明书

```bash
man ls
```

```text
（未实跑：man 需要交互式终端，校验容器里也没装 man-db。先记住三个键：空格翻页、`/` 搜索、`q` 退出）
```

### `命令 --version` 看这个命令的版本

**签名** `<命令> --version` ｜ **返回** 打印版本号与版权信息，通常看第一行就够 ｜ **备注** 出错求助时先把版本贴上去；不同版本行为可能不同（GNU 的 `ls` 和 macOS 的 `ls` 就不一样）

```bash
ls --version | head -n 1
```

```text
ls (GNU coreutils) 9.4
```

> ⚠️ 多数 Linux 命令来自 GNU 项目，macOS 用的是 BSD 版：**同名命令、选项和行为可能不同**（本笔记会在 ⚠️ 里点出来）。

## A2 目录与路径

### `pwd` 我现在在哪个目录

**签名** `pwd` ｜ **返回** 打印当前目录的完整路径（以 `/` 开头的叫绝对路径） ｜ **备注** 迷路时的第一条命令；`cd` 之后想确认自己在哪也用它

```bash
pwd
cd dir1
pwd
```

```text
/root/linux-lab
/root/linux-lab/dir1
```

> ⚠️ 你机器上显示的是你自己的家目录，比如 `/home/kali/linux-lab`；示例里是容器里的 `/root/linux-lab`。

### `ls` 看这个目录里有什么

**签名** `ls [选项] [目录]` ｜ **返回** 把目录里的名字按字母序打印成一列（默认不含隐藏文件，也不给详细信息） ｜ **备注** 最常用的命令，什么都不改；`ls /etc` 可以看别的目录

```bash
ls
ls dir1
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

> ⚠️ 目录为空时 `ls` **什么都不打印**，这不代表出错（`dir1` 就是空的）。

### `ls -a` 连隐藏文件一起列出来

**签名** `ls -a [目录]` ｜ **返回** 列出所有条目：包括 `.`（当前目录）、`..`（上一级）和以 `.` 开头的隐藏文件 ｜ **备注** Linux 里**名字以 `.` 开头就是隐藏文件**，`ls` 默认不显示；配置文件大多是隐藏文件

```bash
touch .secret.txt
ls
ls -a
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

> ⚠️ 别被输出里的 `.` 和 `..` 弄晕：每个目录里都有这两个特殊条目，它们就是「当前目录」和「上一级目录」。

### `ls -l` 长格式：看权限、属主、大小、时间

**签名** `ls -l [目录]` ｜ **返回** 一行一个条目，从左到右 7 列：权限、硬链接数、属主、属组、大小（字节）、修改时间、名字 ｜ **备注** 想知道「这文件谁能改、多大、什么时候动过」就用它；第 1 列权限怎么读见 A7

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

> ⚠️ 时间列是**修改时间**；示例里被固定成 2026-01-01（为了让输出稳定、可校验），你机器上是真实时间。

### `ls -lh` 大小变成 4.0K 这种好读的写法

**签名** `ls -lh [目录]` ｜ **返回** 和 `ls -l` 一样，只是大小那一列用 K / M / G 显示 ｜ **备注** `-h` 是 human readable 的意思；看文件大小、磁盘占用时用 `-lh` 比 `-l` 舒服

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

> ⚠️ 选项可以叠着写：`-lh` 就是 `-l -h`（Linux 命令的通用习惯，如 `tar -xzf`、`ls -la`）。

### `ls -lt` 按修改时间排，最新的在最上面

**签名** `ls -lt [目录]` ｜ **返回** 同 `ls -l`，但按修改时间从新到旧排序 ｜ **备注** 想知道「刚改了哪个文件」就用它；`ls -ltr` 反过来（最旧的先显示），看日志时常用

```bash
touch -t 202602020900 newer.txt
ls -lt
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

> ⚠️ 修改时间完全相同时，`ls` 会按名字排序，所以输出是稳定的。

### `cd` 进到某个目录里

**签名** `cd <目录>` ｜ **返回** 什么都不打印（成功时没有输出），但你的「当前位置」变了 ｜ **备注** 目录必须存在；路径可以写相对的（`dir1`）也可以写绝对的（`/etc`）

```bash
pwd
cd dir1
pwd
cd /etc
pwd
```

```text
/root/linux-lab
/root/linux-lab/dir1
/etc
```

> ⚠️ `cd` 写错的两种报错：目录不存在 → `No such file or directory`；写成了文件 → `Not a directory`。

### `cd .. / cd ~ / cd -` 三个最常用的「跳回去」

**签名** `cd ..`（上一级） / `cd ~`（家目录） / `cd -`（回上一个待过的目录） ｜ **返回** 都只改变当前位置，不打印东西（只有 `cd -` 会把目标路径打印出来） ｜ **备注** `..` 是上一级、`~` 是家目录、`-` 是「刚才那个目录」，两个目录之间来回切特别方便

```bash
cd dir1      # 进 dir1
cd ..        # 回上一级
pwd          # 确认回来了
cd /etc
cd -         # 回上一次待过的目录（cd - 会把它打印出来）
cd           # 不带参数 = 回家目录
pwd
```

```text
/root/linux-lab
/root/linux-lab
/root
```

> ⚠️ 只有 `cd -` 会打印路径，其他形式都是安静的 —— 在脚本里要注意这一点。

### `mkdir` 新建目录

**签名** `mkdir <目录名>` / `mkdir -p a/b/c` ｜ **返回** 不打印任何东西，目录直接出现在文件系统里 ｜ **备注** `-p` = parents：父目录不存在时一起建出来；不加 `-p` 而父目录不存在会报错

```bash
mkdir newdir
mkdir -p a/b/c
find . -type d | sort
```

```text
.
./a
./a/b
./a/b/c
./dir1
./dir2
./newdir
```

> ⚠️ 目录已存在时会报 `File exists`；这不是错，通常忽略即可。

### `tree` 树形看目录结构（一眼看懂层级）

**签名** `tree [目录]` / `tree -L 2`（只看两层） ｜ **返回** 把目录画成树，最后一行给出目录数与文件数 ｜ **备注** 比 `ls -R` 好读；项目目录层级多时特别有用。要装：Ubuntu/Kali 上 `sudo apt install tree`

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

**签名** `touch <文件名>...` ｜ **返回** 文件不存在就创建一个 0 字节的空文件；已存在就把修改时间更新成现在 ｜ **备注** 需要临时占位文件时最方便；配合通配符还能批量刷时间：`touch *.txt`

```bash
touch newfile.txt
ls -1 *.txt
```

```text
empty.txt
fruit.txt
hello.txt
newfile.txt
notes.txt
```

> ⚠️ 它不检查文件内容，也不报「文件已存在」；改的是时间戳，不是内容。

### `cp` 复制文件

**签名** `cp <源> <目标>` ｜ **返回** 不打印任何东西，目标处出现一份内容相同的副本 ｜ **备注** 目标已存在会**直接覆盖**；想被问一次就加 `-i`；复制目录必须加 `-r`（下一条）

```bash
cp hello.txt copy.txt
ls -1 *.txt
cat copy.txt
```

```text
copy.txt
empty.txt
fruit.txt
hello.txt
notes.txt
hello linux
second line
third line
```

> ⚠️ 不加 `-r` 复制目录会报 `omitting directory 'dir1'`（它默认不递归）。

### `cp -r` 复制整个目录（含里面的东西）

**签名** `cp -r <源目录> <目标目录>` ｜ **返回** 不打印任何东西，目标目录被整棵复制出来 ｜ **备注** `-r` = recursive，递归复制；想连权限、时间一起保留用 `-a`（archive）

```bash
cp -r dir1 dir1-copy
find . -maxdepth 1 -type d | sort
```

```text
.
./dir1
./dir1-copy
./dir2
```

> ⚠️ `cp -r 源 目标`：目标不存在就新建，目标已存在会把源目录**塞进目标里面**（变成 `目标/源/...`），这点很容易搞错。

### `mv` 移动文件 / 给文件改名

**签名** `mv <源> <目标>` ｜ **返回** 不打印任何东西；同一个目录里就是改名，跨目录就是移动 ｜ **备注** 改名/移动都是它；目标已存在会**静默覆盖**

```bash
mv empty.txt renamed.txt
ls -1 *.txt
```

```text
fruit.txt
hello.txt
notes.txt
renamed.txt
```

> ⚠️ `mv` 覆盖目标文件时**不提示、不备份**（要提示加 `-i`，要防覆盖加 `-n`）—— 这是最常见的误伤之一。

### `rm` 删文件

**签名** `rm <文件名>...` ｜ **返回** 不打印任何东西（成功时）；文件被删除 ｜ **备注** `-i` 删之前问一次；`-f` 强制（不存在也不报错）；删**目录**要用 `-r`（下一条）

```bash
rm empty.txt
ls -1 *.txt
```

```text
fruit.txt
hello.txt
notes.txt
```

> ⚠️ **没有回收站**：删了就是删了。养成习惯：删之前先 `ls` 看一眼要删的东西。

### `rm -r / rm -rf` 删目录（危险命令）

**签名** `rm -r <目录>` / `rm -rf <目录>` ｜ **返回** 不打印任何东西；目录连同里面的所有东西一起消失 ｜ **备注** `-r` 递归删目录、`-f` 不提示且忽略不存在的文件；`rm -rf` 是最常被滥用的组合

```bash
cp -r dir1 dir1-copy
rm -r dir1-copy
find . -maxdepth 1 -type d | sort
```

```text
.
./dir1
./dir2
```

> ⚠️ `rm -rf /`、`rm -rf ~` 能直接毁掉系统，**永远不要**复制来路不明的这种命令。脚本里删变量路径要加保护：`rm -rf "${DIR:?}"/`，变量为空时 `${DIR:?}` 会直接报错退出，避免变成 `rm -rf /`。

### `ln -s` 建软链接（快捷方式）

**签名** `ln -s <真实文件> <链接名>` ｜ **返回** 不打印任何东西，多出一个指向原文件的「快捷方式」 ｜ **备注** 软链接只是个指针：改动链接内容=改动原文件；`-s` 不能省，否则建的是硬链接（另一种东西）

```bash
ln -s hello.txt link.txt
stat -c '%N' link.txt
cat link.txt
readlink link.txt
```

```text
'link.txt' -> 'hello.txt'
hello linux
second line
third line
hello.txt
```

> ⚠️ 原文件被删掉后链接会「断」：`cat` 会报 `No such file or directory`，但链接本身还在（`ls -l` 里会显示成红色）。

### `stat` 看文件的各种详细信息

**签名** `stat <文件>` / `stat -c '<格式>' <文件>` ｜ **返回** 默认打印一大段元数据（权限、大小、三个时间）；加了 `-c` 就按你的格式输出 ｜ **备注** 想知道权限的数字写法（644 这种）用 `stat -c '%a %n'`；`%s` 大小、`%U` 属主、`%y` 修改时间

```bash
stat -c '%a %U %G %s %n' hello.txt
```

```text
644 root root 35 hello.txt
```

> ⚠️ `-c` 是 GNU 的写法；macOS 的 `stat` 要用 `-f`，格式字母也不同（`%Sp %Su %z`）。

## A4 看文件内容

### `cat` 把文件内容整个打印出来

**签名** `cat <文件>...` ｜ **返回** 按顺序打印文件内容；给多个文件就前后拼起来打印 ｜ **备注** 小文件最快；大文件别用它（会刷屏很久），用 `less` 或 `head`

```bash
cat hello.txt
cat hello.txt notes.txt
```

```text
hello linux
second line
third line
hello linux
second line
third line
login ok
login failed
login ok
```

> ⚠️ `cat` 只能看**文本**文件，看二进制（图片、可执行文件）会刷出乱七八糟的乱码，还可能弄坏终端（这时敲 `reset`）。

### `less` 分页看大文件（可以上下翻、搜索）

**签名** `less <文件>` ｜ **返回** 进入分页阅读器：空格/`PgDn` 下翻、`b` 上翻、`/词` 搜索、`n` 下一个、`q` 退出 ｜ **备注** 看日志、看长配置文件的标配；它不会一次把文件读进内存，所以多大都能开

```bash
less hello.txt
```

```text
（未实跑：less 需要交互式终端。三个必记键：空格翻页、`/` 搜索、`q` 退出）
```

### `head` 只看开头几行

**签名** `head -n <行数> <文件>` ｜ **返回** 打印文件的前 N 行（默认前 10 行） ｜ **备注** 看文件格式/表头时用它；`head -c 100 f` 看前 100 个字节

```bash
head -n 2 notes.txt
```

```text
login ok
login failed
```

> ⚠️ `head -n -2 f` 是 GNU 的玩法（除最后两行都打印），换到 macOS 的 BSD `head` 就用不了。

### `tail` 只看结尾几行（盯日志常用）

**签名** `tail -n <行数> <文件>` / `tail -f <文件>` ｜ **返回** 打印文件最后 N 行（默认最后 10 行）；`-f` 会一直盯着文件，新写入的行实时显示 ｜ **备注** 被用得最多的组合是 `tail -f /var/log/syslog`：一边操作、一边看日志滚出来（`Ctrl+C` 停）

```bash
tail -n 2 notes.txt
```

```text
login failed
login ok
```

> ⚠️ `tail -f` 会**一直挂着不退出**，这是正常现象，用 `Ctrl+C` 停；想边看边过滤就 `tail -f 日志 | grep 关键词`（A6）。

### `wc` 数行数 / 单词数 / 字节数

**签名** `wc [-l] [-w] [-c] [文件]` ｜ **返回** 默认打印 行数 单词数 字节数 文件名；加 `-l` 只要行数 ｜ **备注** `wc -l` 是日常最常用的一个：数日志有多少行、数命令输出有多少条

```bash
wc -l notes.txt
wc -l -w -c hello.txt
ls | wc -l
```

```text
3 notes.txt
 3  6 35 hello.txt
8
```

> ⚠️ 最后一行没有换行符时 `wc -l` 会**少算一行**（它数的是换行符个数）：`printf 'a' | wc -l` 得 0。

### `nl / cat -n` 带行号打印（方便讨论“第几行”）

**签名** `nl <文件>` / `cat -n <文件>` ｜ **返回** 每一行前面加上行号再打印（`nl` 默认不给空行编号，`cat -n` 会给空行也编号） ｜ **备注** 报错信息里的「第几行」就是这么对上的；`nl -ba` 让空行也带编号

```bash
nl hello.txt
cat -n hello.txt
```

```text
     1	hello linux
     2	second line
     3	third line
     1	hello linux
     2	second line
     3	third line
```

> ⚠️ 行号是**打印出来的装饰**，文件内容里并没有；不要拿行号去写进文件。

### `diff` 比较两个文件哪里不一样

**签名** `diff <文件1> <文件2>` ｜ **返回** 不同的地方按 `<`（左边文件）/ `>`（右边文件）打印出来；**完全相同时什么都不打印** ｜ **备注** 改配置文件前后对比、看别人改了什么，全靠它；看目录差异用 `diff -r 目录1 目录2`

```bash
cp hello.txt same.txt
printf 'hello linux\nsecond line\nCHANGED\n' > other.txt
diff hello.txt same.txt
diff hello.txt other.txt
```

```text
3c3
< third line
---
> CHANGED
```

> ⚠️ `diff` 有差异时**退出码是 1**（相同是 0），在脚本里常写 `diff a b || echo 有差异`；想只看「有没有差异」用 `diff -q`。

## A5 查找与搜索

### `find . -name` 按名字找文件（会钻进所有子目录）

**签名** `find <起点目录> -name '<模式>'` ｜ **返回** 打印所有匹配的**路径**（含目录前缀），没找到就什么都不打印 ｜ **备注** `*` 是通配符（任意多个字符）、`?` 是一个字符；找不到东西时第一反应就是它

```bash
find . -name '*.txt' | sort
```

```text
./empty.txt
./fruit.txt
./hello.txt
./notes.txt
```

> ⚠️ 模式**必须加引号**：写成 `find . -name *.txt`，shell 会先把 `*.txt` 展开成一堆文件名再交给 find，直接报 `find: paths must precede expression`。

### `find . -type` 按类型找（只要文件 / 只要目录）

**签名** `find <起点> -type f` / `-type d` ｜ **返回** 打印匹配的路径，`f` = 普通文件、`d` = 目录、`l` = 软链接 ｜ **备注** 还能按大小 `-size +1M`、按修改时间 `-mtime -1`（一天内改过）、只看本层 `-maxdepth 1`

```bash
find . -type d | sort
find . -type f -name '*.csv'
```

```text
.
./dir1
./dir2
./data.csv
```

> ⚠️ `-maxdepth` 要写在**其他条件之前**，放后面 GNU 会警告（位置写错是 find 最常见的坑）。

### `grep` 在文件里找包含某个词的行

**签名** `grep '<模式>' <文件>...` ｜ **返回** 打印**匹配到的整行**；一行都没有时什么都不打印 ｜ **备注** 这是最常用的文本搜索命令：`grep 关键词 日志文件`；模式里可以用正则（`^词` 行首、`词$` 行尾）

```bash
grep ok notes.txt
```

```text
login ok
login ok
```

> ⚠️ 退出码有意义：0 = 找到了、1 = 一行都没匹配、2 = 出错（比如文件不存在）。脚本里用 `grep -q 词 文件` 只看成败、不要输出。

### `grep -n / -i` 显示行号 / 忽略大小写

**签名** `grep -n '<模式>' <文件>` / `grep -i '<模式>' <文件>` ｜ **返回** `-n` 在每行前面加上它在文件里的行号；`-i` 让匹配不区分大小写 ｜ **备注** 报错信息给出行号时，用 `-n` 定位特别快；`-i` 适合记不清大小写的时候

```bash
grep -n failed notes.txt
grep -i LOGIN notes.txt
```

```text
2:login failed
login ok
login failed
login ok
```

### `grep -c / -v` 只数数量 / 看没匹配上的行

**签名** `grep -c '<模式>' <文件>` / `grep -v '<模式>' <文件>` ｜ **返回** `-c` 只打印匹配的**行数**；`-v` 反过来，打印**不**匹配的行 ｜ **备注** 统计日志里出现了几次用 `-c`；排除注释、排除库文件用 `-v`

```bash
grep -c ok notes.txt
grep -v ok notes.txt
```

```text
2
login failed
```

### `grep -r` 在整个目录里递归搜索

**签名** `grep -rn '<模式>' <目录>` ｜ **返回** 从目录开始递归找所有文件，`-n` 带上行号，输出形如 `路径:行号:内容` ｜ **备注** 「这个字符串在项目里哪儿用过」的答案；`-l` 只列文件名不列内容（`grep -rl 词 .`）

```bash
grep -rn hello . | sort
```

```text
./hello.txt:1:hello linux
```

> ⚠️ 递归会连 `.git`、`node_modules`、日志一起搜，又慢又乱：用 `--include='*.py'` 限定文件、`--exclude-dir=.git` 排除目录。

### `which / command -v / type` 这个命令到底是哪个程序

**签名** `which <命令>` / `command -v <命令>` / `type <命令>` ｜ **返回** 打印这个命令对应的可执行文件路径；`type` 还会告诉你它是内建命令、别名还是外部程序 ｜ **备注** 命令「找不到」时用它排查：是没装？还是 PATH 里没有？还是被别名顶掉了？

```bash
which ls
command -v bash
type ls
type cd
```

```text
/usr/bin/ls
/usr/bin/bash
ls is /usr/bin/ls
cd is a shell builtin
```

> ⚠️ `which` 只找外部程序，对内建命令（`cd`、`echo`）会「查无此人」；`command -v` 是更标准的写法。

## A6 管道、重定向与文本处理

### `命令 > 文件` 把输出写进文件（覆盖）

**签名** `<命令> > <文件>` ｜ **返回** 屏幕上看不到输出了，内容都进了文件；文件不存在就新建 ｜ **备注** `>` 会把文件**原来的内容全部清掉**再写，所以别拿它往重要文件里写

```bash
echo "第一行" > out.txt
cat out.txt
```

```text
第一行
```

> ⚠️ `> 文件` 哪怕命令最后什么都没输出，也会先把文件清空 —— 这是常见的数据丢失原因（想追加用 `>>`）。

### `命令 >> 文件` 把输出追加到文件末尾

**签名** `<命令> >> <文件>` ｜ **返回** 内屏上没有输出，内容追加到文件最后（原内容保留） ｜ **备注** 写日志、往配置末尾加一行都用它

```bash
echo "第一行" > out.txt
echo "第二行" >> out.txt
cat out.txt
```

```text
第一行
第二行
```

### `命令 2> 文件` 只把报错信息接进文件

**签名** `<命令> 2> <文件>` ｜ **返回** 正常输出还在屏幕上，只有报错（标准错误，编号 2）被写进文件 ｜ **备注** 术语记一下：标准输出是 1、标准错误是 2；不带编号的 `>` 只管 1

```bash
ls no-such-file 2> err.txt
cat err.txt
```

```text
ls: cannot access 'no-such-file': No such file or directory
```

> ⚠️ `ls` 报错后退出码是 2（非 0）—— 这是「命令失败」的正常表现，不是你写错了。

### `命令 > 文件 2>&1` 正常输出和报错都接进同一个文件

**签名** `<命令> > <文件> 2>&1` ｜ **返回** 两类输出一起进文件，屏幕上一片安静 ｜ **备注** `2>&1` 的意思是「把 2 指向 1 现在指向的地方」；写日志、排查问题时最常用

```bash
ls no-such-file > all.txt 2>&1
cat all.txt
```

```text
ls: cannot access 'no-such-file': No such file or directory
```

> ⚠️ **顺序不能反**：`2>&1 > 文件` 里的 `2>&1` 在 `>` 之前生效，那时 1 还指着屏幕，结果只有正常输出进文件、报错依旧打印在屏幕上。

### `命令1 ｜ 命令2` 管道：把上一条的输出当输入

**签名** `<命令1> | <命令2>` ｜ **返回** 命令1 的标准输出变成命令2 的输入，屏幕上只出现命令2 的输出 ｜ **备注** Linux 的招牌玩法：`命令A | 命令B | 命令C` 串起来，一步一个动作地处理数据

```bash
ls -1 | wc -l
grep ok notes.txt | wc -l
sort fruit.txt | head -n 2
```

```text
8
2
apple 3
banana 5
```

> ⚠️ 管道只接标准输出（1），**报错不走管道**（还在屏幕）；要让报错也进管道就写 `命令 2>&1 | 下一条`。

### `tee` 又打印到屏幕、又存进文件

**签名** `<命令> | tee <文件>` / `tee -a <文件>`（追加） ｜ **返回** 屏幕上照常显示，同时把内容写进文件 ｜ **备注** 调试管道时用它：既能看见中间结果，又留一份存档；`-a` 追加，不加就覆盖

```bash
echo "第四行" | tee -a hello.txt
tail -n 1 hello.txt
```

```text
第四行
第四行
```

### `sort` 排序

**签名** `sort [选项] [文件]` ｜ **返回** 把输入按行排序后打印（不改原文件） ｜ **备注** `-n` 按数字大小、`-r` 倒序、`-k2` 按第 2 列、`-u` 去重；默认是**字典序**，所以 10 会排在 9 前面

```bash
sort fruit.txt
sort -k2 -n fruit.txt
printf '9\n10\n' | sort
```

```text
apple 3
banana 5
cherry 7
apple 3
banana 5
cherry 7
10
9
```

> ⚠️ 默认字典序会把 `10` 排在 `9` 前面；带数字的列要加 `-n`（或 `-h` 处理 1K/2M 这种）。

### `uniq -c` 数一数每行重复出现了几次

**签名** `sort <文件> | uniq -c` ｜ **返回** 打印「次数 内容」，相同的行被合并成一条 ｜ **备注** 统计日志里哪个 IP / 哪个错误出现最多，就靠它；常配 `sort -nr` 按次数排序看 Top 10

```bash
sort notes.txt | uniq -c
```

```text
      1 login failed
      2 login ok
```

> ⚠️ `uniq` 只合并**相邻**的重复行，所以几乎总要先 `sort`；不排序直接用 `uniq` 会得到「没去重」的假象。

### `cut` 按分隔符取某一列

**签名** `cut -d'<分隔符>' -f<列号> <文件>` ｜ **返回** 打印指定列的内容（默认分隔符是 Tab） ｜ **备注** `-d,` 逗号分隔（CSV）、`-d:` 冒号分隔（/etc/passwd）、`-f1,3` 要两列、`-f2-` 从第 2 列到末尾

```bash
cut -d, -f1 data.csv
cut -d, -f2 data.csv
```

```text
name
tom
amy
age
18
20
```

> ⚠️ `cut` 只能按**单个字符**分隔，多空格对齐的（比如 `ps` 的输出）用 `awk` 更好。

### `sed 's/旧/新/'` 替换文本（默认只改输出，不改文件）

**签名** `sed 's/旧/新/[g]' <文件>` / `sed -i 's/旧/新/g' <文件>` ｜ **返回** 把替换后的内容打印出来；不加 `-i` 时**原文件一点都不变** ｜ **备注** `g` = 一行里所有出现都换（不加只换每行第一个）；`-i` 才真改文件，改前先备份

```bash
sed 's/ok/OK/g' notes.txt
```

```text
login OK
login failed
login OK
```

> ⚠️ `-i` 是真改文件、没有撤销：先用不带 `-i` 的版本看一眼结果，确认无误再加 `-i`（macOS 的 `sed -i` 还要求跟一个备份后缀，如 `sed -i '' 's/a/b/'`）。

### `awk '{print $2}'` 取列 / 做简单计算（文本处理万能工具）

**签名** `awk [-F'<分隔符>'] '{print $<列号>}' <文件>` ｜ **返回** 按列处理每一行再打印；默认按空格/Tab 分列，`$1` 是第一列、`$0` 是整行 ｜ **备注** `awk -F, '{print $2}'` 取 CSV 第 2 列；`awk '{s+=$2} END{print s}'` 求和；统计日志特别常用

```bash
awk -F, '{print $2}' data.csv
awk '{s+=$2} END{print s}' fruit.txt
```

```text
age
18
20
15
```

> ⚠️ `cut` 搞不定的（多个空格、条件判断、求和）交给他。它是「一门小语言」，不用全学，先会用 `print $n` 和求和。

### `xargs` 把上一条的输出变成下一条的参数

**签名** `<命令1> | xargs <命令2>` ｜ **返回** 把前一条输出的每个「词」当成参数，接到命令2 后面去执行 ｜ **备注** 很多命令不读管道输入、只认参数（`rm`、`cp`、`wc`），这时就用 `find ... | xargs rm` 这种写法

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

### `chmod +x` 给文件加/减权限（符号写法）

**签名** `chmod [u|g|o|a][+|-|=][r|w|x] <文件>` ｜ **返回** 不打印任何东西，文件的权限位被改掉 ｜ **备注** 三个字母：`u` 自己（user）、`g` 同组（group）、`o` 其他人（other）、`a` 所有人；`+` 加、`-` 减、`=` 设为

```bash
chmod -x run.sh
ls -l run.sh
chmod +x run.sh
ls -l run.sh
```

```text
-rw-r--r-- 1 root root 34 Jan  1  2026 run.sh
-rwxr-xr-x 1 root root 34 Jan  1  2026 run.sh
```

> ⚠️ 脚本报 `Permission denied` 但文件明明在，八成是少了 `x`：`chmod +x 脚本.sh` 就好。

### `chmod 644 / 755` 给文件设权限（数字写法，最常见）

**签名** `chmod <三位数字> <文件>` ｜ **返回** 不打印任何东西；权限位被设成对应数字 ｜ **备注** 数字怎么读：r(读)=4、w(写)=2、x(执行)=1，三个数字依次是「自己/同组/其他人」，各位把要给的加起来。644 = rw-r--r--、755 = rwxr-xr-x、600 = 只有自己能读写

```bash
chmod 644 hello.txt
chmod 755 run.sh
stat -c '%a %n' hello.txt run.sh
```

```text
644 hello.txt
755 run.sh
```

> ⚠️ `chmod 777`（所有人都能读改删）是最糟的权限，安全上别用；日常：普通文件 644、要执行的脚本和目录 755。

### `chmod -R` 递归改一个目录里所有东西的权限

**签名** `chmod -R <权限> <目录>` ｜ **返回** 不打印任何东西；目录本身和里面所有文件都被改 ｜ **备注** `-R` = recursive；目录的 `x` 位很关键：**没有 x 就进不去**这个目录（连 `ls` 都会报 Permission denied）

```bash
mkdir -p perm/sub
printf 'x\n' > perm/sub/file.txt
chmod -R 700 perm
stat -c '%a %n' perm perm/sub perm/sub/file.txt
```

```text
700 perm
700 perm/sub
700 perm/sub/file.txt
```

> ⚠️ 文件和目录需要的权限不一样，一把梭的 `-R` 常出问题：更稳的写法是 `find 目录 -type d -exec chmod 755 {} +`、`find 目录 -type f -exec chmod 644 {} +` 分开设。

### `chown / chgrp` 改文件的属主 / 属组

**签名** `chown <用户>[:<组>] <文件>` / `chgrp <组> <文件>` ｜ **返回** 不打印任何东西，`ls -l` 第 3、4 列会变 ｜ **备注** 要 root 权限才能改（普通用户前面加 `sudo`）；`-R` 递归；用**数字的 uid/gid** 不会因为系统里没这个名字而报错

```bash
chown 1000 hello.txt
stat -c '%u %g %n' hello.txt
chown 1000:1000 hello.txt
stat -c '%u %g %n' hello.txt
```

```text
1000 0 hello.txt
1000 1000 hello.txt
```

> ⚠️ 网站报 403、服务读不到文件，很常见的原因就是属主不对（比如 root 建的文件，服务以 www-data 跑）。

### `umask` 看/改新建文件的默认权限

**签名** `umask` / `umask <三位数字>` ｜ **返回** 不带参数时打印当前掩码（如 0022）；带参数则改掉它，不打印东西 ｜ **备注** umask 是「新建时**不给**哪些权限」：022 → 新文件 644、新目录 755；077 → 新文件 600（只有自己能看）

```bash
umask
touch newfile.txt
stat -c '%a %n' newfile.txt
umask 077
touch private.txt
stat -c '%a %n' private.txt
```

```text
0022
644 newfile.txt
600 private.txt
```

> ⚠️ umask 只影响**之后新建**的文件，已存在的文件不受影响；想长期生效得写进 `~/.bashrc`。

### `whoami / id` 我是谁 / 我的 uid 和组

**签名** `whoami` / `id` / `groups` ｜ **返回** `whoami` 打印用户名；`id` 打印 uid、gid、所属组；`groups` 只列组 ｜ **备注** 在别人机器上先搞清楚自己是谁：很多命令能不能跑、文件能不能读，全看这个

```bash
whoami
id
```

```text
root
uid=0(root) gid=0(root) groups=0(root)
```

> ⚠️ 示例在容器里所以是 `root`；你自己机器上会是你的普通用户名。加了 `sudo` 之后 `whoami` 就变成 root。

### `sudo` 用 root 权限跑一条命令

**签名** `sudo <命令>` / `sudo -i`（进 root shell） ｜ **返回** 像平时一样执行那条命令，但以 root 身份；第一次会问**你自己的密码**（不是 root 的） ｜ **备注** 忘了加 sudo？`sudo !!` 用 root 重跑上一条；`sudo -l` 看你能 sudo 哪些命令

```bash
sudo apt update
```

```text
（未实跑：需要真实系统装了 sudo 并知道密码。别习惯性给所有命令加 sudo —— 它的破坏力也是 root 级的，先问自己「这条命令真的需要 root 吗」）
```

## A8 进程与作业

### `ps` 看这个终端里在跑什么

**签名** `ps` / `ps -e`（所有进程）/ `ps -ef`（所有 + 全格式） ｜ **返回** 打印一行一个进程，几列：PID（进程号）、TTY（哪个终端）、TIME（占了多少 CPU 时间）、CMD（命令） ｜ **备注** `PID` 是给 `kill` 用的编号；想过滤就用管道：`ps -ef | grep 关键词`（A6）

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

### `ps -ef / ps aux` 看整台机器上的所有进程

**签名** `ps -ef` / `ps aux` ｜ **返回** 列出所有用户的进程（不只你终端里的），`-f` 给全格式、`aux` 是 BSD 风格的另一种写法 ｜ **备注** 排查「什么在占内存/端口」的第一步；`ps -ef | grep nginx` 是最常敲的组合

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

**签名** `pgrep <名字>` / `pgrep -a <名字>`（连命令行一起显示） ｜ **返回** 打印匹配进程的 PID（一行一个）；`-c` 只给个数 ｜ **备注** 比 `ps -ef | grep` 省事（自动跳过 grep 自己）；`pkill 名字` 直接按名字结束进程

```bash
sleep 300 &
sleep 300 &
pgrep -c sleep
```

```text
2
```

> ⚠️ 名字是**模糊匹配**：`pgrep ssh` 会连 sshd、ssh-agent 一起匹配到。杀之前先 `pgrep -a` 看清楚。

### `top` 动态看谁在吃 CPU / 内存

**签名** `top` / `top -b -n 1`（拍一张快照） ｜ **返回** 交互式界面：上面是负载和内存，下面是按 CPU 排序的进程列表；`q` 退出、`M` 按内存排、`P` 按 CPU 排 ｜ **备注** `top -b -n 1` 是非交互的「拍照片」，适合往文件/管道里丢；想看彩色的装 `htop` 或 `btop`

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

**签名** `kill <PID>` / `kill -9 <PID>` ｜ **返回** 默认发信号 15（TERM）：请它自己退出（程序有机会保存和清理）；`-9` 是强杀（KILL），程序拦不住 ｜ **备注** `$!` 是「上一个后台进程的 PID」，`kill $!` 就是杀掉刚放到后台的那个

```bash
sleep 300 &
kill $!
wait $! 2>/dev/null
echo "退出码 $?"
```

```text
退出码 143
```

> ⚠️ 顺序是**先 `kill`、不行再 `kill -9`**：`-9` 不给程序收尾机会，可能留下写坏的文件。上面那个 `143` = 128 + 15（被 TERM 结束）。

### `sleep` 等一会儿（暂停 N 秒）

**签名** `sleep <秒数>` / `sleep 1m`、`sleep 2h` ｜ **返回** 什么都不打印，等够时间才继续（`sleep 0` 表示不睡） ｜ **备注** 脚本里等服务器/数据库起来时用；`sleep 0.5` 这种小数 GNU 版支持

```bash
sleep 2
echo "睡完了"
```

```text
睡完了
```

> ⚠️ 前台 `sleep` 会占住终端，等得不耐烦就 `Ctrl+C`；想让它后台睡就写 `sleep 300 &`。

### `命令 &  ｜  jobs / fg` 放到后台跑 / 把后台作业拉回来

**签名** `<命令> &` ｜ `jobs` ｜ `fg %1` ｜ `bg %1` ｜ **返回** 命令末尾加 `&` 立刻回到提示符（命令继续跑）；`jobs` 列出后台作业；`fg` 把作业拉回前台 ｜ **备注** `Ctrl+Z` 把正在跑的命令**挂起**（暂停），再用 `bg` 推到后台继续跑，是很常用的一招

```bash
sleep 300 & sleep 300 &
jobs
```

```text
[1]-  Running                 sleep 300 &
[2]+  Running                 sleep 300 &
```

> ⚠️ 后台进程的输出还是会打到你这个屏幕上（把终端搅乱）：一般配 `> 文件 2>&1` 或 `> /dev/null` 把输出接走。

### `nohup` 关掉终端也别停（后台长任务）

**签名** `nohup <命令> > <日志文件> 2>&1 &` ｜ **返回** 让命令忽略「终端挂断」信号，你退出 SSH 后它还继续跑；输出默认追加到 `nohup.out` ｜ **备注** 跑一次要几十分钟的扫描/爬虫时用；更好的替代是 `tmux`（推荐）或 `screen`，能随时回到那个窗口看

```bash
nohup sleep 300 > nohup.out 2>&1 &
jobs
cat nohup.out
```

```text
[1]+  Running                 nohup sleep 300 > nohup.out 2>&1 &
```

> ⚠️ 不带 `&` 的 `nohup 命令` 还是占着终端（只是不怕挂断）；要真后台，`nohup ... &` 两个一起写。

## A9 网络与远程

### `ip a` 看网卡和 IP 地址

**签名** `ip a` / `ip addr` ｜ **返回** 打印每张网卡的状态、MAC 地址和 IP：找 `inet` 那一行就是 IPv4 地址 ｜ **备注** `lo` 是本机回环（127.0.0.1，永远都在），`eth0` / `ens33` / `wlan0` 才是真实网卡；`ip r` 看默认网关和路由

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

### `ip -o -4 addr show` 一行一个地址（机器好读的格式）

**签名** `ip -o -4 addr show [网卡]` ｜ **返回** 把每张网卡的 IPv4 地址压成一行，便于 `awk` / `cut` 取字段 ｜ **备注** `-o` = one line、`-4` = 只要 IPv4；写脚本取 IP 用它，比解析 `ip a` 的输出容易

```bash
ip -o -4 addr show lo
```

```text
1: lo    inet 127.0.0.1/8 scope host lo\       valid_lft forever preferred_lft forever
```

> ⚠️ 输出里的空格数量会随 iproute2 版本略有差别，取字段用 `awk '{print $4}'` 比按位置切字符串稳。

### `ss -tln` 看谁在监听端口（本机开了哪些服务）

**签名** `ss -tln` / `ss -tlnp`（带进程） ｜ **返回** 列出所有处于 LISTEN 状态的 TCP 端口；`-p` 会多一列显示是哪个进程在听 ｜ **备注** `-t` TCP、`-u` UDP、`-l` 只听着的、`-n` 不解析域名（输出快、显示端口号）

```bash
ss -tln
```

```text
State Recv-Q Send-Q Local Address:Port Peer Address:Port
```

> ⚠️ 加 `-p` 需要 root 权限；老教程里的 `netstat -tlnp` 要装 `net-tools`，`ss` 才是现在的标准工具。

### `ping` 测「通不通」（发 ICMP 包）

**签名** `ping <主机或IP>` / `ping -c 3 <主机>` ｜ **返回** 每秒发一个包，打印往返时间；`-c 3` 表示只发 3 个就停 ｜ **备注** 排网络问题的第一步；`ping 域名` 顺便验证 DNS 解析通不通

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

### `curl` 抓网页 / 调接口（发 HTTP 请求）

**签名** `curl [-s| -i | -o 文件 | -X 方法 -d 数据] <URL>` ｜ **返回** 把响应的正文打到屏幕上；`-i` 连响应头一起看、`-o 文件` 存文件、`-X POST -d 'a=1'` 发 POST ｜ **备注** 测试 Web 服务、看接口返回、确认某个路径是不是 200，都用它；`curl -I URL` 只看响应头

```bash
(python3 -m http.server 8000 --directory . > /dev/null 2>&1 &)
sleep 1
curl -s http://127.0.0.1:8000/hello.txt
```

```text
hello linux
second line
third line
```

> ⚠️ 示例为了不依赖外网，先在本地起了一个测试服务器（第一行那句 `python3 -m http.server`）—— 真实使用时你直接写 `curl https://example.com` 就行。

### `wget` 下载文件到当前目录

**签名** `wget <URL>` / `wget -O <文件名> <URL>` ｜ **返回** 把文件下载到当前目录（curl 默认打到屏幕，wget 默认存文件） ｜ **备注** `-c` 断点续传（下大文件被中断后接着下）、`-O 名字` 另存为、`-q` 安静模式

```bash
(python3 -m http.server 8000 --directory . > /dev/null 2>&1 &)
sleep 1
wget -q -O - http://127.0.0.1:8000/fruit.txt
```

```text
apple 3
banana 5
cherry 7
```

> ⚠️ macOS **没有自带 wget**（只有 curl），要用得先 `brew install wget`；示例同样是在本地测试服务器上跑的。

### `nc -zv` 测某个端口开没开

**签名** `nc -zv <主机> <端口>` ｜ **返回** `-z` 只连不发数据、`-v` 显示结果：端口开着会打印 succeeded，没开就报错 ｜ **备注** 比 ping 更有用：很多服务器禁 ICMP（ping 不通），但服务其实是好的；测服务要用端口测

```bash
nc -zv 127.0.0.1 22 2>&1
```

```text
nc: connect to 127.0.0.1 port 22 (tcp) failed: Connection refused
```

> ⚠️ 两种报错要分清：`Connection refused` = 连到了主机但这个端口没人听；`timed out` = 根本没连上（网络不通或被防火墙丢包）。

### `ssh` 登录远程主机

**签名** `ssh <用户>@<主机>` / `ssh -p <端口> <用户>@<主机>` ｜ **返回** 连上后就在对方的 shell 里操作了（`exit` 退出）；`ssh 主机 命令` 可以直接跑一条命令就断开 ｜ **备注** 第一次连会问 `yes/no`（确认主机指纹，之后记在 `~/.ssh/known_hosts`）；`-i 私钥文件` 指定密钥、`-p 2222` 换端口

```bash
ssh user@example.com
```

```text
（未实跑：需要一台真实的远程主机。三种常见报错：`Permission denied (publickey)` = 密钥/用户名不对；`Connection refused` = 对方没开 sshd 或端口不对；`Host key verification failed` = 主机指纹变了）
```

### `scp` 在本地和远程之间复制文件

**签名** `scp <本地文件> <用户>@<主机>:<远程路径>` / `scp -r <用户>@<主机>:<远程目录> .` ｜ **返回** 把文件传过去/拉回来，显示进度；`-r` 传整个目录；末尾的 `.` 表示「当前的本地目录」 ｜ **备注** 写法是「谁在前谁就是源」：`scp 源 目标`；端口要写成大写 `-P 2222`（和 ssh 的 `-p` 不同，容易记错）

```bash
scp report.txt kali@192.168.1.10:/tmp/
```

```text
（未实跑：需要真实主机。OpenSSH 官方现在更推荐 `sftp` 或 `rsync -av`，但简单传文件 `scp` 还是最顺手）
```

## A10 压缩与打包

### `tar -czf` 把目录/文件打包成 .tar.gz

**签名** `tar -czf <包名.tar.gz> <要打包的东西...>` ｜ **返回** 不打印任何东西（加 `-v` 会边打边列出文件），当前目录多出一个压缩包 ｜ **备注** 四个字母记法：`c` 创建、`z` 用 gzip 压缩、`f` 指定文件名（`f` 后面必须紧跟包名，而且一般放最后）；`-v` 显示过程

```bash
tar -czf bak.tar.gz dir1 hello.txt
stat -c '%s %n' bak.tar.gz
```

```text
168 bak.tar.gz
```

> ⚠️ `tar -czf 包 目录` 是把整个目录（连路径）放进去；打包大量重复文件时 `-z` 很慢，可以先去 `-v` 看是不是包错东西了。

### `tar -tzf` 看一眼压缩包里有什么（不解开）

**签名** `tar -tzf <包名.tar.gz>` ｜ **返回** 列出包里的文件名（不改动任何东西） ｜ **备注** `t` = 列出；下别人的包、解压前先跑一遍，这是基本卫生习惯

```bash
tar -czf bak.tar.gz dir1 hello.txt
tar -tzf bak.tar.gz
```

```text
dir1/
hello.txt
```

> ⚠️ 解压来路不明的包有风险：包里可能带 `../` 或绝对路径，解到你的重要目录会覆盖文件（GNU tar 会自动去掉开头的 `/` 和 `../` 并报 `Member name contains '..'` 退出，但别指望所有解压工具都这么乖）。先 `-tzf` 看文件列表最稳。

### `tar -xzf` 解包（解开 .tar.gz）

**签名** `tar -xzf <包名.tar.gz> [-C <目标目录>]` ｜ **返回** 把包里的东西解出来；`-C 目录` 表示解到那个目录，不加就解到**当前目录** ｜ **备注** `x` = 解开；`.tar`（没压缩）用 `-xf`、`.tar.bz2` 用 `-xjf`、`.tar.xz` 用 `-xJf`

```bash
tar -czf bak.tar.gz dir1 hello.txt
mkdir restore
tar -xzf bak.tar.gz -C restore
find restore -type f | sort
```

```text
restore/hello.txt
```

> ⚠️ 解之前先 `ls` 看当前在哪、最好新建一个空目录再解 —— 否则一堆文件会散在你当前的目录里。

### `gzip / gunzip` 压缩单个文件（不是打包目录）

**签名** `gzip <文件>` / `gunzip <文件.gz>` / `zcat <文件.gz>` ｜ **返回** `gzip` 会把原文件**替换**成 `文件.gz`（原文件消失）；`gunzip` 反向还原；`zcat` 直接看压缩文件内容 ｜ **备注** `-k` 保留原文件（`gzip -k a.txt` 得到 a.txt 和 a.txt.gz）；`-d` 等于 gunzip

```bash
cp hello.txt gz-demo.txt
gzip gz-demo.txt
ls -1 gz-demo.txt.gz
gunzip gz-demo.txt.gz
ls -1 gz-demo.txt
```

```text
gz-demo.txt.gz
gz-demo.txt
```

> ⚠️ gzip 只能压**单个文件**，压目录要用 `tar -czf`（所以才有 `.tar.gz` 这种双后缀）。

### `zip / unzip` 跨平台压缩包（给 Windows 用）

**签名** `zip -r <包名.zip> <目录>` / `unzip <包名.zip>` / `unzip -l <包名.zip>` ｜ **返回** `zip` 打包、`unzip` 解压、`unzip -l` 只看内容清单 ｜ **备注** 要装：`sudo apt install zip unzip`；和 Windows 交换文件时 zip 最省事（Windows 不认 .tar.gz）

```bash
zip -r bak.zip dir1
```

```text
（未实跑：校验容器里没有 zip / unzip。跨系统传 zip 时中文文件名容易乱码，收下后先 `unzip -l` 看一眼名字对不对）
```

## A11 系统信息与软件包

### `cat /etc/os-release` 我在什么系统上（发行版与版本）

**签名** `cat /etc/os-release` / `head -n 3 /etc/os-release` ｜ **返回** 打印发行版的名字和版本号；看 `PRETTY_NAME` 那一行就够了 ｜ **备注** Kali / Ubuntu / Debian / CentOS 各家的字段不完全一样，`PRETTY_NAME` 最稳；`uname -r` 看内核（下一条）

```bash
head -n 3 /etc/os-release
```

```text
PRETTY_NAME="Ubuntu 24.04.5 LTS"
NAME="Ubuntu"
VERSION_ID="24.04"
```

> ⚠️ 你在容器里看到的这个文件是**容器自己的**，和宿主机（你的 macOS）无关。

### `uname -a` 看内核版本和机器架构

**签名** `uname -a` / `uname -r`（只要内核版本）/ `uname -m`（只要架构） ｜ **返回** 打印内核名、主机名、内核版本、编译时间和 CPU 架构（`x86_64` 或 `aarch64`） ｜ **备注** 装软件包、编译程序前先看一眼架构：下载错架构的安装包是最常见的低级错误

```bash
uname -a
```

```text
（结构示例：主机名、内核版本、架构每台机器都不同，只看格式）
Linux hostname 6.8.0-117-generic #117-Ubuntu SMP PREEMPT_DYNAMIC aarch64 GNU/Linux
```

### `df -h` 看磁盘还剩多少空间

**签名** `df -h` / `df -h .`（只看当前目录所在分区） ｜ **返回** 一行一个分区：容量、已用、可用、使用率、挂载点 ｜ **备注** `-h` = 人类可读（G/M）；发现「磁盘满了」就靠它定位是哪个分区

```bash
df -h
```

```text
（结构示例：每台机器的容量和挂载点都不同，只看格式）
Filesystem      Size  Used Avail Use% Mounted on
overlay          59G  4.8G   51G   9% /
tmpfs            64M     0   64M   0% /dev
```

### `du -sh` 看某个目录占了多少空间

**签名** `du -sh <目录>` / `du -sh *` / `du -sh * | sort -h` ｜ **返回** `-s` 只给总计（不列子目录）、`-h` 人类可读；`du -sh *` 逐个列出当前目录下的条目 ｜ **备注** 磁盘满了、想知道是谁占的，就用 `du -sh * | sort -h`（从小到大排，最大的在最后）

```bash
du -sh .
du -sh dir1
```

```text
32K	.
4.0K	dir1
```

> ⚠️ `du` 算的是**占用块**（4K 起跳），和 `ls -l` 显示的字节数不完全一样；软链接默认不跟着算进去。

### `free -h` 看内存和 swap 使用情况

**签名** `free -h` ｜ **返回** 打印总内存、已用、空闲、缓存，以及 swap 的用量；重点看 `available` 那一列 ｜ **备注** `-h` 人类可读；`-s 2` 每 2 秒刷新一次（`Ctrl+C` 停）

```bash
free -h
```

```text
（结构示例：内存大小和用量每台机器都不同，只看格式）
               total        used        free      shared  buff/cache   available
Mem:           7.7Gi       406Mi       5.9Gi       1.0Mi       1.5Gi       7.0Gi
Swap:          2.0Gi          0B       2.0Gi
```

### `echo $PATH` 命令是从哪些目录里找的

**签名** `echo $PATH` ｜ **返回** 打印一串用 `:` 分隔的目录：你敲命令时，shell 从左到右在这些目录里找同名程序 ｜ **备注** 自己装的工具想直接敲名字就能用，要么放进 `/usr/local/bin`，要么把它的目录加进 PATH

```bash
echo $PATH
echo "$PATH" | tr ':' '\n'
```

```text
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
/usr/local/sbin
/usr/local/bin
/usr/sbin
/usr/bin
/sbin
/bin
```

> ⚠️ 改 PATH 必须带上 `$PATH`：写成 `export PATH="$HOME/bin"` 会把系统目录全丢掉，之后 `ls`、`head` 全都 `command not found`（只能关掉这个终端重开）。

### `export / alias` 临时设环境变量 / 造命令别名

**签名** `export <名字>=<值>` / `alias <别名>='<命令>'` ｜ **返回** `export` 让变量传给子进程（`echo $名字` 能看，`env` 里也在）；`alias` 造一个快捷写法 ｜ **备注** 两者都**只对当前这个终端窗口有效**，关掉就没了；想长期生效写进 `~/.bashrc`，再 `source ~/.bashrc` 让它立刻生效

```bash
export SITE=dvwa
echo $SITE
alias ll='ls -l'
alias ll
env | grep '^SITE='
```

```text
dvwa
alias ll='ls -l'
SITE=dvwa
```

> ⚠️ `alias` 只在**交互式** shell 里展开，脚本里不生效（脚本里请用函数或者写完整命令）；别把 `ls` 之类的常用命令覆盖成危险别名。

### `apt` 装 / 卸软件（Debian、Ubuntu、Kali 系）

**签名** `sudo apt update` / `sudo apt install <包名>` / `sudo apt remove <包名>` / `apt search <关键词>` ｜ **返回** `update` 刷新软件清单、`install` 安装、`search` 搜索包名；都会打印一大堆过程和结果 ｜ **备注** Debian 系（含 Kali）用 `apt`；CentOS / RHEL / fedora 系用 `dnf` / `yum`；Arch 系用 `pacman`

```bash
sudo apt update
sudo apt install -y tree
```

```text
（未实跑：需要 root + 网络。注意 `apt update`（只刷新清单）和 `apt upgrade`（真升级已装的包）是两件事，生产环境别随手 upgrade）
```

## 学习建议

### 别背，练

- **一天 10 条**：把 A2、A3、A4 的命令在自己机器上挨个敲一遍，手比眼记得牢。
- **每学一条就问一句「它会不会改东西」**：`ls`、`cat`、`grep` 都不会；`rm`、`mv`、`chmod` 会。会改东西的先在 `linux-lab` 里试。
- **用 Tab 补全、↑ 翻历史**，别手打长路径 —— 新手 80% 的 `No such file or directory` 是打错字。

### 键盘上的保命操作（比命令还常用）

| 按键 | 作用 |
|------|------|
| `Tab` | 补全命令 / 文件名（按一下没反应就再按一下，会列出候选） |
| `↑` `↓` | 翻命令历史；`history` 看全部，`!编号` 重跑第几条 |
| `Ctrl + C` | 中断当前正在跑的命令（比如 `ping` 忘了加 `-c` 停不下来时） |
| `Ctrl + D` | 结束输入 / 退出当前 shell |
| `Ctrl + L` | 清屏（等于 `clear`） |
| `Ctrl + R` | 搜索历史命令：打几个字，回车就把那条重跑一遍 |
| `Ctrl + A` / `Ctrl + E` | 光标跳到行首 / 行尾 |
| `!!` | 重跑上一条命令（常配 `sudo !!`：上一条忘了加 sudo） |
| 命令末尾加 `&` | 让它在后台跑，不占着终端（A8） |

### 三个新手最常踩的坑

- **`rm` 没有回收站**：删了就是删了。`rm -rf /`、`rm -rf ~` 是两条能毁掉系统的命令，永远不要粘贴来路不明的命令。
- **`Permission denied` 先看属主**：多半不是命令写错，而是你没有读 / 写 / 执行那个文件的权限（`ls -l` 看第三列是不是你，A7）。
- **「文件找不到」先 `pwd` + `ls`**：多数时候是当前目录不对，不是文件不存在。

### 下一步（往安全方向走）

- 把 `grep` / `awk` / `cut` / `sort | uniq -c` 练熟：看日志、做 CTF 里的文本分析全靠它们（A5、A6）。
- 然后看 `tcpdump`、日志目录 `/var/log/`、`systemctl` 管服务（不在本笔记范围，先知道名字）。
- 任何命令想看全部选项：`命令 --help`（A1），比背下来靠谱。