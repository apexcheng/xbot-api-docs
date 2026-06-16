# LLM Wiki 总入口

本目录用于沉淀影刀 xbot / AI 开发知识库中的跨文档总结、常见坑点、错误修正和待验证事项。

`xbot-api-docs/docs/` 是稳定 API 文档层；`wiki/` 是 LLM 维护的整理层。

## 页面索引

- [影刀项目协作与实战经验](xbot-project-practices.md): 沉淀知识库检索路径、最小改动约束、钉钉 AI 表格字段约定、通知解耦模式和真实项目收尾要求。
- [浏览器自动化常见踩坑](browser-automation-pitfalls.md): 沉淀 `xbot.web`、元素操作、剪贴板输入、下载等待、登录态和页面清理的跨项目经验。
- [Excel 与表格处理经验](excel-table-practices.md): 沉淀 Excel/WPS/openpyxl/calamine、二维数组写入和字段边界经验。
- [市场指令排查与返回结构边界](market-extension-debug-practices.md): 沉淀市场指令源码排查、编码版参数确认和返回结构适用范围。
- [Agent 模板约定](agent-template-conventions.md): 沉淀 `templates/` 的使用边界、真实项目规则优先级和只读子 agent 职责。
- [错误修正记录](error-book.md): 历史错误结论、正确说法、依据和影响范围。
- [待验证事项](unresolved.md): 还没有运行验证、源码验证或业务确认的内容。

## 使用边界

- 已确认、可直接作为开发依据的 API 说明，写 `xbot-api-docs/docs/`。
- 可复制运行的完整代码示例，写 `xbot-api-docs/examples/`。
- 根规则入口和硬性约束，写根目录 `AGENTS.md`；Wiki 只做经验整理和解释。
- 跨文档总结、常见坑点、历史纠错和待验证内容，先写 `wiki/`。
- 不确定的 API 行为先标 `需运行验证`，确认后再回写到 `xbot-api-docs/docs/`。
- 不要把真实项目路径、账号、token、Cookie 或其他敏感信息写入 Wiki。
