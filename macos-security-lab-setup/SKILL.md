---
name: macos-security-lab-setup
description: Use when building a security lab on Apple Silicon macOS.
---

# Apple Silicon macOS 网安靶场环境

适用：在 M 系列 Mac 上搭渗透/CTF 练习环境（Kali 虚拟机、Docker 靶场、抓包、扫描器工具链）。

## 铁律

1. **一切虚拟机镜像必须 arm64。** M 系列 Mac 跑 amd64 镜像只能靠 QEMU 纯模拟，Metasploit / hashcat 慢到不可用。Kali 从 kali.org → Installer Images → **Apple Silicon (ARM64)**；装完 `uname -m` 应为 `aarch64`（是 x86_64 说明下错了）。
2. **靶场容器用 colima + docker CLI，不用 Docker Desktop。** Docker Desktop 要管理员密码装特权助手、要登录账号、吃 2 GB 磁盘；colima 免密码、纯终端，PHP 靶场性能足够：
   `brew install colima docker docker-compose docker-buildx` → `colima start --cpu 4 --memory 6 --disk 60 --vm-type vz --vz-rosetta`。
   `--vz-rosetta` 让 amd64 镜像经 Rosetta 跑，验证：`docker run --rm --platform linux/amd64 alpine uname -m` → `x86_64`。
3. **brew 的 docker-compose 不会自动注册成 docker 插件**（报 `unknown command: docker compose`）。手动软链：
   `mkdir -p ~/.docker/cli-plugins && ln -sf "$(brew --prefix)/bin/docker-compose" ~/.docker/cli-plugins/docker-compose`（buildx 同理）；或在 `~/.docker/config.json` 里加 `"cliPluginsExtraDirs": ["/opt/homebrew/lib/docker/cli-plugins"]`（brew 的提示写法）。
4. **Wireshark 装 ChmodBPF 后就能免 sudo 抓包。** 官方 cask 的 pkg 安装器要管理员密码，非交互环境下这样做：
   `brew fetch --cask wireshark-app`（或 aria2 下 dmg）→ `hdiutil attach -nobrowse -readonly <dmg>` → `cp -R "<挂载点>/Wireshark.app" /Applications/` → 用 `osascript -e 'do shell script "/usr/sbin/installer -pkg \".../Install ChmodBPF.pkg\" -target / && /usr/sbin/installer -pkg \".../Add Wireshark to the system path.pkg\" -target /" with administrator privileges'`（macOS 原生弹窗里由用户自己输密码）。
   验证：`dumpcap -i lo0 -a duration:3 -w /tmp/x.pcapng` 报出包数即成功；`ls -l /dev/bpf0` 应显示组为 `access_bpf`。
5. **接口名是 macOS 那套**：容器/本机回环流量抓 `lo0`（不是 eth0/any）；`dumpcap -D` 列网卡。
6. **Homebrew 首次安装需要一次 sudo**：非交互 shell 里先 `osascript -e 'do shell script "mkdir -p /opt/homebrew && chown -R <用户>:staff /opt/homebrew" with administrator privileges'` 把目录建好并归用户所有，再跑官方 install.sh（`NONINTERACTIVE=1 CI=1`），否则会卡在密码提示。

## 国内下载提速

- **Kali ISO 换清华源**：`https://mirrors.tuna.tsinghua.edu.cn/kali-images/current/`，实测 71 MB/s（官方 cdimage 只有 130 KB/s）。下完必须 `shasum -a 256 -c` 对官方 SHA256SUMS。
- **单线程慢的站用 aria2c 多线程**：`aria2c -x 8 -s 8 -k 1M`（portswigger CDN 单线程 200 KB/s → 8 线程 11 MB/s）。先小样本测速再决定。
- **brew 自己的下载不支持断点续传**，但它认缓存：按 `<url 的 sha256>--<文件名>` 命名放进 `~/Library/Caches/Homebrew/downloads/`，再 `brew install --cask X` 就会复用。
- **brew 在国内的根问题是两个源都慢**：`formulae.brew.sh`（API 元数据）和 `ghcr.io`（bottle 包）。症状是 `brew install` 卡很久后报 `curl: (28) Operation too slow. Less than 100 bytes/sec` 或 `curl: (92) HTTP/2 stream ... PROTOCOL_ERROR`（后者还会让下载半途留下 `.incomplete`）。**根治：两个源都换国内镜像**，写进 `~/.zprofile` 长期生效：
  ```bash
  export HOMEBREW_API_DOMAIN="https://mirrors.ustc.edu.cn/homebrew-bottles/api"
  export HOMEBREW_BOTTLE_DOMAIN="https://mirrors.ustc.edu.cn/homebrew-bottles"
  ```
  实测中科大镜像下 83 MB 的 bottle 只需 **6 秒**（ghcr.io 折腾十几分钟仍失败）；清华 `mirrors.tuna.tsinghua.edu.cn/homebrew-bottles` 同样可用；**阿里云的 API 会 15 秒超时，别用**。注意换 `HOMEBREW_BOTTLE_DOMAIN` 会改变 bottle URL 的哈希 → brew 旧缓存失效、从镜像重下（镜像够快，可接受）。
