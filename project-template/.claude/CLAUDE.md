# CLAUDE.md

@../AGENTS.md

以上 `AGENTS.md` 是当前影刀项目的唯一主规则入口。Claude Code 执行生成、修改、审查和排错时必须遵守，不得以通用工程化、模块化或抽象化偏好覆盖其中的代码结构规则；不在这里复制另一套规则。

需要确认 xbot API、市场指令、base 骨架或排错资料时，使用用户或项目提供的知识库路径，再按其 `llms.txt` 直达对应页面；路径未提供时不猜测。

读取旧版影刀可视化编排项目时，使用 `.claude/skills/xbot-visual-flow-reader/SKILL.md`；纯 Python 任务不触发该 Skill。

新增 `.py` 文件或用户要求“同步影刀”时，在项目根目录执行 `python shadowbot_sync_tool.py`，不传文件列表。不把同步或静态检查描述成已在影刀编辑器中运行验证。
