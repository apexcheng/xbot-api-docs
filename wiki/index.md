# Wiki 归档入口

本目录只保留影刀 xbot / AI 开发知识库的历史错误和待验证事项。

稳定 API、参数说明、调用示例和开发经验，应优先写入 `xbot-api-docs/docs/` 或 `xbot-api-docs/examples/`。

## 页面索引

- [错误修正记录](error-book.md): 历史错误结论、正确说法、依据和影响范围。
- [待验证事项](unresolved.md): 还没有运行验证、源码验证或业务确认的内容。

## 使用边界

- `wiki/` 不作为默认编码依据。
- Agent 写代码时，应先查看当前项目代码和 `AGENTS.md`；仅当新增或无法确认 xbot API、市场指令、页面行为时，再按 `llms.txt` 定位 `xbot-api-docs/docs/`。
- 只有用户明确询问历史错误、待验证事项，或 API 文档没有答案时，才查 `wiki/`。
- 不确定的 API 行为先标 `需运行验证`，确认后再回写到 `xbot-api-docs/docs/`。
- 不要把真实项目路径、账号、token、Cookie 或其他敏感信息写入 Wiki。
