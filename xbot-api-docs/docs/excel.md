# 影刀表格操作方法整理

> 定位：影刀 / xbot 操作 Excel 的开发者参数手册。  
> 重点：用户写代码时看不到源码，所以本文尽量把**参数名、默认值、可选值、大小写、传参示例**写清楚。  
> 规则：字符串参数必须按文档中的值原样传入，例如 `kind="wps"`，不是 `WPS`，也不是 `PWS`。

---

## 1. 相关文件位置

| 路径 | 作用 |
|---|---|
| `C:\Program Files\ShadowBot\shadowbot-6.0.30\Resources\Code-Activity\Zh-CN\xbot\excel\__init__.py` | Excel 原生入口：创建、打开、获取当前工作簿、关闭 Excel 进程 |
| `C:\Program Files\ShadowBot\shadowbot-6.0.30\Resources\Code-Activity\Zh-CN\xbot\excel\workbook\baseworkbook.py` | 工作簿接口：保存、关闭、Sheet 操作、宏、透视表、导出 PDF 等 |
| `C:\Program Files\ShadowBot\shadowbot-6.0.30\Resources\Code-Activity\Zh-CN\xbot\excel\worksheet\baseworksheet.py` | 工作表接口：读写单元格、行、列、区域，插入/删除/清空等 |
| `C:\Program Files\ShadowBot\shadowbot-6.0.30\Resources\Code-Activity\Zh-CN\xbot\excel\workrange\baseworkrange.py` | 区域对象接口：格式、字体、边框、背景、行高、列宽、数据验证等 |
| `C:\Program Files\ShadowBot\shadowbot-6.0.30\Resources\Code-Activity\Zh-CN\xbot_visual\excel.py` | 影刀可视化动作封装：`launch`、读写、循环、复制粘贴、格式、排序等 |
| [`package.md`](package.md) | 影刀基础对象与全局变量说明 |

---

## 2. 参数传值总规则

### 2.1 字符串可选值区分大小写

正确：

```python
kind="wps"
kind="office"
kind="openpyxl"
```

错误：

```python
kind="WPS"      # 错
kind="PWS"      # 错
kind="Office"   # 错
kind="OPENPYXL" # 错
```

### 2.2 布尔值必须传 Python 布尔值

正确：

```python
visible=True
ignore_formula=False
update_links=False
```

不建议：

```python
visible="True"   # 字符串，不建议
visible="False"  # 字符串，不建议
```

### 2.3 路径建议使用原始字符串

```python
file_name = r"C:\path\demo.xlsx"
```

或者使用双反斜杠：

```python
file_name = "C:\\path\\demo.xlsx"
```

---

## 3. Excel 驱动类型 `kind`

`kind` 是最容易传错的参数，必须使用下面这些**小写字符串**：

| 传参值 | 正确写法 | 说明 | 常见错误 |
|---|---|---|---|
| Office | `kind="office"` | 使用 Microsoft Excel / Office | `"Office"`、`"OFFICE"` |
| WPS | `kind="wps"` | 使用 WPS 表格 | `"WPS"`、`"pws"`、`"PWS"` |
| OpenPyXL | `kind="openpyxl"` | 后台读写 `.xlsx`，不打开界面 | `"openPyXL"`、`"OpenPyxl"` |
| 自动检查 | `kind="auto_check"` | 优先 Office，失败再尝试 WPS | `"auto"`、`"autoCheck"` |
| WPS 插件 | `kind="wps_addon"` | WPS 插件方式 | `"wpsAddon"`、`"wps-addon"` |

推荐选择：

| 场景 | 推荐 |
|---|---|
| 只读写 `.xlsx`，不需要界面 | `kind="openpyxl"` |
| 需要宏、公式刷新、复制粘贴、真实 Excel 行为 | `kind="office"` |
| 公司电脑主要装 WPS | `kind="wps"` |
| 不确定装了 Office 还是 WPS | `kind="auto_check"` |

---

## 4. 创建 Excel：`xbot.excel.create()`

### 4.1 方法签名

```python
workbook = xbot.excel.create(
    kind="office",
    visible=True,
    original_file="",
)
```

