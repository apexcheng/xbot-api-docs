# 登录扩展操作 (activity_7bca6d)

> 调用类型：`both`  
> 主要入口：Code 型登录脚本可直接调用；Visual 型通过 __init__.py 的 processN() 包装调用。  
> 来源说明：本页由原 extension-instructions.md 的 4.4 节拆出；登录参数需按当前安装源码和运行环境复核。  
> 返回：[市场指令扩展开发指南](../extension-instructions.md)

---

**目录/指令名：** `activity_7bca6d` / 登录扩展操作

**调用方式：** both

**用途：** 各类电商/平台自动登录（淘宝、京东、拼多多、抖音、支付宝、1688、千牛等）

**调用入口：**
- Flow（Visual）：`xbot_extensions.activity_7bca6d.processN(...)`（N=1,4,5,6,7,11,12,15,20,21,33,39,40,42,47,56,59,65）
- Direct（Code）：`qn_login.login()`、`taobao_mini.login()`、`login_1688.login()`、`drag_captcha.move_captcha()`、`zfb_login.zfb_login()`

**参数说明：**
- 通用：`username`、`password`、浏览器类型
- 验证码相关：`tj_username`、`tj_password`（图鉴账号）、`识别引擎`
- 淘宝特有：`mode`（登录模式）、`ym_token`、`是否退出已登录`
- 邮箱验证：`验证邮箱`、`邮箱授权码`

**返回值：** `web_page`（登录后的网页对象）

**注意事项：**
- 大部分登录流程是 Visual flow，依赖页面元素定位
- `qn_login.py`、`taobao_mini.py`、`login_1688.py` 是 Code 型，可直接调用
- `drag_captcha.py` 提供滑块拖动能力：`move_captcha(web_page, distance, drag_ele)`
- `zfb_login.py` 提供支付宝登录：`zfb_login(浏览器类型, 登录账号, 登录密码, 重试次数)`
- `utils.py` 提供通用工具：`sdk_create_web_page()`、`drag()`、`get_active_by_web_page()`

**典型调用方式：**
```python
# 千牛登录（Code 型）
from xbot_extensions.activity_7bca6d import qn_login
page = qn_login.login(
    mode="普通模式", engine="图鉴",
    username="xxx", password="xxx",
    retry_count=3, token=""
)

# 淘宝登录（Flow 型）
xbot_extensions.activity_7bca6d.process7(
    mode="普通模式", userid="xxx", password="xxx",
    是否退出已登录=True, ym_token="",
    加载超时时间=30, path_to_chrome_exe="",
    重试次数=3
)

# 滑块拖动
from xbot_extensions.activity_7bca6d.drag_captcha import move_captcha
move_captcha(web_page, distance=100, drag_ele=slider)
```

**调用模板：登录后继续操作**

```python
from xbot_extensions.activity_7bca6d import process56

web_page = process56(
    浏览器类型="chrome",
    京麦账号="xxx",
    京麦密码="xxx",
    图鉴账号="",
    图鉴密码="",
    重试次数=3,
    识别引擎="图鉴",
)

web_page.wait_load_completed(timeout=30)
target = web_page.find_by_xpath('//input[@type="text"]', timeout=20)
target.clipboard_input("测试关键字", delay_after=0.3)
```

**Chrome Profile / 用户环境切换：**

```python
from xbot import web

web.set_user_environment(
    mode="chrome",
    profile_name="Default",
    specifield_userdata=False,
    user_data_dir=None,
)

browser = web.create("https://example.com", mode="chrome", load_timeout=20)
browser.wait_load_completed(timeout=15)
```

使用建议：

- 复用指定 Chrome Profile、维持既有登录态或切换浏览器用户环境时，优先使用原生 `xbot.web.set_user_environment`。
- 这类场景统一使用原生 `xbot.web.set_user_environment`；更多参数说明见 `docs/browser.md`。

---
