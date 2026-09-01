# 影刀 xbot AI Agent 开发指南

> 面向影刀 xbot / 编码版、RPA 自动化和 AI 编程 Agent 的中文开发知识库。

[![GitHub stars](https://img.shields.io/github/stars/apexcheng/yingdao-xbot-ai-agent?style=social)](https://github.com/apexcheng/yingdao-xbot-ai-agent/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/apexcheng/yingdao-xbot-ai-agent?style=social)](https://github.com/apexcheng/yingdao-xbot-ai-agent/network/members)
[![AI Agent](https://img.shields.io/badge/AI-Agent-blue)](AGENTS.md)
[![RPA](https://img.shields.io/badge/RPA-Automation-green)](xbot-api-docs/docs/browser.md)
[![xbot](https://img.shields.io/badge/xbot-Yingdao-orange)](llms.txt)

## 关于这个项目

这是我在实际开发和维护影刀自动化项目时，为个人 AI 辅助开发流程持续整理的知识库。它首先服务于我自己的项目，同时公开出来，希望给同样使用 Codex、Claude Code、Cursor 等工具开发影刀编码版的开发者一些参考。

本仓库不是影刀官方文档，也不追求覆盖所有 API。其中的内容主要来自个人项目中的真实调用、当前安装版本源码核验和可复现问题。版本、市场指令和页面行为可能变化，请以自己的运行环境为准。

## 为什么整理这个知识库

通用代码模型通常熟悉 Python、Selenium、Playwright、pandas 或 openpyxl，但并不天然了解影刀项目中的：

- xbot 对象、元素库、图像库和资源文件的真实用法。
- 浏览器、Excel / WPS、Windows 自动化之间的 API 边界。
- 市场指令在可视化界面和编码版中的参数映射。
- 影刀真实项目目录、`package.json` 和同步流程的关系。
- 哪些结论已验证，哪些仍需要在当前环境运行确认。

这个仓库的目标不是让 AI “记住更多文档”，而是让它在不确定时能找到正确入口，少猜 API，少复制过时经验。

## 仓库包含什么

### AI Agent 开发规则

- [AGENTS.md](AGENTS.md)：跨项目稳定规则，包括最小改动、过程式主流程、不猜 API 和按风险验证。
- [llms.txt](llms.txt)：给 AI Agent 使用的精简文档导航。
- [project-template](project-template/)：可复制到真实影刀项目的最小模板和同步工具。

### xbot API 与自动化文档

- [基础对象、元素库与资源](xbot-api-docs/docs/package.md)
- [浏览器与网页元素](xbot-api-docs/docs/browser.md)
- [Excel / WPS 工作簿与数据读写](xbot-api-docs/docs/excel.md)
- [Windows 窗口、键盘与鼠标](xbot-api-docs/docs/win32.md)
- [影刀日志](xbot-api-docs/docs/logging.md)
- [通知与对话框](xbot-api-docs/docs/notification.md)
- [压缩与解压](xbot-api-docs/docs/xzip.md)
- [iframe2 扩展](xbot-api-docs/docs/iframe2-extension.md)

### 市场指令事实

[市场指令索引](xbot-api-docs/docs/extension-instructions.md) 用于确认当前安装版本的公开入口、参数和返回结构，目前包括：

- 钉钉 AI 表格和钉钉企业机器人消息。
- Excel 扩展操作、离线 OCR、广告处理和网页增强。
- C-ERP 市场指令、ERP 订单查询与字段翻译。
- 登录扩展、iframe 和其他已核验扩展能力。

## 快速开始

### 1. 克隆知识库

```bash
git clone https://github.com/apexcheng/yingdao-xbot-ai-agent.git
```

### 2. 确认真实影刀项目

本仓库只保存知识，不是实际运行的影刀应用。请确认真实项目根目录中存在 `package.json`，再让 AI Agent 进入该目录修改业务代码。

### 3. 复制最小项目模板

把 `project-template/` 中的两个文件复制到真实项目根目录，与 `package.json` 同级：

```text
AGENTS.md
shadowbot_sync_tool.py
```

### 4. 告诉 AI Agent 两个目录

```text
知识库目录：<本仓库的本地路径>
真实项目目录：<影刀项目路径>

先读取真实项目中的 AGENTS.md，再检查现有代码。
只修改当前需求相关内容；无法确认 xbot API 或市场指令时，按知识库 llms.txt 查找事实页。
```

## 影刀同步

真实项目新增 `.py` 文件，或者用户明确要求“同步影刀”时，在真实项目根目录执行：

```powershell
python shadowbot_sync_tool.py
```

同步脚本会扫描项目中的 Python 文件，完成登记和编译处理。“同步影刀”不是 Git 提交或普通文件复制；同步成功也不等于已经在影刀编辑器中运行验证。

## 开发与维护风格

这是一个个人持续维护的实用型知识库，优先保留长期、稳定、能反复帮助真实项目的内容：

- 业务流程优先直接、可读，不追求复杂架构。
- API 结论需要有当前版本源码、真实调用或可追溯代码作为依据。
- 项目专用的页面字段、业务口径和临时 workaround 不上升为公共规则。
- 文档尽量链接到唯一事实页，不为了“看起来完整”重复同一段内容。

如果你发现文档与当前版本不一致，欢迎提交 Issue 或 Pull Request。贡献前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)，并确保账号、Token、Webhook、客户数据和本机路径已脱敏。

## 目录结构

```text
AGENTS.md                    # Agent 稳定开发规则
llms.txt                     # AI / LLM 文档索引
README.md                    # 项目介绍与使用入口
CONTRIBUTING.md              # 事实证据、内容边界与脱敏规则
project-template/            # 真实影刀项目最小模板
tests/                       # 影刀同步工具回归测试
xbot-api-docs/
  AGENTS.md                  # API 文档维护边界
  docs/                      # xbot API 和市场指令事实页
```

## 搜索关键词

影刀、影刀编码版、影刀 xbot、影刀 API、影刀 RPA、浏览器自动化、Excel 自动化、WPS 自动化、Windows 自动化、钉钉 AI 表格、市场指令、AI Agent、Codex、Claude Code、Cursor、Yingdao、xbot API、RPA automation、Python automation。

## 联系与许可证

如需交流影刀编码版、xbot API、RPA 自动化和 AI Agent 开发，可联系 QQ：`1677880403`。

本项目采用 [MIT License](LICENSE)。
