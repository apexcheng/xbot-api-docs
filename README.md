# 影刀 xbot AI 开发知识库

这是一个面向 AI Agent 的影刀 xbot / 编码版开发知识库，集中保存稳定开发规则、已核验 API 事实和市场指令资料，帮助 Agent 少猜 API、少复制过时经验。

它适合使用 Codex、Claude Code、Cursor 等工具维护影刀自动化项目的开发者。本仓库不是影刀官方文档，也不是实际运行的影刀应用目录。

## 从哪里开始

1. 先读 [AGENTS.md](AGENTS.md)，了解所有项目通用的稳定规则。
2. 需要确认 API 或市场指令时，从 [llms.txt](llms.txt) 按任务直达对应文档。
3. 贡献或修正文档前，读 [CONTRIBUTING.md](CONTRIBUTING.md)。
4. API 事实集中在 [xbot-api-docs](xbot-api-docs/docs/) 中。

真实影刀项目保存业务代码、资源和 `package.json`；本仓库只提供规则、知识和模板。修改业务时应进入用户指定的真实项目，不要把知识库当作项目目录。

新项目只需从 `project-template/` 复制以下两个文件到真实项目根目录，与 `package.json` 同级：

```text
AGENTS.md
shadowbot_sync_tool.py
```

真实项目新增 `.py` 文件，或用户要求“同步影刀”时，在真实项目根目录执行：

```powershell
python shadowbot_sync_tool.py
```

同步成功不等于已经在影刀编辑器中运行验证。
