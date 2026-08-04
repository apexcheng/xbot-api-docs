# 增强工具2026 (xbot_enhance_tools)

> 调用类型：`direct python`  
> 主要入口：直接调用 browser_utils.py、exception_utils.py、shop_utils.py、win_utils.py、ntfy_message.py 中的公开函数；__init__.py 仅导入模块。
> 来源说明：本页由原 extension-instructions.md 的 4.8 节拆出；网页登录和下载等待需运行验证。  
> 返回：[市场指令扩展开发指南](../extension-instructions.md)

---

**目录/指令名：** `xbot_enhance_tools` / 增强工具2026

**调用方式：** direct python

**用途：** 面向 `xbot` 的增强工具包。当前已收录浏览器 XPath 等待、下载等待、异常详情格式化、商家后台登录辅助、Windows 元素可点击判断，以及 ntfy 消息发送与接收。

**调用入口：**
- `from xbot_extensions.xbot_enhance_tools import exception_utils, browser_utils, shop_utils, win_utils, ntfy_message`
- `from xbot_extensions.xbot_enhance_tools.browser_utils import wait_appear_by_xpath`
- `from xbot_extensions.xbot_enhance_tools.browser_utils import wait_disappear_by_xpath`
- `from xbot_extensions.xbot_enhance_tools.browser_utils import wait_download_file`
- `from xbot_extensions.xbot_enhance_tools.exception_utils import format_exception_detail`
- `from xbot_extensions.xbot_enhance_tools.shop_utils import login_pdd_seller`
- `from xbot_extensions.xbot_enhance_tools.shop_utils import login_qianniu`
- `from xbot_extensions.xbot_enhance_tools.shop_utils import login_jingmai`
- `from xbot_extensions.xbot_enhance_tools.shop_utils import login_alipay`
- `from xbot_extensions.xbot_enhance_tools.shop_utils import login_douyin_seller`
- `from xbot_extensions.xbot_enhance_tools.win_utils import is_win_element_clickable`
- `from xbot_extensions.xbot_enhance_tools.ntfy_message import send_ntfy_message`
- `from xbot_extensions.xbot_enhance_tools.ntfy_message import receive_ntfy_message`

**当前能力：**
- `wait_appear_by_xpath(page, xpath, timeout=20)`：循环调用 `page.find_by_xpath(xpath, timeout=1)`，找到即返回元素，超时返回 `None`
- `wait_disappear_by_xpath(page, xpath, timeout=20)`：循环调用 `page.find_by_xpath(xpath, timeout=1)`，查找抛异常即视为已消失，返回 `True`；超时返回 `False`
- `wait_download_file(download_dir=None, filename_pattern=None, timeout=300, start_time=None)`：等待下载目录中的文件下载完成；`download_dir` 不传时默认使用当前用户下载目录，不存在则回退到 `~/下载`；`filename_pattern` 可选，传了按指定文件名关键词或 glob 表达式匹配，不传按本次新出现并稳定的文件判断；`start_time` 建议在点击下载前用 `time.time()` 记录
- `format_exception_detail(e)`：返回错误信息、报错位置、当前时间、函数名、代码行，适合通知或日志汇总
- `login_pdd_seller(account, password, profile=None)`：打开拼多多商家中心登录页，登录后按 URL 是否离开 `login` 判断结果
- `login_qianniu(account, password, profile=None)`：打开千牛商家工作台登录页，登录后按 URL 是否离开 `login` 判断结果
- `login_jingmai(account, password, profile=None)`：打开京麦商家工作台登录页，登录后按 URL 是否离开 `login` 判断结果
- `login_alipay(account, password, profile=None)`：打开支付宝登录页，切到“账密登录”，输入账号密码并提交，等待页面跳转后按 URL 是否仍包含 `login` 判断结果
- `login_douyin_seller(account, password, profile=None)`：打开抖音电商后台 `https://fxg.jinritemai.com/login`，切换到邮箱登录，输入邮箱和密码，必要时勾选协议并提交；按 URL 是否离开 `login` 判断结果
- `is_win_element_clickable(element)`：判断 `Win32Window.find()` / `find_all()` 返回的 Win 元素是否显示、可用、矩形有效，且中心点落在当前屏幕范围内；满足时返回 `True`，否则返回 `False`
- `send_ntfy_message(message, topic, server="https://ntfy.sh")`：向指定 ntfy topic 发送纯文本消息；成功返回 `True`，失败抛出异常
- `receive_ntfy_message(topic, server="https://ntfy.sh", since="10m", timeout=15)`：从指定 ntfy topic 拉取一条消息；有消息时返回包含 `id`、`time`、`message` 的字典，无消息时返回 `None`

