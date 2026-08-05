# 影刀浏览器操作方法整理

> 定位：影刀 / xbot 操作浏览器的开发者参数手册。  
> 重点：把 `xbot.web` 常用方法、参数、默认值、可选值写清楚。  
> 规则：字符串参数必须按文档中的值原样传入，例如 `mode="chrome"`，不是 `Chrome` / `CHROME`。

涉及浏览器、URL、网页业务功能时，除非用户明确要求，否则不要使用 `requests`、`httpx`、`aiohttp`、`urllib` 或其他网络相关 Python 库；只使用 `xbot.web` 及其浏览器对象能力处理页面、请求、Cookie、网络监听和下载。

---

## 0. 相关基础文档

| 文档 | 说明 |
|---|---|
| [`package.md`](package.md) | 元素库、图像库、资源文件、全局变量 |
| [`notification.md`](notification.md) | 桌面通知和对话框 |
| [`logging.md`](logging.md) | 日志记录 |
| [`win32.md`](win32.md) | Windows 桌面自动化 |

---

## 1. 相关文件位置

| 路径 | 作用 |
|---|---|
| `C:\Program Files\ShadowBot\shadowbot-6.0.30\Resources\Code-Activity\Zh-CN\xbot\web\__init__.py` | 浏览器入口：打开、获取、关闭、Cookie、上传下载对话框等 |
| `C:\Program Files\ShadowBot\shadowbot-6.0.30\Resources\Code-Activity\Zh-CN\xbot\web\browser.py` | 浏览器对象：页面信息、导航、查找、等待、执行脚本、截图、网络监听等 |
| `C:\Program Files\ShadowBot\shadowbot-6.0.30\Resources\Code-Activity\Zh-CN\xbot\web\element.py` | 元素对象：点击、输入、悬停、取值、拖拽、上传下载、截图等 |

---

## 2. 参数传值总规则

### 2.1 字符串可选值区分大小写

```python
mode="chrome"
mode="cef"
button="left"
simulative=True
```

错误：

```python
mode="Chrome"
mode="CHROME"
button="Left"
simulative="True"
```

### 2.2 布尔值必须传 Python 布尔值

```python
visible=True
wait_complete=True
ignore_beforeunload=False
```

### 2.3 路径建议使用原始字符串

```python
file_folder = r"C:\Downloads"
file_name = r"C:\test.txt"
```

### 2.4 不要使用影刀可视化选择器

编码版优先用 XPath / CSS，不建议直接依赖可视化选择器。

```python
element = browser.find_by_xpath('//div[@class="item"]', timeout=10)
element = browser.find_by_css('.item', timeout=10)
```

### 2.5 运行日志

```python
from xbot.app import logging

logging.info("第1页采集中...")
```

真实影刀项目里的运行日志优先使用 `xbot.app.logging`，不要使用 Python 内置 `print()`。`xbot.print()` 属于历史兼容写法，普通新代码不再优先推荐。

### 2.6 全局变量 `package.variables`

更完整的 `package` 用法见 [`package.md`](package.md)。

```python
from .package import variables as glv
client_id = glv['client_id']
glv['my_var'] = 'value'
```

---

## 3. 三层能力分工

| 层级 | 推荐使用场景 | 返回对象 |
|---|---|---|
| `xbot.web` | 普通网页自动化主线 | 原生 `WebBrowser` / `WebElement` |
| `xbot_visual.web` | 影刀可视化组件内部 | 多数为原生对象 |

重点：不要默认把 `xbot.web` 理解成带有 `wait_for_element` 一类的等待元素能力。Agent 编码场景里如果只有 XPath 字符串，优先看市场扩展文档里的 `xbot_enhance_tools.browser_utils.wait_appear_by_xpath()` / `wait_disappear_by_xpath()`。

---

## 4. 浏览器类型 `mode`

| 浏览器 | 正确写法 | 说明 |
|---|---|---|
| 自动选择 | `mode="auto"` | 自动选择浏览器类型 |
| 影刀内置浏览器 | `mode="cef"` | 影刀内置浏览器 |
| 谷歌浏览器 | `mode="chrome"` | Google Chrome |
| Edge 浏览器 | `mode="edge"` | Microsoft Edge |
| IE 浏览器 | `mode="ie"` | Internet Explorer |
| 360 安全浏览器 | `mode="360se"` | 360 安全浏览器 |
| 火狐浏览器 | `mode="firefox"` | Firefox |

---

## 5. 打开网页：`xbot.web.create()`

