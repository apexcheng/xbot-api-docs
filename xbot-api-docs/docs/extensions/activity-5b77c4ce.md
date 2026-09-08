# 钉钉AI表格 (activity_5b77c4ce)

> 调用类型：`direct python`
> 主要入口：直接调用 general_table_action.py 中的 main()；__init__.py 仅做模块导入。
> 证据边界：返回结构和 action 枚举以当前安装版本源码或实测为准。
> 返回：[市场指令索引](../extension-instructions.md)

---

**目录/指令名：** `activity_5b77c4ce` / 钉钉AI表格

**调用方式：** direct python

**用途：** 钉钉多维表格（AI 表格）的增删改查

**调用入口：**
- `xbot_extensions.activity_5b77c4ce.general_table_action.main(args)`
- 底层 SDK：`croe.py` 中的 `yd_ai_table_action()` 及 `yd_*` 系列函数

**通用调用格式：**

```text
非执行调用说明（不可直接运行）：

from xbot_extensions.activity_5b77c4ce.croe import yd_ai_table_action

result = yd_ai_table_action(
    action="创建数据表",
    client_id="你的client_id",
    client_secret="你的client_secret",
    base_id="你的base_id",
    user_id="你的user_id",
    params={...}
)
```

**通用参数：**

| 参数 | 必填 | 说明 |
|---|---|---|
| `action` | 是 | 操作类型（中文 action 名） |
| `client_id` | 是 | 钉钉应用 AppKey |
| `client_secret` | 是 | 钉钉应用 AppSecret |
| `base_id` | 视 action | AI 表格 baseId |
| `sheet` | 视 action | 数据表名称或 ID，**推荐传 ID** |
| `space_id` | 视 action | 钉盘空间 ID |
| `user_id` | 身份三选一 | 推荐传这个，脚本自动转 unionId |
| `operator_id` | 身份三选一 | unionId |
| `sender_union_id` | 身份三选一 | 也可作为操作者身份 |
| `params` | 否 | 业务参数（字典或 JSON 字符串） |

**身份参数：** `user_id`、`operator_id`、`sender_union_id` 至少传一个。普通使用直接传 `user_id`。

---

## 用法速查

Agent 查询钉钉 AI 表格时，先按本节确认调用入口、参数和返回结构；只有返回异常或结果不符合预期时，再看后面的稳定性说明。

| 需求 | 优先查看 | 关键点 |
|---|---|---|
| 调用市场指令 | 通用调用格式、通用参数 | 常用 `yd_ai_table_action()`；至少传 `action`、`client_id`、`client_secret` 和身份参数 |
| 读取记录 | 获取多行记录 / 获取多行记录分页 | 记录列表从 `result.get("data", {}).get("records")` 取 |
| 新增记录 | 新增记录 / 新增多行记录 | `params.record` 或 `params.records` 放业务字段 |
| 更新记录 | 更新记录 / 更新多行记录 | 单行用 `record_id` + `fields`；多行每条记录带 `id` 和 `fields` |
| 条件查询 | 记录筛选 `filter` | `extra_body.filter.conditions`；每个条件的 `value` 必须是列表 |
| 附件字段 | 附件操作 | 上传后用返回的 `attachment` 写入附件字段 |

只有出现返回异常、字段命中不符合预期、分页结果异常时，再看本文后面的稳定性说明和错误示例。

#### Action 详解

##### 数据表操作

**创建数据表**
- `action="创建数据表"`
- `params.sheet_name`（必填）：新数据表名称
- `params.fields`（可选）：初始化字段列表，每项含 `name` 和 `type`

```json
{
  "sheet_name": "测试数据表",
  "fields": [
    {"name": "标题", "type": "text"},
    {"name": "金额", "type": "number"}
  ]
}
```

**获取所有数据表**
- `action="获取所有数据表"`
- 仅需 `base_id`

**获取数据表**
- `action="获取数据表"`
- `params.sheet`（必填）：数据表 ID

**更新数据表**
- `action="更新数据表"`
- `params.sheet`（必填）、`params.new_name`（必填）

**删除数据表**
- `action="删除数据表"`
- `params.sheet`（必填）

---

##### 字段操作

