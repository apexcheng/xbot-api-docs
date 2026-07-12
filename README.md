# 影刀 xbot AI Agent 开发指南

> 面向 AI 编程 Agent 的影刀编码版开发知识库。
>
> 整理影刀 xbot / RPA 自动化开发过程中的 API、浏览器自动化、Excel 操作、调试排错、Agent Coding 规范和最佳实践。

[![AI Agent](https://img.shields.io/badge/AI-Agent-blue)]()
[![RPA](https://img.shields.io/badge/RPA-Automation-green)]()
[![xbot](https://img.shields.io/badge/xbot-Yingdao-orange)]()

## 📖 项目简介

这是一个 **影刀 xbot AI Agent 开发知识库**，目标是帮助开发者使用 Claude Code、Codex 等 AI 编程 Agent 开发和维护影刀自动化项目。

本仓库不是实际运行的影刀项目，而是 Agent 开发时使用的知识、规则和工具集合。

核心内容包括：

- 影刀编码版 API 文档
- xbot 开发示例
- RPA 自动化开发规范
- 浏览器自动化方案
- Excel / 表格自动化处理
- 常见错误排查
- AI Agent 开发工作流
- Claude Code / Codex 使用规范

## 🔍 Keywords

影刀、影刀编码版、影刀 xbot、影刀 API、影刀开发、影刀教程、影刀 RPA、RPA 自动化、AI Agent、Agent Coding、Claude Code、Codex、Browser Automation、Excel Automation。

## 🚀 使用方式

AI Agent 推荐按照以下顺序读取：

1. 阅读 `AGENTS.md`
   - 了解项目开发规则和稳定约束。

2. 阅读 `llms.txt`
   - 获取知识库索引。

3. 查询 `xbot-api-docs/docs/`
   - 获取影刀编码版 API。

4. 浏览器自动化开发
   - 查看 `xbot-api-docs/docs/browser.md`

5. Excel / 表格处理
   - 查看 `xbot-api-docs/docs/excel.md`

6. 问题排查
   - 查看 `xbot-api-docs/docs/debug/`

## 🧩 AI Agent 开发流程

推荐工作方式：

```
需求分析
    ↓
编写 TASK.md / 开发草稿
    ↓
AI Agent 分析项目
    ↓
Agent 编码实现
    ↓
运行同步工具
    ↓
影刀环境验证
```

适用于：

- 新建影刀自动化应用
- 修改复杂流程
- 多文件项目维护
- 浏览器自动化
- 数据处理自动化

## 📁 项目结构

```
AGENTS.md                 # Agent 开发规则
llms.txt                  # AI 知识库入口
.claude/                  # Claude Code 配置入口
.codex/                   # Codex Agent 模板
xbot-api-docs/            # xbot API 文档
  docs/
  examples/
shadowbot_sync_tool.py    # 项目同步工具
待优化清单.md
```

## 🤖 Agent 支持

本项目针对以下 AI 编程工具设计：

- Claude Code
- OpenAI Codex
- Cursor
- 其他支持 AGENTS.md / llms.txt 的 AI Agent 工具

## 🛠️ 开发后同步

Agent 在真实影刀项目目录完成修改后，需要运行同步工具：

```powershell
python "C:\path\to\yingdao-xbot-ai-agent\shadowbot_sync_tool.py" prepare main.py
```

注意：

`shadowbot_sync_tool.py` 位于本知识库仓库中，不在真实影刀项目目录中。

## 🌟 为什么需要 AI Agent + 影刀

传统 RPA 开发通常依赖人工拖拽流程。

结合 AI Agent 后，可以实现：

- 自然语言描述需求
- Agent 分析业务流程
- 自动生成 xbot 代码
- 自动排查错误
- 持续维护自动化项目

这是一种面向未来的 **AI 驱动 RPA 开发方式**。

## 📚 推荐阅读

- AI Agent 工作流设计
- 自动化项目工程化实践
- 浏览器自动化最佳实践
- RPA 与大模型结合方案

## License

MIT
