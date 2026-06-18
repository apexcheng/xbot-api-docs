# 影刀市场指令扩展开发指南

> 分析范围：8 个常用市场指令目录
> 分析日期：2026-06-08
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
| `activity_6f13bae5` | 钉钉企业机器人消息_v2 | both | ✅ | ✅ | ✅ (process1/2/3) | ✅ (core.py) | ✅ (4 个) |
| `activity_7bca6d` | 登录扩展操作 | both | ✅ | ✅ | ✅ (17 个 process) | ❌ | ✅ (11 个业务) |
| `activity_dae43741` | 增强工具2026 | direct python | ✅ | ✅ | ✅ (仅模块导入) | ❌ | ✅ (`browser_utils.py`、`exception_utils.py`、`shop_utils.py`) |
| `activity_df0688e4` | C-ERP API | direct python | ✅ | ✅ | ✅ (仅 import) | ✅ (core.py) | ✅ (7 个业务) |
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

### 2.3 activity_6f13bae5 — 钉钉企业机器人消息_v2

| 指令显示名 | 调用类型 | 对应 function | __init__.py 入口 | 独立 Python | 主要入参 | 主要出参 |
|---|---|---|---|---|---|---|
| 发送私聊消息 | flow | `process1` | `process1()` | — | app_key、app_secret、title、message_type、content、user_mobiles | result |
| 发送群聊消息 | flow | `process2` | `process2()` | — | app_key、app_secret、open_conversation_id、title、message_type、content、webhook_url、webhook_secret、at_mobiles、at_all | result |
| 群聊使用说明 | flow | `process3` | `process3()` | — | — | help |
| 生成markdown表格 | direct python | `to_table_format` | —（import） | `to_table_format.py` | data、max_cell_length | md_table |

**调用方式总结：**
- process1/process2/process3 通过 `__init__.py` 包装调用 Visual flow
- `core.py` 是底层发送逻辑（`send_dingtalk_group`、`send_dingtalk_private`、`send_text`、`send_markdown`、`send_image`），不直接暴露为指令
- `to_table_format.py` 可直接调用 `to_markdown_table(data, max_cell_length)`

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

### 2.5 activity_df0688e4 — C-ERP API

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

### 2.8 activity_dae43741 — 增强工具2026

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
- 例：`activity_df0688e4.core.py` 中的 `make_sign()`、`build_payload()`、`gy_call()` 是管易 API 签名和请求封装

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

### 4.1 小工具指令集 (activity_47680f64)

**目录/指令名：** `activity_47680f64` / 小工具指令集

**调用方式：** both（flow + direct python）

**用途：** 文件操作、日期处理、邮件获取、验证码获取

**调用入口：**
- Flow：`xbot_extensions.activity_47680f64.process1()` ~ `process5()`
- Direct：`CreateDir.main()`、`MoveToPardir.main()`、`DateStringCheck.main()`、`latest_email.main()`、`get_SMS_code.main()`

**参数说明：**
- `process2(是否弹窗下载, 保存文件夹, 文件名, 下载前文件数量, 浏览器下载保存路径, 最大等待时长)`

**默认值：**
- 浏览器下载保存路径：默认 `$HOME/Downloads`

**注意事项：**
- Code 型指令直接调用 `.py` 中的 `main()`，不是 `__init__.py` 中的包装函数
- Visual 型指令（process1~5）通过 `__init__.py` 包装调用
- `latest_email.py` 支持 163 邮箱，需要 email + password
- `get_SMS_code.py` 需要配置验证码获取接口 URL

**典型调用方式：**
```python
# Flow 型
xbot_extensions.activity_47680f64.process2(
    是否弹窗下载=False,
    保存文件夹="/save",
    文件名="file.zip",
    下载前文件数量=0,
    浏览器下载保存路径="",
    最大等待时长=30
)
```

---

### 4.2 钉钉AI表格 (activity_5b77c4ce)

**目录/指令名：** `activity_5b77c4ce` / 钉钉AI表格

**调用方式：** direct python

