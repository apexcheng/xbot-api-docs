# 影刀 xbot / AI 开发知识库

本仓库是影刀 xbot / AI 开发知识库，用于整理影刀编码版 API、开发限制、排错方法和示例。

本仓库不是真实影刀项目根目录。Agent 实际开发影刀项目时，应打开真实影刀项目根目录工作。

## 开发后同步

Agent 在真实影刀项目目录完成开发或修改后，必须再运行本仓库根目录的 `shadowbot_sync_tool.py`。

注意：`shadowbot_sync_tool.py` 不在真实影刀项目目录里，调用时不要默认使用当前目录下的相对路径。

最小示例：

```powershell
python "C:\path\to\影刀xAI开发指南\shadowbot_sync_tool.py" --project-dir "%LOCALAPPDATA%\ShadowBot\users\<user_id>\apps\<app_id>" prepare main.py
```

## 怎么使用

1. Agent 先遵循 `AGENTS.md`，了解当前知识库仓库的稳定规则。
2. 再看 `llms.txt`，了解仓库入口和文档索引。
3. 需要写影刀编码版代码时，查 `xbot-api-docs/docs/`。
4. 需要浏览器操作时，查 `xbot-api-docs/docs/browser.md`。
5. 需要表格操作时，查 `xbot-api-docs/docs/excel.md`。
6. 需要市场指令排查时，查 `xbot-api-docs/docs/debug/market-extension-source.md`。
7. 修改真实影刀项目代码后，运行本仓库根目录 `shadowbot_sync_tool.py` 完成同步准备。

## 新应用开发流程

新建一个影刀应用时，推荐按“先把流程写清楚，再让 Agent 开发”的方式推进。

1. 在影刀编辑器中创建新应用，确认真实项目目录。
2. 将根目录 `AGENTS.md`、`.claude/CLAUDE.md`、`.codex/agents/` 按需复制到影刀项目目录。
3. 在项目目录编写开发草稿，说明业务目标、输入输出、页面 / 表格 / 文件路径、人工确认点和失败处理要求。
4. 让 Agent 结合《[如何设计一个可维护的自动化 Agent 工作流](https://apexcheng.github.io/articles/automation-agent-workflow/)》在项目目录生成开发用 Markdown 文件，建议命名为 `TASK.md` 或 `开发草稿.md`。
5. Agent 按开发草稿和 `TASK.md` 开发；每完成一个阶段，更新当前进度、实际改动、未完成事项和风险点。
6. 开发完成后，按需运行本仓库的 `shadowbot_sync_tool.py prepare` 同步准备，再到影刀编辑器内运行验证。

`TASK.md` 只适合新应用、跨多文件、多阶段或不确定性较高的任务。简单改一个函数、调整文案、删除少量规则时，直接按快改方式处理，不要额外引入任务文件。

推荐的 `TASK.md` 内容：

```md
# 当前任务目标

写清最终要实现什么，以及验收标准。

## 执行阶段

- 阶段 1：梳理输入、输出和人工确认点，状态：未开始
- 阶段 2：实现主流程，状态：未开始
- 阶段 3：处理异常和日志，状态：未开始
- 阶段 4：同步准备和影刀内验证，状态：未开始

## 当前进度

记录当前做到哪一步。

## 未完成事项

- 还没处理的页面、表格、文件或业务分支
- 需要继续验证的选择器、参数或市场指令

## 风险 / 待确认

- 可能影响旧流程的地方
- 需要人工确认的取舍
```

## Agent 规则文件

根目录 `AGENTS.md` 是当前知识库仓库的唯一主规则入口，也可复制到真实影刀项目根目录复用。

`.claude/CLAUDE.md` 是 Claude Code 的轻量入口，只桥接到 `AGENTS.md`。

`.codex/agents/` 是 Codex 只读子 Agent 模板，可按需复制到真实项目。

## 目录结构

```text
AGENTS.md
llms.txt
.claude/
  CLAUDE.md
.codex/
  agents/
xbot-api-docs/
  docs/
  examples/
shadowbot_sync_tool.py
待优化清单.md
```
