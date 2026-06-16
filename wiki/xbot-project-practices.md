# 影刀项目协作与实战经验

本文只沉淀跨项目可复用的协作经验、代码风格和常见组织方式，不替代 `xbot-api-docs/docs/` 的稳定 API 文档。

## 1. 协作流程

1. 先遵循根目录 `AGENTS.md`，再用 `llms.txt` 和 `xbot-api-docs/` 定位具体 API 文档。
2. 任务涉及知识库规则、影刀 / RPA 流程、跨文件修改时，可以先收集和当前任务直接相关的规则与证据位置。
3. 完成方案或改动后，复核本次 diff，重点检查有没有过度优化、无关扩写、偏离最小改动。
4. API、字段结构、市场指令参数不确定时，明确标注“需运行验证”，并回到文档或源码核实。
5. Wiki 只写可复用经验和确认过的结论，不写账号、token、Cookie、真实业务数据；未确认事项写到 `wiki/unresolved.md`。

## 2. 钉钉 AI 表格记录结构约定

- 记录列表统一从 `result.get("data", {}).get("records")` 取，不直接从根层 `.get("records")` 取。
- 钉钉记录默认按 `record["fields"]` 使用；调用方已经明确是表格记录时，不要再在业务逻辑里重复做 `isinstance` 兜底。
- 多选字段显示值按 `{"name": "...", "id": "..."}` 结构取 `.get("name")`，不要把整个字典直接当文本用。

示例：

```python
result = table_action("获取多行记录分页", client_id, client_secret, base_id, user_id, sheet="账号表", params={"page_size": 100, "max_pages": 100})
records = result.get("data", {}).get("records") or []
platform = (record["fields"].get("平台") or {}).get("name") or ""
```

## 3. 业务结果与通知解耦

- `process_xxx` 只负责业务处理、表格回写，并返回通知需要的结果列表。
- 通知层统一消费 `notify_records`，现场计算汇总、异常数和明细，不在业务层提前固化更多通知结构。
- 新增平台时，优先保持“业务处理函数返回统一结果结构，通知层零改动”的模式。

建议结果字段：

```python
{
    "platform": "京东",
    "shop": "店铺A",
    "skuid": "123",
    "link": "https://...",
    "target": 99,
    "actual": 109,
    "status": "价格不一致",
    "updates": {"id": "...", "fields": {...}},
}
```

## 4. 最小改动风格

- 优先单函数完整逻辑，少抽象，少间接层。
- 写代码前先问：是否真的需要新函数、新常量、新类、配置层、重试框架、异常体系；不需要就不要写。
- 一个函数如果只被引用 1 次，默认不要抽；一个函数如果只有 1 条语句，默认不要单独封装。
- 已知入参契约明确时，不要在业务逻辑里反复做防御性判断。
- 单次使用的常量、URL、小函数默认直接写使用处，不为“看起来更工程化”而提取。
- 阅读性优先于工程化；如果内联后主流程更直观，就不要为了“结构更漂亮”再包一层函数。
- XPath 失效时优先人工修正定位，不在代码里堆多个候选 XPath 做兜底。
- 项目内 `README.md` 默认是使用说明；没有明确规则要求时，经验沉淀优先写知识库 `wiki/`。

### 代码生成前自检

1. 删除新抽出的函数后，主流程是否仍然清楚？如果是，别抽。
2. 这个新函数是不是只被调用 1 次，或者只有 1 条语句？如果是，别封装。
3. 删除新提的常量后，调用处是否更直观？如果是，别提。
4. 删除 `isinstance` / `dict(...)` / 空结构兜底后，是否仍符合调用方约定？如果是，别兜底。
5. 删除重试、多 XPath、兼容分支后，当前需求是否仍可完成？如果是，别加。
6. 删除新增注释后，代码是否仍能读懂？如果是，别注释。

## 5. 真实项目开发收尾

- 真实影刀项目修改 `.py` 后，必须运行 `shadowbot_sync_tool.py --project-dir "<项目根目录>" prepare <files...>`。
- 这一步会登记 flow 并编译；不执行的话，影刀编辑器可能感知不到新代码。
- `prepare <entry.py>` 会登记传入的入口 `.py` flow，并自动发现入口文件相对 import 的本地 helper 模块一起编译；helper 被编译不等于被登记为独立 flow。
- `prepare` 不自动备份项目；需要备份时单独运行 `backup <files...>`。
- 测试由人类在影刀编辑器中完成，Agent 不要把“已同步”写成“已在编辑器内验证通过”。

最小示例：

```powershell
python C:\Users\Administrator\Desktop\影刀xAI开发指南\shadowbot_sync_tool.py --project-dir "C:\path\to\real_project" prepare main.py run.py
```

## 6. 不建议继承到新项目的内容

- 跨文件 `from .xxx import *`：隐式依赖多，建议显式 import。
- 动态 import 登录模块：`__import__("process7", ...)` 写法不直观，建议直接 import。
- 未分类的全局 `atexit` 钩子：小项目可以，大项目优先显式管理保存时机。
- 硬编码业务字段、店铺名、平台代码、业务 XPath：不应沉淀为通用模式。
- 还没验证能否跨项目复用的内部辅助模式：先写 `wiki/unresolved.md` 标注“需运行验证”。

## 7. 下载等待辅助方法约定

- 下载文件业务统一优先使用市场扩展 `activity_dae43741.browser_utils.wait_download_file(download_dir, filename=None, timeout=300, interval=1)`。
- `filename` 是可选参数：传了就按指定文件名等，不传就按“本次新出现并稳定的文件”判断。
- 不再为同类下载等待业务单独维护旧封装。

## 8. 源表高速只读

- 只读源表、无需公式刷新、无需真实界面交互时，可以优先用 `python-calamine` 直接读 `.xlsm` / `.xlsx`。
- 常见流程是 `CalamineWorkbook.from_path()` -> 检查 `sheet_names` -> `get_sheet_by_name(...).to_python()` -> 取首行做表头 -> 重复列名按后缀去重。
- 这类方案适合做源表清洗、汇总前的数据抓取；它不替代 `xbot.excel` 的写入、保存和真实 WPS / Excel 行为。

## 9. 本地 pytest 测影刀代码

- 本地单测影刀代码时，可以用 `types.ModuleType` 和 `sys.modules.setdefault()` 注入轻量 `xbot`、`xbot.app`、`xbot.selector`、`xbot.primitives`。
- 这种方式适合测纯函数、数据清洗、汇总、Markdown 生成等不依赖真实界面的逻辑。
- 只能把它当成本地测试手段，不能把 pytest 通过直接说成“影刀编辑器内验证通过”。
