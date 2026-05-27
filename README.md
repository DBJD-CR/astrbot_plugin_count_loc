<!-- markdownlint-disable MD028 -->
<!-- markdownlint-disable MD033 -->
<!-- markdownlint-disable MD041 -->

![astrbot_plugin_helloworld](https://socialify.git.ci/DBJD-CR/astrbot_plugin_helloworld/image?custom_description=AstrBot+Plugin+%E6%8F%92%E4%BB%B6%E6%A8%A1%E6%9D%BF&description=1&font=Inter&forks=1&issues=1&language=1&name=1&owner=1&pattern=Brick+Wall&pulls=1&stargazers=1&theme=Auto)

<p align="center">
  <img src="assets/PluginRank.svg" alt="Plugin Rank">
  <img src="assets/StarRank.svg" alt="Star Rank">
  <img src="assets/ShitMountain.svg" alt="ShitMountain">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/License-AGPL_3.0-blue.svg" alt="License: AGPL-3.0">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/AstrBot-v4.11.2+-orange.svg" alt="AstrBot v4.11.2+">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/AstrBot-v4.24.2%20Compatible-brightgreen.svg" alt="Compatible with AstrBot v4.24.2">
  <img src="https://img.shields.io/github/v/release/DBJD-CR/astrbot_plugin_helloworld?label=Release&color=brightgreen" alt="Latest Release">
  <img src="https://img.shields.io/badge/QQ群-1033089808-12B7F3.svg" alt="QQ群">
</p>

[![Moe Counter](https://count.getloli.com/get/@DBJD-CR6?theme=moebooru)](https://github.com/DBJD-CR/astrbot_plugin_helloworld)

---

一个为 [AstrBot](https://github.com/AstrBotDevs/AstrBot) 设计的自定义插件模板，基于官方基础模板扩展而来。当前版本主要补充了更完整的仓库工程化配置、社区协作文件、自动化工作流，以及更完善的插件元数据示例（包含版本约束与平台声明），适合作为个人或团队维护 AstrBot 插件仓库时的起始模板。

## 📑 快速导航

- [✨ 功能特性](#-功能特性)
- [📊 输出示例](#-输出示例)
- [🚀 安装与使用](#-安装与使用)
- [📋 指令说明](#-指令说明)
- [⚙️ 配置项详解](#️-配置项详解)
- [📂 插件目录与结构](#-插件目录与结构)
- [🏗️ 架构说明](#️-架构说明)
- [❓ 常见问题](#-常见问题)
- [🚧 已知限制](#-已知限制)
- [📄 许可证](#-许可证)

---
<!-- 开发者的话 -->
> **开发者的话：**
>
> 大家好，我是 DBJD-CR，这是我为 AstrBot 改的一个插件模板，如果存在做的不好的地方还请理解。
>
> 和我写的其他插件一样，本插件模板也是"Vibe Coding"的产物。
>
> 所以，**本插件的所有文件内容，全部由 AI 编写完成**，我几乎没有为该插件编写任何一行代码，仅进行了架构设计与修改部分文字描述和负责本文档的润色。所以，或许有必要添加下方的声明：

> [!WARNING]  
> 本插件和文档由 AI 生成，内容仅供参考，请仔细甄别。
>
> 插件目前仍处于开发阶段，无法 100% 保证稳定性与可用性。
>
> 虽然这只是个插件模板，也还是诚邀各路大佬对本模板提出一些意见，希望大家多多指点。
>
> 如果觉得这个模板比较实用的话，**就为这个模板点个** 🌟 **Star** 🌟 **吧~** ，这是对我们的最大认可与鼓励！

> [!NOTE]
> 虽然本插件的开发过程中大量使用了 AI 进行辅助，但我保证所有内容都经过了我的严格审查，所有的 AI 生成声明都是形式上的。你可以放心参观本仓库和使用本插件。
>
> 目前插件的主要功能都能正常运转。但仍有很多可以优化的地方。

> [!TIP]
> 本项目的相关开发数据 (持续更新中)：
>
> 开发时长：累计 1 天（主插件部分）
>
> 累计工时：约 3 小时（主插件部分）
>
> 使用的大模型：GPT 5.5(With RooCode in VSCode)
>
> 对话窗口搭建：VSCode RooCode 扩展
>
> Tokens Used：1,814,900

---

## ✨ 功能特性

相较于官方基础模板，本插件模板当前新增或调整了以下内容：

- **完整重写的 README 展示结构**：新增 Socialify 封面、状态徽章、访问计数、快速导航、开发者说明、友情链接、推荐阅读、仓库状态与 Star 历史等更完整的仓库首页展示内容。
- **更适合二次分发的文档骨架**：为安装、指令、配置、目录结构、架构说明、常见问题、已知限制等章节预留了更清晰的模板化占位结构，方便后续按真实插件内容补全。
- **补充 [`metadata.yaml`](metadata.yaml) 元数据方案**：插件标识改为 `astrbot_plugin_helloworld` 前缀形式，并同步调整展示名、描述、作者、仓库地址、版本信息、AstrBot 版本约束与支持平台列表，作为更贴近实际发布场景的参考写法。
- **改为以 [`metadata.yaml`](metadata.yaml) 作为主要元数据来源**：在 [`main.py`](main.py) 中移除了 [`register()`](main.py) 装饰器写法，仅保留基于插件类的实现方式，使模板结构与当前元数据文件协同。
- **新增贡献指南 [`CONTRIBUTING.md`](CONTRIBUTING.md)**：补充了 Issue 使用说明、代码贡献流程、代码风格要求、提交规范与文档贡献说明。
- **新增更新日志 [`CHANGELOG.md`](CHANGELOG.md)**：提供标准化版本记录文件，便于后续按发布节奏维护变更历史。
- **新增社区协作文件**：补充 [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md)、[`PULL_REQUEST_TEMPLATE.md`](.github/PULL_REQUEST_TEMPLATE.md) 与多种 GitHub Issue 模板，覆盖 Bug、功能建议、文档建议、设计建议与开放讨论等协作场景。
- **新增 Dependabot 配置**：通过 [`dependabot.yml`](.github/dependabot.yml) 为 GitHub Actions 与 Python 依赖提供定期更新检查能力。
- **新增 Ruff 质量工作流**：通过 [`ruff-format.yml`](.github/workflows/ruff-format.yml) 增加格式化、自动修复、质量报告与 PR 评论能力，用于改进模板仓库的代码规范体验。
- **新增长期未活跃 Issue 清理工作流**：通过 [`stale.yml`](.github/workflows/stale.yml) 自动标记和关闭长期无活动 Issue，减少仓库维护负担。
- **新增自动发布工作流**：通过 [`release.yml`](.github/workflows/release.yml) 在 [`metadata.yaml`](metadata.yaml) 的版本号发生变更后自动提取版本信息、检查是否已有同名 Release，并尝试结合 [`CHANGELOG.md`](CHANGELOG.md) 生成发布说明，用于简化模板仓库的版本发布流程。
- **新增“屎山检测”工作流**：通过 [`shit-mountain.yml`](.github/workflows/shit-mountain.yml) 集成额外的趣味化代码质量分析流程，作为仓库 CI 展示和风格化管理的一部分。
- **新增仓库展示资源与脚本**：增加 [`assets/`](assets/) 下的可视化徽图资源，以及 Windows 环境下可直接运行的 [`run_ruff.bat`](run_ruff.bat) 脚本，方便本地维护。

整体上，这个模板已经不再只是官方示例的最小复制，而是一个偏向“可直接拿去改造成个人仓库”的增强版起始模板。

## 📊 输出示例

示例输出。

## 🚀 安装与使用

1. **下载插件**: ~~通过 AstrBot 的插件市场下载。~~或从本 GitHub 仓库的 Release 下载 `astrbot_plugin_helloworld` 的 `.zip` 文件，在 AstrBot WebUI 中的插件页面中选择 `从文件安装` 。
2. **安装依赖**: 本插件的核心依赖为 `None`，插件下载安装时会自动安装插件所需的依赖，通常无需额外安装。如果你的环境中确实缺少相关依赖，请安装：

   ```bash
   pip install -r requirements.txt
   ```

3. **重启 AstrBot (可选)**: 如果插件没有正常加载或生效，可以尝试重启你的 AstrBot 程序。
4. **配置插件**: 进入 AstrBot WebUI，找到 `AstrBot 插件模板` 插件，选择 `插件配置` 选项，配置相关参数：

---

## 📋 指令说明

这个插件没有命令。

---

## ⚙️ 配置项详解

---

## 📂 插件目录与结构

```bash
AstrBot/
└─ data/
   └─ plugins/
      └─ astrbot_plugin_helloworld/
         ├─ .gitignore                       # Git 忽略规则
         ├─ _conf_schema.json                # AstrBot WebUI 配置界面 schema 定义
         ├─ CHANGELOG.md                     # 插件更新日志，适用于 AstrBot v4.11.2+
         ├─ CONTRIBUTING.md                  # 本插件的贡献指南
         ├─ LICENSE                          # 许可证文件
         ├─ main.py                          # 插件主入口文件
         ├─ metadata.yaml                    # 插件元数据信息
         ├─ README.md                        # 插件说明文档
         ├─ run_ruff.bat                     # Ruff 一键格式化与自动修复脚本
         │
         └─ assets/                          # README / 仓库展示资源
```

示例结构说明。

---

## 🏗️ 架构说明

```mermaid

```

示例架构说明。

---

## ❓ 常见问题

### Q1：README 最上面那个头图好好看，怎么弄的？

[Socialify](https://socialify.git.ci/)；[仓库地址](https://github.com/wei/socialify)

### Q2: 那个猫猫访客数又是怎么弄的？

[MoeCounter](https://count.getloli.com)；[仓库地址](https://github.com/journey-ad/Moe-Counter)

### Q3: 仓库状态这个卡片呢？

[Repobeats](https://repobeats.axiom.co/?ref=producthunt)

### Q4：要钱吗？

都是免费的哦。

---

## 🚧 已知限制

要在你自己的仓库使用此模板，请修改以下文件的内容为你的实际情况 (主要是涉及仓库链接、徽章资源、发布流程与文档格式的替换)：

- PULL_REQUEST_TEMPLATE.md
- ShitMountain.svg 等 SVG 徽章资源 (不想要可以都删了)
- CHANGELOG.md
- CODE_OF_CONDUCT.md (替换为你的实际邮箱)
- CONTRIBUTING.md
- metadata.yaml (废话)
- README.md (不然呢)
- .github/workflows/release.yml (如你的版本字段、分支策略或 Changelog 标题格式不同，请一并调整)

> [!TIP]
>
> 要使用本仓库提供的 Issue 模板，您还需要运行该脚本 [Issue & PR 标签自动替换脚本](https://github.com/DBJD-CR/awesome_issue_pr_label) 以适配自定义的标签。
>
> 当前 [`release.yml`](.github/workflows/release.yml) 的整体思路是可复用的，但它默认依赖 [`metadata.yaml`](metadata.yaml) 中存在 `version` 字段，且更适合配合形如 `## [v1.0.0] - 2026-05-08` 的 [`CHANGELOG.md`](CHANGELOG.md) 标题格式使用；如果你的仓库使用不同的分支模型、版本命名或更新日志格式，建议在套用模板时同步修改该工作流。

## 💖 友情链接与致谢

- [AstrBot](https://github.com/AstrBotDevs/AstrBot)：在此感谢其开发团队对该项目的付出。

## 📚 推荐阅读

我的其他插件：

- [主动消息 (Proactive_Chat)](https://github.com/DBJD-CR/astrbot_plugin_proactive_chat) - 它能让你的 Bot 在特定的会话长时间没有新消息后，用一个随机的时间间隔，主动发起一次拥有上下文感知、符合人设且包含动态情绪的对话。
- [灾害预警 (Disaster_Warning)](https://github.com/DBJD-CR/astrbot_plugin_disaster_warning) - 它能让你的 Bot 提供实时的地震、海啸、气象预警信息推送服务。
- [视奸面板 (Live_Dashboard)](https://github.com/DBJD-CR/astrbot_plugin_live_dashboard) - 它能让你的 Bot 和群友随时随地视奸你。

## 🤝 贡献

欢迎提交 [Issue](https://github.com/DBJD-CR/astrbot_plugin_helloworld/issues) 和 [Pull Request](https://github.com/DBJD-CR/astrbot_plugin_helloworld/pulls) 来改进这个插件！

- 对于新功能的添加，请先通过 Issue 等方式讨论。
- 对于 PR (拉取请求)，请确保你已阅读并同意遵守本项目的 [贡献指南](https://github.com/DBJD-CR/astrbot_plugin_helloworld/blob/main/CONTRIBUTING.md)。

### 📞 联系我们

如果你对这个插件有任何疑问、建议或 bug 反馈，欢迎加入我的 QQ 交流群。

- **QQ 群**: 1033089808
- **群二维码**:
  
  <img width="281" alt="QQ Group QR Code" src="https://github.com/user-attachments/assets/53acb3c8-1196-4b9e-b0b3-ad3a62d5c41d" />

## 📄 许可证

GNU Affero General Public License v3.0 - 详见 [LICENSE](LICENSE) 文件。

本插件采用 AGPL v3.0 许可证，这意味着：

- 您可以自由使用、修改和分发本插件。
- 如果您在网络服务中使用本插件，必须公开源代码。
- 任何修改都必须使用相同的许可证。

## 📊 仓库状态

![Alt](https://repobeats.axiom.co/api/embed/2c8d42b135fc9fc4c4bf1b4d88c4490bbc57a919.svg "Repobeats analytics image")

## ⭐️ 星星

[![Star History Chart](https://api.star-history.com/svg?repos=DBJD-CR/astrbot_plugin_helloworld&type=Date)](https://www.star-history.com/#DBJD-CR/astrbot_plugin_helloworld&Date)

---

Made with ❤️ by DBJD-CR & GPT