```python
from xbot import web

browser = web.create(
    url="https://example.com",
    mode="chrome",
    load_timeout=20,
    stop_if_timeout=False,
    silent_running=False,
    executable_path=None,
    arguments=None,
)
```

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|---|---|---:|---|---|
| `url` | `str` | 是 | 无 | 要打开的网页地址 |
| `mode` | `str` | 否 | `"cef"` | 浏览器类型，必须小写 |
| `load_timeout` | `int` / `float` | 否 | `20` | `0` 不等待；`-1` 无限等待 |
| `stop_if_timeout` | `bool` | 否 | `False` | 页面加载超时后是否停止加载 |
| `silent_running` | `bool` | 否 | `False` | 是否静默运行 |
| `executable_path` | `str` / `None` | 否 | `None` | 自定义浏览器路径 |
| `arguments` | `list` / `str` / `None` | 否 | `None` | 启动参数 |

实战建议：

- 普通页面打开可先用默认 `load_timeout=20`
- 登录、电商后台、采价等慢页面，旧项目里更常见 `load_timeout=30`
- 如果文档写的是默认值，不代表业务里一定适合默认值；以当前页面加载稳定性为准

---

## 6. 获取网页：`get()` / `get_active()` / `get_all()`

```python
browser = web.get(title="订单")
browser = web.get_active(mode="chrome")
browsers = web.get_all(mode="chrome")
```

注意：`web.get_active()` 依赖浏览器已经启动；如果当前还没有启动浏览器，这里会获取失败。初始化浏览器时建议直接用 `web.create('')`，再按业务需要传入 `mode` 和 `url`。

| 方法 | 主要参数 | 说明 |
|---|---|---|
| `get(title=None, url=None, mode='cef', ...)` | `title` / `url` / `mode` / `open_page` / `page_url` | 按标题或网址匹配已打开网页 |
| `get_active(mode='cef', ...)` | `mode` | 获取当前激活网页 |
| `get_all(mode='cef', ...)` | `title` / `url` / `use_wildcard` | 获取所有网页 |

---

## 7. 关闭网页：`close()` / `close_all()`

```python
browser.close(ignore_beforeunload=False)
web.close_all(mode="chrome", task_kill=False, ignore_beforeunload=False)
```

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `ignore_beforeunload` | `bool` | `False` | 是否忽略“确认离开页面”弹窗 |
| `mode` | `str` | `"cef"` | 要关闭的浏览器类型 |
| `task_kill` | `bool` | `False` | 是否强制结束浏览器进程 |

---

## 8. `Browser` 常用方法

`xbot.web.Browser` 是网页对象。

| 方法 | 作用 |
|---|---|
| `get_url()` | 获取当前网页地址 |
| `get_title()` | 获取当前网页标题 |
| `get_text()` | 获取页面文本 |
| `get_html()` | 获取页面 HTML |
| `activate()` | 激活网页 |
| `activateTab()` | 激活标签页 |
| `close(ignore_beforeunload=False)` | 关闭当前网页 |
| `navigate(url, load_timeout=20)` | 跳转网址 |
| `go_back(load_timeout=20)` | 后退 |
| `go_forward(load_timeout=20)` | 前进 |
| `reload(ignore_cache=False, load_timeout=20)` | 刷新页面 |
| `stop_load()` | 停止加载 |
| `wait_load_completed(timeout=20)` | 等待页面加载完成 |
| `find(selector, timeout=20)` | 查找单个元素 |
| `find_all(selector, timeout=20)` | 查找多个元素 |
| `find_by_css(css_selector, timeout=20)` | 按 CSS 查找单个元素 |
| `find_all_by_css(css_selector, timeout=20)` | 按 CSS 查找多个元素 |
| `find_by_xpath(xpath_selector, timeout=20)` | 按 XPath 查找单个元素 |
| `find_all_by_xpath(xpath_selector, timeout=20)` | 按 XPath 查找多个元素 |
| `scroll_to(location, ...)` | 滚动页面 |
| `execute_javascript(code, argument=None, execution_world="ISOLATED")` | 执行 JavaScript |
| `handle_javascript_dialog(dialog_result, text=None, wait_appear_timeout=20)` | 处理 JS 弹窗 |
| `get_javascript_dialog_text(wait_appear_timeout=20)` | 获取 JS 弹窗文本 |
| `start_monitor_network(...)` | 开始网络监听 |
| `get_responses(...)` | 获取已监听响应 |
| `stop_monitor_network()` | 停止网络监听 |
| `http_request(...)` | 发起网页 HTTP 请求 |
| `screenshot(...)` | 截图 |

---

## 9. 页面基础信息和加载控制