**用途：** 钉钉多维表格（AI 表格）的增删改查

**调用入口：**
- `xbot_extensions.activity_5b77c4ce.general_table_action.main(args)`
- 底层 SDK：`croe.py` 中的 `yd_ai_table_action()` 及 `yd_*` 系列函数

**通用调用格式：**

```python
from xbot_extensions.activity_5b77c4ce.croe import yd_ai_table_action

result = yd_ai_table_action(
    action="创建数据表",
    client_id="你的client_id",
    client_secret="你的client_secret",
    base_id="你的base_id",
    user_id="你的user_id",
    params={...}
)
```

**通用参数：**

| 参数 | 必填 | 说明 |
|---|---|---|
| `action` | 是 | 操作类型（中文 action 名） |
| `client_id` | 是 | 钉钉应用 AppKey |
| `client_secret` | 是 | 钉钉应用 AppSecret |
| `base_id` | 视 action | AI 表格 baseId |
| `sheet` | 视 action | 数据表名称或 ID，**推荐传 ID** |
| `space_id` | 视 action | 钉盘空间 ID |
| `user_id` | 身份三选一 | 推荐传这个，脚本自动转 unionId |
| `operator_id` | 身份三选一 | unionId |
| `sender_union_id` | 身份三选一 | 也可作为操作者身份 |
| `params` | 否 | 业务参数（字典或 JSON 字符串） |

**身份参数：** `user_id`、`operator_id`、`sender_union_id` 至少传一个。普通使用直接传 `user_id`。

---

#### Action 详解

##### 数据表操作

**创建数据表**
- `action="创建数据表"`
- `params.sheet_name`（必填）：新数据表名称
- `params.fields`（可选）：初始化字段列表，每项含 `name` 和 `type`

```json
{
  "sheet_name": "测试数据表",
  "fields": [
    {"name": "标题", "type": "text"},
    {"name": "金额", "type": "number"}
  ]
}
```

**获取所有数据表**
- `action="获取所有数据表"`
- 仅需 `base_id`

**获取数据表**
- `action="获取数据表"`
- `params.sheet`（必填）：数据表 ID

**更新数据表**
- `action="更新数据表"`
- `params.sheet`（必填）、`params.new_name`（必填）

**删除数据表**
- `action="删除数据表"`
- `params.sheet`（必填）

---

##### 字段操作

**新增字段**
- `action="新增字段"`
- `params.sheet`、`params.field_name`（必填）
- `params.field_type`（可选，默认 `text`）：`text`、`number`、`date`、`checkbox`、`singleSelect`、`multipleSelect`、`attachment`
- `params.field_property`（可选）：字段属性字典

```json
{
  "sheet": "rPbLtRx",
  "field_name": "金额",
  "field_type": "number"
}
```

**获取所有字段**
- `action="获取所有字段"`
- `params.sheet`（必填）

**更新字段**
- `action="更新字段"`
- `params.sheet`、`params.field`（字段 ID，推荐）
- `params.new_name`、`params.field_type`、`params.field_property` 至少传一个

**删除字段**
- `action="删除字段"`
- `params.sheet`、`params.field`（必填）

---

##### 记录操作

**新增多行记录**
- `action="新增多行记录"`
- `params.sheet`、`params.records`（必填）

```json
{
  "sheet": "rPbLtRx",
  "records": [
    {"标题": "第一行", "金额": 1},
    {"标题": "第二行", "金额": 2}
  ]
}
```

**新增记录**
- `action="新增记录"`
- `params.sheet`、`params.record`（必填）

**获取多行记录**
- `action="获取多行记录"`
- `params.sheet`（必填）
- `params.max_results`（可选，1~100）
- `params.next_token`（可选）：分页游标

**获取多行记录分页**
- `action="获取多行记录分页"`
- `params.sheet`（必填）
- `params.page_size`（可选）、`params.max_pages`（可选）

**获取记录**
- `action="获取记录"`
- `params.sheet`、`params.record_id`（必填）

