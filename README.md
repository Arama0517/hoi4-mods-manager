# 钢铁雄心 4 模组管理器

<p style="text-align: left;">
  <a href="LICENSE"><img alt="GitHub License" src="https://img.shields.io/github/license/Arama0517/hoi4-mods-manager"></a>
  <a href="../../actions/workflows/check.yml"><img alt="GitHub Actions Workflow Status" src="https://img.shields.io/github/actions/workflow/status/Arama0517/hoi4-mods-manager/check.yml?label=CI"></a>
  <a href="../../releases/latest"><img alt="GitHub Release" src="https://img.shields.io/github/v/release/Arama0517/hoi4-mods-manager"></a>
</p>

## 使用方式

1. 从[发行版](../../releases/latest)下载最新版本
2. 解压到游戏的根目录
3. 运行

> [!WARNING] 内置的账号不一定可用

## 完成的功能

- [ ] 功能类
  - [x] 模组管理
  - [x] 生成模组定位文件
  - [x] 设置页
  - [ ] 支持大部分 P 社游戏
  - [ ] 弃用官方客户端 (不通过启动 `dowser.exe` 的方式启动客户端, 而是直接运行游戏)
- [ ] 下载类
  - [x] 弃用 `steamcmd`
  - [x] 实现多线程下载 Mod
  - [x] 实现均匀分配文件给每个线程
  - [ ] 实现实时分配文件给每个线程
  - [ ] 实现使用类似 `aria2` 的多线程下载文件方式
- [ ] GUI

# 开发

## 环境要求

- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [task](https://taskfile.dev/installation/) 类似 `make` (可选)
- [VS 2022 Build Tools](https://visualstudio.microsoft.com/zh-hans/downloads/#build-tools-for-visual-studio-2022) 用于 nuitka 构建

## 初始化项目

1. 克隆本项目
2. 在项目根目录创建一个 `launcher-settings.json`, 内容:

```json
{}
```

3. 运行 `uv sync`

## 加速 `uv` 下载依赖和 `python`

> [!TIP] 仅适用于中国地区用户

1. 设置环境变量 `UV_PYTHON_INSTALL_MIRROR` 为 `https://ghp.ci/https://github.com/indygreg/python-build-standalone/releases/download`
2. 进入 `~\AppData\Roaming\uv` _如果没有这个目录就新建一个_
3. 新建 `uv.toml` 文件, 内容:

```toml
# 这里的镜像可以换成你自己喜欢的, 这里用的清华源
index-url = "https://pypi.tuna.tsinghua.edu.cn/simple"
```