```python
url = browser.get_url()
title = browser.get_title()
text = browser.get_text()
html = browser.get_html()

browser.activate()
browser.activateTab()
browser.navigate("https://example.com/list", load_timeout=20)
browser.go_back(load_timeout=20)
browser.go_forward(load_timeout=20)
browser.reload(ignore_cache=False, load_timeout=20)
browser.stop_load()
browser.wait_load_completed(timeout=20)
```

| 方法 | 参数 | 说明 |
|---|---|---|
| `navigate(url, load_timeout=20)` | `url: str` | 跳转网址 |
| `go_back(load_timeout=20)` | `load_timeout` | 后退 |
| `go_forward(load_timeout=20)` | `load_timeout` | 前进 |
| `reload(ignore_cache=False, load_timeout=20)` | `ignore_cache: bool` | 是否忽略缓存刷新 |
| `wait_load_completed(timeout=20)` | `timeout` | `-1` 无限等待，正数为秒 |

---

## 10. 查找元素

```python
element = browser.find(my_selector, timeout=10)
elements = browser.find_all(my_selector, timeout=10)
element = browser.find_by_css("#kw", timeout=10)
elements = browser.find_all_by_css(".item", timeout=10)
element = browser.find_by_xpath('//input[@name="q"]', timeout=10)
elements = browser.find_all_by_xpath('//div[@class="item"]', timeout=10)
```

从已找到的元素内部继续查找时，直接对元素调用同名方法，并使用以 `.//` 开头的相对 XPath：

```python
row = browser.find_by_xpath('//div[@role="row"]', timeout=10)
name_element = row.find_by_xpath('.//div[@aria-colindex="2"]', timeout=2)
buttons = row.find_all_by_xpath('.//button[contains(@class, "action")]', timeout=2)
```

注意：元素内部查找必须使用 `.//` 表示“从当前元素向下查找”。写成 `//` 会从整个页面根节点开始查找，可能匹配到其他行中的元素。

| 方法 | 参数 | 类型 |
|---|---|---|
| `find` | `selector` | `str` / `Selector` |
| `find_all` | `selector` | `str` / `Selector` |
| `find_by_css` | `css_selector` | `str` |
| `find_all_by_css` | `css_selector` | `str` |
| `find_by_xpath` | `xpath_selector` | `str` |
| `find_all_by_xpath` | `xpath_selector` | `str` |
| 所有查找方法 | `timeout` | `int` / `float` |

| 方法 | 未找到 | 匹配多个 |
|---|---|---|
| `find()` | 抛异常 | 抛异常 |
| `find_all()` | 返回空列表 | 返回列表 |
| `find_by_css()` | 抛异常 | 抛异常 |
| `find_all_by_css()` | 返回空列表 | 返回列表 |
| `find_by_xpath()` | 抛异常 | 抛异常 |
| `find_all_by_xpath()` | 返回空列表 | 返回列表 |

---

## 11. 等待元素

```python
from xbot_extensions.xbot_enhance_tools.browser_utils import (
    wait_appear_by_xpath,
    wait_disappear_by_xpath,
)

element = wait_appear_by_xpath(browser, '//button[contains(., "查询")]', timeout=10)
loading_done = wait_disappear_by_xpath(browser, '//div[@class="loading"]', timeout=30)
```

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `page` | `WebBrowser` | 必填 | 当前网页对象 |
| `xpath` | `str` | 必填 | 要等待的 XPath |
| `timeout` | `int` / `float` | `20` | 等待秒数 |

返回：`wait_appear_by_xpath()` 找到时返回元素，超时返回 `None`；`wait_disappear_by_xpath()` 消失返回 `True`，超时返回 `False`。

---

## 12. `Element` 常用方法

`xbot.web.Element` 用于处理网页元素。

| 方法 | 作用 |
|---|---|
| `click()` | 点击元素 |
| `dblclick()` | 双击元素 |
| `hover()` | 鼠标悬停 |
| `focus()` | 聚焦元素 |
| `input(text)` | 输入文本 |
| `clipboard_input(text)` | 剪切板输入文本 |
| `get_text()` | 获取元素文本 |
| `get_html()` | 获取元素 HTML |
| `get_value()` | 获取元素值 |
| `set_value(value)` | 设置元素值 |
| `get_attribute(name)` | 获取元素属性 |
| `get_all_attributes()` | 获取全部属性 |
| `set_attribute(name, value)` | 设置属性 |
| `parent()` | 获取父元素 |
| `children()` | 获取子元素列表 |
| `check(mode)` | 复选框选中 / 取消 |
| `select(item, mode)` | 下拉框选择 |
| `select_by_index(index)` | 按下标选择 |
| `select_multiple(items, mode, append=False)` | 多选下拉选择 |
| `select_multiple_by_index(indexes, append=False)` | 按下标多选 |
| `is_displayed()` | 判断是否显示 |
| `is_enabled()` | 判断是否可用 |
| `is_checked()` | 判断是否选中 |
| `get_bounding(to96dpi=True, relative_to="screen")` | 获取元素矩形 |
| `scroll_to(location, behavior="instant", search_up=False)` | 滚动元素 |
| `execute_javascript(code, argument=None, execution_world="ISOLATED")` | 执行 JavaScript |
| `upload(file_path)` | 上传文件 |
| `download(file_folder, ...)` | 下载文件 |
| `drag_to(...)` | 拖拽元素 |
| `drag_to_by_cdp(...)` | 用 CDP 拖拽 |

