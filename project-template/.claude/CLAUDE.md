# CLAUDE.md

根目录 `AGENTS.md` 是唯一主规则入口，Claude Code 执行代码生成、修改、审查和排错时先遵守该文件。

Claude Code 专用补充：

1. 知识库固定路径是 `C:\Users\Administrator\Desktop\影刀xAI开发指南`。
2. 开始任务时先确认知识库目录存在；不存在就立即停止并请用户补充正确路径，不要猜测。
3. 先检查当前项目现有代码；仅当新增或无法确认 xbot API、市场指令、页面行为时，再读取知识库中的 `llms.txt` 和相关文档。
4. `shadowbot_sync_tool.py` 位于当前项目根目录。
5. 新增文件后执行 `python shadowbot_sync_tool.py`。
6. 用户说“同步影刀”“执行影刀同步”“同步到影刀”等同类表述时，均指执行该命令。
7. 不要把静态检查或同步完成描述成已在影刀编辑器内验证通过。