### 4.2 参数说明

| 参数 | 类型 | 必填 | 默认值 | 可选值 | 说明 |
|---|---|---:|---|---|---|
| `kind` | `str` | 否 | `"office"` | `"office"` / `"wps"` / `"openpyxl"` / `"auto_check"` / `"wps_addon"` | 创建方式，必须小写 |
| `visible` | `bool` | 否 | `True` | `True` / `False` | 是否显示 Excel/WPS 窗口；主要对 `office`、`wps` 有效 |
| `original_file` | `str` | 否 | `""` | 文件路径字符串 | 原始文件路径；通常可不传 |

### 4.3 示例

```python
import xbot.excel

# 用 Office 新建
workbook = xbot.excel.create(kind="office", visible=True)

# 用 WPS 新建
workbook = xbot.excel.create(kind="wps", visible=True)

# 用 openpyxl 后台新建
workbook = xbot.excel.create(kind="openpyxl")
```

---

## 5. 打开 Excel：`xbot.excel.open()`

### 5.1 方法签名

```python
workbook = xbot.excel.open(
    file_name=r"C:\path\demo.xlsx",
    kind="office",
    visible=True,
    password="",
    write_password="",
    ignore_formula=False,
    update_links=False,
)
```

### 5.2 参数说明

| 参数 | 类型 | 必填 | 默认值 | 可选值 | 说明 |
|---|---|---:|---|---|---|
| `file_name` | `str` | 是 | 无 | Excel 文件路径 | 要打开的文件路径 |
| `kind` | `str` | 否 | `"office"` | `"office"` / `"wps"` / `"openpyxl"` / `"auto_check"` / `"wps_addon"` | 打开方式，必须小写 |
| `visible` | `bool` | 否 | `True` | `True` / `False` | 是否显示窗口；主要对 `office`、`wps` 有效 |
| `password` | `str` | 否 | `""` | 密码字符串 | 打开密码；主要对 `office`、`wps` 有效 |
| `write_password` | `str` | 否 | `""` | 密码字符串 | 编辑密码；主要对 `office`、`wps` 有效 |
| `ignore_formula` | `bool` | 否 | `False` | `True` / `False` | `openpyxl` 下会传给 `data_only`；`True` 倾向读取公式结果，`False` 倾向保留公式 |
| `update_links` | `bool` | 否 | `False` | `True` / `False` | 是否更新外部链接；主要对 `office`、`wps` 有效 |

### 5.3 正确示例

```python
import xbot.excel

# Office 打开
workbook = xbot.excel.open(
    file_name=r"C:\path\demo.xlsx",
    kind="office",
    visible=False,
)

# WPS 打开：注意是小写 wps
workbook = xbot.excel.open(
    file_name=r"C:\path\demo.xlsx",
    kind="wps",
    visible=True,
)

# openpyxl 后台打开
workbook = xbot.excel.open(
    file_name=r"C:\path\demo.xlsx",
    kind="openpyxl",
    ignore_formula=True,
)
```

### 5.4 常见错误

```python
kind="WPS"       # 错，应该是 kind="wps"
kind="PWS"       # 错，拼写错误
kind="xlsx"      # 错，kind 不是文件类型
visible="False"  # 不建议，应该用 visible=False
```

---

## 6. 获取当前工作簿：`xbot.excel.get_active_workbook()`

```python
workbook = xbot.excel.get_active_workbook()
```

| 参数 | 说明 |
|---|---|
| 无 | 获取当前激活的 Excel / WPS 工作簿 |

注意：当前无法从参数里指定 `kind`，源码会按运行环境尝试获取当前激活工作簿。

---

## 7. 关闭 Excel 进程：`xbot.excel.kill_excel_process()`

```python
xbot.excel.kill_excel_process("office", False)
xbot.excel.kill_excel_process("wps", True)
```

| 参数 | 类型 | 必填 | 可选值 | 说明 |
|---|---|---:|---|---|
| `close_process` | `str` | 是 | `"office"` / `"wps"` | 关闭 Office Excel 或 WPS 表格进程，必须小写 |
| `kill_task` | `bool` | 是 | `True` / `False` | 是否强制结束进程 |