---

## 13. 点击、双击、悬停、聚焦

```python
element.click(button="left", simulative=True, keys="none", delay_after=0.3)
element.dblclick(simulative=True, delay_after=0.3)
element.hover(simulative=True, delay_after=0.3)
element.focus()
```

### 13.1 `click()` 参数

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `button` | `str` | `"left"` | 鼠标左键 / 右键，必须小写 |
| `simulative` | `bool` | `True` | 是否模拟人工点击 |
| `keys` | `str` | `"none"` | 辅助键，必须小写 |
| `delay_after` | `int` / `float` | `1` | 操作后等待 |
| `move_mouse` | `bool` | `False` | 是否显示鼠标轨迹 |
| `anchor` | `tuple` / `None` | `None` | 点击位置和偏移 |

### 13.2 `anchor` 可选值

| 第一项 | 说明 |
|---|---|
| `"topLeft"` | 左上 |
| `"topCenter"` | 上中 |
| `"topRight"` | 右上 |
| `"middleLeft"` | 左中 |
| `"middleCenter"` | 中心 |
| `"middleRight"` | 右中 |
| `"bottomLeft"` | 左下 |
| `"bottomCenter"` | 下中 |
| `"bottomRight"` | 右下 |
| `"random"` | 随机位置 |

### 13.3 `hover()` 参数

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `simulative` | `bool` | `True` | 是否模拟人工移动（鼠标轨迹） |
| `delay_after` | `int` / `float` | `1` | 操作后等待 |

---

## 14. 输入文本

### 14.1 普通输入

```python
element.input(
    text="测试内容",
    simulative=True,
    cdp_input=False,
    driver_input=False,
    append=False,
    contains_hotkey=False,
    force_ime_ENG=False,
    send_key_delay=50,
    focus_timeout=1000,
    delay_after=0.3,
    click_before_input=True,
    input_check=False,
    retry_times=3,
    check_value="",
)
```

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `text` | `str` | 必填 | 要输入的内容 |
| `simulative` | `bool` | `True` | 是否模拟人工输入 |
| `cdp_input` | `bool` | `False` | 极速直写输入 |
| `driver_input` | `bool` | `False` | 驱动输入，非静默模式下生效 |
| `append` | `bool` | `False` | 是否追加输入 |
| `contains_hotkey` | `bool` | `False` | 输入内容是否包含快捷键 |
| `force_ime_ENG` | `bool` | `False` | 是否强制英文输入法 |
| `send_key_delay` | `int` | `50` | 按键间隔（毫秒） |
| `focus_timeout` | `int` | `1000` | 获取焦点超时（毫秒） |
| `delay_after` | `int` / `float` | `1` | 操作后等待 |
| `click_before_input` | `bool` | `True` | 输入前是否点击元素 |
| `input_check` | `bool` | `False` | 是否开启输入校验 |
| `retry_times` | `int` | `3` | 校验失败重试次数 |
| `check_value` | `str` | `""` | 校验目标值 |

### 14.2 剪切板输入

```python
element.clipboard_input(
    "中文内容",
    append=False,
    focus_timeout=1000,
    delay_after=0.3,
    send_key_delay=50,
    click_before_input=True,
)
```

推荐：中文、长文本、输入法不稳定时，优先用 `clipboard_input()`。

---

## 15. 文本、源码、属性和值

```python
text = element.get_text()
html = element.get_html()
value = element.get_value()
element.set_value("新值")
href = element.get_attribute("href")
url = element.get_attribute("absoluteUrl")
attrs = element.get_all_attributes()
element.set_attribute("data-id", "123")
```

| 方法 | 参数 | 说明 |
|---|---|---|
| `get_text()` | 无 | 获取元素文本 |
| `get_html()` | 无 | 获取元素 HTML |
| `get_value()` | 无 | 获取元素值 |
| `set_value(value)` | `value: str` | 设置元素值 |
| `get_attribute(name)` | `name: str` | 获取属性；`"absoluteUrl"` 可取绝对链接 |
| `get_all_attributes()` | 无 | 获取全部属性 |
| `set_attribute(name, value)` | `str, str` | 设置属性 |

