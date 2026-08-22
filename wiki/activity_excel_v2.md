# activity_excel_v2 Excel扩展操作

## 定位

`activity_excel_v2` 是影刀 Excel 原生指令的扩展市场指令，不替代原生 Excel 指令。

适用于原生 Excel 指令缺少的高级表格处理能力，例如：

- 批量公式填充
- 高级筛选处理
- 图片与单元格操作
- 工作表管理
- 数据辅助处理

普通 Excel 读写优先使用原生 Excel 指令；只有原生能力不足时使用本扩展。

## 能力分类

以下为正式公开指令能力，不包含 `test_*` 等内部测试 flow。

### 单元格填充

- 公式向下填充
- 公式向右填充
- 自动向下填充
- 空白单元格填充

### 单元格操作

- 文本转数字
- 数字转文本
- 分列
- 内容替换
- 自动换行
- 超链接读取/设置
- 注释读取
- 公式转换成值
- 新建注释
- 获取背景色
- 获取合并单元格区域
- 合并单元格 / 取消单元格合并

### 筛选增强

- 条件筛选
- 颜色筛选
- 读取筛选内容
- 删除筛选内容
- 清除筛选

### 图片处理

- 单元格填充图片
- 导出单元格图片
- 删除单元格图片
- 删除所有图片

### 工作表与其它能力

- 隐藏/取消隐藏工作表
- 获取隐藏工作表名
- 合并计算
- 设置密码
- 查找数据所在行/列
- 合成字典
- 刷新透视表
- 数字列名转换
- 设置切片器
- 执行文本宏
- 冻结首行

## API 入口说明

公开调用入口以函数名为准，例如：

```python
from xbot_extensions import activity_excel_v2

activity_excel_v2.fill_down_formula(...)
activity_excel_v2.filter(...)
activity_excel_v2.refresh_pivot_table(...)
```

部分历史指令使用 `processXX` 形式命名，例如区域截图、冻结首行等能力。
不要根据 `processXX` 名称猜测功能，应以市场指令名称和源码元数据为准。

## 常用参数

| 参数 | 说明 |
| --- | --- |
| excel_instance | Excel对象 |
| sheet_name | Sheet名称 |
| row / begin_row / end_row | 行范围 |
| column / begin_column / end_column | 列范围 |

具体参数以当前安装版本 `prototype.block.json` 为准。

## 调用注意

- 市场指令入口以当前安装版本为准。
- 编码版调用前建议使用 `inspect.signature()` 确认参数。
- 不根据可视化界面文字猜测编码参数。
- 本指令内部大量能力通过 Visual flow 包装实现。

## API Reference（参数级）

以下为公开指令参数索引。参数来源于 `prototype.block.json`，隐藏测试模块不纳入。

| 指令 | function | 参数 | 类型 | 默认值 | 输出 |
| --- | --- | --- | --- | --- | --- |
| 批量向下填充(公式) | `fill_down_formula` | excel_instance, formula_content, column, begin_row, end_row, sheet_name, 数组公式 | Workbook, str | None/空/False | 无 |
| 批量向右填充(公式) | `fill_right_formula` | excel_instance, formula_content, row, begin_column, end_column, sheet_name, array_formula_mode | Workbook, str | None/空/False | 无 |
| 筛选 | `filter` | excel_instance, select_type, row, column, select_content, sheet_name, operator, select_type2, select_content2 | Workbook, str | None | 无 |
| 区域文本转数字 | `text_format_to_num` | excel_instance, begin_row, begin_column, end_row, end_column, sheet_name | Workbook, str | None | 无 |
| 区域数字转文本 | `num_format_to_text` | excel_instance, begin_row, begin_column, end_row, end_column, sheet_name | Workbook, str | None | 无 |
| 区域截图 | `process24` | excel_instance, begin_row, begin_column, end_row, end_column, save_path, sheet_name | Workbook, int, str | None | 图片路径/字典 |
| 读取筛选内容 | `process21` | excel_instance, begin_row, sheet_name, content_type, using_text, using_text_cols, data_columns | Workbook, str, bool | None | 列表/数据 |
| 获取合并单元格区域 | `process55` | excel_instance, row, column, sheet_name | Workbook, str | None | 是否合并、区域 |
| 冻结首行 | `process56` | excel_instance, kind, area, sheet_name | Workbook, str | None | 无 |
| 设置切片器 | `process57` | excel_instance, slicercache_name, item_name, selected | Workbook, str, bool | True | 无 |
| 刷新透视表 | `refresh_pivot_table` | excel_instance, sheet_name | Workbook, str | None | 无 |
| 执行文本宏 | `process58` | excel_instance, macro_name, macro_string | Workbook, str | None | 无 |