**新增字段**
- `action="新增字段"`
- `params.sheet`、`params.field_name`（必填）
- `params.field_type`（可选，默认 `text`）：`text`、`number`、`date`、`checkbox`、`singleSelect`、`multipleSelect`、`attachment`
- `params.field_property`（可选）：字段属性字典

```json
{
  "sheet": "rPbLtRx",
  "field_name": "金额",
  "field_type": "number"
}
```

**获取所有字段**
- `action="获取所有字段"`
- `params.sheet`（必填）

**更新字段**
- `action="更新字段"`
- `params.sheet`、`params.field`（字段 ID，推荐）
- `params.new_name`、`params.field_type`、`params.field_property` 至少传一个

**删除字段**
- `action="删除字段"`
- `params.sheet`、`params.field`（必填）

---

##### 记录操作

**新增多行记录**
- `action="新增多行记录"`
- `params.sheet`、`params.records`（必填）

```json
{
  "sheet": "rPbLtRx",
  "records": [
    {"标题": "第一行", "金额": 1},
    {"标题": "第二行", "金额": 2}
  ]
}
```

**新增记录**
- `action="新增记录"`
- `params.sheet`、`params.record`（必填）

**获取多行记录**
- `action="获取多行记录"`
- `params.sheet`（必填）
- `params.max_results`（可选，1~100）
- `params.next_token`（可选）：分页游标
- `params.extra_body`（可选）：传筛选条件等额外请求体参数

**获取多行记录分页**
- `action="获取多行记录分页"`
- `params.sheet`（必填）
- `params.page_size`（可选）、`params.max_pages`（可选）
- `params.extra_body`（可选）：传筛选条件等额外请求体参数

###### 记录筛选 `filter`

已验证的筛选结构：

```text
非执行调用说明（不可直接运行）：

params = {
    "page_size": 1,
    "max_pages": 1,
    "extra_body": {
        "filter": {
            "combination": "and",
            "conditions": [
                {
                    "field": "平台",
                    "operator": "equal",
                    "value": ["淘宝"],
                },
                {
                    "field": "订单号",
                    "operator": "equal",
                    "value": ["3300000000000000000"],
                },
                {
                    "field": "商品ID",
                    "operator": "equal",
                    "value": ["900000000000"],
                },
            ],
        }
    },
}
```

调用示例：

```text
非执行调用说明（不可直接运行）：

result = yd_ai_table_action(
    action="获取多行记录分页",
    client_id=client_id,
    client_secret=client_secret,
    base_id=base_id,
    user_id=user_id,
    sheet="评价收集明细",
    params=params,
)
```

已验证规则：

| 项目 | 正确用法 |
|---|---|
| 顶层参数名 | 使用单数 `filter`，不要写成 `filters` |
| 条件组合 | `combination: "and"` |
| 条件列表 | `conditions` |
| 字段 | 可传字段名称或字段 ID |
| 文本 / 单选匹配 | 使用 `operator: "equal"` |
| `value` | 必须是列表，即使只有一个值 |
| 单选字段值 | 显示名称或选项 ID 均已验证可用 |

错误示例：

```text
非执行调用说明（不可直接运行）：

# 错误：filters 复数可能被接口静默忽略，结果相当于未筛选
{"filters": {"combination": "and", "conditions": [...]}}

# 错误：value 不是列表，会返回 JSON Array parsing error
{"field": "订单号", "operator": "equal", "value": "3300000000000000000"}
```

存在性查询或查重只需要确认是否有记录时，推荐：

```text
非执行调用说明（不可直接运行）：

{
    "page_size": 1,
    "max_pages": 1,
    "extra_body": {"filter": {...}},
}
```

不要因为订单号位数长或包含连字符，就判断 `filter` 无法查询。已实测 16 位、19 位纯数字订单号和带连字符订单号均可正常命中。

当前接口存在两个已验证的稳定性问题：

1. 携带 `filter` 时，较大的 `maxResults` / `page_size` 更容易触发 `HTTP 500 unknownError`。对于只需要判断记录是否存在的查询，优先设置为 `1`。
2. 筛选结果为零条时，接口有时返回正常空数组，有时错误返回 `HTTP 500 unknownError`。因此 `500` 不一定表示 `filter` 结构错误，也可能是零匹配触发的钉钉后端异常。

`HTTP 500 unknownError` 是歧义失败，不能当成“没有匹配记录”。存在性查询只有在请求成功且明确返回空结果时，才能判定未命中；遇到 `500` 应保留查询条件和原始错误，并按业务风险重试、停止或交由人工确认，避免误新增重复数据。