---

## 8. 工作簿常用方法

### 8.1 保存 / 另存 / 关闭

```python
workbook.save()
workbook.save_as(r"C:\path\new.xlsx")
workbook.close()
```

| 方法 | 参数 | 说明 |
|---|---|---|
| `save()` | 无 | 保存当前文件 |
| `save_as(filename)` | `filename: str` | 另存为指定路径 |
| `close()` | 无 | 关闭工作簿 |
| `is_closed()` | 无 | 判断工作簿对象是否已关闭 |
| `set_saved(True)` | `True` / `False` | 标记保存状态；常用于不保存关闭 |

---

## 9. Sheet 操作

### 9.1 获取 Sheet

```python
sheet = workbook.get_active_sheet()
sheet = workbook.get_sheet_by_name("Sheet1")
sheet = workbook.get_sheet_by_index(1)
sheets = workbook.get_all_sheets()
```

| 方法 | 参数 | 参数说明 | 返回 |
|---|---|---|---|
| `get_active_sheet()` | 无 | 当前激活 Sheet | `WorkSheet` |
| `get_sheet_by_name(name)` | `name: str` | Sheet 名称 | `WorkSheet` |
| `get_sheet_by_index(index)` | `index: int` | Sheet 位置，通常从 `1` 开始 | `WorkSheet` |
| `get_all_sheets()` | 无 | 获取全部 Sheet | Sheet 列表 |

### 9.2 激活 / 创建 / 删除 / 重命名

```python
workbook.active_sheet_by_name("Sheet1")
workbook.active_sheet_by_index(1)
workbook.create_sheet("新Sheet", "last")
workbook.rename_sheet("旧名称", "新名称")
workbook.delete_sheet("Sheet1")
```

| 方法 | 参数 | 可选值 / 说明 |
|---|---|---|
| `active_sheet_by_name(name)` | `name: str` | Sheet 名称 |
| `active_sheet_by_index(index)` | `index: int` | Sheet 位置 |
| `create_sheet(name, create_way)` | `create_way: str` | `"first"` / `"last"`，必须小写 |
| `rename_sheet(name, new_name)` | `name/new_name: str` | 旧名称 / 新名称 |
| `delete_sheet(name)` | `name: str` | 要删除的 Sheet 名称 |
| `copy_sheet(name, new_name, is_cover)` | `is_cover: bool` | 是否覆盖同名 Sheet |
| `copy_sheet_to_workbook(name, workbook, new_name, is_cover)` | `workbook` | 复制到另一个工作簿 |

---

## 10. 读取数据

### 10.1 原生 Sheet 方法

```python
value = sheet.get_cell(1, "A")
row_data = sheet.get_row(1)
col_data = sheet.get_column("A")
data = sheet.get_range(1, "A", 10, "D")
data = sheet.get_used_range()
```

| 方法 | 参数 | 参数说明 | 返回 |
|---|---|---|---|
| `get_cell(row, column)` | `row: int`, `column: str` | 行号从 `1` 开始；列名如 `"A"` | 单元格值 |
| `get_row(row)` | `row: int` | 行号从 `1` 开始 | 一维列表 |
| `get_column(column)` | `column: str` | 列名如 `"A"` | 一维列表 |
| `get_range(start_row, start_col, end_row, end_col)` | `int/str` | 起止行列 | 二维列表 |
| `get_used_range()` | 无 | 已使用区域 | 二维列表 |

### 10.2 可视化封装读数据：`read_data_from_workbook`

常见 `read_way` 可选值：

| `read_way` | 说明 | 需要的关键参数 |
|---|---|---|
| `"cell"` | 读取单元格 | `cell_row_num`、`cell_column_name` |
| `"range"` | 读取区域 | `area_begin_row_num`、`area_begin_column_name`、`area_end_row_num`、`area_end_column_name` |
| `"row"` | 读取整行 | `row_row_num` |
| `"column"` | 读取整列 | `column_column_name` |
| `"used_range"` | 读取已使用区域 | 无关键行列参数 |

其它参数：

