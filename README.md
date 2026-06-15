# 影刀 xbot / AI 开发知识库

本仓库是影刀 xbot / AI 开发知识库，用于整理影刀编码版 API、开发限制、排错方法和示例。

本仓库不是真实影刀项目根目录。Agent 实际开发影刀项目时，应打开真实影刀项目根目录工作。

## 开发后同步

Agent 在真实影刀项目目录完成开发或修改后，必须再运行本仓库根目录的 `shadowbot_sync_tool.py`。

注意：`shadowbot_sync_tool.py` 不在真实影刀项目目录里，调用时不要默认使用当前目录下的相对路径。

最小示例：

```powershell
python C:\Users\Administrator\Desktop\影刀xAI开发指南\shadowbot_sync_tool.py --project-dir "%LOCALAPPDATA%\ShadowBot\users\<user_id>\apps\<app_id>" prepare main.py
```

## 怎么使用

1. Agent 先遵循 `AGENTS.md`，了解当前知识库仓库的稳定规则。
2. 再看 `llms.txt`，了解仓库入口和文档索引。
3. 需要写影刀编码版代码时，查 `xbot-api-docs/docs/`。
4. 需要浏览器操作时，查 `xbot-api-docs/docs/browser.md`。
5. 需要表格操作时，查 `xbot-api-docs/docs/excel.md`。
6. 需要市场指令排查时，查 `xbot-api-docs/docs/debug/market-extension-source.md`。
7. 修改真实影刀项目代码后，运行本仓库根目录 `shadowbot_sync_tool.py` 完成同步准备。

## Agent 模板

`templates/AGENTS.md` 是可复制到真实影刀项目根目录的通用 Agent 规则模板，适用于 OpenClaw、Codex、Claude Code 等 Agent。

模板文件不参与本知识库检索；当前知识库仓库的规则入口始终是根目录 `AGENTS.md`。

## 目录结构

```text
AGENTS.md
llms.txt
templates/
  AGENTS.md
xbot-api-docs/
  docs/
  examples/
shadowbot_sync_tool.py
待优化清单.md
```
