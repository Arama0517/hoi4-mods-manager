# 钢铁雄心4 模组管理器

_**从SteamCDN多线程下载模组**_

## 食用方式

1. 从[发行版](https://github.com/Arama0517/hoi4-mod-manager/releases/latest)下载最新版本
2. 解压到游戏的根目录
3. 运行

**注意**: 本程序内置的共享账号可能会有时无法登陆

## 完成的功能

- [ ] 功能类
  - [x] 模组管理
  - [x] 生成模组定位文件
  - [ ] 设置页
  - [ ] 支持大部分P社游戏
  - [ ] 弃用官方客户端 (不通过启动 `dowser.exe` 的方式启动客户端, 而是直接运行游戏)
- [ ] 下载类
  - [x] 弃用 `steamcmd`
  - [x] 实现多线程下载 Mod
  - [x] 实现均匀分配文件给每个线程
  - [ ] 实现实时分配文件给每个线程
  - [ ] 实现使用类似 `aria2` 的多线程下载文件方式
- [ ] 实现 GUI

## 开发环境设置
### 必须安装
- [Git](https://git-scm.com/downloads/win)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

### 建议安装
- [Task](https://taskfile.dev/installation/) 类似 `make` 的工具
- [Visual Studio 生成工具](https://visualstudio.microsoft.com/zh-hans/downloads/#build-tools-for-visual-studio-2022) 用于构建

### 初始化项目
1. 同步依赖: `uv sync`
2. 创建 `launcher-settings.json`
3. 开始开发