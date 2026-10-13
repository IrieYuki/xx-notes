---
name: vscode-extension-offline-install
description: Use when VS Code extension install hangs or times out.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [vscode, extensions, china-network, proxy]
    related_skills: [hermes-desktop-app-settings]
---

# VS Code 扩展装不上时的手动装法

## When to Use

- `code --install-extension <id>` 跑了很久没输出、超时被杀。
- VS Code 图形界面里装扩展一直转圈、或报下载失败。
- 需要给国内网络的机器装微软自营扩展（`ms-vscode.*` / `ms-python.*`）。

`marketplace.visualstudio.com` 能通 **不代表** 扩展能装：真正的字节从
`*.gallerycdn.vsassets.io` / `*.vscode-unpkg.net` 取，国内常被限速或卡死，
表现为 `code --install-extension` 静默挂到超时（几分钟无输出）。

## 判断

```bash
# 入口页通常 200，别被骗
curl -s -o /dev/null -w '%{http_code}\n' --max-time 10 https://marketplace.visualstudio.com/
# 真下载走 vspackage 接口，单独测（默认 60s 超时就说明卡了）
curl -sL --max-time 60 -o /tmp/t.vsix "https://marketplace.visualstudio.com/_apis/public/gallery/publishers/<publisher>/vsextensions/<ext>/latest/vspackage"
```

另有两个坑：
- `curl -I`（HEAD）对该接口返回 **405**，别据此判断不通。
- GUI 版 VS Code 正在运行时，CLI 装扩展偶尔卡在扩展目录锁上——先试一次，卡了再走下面。

## 走代理手动下（推荐）

```bash
cd ~/.hermes/cache/scratch
curl -sL --max-time 1500 -x http://127.0.0.1:7897 -o ext.vsix \
  "https://marketplace.visualstudio.com/_apis/public/gallery/publishers/<publisher>/vsextensions/<ext>/latest/vspackage"
```

大扩展（cpptools ≈113MB）别放前台跑，用 `background=true`，再循环 `stat -f%z` 看进度。

### 关键坑：拿到的是 gzip，不是 zip

服务器返回 `Content-Encoding: gzip` 且 curl 不解压，于是：

```bash
file ext.vsix          # → "gzip compressed data"（若是 Zip 则跳过这步）
gzip -t ext.vsix       # 校验完整性，比看大小可靠
gunzip -c ext.vsix > ext.zip
unzip -t ext.zip        # 必须 "No errors detected"
```

`unzip -t` 直接对 gzip 文件跑会报「不完整」，这不是下载失败。

## 装

```bash
code --install-extension /tmp/ext.zip     # 本地文件秒装
code --list-extensions | grep -i <ext>    # 核实
ls ~/.vscode/extensions/ | grep <ext>     # 核实真实目录与版本号
```

## 备选：Open VSX

微软自营扩展（`ms-vscode.*`、`ms-python.*`）**不在** Open VSX，会返回
`Extension not found`。第三方扩展可以：

```bash
curl -s https://open-vsx.org/api/<publisher>/<ext> | python3 -c "import sys,json;print(json.load(sys.stdin)['files']['download']['url'])"
```

注意 Open VSX 上有的是**精简包**（如 `vadimcn.vscode-lldb` 只有 285KB，运行时自己去 GitHub 拉二进制——国内直接废掉）。这类扩展别从 Open VSX 装。