如果需要获取所有满足条件的记录，不要直接假设较大 `page_size` 稳定可用；应先在当前表和当前租户中运行验证，再决定分页参数和重试策略。

**获取记录**
- `action="获取记录"`
- `params.sheet`、`params.record_id`（必填）

**更新记录**
- `action="更新记录"`
- `params.sheet`、`params.record_id`、`params.fields`（必填）

```json
{
  "sheet": "rPbLtRx",
  "record_id": "44jzHpsgbx",
  "fields": {"金额": 100, "状态": "已更新"}
}
```

**更新多行记录**
- `action="更新多行记录"`
- `params.sheet`、`params.records`（必填）
- 每条记录必须带 `id`（也接受 `recordId`、`record_id`）

```json
{
  "sheet": "rPbLtRx",
  "records": [
    {"id": "44jzHpsgbx", "fields": {"金额": 100}},
    {"id": "nApqiOPYVe", "fields": {"金额": 101}}
  ]
}
```

**删除多条记录**
- `action="删除多条记录"`
- `params.sheet`、`params.record_ids`（必填，列表或逗号字符串）

---

##### 附件操作

附件上传流程（脚本自动完成）：
1. 申请上传信息 → 2. PUT 上传文件 → 3. 将 `resourceId` 写入附件字段

附件字段值格式：
```json
[{"filename": "demo.pdf", "resourceId": "xxx"}]
```

**上传附件**
- `action="上传附件"`
- `params.file_path`（必填）
- `params.filename`、`params.mime_type`（可选）
- `params.upload_info`（可选）：一般不用传，脚本自动申请

```json
{
  "file_path": "/tmp/demo.pdf",
  "filename": "demo.pdf",
  "mime_type": "application/pdf"
}
```

返回 `result.attachment` 可直接用于后续写入附件字段。

**上传附件并新增记录**
- `action="上传附件并新增记录"`
- `params.sheet`、`params.attachment_field`、`params.file_path`（必填）
- `params.fields`（可选）：其他普通字段

**上传附件并更新记录**
- `action="上传附件并更新记录"`
- `params.sheet`、`params.record_id`、`params.attachment_field`、`params.file_path`（必填）

---

##### 空间与文件操作

**获取空间列表**
- `action="获取空间列表"`（别名：`"获取space_id"`、`"获取spaceId"`）
- `params.max_results`（可选，1~50）、`params.space_type`（可选，默认 `org`）

**获取空间列表分页**
- `action="获取空间列表分页"`
- `params.page_size`、`params.max_pages`（可选）

**获取空间信息**
- `action="获取空间信息"`
- `params.space_id`（必填）

**获取文件列表**
- `action="获取文件列表"`
- `params.space_id`（必填）、`params.parent_id`（可选）

**获取文件列表分页**
- `action="获取文件列表分页"`
- `params.space_id`（必填）

**获取AI表格列表 / 搜索AI表格 / 搜索表格文件**
- `action="获取AI表格列表"` / `"搜索AI表格"` / `"搜索表格文件"`
- `params.space_id`（必填）、`params.keyword`（可选）
- `params.only_ai_table_candidates`（可选）：是否只保留看起来像 AI 表格的文件

> 文件接口通常需要钉钉应用开通 `Drive.File.Read` 权限。

---

**注意事项：**
- `sheet`、`field`、`record_id` 虽然支持"名称或 ID"，但**推荐优先传 ID**
- `更新多行记录` 时每条记录必须带 `id`（或 `recordId` / `record_id`）
- 使用记录筛选时，顶层参数必须是单数 `filter`，每个条件的 `value` 必须是列表
- 存在性查询优先使用 `page_size=1`、`max_pages=1`；不要把订单号长度误判为筛选失败原因
- `__init__.py` 没有包装函数，直接调用 `general_table_action.py` 中的 `main()` 或 import `croe.py` 的函数
- 如需更精细控制，可直接 import `croe.py` 中的函数
- 获取多行记录时，记录列表从 `result.get("data", {}).get("records")` 取；记录业务字段在 `record["fields"]` 中。
- 多选或选项字段常见结构为 `{"name": "...", "id": "..."}`，显示值取 `name`。

---