- **只差个别 bottle 时别整站重下**：直接从镜像补齐到 brew 缓存即可 —— 先 `ls -la ~/Library/Caches/Homebrew/downloads/` 找到那个 `.incomplete` 文件的完整名字，去掉 `.incomplete` 作为目标名：
  `curl -L -o "<去掉.incomplete的文件名>" "https://mirrors.ustc.edu.cn/homebrew-bottles/bottles/<公式>-<版本>.<tag>.bottle.tar.gz"`，再 `rm -f *.incomplete`，brew install 会认（它自己校验 sha256）。
- **bottle 的 tag 必须匹配本机**：Apple Silicon + macOS 26 是 `arm64_tahoe`，别照抄 `ventura`/`sonoma` 的示例 URL；`?` 或 `-r 0-100` 请求看返回码确认镜像里有没有（`206` = 有，`404` = 没有）。
- **Docker Hub TLS 握手超时**：给 colima VM 里的 docker 配镜像加速。写 `/etc/docker/daemon.json` 的 `registry-mirrors`（可用 `https://docker.m.daocloud.io`、`https://docker.1ms.run`），用 base64 绕开多层引号：
  `B64=$(base64 < daemon.json | tr -d '\n'); colima ssh -- bash -c "echo '$B64' | base64 -d | sudo tee /etc/docker/daemon.json > /dev/null && sudo systemctl restart docker"`，再 `docker info | grep -A3 'Registry Mirrors'` 确认。
- **colima VM 的 DNS 会挂**（报 `lookup ... on [::1]:53: connection refused`）：`colima stop && colima start --dns 223.5.5.5 --dns 119.29.29.29 --dns 8.8.8.8`。

## 本机装 MySQL / PHP（学习 Web 安全用，实测步骤）

- **版本选择**：`mysql@8.0` 已被上游弃用（brew 标明 2027-04-30 停用），别再装；`mysql@9.x` / `mysql`（最新）太新，教程与 CTF 环境基本都是 8.x。选 **`mysql@8.4`（LTS）**。PHP 装最新的 `php`。
- **两个都是 keg-only**：装完必须把 bin 加进 PATH，否则命令找不到 —— `~/.zprofile` 里加 `export PATH="/opt/homebrew/opt/mysql@8.4/bin:$PATH"`。
- **启动与连接**：`brew services start mysql@8.4` → `mysqladmin ping -u root --silent` 报 `mysqld is alive`（实测 3 秒就绪）→ `mysql -u root`。brew 装的 MySQL **root 初始无密码**，要设密码跑 `mysql_secure_installation`。
- **PHP 连 MySQL 不用额外装扩展**：brew 的 `php` 自带 `mysqli` 与 `pdo_mysql`，实测 `new mysqli("127.0.0.1","root","")` 与 `new PDO("mysql:host=127.0.0.1;dbname=...","root","")` 都直连成功。
- **装完先建练习库再写笔记**：示例数据落进真库（如 `learn_sql` 带 students/courses/scores），笔记里每条 SQL 的运行结果才能是真输出。

## 四个隐蔽陷阱

