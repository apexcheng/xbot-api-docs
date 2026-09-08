# iframe2 扩展指令说明

> 保留的 Python 片段依赖当前流程已取得的对象、输入数据和项目已确认的参数。片段不是独立脚本；[示例边界](../../AGENTS.md)。

> 来源目录：`xbot_extensions/iframe2`
> 结论依据：`package.json`、`prototype.block.json`、`api.py`、`_core.py`
> 整理日期：2026-06-16

---

## 1. 定位

`iframe2` 是一个面向跨 `iframe` / `frame` 场景的市场扩展指令集，核心能力是：

- 先把 `web_page` 包装成可跨域定位的 `iframe_instance`
- 再按 XPath 切换 iframe、查找元素、点击、输入、等待、读取文本或属性
- 在编码版里也可以直接调用 `xbot_extensions.iframe2.api` 暴露的方法

它适合这些场景：

- 原生元素库不方便直接覆盖多层 iframe
- 页面结构变化不大，但需要按 XPath 精确切入某一层 iframe
- 已有 `web_page`，希望继续用 `xbot.web` / `WebElement` 能力完成后续操作

Shadow Root、隐藏块和不同浏览器下的真实稳定性仍需按具体项目运行验证，不要直接当成稳定结论。

---

## 2. 调用方式

### 2.1 可视化指令入口

| 分组 | 指令名 | function | 主要出参 |
|---|---|---|---|
| A0 | `A0-初始化IFrame` | `xbot_extensions.iframe2.init_iframe` | `iframe_instance` |
| A1 | `A1-切换IFrame` | `xbot_extensions.iframe2.to_iframe` | `new_iframe_instance` |
| B1 | `B1-获取元素对象` | `xbot_extensions.iframe2.find_ele` | `web_element` |
| B2 | `B2-获取相似元素` | `xbot_extensions.iframe2.find_all_ele` | `web_element_list` |
| C1 | `C1-点击元素` | `xbot_extensions.iframe2.click_by_xpath` | — |
| C2 | `C2-填写输入框` | `xbot_extensions.iframe2.input_by_xpath` | — |
| C3 | `C3-等待元素` | `xbot_extensions.iframe2.wait_by_xpath` | `wait_result` |
| D1 | `D1-获取元素信息` | `xbot_extensions.iframe2.process2` | `attribute` |
| D2 | `D2-获取元素属性` | `xbot_extensions.iframe2.process3` | `attribute` |

说明：

- `A2-切换至父IFrame` 在 `prototype.block.json` 中存在，但 `hidden=true`，不作为当前稳定公开入口。
- `main`、`_core`、`api`、`js_code`、`测试` 这些 flow 也存在，但不是面向业务开发的主要指令入口。

### 2.2 Python 直接调用入口

`api.py` 中当前可直接调用的公开方法：

- `xbot_extensions.iframe2.api.init_iframe(web_page)`
- `xbot_extensions.iframe2.api.to_iframe(iframe_instance, iframe_xpath, current_global, timeout)`
- `xbot_extensions.iframe2.api.find_ele(iframe_instance, xpath, current_global, timeout)`
- `xbot_extensions.iframe2.api.find_all_ele(iframe_instance, xpath, current_global=False, timeout=10)`
- `xbot_extensions.iframe2.api.click_by_xpath(...)`
- `xbot_extensions.iframe2.api.input_by_xpath(...)`
- `xbot_extensions.iframe2.api.wait(iframe_instance, xpath, state="appear", current_global=False, timeout=20)`
- `xbot_extensions.iframe2.api.get_elem_info(iframe_instance, xpath, op, attr_name=None, current_global=False, timeout=20)`

---

## 3. 参数规律

### 3.1 通用入参

| 源码名 | 可视化含义 | 说明 |
|---|---|---|
| `web_page` | 网页对象 | 仅初始化时使用 |
| `iframe_instance` | IFrame 对象 | 可以直接传 `web_page`；`check_obj` 会自动包装成 `IframePage` |
| `iframe_xpath` / `xpath` | XPath / IFrame_XPath | 支持单个 XPath，也支持数组形式逐层切入 |
| `current_global` | 基于当前 IFrame 全局查找 | `True` 时会遍历当前 iframe 树做全局查找 |
| `timeout` | 超时时间 | `to_iframe` / 查找 / 点击 / 输入默认单位是秒 |

### 3.2 XPath 数组规则

- `find_ele()`、`find_all_ele()`、`to_iframe()` 底层都支持 `xpath` / `iframe_xpath` 传 `list`
- 传数组时会按顺序逐层切入，前面的路径按 iframe 查找，最后一段再查目标元素
- 传数组时不会走 `current_global=True` 的全局查找路径

可理解为：

```python
[
    '//iframe[@id="outer"]',
    '//iframe[@id="inner"]',
    '//button[contains(., "查询")]',
]
```

### 3.3 点击与输入的关键枚举

`click_by_xpath()`：