其它公开指令遵循相同规则，参数以 `prototype.block.json` 中 inputs 定义为准。

## 参数级 API 说明

### 通用参数

| 参数 | 类型 | 默认值 | 说明 | 输出 |
| --- | --- | --- | --- | --- |
| excel_instance | openpyxl.Workbook | None | 待处理 Excel 对象 | 无 |
| sheet_name | str | 当前激活 Sheet | 指定处理 Sheet | 无 |
| row / begin_row / end_row | str/int | 按指令定义 | 行范围参数 | 无 |
| column / begin_column / end_column | str | 按指令定义 | 列范围参数 | 无 |

### 主要 API 示例

| API | 参数 | 输出 |
| --- | --- | --- |
| fill_down_formula | excel_instance, formula_content, column, begin_row, end_row, sheet_name | 无 |
| fill_right_formula | excel_instance, formula_content, row, begin_column, end_column, sheet_name | 无 |
| filter | excel_instance, row, column, select_content, select_type, sheet_name | 无 |
| process24（区域截图） | excel_instance, begin_row, begin_column, end_row, end_column, save_path, sheet_name | 图片路径/结果对象 |
| process21（读取筛选内容） | excel_instance, 查询参数 | 筛选结果 |

说明：完整参数以当前版本 `prototype.block.json` 为准，不同影刀版本可能存在差异。

## 完整公开指令参数补充

以下补充低频公开能力。参数来源于 `prototype.block.json`，仅记录公开市场指令。

| 指令 | function | 参数 | 类型 | 默认值 | 输出 |
| --- | --- | --- | --- | --- | --- |
| 单元格填充图片 | add_picture | excel_instance, image_path, row, column, sheet_name | Workbook / str | None | 无 |
| 导出单元格图片 | export_cell_picture | excel_instance, row, column, save_path, sheet_name | Workbook / str | None | 图片路径 |
| 删除单元格图片 | delete_cell_picture | excel_instance, row, column, sheet_name | Workbook / str | None | 无 |
| 删除所有图片 | delete_all_picture | excel_instance, sheet_name | Workbook / str | None | 无 |
| 隐藏/取消隐藏 Sheet | process48 | excel_instance, sheet_name, hidden | Workbook / bool | False | 无 |
| 获取隐藏 Sheet | process47 | excel_instance | Workbook | None | Sheet列表 |
| 公式转换成值 | process45 | excel_instance, begin_row, begin_column, end_row, end_column, sheet_name | Workbook / str | None | 无 |
| 新建注释 | process46 | excel_instance, row, column, content, sheet_name | Workbook / str | None | 无 |
| 自动换行 | process50 | excel_instance, begin_row, begin_column, end_row, end_column, sheet_name | Workbook / str | None | 无 |
| 合并计算 | process51 | excel_instance, source_range, target_range, sheet_name | Workbook / str | None | 无 |
| 设置/取消密码 | process49 | excel_instance, password, sheet_name | Workbook / str | None | 无 |
| 查找数据所在行 | process18 | excel_instance, content, column, sheet_name | Workbook / str | None | 行号 |
| 查找数据所在列 | process17 | excel_instance, content, row, sheet_name | Workbook / str | None | 列号 |
| 生成字典(数值累加) | process19 | key_column, value_column | str | None | dict |
| 生成字典(列表拼接) | process20 | key_column, value_column | str | None | dict |
| 数字列名转换 | process16 | column | str | None | 列名 |

注：部分 processXX 为历史内部命名，实际调用时应优先使用市场指令名称或当前版本导出的函数入口。

