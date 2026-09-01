# 影刀 xbot 快速开始：使用 AI Agent 开发影刀编码版项目

本文面向第一次使用本仓库的开发者，说明如何让 Claude Code、OpenAI Codex、Cursor 或其他 AI 编程 Agent 正确读取影刀 xbot 开发资料，并在真实影刀项目中完成修改。

## 先理解两个目录

开发时通常会同时存在两个目录：

### 1. 知识库目录

也就是本仓库：

```text
yingdao-xbot-ai-agent/
```

它负责保存：

- `AGENTS.md`：Agent 开发规则
- `llms.txt`：文档索引
- `xbot-api-docs/`：影刀 xbot API 文档与示例
- `project-template/`：复制到真实项目根目录的规则和 Agent 配置
- 调试记录、历史错误和待验证事项

### 2. 真实影刀项目目录

这是影刀应用实际运行的项目目录，常见位置类似：

```text
%LOCALAPPDATA%\ShadowBot\users\<user_id>\apps\<app_id>\xbot_robot
```

真实业务代码、流程文件和应用资源应在这里修改。

> 不要把知识库目录当成真实影刀项目目录，也不要只修改知识库中的示例文件后就认为真实应用已经更新。

## 推荐准备方式

### 步骤 1：确认真实项目目录

先在影刀编辑器或本机目录中确认当前应用对应的真实项目路径。

确认点：

- 目录中存在当前应用实际使用的代码文件
- 修改该目录后，能够通过影刀编辑器进行验证
- 不要仅凭目录名称猜测项目路径

### 步骤 2：复制项目模板

把知识库 `project-template/` 目录中的内容复制到真实影刀项目根目录：

```text
AGENTS.md
.claude/
.codex/
```

不要复制知识库根目录的 `.claude/settings.local.json`，它包含本机权限配置，不属于通用模板。

### 步骤 3：让 Agent 读取规则和索引

建议向 Agent 明确提供：

```text
知识库：C:\Users\Administrator\Desktop\影刀xAI开发指南
真实项目：C:\path\to\real-shadowbot-project

先读取真实项目根目录中的 AGENTS.md。
先确认知识库目录存在；若不存在，立即停止并让我补充正确路径。
再检查真实项目现有代码并完成修改。
仅当新增或无法确认 xbot API、市场指令、页面行为时，
再按 llms.txt 定位相关文档。
```

Agent 应按以下顺序处理：

1. 读取真实项目根目录中的 `AGENTS.md`。
2. 检查真实项目现有代码和业务说明。
3. 确认固定知识库路径存在；不存在就停止并要求用户补充。
4. 仅当新增或无法确认 xbot API、市场指令、页面行为时，再按知识库中的 [`llms.txt`](../llms.txt) 定位相关文档。

### 步骤 4：判断是否需要 TASK.md

`TASK.md` 不是复杂任务的默认要求。以下情况适合创建 `TASK.md`：

- 任务需要跨会话持续推进
- 阶段较多，需要持久化当前进度
- 存在较多待确认事项或长期未完成事项
- 用户明确要求记录实施过程

普通多文件修改、一次会话内可以完成的复杂任务，只需先给简短计划，不需要额外创建任务文件。简单修改同样不需要，例如：

- 修改一个函数
- 调整少量参数
- 修正一条错误描述
- 修改一段提示文案

## TASK.md 最小模板

```md
# 当前任务目标

写清最终需要实现什么，以及怎样算完成。

## 执行阶段

- 阶段 1：确认输入、输出和人工确认点，状态：未开始
- 阶段 2：实现主流程，状态：未开始
- 阶段 3：处理异常和日志，状态：未开始
- 阶段 4：同步准备和影刀内验证，状态：未开始

## 当前进度

记录当前已经完成的内容。

## 未完成事项

- 尚未实现的业务分支
- 尚未验证的页面、表格或接口行为

## 风险 / 待确认

- 可能影响旧流程的改动
- 需要人工确认的参数或业务规则
```

## 根据任务选择文档

| 开发任务 | 入口 |
| --- | --- |
| xbot 基础对象、全局变量和资源 | [`package.md`](../xbot-api-docs/docs/package.md) |
| 网页、元素、Cookie、下载、网络监听 | [`browser.md`](../xbot-api-docs/docs/browser.md) |
| Excel / WPS 读写和格式 | [`excel.md`](../xbot-api-docs/docs/excel.md) |
| Windows 窗口和桌面自动化 | [`win32.md`](../xbot-api-docs/docs/win32.md) |
| 键盘、鼠标、滚轮和剪贴板 | [`keyboard-mouse.md`](../xbot-api-docs/docs/keyboard-mouse.md) |
| 日志输出 | [`logging.md`](../xbot-api-docs/docs/logging.md) |
| 对话框和通知 | [`notification.md`](../xbot-api-docs/docs/notification.md) |
| 市场指令异常 | [`market-extension-source.md`](../xbot-api-docs/docs/debug/market-extension-source.md) |
| 钉钉 AI 表格 | [`activity-5b77c4ce.md`](../xbot-api-docs/docs/extensions/activity-5b77c4ce.md) |

## 开发过程中的基本原则

### 先读现有代码

不要在没有读取真实项目现有实现的情况下，直接生成一套全新的结构。

### 只改当前需求相关内容

避免顺手重构无关文件、替换现有风格或删除与当前问题无关的代码。

### API 用法必须有依据

先检查真实项目现有代码。仅当新增或无法确认 xbot API、市场指令、页面行为时，再按 `llms.txt` 定位文档、示例或市场指令源码，不要凭相似库的用法猜测。

### 区分已验证与待验证

- 已经在影刀环境中运行通过：可记录为已验证
- 只阅读源码或文档：应说明依据
- 仅根据错误现象推测：应标记为待验证

## 最终验收清单

- [ ] 修改发生在真实影刀项目目录
- [ ] Agent 已读取 `AGENTS.md` 并检查真实项目现有代码
- [ ] 没有改动无关代码
- [ ] 关键参数和调用方式有现有代码、文档或源码依据
- [ ] 已在影刀环境中实际验证
- [ ] 未验证结论已经明确标记

## 下一步

继续阅读：

- [AI Agent 开发工作流](ai-agent-development.md)
- [xbot API 导航指南](xbot-api-guide.md)
- [影刀开发排错指南](troubleshooting.md)
