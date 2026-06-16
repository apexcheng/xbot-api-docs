# Agent 模板约定

本文沉淀 `templates/` 目录中 Agent 模板的使用边界和长期约定，不替代根目录 `AGENTS.md`。

## 1. 模板只用于复制到真实项目

- `templates/AGENTS.md` 可复制到真实影刀项目根目录，作为通用 Agent 规则模板。
- `templates/.claude/CLAUDE.md` 可复制到真实项目 `.claude/CLAUDE.md`，用于 Claude Code 读取同一套协作偏好。
- `templates/.codex/agents/` 可复制到真实项目 `.codex/agents/`，作为 Codex 只读子 agent 模板。
- 模板目录不参与当前知识库自身规则加载；当前知识库的稳定规则入口始终是根目录 `AGENTS.md`。

## 2. 真实项目中的规则优先级

- 真实项目同时存在 `AGENTS.md` 和工具专用规则文件时，以项目根目录 `AGENTS.md` 作为主规则入口。
- 工具专用文件只同步核心偏好，避免和主规则维护两套互相冲突的细节。
- 如果模板和真实项目已有规则冲突，先按真实项目规则执行，再考虑是否需要人工同步模板。

## 3. 子 agent 职责边界

- `implementation_reviewer` 是只读审查角色，只看本轮 diff 和项目规则，不直接改代码。
- `knowledge_base_researcher` 是只读检索角色，只返回和当前问题直接相关的知识库规则、约束和证据位置。
- 子 agent 不应替主 agent 做无关架构建议、扩大修改范围或引入新依赖。

## 4. 模板内应保留的核心偏好

- 最小改动、少工程化、不要无关重构。
- 写影刀编码版代码前先查 `xbot-api-docs`。
- 不确定 API 行为时标注“需运行验证”。
- 浏览器业务默认用 `xbot.web`，不擅自改用网络请求库。
- 真实影刀项目修改 `.py` 后运行 `shadowbot_sync_tool.py prepare` 同步收尾。

## 5. 不适合写进模板的内容

- 当前业务项目的账号、路径、token、Cookie、店铺名、平台字段、业务 XPath。
- 未验证的内部辅助模式。
- 某个项目临时使用的一次性字段名、URL、参数默认值。
- 完整 API 参数表；这些内容应留在 `xbot-api-docs/docs/`。

## 6. 维护建议

- 模板只放跨项目稳定规则，不追求覆盖所有细节。
- 新增长期经验时，先判断是主规则、Wiki 经验、稳定 API 文档，还是模板规则。
- 如果只是解释为什么这么做，优先写 Wiki；如果是每个 Agent 进入项目都必须遵守的硬规则，再同步到模板。
