# 登录扩展操作 (activity_7bca6d)

> 调用类型：`both`  
> 主要入口：Code 型登录脚本可直接调用；Visual 型通过 __init__.py 的 processN() 包装调用。  
> 证据边界：登录参数需按当前安装版本和运行环境复核。
> 返回：[市场指令索引](../extension-instructions.md)

---

**目录/指令名：** `activity_7bca6d` / 登录扩展操作

**调用方式：** both

**用途：** 各类电商/平台自动登录（淘宝、京东、拼多多、抖音、支付宝、1688、千牛等）

**调用入口：**
- Flow（Visual）：`xbot_extensions.activity_7bca6d.processN(...)`（N=1,4,5,6,7,11,12,15,20,21,33,39,40,42,47,56,59,65）
- Direct（Code）：`qn_login.login()`、`taobao_mini.login()`、`login_1688.login()`、`drag_captcha.move_captcha()`、`zfb_login.zfb_login()`

**公开入口速查：**

| 入口 | 用途 | 主要入参 | 主要输出 / 定位 |
|---|---|---|---|
| `process1` | 巨量登录 | web_type、username、password、tj_username、tj_password | `web_page` |
| `process4` | 抖店登录 | username、password、验证邮箱、邮箱授权码、退出已登录账户、验证码失败最大重试次数 | `web_page` |
| `process5` | 有赞登录 | web_type、username、password、tj_username、tj_password | `web_page` |
| `process6` | 京东登录 | web_mode、username、password、tj_username、tj_password、rec_count、login_url | `web_page`；京东买家平台 |
| `process7` | 淘宝登录 | mode、userid、password、是否退出已登录、ym_token、加载超时时间、path_to_chrome_exe、重试次数 | `web_page`；淘宝 / 天猫买家平台 |
| `process11` | 滑块拖动 | web_page、drag_start_element、background_element | 无固定业务输出 |
| `process12` | 巨量纵横登录 | web_type、username、password、tj_username、tj_password | `web_page` |
| `process15` | 电商罗盘登录 | 网页对象、username、password、登录的店铺名称、是否要退出已登录账号 | `web_page` |
| `process20` | 支付宝登录 | 浏览器类型、登录账号、登录密码、重试次数 | `web_page` |
| `process21` | 拼多多登录 | 浏览器类型、识别引擎、账号、密码、验证码重试次数、是否创建新页面 | 网页对象 |
| `process33` | 爱库存登录 | 浏览器类型、账号、密码、验证重试次数 | `web_page` |
| `process39` | 旺店通登录 | 用户名、密码 | `process_result` |
| `process40` | 京准通登录 | 网页对象、识别引擎、登录用户名、登录密码、子平台、退出已登录账户、短信验证码获取接口 | 网页对象 |
| `process42` | 阿里妈妈数智登录 | 浏览器类型、账户、密码、退出已登录账户、短信验证码接口 | `web_page` |
| `process47` | 巨量引擎邮箱登录 | 登录邮箱、登录密码、验证邮箱、邮箱授权码、退出已登录账户、retry_cnt | `web_page` |
| `process56` | 京麦登录 | 浏览器类型、京麦账号、京麦密码、图鉴账号、图鉴密码、重试次数、识别引擎 | 网页对象；京东商家后台 |
| `process59` | 电商罗盘策略登陆 | 网页对象、账号、密码、登录的店铺名称、是否要退出已登陆账号 | 无固定业务输出 |
| `process65` | 美团开店宝滑块 | 网页对象、滑块元素、滑动条背景图元素 | 无固定业务输出 |
| `qn_login.login()` | 千牛登录 | mode、engine、username、password、retry_count、token | `web_page`；淘宝 / 天猫商家后台 |
| `taobao_mini.login()` | 淘宝 mini 登录 | mode、engine、username、password、token、retry_count | 需按当前版本复核 |
| `login_1688.login()` | 1688 登录 | mode、engine、username、password、retry_count、token | `web_page` |
| `drag_captcha.move_captcha()` | 滑块拖动 | web_page、distance、drag_ele | 无固定业务输出 |
| `zfb_login.zfb_login()` | 支付宝登录 Direct 入口 | 以当前公开签名为准 | 需按当前版本复核 |

**参数说明：**
- 通用：`username`、`password`、浏览器类型
- 验证码相关：`tj_username`、`tj_password`（图鉴账号）、`识别引擎`
- 淘宝特有：`mode`（登录模式）、`ym_token`、`是否退出已登录`
- 邮箱验证：`验证邮箱`、`邮箱授权码`

**返回值：** 多数登录入口返回 `web_page`（登录后的网页对象），具体以入口映射和当前安装版本为准。

上面的 `web_page` 只是多数登录入口的常见输出，不代表该扩展所有入口都返回网页对象；例如滑块流程没有同类输出，`process39` 返回 `process_result`。新增调用时按上表和当前安装版本的公开签名判断，不要把一种返回结构套到整个扩展。

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

使用建议：

- Chrome Profile、`set_user_environment()`、`get_all()` 与页面清理属于原生浏览器能力，统一按 [`browser.md`](../browser.md) 处理，本页不重复维护第二套参数和生命周期规则。
- `process6` 是京东买家平台登录，`process56` 是京麦商家后台；`process7` 是淘宝 / 天猫买家平台，`qn_login` 是千牛商家后台。不要因为同属京东或淘宝体系就混用买家登录与商家后台登录。
- 普通购物页、买家订单页优先匹配买家平台入口；商家经营后台、店铺管理页优先匹配京麦 / 千牛等商家后台入口。
- `process56` 与 `process6` 的完整参数差异、`qn_login.login()` 的 `engine` 完整枚举仍以当前安装版本为准，必要时用 `inspect.signature()` 复核。

---
