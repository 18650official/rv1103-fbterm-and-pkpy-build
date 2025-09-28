# Luckfox Pico 定制化终端环境 - 全自动构建与部署系统

[![Build Status](https://github.com/18650official/rv1103-fbterm-and-pkpy-build/actions/workflows/build-and-deploy.yml/badge.svg)](https://github.com/18650official/rv1103-fbterm-and-pkpy-build/actions)

## 1. 项目介绍 (Project Introduction)

本项目是一个为 **Luckfox Pico (RV1103)** 开发板量身定制的、完整的终端环境构建系统。它旨在解决嵌入式环境下，从零开始交叉编译一套包含复杂依赖（如字体渲染）的软件系统时所面临的各种挑战。

项目核心组件包括：
* 一个经过深度优化和功能增强的 **Framebuffer 终端 (`fbterm`)**。
* 一个轻量级、可嵌入的 **Python 解释器 (`pocketpy`)**。
* 所有必要的静态链接依赖库（`zlib`, `expat`, `libiconv`, `freetype`, `fontconfig`）。

整个项目通过一套**全自动的编译和部署脚本**进行管理，实现了在任意干净的 Ubuntu/Debian 主机上“一键式”完成所有组件的编译、打包和部署文件生成，确保了流程的**透明、严谨和高度可复现性**。

## 2. 核心特性 (Features)

* **完全自动化 (Fully Automated)**：仅需一条命令，即可完成从环境配置到最终产物打包的全过程。
* **自给自足 (Self-Contained)**：脚本自动处理主机环境依赖安装、交叉编译工具链下载、以及构建工具（如`autoconf`）的版本检查与升级。
* **高度可复现 (Reproducible)**：通过锁定依赖版本和标准化的编译流程，确保在任何机器上都能得到完全一致的编译结果。
* **CI/CD 集成 (CI/CD Integrated)**：内置 GitHub Actions 工作流，在代码推送到 `master` 分支后，自动在云端执行完整的编译、打包流程，并提供可供下载的部署包。
* **健壮的兼容性修复 (Robust Compatibility)**：脚本内包含了针对旧版软件（如 `fbterm`, `fontconfig`）在现代化编译环境下所需的各种兼容性修复，确保编译过程顺利。

## 3. 目录及脚本说明 (Directory and Script Descriptions)

| 文件/目录 | 功能说明 |
| :--- | :--- |
| `fbterm-truecolor/` | Framebuffer 终端 (`fbterm`) 源码 |
| `pocketpy/` | PocketPy Python 解释器源码 |
| `zlib-1.3.1/` 等 | 各依赖库源码 (zlib, expat, freetype...) |
| `dep/` | 静态资源文件（模拟目标设备目录结构） |
| **`auto_build_rv1103.sh`** | **核心脚本：一键编译所有项目** |
| **`gen_installer.sh`** | **核心脚本：一键打包部署文件** |
| **`clean.sh`** | **辅助脚本：一键清理所有编译产物** |
| `.gitignore` | Git 忽略规则，确保仓库只包含源码和脚本 |
| `.github/workflows/` | GitHub Actions 自动化工作流配置文件 |

## 4. 本地构建指南 (Local Build Guide)

本项目的构建流程被设计为完全自动化，确保在任何一台新的电脑上都可以轻松复现。

### 编译环境要求
* 一个基于 Debian/Ubuntu 的 Linux 系统 (推荐 Ubuntu 20.04 LTS 或更高版本)。
* `git` 已安装。
* 拥有 `sudo` 权限（用于首次运行时安装编译所需的依赖包）。

### 一键编译步骤

1.  **克隆本仓库**
    ```bash
    git clone [https://github.com/18650official/rv1103-fbterm-and-pkpy-build.git](https://github.com/18650official/rv1103-fbterm-and-pkpy-build.git)
    cd rv1103-fbterm-and-pkpy-build
    ```

2.  **准备源码**
    确保所有依赖库的源码文件夹（如 `zlib-1.3.1`, `freetype-2.14.1` 等）都已存在于项目根目录下，与脚本文件并列。

3.  **执行一键编译脚本**
    ```bash
    chmod +x auto_build_rv1103.sh
    ./auto_build_rv1103.sh
    ```
    该脚本将会自动执行以下所有操作：
    * **安装主机依赖**：使用 `apt-get` 安装所有编译所需的工具。
    * **下载交叉编译工具链**：自动从 Gitee 克隆 Luckfox Pico 官方的交叉编译工具链到 `luckfox_toolchain/` 目录。
    * **升级构建工具**：自动检查并按需编译安装最新版的 `autoconf`。
    * **顺序编译**：严格按照依赖关系，依次编译所有组件。
    * **生成产物**：编译好的依赖库会被安装到独立的 `staging/` 目录，最终的可执行文件会生成在各自的项目目录中。

4.  **打包用于部署**
    编译成功后，运行打包脚本：
    ```bash
    chmod +x gen_installer.sh
    ./gen_installer.sh
    ```
    此脚本会自动将编译好的程序和 `dep/` 目录下的资源文件，打包成一个 `update.tar` 和一个智能安装脚本 `install.sh`，并存放在 `install/` 目录中。

5.  **部署到开发板**
    将 `install/` 目录下的两个文件上传到开发板的 `/tmp` 目录，并执行 `install.sh` 即可完成部署。

## 5. 自动化工作流 (GitHub Actions)

本仓库已配置 GitHub Actions，实现了完整的持续集成/持续交付 (CI/CD) 流程。

* **触发机制**：每当有新的代码被推送到 `master` 分支时，工作流会自动触发。
* **执行过程**：工作流会自动在云端 `ubuntu-20.04` 环境中，完整地执行 `auto_build_rv1103.sh` 和 `gen_installer.sh` 脚本。
* **获取产物**：当工作流成功运行后，您可以在仓库的 **"Actions"** 标签页中，找到对应的运行记录。在记录的 **"Summary"** 页面下方，有一个名为 **"Artifacts"** 的区域，您可以在此下载到新鲜出炉的、包含 `update.tar` 和 `install.sh` 的部署包 `luckfox-pico-deployment-package.zip`。

## 6. 技术原理解析：`fbterm` 字体渲染流水线

`fbterm` 作为一个终端应用程序，本身不负责复杂的字体绘制工作。它依赖于 Linux 系统中标准且强大的字体渲染技术栈，该技术栈主要由 `Fontconfig` 和 `FreeType` 组成。

其工作流程如同一条清晰的“流水线”：

`fbterm` (应用层) -> `Fontconfig` (字体管理层) -> `FreeType` (字体渲染层) -> `Framebuffer` (硬件显示层)

1.  **`fbterm` (应用层 - “下达指令者”)**
    * `fbterm` 的任务是知道**“什么”**字符需要被显示在**“哪里”**。例如，它决定在屏幕的第10行第5列，需要显示一个 Unicode 编码为 `U+4F60` 的字符‘你’。
    * 它本身并不知道‘你’这个字长什么样，也不知道如何将它画出来。

2.  **`Fontconfig` (字体管理层 - “图书管理员”)**
    * `fbterm` 向 `Fontconfig` 发出一个请求：“我需要一个18像素、等宽风格、能显示 `U+4F60` 的字体”。
    * `Fontconfig` 会根据系统的配置文件（`/etc/fonts/fonts.conf` 等），像一个图书管理员一样，在系统的字体库（`/usr/share/fonts`）中进行检索。
    * 它会根据优先级、语言支持等规则，找到最匹配的字体文件（例如 `Sarasa Mono SC`），并将这个字体文件的路径和详细信息返回给 `fbterm`。

3.  **`FreeType` (字体渲染层 - “艺术家”)**
    * `fbterm` 拿着 `Fontconfig` 提供的字体文件路径，连同字符 `U+4F60` 和要求的尺寸 `18px`，一并交给了 `FreeType`。
    * `FreeType` 是真正的渲染引擎。它会：
        * **读取**字体文件，找到 `U+4F60` 对应的矢量轮廓数据（由数学曲线定义）。
        * **应用微调 (Hinting)**：这是最关键的一步。`FreeType` 会读取字体文件中内嵌的 Hinting 指令，对矢量轮廓进行微小的、智能的扭曲和调整，使其关键的横平竖直笔画，能够完美地“吸附”到离散的像素网格上。**这就是字体在低分辨率屏幕上保持锐利、无毛边的核心技术。**
        * **栅格化 (Rasterize)**：将经过微调后的轮廓，填充成一张**像素位图 (bitmap)**。如果配置为无抗锯齿，这张位图就是非黑即白的。
    * 最后，`FreeType` 将这张渲染好的、包含了‘你’字形像素数据的位图，返回给 `fbterm`。

4.  **Framebuffer (硬件显示层 - “画布”)**
    * `fbterm` 收到 `FreeType` 生成的位图后，它所做的最后一步工作，就是将这张位图的像素数据，直接复制到 Framebuffer 设备 (`/dev/fb0`) 对应的内存区域中。
    * Framebuffer 是Linux内核提供的直接访问显示硬件的接口，写入这块内存就等于直接在屏幕上点亮了对应的像素点。

至此，一个字符的完整渲染流程就结束了。`Hinting` 在这个流程中，是 `Free-Type` 这一环里，保证低分辨率显示质量的、不可或缺的关键技术。
