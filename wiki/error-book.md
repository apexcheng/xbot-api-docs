# 错误修正记录

记录历史错误结论，避免后续重复犯错。

## 记录格式

```md
## YYYY-MM-DD 错误标题

- 错误说法：
- 正确说法：
- 依据：
- 影响范围：
- 后续处理：
```

## 记录列表

## 2026-06-17 `package.resources` 不应写成下标访问

- 错误说法：`package.resources["模板.xlsx"]`、`package.resources["config.json"]` 这类下标写法可以直接使用。
- 正确说法：当前知识库按本机可见 `xbot.primitives.ResourceReader` 方法整理，应使用 `get_path()`、`get_text()`、`get_bytes()`、`copy_to()`、`copy_to_clipboard()`；不应把 `package.resources` 当成字典使用。
- 依据：`C:\Program Files\ShadowBot\shadowbot-6.0.30\Resources\Code-Activity\Zh-CN\xbot\primitives.py` 中当前可见 `ResourceReader` 公开方法为 `get_text`、`get_path`、`get_bytes`、`copy_to`、`copy_to_clipboard`，未见 `__getitem__`。
- 影响范围：知识库中所有 `package.resources` 用法说明与示例。
- 后续处理：统一删除 `package.resources["xxx"]` 示例，改为方法调用写法；后续若发现版本差异，再按实测结果补充“需运行验证”说明。

## 2026-06-16 钉钉 AI 表格返回结构不要套用到所有市场指令

- 错误说法：封装市场指令时，可以先统一假设返回值都是 `dict`。
- 正确说法：市场指令的返回值结构必须按单个指令的文档、源码或实测结果判断，不能把某一个指令的返回结构泛化成所有市场指令的通用规则。
- 依据：当前项目里 `yd_ai_table_action` 的封装确实按 `dict` 处理，但这只是钉钉 AI 表格指令的已验证行为，不能外推到其他市场指令。
- 影响范围：所有依赖市场指令的编码版封装。
- 后续处理：新增或改造市场指令调用时，先确认该指令的真实返回结构，再决定是否做类型校验。

## 2026-06-16 钉钉 AI 表格多选字段显示值取 name

- 错误说法：AI 表格多选 / 选项字段可以直接当字符串使用。
- 正确说法：已验证的钉钉 AI 表格多选字段在当前项目里常见为 `{"name": "...", "id": "..."}`，显示值应取 `.get("name")`。
- 依据：当前项目读取表格 `平台` 字段时采用该结构。
- 影响范围：所有读取钉钉 AI 表格选项字段的编码版逻辑。
- 后续处理：开发前仍需用真实返回数据确认字段结构，不要仅凭经验假设。