---

## 16. 复选框和下拉框

```python
element.check("check")
element.check("uncheck")
element.check("toggle")
checked = element.is_checked()

element.select("选项文本", mode="fuzzy")
element.select_by_index(0)
element.select_multiple(["选项1", "选项2"], mode="fuzzy", append=False)
element.select_multiple_by_index([0, 2], append=False)
```

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `mode` | `str` | `"fuzzy"` | 下拉框匹配模式 |
| `append` | `bool` | `False` | 是否追加选择 |
| `item` | `str` | 必填 | 单选文本 |
| `items` | `list[str]` | 必填 | 多选文本 |
| `index` | `int` | 必填 | 单选下标 |
| `indexes` | `list[int]` | 必填 | 多选下标 |

---

## 17. 状态、坐标、滚动

```python
visible = element.is_displayed()
enabled = element.is_enabled()
checked = element.is_checked()
x, y, width, height = element.get_bounding(to96dpi=True, relative_to="screen")
```

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `to96dpi` | `bool` | `True` | 是否转换为 96 DPI |
| `relative_to` | `str` | `"screen"` | 相对屏幕或窗口客户区 |

```python
browser.scroll_to(location="bottom", behavior="smooth")
browser.scroll_to(location="point", top=500, left=0)
element.scroll_to(location="bottom", behavior="instant", search_up=True)
```

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `location` | `str` | `"bottom"` | `"bottom"` / `"top"` / `"point"` / `"oneScreen"` |
| `behavior` | `str` | `"instant"` / 页面常见 `"smooth"` | 滚动效果 |
| `top` | `int` | `0` | 指定纵坐标 |
| `left` | `int` | `0` | 指定横坐标 |
| `search_up` | `bool` | `False` | 无滚动条时是否向上找可滚动父级 |

---

## 18. 执行 JavaScript

```python
result = browser.execute_javascript(
    """
    function (element, args) {
        return document.title;
    }
    """,
    argument=None,
    execution_world="ISOLATED",
)

result = element.execute_javascript(
    """
    function (element, args) {
        return element.innerText;
    }
    """,
    argument=None,
    execution_world="ISOLATED",
)
```

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `code` | `str` | 必填 | JS 函数字符串，必须是函数形式 |
| `argument` | `str` / `None` | `None` | 传给 JS 的参数，复杂对象建议转 JSON 字符串 |
| `execution_world` | `str` | `"ISOLATED"` | `"ISOLATED"` / `"MAIN"` |

注意：

- `execution_world` 建议按文档中的大写值传入，不要自行改成小写
- 需要隔离执行时优先用 `"ISOLATED"`
- 需要直接访问页面主环境对象时再考虑 `"MAIN"`

---

## 19. 网页弹窗

```python
browser.handle_javascript_dialog("ok", text=None, wait_appear_timeout=20)
browser.handle_javascript_dialog("cancel", wait_appear_timeout=20)
text = browser.get_javascript_dialog_text(wait_appear_timeout=20)
```

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `dialog_result` | `str` | `"ok"` | `"ok"` / `"cancel"` |
| `text` | `str` / `None` | `None` | prompt 输入内容 |
| `wait_appear_timeout` | `int` / `float` | `20` | 等待弹窗出现 |

---

## 20. Cookie

```python
cookies = web.get_cookies("https://example.com", mode="chrome")
cookie = web.get_cookie("https://example.com", mode="chrome", name="token")
web.set_cookie("https://example.com", mode="chrome", name="token", value="abc")
web.remove_cookie("https://example.com", "token", mode="chrome")
```

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `url` | `str` | 必填 | Cookie 对应网址 |
| `mode` | `str` | `"cef"` | 浏览器类型 |
| `name` | `str` / `None` | `None` | Cookie 名称 |
| `value` | `str` / `None` | `None` | Cookie 值 |
| `domain` | `str` / `None` | `None` | 域名 |
| `path` | `str` / `None` | `None` | 路径 |
| `secure` | `bool` / `None` | `None` | 是否 secure |
| `session` | `bool` / `None` | `None` | 是否会话 Cookie |
| `sessionCookie` | `bool` | `True` | `set_cookie` 中是否为会话 Cookie |
| `expires` | `int` | `100` | 持久化 Cookie 有效秒数 |
| `httpOnly` | `bool` | `False` | 是否 HttpOnly |

---

## 21. 上传和下载

