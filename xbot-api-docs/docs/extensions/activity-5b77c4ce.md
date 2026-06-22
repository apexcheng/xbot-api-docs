# 钉钉AI表格 (activity_5b77c4ce)

> 调用类型：`direct python`  
> 主要入口：直接调用 general_table_action.py 中的 main()；__init__.py 仅做模块导入。  
> 来源说明：本页由原 extension-instructions.md 的 4.2 节拆出；返回结构和 action 枚举以当前源码或实测为准。  
> 返回：[市场指令扩展开发指南](../extension-instructions.md)

---

**目录/指令名：** `activity_5b77c4ce` / 钉钉AI表格

**调用方式：** direct python

**用途：** 钉钉多维表格（AI 表格）的增删改查

**调用入口：**
- `xbot_extensions.activity_5b77c4ce.general_table_action.main(args)`
- 底层 SDK：`croe.py` 中的 `yd_ai_table_action()` 及 `yd_*` 系列函数

**通用调用格式：**

```python
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

**获取多行记录分页**
- `action="获取多行记录分页"`
- `params.sheet`（必填）
- `params.page_size`（可选）、`params.max_pages`（可选）

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
- `__init__.py` 没有包装函数，直接调用 `general_table_action.py` 中的 `main()` 或 import `croe.py` 的函数
- 如需更精细控制，可直接 import `croe.py` 中的函数

**典型调用方式：**
```python
from xbot_extensions.activity_5b77c4ce.croe import yd_ai_table_action

# 创建数据表
result = yd_ai_table_action(
    action="创建数据表",
    client_id="xxx", client_secret="xxx",
    base_id="xxx", user_id="xxx",
    params={"sheet_name": "新表", "fields": [{"name": "标题", "type": "text"}]}
)

# 新增记录
result = yd_ai_table_action(
    action="新增记录",
    client_id="xxx", client_secret="xxx",
    base_id="xxx", user_id="xxx",
    params={"sheet": "rPbLtRx", "record": {"标题": "测试", "金额": 100}}
)

# 获取记录列表（自动分页）
result = yd_ai_table_action(
    action="获取多行记录分页",
    client_id="xxx", client_secret="xxx",
    base_id="xxx", user_id="xxx",
    params={"sheet": "rPbLtRx", "page_size": 50, "max_pages": 10}
)
```

**项目里的推荐包装方式：**

```python
def table_action(action, client_id, client_secret, base_id, user_id, sheet, params=None):
    from xbot_extensions.activity_5b77c4ce.croe import yd_ai_table_action

    result = yd_ai_table_action(
        action=action,
        client_id=client_id,
        client_secret=client_secret,
        base_id=base_id,
        user_id=user_id,
        sheet=sheet,
        params=params or {},
    )
    if not isinstance(result, dict):
        raise ValueError(f"表格操作 {action} 返回异常: {result!r}")
    return result


records = table_action(
    "获取多行记录分页",
    client_id, client_secret, base_id, user_id,
    sheet="账号表",
    params={"page_size": 100, "max_pages": 100},
).get("data", {}).get("records") or []
```

补充约定：

- 项目里更推荐先统一封装 `yd_ai_table_action()`，再让业务层读取 `data.records`。
- 记录结构进入业务逻辑后，优先直接按 `record["fields"]` 使用；多选字段显示值取 `.get("name")`。

---
