# 广告杀手 (ad_killer)

> 调用类型：`both`  
> 主要入口：通过 close_ads / close_ads_win 包装入口调用，也可在确认兼容后直接使用 _core.py 中的 AdKiller。  
> 来源说明：本页由原 extension-instructions.md 的 4.6 节拆出；close_type 等枚举值以源码为准。  
> 返回：[市场指令扩展开发指南](../extension-instructions.md)

---

**目录/指令名：** `ad_killer` / 广告杀手

**调用方式：** both

**用途：** 异步关闭网页广告弹窗、Win32 弹窗

**调用入口：**
- Flow：`xbot_extensions.ad_killer.close_ads(网页对象, 广告Xpath, 使用内置广告Xpath, 关闭方式)`
- Flow：`xbot_extensions.ad_killer.close_ads_win(元素选择器列表)`

**参数说明：**
- `广告Xpath`：自定义广告元素 XPath
- `使用内置广告Xpath`：是否使用内置广告名单（布尔值）
- `关闭方式`：`"hidden"`（隐藏，默认）或 `"click"`（点击关闭）
- `元素选择器列表`：Win32 弹窗的选择器列表

**默认值：**
- `关闭方式`：`"hidden"`
- `使用内置广告Xpath`：`False`

**关闭方式 `关闭方式` 详解：**

| 值 | 行为 | 适用场景 | 注意事项 |
|---|---|---|---|
| `"hidden"`（默认） | 使用 CSS `display: none` 或 `visibility: hidden` 隐藏元素 | 广告元素已渲染但不可见 | 广告元素 DOM 仍存在，页面结构不变；**推荐优先使用** |
| `"click"` | 模拟人工点击广告的关闭按钮（需要广告有可点击的关闭按钮） | 弹窗类广告有明确关闭按钮 | 需要广告 DOM 中有可定位的关闭按钮元素；否则无效 |

**`使用内置广告Xpath` 行为：**

| 值 | 行为 |
|---|---|
| `True` | 使用内置广告名单（`ad_conf.py` 中按域名分类的黑名单 XPath） |
| `False` | 仅使用 `广告Xpath` 参数传入的自定义 XPath |

**内置广告名单说明：**
- 内置名单在 `ad_conf.py` 中，按域名分类
- 部分广告可能同时出现在多个域名下
- 使用 `True` 时仍可叠加自定义 `广告Xpath`

**注意事项：**
- Web 广告关闭：网页刷新后失效，需要重新调用
- Win32 广告关闭：后台监测，全流程调用一次即可，随主流程结束而结束
- 内置广告名单在 `ad_conf.py` 中，按域名匹配
- `_core.py` 中的 `AdKiller` 类可直接使用

**选择建议：**

- 能确认广告元素但不确定关闭按钮时，优先用 `关闭方式="hidden"`
- 只有在广告弹窗确实存在可点击关闭按钮时，再用 `关闭方式="click"`
- 已知目标站点经常弹广告时，优先尝试 `使用内置广告Xpath=True`
- 内置名单不生效时，再补自定义 `广告Xpath`

**典型调用方式：**
```python
# 方式一：使用内置广告名单（推荐）
xbot_extensions.ad_killer.close_ads(
    网页对象=web_page,
    广告Xpath="",
    使用内置广告Xpath=True,
    关闭方式="hidden"
)

# 方式二：自定义 XPath + hidden
xbot_extensions.ad_killer.close_ads(
    网页对象=web_page,
    广告Xpath="//div[@class='ad-modal']",
    使用内置广告Xpath=False,
    关闭方式="hidden"
)

# 方式三：点击关闭按钮（广告必须有关闭按钮）
xbot_extensions.ad_killer.close_ads(
    网页对象=web_page,
    广告Xpath="//div[@class='ad']//button[@class='close-btn']",
    使用内置广告Xpath=False,
    关闭方式="click"
)

# 方式四：组合使用（内置 + 自定义）
xbot_extensions.ad_killer.close_ads(
    网页对象=web_page,
    广告Xpath="//div[@class='ad-modal']",
    使用内置广告Xpath=True,
    关闭方式="hidden"
)

# 直接使用核心类
from xbot_extensions.ad_killer._core import AdKiller
killer = AdKiller(web_page, ad_xpath="//div[@class='ad']",
                  close_type="hidden", use_builtin=True)
killer.close_ads()
```

**调用模板：登录后先关广告再采集**

```python
from xbot_extensions.activity_7bca6d import process21
from xbot_extensions.ad_killer import close_ads

web_page = process21(
    浏览器类型="chrome",
    识别引擎="图鉴",
    账号="xxx",
    密码="xxx",
    验证码重试次数=3,
    是否创建新页面=True,
)

close_ads(
    网页对象=web_page,
    广告Xpath="",
    使用内置广告Xpath=True,
    关闭方式="hidden",
)

web_page.wait_load_completed(timeout=30)
rows = web_page.find_all_by_xpath('//div[@class="item"]', timeout=10)
```

---
