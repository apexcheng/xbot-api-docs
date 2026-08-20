# 影刀市场指令扩展开发指南

> 分析范围：13 个常用市场指令目录
> 最近补充：2026-08-20
> 分析原则：不猜测，所有结论均有文件依据

---

## 目录

- [一、目录总览](#一目录总览)
- [二、指令映射表](#二指令映射表)
- [三、调用规则](#三调用规则)
- [四、开发指令](#四开发指令)
- [五、证据引用](#五证据引用)

---

## 一、目录总览

| 目录名 | 指令名 | 调用类型 | package.json | prototype.block.json | __init__.py | core.py / py_api.py | 独立 .py 文件 |
|---|---|---|---|---|---|---|---|
| `activity_47680f64` | 小工具指令集 | both | ✅ | ✅ | ✅ (processN 包装) | ❌ | ✅ (5 个业务 + 5 个 process) |
| `activity_5b77c4ce` | 钉钉AI表格 | direct python | ✅ | ✅ | ✅ (仅 import) | ❌ | ✅ (3 个) |
| `dingtalk_bot_message` | 钉钉企业机器人消息_v2 | both | ✅ | ✅ | ✅ (process1/2/3) | ✅ (core.py) | ✅ (4 个) |
| `activity_7bca6d` | 登录扩展操作 | both | ✅ | ✅ | ✅ (17 个 process) | ❌ | ✅ (11 个业务) |
| `xbot_enhance_tools` | 增强工具2026 | direct python | ✅ | ✅ | ✅ (无 processN 包装) | ❌ | ✅ (`browser_utils.py`、`exception_utils.py`、`shop_utils.py`、`win_utils.py`、`excel_utils.py`、`ntfy_message.py`) |
| `guanyi_erp_api` | C-ERP API | direct python | ✅ | ✅ | ✅ (仅 import) | ✅ (core.py) | ✅ (7 个业务) |
| `activity_excel_v2` | Excel扩展操作 | flow | ✅ | ✅ | ✅ (包装入口 + 模块导入) | ❌ | ✅ (Visual / Code flow 对应 .py + 工具模块) |
| `activity_a90a8311` | C-ERP 市场指令 | flow | ✅ | ✅ | ✅ (processN 包装) | ❌ | ✅ (Visual flow) |
| `activity_df0688e4` | ERP订单详情查询与字段翻译 | direct python | ✅ | ✅ | ✅ (模块导入) | ✅ | ✅ (`select_order_dteail.py`、`translation.py`) |
| `activity_179ea575` | 离线 OCR | flow | ✅ | ✅ | ✅ (`process1`) | ❌ | ✅ (OCR 业务模块) |
| `iframe2` | XPath跨域获取网页元素 | both | ✅ | ✅ | ❌ | ✅ (`_core.py`) | ✅ (`api.py`、`js_code.py`) |
| `ad_killer` | 广告杀手 | both | ✅ | ✅ | ✅ (close_ads/close_ads_win) | ✅ (_core.py) | ✅ (7 个) |
| `web_action` | 网页扩展操作 | both | ✅ | ✅ | ✅ (18 个 process) | ❌ | ✅ (10 个业务) |

**调用类型说明：**
- `flow`：通过 `__init__.py` 中的 `processN()` 包装函数调用 Visual 流程
- `direct python`：直接调用 `.py` 文件中的 `main()` 或其他函数
- `both`：同时支持两种调用方式

---

## 二、指令映射表

### 2.1 activity_47680f64 — 小工具指令集

| 指令显示名 | 调用类型 | 对应 function | __init__.py 入口 | 独立 Python | 主要入参 | 主要出参 |
|---|---|---|---|---|---|---|
| 递归创建文件夹 | direct python | `CreateDir` | — | `CreateDir.py` | 创建文件夹路径 | — |
| 移动文件到上一级目录 | direct python | `MoveToPardir` | — | `MoveToPardir.py` | 文件路径 | 移动后文件路径 |
| 解压文件到当前目录 | flow | `process1` | `process1()` | `process1.py` (仅 main) | 压缩文件路径、删除原文件 | 文件路径列表 |
| 下载一个文件 | flow | `process2` | `process2()` | `process2.py` (仅 main) | 是否弹窗下载、保存文件夹、文件名、下载前文件数量、浏览器下载保存路径、最大等待时长 | 文件路径 |
| 快捷日期检验和转换 | flow | `process3` | `process3()` | `process3.py` (仅 main) | 日期范围或快捷日期、quick_select_map | 勾选日期 |
| 日期检验 | direct python | `DateStringCheck` | — | `DateStringCheck.py` | 开始日期、结束日期、日期格式 | — |
| 获取收件箱最新的一封邮件 | direct python | `latest_email` | — | `latest_email.py` | email、password、select_from | latest_email |
| 获取短信验证码 | direct python | `get_SMS_code` | — | `get_SMS_code.py` | 获取验证码接口 | 验证码 |
| 入参校验 | flow | `process5` | `process5()` | `process5.py` (仅 main) | 传入值、可选项列表、是否多选、分隔符 | — |

**调用方式总结：**
- **Code 型 flow**（CreateDir、MoveToPardir、DateStringCheck、latest_email、get_SMS_code）：直接调用对应 `.py` 文件中的 `main()` 函数
- **Visual 型 flow**（process1~5）：通过 `__init__.py` 中的 `processN()` 包装函数调用 `xbot_visual.process.run()`

---

### 2.2 activity_5b77c4ce — 钉钉AI表格

| 指令显示名 | 调用类型 | 对应 function | __init__.py 入口 | 独立 Python | 主要入参 | 主要出参 |
|---|---|---|---|---|---|---|
| 通用表格操作 | direct python | `general_table_action` | —（仅 import） | `general_table_action.py` | action、client_id、client_secret、base_id、sheet、user_id、params、space_id | ret |

**调用方式总结：**
- `__init__.py` 仅做 import，没有 processN 包装函数
- **唯一公开指令**是 `general_table_action`，直接调用 `general_table_action.py` 中的 `main()`
- `croe.py` 是底层 SDK（约 50+ 个函数，如 `yd_list_spaces`、`yd_insert_records`、`yd_upload_attachment`），不直接暴露为指令

**action 枚举值（30个）：**
创建数据表、获取所有数据表、获取数据表、更新数据表、删除数据表、新增字段、获取所有字段、更新字段、删除字段、新增多行记录、新增记录、获取多行记录、获取多行记录分页、获取记录、更新多行记录、更新记录、删除多条记录、上传附件、上传附件并新增记录、上传附件并更新记录、获取空间列表、获取空间列表分页、获取空间信息、获取space_id、获取spaceId、获取文件列表、获取文件列表分页、获取AI表格列表、搜索AI表格、搜索表格文件

**底层 SDK 关键函数（croe.py）：**
| 函数 | 用途 |
|---|---|
| `yd_get_access_token(client_id, client_secret)` | 获取钉钉 accessToken |
| `yd_ai_table_action(action, client_id, client_secret, ...)` | 统一入口函数 |
| `yd_create_sheet(...)` | 创建数据表 |
| `yd_insert_records(...)` | 新增多行记录 |
| `yd_list_records(...)` | 获取多行记录 |
| `yd_update_records(...)` | 更新多行记录 |
| `yd_delete_records(...)` | 删除多条记录 |
| `yd_upload_attachment(...)` | 上传附件 |

---

### 2.3 dingtalk_bot_message — 钉钉企业机器人消息_v2

| 指令显示名 | 调用类型 | 对应 function | __init__.py 入口 | 独立 Python | 主要入参 | 主要出参 |
|---|---|---|---|---|---|---|
| 发送私聊消息 | direct python 优先 | `send_dingtalk_private` | `py_api.py` | `py_api.py` | message_type、content、app_key、app_secret、user_ids / user_mobiles | 钉钉接口结果 |
| 发送群聊消息 | direct python 优先 | `send_dingtalk_group` | `py_api.py` | `py_api.py` | message_type、content、应用机器人或 webhook 参数 | 钉钉接口结果 |
| 群聊使用说明 | flow | `process3` | `process3()` | — | — | help |
| 生成markdown表格 | direct python | `to_table_format` | —（import） | `to_table_format.py` | data、max_cell_length | md_table |

**调用方式总结：**
- 新代码优先从 `xbot_extensions.dingtalk_bot_message.py_api` 导入 `send_dingtalk_group()` / `send_dingtalk_private()`。
- `process1()` / `process2()` 仍可兼容旧项目，但会额外经过 Visual flow，不再作为编码版首选。
- `to_table_format.py` 可直接调用 `to_markdown_table(data, max_cell_length)`。
- 发送失败会抛出异常，不要按返回 `False` 处理。

**message_type 枚举值：** text、markdown、image

---

### 2.4 activity_7bca6d — 登录扩展操作

| 指令显示名 | 调用类型 | 对应 function | __init__.py 入口 | 独立 Python | 主要入参 | 主要出参 |
|---|---|---|---|---|---|---|
| 巨量登录 | flow | `process1` | `process1()` | — | web_type、username、password、tj_username、tj_password | web_page |
| 抖店登录 | flow | `process4` | `process4()` | — | username、password、验证邮箱、邮箱授权码、退出已登录账户、验证码失败最大重试次数 | web_page |
| 有赞登录 | flow | `process5` | `process5()` | — | web_type、username、password、tj_username、tj_password | web_page |
| 京东登录 | flow | `process6` | `process6()` | — | web_mode、username、password、tj_username、tj_password、rec_count、login_url | web_page | 买家平台（京东购物） |
| 淘宝登录 | flow | `process7` | `process7()` | — | mode、userid、password、是否退出已登录、ym_token、加载超时时间、path_to_chrome_exe、重试次数 | web_page | 买家平台（淘宝/天猫） |
| 京麦登录 | flow | `process56` | `process56()` | — | 浏览器类型、京麦账号、京麦密码、图鉴账号、图鉴密码、重试次数、识别引擎 | 保存网页对象 | 商家后台（京麦） |
| 滑块拖动 | flow | `process11` | `process11()` | — | web_page、drag_start_element、background_element | — |
| 巨量纵横登录 | flow | `process12` | `process12()` | — | web_type、username、password、tj_username、tj_password | web_page |
| 电商罗盘登录 | flow | `process15` | `process15()` | — | 网页对象、username、password、登录的店铺名称、是否要退出已登录账号 | web_page |
| 支付宝登录 | flow | `process20` | `process20()` | — | 浏览器类型、登录账号、登录密码、重试次数 | web_page |
| 拼多多登录 | flow | `process21` | `process21()` | — | 浏览器类型、识别引擎、账号、密码、验证码重试次数、是否创建新页面 | 网页对象 |
| 爱库存登录 | flow | `process33` | `process33()` | — | 浏览器类型、账号、密码、验证重试次数 | web_page |
| 旺店通登录 | flow | `process39` | `process39()` | — | 用户名、密码 | process_result |
| 京准通登录 | flow | `process40` | `process40()` | — | 网页对象、识别引擎、登录用户名、登录密码、子平台、退出已登录账户、短信验证码获取接口 | 输出网页对象 |
| 阿里妈妈数智登录 | flow | `process42` | `process42()` | — | 浏览器类型、账户、密码、退出已登录账户、短信验证码接口 | web_page |
| 巨量引擎邮箱登录 | flow | `process47` | `process47()` | — | 登录邮箱、登录密码、验证邮箱、邮箱授权码、退出已登录账户、retry_cnt | web_page |
| 京麦登录 | flow | `process56` | `process56()` | — | 浏览器类型、京麦账号、京麦密码、图鉴账号、图鉴密码、重试次数、识别引擎 | 保存网页对象 |
| 电商罗盘策略登陆 | flow | `process59` | `process59()` | — | 网页对象、账号、密码、登录的店铺名称、是否要退出已登陆账号 | — |
| 美团开店宝滑块 | flow | `process65` | `process65()` | — | 网页对象、滑块元素、滑动条背景图元素 | — |
| 千牛登录 | direct python | `qn_login` | — | `qn_login.py` | mode、engine、username、password、retry_count、token | web_page | 商家后台（千牛工作台） |
| 淘宝mini登录 | direct python | `taobao_mini` | — | `taobao_mini.py` | mode、engine、username、password、token、retry_count | — |
| 1688登录 | direct python | `login_1688` | — | `login_1688.py` | mode、engine、username、password、retry_count、token | web_page |
| 滑块拖动 | direct python | `drag_captcha` | — | `drag_captcha.py` | web_page、distance、drag_ele | — |
| 支付宝登录(源码) | direct python | `zfb_login` | — | `zfb_login.py` | — | — |
| 淘宝注册辅助 | direct python | `taobao_reg` | — | `taobao_reg.py` | — | — |

**通用参数说明：**
- `tj_username` / `tj_password`：图鉴（验证码识别平台）账号密码
- `识别引擎`：验证码识别引擎选择
- `mode`：登录模式（如普通模式、扫码模式等）
- `ym_token`：云码 token（另一验证码识别平台）

**平台区分说明：**

| 平台类型 | 登录指令 | 说明 |
|---|---|---|
| 买家平台 | `process6`(京东) / `process7`(淘宝) | 面向普通消费者购物平台 |
| 商家后台 | `process56`(京麦) / `qn_login`(千牛) | 商家经营管理后台 |

- `process6` 京东登录：京东买家平台（购物）
- `process56` 京麦登录：京东商家后台（京麦工作台）
- `process7` 淘宝登录：淘宝/天猫买家平台（购物）
- `qn_login` 千牛登录：淘宝/天猫商家后台（千牛工作台）

**选择建议：**

- 目标是普通购物页、订单页、买家视角页面时，优先选 `process6` / `process7`
- 目标是商家后台、经营工作台、店铺管理页时，优先选 `process56` / `qn_login`
- 不要因为平台同属京东或淘宝，就把买家登录和商家后台登录混用
- `qn_login` 是 Direct Python 调用，适合编码版直接控制；`process7` 是 Visual flow，更接近可视化流程入口

**需运行验证：**

- `process56` 与 `process6` 的全部入参差异
- `qn_login.login()` 中 `engine` 的完整可选值

---

### 2.5 guanyi_erp_api — C-ERP API

| 指令显示名 | 调用类型 | 对应 function | __init__.py 入口 | 独立 Python | 主要入参 | 主要出参 |
|---|---|---|---|---|---|---|
| 查询库存 | direct python | `select_stock` | —（import） | `select_stock.py` | max_page_no、app_key、session_key、secret、item_code、item_sku_code、warehouse_code | stocks |
| 查询商品 | direct python | `select_item` | —（import） | `select_item.py` | max_page_no、code、app_key、session_key、secret、combine | items |
| 查询组合商品 | direct python | `select_combine_item` | —（import） | `select_combine_item.py` | code | items、context |
| 翻译Dict | direct python | `translation` | —（import） | `translation.py` | record | new_record |
| 订单查询详情 | direct python | `select_order_dteail` | —（import） | `select_order_dteail.py` | code、platform_code | order_detail |
| 查询订单列表 | direct python | `select_order_list` | —（import） | `select_order_list.py` | platform_code、date_type、shop_code、code、has_cancel_data、start_date、end_date | orders |
| 商品查询by商品条码 | direct python | `select_item_by_sku_code` | —（import） | `select_item_by_sku_code.py` | 商品条码 | items |

**调用方式总结：**
- `__init__.py` 仅 import，没有 processN 包装
- 所有指令都是 **Code 型 flow**，直接调用对应 `.py` 文件中的 `main()`
- `core.py` 提供基础能力：`make_sign()`、`urlencode_utf8()`、`build_payload()`、`gy_call()`（管易 ERP API 签名和请求封装）

**API 配置：**
- 地址：`http://api.guanyierp.com/rest/erp_open`
- 签名规则：`MD5(secret + json_str + secret).upper()`
- 凭证来源：`package.variables` 中的 `APP_KEY`、`SESSION_KEY`、`SECRET`

---

### 2.6 iframe2 — XPath跨域获取网页元素

| 指令显示名 | 调用类型 | 对应 function | __init__.py 入口 | 独立 Python | 主要入参 | 主要出参 |
|---|---|---|---|---|---|---|
| A0-初始化IFrame | both | `init_iframe` | — | `api.py` | `web_page` | `iframe_instance` |
| A1-切换IFrame | both | `to_iframe` | — | `api.py` | `iframe_instance`、`iframe_xpath`、`current_global`、`timeout` | `new_iframe_instance` |
| B1-获取元素对象 | both | `find_ele` | — | `api.py` | `iframe_instance`、`xpath`、`current_global`、`timeout` | `web_element` |
| B2-获取相似元素 | both | `find_all_ele` | — | `api.py` | `iframe_instance`、`xpath`、`current_global`、`timeout` | `web_element_list` |
| C1-点击元素 | both | `click_by_xpath` | — | `api.py` | `iframe_instance`、`xpath`、`current_global`、点击参数 | — |
| C2-填写输入框 | both | `input_by_xpath` | — | `api.py` | `iframe_instance`、`xpath`、`text`、输入参数 | — |
| C3-等待元素 | both | `wait` | — | `api.py` | `iframe_instance`、`xpath`、`state`、`current_global`、`timeout` | `wait_result` |
| D1-获取元素信息 | both | `get_elem_info` | — | `api.py` | `iframe_instance`、`xpath`、`op`、`current_global`、`timeout` | `attribute` |
| D2-获取元素属性 | both | `get_elem_info` | — | `api.py` | `iframe_instance`、`xpath`、`attr_name`、`current_global`、`timeout` | `attribute` |

**调用方式总结：**
- 可视化层通过 `prototype.block.json` 暴露 A/B/C/D 分组指令，主入口是 `xbot_extensions.iframe2.*`
- 编码版可直接调用 `api.py` 中的 `init_iframe`、`to_iframe`、`find_ele`、`find_all_ele`、`click_by_xpath`、`input_by_xpath`、`wait`、`get_elem_info`
- `_core.py` 提供 `IframePage`、XPath 数组逐层切入、全局查找、跨域 JS 执行等核心实现

**当前已确认规律：**
- `iframe_instance` 可直接传 `web_page`，`check_obj` 会自动包装成 `IframePage`
- `xpath` / `iframe_xpath` 支持传数组，数组模式下按层切入，不走全局查找
- `wait` 的状态枚举按源码只确认 `appear` / `disappear`
- `click_by_xpath` 的点击方式只确认 `单击` / `双击`
- `input_by_xpath` 的输入方式区分 `模拟人工输入`、`剪贴板输入`、`自动化接口输入`

**专题文档：**
- [iframe2 扩展指令说明](iframe2-extension.md)

---

### 2.7 ad_killer — 广告杀手

| 指令显示名 | 调用类型 | 对应 function | __init__.py 入口 | 独立 Python | 主要入参 | 主要出参 |
|---|---|---|---|---|---|---|
| 异步关闭广告(web) | both | `close_ads` | `close_ads()` | `close_ads.py` (main) | 网页对象、广告Xpath、使用内置广告Xpath、关闭方式 | — |
| 异步关闭广告(win) | both | `close_ads_win` | `close_ads_win()` | `close_ads_win.py` (main) | 元素选择器列表 | — |

**调用方式总结：**
- `__init__.py` 包装了两个 flow 入口
- `_core.py` 提供真实业务逻辑：
  - `AdKiller` 类：`close_type` 默认 `"hidden"`，`use_builtin` 布尔值控制是否使用内置广告名单
  - `AdKillerWin` 类：Win32 弹窗关闭
- `api.py` 提供异步入口：`async_close_ads()`、`async_close_ads_win()`

**关闭方式枚举值：** `"hidden"`（默认）、`"click"`

---

### 2.8 web_action — 网页扩展操作

| 指令显示名 | 调用类型 | 对应 function | __init__.py 入口 | 独立 Python | 主要入参 | 主要出参 |
|---|---|---|---|---|---|---|
| 智能日期选择器 | direct python | `select_date` | —（import） | `select_date.py` | web_page、date_elem、date_start、date_end、simulative | — |
| 通用设置下拉框 | direct python | `auto_drop_selector` | —（import） | `auto_drop_selector.py` | web_page、drop_ele、target_text、click_flag、simulative | web_element |
| 滚动元素至可视区域 | flow | `process1` | `process1()` | `process1.py` (main) | 网页对象、操作目标、垂直方向、水平方向 | — |
| 隐藏元素 | flow | `process2` | `process2()` | `process2.py` (main) | 网页对象、操作目标 | — |
| 显示元素 | flow | `process3` | `process3()` | `process3.py` (main) | 网页对象、操作目标 | — |
| 获取元素背景颜色 | flow | `process4` | `process4()` | `process4.py` (main) | 网页对象、操作目标 | 背景色 |
| 获取元素字体颜色 | flow | `process6` | `process6()` | `process6.py` (main) | 网页对象、操作目标 | 字体颜色 |
| 获取元素背景图片 | flow | `process19` | `process19()` | `process19.py` (main) | 网页对象、操作目标 | 背景图片 |
| 导入常用JS库 | flow | `process7` | `process7()` | `process7.py` (main) | 网页对象、JS库 | — |
| 导入JS库 | flow | `process11` | `process11()` | `process11.py` (main) | 网页对象、JS来源类型、JS来源 | — |
| 删除元素 | flow | `process12` | `process12()` | `process12.py` (main) | 网页对象、操作目标 | — |
| 元素长截图 | flow | `process14` | `process14()` | `process14.py` (main) | 网页对象、操作目标、超时时间、保存路径 | — |
| 元素增加边框 | flow | `process15` | `process15()` | `process15.py` (main) | 网页对象、操作目标、粗细、样式、颜色 | — |
| 取消HTML缩放 | flow | `process18` | `process18()` | `process18.py` (main) | 网页对象 | — |
| 获取当前激活的网页对象 | flow | `process8` | `process8()` | `process8.py` (main) | 网页对象 | web_page |
| 关闭其他网页 | flow | `process10` | `process10()` | `process10.py` (main) | 保留网页对象 | — |
| 浏览器启动配置 | flow | `process13` | `process13()` | `process13.py` (main) | 禁用图片、指定端口、用户数据、指定用户、最大化、无痕模式、设置UA、隐藏崩溃弹窗、禁止默认浏览器检查 | 命令行 |
| 获取文本节点内容 | flow | `process20` | `process20()` | `process20.py` (main) | 网页对象、XPath | text_list |
| 获取本地存储 | flow | `process21` | `process21()` | `process21.py` (main) | 网页对象 | local_storage |
| 获取会话存储 | flow | `process22` | `process22()` | `process22.py` (main) | 网页对象 | session_storage |
| 获取网页对象类型 | flow | `process23` | `process23()` | `process23.py` (main) | 网页对象 | 网页类型 |
| 强制关闭网页 | flow | `process24` | `process24()` | `process24.py` (main) | 网页对象 | — |

**底层能力文件：**
| 文件 | 关键函数 |
|---|---|
| `element_core.py` | `hide_element`、`show_element`、`remove_element`、`scroll_into_view`、`get_background_color`、`get_font_color`、`get_background_image`、`add_border`、`long_screenshot` |
| `js_utility.py` | `execute_javascript`、`import_js_lib`、`import_js_lib_by_src` |
| `web_page_core.py` | `get_active_by_web_page`、`close_other_web_page`、`chromium_options`、`get_local_storage`、`get_session_storage`、`close_web_page` |

**垂直/水平方向枚举值：** `"start"`、`"center"`、`"end"`、`"nearest"`

**JS库枚举值：** `"jquery"`、`"html2canvas.min.js"`、`"$x.js"`

**JS来源类型枚举值：** `"在线地址"`、`"文件路径"`、`"字符串"`

---

### 2.9 xbot_enhance_tools — 增强工具2026

| 指令显示名 | 调用类型 | 对应 function | __init__.py 入口 | 独立 Python | 主要入参 | 主要出参 |
|---|---|---|---|---|---|---|
| XPath 等待出现 | direct python | `wait_appear_by_xpath` | —（仅模块导入） | `browser_utils.py` | `page`、`xpath`、`timeout` | `WebElement` 或 `None` |
| XPath 等待消失 | direct python | `wait_disappear_by_xpath` | —（仅模块导入） | `browser_utils.py` | `page`、`xpath`、`timeout` | `bool` |
| 等待下载完成 | direct python | `wait_download_file` | —（仅模块导入） | `browser_utils.py` | `download_dir`、`filename_pattern`、`timeout`、`start_time` | `Path` |
| 异常详情格式化 | direct python | `format_exception_detail` | —（仅模块导入） | `exception_utils.py` | `e` | `str` |
| 拼多多商家中心登录 | direct python | `login_pdd_seller` | —（仅模块导入） | `shop_utils.py` | `account`、`password`、`profile` | `bool` |
| 千牛商家工作台登录 | direct python | `login_qianniu` | —（仅模块导入） | `shop_utils.py` | `account`、`password`、`profile` | `bool` |
| 京麦商家工作台登录 | direct python | `login_jingmai` | —（仅模块导入） | `shop_utils.py` | `account`、`password`、`profile` | `bool` |
| 支付宝登录 | direct python | `login_alipay` | —（仅模块导入） | `shop_utils.py` | `account`、`password`、`profile` | `bool` |
| 抖音店铺登录 | direct python | `login_douyin_seller` | —（仅模块导入） | `shop_utils.py` | `account`、`password`、`profile` | `bool` |
| Win 元素可点击判断 | direct python | `is_win_element_clickable` | —（仅模块导入） | `win_utils.py` | `element` | `bool` |
| WPS / Excel 占用者识别 | direct python | `get_wps_lock_user` | — | `excel_utils.py` | `workbook` | 占用者用户名、`"未知用户"` 或 `None` |
| 发送 ntfy 消息 | direct python | `send_ntfy_message` | —（仅模块导入） | `ntfy_message.py` | `message`、`topic`、`server` | `bool` |
| 接收 ntfy 消息 | direct python | `receive_ntfy_message` | —（仅模块导入） | `ntfy_message.py` | `topic`、`server`、`since`、`timeout` | 按时间倒序的消息列表；无消息为空列表 |

---

### 2.10 activity_excel_v2 — Excel扩展操作

| 指令显示名 | 调用类型 | 对应 function | __init__.py 入口 | 独立 Python | 主要入参 | 主要出参 |
|---|---|---|---|---|---|---|
| 批量向下填充(公式) | flow | `fill_down_formula` | `fill_down_formula()` | `fill_down_formula.py` | excel_instance、formula_content、column、begin_row、end_row、sheet_name、数组公式 | — |
| 批量向右填充(公式) | flow | `fill_right_formula` | `fill_right_formula()` | `fill_right_formula.py` | excel_instance、formula_content、row、begin_column、end_column、sheet_name、array_formula_mode | — |
| 自动向下填充 | flow | `process31` | `process31()` | `process31.py` | excel_instance、begin_row、begin_column、end_row、end_column、填充类型、sheet_name | — |
| 空白单元格填充(向上填充) | flow | `process36` | `process36()` | `process36.py` | excel_instance、begin_row、begin_column、end_row、end_column、sheet_name | — |
| 公式转换成值 | flow | `process52` | `process52()` | `process52.py` | excel_instance、dim、set_range、sheet_name | — |
| 新建注释 | flow | `process53` | `process53()` | `process53.py` | excel_instance、row_num、column_name、comment、sheet_name | — |
| 分列 | flow | `process19` | `process19()` | `process19.py` | excel_instance、column、分隔符设置、行列范围、sheet_name、destination_column、field_info | — |
| 区域截图 | flow | `process24` | `process24()` | `process24.py` | excel_instance、begin_row、begin_column、end_row、end_column、save_path、sheet_name | image_save_path |
| 内容替换 | flow | `process26` | `process26()` | `process26.py` | excel_instance、search_text、replace_text、替换范围、替换区域、lookat、sheet_name、case_sensitive | — |
| 获取单元格超链接 | flow | `process32` | `process32()` | `process32.py` | excel_instance、col_name、row_num、sheet_name | hyperlink |
| 设置单元格超链接 | flow | `process33` | `process33()` | `process33.py` | excel_instance、row_num、col_name、address、sheet_name、subaddress、screentip、texttodisplay | — |
| 合并单元格 / 取消单元格合并 | flow | `process34` | `process34()` | `process34.py` | excel_instance、is_merge、begin_row、begin_column、end_row、end_column、sheet_name | — |
| 读取单元格注释 | flow | `process37` | `process37()` | `process37.py` | excel_instance、column、row、sheet_name | comment |
| 导出单元格的图片 | flow | `process42` | `process42()` | `process42.py` | excel_instance、sheet_name、column_name、row_number、folder_path | pic_path |
| 删除单元格的图片 | flow | `process45` | `process45()` | `process45.py` | Excel对象、Sheet页名称、行号、列名 | — |
| 区域文本转数字 | flow | `text_format_to_num` | `text_format_to_num()` | `text_format_to_num.py` | excel_instance、begin_row、begin_column、end_row、end_column、sheet_name | — |
| 区域数字转文本 | flow | `num_format_to_text` | `num_format_to_text()` | `num_format_to_text.py` | excel_instance、begin_row、begin_column、end_row、end_column、sheet_name | — |
| 获取背景色 | flow | `process54` | `process54()` | `process54.py` | excel_instance、dim、target_range、sheet_name | background_color |
| 获取合并单元格区域 | flow | `process55` | `process55()` | `process55.py` | excel_instance、row、column、sheet_name | is_merge、merge_range |
| 筛选 | flow | `filter` | `filter()` | `filter.py` | excel_instance、row、column、select_content、select_type、sheet_name、operator、select_content2、select_type2 | — |
| 清除筛选 | flow | `process16` | `process16()` | `process16.py` | excel_instance、column_name、sheet_name | — |
| 删除筛选内容 | flow | `process20` | `process20()` | `process20.py` | excel_instance、begin_row、end_row、removefiltermode、sheet_name | — |
| 读取筛选内容 | flow | `process21` | `process21()` | `process21.py` | excel_instance、begin_row、content_type、sheet_name、using_text、using_text_cols、data_columns | filter_content |
| 筛选颜色 | flow | `process38` | `process38()` | `process38.py` | excel_instance、xl_filter、column_name、row_num、rgb、sheet_name | — |
| 数字列名转换 | flow | `process23` | `process23()` | `process23.py` | text_input、convert_type | convert_result |
| 查找数据所在列 | flow | `process27` | `process27()` | `process27.py` | excel_instance、row、search_text、find_all、lookat、sheet_name、num_flag、look_in | column_name |
| 查找数据所在行 | flow | `process28` | `process28()` | `process28.py` | excel_instance、column、search_text、find_all、lookat、sheet_name | 查找结果 |
| 生成字典(数值累加) | flow | `process29` | `process29()` | `process29.py` | excel_instance、key_column、value_column、begin_row、end_row、sheet_name | result_dict |
| 生成字典(列表拼接) | flow | `process30` | `process30()` | `process30.py` | excel_instance、key_column、value_column、begin_row、end_row、sheet_name | result_dict |
| 单元格填充图片 | flow | `process18` | `process18()` | `process18.py` | excel_instance、image_path、row_num、column_name、row_height、colnum_width、sheet_name、lockaspectratio、placement、compress | — |
| 删除所有图片 | flow | `process44` | `process44()` | `process44.py` | excel_instance、sheet_name | — |
| 隐藏 / 取消隐藏 Sheet 页 | flow | `process46` | `process46()` | `process46.py` | Excel对象、Sheet页名称、设置为 | — |
| 获取隐藏的 Sheet 页 | flow | `process47` | `process47()` | `process47.py` | Excel对象 | 隐藏的工作表名列表 |
| 合并计算 | flow | `process48` | `process48()` | `process48.py` | Excel对象、行号、列名、函数、所引用的位置、Sheet页名称、创建指向数据源的链接、最左侧、首列 | — |
| 设置/取消密码 | flow | `process49` | `process49()` | `process49.py` | Excel对象、打开密码、编辑密码 | — |
| 自动换行 | flow | `process51` | `process51()` | `process51.py` | Excel对象、自动换行范围、自动换行区域、operation、Sheet页名称 | — |
| 冻结首行 | flow | `process56` | `process56()` | `process56.py` | excel_instance、kind、area、sheet_name | — |
| 设置切片器 | flow | `process57` | `process57()` | `process57.py` | excel_instance、slicercache_name、item_name、selected | — |
| 刷新透视表 | flow | `refresh_pivot_table` | —（模块导入） | `refresh_pivot_table.py` | excel_instance、sheet_name | — |
| 执行文本宏 | flow | `process58` | `process58()` | `process58.py` | excel_instance、macro_name、macro_string | — |

**调用方式总结：**
- 公开指令均来自 `prototype.block.json` 中 `hidden=false` 的 block，共 40 个。
- 编码版优先通过 `xbot_extensions.activity_excel_v2.<入口函数>(...)` 调用 `__init__.py` 包装入口，再由 `xbot_visual.process.run()` 执行对应 Visual flow；`refresh_pivot_table` 是模块导入型入口，按 `refresh_pivot_table.main(args)` 调用。
- `utils`、`validators`、`invoke_modules`、`tmp`、`test_*` 等模块属于内部工具或测试模块，不作为公开指令记录。

---

### 2.11 activity_a90a8311 — C-ERP 市场指令

| 指令显示名 | 调用类型 | 对应 function | 主要入参 | 主要出参 |
|---|---|---|---|---|
| init_v2 | flow | `process13` | username、password、ERP浏览器标识、refresh | ERP网页对象 |
| 库存下载 | flow | `process4` | 商品代码、规格代码、仓库名称 | file_path |
| 发货商品汇总下载 | flow | `process12` | 店铺名称、发货时间start、发货时间end、店铺汇总 | file_path |
| 发货订单明细下载 | flow | `process14` | 店铺名称、发货时间start、发货时间end | file_path |
| 退货商品明细下载 | flow | `process15` | 店铺名称、发货时间start、发货时间end | file_path |

**调用方式总结：**
- 先用 `process13(...)` 初始化或复用 ERP 页面，再调用下载入口。
- 下载类入口按文件路径使用，返回空值时立即抛出明确异常，不要继续调用 `xbot.excel.open()`。
- `process12` 的 `发货时间start` 和 `发货时间end` 都表示对应日期的 `00:00`，时间范围按 `[start, end)` 处理；下载 `2026/08/01` 应传 `2026/08/01` 到 `2026/08/02`，不要把起止日期传成同一天。
- 当前未发现等价的原生 `xbot` ERP 业务接口，因此保留该市场指令。
- 详细参数与示例见 [C-ERP 市场指令](extensions/activity-a90a8311-cerp-visual.md)。

---

### 2.12 activity_df0688e4 — ERP 订单详情查询与字段翻译

| 指令显示名 | 调用类型 | 对应 function | 主要入参 | 主要出参 |
|---|---|---|---|---|
| 订单查询详情 | direct python | `select_order_dteail.main(args)` | `platform_code` 或 `code` | 原始订单详情或 `None` |
| 翻译 Dict | direct python | `translation.main(args)` | `record` | 中文字段数据 |

**调用方式总结：**
- `platform_code` 和 `code` 至少提供一个，否则抛出 `ValueError`。
- 先查当前订单，再查历史订单；查询过程异常继续向上抛出。
- 详细参数与示例见 [ERP 订单详情查询与字段翻译](extensions/activity-df0688e4.md)。

---

### 2.13 activity_179ea575 — 离线 OCR

| 指令显示名 | 调用类型 | 对应 function | 主要入参 | 主要出参 |
|---|---|---|---|---|
| 离线 OCR | flow | `process1` | 图片路径或图片url、输出完整结果、文字检测框过滤的阈值、文字检测框的大小 | OCR 结果 |

**调用方式总结：**
- 支持本地图片路径和网络图片 URL。
- 当前未发现等价的原生 `xbot` OCR 接口，可保留为 OCR 实现。
- 完整结果字段和识别准确率需在目标图片上运行验证。
- 详细参数与示例见 [离线 OCR](extensions/activity-179ea575.md)。

---

## 三、调用规则

### 3.1 package.json 定位 flow 指令

```json
{
  "name": "指令集名称",
  "activity_code": "activity_xxxxxxx",
  "startup": "main",
  "flows": [
    {
      "name": "显示名",
      "filename": "process1",    // ← 对应 process1.py 或 __init__.py 中的 process1()
      "kind": "Visual",          // ← Visual=可视化流程, Code=编码流程
      "groupName": "分组名"
    }
  ]
}
```

**规则：**
- `kind=Visual` → 通过 `__init__.py` 中的 `processN()` 包装函数调用
- `kind=Code` → 直接调用对应 `.py` 文件中的 `main()` 函数
- `filename` 与 `__init__.py` 中的函数名一致（Visual）或与 `.py` 文件名一致（Code）

### 3.2 prototype.block.json 确认界面参数

```json
{
  "blocks": [
    {
      "name": "xbot_extensions.activity_xxx.process1",
      "title": "显示标题",
      "function": "xbot_extensions.activity_xxx.process1",
      "hidden": false,      // ← false=对外可见, true=内部使用
      "inputs": [
        {
          "name": "参数名",   // ← 编码版传入的参数名
          "label": "界面标签", // ← 可视化界面显示名
          "type": "text",     // ← 参数类型
          "default": "..."    // ← 默认值
        }
      ],
      "outputs": [
        {"name": "返回值名"}
      ]
    }
  ]
}
```

**规则：**
- `hidden=true` 的 block 是内部子流程，不对外暴露
- `inputs[].name` 是编码版真实参数名（可能与界面中文不同）
- `outputs[].name` 是返回值名

### 3.3 __init__.py 找到真实调用入口

**Visual 型 flow 的标准包装模式：**

```python
def process1(参数1, 参数2):
    """
    指令显示名
    * @param 参数1，参数说明
    * @param 参数2，参数说明
    * @return 返回值，返回值说明
    """
    outputs = ["返回值"]
    inputs = {"参数1": 参数1, "参数2": 参数2}
    extension_module, activity_func = xbot_visual.process.activity_entry(
        "xbot_extensions.activity_xxx.process1", __name__)
    try:
        return xbot_visual.process.run(
            process="xbot_extensions.activity_xxx.process1",
            package=__name__,
            inputs=inputs,
            outputs=outputs)
    finally:
        xbot_visual.process.replace_activity_module_to_entry_method(
            "xbot_extensions.activity_xxx.process1", extension_module, activity_func)
```

**规则：**
- `outputs` 列表中的字符串必须与 `prototype.block.json` 中 `outputs[].name` 一致
- `inputs` 字典的 key 必须与 `prototype.block.json` 中 `inputs[].name` 一致
- 编码版调用：`xbot_extensions.activity_xxx.process1(参数1, 参数2)`

### 3.4 core.py / _core.py 判断真实业务逻辑

- `core.py` / `_core.py` 通常包含真实业务类和方法
- `__init__.py` 只是包装层，真实逻辑在 core 中
- 例：`ad_killer._core.py` 中的 `AdKiller.close_ads()` 是真实关闭逻辑
- 例：`guanyi_erp_api.core.py` 中的 `make_sign()`、`build_payload()`、`gy_call()` 是管易 API 签名和请求封装

### 3.5 独立 .py 文件作为直接调用入口

**Code 型 flow 的标准模式：**

```python
# filename.py
def main(args):
    # 真实业务逻辑
    pass
```

**规则：**
- Code 型 flow 直接调用 `.py` 文件中的 `main()` 函数
- `main()` 的参数 `args` 是 `package.variables` 中的全局变量
- 如果该 `.py` 同时被 import，也可以直接调用其中的其他函数

---

## 四、开发指令

各市场指令的详细参数、调用示例和注意事项已拆分到独立页面：

| 指令目录 | 指令名 | 调用类型 | 详细说明 |
|---|---|---|---|
| `activity_47680f64` | 小工具指令集 | both | [activity-47680f64.md](extensions/activity-47680f64.md) |
| `activity_5b77c4ce` | 钉钉AI表格 | direct python | [activity-5b77c4ce.md](extensions/activity-5b77c4ce.md) |
| `dingtalk_bot_message` | 钉钉企业机器人消息_v2 | direct python 优先 | [dingtalk-bot-message.md](extensions/dingtalk-bot-message.md) |
| `activity_7bca6d` | 登录扩展操作 | both | [activity-7bca6d.md](extensions/activity-7bca6d.md) |
| `guanyi_erp_api` | C-ERP API | direct python | [guanyi-erp-api.md](extensions/guanyi-erp-api.md) |
| `activity_a90a8311` | C-ERP 市场指令 | flow | [activity-a90a8311-cerp-visual.md](extensions/activity-a90a8311-cerp-visual.md) |
| `activity_df0688e4` | ERP订单详情查询与字段翻译 | direct python | [activity-df0688e4.md](extensions/activity-df0688e4.md) |
| `activity_179ea575` | 离线 OCR | flow | [activity-179ea575.md](extensions/activity-179ea575.md) |
| `iframe2` | XPath跨域获取网页元素 | both | [iframe2-extension.md](iframe2-extension.md) |
| `ad_killer` | 广告杀手 | both | [ad-killer.md](extensions/ad-killer.md) |
| `web_action` | 网页扩展操作 | both | [web-action.md](extensions/web-action.md) |
| `xbot_enhance_tools` | 增强工具2026 | direct python | [xbot-enhance-tools.md](extensions/xbot-enhance-tools.md) |
| `activity_excel_v2` | Excel扩展操作 | flow | [activity-excel-v2.md](extensions/activity-excel-v2.md) |

---

## 五、证据引用

### 5.1 文件路径汇总

| 结论 | 文件路径 |
|---|---|
| package.json 结构 | `activity_*/package.json`、`ad_killer/package.json`、`web_action/package.json` |
| block 定义 | `activity_*/prototype.block.json` |
| __init__.py 包装模式 | `activity_47680f64/__init__.py`、`dingtalk_bot_message/__init__.py`、`ad_killer/__init__.py`、`web_action/__init__.py` |
| Excel扩展操作公开指令 | `activity_excel_v2/prototype.block.json`：`hidden=false` 的 40 个公开 block |
| Excel扩展操作包装入口 | `activity_excel_v2/__init__.py`：`fill_down_formula()`、`filter()`、`process16()` 等包装函数；`refresh_pivot_table` 为模块导入 |
| Excel扩展操作分组 | `activity_excel_v2/package.json` flows 列表中的 `A_单元格填充`、`B_单元格操作`、`C_筛选`、`D_其他` |
| 增强工具包入口 | `xbot_enhance_tools/__init__.py`：当前不提供 processN 包装；编码版能力从各独立模块直接导入 |
| 浏览器等待增强 | `xbot_enhance_tools/browser_utils.py`：`wait_appear_by_xpath()`、`wait_disappear_by_xpath()`、`wait_download_file()` |
| 异常详情格式化 | `xbot_enhance_tools/exception_utils.py`：`format_exception_detail()` |
| 商家后台登录辅助 | `xbot_enhance_tools/shop_utils.py`：`login_pdd_seller()`、`login_qianniu()`、`login_jingmai()`、`login_alipay()` |
| Windows 元素判断辅助 | `xbot_enhance_tools/win_utils.py`：`is_win_element_clickable()` |
| Excel / WPS 占用者识别 | `xbot_enhance_tools/excel_utils.py`：`get_wps_lock_user(workbook)` |
| ntfy 消息发送与接收 | `xbot_enhance_tools/ntfy_message.py`：`send_ntfy_message()`、`receive_ntfy_message()` |
| processN() 标准包装 | `activity_47680f64/__init__.py:process2` 第 18-28 行、`web_action/__init__.py:process1` 第 5-15 行 |
| 仅 import 无包装 | `activity_5b77c4ce/__init__.py`、`guanyi_erp_api/__init__.py` |
| close_ads 默认值 | `ad_killer/_core.py` 第 25-28 行：`close_type` 默认 `"hidden"` |
| AdKiller 类定义 | `ad_killer/_core.py` 第 22-65 行 |
| core.py 签名封装 | `guanyi_erp_api/core.py` 第 30-45 行：`make_sign()`、`build_payload()` |
| 钉钉机器人 Direct API | `dingtalk_bot_message/py_api.py`：`send_dingtalk_group()`、`send_dingtalk_private()` |
| ERP订单详情查询 | `activity_df0688e4/select_order_dteail.py`：当前订单、历史订单查询与返回规则 |
| ERP字段翻译 | `activity_df0688e4/translation.py`：递归字段映射与 `new_record` 输出 |
| 离线 OCR 参数 | `activity_179ea575/__init__.py`：`process1()` 包装参数 |
| 通用表格操作参数 | `activity_5b77c4ce/prototype.block.json`：`general_table_action` block |
| 智能日期选择器 | `web_action/select_date.py`：`select_date()` 函数 |
| 通用下拉框 | `web_action/auto_drop_selector.py`：`set_dropdown()` 函数 |
| 元素核心操作 | `web_action/element_core.py`：`hide_element`、`show_element`、`remove_element` 等 |
| 管易 API 地址 | `guanyi_erp_api/core.py` 第 24 行：`API_URL = "http://api.guanyierp.com/rest/erp_open"` |
| 钉钉 AI 表格 action 枚举 | `activity_5b77c4ce/prototype.block.json`：`general_table_action` inputs[0] editor.options |
| 登录扩展操作分组 | `activity_7bca6d/package.json` flows 列表中的 groupName 字段 |
| 广告杀手内置配置 | `ad_killer/ad_conf.py`：`ad_conf` 字典 |

### 5.2 通用调用规律总结

```
影刀指令调用链：

1. Flow 型（Visual）：
   package.json flows[kind=Visual]
   → prototype.block.json [hidden=false]
   → __init__.py processN() 包装函数
   → xbot_visual.process.run()
   → .dev/processN.flow.json.enc（可视化流程定义）

2. Flow 型（Code）：
   package.json flows[kind=Code]
   → prototype.block.json [hidden=false]
   → 直接调用 filename.py 中的 main()
   （无 __init__.py 包装）

3. Direct Python：
   直接 import 并调用 .py 文件中的函数
   不经过 xbot_visual.process.run()
```

---

## 附录：快速查询

### 按场景查询

| 场景 | 推荐目录 | 推荐指令 |
|---|---|---|
| 文件下载/移动/解压 | `activity_47680f64` | `process1`、`process2` |
| 钉钉表格操作 | `activity_5b77c4ce` | `general_table_action`、`yd_ai_table_action` |
| 钉钉消息通知 | `dingtalk_bot_message` | `process1`、`process2`、`to_markdown_table` |
| Excel 公式填充 / 筛选 / 单元格扩展操作 | `activity_excel_v2` | `fill_down_formula`、`filter`、`process21`、`process56` |
| 电商后台登录 | `activity_7bca6d` / `xbot_enhance_tools` | `activity_7bca6d` 提供成熟登录流程；`xbot_enhance_tools.shop_utils` 提供轻量账号密码登录辅助 |
| ERP 数据查询 | `guanyi_erp_api` | `select_stock`、`select_item`、`select_order_list` |
| 跨 iframe XPath 查找 / 点击 / 输入 / 等待 | `iframe2` | `init_iframe`、`to_iframe`、`find_ele`、`click_by_xpath`、`input_by_xpath`、`wait` |
| XPath 等待 / 下载等待 / 异常详情格式化 / 轻量商家登录 / Windows 元素可点击判断 / ntfy 消息 | `xbot_enhance_tools` | `wait_appear_by_xpath`、`wait_disappear_by_xpath`、`wait_download_file`、`format_exception_detail`、`shop_utils`、`is_win_element_clickable`、`send_ntfy_message`、`receive_ntfy_message` |
| 关闭网页广告 | `ad_killer` | `close_ads`、`close_ads_win` |
| 网页元素扩展操作 | `web_action` | `process1`(滚动)、`process4`(背景色)、`select_date` |

### 按调用类型查询

| 调用类型 | 目录 |
|---|---|
| 仅 Flow | `activity_excel_v2` |
| 仅 Direct Python | `activity_5b77c4ce`、`xbot_enhance_tools`、`guanyi_erp_api` |
| Flow + Direct | `activity_47680f64`、`dingtalk_bot_message`、`activity_7bca6d`、`iframe2`、`ad_killer`、`web_action` |
