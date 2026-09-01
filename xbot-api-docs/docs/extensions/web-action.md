# 网页扩展操作 (web_action)

> 调用类型：`both`  
> 主要入口：Flow 型通过 processN() 调用；Direct 型可调用 element_core.py、import_js.py、select_date.py 等独立模块。  
> 证据边界：页面行为需结合目标网页运行验证。
> 返回：[市场指令索引](../extension-instructions.md)

---

**目录/指令名：** `web_action` / 网页扩展操作

**调用方式：** both

**用途：** 网页元素操作扩展（滚动、隐藏、显示、删除、截图、颜色获取、JS 导入、存储获取等）

**调用入口：**
- Flow（Visual）：`xbot_extensions.web_action.processN(...)`（N=1,2,3,4,6,7,8,10,11,12,13,14,15,18,19,20,21,22,23,24）
- Direct（Code）：`select_date.select_date()`、`auto_drop_selector.set_dropdown()`、`element_core.*`、`js_utility.*`、`web_page_core.*`

**参数说明：**
- `网页对象` / `web_page`：网页对象
- `操作目标`：WebElement 元素
- `垂直方向` / `水平方向`：滚动方向（`"start"`、`"center"`、`"end"`、`"nearest"`）
- `JS库`：如 `"jquery"`、`"html2canvas.min.js"`
- `JS来源类型`：`"在线地址"`、`"文件路径"`、`"字符串"`
- `JS来源`：URL 或 JS 代码文本

**返回值：**
- `背景色`、`字体颜色`、`背景图片`、`text_list`、`local_storage`、`session_storage`、`网页类型`、`web_page`、`命令行`

**注意事项：**
- `element_core.py` 提供了所有元素操作的原子函数，可直接 import 使用
- `js_utility.py` 提供 JS 执行和库导入
- `web_page_core.py` 提供网页对象管理（激活、关闭、存储获取）
- `select_date.py` 是智能日期选择器，支持 Shadow DOM

**典型调用方式：**
```python
# Flow 型
xbot_extensions.web_action.process1(
    网页对象=page, 操作目标=elem,
    垂直方向="center", 水平方向="center"
)

# Direct 型 - 元素操作
from xbot_extensions.web_action.element_core import (
    hide_element, get_background_color, scroll_into_view
)
hide_element(web_page, element)
color = get_background_color(web_page, element)
scroll_into_view(web_page, element, block="center", inline="center")

# Direct 型 - JS 导入
from xbot_extensions.web_action.js_utility import import_js_lib
import_js_lib(web_page, element, "jquery")

# Direct 型 - 存储获取
from xbot_extensions.web_action.web_page_core import (
    get_local_storage, get_session_storage
)
storage = get_local_storage(web_page)
session = get_session_storage(web_page)

# Direct 型 - 智能日期选择
from xbot_extensions.web_action.select_date import select_date
select_date(web_page, date_elem, "2024-01-01", "2024-12-31", simulative=True)
```

---