| 参数 | 类型 | 默认值 | 可选值 | 说明 |
|---|---|---|---|---|
| `has_header_row` | `bool` | 视调用传入 | `True` / `False` | 读取区域时是否跳过首行表头 |
| `using_text` | `bool` | `False` | `True` / `False` | 是否读取显示文本；`openpyxl` 不支持 |
| `text_cols` | `str` | `""` | 如 `"C,F"` | 指定按文本读取的列 |
| `clear_space` | `bool` | `False` | `True` / `False` | 是否清理前后空白 |

---

## 11. 写入数据

### 11.1 原生 Sheet 方法

```python
sheet.set_cell(1, "A", "hello")
sheet.set_row(1, ["姓名", "年龄"], begin_column_name="A")
sheet.append_row(["张三", 18], begin_column_name="A")
sheet.insert_row(2, ["李四", 20], begin_column_name="A")
sheet.set_column("A", ["姓名", "张三"], begin_row_num=1)
sheet.set_range(1, "A", [["姓名", "年龄"], ["张三", 18]])
```

| 方法 | 参数 | 参数说明 |
|---|---|---|
| `set_cell(row, column, value)` | `row: int`, `column: str`, `value` | 写入单元格 |
| `set_row(row, values, begin_column_name="A")` | `values: list` | 覆盖一行 |
| `append_row(values, begin_column_name="A")` | `values: list` | 追加一行 |
| `insert_row(row, values, begin_column_name="A")` | `row: int` | 插入一行 |
| `set_column(column, values, begin_row_num=1)` | `values: list` | 覆盖一列 |
| `set_range(row, column, values)` | `values: list[list]` | 从指定位置写入二维数组 |

### 11.2 可视化封装写数据：`write_data_to_workbook`

`write_range` 可选值：

| `write_range` | 说明 | 常用关键参数 |
|---|---|---|
| `"cell"` | 写单元格 | `row_num`、`column_name`、`content` |
| `"row"` | 写一行 | `write_way`、`row_num`、`begin_column_name`、`content` |
| `"column"` | 写一列 | `write_column_way`、`column_name`、`begin_row_num`、`content` |
| `"area"` | 写区域 | `row_num`、`column_name`、`content` |

`write_way` 可选值：

| 值 | 说明 |
|---|---|
| `"append"` | 追加 |
| `"insert"` | 插入 |
| `"override"` | 覆盖 |

`write_column_way` 可选值：

| 值 | 说明 |
|---|---|
| `"append"` | 追加列 |
| `"insert"` | 插入列 |
| `"override"` | 覆盖列 |

其它参数：

| 参数 | 类型 | 示例 | 说明 |
|---|---|---|---|
| `write_as_text_cols` | `str` | `"C,F"` | 指定哪些列按文本写入，避免数字字符串被转成数字 |
| `content` | 任意 / `list` / `list[list]` | `"hello"`、`[1,2]`、`[[1,2]]` | 写入内容 |

---

## 12. 行列和区域操作

```python
row_count = sheet.get_row_count()
column_count = sheet.get_column_count()
first_free_row = sheet.get_first_free_row()
first_free_column = sheet.get_first_free_column()
row_num = sheet.get_first_free_row_on_column("A")
```

```python
sheet.remove_row(2)
sheet.remove_column("C")
sheet.insert_blank_row(2, amount=1)
sheet.insert_blank_column("B", amount=1)
sheet.clear()
```

常见参数：

| 参数 | 类型 | 可选值 / 示例 | 说明 |
|---|---|---|---|
| `row_num` | `int` / `str` | `1`、`"1:3"`、`"1,3,5"` | 行号或行范围；部分封装支持范围字符串 |
| `column_name` | `str` / `int` | `"A"`、`"A:C"`、`"A,C"`、`1` | 列名或列范围；部分封装支持数字列 |
| `amount` | `int` | `1`、`2` | 插入空行/空列数量，必须大于 0 |

---

## 13. 清空、复制、粘贴、选择

### 13.1 清空区域

可视化封装 `clear_range` 的常见参数：