**更新记录**
- `action="更新记录"`
- `params.sheet`、`params.record_id`、`params.fields`（必填）

```json
{
  "sheet": "rPbLtRx",
  "record_id": "44jzHpsgbx",
  "fields": {"金额": 100, "状态": "已更新"}
}
```

**更新多行记录**
- `action="更新多行记录"`
- `params.sheet`、`params.records`（必填）
- 每条记录必须带 `id`（也接受 `recordId`、`record_id`）

```json
{
  "sheet": "rPbLtRx",
  "records": [
    {"id": "44jzHpsgbx", "fields": {"金额": 100}},
    {"id": "nApqiOPYVe", "fields": {"金额": 101}}
  ]
}
```

**删除多条记录**
- `action="删除多条记录"`
- `params.sheet`、`params.record_ids`（必填，列表或逗号字符串）

---

##### 附件操作

附件上传流程（脚本自动完成）：
1. 申请上传信息 → 2. PUT 上传文件 → 3. 将 `resourceId` 写入附件字段

附件字段值格式：
```json
[{"filename": "demo.pdf", "resourceId": "xxx"}]
```

**上传附件**
- `action="上传附件"`
- `params.file_path`（必填）
- `params.filename`、`params.mime_type`（可选）
- `params.upload_info`（可选）：一般不用传，脚本自动申请

```json
{
  "file_path": "/tmp/demo.pdf",
  "filename": "demo.pdf",
  "mime_type": "application/pdf"
}
```

返回 `result.attachment` 可直接用于后续写入附件字段。

**上传附件并新增记录**
- `action="上传附件并新增记录"`
- `params.sheet`、`params.attachment_field`、`params.file_path`（必填）
- `params.fields`（可选）：其他普通字段

**上传附件并更新记录**
- `action="上传附件并更新记录"`
- `params.sheet`、`params.record_id`、`params.attachment_field`、`params.file_path`（必填）

---

##### 空间与文件操作

**获取空间列表**
- `action="获取空间列表"`（别名：`"获取space_id"`、`"获取spaceId"`）
- `params.max_results`（可选，1~50）、`params.space_type`（可选，默认 `org`）

**获取空间列表分页**
- `action="获取空间列表分页"`
- `params.page_size`、`params.max_pages`（可选）

**获取空间信息**
- `action="获取空间信息"`
- `params.space_id`（必填）

**获取文件列表**
- `action="获取文件列表"`
- `params.space_id`（必填）、`params.parent_id`（可选）

**获取文件列表分页**
- `action="获取文件列表分页"`
- `params.space_id`（必填）

**获取AI表格列表 / 搜索AI表格 / 搜索表格文件**
- `action="获取AI表格列表"` / `"搜索AI表格"` / `"搜索表格文件"`
- `params.space_id`（必填）、`params.keyword`（可选）
- `params.only_ai_table_candidates`（可选）：是否只保留看起来像 AI 表格的文件

> 文件接口通常需要钉钉应用开通 `Drive.File.Read` 权限。

---

**注意事项：**
- `sheet`、`field`、`record_id` 虽然支持"名称或 ID"，但**推荐优先传 ID**
- `更新多行记录` 时每条记录必须带 `id`（或 `recordId` / `record_id`）
- `__init__.py` 没有包装函数，直接调用 `general_table_action.py` 中的 `main()` 或 import `croe.py` 的函数
- 如需更精细控制，可直接 import `croe.py` 中的函数

**典型调用方式：**
```python
from xbot_extensions.activity_5b77c4ce.croe import yd_ai_table_action

# 创建数据表
result = yd_ai_table_action(
    action="创建数据表",
    client_id="xxx", client_secret="xxx",
    base_id="xxx", user_id="xxx",
    params={"sheet_name": "新表", "fields": [{"name": "标题", "type": "text"}]}
)

# 新增记录
result = yd_ai_table_action(
    action="新增记录",
    client_id="xxx", client_secret="xxx",
    base_id="xxx", user_id="xxx",
    params={"sheet": "rPbLtRx", "record": {"标题": "测试", "金额": 100}}
)

# 获取记录列表（自动分页）
result = yd_ai_table_action(
    action="获取多行记录分页",
    client_id="xxx", client_secret="xxx",
    base_id="xxx", user_id="xxx",
    params={"sheet": "rPbLtRx", "page_size": 50, "max_pages": 10}
)
```