```python
web.handle_upload_dialog(
    filenames=[r"C:\test.txt"],
    dialog_result="ok",
    mode="chrome",
    simulative=False,
    clipboard_input=True,
    wait_appear_timeout=20,
)

file_path = web.handle_save_dialog(
    file_folder=r"C:\Downloads",
    dialog_result="ok",
    mode="chrome",
    file_name="demo.xlsx",
    overwrite=True,
    wait_complete=True,
    wait_complete_timeout=300,
)

element.upload(r"C:\test.txt")
file_path = element.download(r"C:\Downloads", file_name="result.xlsx", wait_complete=True)
file_path = browser.dowload_url(
    "https://example.com/demo.xlsx",
    r"C:\Downloads",
    file_name="demo.xlsx",
    overwrite=True,
    wait_complete=True,
)
```

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `filenames` | `str` / `list[str]` | 必填 | 单文件或多文件 |
| `dialog_result` | `str` | `"ok"` | `"ok"` / `"cancel"` |
| `file_folder` | `str` | 必填 | 保存目录 |
| `file_name` | `str` / `None` | `None` | 保存文件名 |
| `overwrite` | `bool` | `True` | 同名是否覆盖 |
| `wait_complete` | `bool` | `False` | 是否等待下载完成 |
| `wait_complete_timeout` | `int` / `float` | `300` | 下载完成超时 |

注意：方法名是 `dowload_url`，不是 `download_url`。

业务里凡是“下载文件后等待结果”的场景，统一优先使用市场扩展 `xbot_enhance_tools.browser_utils.wait_download_file(download_dir=None, filename_pattern=None, timeout=300, start_time=None)`；这里的 `wait_complete` / `wait_complete_timeout` 只作为原生接口参数说明保留。

---

## 22. 截图

```python
browser.screenshot(
    folder_path=r"C:\screenshots",
    file_name="page.png",
    full_size=True,
    piece_height=0,
    height=0,
)

path = element.screenshot(
    folder_path=r"C:\screenshots",
    filename="button.png",
)
```

| 参数 | 类型 | 默认值 |
|---|---|---|
| `folder_path` | `str` | 必填 |
| `file_name` / `filename` | `str` / `None` | `None` |
| `full_size` | `bool` | `True` |
| `piece_height` | `int` | `0` |
| `height` | `int` | `0` |

---

## 23. 网络监听和请求

```python
# 开始监听必须放在触发页面请求之前；URL 不需要写完整，尽量用通配符提高命中率
browser.start_monitor_network(url="*client.action*", use_wildcard=True, resource_type="XHR|Fetch")

# 已在 start_monitor_network 里限定 URL 时，读取时通常只按资源类型取数即可
responses = browser.get_responses(resource_type="XHR|Fetch")
browser.stop_monitor_network()

result = browser.http_request(
    url="https://example.com/api/list",
    method="GET",
    headers={"token": "abc"},
    body=None,
    save_filename=None,
    connect_timeout=30,
    dowload_timeout=300,
)
```

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `url` | `str` | `""` | 过滤请求 URL |
| `use_wildcard` | `bool` | `False` | 是否通配符匹配 |
| `resource_type` | `str` | `"All"` | `"All"` / `"XHR"` / `"Fetch"` / `"Script"` / `"Image"` 等 |
| `method` | `str` | `"GET"` | 请求方法 |
| `headers` | `dict` / `None` | `None` | 请求头 |
| `body` | 任意 / `None` | `None` | 请求体 |
| `save_filename` | `str` / `None` | `None` | 保存响应文件路径 |
| `connect_timeout` | `int` | `30` | 连接超时秒数 |
| `dowload_timeout` | `int` | `300` | 等待下载/响应超时秒数；源码拼写是 `dowload_timeout` |

`start_monitor_network()` / `get_responses()` 说明：

- 两个方法都支持 `url`、`use_wildcard`、`resource_type` 过滤；`resource_type` 可用 `|` 连接多个类型，例如 `"XHR|Fetch"`。
- 监听要在点击、刷新、滚动、加载更多等触发请求动作之前开启。
- 指定 URL 时优先使用通配符，例如 `url="*client.action*", use_wildcard=True`；不要强依赖完整 URL，避免查询参数或域名变化导致匹配不到。
- 如果 `start_monitor_network()` 已经指定了 URL 过滤，后续 `get_responses(resource_type="XHR|Fetch")` 通常不必重复传 URL。
- `get_responses()` 返回 `list[dict]`。单条记录常见键包括：`url`、`type`、`headers`、`body`、`base64Encoded`、`status`、`requestHeaders`、`requestBody`、`method`，读取方式如 `item["body"]`。
- `body` 的具体内容形态、非 JSON 响应和异常请求表现，仍建议以真实运行日志为准，需运行验证。

