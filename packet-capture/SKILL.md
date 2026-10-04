---
name: packet-capture
description: Use when capturing or analyzing packets with dumpcap/tshark.
---

# 抓包与过滤器速查（dumpcap / tshark / Wireshark）

> 正本仓库：IrieYuki/xx-notes。Day 2 讲义（~/xx/CS）用到本技能的命令；这里只放**可复用查表**，概念讲解留在讲义。

## 三件套定位

| 工具 | 定位 | 什么时候用 |
|---|---|---|
| `dumpcap` | 只抓，权限最低 | 长时间抓包 |
| `tshark` | 命令行分析 | SSH/脚本/一条命令出答案 |
| `Wireshark` | 图形界面 | 看协议细节、Follow Stream |

> macOS：tshark/dumpcap 在 /opt/homebrew/bin，装 ChmodBPF 后免 sudo。接口名是 macOS 那套（lo0/en0/bridge100），不是 eth0；**本机回环/容器流量抓 `lo0`**。

## dumpcap（抓包）

```bash
dumpcap -D                                        # 列出网卡
dumpcap -i lo0 -f "tcp port 8081" -w out.pcapng   # 抓：接口+过滤器+存文件（Ctrl+C 停）
dumpcap -i lo0 -f "tcp port 8081" -a duration:10 -w out.pcapng  # 自动停 10 秒
capinfos out.pcapng                               # 抓包文件信息（包数/时长）
```

- `-f` 是**捕获过滤器**（BPF，内核层就丢包，省内存磁盘）；`-w` 目标文件已存在会**直接覆盖**。
- 判断抓没抓到：Ctrl+C 后看 `Packets captured: N`，**N>0 才算**（0 = 登录/流量没在窗口内发生）。

## tshark（命令行分析）

```bash
tshark -r out.pcapng                              # 逐包打印
tshark -r out.pcapng -Y 'http.request'            # 显示过滤器（抓完再筛）
tshark -r out.pcapng -Y '...' -T fields -e ip.src -e http.host -e http.request.uri
tshark -r out.pcapng -Y 'http.request.method=="POST"' -T fields -e http.file_data | xxd -r -p  # POST 正文转明文
tshark -r out.pcapng -q -z io,phs                  # 协议分层统计
```

- `-Y` 显示过滤器 vs `-f` 捕获过滤器：**语法不同**，别混用。
- `-T fields -e 字段` 提取指定字段；字段名 = Wireshark 里点开包、底部看到的 Field Name。
- **十六进制转明文**：`http.file_data` 是 hex，管道接 `xxd -r -p`。
- 常用字段：`ip.src` `ip.dst` `tcp.srcport` `tcp.dstport` `http.host` `http.request.uri` `http.request.method` `http.file_data` `http.cookie`。

## BPF 捕获过滤器（dumpcap -f / tcpdump 表达式）

| 表达式 | 含义 |
|---|---|
| `host 192.168.1.1` | 该 IP 收发 |
| `src host 1.2.3.4` / `dst host 1.2.3.4` | 只源/只目的 |
| `net 192.168.0.0/16` | 网段 |
| `port 80` / `tcp port 80` / `udp port 53` | 端口（可带协议前缀） |
| `tcp` / `udp` / `icmp` / `arp` | 按协议 |
| `tcp port 8081 and host 127.0.0.1` | 组合（and/or/not） |

## 显示过滤器（Wireshark 过滤栏 / tshark -Y）

| 过滤器 | 含义 |
|---|---|
| `http` / `http.request` / `http.response` | HTTP 请求/响应 |
| `http.request.method == "POST"` | 只看 POST（登录/上传） |
| `ip.addr == 192.168.64.2` | 与某 IP 通信（src/dst 都算） |
| `ip.src == 127.0.0.1 && tcp.port == 8081` | 组合（`&&` 与、`\|\|` 或、`!` 非） |
| `tcp.flags.syn == 1` / `tcp.flags.reset == 1` | 握手包 / RST |
| `tcp.stream eq 0` | 第 0 条 TCP 流 |
| `icmp` / `arp` / `dns` | 按协议 |
| `http contains "password"` | 内容含关键词 |
| `tls.handshake.type == 1` | TLS ClientHello（HTTPS 只看得到这层） |

- 新手最该用的：右键包 → **Follow → TCP/HTTP Stream**，把一次完整对话拼出来看。

## xxd 十六进制 ↔ 文本

```bash
echo -n "hello" | xxd           # 文本 → hex
echo "68656c6c6f" | xxd -r -p   # hex → 文本
```

- `-r` 逆向（hex→字节），`-p` 纯 hex（无地址栏）；tshark 的 `http.file_data` 输出正好是 `-p` 格式。

## 真实案例速记

- **抓明文登录口令**：`dumpcap -i lo0 -f "tcp port 8081" -w x.pcapng` → `tshark -r x.pcapng -Y 'http.request.method=="POST"' -T fields -e http.file_data | xxd -r -p` → 直接看到 `username=...&password=...`。
- **DVWA 脚本登录要两步**（登录页有 CSRF token）：先 GET 拿 `user_token`，再带 token POST —— 详见 `macos-security-lab-setup` 技能。