**项目里的推荐包装方式：**

```python
def table_action(action, client_id, client_secret, base_id, user_id, sheet, params=None):
    from xbot_extensions.activity_5b77c4ce.croe import yd_ai_table_action

    result = yd_ai_table_action(
        action=action,
        client_id=client_id,
        client_secret=client_secret,
        base_id=base_id,
        user_id=user_id,
        sheet=sheet,
        params=params or {},
    )
    if not isinstance(result, dict):
        raise ValueError(f"表格操作 {action} 返回异常: {result!r}")
    return result


records = table_action(
    "获取多行记录分页",
    client_id, client_secret, base_id, user_id,
    sheet="账号表",
    params={"page_size": 100, "max_pages": 100},
).get("data", {}).get("records") or []
```

补充约定：

- 项目里更推荐先统一封装 `yd_ai_table_action()`，再让业务层读取 `data.records`。
- 记录结构进入业务逻辑后，优先直接按 `record["fields"]` 使用；多选字段显示值取 `.get("name")`。

---

### 4.3 钉钉企业机器人消息_v2 (activity_6f13bae5)

**目录/指令名：** `activity_6f13bae5` / 钉钉企业机器人消息_v2

**调用方式：** both

**用途：** 发送钉钉私聊消息、群聊消息、生成 markdown 表格

**调用入口：**
- Flow：`xbot_extensions.activity_6f13bae5.process1(app_key, app_secret, title, message_type, content, user_mobiles)`
- Flow：`xbot_extensions.activity_6f13bae5.process2(app_key, app_secret, open_conversation_id, title, message_type, content, webhook_url, webhook_secret, at_mobiles, at_all)`
- Direct：`xbot_extensions.activity_6f13bae5.to_table_format.to_markdown_table(data, max_cell_length)`

**参数说明：**
- `message_type`：消息类型（`text` / `markdown` / `image`）
- `content`：文本/markdown内容 或 图片路径
- `user_mobiles`：接收人手机号列表（私聊，自动换取 userId）
- `webhook_url` / `webhook_secret`：自定义机器人 webhook
- `at_mobiles` / `at_all`：@ 相关

**返回值：** `result`（发送结果）

**注意事项：**
- 群聊图片需要 `app_key` + `app_secret` + `open_conversation_id`
- 群聊文本/Markdown 可以用 webhook 机器人
- `to_table_format.py` 可直接调用生成 markdown 表格

**典型调用方式：**
```python
# 发送私聊消息
xbot_extensions.activity_6f13bae5.process1(
    app_key="xxx", app_secret="xxx",
    title="通知", message_type="markdown",
    content="## 标题\n内容", user_mobiles=["13800138000"]
)

# 生成 markdown 表格
from xbot_extensions.activity_6f13bae5.to_table_format import to_markdown_table
md = to_markdown_table(
    data=[["a", "b"], ["1", "2"]],
    max_cell_length=100
)
```

**项目里的 Markdown 群通知模式：**

```python
from xbot_extensions.activity_6f13bae5 import process2 as send_group_message
from xbot.app import logging

try:
    send_group_message(
        app_key=app_key,
        app_secret=app_secret,
        open_conversation_id=open_conversation_id,
        title="商品链接价格监测完成",
        message_type="markdown",
        content=content,
        webhook_url="",
        webhook_secret="",
        at_mobiles=[],
        at_all=False,
    )
except Exception as e:
    logging.error(f"钉钉群通知发送失败：{e}")
```

补充约定：

- 群通知里更推荐 `title` 和 `content` 分离，正文统一传 Markdown。
- 如果通知失败只影响提醒链路，不影响主业务，可只记录日志，不中断主流程。