---

## 24. 拖拽

```python
element.drag_to(top=100, left=0, simulative=True, move_speed="middle")
element.drag_to_by_cdp(targetX=500, targetY=300, targetType="viewport", move_speed="middle")
```

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `top` / `left` | `int` | `0` | 相对位移 |
| `targetX` / `targetY` | `int` | `0` | 目标坐标 |
| `targetType` | `str` | `"viewport"` | `"viewport"` / `"screen"` |
| `move_speed` | `str` | `"middle"` | `"instant"` / `"fast"` / `"middle"` / `"slow"` |

---

## 25. 自动处理弹窗和用户环境

```python
web.auto_handle_popup(
    handle_method="close_dialog",
    close_button=close_button_selector,
)

web.auto_handle_popup(
    handle_method="execute_process",
    element_selector=target_selector,
    process="流程名",
    package=__name__,
)

web.set_user_environment(
    mode="chrome",
    profile_name="Profile 1",
    specifield_userdata=False,
    user_data_dir=None,
)
```

| 参数 | 可选值 | 说明 |
|---|---|---|
| `handle_method` | `"close_dialog"` / `"execute_process"` | 自动关闭弹窗 / 执行指定流程 |
| `close_button` | `Selector` | 关闭按钮选择器 |
| `element_selector` | `Selector` | 触发流程的目标元素 |
| `process` | `str` | 流程名，不要带 `.py` |
| `package` | `str` | 一般传 `__name__` |
| `mode` | `str` | 通常 `"chrome"` / `"edge"` |
| `profile_name` | `str` | 浏览器 Profile 名 |
| `specifield_userdata` | `bool` | 是否指定用户数据目录 |
| `user_data_dir` | `str` / `None` | `specifield_userdata=True` 时使用的用户数据目录 |

---

## 26. 常用模板

### 26.1 XPath 等待后点击

```python
from xbot import web
from xbot_extensions.xbot_enhance_tools.browser_utils import wait_appear_by_xpath

browser = web.get_active(mode="chrome")

element = wait_appear_by_xpath(browser, '//button[contains(., "查询")]', timeout=10)
if not element:
    raise RuntimeError("目标元素未出现")

element.click(delay_after=0.3)
```

### 26.2 历史包装层写法需运行验证

```python
# 历史项目里可能看到类似写法，但不要默认当前环境可用
# 如需等待 XPath 字符串，优先参考 xbot_enhance_tools.browser_utils
from xbot_extensions.xbot_enhance_tools.browser_utils import wait_appear_by_xpath

element = wait_appear_by_xpath(page, '//button[contains(., "查询")]', timeout=10)
if not element:
    raise RuntimeError("目标元素等待超时")
element.click(delay_after=0.3)
```

说明：如果历史代码里出现包装层方法或 `page.wait_for_element()` 这类写法，需运行验证，不要直接当成当前稳定能力。

### 26.3 输入中文

```python
input_ele = browser.find_by_xpath('//input[@name="wd"]')
input_ele.clipboard_input("影刀 RPA", delay_after=0.3)
```

### 26.4 下载文件

```python
button = browser.find_by_xpath('//button[contains(., "下载")]')
file_path = button.download(
    file_folder=r"C:\Downloads",
    file_name="result.xlsx",
    wait_complete=True,
)
```

### 26.5 电商项目常用浏览器组织模式

```python
from xbot import web

browser = web.create(link, mode="chrome", load_timeout=20)
browser.wait_load_completed(timeout=15)

if not ensure_login(browser, account):
    raise RuntimeError("账号未登录")

for page in web.get_all(mode="chrome"):
    if page.get_url() != browser.get_url():
        page.close()
```

适用经验：

- 电商页通常先 `web.create(..., mode="chrome", load_timeout=20)`，再补一层 `browser.wait_load_completed(timeout=15)`。
- 登录流程建议先判断是否已登录，未登录再跳登录页，不要每次无条件重登。
- 多页面任务结束后，可用 `web.get_all(mode="chrome")` 遍历关闭无关页面，只保留当前任务页。
- `browser.get_cookies()` 可用于登录态判定；例如项目里会按 Cookie 名判断拼多多是否已登录。

`browser.get_cookies()` 示例：

```python
cookies = browser.get_cookies()
names = [cookie.get("name") for cookie in cookies]
is_logged_in = "PDDAccessToken" in names or "pdd_user_id" in names
```

说明：

- Cookie 名判断属于项目实战模式，不代表所有站点都适用；跨项目复用前建议先运行验证。
- 页面清理逻辑只适合“当前浏览器实例由本流程统一接管”的任务，不要误关用户手工保留的工作页。

