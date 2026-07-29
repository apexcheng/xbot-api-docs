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

## 2026-07-29 WPS `set_range()` 固定批次 COM 异常可能是等号文本被当成公式

- 错误说法：WPS 批量写入在不同位置报 `pywintypes.com_error: (-2147352567, '发生意外。', ..., -1880948725)`，通常是 COM 随机不稳定、写入过快或单批数据量太大，应优先增加等待、分批和重试。
- 正确说法：本次实测根因是业务备注字段存在以 `=` 开头的普通文本。WPS 在 `set_range()` 时把它当成公式解析，内容不是合法公式后抛出模糊 COM 异常。写入前给这类文本增加英文单引号，再一次性写入即可成功。
- 依据：两份不同日期、数千行的 CSV 分别稳定失败在不同的 500 行批次；每批连续重试 3 次仍失败；去除日期时区、改用 `csv.reader` 保持纯字符串、把失败批次单独写入新工作簿后仍在同一批次失败。递归按行列二分后，两份数据都只定位到 `线下备注` 中一个以 `=` 开头的单元格；为等号文本增加英文单引号后，两份完整数据均可不分批一次性写入 WPS。
- 影响范围：通过 `xbot.excel` 的 WPS 驱动，将 CSV、接口或业务表中的二维数组写入工作表；尤其是备注、地址、客服说明等自由文本字段。
- 易踩坑：错误位置看起来像随机变化，是因为每天异常备注所在行不同；对同一份数据则会稳定卡在包含异常单元格的固定批次。openpyxl 还可能先暴露日期时区等独立问题，不能因此直接认定它就是 WPS COM 的根因。
- 后续处理：遇到固定批次 COM 异常时，先把失败批次单独写入，再按行列二分到具体单元格；检查以 `=` 开头的业务文本。确认不是公式后使用 `value = "'" + value`，然后继续用 `set_range()` 一次性写二维数组，不需要为了这个问题长期保留分批、等待和重试逻辑。

## 2026-07-12 钉钉 AI 表格 `filter` 失败不是订单号过长

- 错误说法：订单号位数太长，或订单号包含连字符，会导致钉钉 AI 表格 `filter` 无法查询。
- 正确说法：16 位、19 位纯数字订单号和带连字符订单号均已验证可以正常查询。当前主要异常与较大的 `maxResults` / `page_size`，以及零匹配时钉钉接口偶发返回 `HTTP 500 unknownError` 有关。
- 依据：使用 10 个真实订单号覆盖不同长度和格式，在 `maxResults=1` 下分别测试字段名称、字段 ID、单订单号条件，以及“平台 + 订单号 + 商品 ID”三条件查询，共执行 50 次，50 次成功；把同类查询改为 `maxResults=30` 后，大量请求返回 `HTTP 500 unknownError`。同一个确定零匹配的条件也已复现“有时返回空数组、有时返回 500”。
- 影响范围：订单查重、评价记录查询、平台 + 订单号 + 商品 ID 联合查询，以及所有通过 `extra_body.filter` 判断记录是否存在的流程。
- 易踩坑：正常程序员会把“查不到记录”和“查询异常”当成两个概念；但钉钉 AI 表格 `filter` 在当前实测场景下，查不到和真实查询异常都可能表现为 `HTTP 500 unknownError`。因此看到 500 不能直接认定是代码写错，也不能无条件当作无数据，需要结合请求结构、分页参数和业务目标判断。
- 后续处理：存在性查询优先使用 `page_size=1`、`max_pages=1`；顶层使用单数 `filter`；每个条件的 `value` 必须是列表；不要再根据订单号长度判断失败原因；对 500 保留原始查询条件和错误信息，作为“可能零匹配，也可能真异常”的业务分支处理。

## 2026-06-18 影刀项目日志禁止使用 Python 标准 `logging`

- 错误说法：影刀项目里写日志可以沿用 `import logging` + `logging.basicConfig()` + `logger = logging.getLogger(__name__)` 这种 Python 标准库写法。
- 正确说法：影刀项目里写日志时，Python 标准 `logging` 属于错误实现，必须拒绝使用并改为 `from xbot.app import logging`。出现 `import logging`、`logging.basicConfig(...)`、`logging.getLogger(...)`、`logger.info(...)`、`logger.warning(...)`、`logger.error(...)`、`logger.exception(...)` 都应视为需要修正的错误模式。影刀 API 是模块级单例，方法只接受单一 `text` 参数（`logging.info(text)`、`logging.warning(text)`、`logging.error(text)`），需要动态内容时使用 f-string；异常堆栈用 `logging.error(f"...\n{traceback.format_exc()}")`。
- 依据：`xbot-api-docs/docs/logging.md` 明确说明 Python 内置 `print()` 不会自动进入影刀日志面板，标准 `logging` 同理；影刀 API 提供的级别为 `trace / debug / info / success / warning / error`，另有 `export(save_path)` 导出文件。
- 影响范围：所有在真实影刀项目里写过或将要写日志的 Python 文件。`logger = logging.getLogger(...)` 配 `logger.info("x=%s", v)` 这种 printf 风格在影刀进程里不仅不会进日志面板，多写的参数还可能被忽略或报 TypeError。
- 后续处理：知识库顶层 `AGENTS.md` 增补「影刀日志规则」段落，明确 API 与签名；项目级 `xbot_robot/.claude/CLAUDE.md` 同步加规则；扫描已有真实影刀项目代码，发现 stdlib `logging` 引用时按本次经验替换。

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