---

### 4.4 登录扩展操作 (activity_7bca6d)

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

### 4.5 C-ERP API (activity_df0688e4)

**目录/指令名：** `activity_df0688e4` / C-ERP API

**调用方式：** direct python

**用途：** 管易 ERP / C-ERP 的库存查询、商品查询、订单查询

**调用入口：**
- `xbot_extensions.activity_df0688e4.select_stock.main(args)`
- `xbot_extensions.activity_df0688e4.select_item.main(args)`
- `xbot_extensions.activity_df0688e4.select_order_list.main(args)`
- `xbot_extensions.activity_df0688e4.select_order_dteail.main(args)`
- `xbot_extensions.activity_df0688e4.select_combine_item.main(args)`
- `xbot_extensions.activity_df0688e4.select_item_by_sku_code.main(args)`

**参数说明：**
- `app_key`、`session_key`、`secret`：ERP 接口凭证（来自 `package.variables`）
- `code`：商品编码 / 订单编号
- `platform_code`：平台代码
- `start_date`、`end_date`：日期范围
- `max_page_no`：最大页码

**返回值：** 查询结果列表（items、orders、stocks 等）

**注意事项：**
- `core.py` 提供 API 签名和请求封装：`make_sign()`、`build_payload()`、`gy_call()`
- API 地址：`http://api.guanyierp.com/rest/erp_open`
- 签名规则：`MD5(secret + json_str + secret).upper()`
- 所有业务 `.py` 文件通过 `package.variables` 读取 `APP_KEY`、`SESSION_KEY`、`SECRET`

**典型调用方式：**
```python
from xbot_extensions.activity_df0688e4 import select_stock
from xbot_extensions.activity_df0688e4.core import build_payload, gy_call

# 通过 flow 调用（参数通过 package.variables 传入）
select_stock.main(args)

# 直接调用 core 函数
payload = build_payload(
    method="gy.erp.stock.get",
    warehouse_code="WH001"
)
result = gy_call(payload)
```

**调用模板：从 `package.variables` 读取 ERP 凭证**

```python
from . import package
from xbot_extensions.activity_df0688e4.core import build_payload, gy_call

payload = build_payload(
    method="gy.erp.order.get",
    app_key=package.variables["APP_KEY"],
    session_key=package.variables["SESSION_KEY"],
    secret=package.variables["SECRET"],
    code=package.variables["order_code"],
)
result = gy_call(payload)
```

---

### 4.6 广告杀手 (ad_killer)

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

### 4.7 网页扩展操作 (web_action)

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

### 4.8 增强工具2026 (activity_dae43741)

**目录/指令名：** `activity_dae43741` / 增强工具2026

**调用方式：** direct python

**用途：** 面向 `xbot` 的增强工具包。当前已收录浏览器 XPath 等待、下载等待、异常详情格式化和商家后台登录辅助。

**调用入口：**
- `from xbot_extensions.activity_dae43741 import exception_utils, browser_utils, shop_utils`
- `from xbot_extensions.activity_dae43741.browser_utils import wait_appear_by_xpath`
- `from xbot_extensions.activity_dae43741.browser_utils import wait_disappear_by_xpath`
- `from xbot_extensions.activity_dae43741.browser_utils import wait_download_file`
- `from xbot_extensions.activity_dae43741.exception_utils import format_exception_detail`
- `from xbot_extensions.activity_dae43741.shop_utils import login_pdd_seller`
- `from xbot_extensions.activity_dae43741.shop_utils import login_qianniu`
- `from xbot_extensions.activity_dae43741.shop_utils import login_jingmai`
- `from xbot_extensions.activity_dae43741.shop_utils import login_alipay`

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

from xbot_extensions.activity_dae43741.browser_utils import (
    wait_appear_by_xpath,
    wait_disappear_by_xpath,
    wait_download_file,
)
from xbot_extensions.activity_dae43741.exception_utils import format_exception_detail
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
from xbot_extensions.activity_dae43741 import shop_utils


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

