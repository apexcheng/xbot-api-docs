# 增强工具2026 (xbot_enhance_tools)

> 调用类型：`direct python`  
> 主要入口：直接调用 browser_utils.py、exception_utils.py、shop_utils.py 中的公开函数；__init__.py 仅导入模块。  
> 来源说明：本页由原 extension-instructions.md 的 4.8 节拆出；网页登录和下载等待需运行验证。  
> 返回：[市场指令扩展开发指南](../extension-instructions.md)

---

**目录/指令名：** `xbot_enhance_tools` / 增强工具2026

**调用方式：** direct python

**用途：** 面向 `xbot` 的增强工具包。当前已收录浏览器 XPath 等待、下载等待、异常详情格式化和商家后台登录辅助。

**调用入口：**
- `from xbot_extensions.xbot_enhance_tools import exception_utils, browser_utils, shop_utils`
- `from xbot_extensions.xbot_enhance_tools.browser_utils import wait_appear_by_xpath`
- `from xbot_extensions.xbot_enhance_tools.browser_utils import wait_disappear_by_xpath`
- `from xbot_extensions.xbot_enhance_tools.browser_utils import wait_download_file`
- `from xbot_extensions.xbot_enhance_tools.exception_utils import format_exception_detail`
- `from xbot_extensions.xbot_enhance_tools.shop_utils import login_pdd_seller`
- `from xbot_extensions.xbot_enhance_tools.shop_utils import login_qianniu`
- `from xbot_extensions.xbot_enhance_tools.shop_utils import login_jingmai`
- `from xbot_extensions.xbot_enhance_tools.shop_utils import login_alipay`

**当前能力：**
- `wait_appear_by_xpath(page, xpath, timeout=20)`：循环调用 `page.find_by_xpath(xpath, timeout=1)`，找到即返回元素，超时返回 `None`
- `wait_disappear_by_xpath(page, xpath, timeout=20)`：循环调用 `page.find_by_xpath(xpath, timeout=1)`，查找抛异常即视为已消失，返回 `True`；超时返回 `False`
- `wait_download_file(download_dir=None, filename_pattern=None, timeout=300, start_time=None)`：等待下载目录中的文件下载完成；`download_dir` 不传时默认使用当前用户下载目录，不存在则回退到 `~/下载`；`filename_pattern` 可选，传了按指定文件名关键词或 glob 表达式匹配，不传按本次新出现并稳定的文件判断；`start_time` 建议在点击下载前用 `time.time()` 记录
- `format_exception_detail(e)`：返回错误信息、报错位置、当前时间、函数名、代码行，适合通知或日志汇总
- `login_pdd_seller(account, password, profile=None)`：打开拼多多商家中心登录页，登录后按 URL 是否离开 `login` 判断结果
- `login_qianniu(account, password, profile=None)`：打开千牛商家工作台登录页，登录后按 URL 是否离开 `login` 判断结果
- `login_jingmai(account, password, profile=None)`：打开京麦商家工作台登录页，登录后按 URL 是否离开 `login` 判断结果
- `login_alipay(account, password, profile=None)`：打开支付宝登录页，切到“账密登录”，输入账号密码并提交，等待页面跳转后按 URL 是否仍包含 `login` 判断结果

**适用场景：**
- Agent 编码场景里只有 XPath 字符串，没有元素库选择器
- 原生 `wait_appear()` / `wait_disappear()` 不方便直接用于 XPath 字符串等待
- 下载文件业务需要统一等待下载完成
- 需要把异常对象整理成更易读的文本内容
- 需要在编码版里直接调用商家后台登录辅助函数，并复用指定 Chrome profile

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
```

**注意事项：**
- 这是市场扩展能力，不是原生 `xbot` 内置 API
- `wait_appear_by_xpath()` / `wait_disappear_by_xpath()` 面向 XPath 字符串，不是元素库选择器
- `wait_disappear_by_xpath()` 的判定依据是“查找抛异常即视为已消失”
- 下载文件业务统一优先使用 `wait_download_file()`，不要再为同类业务单独维护旧下载等待封装
- `shop_utils` 中的登录 XPath 会随平台页面变化，当前页面行为需运行验证
- 商家后台登录只处理账号密码输入和提交，不处理验证码、扫码、安全验证、短信验证、人机验证等复杂分支
- 当前 `__init__.py` 仅做模块导入，不建议把隐藏的 Visual block 当作主要调用方式
- 后续如果该扩展新增能力，应按源码实际接口继续补充，不要提前推断

---
