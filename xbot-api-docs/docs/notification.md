# 影刀桌面对话框与通知方法

> 定位：影刀 / xbot 桌面端对话框、通知、选择器交互接口。
> 说明：本页基于 `xbot.app.dialog` 源码整理，优先按源码参数和返回值描述；旧文档若有冲突，以源码为准。

---

## 1. 相关文件位置

| 路径 | 作用 |
|---|---|
| `C:\Program Files\ShadowBot\shadowbot-6.0.30\Resources\Code-Activity\Zh-CN\xbot\app\dialog.py` | 对话框、通知入口 |

---

## 2. `show_alert(message, title=...)`

### 作用

打开消息提示框。

### 返回值

无。

### 注意事项

- `title` 默认值来自 `strings.Dialog_Alter_Title`，源码未直接展开字符串内容。

---

## 3. `show_confirm(message, title=...) -> bool`

### 作用

打开确认对话框，返回用户是否确认。

### 返回值

- `True`：确认
- `False`：取消

---

## 4. `show_custom_dialog(settings, *, storage_key=None) -> dict`

### 作用

打开自定义对话框。

### 常用场景

- 组合输入框、按钮、选择框
- 复杂参数收集
- 需要记住用户输入时

### 参数

| 参数名 | 类型 | 是否必填 | 说明 |
|---|---|---|---|
| `settings` | `dict` / `json串` | 是 | 对话框配置 |
| `storage_key` | `str` / `None` | 否 | 记忆输入内容的存储键 |

### 返回值

- 成功时返回对话框数据字典
- 失败时抛异常

### 注意事项

- `storage_key` 不为空时，源码会尝试读取/保存历史输入。
- 对话框配置结构较复杂，建议按源码注释逐项填写。
- **下拉/列表类控件（`Select`、`MultiSelect`、`List`、`MultiList`）的 `options` 不能用纯字符串数组**。`dialog.py` 源码注释里 `options: ["选项1", "选项2"]` 的示例已过时；所有影刀版本都应按对象数组写：`{"value": ..., "display": ...}`。控件级默认值 `value` 必须等于某个选项的 `value`。
  - 来源：`dnfile` 解析 `shadowbot-6.2.18/ShadowBot.Shell.ShadowBotToolkit.dll`，确认 `OptionItem` 只声明 `Value`、`Display` 两个属性；JSON 键按其它字段（`nullText`、`isTextEditable`）的驼峰小写规律写为 `value` / `display`。

### 示例

下拉框 `options` 的正确写法（对象数组，非字符串数组）：

```python
from xbot.app.dialog import show_custom_dialog

dialog_settings = {
    "dialogTitle": "采集参数",
    "settings": {
        "editors": [
            {"type": "TextBox", "label": "链接", "VariableName": "url",
             "value": None, "nullText": "请输入链接"},
            {"type": "Select", "label": "浏览器类型", "VariableName": "browser_type",
             "value": "chrome",  # 必须等于某个选项的 value
             "options": [{"value": "chrome", "display": "chrome"},
                         {"value": "edge", "display": "edge"}]},
        ],
        "buttons": [
            {"type": "Button", "label": "确定", "theme": "red", "hotkey": "Enter"},
            {"type": "Button", "label": "取消", "theme": "white", "hotkey": "Esc"},
        ],
    },
}
result = show_custom_dialog(dialog_settings)
# result["browser_type"] 取到选项的 value（如 "chrome"）
```

---

## 5. `show_message_box(title, message, button='ok', *, timeout=-1, default_button=None) -> str`

### 作用

打开消息对话框，支持单按钮或多按钮选择。

### 参数

| 参数名 | 类型 | 是否必填 | 说明 |
|---|---|---|---|
| `title` | `str` | 是 | 标题 |
| `message` | `str` | 是 | 消息内容 |
| `button` | `str` | 否 | 按钮组合，如 `ok`、`okcancel`、`yesno`、`yesnocancel` |
| `timeout` | `int` | 否 | 超时时间，`-1` 一直等，`0` 不等 |
| `default_button` | `str` / `None` | 否 | 默认按钮；不传时按源码规则自动推断 |

### 返回值

返回用户点击的按钮名。

### 注意事项

