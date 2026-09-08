# 网页扩展操作 (web_action)

> 调用类型：`both`  
> 主要入口：Flow 型通过 processN() 调用；Direct 型可调用 element_core.py、js_utility.py、select_date.py 等独立模块。
> 证据边界：页面行为需结合目标网页运行验证。
> 返回：[市场指令索引](../extension-instructions.md)

---

**目录/指令名：** `web_action` / 网页扩展操作

**调用方式：** both

**用途：** 网页元素操作扩展（滚动、隐藏、显示、删除、截图、颜色获取、JS 导入、存储获取等）

**调用入口：**
- Flow（Visual）：`xbot_extensions.web_action.processN(...)`（N=1,2,3,4,6,7,8,10,11,12,13,14,15,18,19,20,21,22,23,24）
- Direct（Code）：`select_date.select_date()`、`auto_drop_selector.set_dropdown()`、`element_core.*`、`js_utility.*`、`web_page_core.*`

**Flow 入口映射：**

| 入口 | 能力 | 主要入参 | 主要输出 |
|---|---|---|---|
| `process1` | 滚动元素至可视区域 | 网页对象、操作目标、垂直方向、水平方向 | — |
| `process2` | 隐藏元素 | 网页对象、操作目标 | — |
| `process3` | 显示元素 | 网页对象、操作目标 | — |
| `process4` | 获取元素背景颜色 | 网页对象、操作目标 | 背景色 |
| `process6` | 获取元素字体颜色 | 网页对象、操作目标 | 字体颜色 |
| `process7` | 导入常用 JS 库 | 网页对象、JS库 | — |
| `process8` | 获取当前激活网页对象 | 网页对象 | `web_page` |
| `process10` | 关闭其他网页 | 保留网页对象 | — |
| `process11` | 导入 JS 库 | 网页对象、JS来源类型、JS来源 | — |
| `process12` | 删除元素 | 网页对象、操作目标 | — |
| `process13` | 浏览器启动配置 | 禁用图片、端口、用户数据、指定用户、最大化、无痕、UA 等 | 命令行 |
| `process14` | 元素长截图 | 网页对象、操作目标、超时时间、保存路径 | — |
| `process15` | 元素增加边框 | 网页对象、操作目标、粗细、样式、颜色 | — |
| `process18` | 取消 HTML 缩放 | 网页对象 | — |
| `process19` | 获取元素背景图片 | 网页对象、操作目标 | 背景图片 |
| `process20` | 获取文本节点内容 | 网页对象、XPath | `text_list` |
| `process21` | 获取 localStorage | 网页对象 | `local_storage` |
| `process22` | 获取 sessionStorage | 网页对象 | `session_storage` |
| `process23` | 获取网页对象类型 | 网页对象 | 网页类型 |
| `process24` | 强制关闭网页 | 网页对象 | — |

Direct 入口的职责也应按模块区分：`element_core.py` 负责元素隐藏、显示、删除、滚动、颜色、边框和长截图；`js_utility.py` 负责 JS 执行和库导入；`web_page_core.py` 负责网页对象、存储和关闭；`select_date.py` / `auto_drop_selector.py` 分别处理智能日期和通用下拉框。不要仅凭 `processN` 编号猜功能。

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
```text
非执行调用说明（不可直接运行）：

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
