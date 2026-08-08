# 影刀 xbot AI Agent 文档中心

这里是 `yingdao-xbot-ai-agent` 的公开文档入口，面向影刀编码版开发者、RPA 自动化工程师，以及使用 Claude Code、OpenAI Codex、Cursor 等 AI 编程工具开发影刀项目的用户。

> 技术接口细节以 `xbot-api-docs/docs/` 中的现有文档为准。本目录主要负责入门、导航、工作流和问题定位，不重复维护未经验证的 API 说明。

## 快速导航

| 需求 | 推荐文档 |
| --- | --- |
| 第一次使用本仓库 | [影刀 xbot 快速开始](getting-started.md) |
| 使用 AI Agent 开发影刀应用 | [AI Agent 开发工作流](ai-agent-development.md) |
| 新建或重构多数据源报表项目 | [标准流程项目参考](standard-project-reference.md) |
| 查找 xbot API | [xbot API 导航指南](xbot-api-guide.md) |
| 开发网页自动化 | [影刀浏览器自动化指南](browser-automation.md) |
| 操作 Excel 或 WPS | [影刀 Excel / WPS 自动化指南](excel-automation.md) |
| 遇到异常或市场指令问题 | [影刀开发排错指南](troubleshooting.md) |
| 了解常见问题 | [常见问题 FAQ](faq.md) |
| 让 AI 读取仓库 | [`llms.txt`](../llms.txt) |
| 查看 Agent 稳定规则 | [`AGENTS.md`](../AGENTS.md) |

## 核心技术文档

- [基础对象与全局变量](../xbot-api-docs/docs/package.md)
- [浏览器操作](../xbot-api-docs/docs/browser.md)
- [Excel / WPS 表格操作](../xbot-api-docs/docs/excel.md)
- [Windows 桌面自动化](../xbot-api-docs/docs/win32.md)
- [键盘鼠标操作](../xbot-api-docs/docs/keyboard-mouse.md)
- [日志记录](../xbot-api-docs/docs/logging.md)
- [桌面对话框与通知](../xbot-api-docs/docs/notification.md)
- [压缩与解压](../xbot-api-docs/docs/xzip.md)
- [iframe2 扩展指令](../xbot-api-docs/docs/iframe2-extension.md)
- [市场指令与扩展开发](../xbot-api-docs/docs/extension-instructions.md)
- [钉钉 AI 表格](../xbot-api-docs/docs/extensions/activity-5b77c4ce.md)

## 推荐阅读顺序

### 新手

1. [快速开始](getting-started.md)
2. [xbot API 导航指南](xbot-api-guide.md)
3. 先检查真实项目现有代码
4. 仅当新增或无法确认 API、市场指令、页面行为时，选择对应文档
5. 把 `project-template/` 内容复制到真实项目根目录
6. 回到影刀编辑器内验证

### 使用 AI Agent 的开发者

1. [`AGENTS.md`](../AGENTS.md)
2. 真实影刀项目现有代码和业务说明
3. [AI Agent 开发工作流](ai-agent-development.md)
4. 复杂任务使用真实影刀项目中的业务草稿或 `TASK.md`
5. 仅在多个数据源写入同一工作簿并需要统一保存通知时读取 [标准流程项目参考](standard-project-reference.md)
6. 仅在新增或无法确认 API、市场指令、页面行为时使用 [`llms.txt`](../llms.txt) 定位文档

### 排查异常

1. 记录完整错误信息和触发步骤
2. 查 [排错指南](troubleshooting.md)
3. 查对应 API 文档
4. 涉及市场指令时查看 [市场指令源码排查](../xbot-api-docs/docs/debug/market-extension-source.md)
5. 区分“已验证结论”和“待验证推测”

## 本仓库覆盖的搜索主题

影刀开发、影刀编码版、影刀 xbot、影刀 API、影刀 RPA、RPA 自动化、AI Agent、Agent Coding、Claude Code、Codex、浏览器自动化、网页自动化、Excel 自动化、WPS 自动化、Windows 自动化、Python 自动化、市场指令排错、钉钉 AI 表格。

## 仓库定位

本仓库是知识库、规则库、示例库和排错资料集合，不是实际运行的影刀应用目录。开发真实项目时，应在真实影刀项目根目录内修改代码，再使用本仓库提供的同步工具完成收尾。
