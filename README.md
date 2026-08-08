# 影刀 xbot AI Agent 开发指南

> 面向影刀编码版、xbot、RPA 自动化和 AI 编程 Agent 的中文开发知识库。
>
> 收录影刀 API、浏览器自动化、Excel / WPS、Windows 自动化、市场指令排错、Claude Code、OpenAI Codex 开发规范与真实问题修正记录。

[![GitHub stars](https://img.shields.io/github/stars/apexcheng/yingdao-xbot-ai-agent?style=social)](https://github.com/apexcheng/yingdao-xbot-ai-agent/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/apexcheng/yingdao-xbot-ai-agent?style=social)](https://github.com/apexcheng/yingdao-xbot-ai-agent/network/members)
[![AI Agent](https://img.shields.io/badge/AI-Agent-blue)](docs/ai-agent-development.md)
[![RPA](https://img.shields.io/badge/RPA-Automation-green)](docs/README.md)
[![xbot](https://img.shields.io/badge/xbot-Yingdao-orange)](docs/xbot-api-guide.md)

简体中文 | [English](README_EN.md)

## 💬 联系作者

如需交流影刀编码版、xbot API、RPA 自动化和 AI Agent 开发，可联系作者。

**联系作者 QQ：1677880403**

## 项目简介

`yingdao-xbot-ai-agent` 是一个面向 **影刀 xbot AI Agent 开发** 的知识库，帮助开发者使用 Claude Code、OpenAI Codex、Cursor 或其他 AI 编程工具开发、维护和排查影刀自动化项目。

本仓库重点解决以下问题：

- 影刀编码版 API 资料分散，Agent 容易猜测函数和参数
- 真实影刀项目目录与知识库目录容易混淆
- 浏览器、Excel / WPS、Windows 和市场指令需要不同排查方法
- AI 生成的代码可能混用 Selenium、Playwright、openpyxl 等其他库的 API
- 修改完成后容易遗漏同步和影刀环境验证
- 错误结论容易被反复复制，缺少可追溯的修正记录

> 本项目是社区知识库，不是影刀官方仓库，也不是实际运行的影刀应用目录。

## 项目包含什么

### 影刀 xbot API 文档

覆盖或导航到：

- 基础对象、元素库、图像库、资源文件和全局变量
- 浏览器对象、网页元素、点击、输入、下载、Cookie 和网络监听
- Excel / WPS 工作簿、Sheet、区域、读写和格式
- Windows 窗口、桌面自动化、键盘和鼠标
- 日志、通知、对话框、压缩和解压
- iframe 扩展指令
- 市场指令参数映射与源码排查
- 钉钉 AI 表格调用入口、读写记录、filter、分页和附件

### AI Agent 开发规则

- `AGENTS.md`：稳定开发规则入口
- `llms.txt`：面向 Agent 的文档索引
- `docs/standard-project-reference.md`：多数据源下载写表项目的标准流程与首选参考项目
- `project-template/`：复制到真实影刀项目根目录的 `AGENTS.md`、`.claude`、`.codex` 和同步工具
- `TASK.md` 工作流：适用于复杂、多文件和多阶段任务

### 真实问题排错

- 页面元素和 iframe
- 登录、验证码和风控
- Excel / WPS 文件占用和数据类型
- 市场指令 UI 与编码版参数不一致
- HTTP 500、unknownError 和 request id
- 钉钉 AI 表格 filter 多条件写法与结果校验
- 错误描述修正和待验证事项管理

## 快速开始

### 1. 准备知识库

```bash
git clone https://github.com/apexcheng/yingdao-xbot-ai-agent.git
```

### 2. 确认真实影刀项目目录

真实项目常见位置类似：

```text
%LOCALAPPDATA%\ShadowBot\users\<user_id>\apps\<app_id>\xbot_robot
```

实际路径应以当前应用为准，并确认该目录中存在 `package.json`。

### 3. 复制项目模板

把 `project-template/` 目录中的内容复制到真实影刀项目根目录，使以下文件与 `package.json` 同级：

```text
AGENTS.md
.claude/
.codex/
shadowbot_sync_tool.py
```

`.claude/settings.local.json` 不属于模板，因为它是本机权限配置。

### 4. 告诉 AI Agent 两个目录

```text
知识库目录：C:\Users\Administrator\Desktop\影刀xAI开发指南
真实项目目录：C:\path\to\shadowbot-project

先读取真实项目根目录中的 AGENTS.md。
开始任务时先确认知识库目录存在；若不存在，立即停止并让我补充正确路径。
再检查真实项目现有代码，只修改与当前需求直接相关的内容。
仅当新增或无法确认 xbot API、市场指令、页面行为时，
再按知识库中的 llms.txt 定位相关文档。
```

### 5. 根据任务读取文档

| 任务 | 文档入口 |
| --- | --- |
| 第一次使用 | [影刀 xbot 快速开始](docs/getting-started.md) |
| 使用 Claude Code / Codex 开发 | [AI Agent 开发工作流](docs/ai-agent-development.md) |
| 新建或重构多数据源报表流程 | [标准流程项目参考](docs/standard-project-reference.md) |
| 查找 xbot API | [xbot API 导航指南](docs/xbot-api-guide.md) |
| 网页、元素、滚动、下载、Cookie | [浏览器自动化指南](docs/browser-automation.md) |
| Excel、WPS、Sheet、单元格和格式 | [Excel / WPS 自动化指南](docs/excel-automation.md) |
| API、页面、表格或市场指令报错 | [影刀开发排错指南](docs/troubleshooting.md) |
| 常见问题 | [FAQ](docs/faq.md) |
| 所有公开文档 | [文档中心](docs/README.md) |

## AI Agent 推荐开发流程

```text
明确业务目标和验收标准
          ↓
确认知识库与真实项目目录
          ↓
复制 project-template 内容到真实项目根目录
          ↓
读取项目根目录 AGENTS.md，并确认固定知识库路径存在
          ↓
复杂任务创建 TASK.md
          ↓
检查真实项目现有代码
          ↓
多个数据源写入同一工作簿并需统一保存通知时读取标准流程项目参考
          ↓
仅在新增或无法确认 API、市场指令、页面行为时查 llms.txt 和对应文档
          ↓
实施最小必要修改
          ↓
新增 `.py` 文件或用户明确要求“同步影刀”时运行 shadowbot_sync_tool.py
          ↓
在影刀环境实际验证
          ↓
记录验证结果和待验证事项
```

适合创建 `TASK.md` 的任务：

- 新建影刀应用
- 跨多个文件修改
- 多阶段业务流程
- 页面、表格、文件和接口之间存在复杂依赖
- 需求仍有较多待确认事项

简单修改一个函数、参数、文案或错误描述时，直接做最小修改，不必额外引入任务文件。

## 文档地图

### 入门与工作流

- [文档中心](docs/README.md)
- [影刀 xbot 快速开始](docs/getting-started.md)
- [AI Agent 开发工作流](docs/ai-agent-development.md)
- [标准流程项目参考](docs/standard-project-reference.md)
- [常见问题 FAQ](docs/faq.md)

### xbot API 与自动化专题

- [xbot API 导航指南](docs/xbot-api-guide.md)
- [基础对象与全局变量](xbot-api-docs/docs/package.md)
- [浏览器操作](xbot-api-docs/docs/browser.md)
- [Excel / WPS 操作](xbot-api-docs/docs/excel.md)
- [Windows 自动化](xbot-api-docs/docs/win32.md)
- [键盘鼠标](xbot-api-docs/docs/keyboard-mouse.md)
- [日志记录](xbot-api-docs/docs/logging.md)
- [桌面对话框与通知](xbot-api-docs/docs/notification.md)
- [压缩解压](xbot-api-docs/docs/xzip.md)
- [iframe2 扩展](xbot-api-docs/docs/iframe2-extension.md)

### 市场指令与排错

- [影刀开发排错指南](docs/troubleshooting.md)
- [市场指令扩展开发](xbot-api-docs/docs/extension-instructions.md)
- [市场指令源码排查](xbot-api-docs/docs/debug/market-extension-source.md)
- [钉钉 AI 表格](xbot-api-docs/docs/extensions/activity-5b77c4ce.md)
- [影刀增强工具](xbot-api-docs/docs/extensions/xbot-enhance-tools.md)
- [钉钉企业机器人消息](xbot-api-docs/docs/extensions/dingtalk-bot-message.md)
- [Excel 扩展操作](xbot-api-docs/docs/extensions/activity-excel-v2.md)
- [C-ERP 市场指令](xbot-api-docs/docs/extensions/activity-a90a8311-cerp-visual.md)
- [ERP 订单详情查询与字段翻译](xbot-api-docs/docs/extensions/activity-df0688e4.md)
- [离线 OCR](xbot-api-docs/docs/extensions/activity-179ea575.md)
- [最小可运行示例](xbot-api-docs/examples/README.md)
- [错误修正记录](wiki/error-book.md)
- [待验证事项](wiki/unresolved.md)

## 影刀同步

`shadowbot_sync_tool.py` 位于真实影刀项目根目录，与 `package.json` 同级。

只要真实影刀项目新增了 `.py` 文件，就必须执行；用户说“同步影刀”“执行影刀同步”“同步到影刀”等同类表述时，也都指执行下面的命令，即使本次只修改了已有 `.py` 文件：

```powershell
python shadowbot_sync_tool.py
```

必须区分：

- 命令在真实影刀项目根目录执行
- 同步脚本自动扫描项目根目录下的 Python 文件，不接收文件列表
- “同步影刀”不是 Git commit、Git push 或普通文件复制
- 同步成功不等于业务验证成功
- 最终仍需回到影刀编辑器内实际运行

## 目录结构

```text
AGENTS.md                    # Agent 稳定开发规则
llms.txt                     # AI / LLM 文档索引
README.md                    # 中文项目首页
README_EN.md                 # English overview
CONTRIBUTING.md              # 贡献与验证规范
docs/                        # 入门、工作流、专题和 FAQ
.claude/CLAUDE.md            # Claude Code 入口
.codex/agents/               # Codex 子 Agent 模板
project-template/            # 复制到真实影刀项目根目录的完整模板
  AGENTS.md
  .claude/CLAUDE.md
  .codex/agents/
  shadowbot_sync_tool.py
xbot-api-docs/
  AGENTS.md                  # API 子目录补充规则
  docs/                      # xbot API 技术文档
  examples/                  # 示例
wiki/
  error-book.md              # 历史错误修正
  unresolved.md              # 待验证事项
待优化清单.md                # 后续补充和验证事项
```

## 为什么 AI Agent 需要专门的影刀知识库

传统代码模型通常熟悉 Python、Selenium、Playwright、pandas 或 openpyxl，但不了解当前影刀项目中的：

- xbot 对象来源
- 元素库和资源文件
- 市场指令参数映射
- 影刀编辑器与真实项目目录关系
- 同步工具和验证流程
- 已知限制和历史错误

通过 `AGENTS.md`、`llms.txt`、API 文档和错误修正记录，可以让 Agent 按项目真实规则开发，而不是仅凭相似库经验生成代码。

## 搜索关键词

本仓库覆盖以下中文和英文主题：

**中文：** 影刀、影刀编码版、影刀开发、影刀教程、影刀 xbot、影刀 API、影刀 RPA、RPA 自动化、浏览器自动化、网页自动化、Excel 自动化、WPS 自动化、Windows 自动化、钉钉 AI 表格、市场指令、AI Agent、智能体开发、Claude Code、Codex。

**English:** Yingdao, Yingdao xbot, Yingdao RPA, Yingdao coding mode, xbot API, RPA automation, AI Agent, Agent Coding, browser automation, Excel automation, WPS automation, Windows automation, Claude Code, OpenAI Codex, Python automation.

## 贡献

欢迎提交：

- 已验证的 xbot API 用法
- 浏览器、Excel / WPS 和 Windows 自动化示例
- 市场指令真实参数
- 可复现的错误和 request id
- 错误文档修正
- Agent 工作流和文档导航改进

提交前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)，并确保示例已经脱敏，明确区分“已验证”“源码确认”和“待验证”。

## 免责声明

本仓库为社区整理的开发知识库，不代表影刀官方。影刀版本、市场指令、网页结构和第三方接口可能发生变化，实际行为应以当前运行环境和验证结果为准。

## License

MIT