| 参数 | 类型 | 可选值 | 说明 |
|---|---|---|---|
| `clear_way` | `str` | `"cell"` / `"range"` / `"row"` / `"column"` / `"used_range"` | 清空目标类型 |
| `clear_target` | `str` | 常见为 `"all"` | 清空目标，源码直接传给底层 |
| `cell_row_num` | `int` | `1` | 单元格行号 |
| `cell_column_name` | `str` | `"A"` | 单元格列名 |
| `area_begin_row_num` | `int` | `1` | 区域开始行 |
| `area_begin_column_name` | `str` | `"A"` | 区域开始列 |
| `area_end_row_num` | `int` | `10` | 区域结束行 |
| `area_end_column_name` | `str` | `"D"` | 区域结束列 |

### 13.2 复制区域

`copy_way` 可选值：

| 值 | 说明 |
|---|---|
| `"cell"` | 复制单元格 |
| `"range"` | 复制区域 |
| `"row"` | 复制行 |
| `"column"` | 复制列 |
| `"used_range"` | 复制已使用区域 |

### 13.3 粘贴区域

```python
sheet.paste_range_ex(
    row_num=1,
    column_name="A",
    paste_type=-4104,
    paste_special_operation=-4142,
    skip_blanks=False,
    transpose=False,
)
```

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `row_num` | `int` | 无 | 粘贴起始行 |
| `column_name` | `str` | 无 | 粘贴起始列 |
| `paste_type` | `int` | `-4104` | Excel 粘贴类型常量 |
| `paste_special_operation` | `int` | `-4142` | Excel 特殊粘贴操作常量 |
| `skip_blanks` | `bool` | `False` | 是否跳过空白 |
| `transpose` | `bool` | `False` | 是否转置 |

---

## 14. 格式设置

### 14.1 获取区域对象

```python
cell_range = sheet.cell("A", 1)
row_range = sheet.row(1)
column_range = sheet.column("A")
area_range = sheet.range("A1:D10")
used_range = sheet.used_range()
```

### 14.2 区域格式方法

| 方法 | 参数 | 可选值 / 示例 | 说明 |
|---|---|---|---|
| `set_format(setting)` | `dict` | 格式字典 | 设置完整格式 |
| `set_number_format(number_format)` | `str` | `"0.00"`、`"yyyy-mm-dd"` | 设置数字格式 |
| `set_alignment(setting)` | `dict` | 对齐设置 | 设置对齐 |
| `set_border(setting)` | `dict` | 边框设置 | 设置边框 |
| `set_font(setting)` | `dict` | 字体设置 | 设置字体 |
| `set_background(setting)` | `dict` | 背景设置 | 设置背景色 |
| `set_protection(locked=True, formula_hidden=None)` | `bool` | `True` / `False` | 设置保护 |
| `clear_format()` | 无 | 无 | 清空格式 |
| `set_column_width(mode, value=None)` | `mode: str` | `"autoFit"` 或指定宽度 | 设置列宽 |
| `set_row_height(mode, value=None)` | `mode: str` | `"autoFit"` 或指定高度 | 设置行高 |
| `add_validation(setting)` | `dict` | 数据验证设置 | 添加数据验证 |

注意：`autoFit` 大小写按源码注释写法，建议原样传 `"autoFit"`。

---

## 15. 高级功能

```python
workbook.execute_macro("宏名称")
workbook.refresh_data()
workbook.export_to_pdf(r"C:\path\demo.pdf", sheet_name="Sheet1", all_sheets=False, override=True)
```

| 方法 | 关键参数 | 可选值 / 说明 |
|---|---|---|
| `execute_macro(macro)` | `macro: str` | 宏名称 |
| `refresh_data()` | 无 | 刷新数据 |
| `create_pivot_table(setting, source, sheet_name=None, pivot_name=None)` | `dict/str` | 创建数据透视表 |
| `refresh_pivot_table(name_or_index, sheet_name, refresh_all)` | `refresh_all: bool` | 刷新透视表 |
| `filter_pivot_table(sheet_name, name_or_index, field_name, select_type, filter_value_list)` | `select_type` | 常见 `"partial"` |
| `export_to_pdf(pdf_name, sheet_name=None, all_sheets=False, override=True)` | `all_sheets/override: bool` | 导出 PDF |