### 26.6 Chrome Profile 与登录态复用

需要复用登录态、切换浏览器用户环境或指定 Chrome Profile 时，优先使用原生 `xbot.web.set_user_environment`。Profile 名称可以来自账号表或配置项；为空时可回退到 `"Default"`。

```python
from xbot import web

profile = str(profile_name or "Default").strip() or "Default"
web.set_user_environment(
    mode="chrome",
    profile_name=profile,
    specifield_userdata=False,
    user_data_dir=None,
)

browser = web.create("https://example.com", mode="chrome", load_timeout=20)
browser.wait_load_completed(timeout=15)
```

登录态处理建议：

- 进入业务页后，先通过 URL、Cookie 或页面元素判断是否已登录，已登录就继续，不要每次无条件重登。
- 未登录时再跳转登录页、执行登录流程，或明确返回失败交给业务层处理。
- 如果某个平台只能依赖人工保持登录态，未登录时应显式失败，不要伪装成功或静默继续。
- 登录态判断方式必须按目标站点实测，不要把某个站点的 Cookie 名或 URL 规则当成通用规则。

---

## 27. 经验

- 涉及浏览器、URL、页面元素、Cookie、下载、网络监听等网页业务时，默认使用 `xbot.web` 和浏览器对象能力；除非用户明确要求接口方式，不要改用 `requests`、`httpx`、`aiohttp`、`urllib` 绕过浏览器。
- 需要页面登录态、Cookie、JS 渲染、下载对话框或页面事件时，更应走浏览器能力，不要把网页当成普通 HTTP 接口猜。
- 能用 XPath、CSS、元素库或页面对象定位时，不要先写坐标点击；坐标受分辨率、缩放、窗口位置影响，只适合作为确实无法定位元素时的最后手段。
- XPath 失效时，优先人工修正定位规则，不要在代码里堆多个未验证候选 XPath 做兜底。
- 中文、长文本、输入法不稳定的场景，优先用元素的 `clipboard_input()`；全局 `send_keys()` 更适合快捷键或当前焦点明确的短输入。
- 历史项目中的 `wait_for_element()`、自定义 `page.xxx()` 等包装层，不要直接当成当前稳定能力；只有 XPath 字符串等待需求时，优先使用 `xbot_enhance_tools.browser_utils.wait_appear_by_xpath()` / `wait_disappear_by_xpath()`。
- 下载后等待文件生成，优先使用 `xbot_enhance_tools.browser_utils.wait_download_file(download_dir=None, filename_pattern=None, timeout=300, start_time=None)`；不要为同类下载等待重复维护旧封装。
- 登录流程建议先判断是否已登录，未登录再跳登录页；登录态判断必须按目标站点实测，不要把某个站点的 Cookie 名、URL 规则或按钮文案当成通用规则。
- 页面清理只适合“当前浏览器实例由本流程统一接管”的任务，不要误关用户手工保留的工作页。
- 需要监听接口响应时，优先按稳定片段设置通配规则，例如 `start_monitor_network(url="*client.action*", use_wildcard=True, resource_type="XHR|Fetch")`；监听和读取响应时的 `resource_type` 要保持一致。
- 排查浏览器问题时，先确认对象是否来自 `xbot.web`，再确认字符串参数、元素定位、iframe、弹窗、登录态和页面加载状态，最后再考虑坐标、图像识别或项目专用包装层。

---

## 28. 排错速查

| 报错 / 现象 | 常见原因 | 处理 |
|---|---|---|
| `ChromiumBrowser` 没有 `wait_for_element` | 当前对象没有该方法，不代表 `get_active_page()` 入口不存在 | 不要依赖 `wait_for_element`；XPath 等待改看 `xbot_enhance_tools.browser_utils.*` |
| `mode="Chrome"` 不稳定或报错 | 字符串大小写错误 | 改成 `mode="chrome"` |
| `download_url` 不存在 | 源码拼写是 `dowload_url` | 调用 `browser.dowload_url(...)` |
| `dowload_timeout` 拼写奇怪 | 源码就是这个拼写 | 按源码传 `dowload_timeout` |
| 元素匹配多个 | 单元素查找要求唯一 | 改选择器，或用 `find_all*` 后自己取 |
| 中文输入异常 | 输入法干扰 | 改用 `clipboard_input()` |
| 下载后文件还没生成 | 没等下载完成 | 业务里统一改用 `xbot_enhance_tools.browser_utils.wait_download_file(...)` |
| `dialog_result="OK"` 不确定 | 源码注释是小写 `ok` / `cancel` | 建议传 `"ok"` / `"cancel"` |