- `clicks` / `点击方式`：`"单击"`、`"双击"`
- `button` / `鼠标按键`：`"left"`、`"right"`
- `keys` / `辅助按键`：`"none"`、`"alt"`、`"ctrl"`、`"shift"`、`"win"`

`input_by_xpath()`：

- `simulative` / `输入方式` 在可视化层实际有 3 种：
  - `模拟人工输入`
  - `剪贴板输入`
  - `自动化接口输入`
- `append`：是否追加输入
- `contains_hotkey`：输入内容是否包含快捷键
- `force_ime_ENG`：是否强制加载美式键盘
- `send_key_delay`、`focus_timeout`：单位是毫秒
- `delay_after`：单位是秒
- `click_before_input`：输入前是否先点击元素

### 3.4 等待规则

`wait()` / `C3-等待元素`：

- `state` / `等待状态` 只写两种稳定枚举：
  - `appear`
  - `disappear`
- 返回值是 `bool`
- `timeout=""` 或 `None` 时，底层会按无限等待处理

### 3.5 读取元素信息规则

`get_elem_info()` / `D1-获取元素信息` 当前映射到这些操作：

- `获取元素文本内容` -> `get_text()`
- `获取元素源代码` -> `get_html()`
- `获取元素值` -> `get_value()`
- `获取元素位置` -> `get_bounding()`

`D2-获取元素属性` 本质上也是查到元素后调用 `get_attribute(attr_name)`。

---

## 4. 最小示例

### 4.1 初始化并切入一层 iframe

```python
from xbot_extensions.iframe2.api import init_iframe, to_iframe

iframe_page = init_iframe(web_page)
detail_iframe = to_iframe(
    iframe_instance=iframe_page,
    iframe_xpath='//iframe[@id="detail-frame"]',
    current_global=True,
    timeout=5,
)
```

### 4.2 按数组 XPath 逐层切入

```text
非执行调用说明（不可直接运行）：

from xbot_extensions.iframe2.api import find_ele

submit_btn = find_ele(
    iframe_instance=web_page,
    xpath=[
        '//iframe[@id="outer"]',
        '//iframe[@id="inner"]',
        '//button[contains(., "提交")]',
    ],
    current_global=False,
    timeout=5,
)
submit_btn.click()
```

### 4.3 跨 iframe 点击

```text
非执行调用说明（不可直接运行）：

from xbot_extensions.iframe2.api import click_by_xpath

click_by_xpath(
    iframe_instance=web_page,
    xpath='//button[contains(., "查询")]',
    current_global=True,
    simulative=True,
    move_mouse=False,
    button='left',
    keys='none',
    clicks='单击',
    delay_after=1,
    timeout=5,
)
```

### 4.4 跨 iframe 输入

```text
非执行调用说明（不可直接运行）：

from xbot_extensions.iframe2.api import input_by_xpath

input_by_xpath(
    iframe_instance=web_page,
    xpath='//input[@placeholder="请输入关键词"]',
    text='影刀',
    current_global=True,
    simulative='剪贴板输入',
    append=False,
    contains_hotkey=False,
    force_ime_ENG=False,
    send_key_delay=50,
    focus_timeout=1000,
    delay_after=1,
    click_before_input=True,
    timeout=5,
)
```

### 4.5 等待元素出现

```python
from xbot_extensions.iframe2.api import wait

ok = wait(
    iframe_instance=web_page,
    xpath='//div[@class="loading-mask"]',
    state='disappear',
    current_global=True,
    timeout=20,
)
if not ok:
    raise RuntimeError("loading 未消失")
```

### 4.6 读取文本和属性

```python
from xbot_extensions.iframe2.api import get_elem_info

text = get_elem_info(
    iframe_instance=web_page,
    xpath='//span[@class="shop-name"]',
    op='获取元素文本内容',
    current_global=True,
    timeout=5,
)

placeholder = get_elem_info(
    iframe_instance=web_page,
    xpath='//input[@name="keyword"]',
    op='获取元素属性',
    attr_name='placeholder',
    current_global=True,
    timeout=5,
)
```

---

## 5. 注意事项

- `check_obj` 会把传入的 `web_page` 自动包装成 `IframePage`，所以编码版不一定非要先手动 `init_iframe()` 才能调用其他接口。
- `current_global=True` 时，底层会遍历当前 iframe 树查找；如果多个 iframe 同时命中，可能报“无法唯一确定”一类异常。
- 传 XPath 数组时走的是逐层切入逻辑，不依赖全局查找，更适合多层 iframe 已知路径的场景。
- `wait()` 的返回值是布尔值，不直接返回元素对象。
- `input_by_xpath()` 在非剪贴板输入分支里会尝试额外触发一次 `input` 事件，适合有前端监听输入事件的页面。
- 本文只沉淀源码已确认的接口行为；Shadow Root 路径、浏览器兼容性、页面未完全加载时的真实重试表现，仍需运行验证。

---

## 6. 关联文档

- [市场指令入口与签名核验](extension-instructions.md)