**适用场景：**
- Agent 编码场景里只有 XPath 字符串，没有元素库选择器
- XPath 字符串等待优先使用本扩展里的等待方法
- 下载文件业务需要统一等待下载完成
- 需要把异常对象整理成更易读的文本内容
- 需要在编码版里直接调用商家后台登录辅助函数，并复用指定 Chrome profile
- 点击 Windows 元素前，需要先判断元素当前是否适合直接点击
- 需要在 iOS 快捷指令与影刀 RPA 之间传递短信、验证码或其他文本消息

**最小示例：**

```python
import time

from xbot_extensions.xbot_enhance_tools.browser_utils import (
    wait_appear_by_xpath,
    wait_disappear_by_xpath,
    wait_download_file,
)
from xbot_extensions.xbot_enhance_tools.exception_utils import format_exception_detail
from xbot.app import logging


element = wait_appear_by_xpath(page, '//button[contains(., "查询")]', timeout=10)
if not element:
    raise RuntimeError("查询按钮等待超时")
element.click()

if not wait_disappear_by_xpath(page, '//div[@class="loading"]', timeout=20):
    raise RuntimeError("loading 未消失")

start_time = time.time()
file_path = wait_download_file(filename_pattern="result.xlsx", timeout=300, start_time=start_time)

try:
    page.find_by_xpath('//input[@name="keyword"]', timeout=3).input("影刀")
except Exception as e:
    detail = format_exception_detail(e)
    logging.error(detail)
```

**商家后台登录示例：**

```python
from xbot_extensions.xbot_enhance_tools import shop_utils


ok = shop_utils.login_pdd_seller("账号", "密码", profile="Default")
if not ok:
    raise RuntimeError("拼多多商家中心登录失败")

ok = shop_utils.login_alipay("账号", "密码", profile="Default")
if not ok:
    raise RuntimeError("支付宝登录失败")

ok = shop_utils.login_douyin_seller("邮箱账号", "密码", profile="Default")
if not ok:
    raise RuntimeError("抖音店铺登录失败")
```

**Windows 元素可点击判断示例：**

```python
from xbot_extensions.xbot_enhance_tools.win_utils import is_win_element_clickable


element = window.find("确定", timeout=3)
if not is_win_element_clickable(element):
    raise RuntimeError("确定按钮当前不可点击")
element.click()
```

**ntfy 消息发送与接收示例：**

```python
from xbot_extensions.xbot_enhance_tools.ntfy_message import (
    receive_ntfy_message,
    send_ntfy_message,
)


send_ntfy_message("验证码 382914", topic="your-private-topic")

message = receive_ntfy_message(
    topic="your-private-topic",
    since="10m",
    timeout=15,
)
if message:
    print(message["message"])
```

**注意事项：**
- 这是市场扩展能力，不是原生 `xbot` 内置 API
- `wait_appear_by_xpath()` / `wait_disappear_by_xpath()` 面向 XPath 字符串，不是元素库选择器
- `wait_disappear_by_xpath()` 的判定依据是“查找抛异常即视为已消失”
- 下载文件业务统一优先使用 `wait_download_file()`，不要再为同类业务单独维护旧下载等待封装
- `shop_utils` 中的登录 XPath 会随平台页面变化，当前页面行为需运行验证
- 商家后台登录只处理账号密码输入和提交，不处理验证码、扫码、安全验证、短信验证、人机验证等复杂分支
- 抖音登录使用邮箱账号；协议勾选仅在页面显示未勾选状态时处理，登录后的跳转和风控页面仍需在实际环境确认
- 当前 `__init__.py` 仅做模块导入，不建议把隐藏的 Visual block 当作主要调用方式
- `is_win_element_clickable()` 只判断元素当前状态和中心点是否在屏幕范围内，不会自动滚动、激活窗口或处理遮挡；复杂窗口状态仍需运行验证
- `ntfy_message.py` 依赖 `requests`，当前市场指令项目已登记该依赖
- 使用公共 `ntfy.sh` 时，topic 即消息地址的一部分，应使用难以猜测的私有 topic，避免传递账号密码等高敏感信息
- `receive_ntfy_message()` 使用 ntfy JSON 流接口轮询，并返回读取到的第一条消息；是否需要去重或持久化消费进度由调用方处理
- 后续如果该扩展新增能力，应按源码实际接口继续补充，不要提前推断

---