---

## 16. 推荐模板

### 16.1 只读数据

```python
import xbot.excel

workbook = xbot.excel.open(
    file_name=r"C:\path\demo.xlsx",
    kind="openpyxl",
    ignore_formula=True,
)

sheet = workbook.get_active_sheet()
data = sheet.get_used_range()
workbook.close()
```

### 16.2 写入数据并保存

```python
import xbot.excel

workbook = xbot.excel.open(
    file_name=r"C:\path\demo.xlsx",
    kind="office",
    visible=False,
)

sheet = workbook.get_sheet_by_name("Sheet1")
sheet.set_range(1, "A", [["姓名", "年龄"], ["张三", 18]])

workbook.save()
workbook.close()
```

### 16.3 WPS 打开文件

```python
import xbot.excel

workbook = xbot.excel.open(
    file_name=r"C:\path\demo.xlsx",
    kind="wps",  # 必须是小写 wps
    visible=True,
)
```

---

## 17. 经验

- `kind` 等字符串参数大小写敏感，按文档传 `kind="wps"`、`kind="office"`、`kind="openpyxl"`，不要写 `"WPS"`、`"PWS"`、`"Office"` 或界面中文展示值。
- 影刀项目默认优先使用 `xbot.excel` 处理 Excel / WPS 文件；涉及公式刷新、界面交互、宏、另存、格式、文件占用、真实 Office / WPS 行为时，不要为了图快改用其它后台读写库。
- 表格大量写入时，优先整理成二维数组后用 `set_range()` 批量写入，减少逐单元格操作；写入前先明确表头、起始单元格和目标区域。
- 需要写入真实 Excel / WPS 工作簿时，建议先用 `workbook.workbook.ReadOnly` 判断是否只读；第一次只读可能是本机残留进程占用，可关闭后 kill 本机 WPS / Excel 进程再二次打开判断，第二次仍只读再判定可能被他人占用。
- `kind="wps"` 对应 `xbot.excel.kill_excel_process("wps", True)`；`kind="office"` 对应 `xbot.excel.kill_excel_process("office", True)`。
- 字段名来自当前业务表时，不要抽成跨项目通用常量；当前项目已约定字段结构时，业务逻辑直接按约定取值，不要反复写 `isinstance` 和空结构兜底。
- 用户需要看到 WPS / Excel 写入过程时，可用 `xbot.win32.get(title="*文件名*", use_wildcard=True)` 激活窗口，再用表格对象能力选中新增行；不要优先坐标点击或猜窗口句柄。
- 本地脚本或 pytest 通过，只能说明后台数据处理逻辑可用；涉及 WPS / Office 界面、公式刷新、宏、弹窗、文件占用时，最终仍需在影刀编辑器或真实运行环境验证。
- 按日期批量扫描表格时，如果业务要求日期连续，遇到缺失文件优先从模板资源复制补齐；模板路径应通过 `package.resources.get_path()` 或 `copy_to()` 获取，不要写 `package.resources["xxx"]`。
- 平台导出 ZIP 后如果包含多个 `.xlsx`，不要随手取第一个文件；优先按业务文件名关键词、表头结构、sheet 名识别目标报表，无法判断时应抛出明确异常或进入失败结果。

---

## 18. 排错速查

| 现象 | 常见原因 | 处理 |
|---|---|---|
| `kind="WPS"` 打不开 | 参数值大小写错误 | 改成 `kind="wps"` |
| `kind="PWS"` 报错 | 拼写错误 | 改成 `kind="wps"` |
| `openpyxl` 读取不到显示文本 | `openpyxl` 不支持 `using_text=True` | 改用 `office` / `wps` |
| 写入数字字符串变成数字 | Excel 自动识别类型 | 用 `write_as_text_cols="C,F"` 或写入前加文本标记 |
| 大量写入很慢 | 循环逐单元格写入 | 改用 `set_range()` 一次性写二维数组 |
| 宏无法执行 | `openpyxl` 不支持宏执行 | 改用 `office` 或 `wps` |