## 五、证据引用

### 5.1 文件路径汇总

| 结论 | 文件路径 |
|---|---|
| package.json 结构 | `activity_*/package.json`、`ad_killer/package.json`、`web_action/package.json` |
| block 定义 | `activity_*/prototype.block.json` |
| __init__.py 包装模式 | `activity_47680f64/__init__.py`、`activity_6f13bae5/__init__.py`、`ad_killer/__init__.py`、`web_action/__init__.py` |
| 仅模块导入型增强工具 | `activity_dae43741/__init__.py`：仅导入 `package`、`xbot_visual`、`exception_utils`、`browser_utils`、`shop_utils` |
| 浏览器等待增强 | `activity_dae43741/browser_utils.py`：`wait_appear_by_xpath()`、`wait_disappear_by_xpath()`、`wait_download_file()` |
| 异常详情格式化 | `activity_dae43741/exception_utils.py`：`format_exception_detail()` |
| 商家后台登录辅助 | `activity_dae43741/shop_utils.py`：`login_pdd_seller()`、`login_qianniu()`、`login_jingmai()`、`login_alipay()` |
| processN() 标准包装 | `activity_47680f64/__init__.py:process2` 第 18-28 行、`web_action/__init__.py:process1` 第 5-15 行 |
| 仅 import 无包装 | `activity_5b77c4ce/__init__.py`、`activity_df0688e4/__init__.py` |
| close_ads 默认值 | `ad_killer/_core.py` 第 25-28 行：`close_type` 默认 `"hidden"` |
| AdKiller 类定义 | `ad_killer/_core.py` 第 22-65 行 |
| core.py 签名封装 | `activity_df0688e4/core.py` 第 30-45 行：`make_sign()`、`build_payload()` |
| 钉钉机器人参数 | `activity_6f13bae5/__init__.py:process1` 第 5-25 行 |
| 通用表格操作参数 | `activity_5b77c4ce/prototype.block.json`：`general_table_action` block |
| 智能日期选择器 | `web_action/select_date.py`：`select_date()` 函数 |
| 通用下拉框 | `web_action/auto_drop_selector.py`：`set_dropdown()` 函数 |
| 元素核心操作 | `web_action/element_core.py`：`hide_element`、`show_element`、`remove_element` 等 |
| 管易 API 地址 | `activity_df0688e4/core.py` 第 24 行：`API_URL = "http://api.guanyierp.com/rest/erp_open"` |
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
| 钉钉消息通知 | `activity_6f13bae5` | `process1`、`process2`、`to_markdown_table` |
| 电商后台登录 | `activity_7bca6d` / `activity_dae43741` | `activity_7bca6d` 提供成熟登录流程；`activity_dae43741.shop_utils` 提供轻量账号密码登录辅助 |
| ERP 数据查询 | `activity_df0688e4` | `select_stock`、`select_item`、`select_order_list` |
| 跨 iframe XPath 查找 / 点击 / 输入 / 等待 | `iframe2` | `init_iframe`、`to_iframe`、`find_ele`、`click_by_xpath`、`input_by_xpath`、`wait` |
| XPath 等待 / 下载等待 / 异常详情格式化 / 轻量商家登录 | `activity_dae43741` | `wait_appear_by_xpath`、`wait_disappear_by_xpath`、`wait_download_file`、`format_exception_detail`、`shop_utils` |
| 关闭网页广告 | `ad_killer` | `close_ads`、`close_ads_win` |
| 网页元素扩展操作 | `web_action` | `process1`(滚动)、`process4`(背景色)、`select_date` |

### 按调用类型查询

| 调用类型 | 目录 |
|---|---|
| 仅 Flow（Visual） | —（所有支持 Flow 的目录也支持 Direct） |
| 仅 Direct Python | `activity_5b77c4ce`、`activity_dae43741`、`activity_df0688e4` |
| Flow + Direct | `activity_47680f64`、`activity_6f13bae5`、`activity_7bca6d`、`iframe2`、`ad_killer`、`web_action` |