- 按钮名应传小写，源码按小写判断。
- `default_button` 不传时，源码会根据 `button` 自动选择。

---

## 6. `show_workbook_dialog(title, message) -> str`

### 作用

打开数据表格对话框。

### 返回值

返回用户点击的按钮名。

---

## 7. `show_input_dialog(title, label, typestr, *, value=None, storage_key=None) -> dict`

### 作用

打开输入对话框。

### `typestr` 可选值

- `input`
- `password`
- `multiInput`

### 返回值

对话框结果字典。

### 注意事项

- `multiInput` 会被构造成多行输入框。
- 其他类型会走单行输入或密码框。

---

## 8. `show_datetime_dialog(title, label, kind, formatstr, *, begin_date=None, end_date=None, storage_key=None) -> dict`

### 作用

打开日期/时间选择对话框。

### `kind` 可选值

- `date`
- `dateRange`

### `formatstr` 常见值

- `yyyy-MM-dd`
- `yyyy-MM-dd HH:mm:ss`
- `yyyy/MM/dd`
- `yyyy/MM/dd HH:mm:ss`

### 返回值

对话框结果字典。

---

## 9. `show_select_dialog(title, label, select_type, select_model, *, values=None, is_selected_first=True, storage_key=None) -> dict`

### 作用

打开单选/多选选择对话框。

### `select_type`

- `combobox`
- `list`

### `select_model`

- `single`
- `multi`

### `values`

可传 `list[str]` 或按换行分隔的字符串。

### 返回值

对话框结果字典。

### 注意事项

- `values` 不能为空，否则会报类型错误。
- `is_selected_first=True` 时会默认选中第一项。

---

## 10. `show_select_file_dialog(title, *, folder=None, filter=..., is_multi=False, is_checked_exists=False) -> dict`

### 作用

打开文件选择对话框。

### 返回值

对话框结果字典。

---

## 11. `show_select_folder_dialog(title, *, folder=None) -> dict`

### 作用

打开文件夹选择对话框。

### 返回值

对话框结果字典。

---

## 12. `show_notifycation(message, *, placement='rightbottom', level='info', timeout=3)`

### 作用

发送桌面通知。

### 参数

| 参数名 | 类型 | 是否必填 | 说明 |
|---|---|---|---|
| `message` | `str` | 是 | 通知内容 |
| `placement` | `str` | 否 | 显示位置，源码默认 `rightbottom` |
| `level` | `str` | 否 | `info` / `warning` / `error` |
| `timeout` | `int` / `float` | 否 | 显示时长，默认 3 秒 |

### 返回值

无。

### 注意事项

- 旧文档曾写默认值是 `top`，以当前源码为准，默认是 `rightbottom`。
- `placement` 与 `level` 的完整可选值若需更广覆盖，建议运行验证。

### 示例

```python
from xbot.app.dialog import show_notifycation

show_notifycation("✅ 完成", placement="rightbottom", level="info")
```

### 旧项目常见写法

```python
from xbot.app.dialog import show_notifycation

show_notifycation(
    message="❌ 采集失败",
    placement="top",
    level="warning",
)
```

### 使用建议

- 成功提示：优先用 `level="info"`
- 失败或异常提示：优先用 `level="warning"` 或 `level="error"`
- 旧项目里常见 `placement="top"`，当前源码默认值仍以 `rightbottom` 为准
- 如果只是补充进度提示，建议只传 `message` 和 `level`，避免无必要依赖位置参数

### 需运行验证

- `placement` 的完整可选值
- `level` 是否还有 `success` 等别名
- 不同影刀版本下通知展示样式是否一致

---

## 13. `close_notifycation()`

### 作用

关闭桌面通知框。

### 返回值

无。

---

## 14. 推荐用法

- 运行中提示：`show_notifycation()`
- 用户确认：`show_confirm()`
- 单次提示：`show_alert()` 或 `show_message_box()`
- 复杂参数输入：`show_custom_dialog()`
- 文件/文件夹选择：`show_select_file_dialog()` / `show_select_folder_dialog()`

---

## 15. 备注

- 旧文档中若出现未确认的推断名，建议保留“需运行验证”标注。
- 若要继续细化对话框控件配置，可再单独补一个“自定义对话框配置模板”章节。
