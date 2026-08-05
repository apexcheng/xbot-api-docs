# Excel扩展操作 (activity_excel_v2)

> 调用类型：`flow`  
> 主要入口：主要通过 __init__.py 包装入口调用 Visual / Code flow；refresh_pivot_table 为模块导入入口。  
> 来源说明：本页由原 extension-instructions.md 的 4.9 节拆出；编码版调用前建议用 inspect.signature() 核对当前安装版本。  
> 返回：[市场指令扩展开发指南](../extension-instructions.md)

---

**目录/指令名：** `activity_excel_v2` / Excel扩展操作

**调用方式：** flow

**用途：** 补充原生 Excel 操作之外的常见表格处理能力，如公式填充、筛选、文本数字转换、图片操作、合并单元格、透视表刷新等。

**调用入口：**
- Visual flow 包装入口：`xbot_extensions.activity_excel_v2.<入口函数>(...)`
- Code flow 模块入口：`xbot_extensions.activity_excel_v2.refresh_pivot_table.main(args)`
- 常用入口：`fill_down_formula()`、`fill_right_formula()`、`filter()`、`text_format_to_num()`、`num_format_to_text()`、`process16()` 等
- 区域截图入口：`process24(excel_instance, begin_row, begin_column, end_row, end_column, save_path, sheet_name)`

**参数说明：**
- `excel_instance` / `Excel对象`：待处理 Excel 对象。
- `sheet_name` / `Sheet页名称`：Sheet 名称；多数指令可选，通常默认当前激活 Sheet。
- 行列参数按指令定义传入，如 `row`、`begin_row`、`end_row`、`column`、`column_name`、`begin_column`、`end_column`。
- 具体入口函数、参数顺序和返回值以 `prototype.block.json` 与 `__init__.py` 为准，不根据可视化中文界面猜测编码版参数。

**典型调用方式：**
```python
from xbot_extensions.activity_excel_v2 import (
    fill_down_formula,
    filter,
    process21,
    process24,
    process56,
)

# 向下填充公式
fill_down_formula(
    excel_instance=workbook,
    formula_content="=A2+B2",
    column="C",
    begin_row="2",
    end_row="-1",
    sheet_name="",
    数组公式=False,
)

# 按内容筛选后读取筛选结果
filter(
    excel_instance=workbook,
    row="1",
    column="A",
    select_content="已完成",
    select_type="={0}",
    sheet_name="",
    operator="7",
    select_content2="",
    select_type2="",
)

filter_content = process21(
    excel_instance=workbook,
    begin_row="2",
    sheet_name="",
    content_type="data",
    using_text=True,
    using_text_cols="",
    data_columns="",
)

# 冻结首行
process56(
    excel_instance=workbook,
    sheet_name="",
    kind="ROW",
    area="1",
)

# 把指定区域保存为图片
result = process24(
    excel_instance=workbook,
    begin_row=1,
    begin_column="E",
    end_row=last_row,
    end_column=last_column,
    save_path=image_path,
    sheet_name="每日报表",
)
if isinstance(result, dict):
    image_path = result.get("image_save_path", image_path)
```

### 区域截图 `process24()`

```python
result = process24(excel_instance, begin_row, begin_column, end_row, end_column, save_path, sheet_name)
```

| 参数 | 类型 | 说明 |
|---|---|---|
| `excel_instance` | 工作簿对象 | 已打开的 Excel / WPS 工作簿 |
| `begin_row` | `int` | 起始行 |
| `begin_column` | `str` | 起始列，如 `"E"` |
| `end_row` | `int` | 结束行 |
| `end_column` | `str` | 结束列，如 `"T"` |
| `save_path` | `str` | 图片保存路径 |
| `sheet_name` | `str` | 要截图的 Sheet 名称 |

输出名为 `image_save_path`。当前真实项目中包装入口可能直接返回路径，也可能返回包含 `image_save_path` 的字典，因此调用方可按上例兼容读取。该能力没有发现等价的原生 `xbot.excel` 区域截图接口，适合保留为市场指令用法。

完整示例见 [`excel-range-screenshot.py`](../../examples/excel-range-screenshot.py)。

**注意事项：**
- 这是市场扩展能力，不是原生 `xbot.excel` 内置 API；能用原生 `xbot.excel` 清晰完成的任务仍优先查 `docs/excel.md`。
- 普通读写、清空、复制优先使用原生 `xbot.excel`；只有区域截图等原生 API 缺失的能力才使用本扩展。
- 该扩展大多数编码版入口是 `__init__.py` 中的包装函数，调用后进入 Visual flow；`refresh_pivot_table` 是 Code flow 模块入口；不要把内部工具模块或测试模块当作公开调用入口。
- `process45`、`process46`、`process47` 等入口在源码中使用中文参数名，编码版调用前建议按当前安装版本再次用 `inspect.signature()` 核对。
- 本节仅根据源码结构和 block 元数据整理，未在影刀编辑器内运行验证。

---