- **macOS 默认没有 `timeout` 命令**（GNU coreutils 才有，或装 `coreutils` 后用 `gtimeout`）。脚本里写了 `timeout 240 docker pull ...` 会直接 `command not found` 而失败，且看起来像拉取失败。用 `while/until` 循环 + 计数控制时长更稳。
- **amd64 镜像的平台警告是正常的**：`docker compose up` 会打印 `The requested image's platform (linux/amd64) does not match the detected host platform (linux/arm64/v8)`，但 Rosetta 下照常跑。在 compose 里给每个 service 写 `platform: linux/amd64` 可以让意图明确并消除该警告。
- **本地端口测试要绕过代理**：终端里 export 过 `ALL_PROXY=http://127.0.0.1:7897` 时，`curl http://127.0.0.1:8081` 会被送给 Clash 并返回 **502**，看起来像靶场挂了。用 `curl --noproxy '*'`，或先 unset 代理变量。
- **镜像站会拒绝特定仓库**：`docker.m.daocloud.io` 对部分镜像直接返回 `403 Forbidden`，此时换 `docker.1ms.run`，或退回 `docker pull 原镜像名`（多试几次也能过）。
- **重试条件别用管道**：`if docker pull X | tail -3; then` 恒为真（退出码是 tail 的），要写 `until docker pull X; do sleep 8; done` 并设最大次数。
- **`docker compose up` 是长驻进程**：终端工具会拒绝对它做前台调用，用后台模式跑（`background=true`），之后单独用 `docker compose ps` 和 `curl` 验证就绪。
- **DVWA 登录页有 CSRF token，脚本登录必须两步**：`vulnerables/web-dvwa` 的 `login.php` 无条件执行 `checkToken()`，裸 `curl -d "username=admin&password=password&Login=Login"` 会 `302 → login.php`（看起来像密码错，其实是缺 token）。正确做法：先 `curl -s -c /tmp/c.txt http://127.0.0.1:8081/login.php` 抓出隐藏字段 `user_token`（单引号 `value='...'`），再 `curl -b /tmp/c.txt -d "...&user_token=$TOK"` 登录，成功后跳 `index.php` 且出现 `You have logged in as 'admin'`。用户 `app`/`vulnerables`（容器内 DB，PostgreSQL 端口写 5432 是死配置行，实际跑的是 MariaDB/MySQL 3306），admin 密码哈希 `md5('password')=5f4dcc3b...` 核对无误。

## UTM 建 Kali 虚拟机（向导逐项答案）

下载：kali.org → Installer Images → **Apple Silicon (ARM64)**（约 3.7 GB，用清华镜像下，见上）。UTM 用 `brew install --cask utm` 装。

**向导里易错的几个选择：**

- 第一屏必须选 **Virtualize**，不是 Emulate。
- 显示输出那页（**只在没勾 Use Apple Virtualization 时出现，客户机选 Linux**）：**勾「启用显示输出」、不勾「启用 OpenGL 硬件加速」**。UTM 源码里的原话是 3D 加速对某些新 Linux 驱动有黑屏/合成异常等已知问题，且勾了会禁用快照挂起（`Suspend is not supported when GPU acceleration is enabled.`）。
- **「启用 Rosetta（x86_64 模拟）」不要勾**：官方文档写明它属于苹果虚拟化后端（`using Apple Virtualization backend`），QEMU 后端下不生效；就算生效，客户机里还得 mount virtiofs `rosetta` + 装 `binfmt-support` + `update-binfmts` 注册。Kali ARM64 工具链全原生，用不到。
- 磁盘给 **60 GiB**（稀疏镜像，用多少占多少；创建后只能变大不能变小）。内存 6 GiB、CPU 6 核。
- 向导看到「显示输出/模拟显卡/Balloon 设备」这组选项 = 当前是 **QEMU 引擎**，不是苹果虚拟化。对 Linux 客户机这反而更稳（苹果虚拟化对 Linux 仍偏实验性），不用回头重选。

**Kali 安装器逐项答案**（Graphical install）：语言 English（选中文会让安装期终端乱码）、位置 other→Asia→China、locale `en_US.UTF-8`、键盘 American English、主机名 `kali`。

- 分区：**Guided - use entire disk** → 选那块 64 GiB 的 VirtIO 盘 → **All files in one partition** → 写盘 Yes。分区界面里只有虚拟磁盘，碰不到 Mac 硬盘。
- 软件源：**Use a network mirror → Yes** → 国家 China → 优先 `mirrors.tuna.tsinghua.edu.cn`。
- 软件选择（Kali 专属界面，键盘：**空格勾选、Tab 换焦点、回车触发焦点上的东西**——在列表上回车是切换该项，不是确认，要 Tab 到 `<Continue>` 再回车）：**Desktop environment 选 Xfce**（Kali 默认、最轻，无 3D 加速时 GNOME/KDE 会卡）；**Collection of tools 选 `default - recommended tools`**（与 live 系统一致；`top10` 只有 10 个工具，二选一不要都勾）。
- GRUB：**Yes** → `/dev/sda`（别选 `/dev/sr0`）。
- ⚠️ 重启后发现又回到安装菜单 = ISO 还挂在光驱里，在 UTM 工具栏把 CD 弹出。

