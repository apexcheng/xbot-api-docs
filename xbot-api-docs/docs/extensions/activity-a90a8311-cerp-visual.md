# C-ERP 市场指令

> 来源：本地已安装市场指令目录 `xbot_robot`。  
> 指令 UUID：`86515626-37c2-4a22-971b-62cf6971df12`。  
> Activity code：`activity_a90a8311`。  
> 调用类型：Visual flow 包装入口；当前未发现等价的原生 `xbot` ERP 业务接口。
> 记录原则：只记录从 `package.json`、`prototype.block.json`、`__init__.py` 可确认的信息；页面行为、筛选条件效果和下载结果需运行验证。

---

## 1. 调用方式

编码版通过 `xbot_extensions.activity_a90a8311` 暴露的包装函数调用：

```python
from xbot_extensions import activity_a90a8311

web = activity_a90a8311.process13(username=username, password=password, ERP浏览器标识="Default", refresh=True)
file_path = activity_a90a8311.process14(店铺名称=None, 发货时间start="2026/08/01", 发货时间end="2026/08/05")
if not file_path:
    raise RuntimeError("发货订单明细下载未返回文件路径")
```

包装函数内部会组装 `inputs` / `outputs`，再调用：

```python
xbot_visual.process.run(
    process="xbot_extensions.activity_a90a8311.processN",
    package=__name__,
    inputs=inputs,
    outputs=outputs,
)
```

因此编码版调用时优先使用 `__init__.py` 暴露的 `processN(...)` 函数，不要直接猜可视化块内部参数。

本包的 `process4` 是 `__init__.py` 中定义的函数，不是模块，因此不要写成 `activity_a90a8311.process4.main(...)`。`.main(...)` 只适用于实际导入的是带 `main` 入口的独立代码模块。

---

## 2. 公开指令

| 指令 | 函数 | 入参 | 出参 | 说明 |
|---|---|---|---|---|
| 库存下载 | `process4(商品代码, 规格代码, 仓库名称)` | `商品代码: str`、`规格代码: str`、`仓库名称: str` | `file_path: str` | 过滤式下载库存 |
| 进入选项卡 | `process5(菜单项Name, web)` | `菜单项Name: str`、`web: WebBrowser` | 无 | 进入菜单项，如库存统计、订单查看；`web` 界面提示为可选 |
| 获取下载文件 | `process8(文件关键词, 下载时间, 等待超时)` | `文件关键词: str`、`下载时间: datetime`、`等待超时: int` | `file_path: str` | 等待超时单位为秒 |
| init初始化ERP | `process10(username, password, ERP浏览器标识)` | `username: str`、`password: str`、`ERP浏览器标识: str` | `ERP网页对象: WebBrowser` | 使用前初始化 ERP |
| 平台铺货下载 | `process11(平台类型, 店铺名称, 平台商品ID)` | `平台类型: str`、`店铺名称: str`、`平台商品ID: str` | `file_path: str` | 过滤式下载平台铺货 |
| 发货商品汇总下载 | `process12(店铺名称, 发货时间start, 发货时间end, 店铺汇总)` | `店铺名称: str`、`发货时间start: str`、`发货时间end: str`、`店铺汇总: bool` | `file_path: str` | 日期格式为 `yyyy/mm/dd`；时间范围按 `[start, end)` 处理 |
| init_v2 | `process13(username, password, ERP浏览器标识, refresh)` | `username: str`、`password: str`、`ERP浏览器标识: str`、`refresh: bool` | `ERP网页对象: WebBrowser` | 如果已有网页则不打开新页面；`refresh` 表示已有网页时是否刷新 |
| 发货订单明细下载 | `process14(店铺名称, 发货时间start, 发货时间end)` | `店铺名称: str`、`发货时间start: str`、`发货时间end: str` | `file_path: str` | 日期格式提示为 `yyyy/mm/dd` |
| 退货商品明细下载 | `process15(店铺名称, 发货时间start, 发货时间end)` | `店铺名称: str`、`发货时间start: str`、`发货时间end: str` | `file_path: str` | 日期格式提示为 `yyyy/mm/dd` |

---

## 3. 默认值与参数提示

