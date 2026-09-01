# CLAUDE.md

本文件是 Claude Code 在影刀 xbot / 编码版项目中的协作入口。

根目录 `AGENTS.md` 是唯一主规则入口；Claude Code 执行代码生成、修改、审查和排错时，先遵守 `AGENTS.md`。

本文件只保留 Claude Code 专用补充：

1. 不要把知识库目录当成真实业务项目目录。
2. 真实影刀项目开发时，应打开真实影刀项目根目录工作。
3. 知识库固定路径是 `C:\Users\Administrator\Desktop\影刀xAI开发指南`；开始任务时先确认目录存在，不存在就立即停止并请用户补充正确路径。
4. 当前知识库只用于查规则、API、示例和项目模板。
5. `shadowbot_sync_tool.py` 位于真实项目根目录。新增文件后执行 `python shadowbot_sync_tool.py`。
6. 用户说“同步影刀”“执行影刀同步”“同步到影刀”等同类表述时，均指执行 `python shadowbot_sync_tool.py`。
7. 未运行测试或同步时，最终回复必须明确说明。
8. 不要把静态检查、代码阅读、同步完成描述成真实影刀编辑器内验证通过。