**装完的第一批命令（客户机内）**：

```bash
uname -m                                            # 期望 aarch64
ip -brief a                                         # 期望拿到 192.168.64.x
sudo apt update && sudo apt full-upgrade -y
sudo apt install -y openssh-server spice-vdagent    # SSH 便于从 Mac 终端操作；spice 提供剪贴板共享
sudo systemctl enable --now ssh
which nmap msfconsole sqlmap hydra burpsuite       # 缺哪个 apt install 哪个
```

验证客户机在线（在 Mac 上）：UTM 的共享网络下虚拟机在 `bridge100` 网段，`arp -an | grep 192.168.64` 或 `ifconfig bridge100` 能看到宿主 192.168.64.1、客户机通常是 192.168.64.2。`utmctl` 在非 GUI 会话（如 agent 的 shell）里会报 OSStatus -1743，不可用于自动化检查。

## UTM 客户机：剪贴板与 SSH（打通后基本不用在 VM 窗口里打字）

- **剪贴板不通多半不是 UTM 的问题**。先在 Mac 上读 VM 配置确认：`plutil -p ~/Library/Containers/com.utmapp.UTM/Data/Documents/<vm>.utm/config.plist`（应看到 `ClipboardSharing => true`）；真正要装的是客户机里的 `spice-vdagent`（UTM 自己的说明：*Requires SPICE guest agent tools to be installed.*）。
- **Kali 安装器装完会清空 `/var/lib/apt/lists`**，所以紧接着的 `sudo apt install X` 会报 `E: Unable to locate package X`，看起来像是“装成功了但不生效”。**先 `sudo apt update`**。`systemctl enable spice-vdagentd` 报 *Unit does not exist* = 包压根没装上，同一个原因。
- 装好后客户机里要有**两个**进程：`/usr/sbin/spice-vdagentd`（root）与 `/usr/bin/spice-vdagent`（图形会话内）。`systemctl is-active spice-vdagentd` 显示 inactive 但进程在跑也可能正常（socket 激活或手工启动）；包还带 `/etc/xdg/autostart/spice-vdagent.desktop`，装完**注销重登**会自动拉起用户态客户端。
- **最大的坑：粘贴不是 Cmd+V。** UTM 把 Mac 的 ⌘(Cmd) 映射成 Linux 的 Super 键，所以 Cmd+V 根本到不了客户机的粘贴。图形程序用 **Ctrl+V / Ctrl+C**，**终端里必须用 `Ctrl+Shift+V` / `Ctrl+Shift+C`**（终端里 Ctrl+C 是中断信号，会打断正在跑的安装）。
- 免密 SSH：Mac 上 `ssh-keygen -t ed25519 -N "" -f ~/.ssh/kali_lab_ed25519`，把 `.pub` 内容接到客户机的 `~/.ssh/authorized_keys`（剪贴板通了就是一次 Ctrl+Shift+V），之后 `ssh -i ~/.ssh/kali_lab_ed25519 kali@192.168.64.2` 直连。**注意**：客户机的 sudo 仍要密码，所以远程只能做只读检查和非 sudo 操作，需要 root 的让用户自己在窗口里跑。
- 找客户机 IP：Mac 侧 `arp -an | grep 192.168.64`（宿主是 `192.168.64.1`，客户机通常是 `.2`；用 `ping` 刚开机时可能短暂不通，稍等再试）。

## 靶场清单（实测可拉起）

| 端口 | 镜像 | 说明 |
|---|---|---|
| 8081 | `vulnerables/web-dvwa` | DVWA，先点 Create/Reset Database，安全级别 low |
| 8082 | `c0ny1/upload-labs` | 文件上传 21 关。**镜像不自带 `upload/` 目录**，上传会报「../upload 文件夹不存在」——在 compose 里给该 service 加 `command: sh -c "mkdir -p /var/www/html/upload && chmod 777 /var/www/html/upload && apache2-foreground"`（镜像 Entrypoint 为空、Cmd 就是 `apache2-foreground`，可安全覆盖） |
| 8083 | `acgpiano/sqli-labs` | SQL 注入 65 关 |
| 8084 | `vulfocus/xss-labs` | XSS 20 关 |
| 8085 | `vulfocus/pikachu` | 综合靶场（`area39/pikachu` 在国内镜像站会卡死，别用） |