以下默认值来自 `prototype.block.json`：

| 函数 | 参数 | 默认值 / 提示 |
|---|---|---|
| `process4` | `仓库名称` | 默认 `正品仓` |
| `process8` | `等待超时` | 默认 `600`，单位：秒 |
| `process10` | `username` / `password` | 默认示例值为 `1123`，实际项目不要写死账号密码 |
| `process10` | `ERP浏览器标识` | 默认 `Default`，界面提示必填 |
| `process11` | `平台类型` | 默认 `淘宝` |
| `process12` | `发货时间start` / `发货时间end` | 必填，格式 `yyyy/mm/dd`；两者都表示对应日期的 `00:00`，范围按 `[start, end)` 处理 |
| `process12` | `店铺汇总` | 默认 `False` |
| `process13` | `ERP浏览器标识` | 默认 `Default` |
| `process13` | `refresh` | 默认 `False` |

---

## 4. 推荐调用顺序

优先使用 `init_v2` 初始化或复用 ERP 页面：

```python
from xbot_extensions import activity_a90a8311

web = activity_a90a8311.process13(username=username, password=password, ERP浏览器标识="Default", refresh=True)
```

需要进入某个菜单页时：

```python
activity_a90a8311.process5("库存统计", web)
```

下载类指令直接返回 `file_path`：

```python
stock_path = activity_a90a8311.process4(商品代码=None, 规格代码=None, 仓库名称="正品仓")
platform_path = activity_a90a8311.process11("淘宝", "店铺名称", "平台商品ID")
summary_path = activity_a90a8311.process12("BOW官方旗舰店", "2026/08/01", "2026/08/05", False)
order_path = activity_a90a8311.process14(店铺名称=None, 发货时间start="2026/08/01", 发货时间end="2026/08/05")
return_path = activity_a90a8311.process15(店铺名称=None, 发货时间start="2026/08/01", 发货时间end="2026/08/05")

for report_name, file_path in {
    "库存": stock_path,
    "平台铺货": platform_path,
    "发货商品汇总": summary_path,
    "发货订单明细": order_path,
    "退货商品明细": return_path,
}.items():
    if not file_path:
        raise RuntimeError(f"{report_name}下载未返回文件路径")
```

真实项目中下载类入口均按“返回文件路径”使用。调用后应立即检查返回值，避免后续把空值传给 `xbot.excel.open()`。

`process12` 的日期参数是时间边界，不是“起止日期都包含”。例如下载 `2026/08/01` 一整天，应传入 `2026/08/01 00:00` 到 `2026/08/02 00:00`：

```python
from datetime import timedelta

download_start_text = download_date.strftime("%Y/%m/%d")
download_end_text = (download_date + timedelta(days=1)).strftime("%Y/%m/%d")
file_path = activity_a90a8311.process12("BOW官方旗舰店", download_start_text, download_end_text, False)
```

不要把同一个日期同时传给 `发货时间start` 和 `发货时间end`，否则时间范围为空，无法表示当天完整数据。

如果需要等待并获取下载文件：

```python
file_path = activity_a90a8311.process8("文件关键词", None, 600)
```

---

## 5. 需运行验证

以下内容当前只能从可视化流程名称和参数提示推断，不能写成已验证结论：

- `菜单项Name` 支持的完整菜单名称列表。
- `平台类型` 除默认 `淘宝` 外的完整可选值。
- `店铺名称`、`平台商品ID`、`商品代码`、`规格代码` 为空时的真实筛选行为。
- 各下载流程触发下载后的文件命名规则、下载目录和失败返回形态。
- `process10` 与 `process13` 在已有浏览器、登录态失效、`refresh=True` 时的行为差异。

---

## 6. 证据文件

| 结论 | 文件 |
|---|---|
| 指令名称、UUID、activity code、flows、全局变量 | `package.json` |
| 公开块、参数类型、默认值、输出名 | `prototype.block.json` 中 `hidden=false` 的 blocks |
| 编码版包装函数、入参顺序、输出列表、`xbot_visual.process.run` 调用方式 | `__init__.py` |

不要把该市场指令目录下的完整源码、流程文件、选择器文件或账号密码提交到知识库。
