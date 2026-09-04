# C-ERP API (guanyi_erp_api)

> 调用类型：`direct python`  
> 主要入口：直接调用各业务 .py 或 core.py 中的函数；__init__.py 仅做模块导入。  
> 证据边界：接口凭证、服务可用性和返回结构需按当前项目验证。
> 返回：[市场指令索引](../extension-instructions.md)

---

**目录/指令名：** `guanyi_erp_api` / C-ERP API

**调用方式：** direct python

**用途：** 管易 ERP / C-ERP 的库存查询、商品查询、订单查询

**调用入口：**
- `xbot_extensions.guanyi_erp_api.select_stock.main(args)`
- `xbot_extensions.guanyi_erp_api.select_item.main(args)`
- `xbot_extensions.guanyi_erp_api.select_order_list.main(args)`
- `xbot_extensions.guanyi_erp_api.select_order_dteail.main(args)`
- `xbot_extensions.guanyi_erp_api.select_combine_item.main(args)`
- `xbot_extensions.guanyi_erp_api.select_item_by_sku_code.main(args)`

**公开入口参数速查：**

| 入口 | 用途 | 主要入参 | 主要输出 |
|---|---|---|---|
| `select_stock.main(args)` | 查询库存 | max_page_no、app_key、session_key、secret、item_code、item_sku_code、warehouse_code | `stocks` |
| `select_item.main(args)` | 查询商品 | max_page_no、code、app_key、session_key、secret、combine | `items` |
| `select_combine_item.main(args)` | 查询组合商品 | code | `items`、`context` |
| `translation.main(args)` | 翻译 Dict | record | `new_record` |
| `select_order_dteail.main(args)` | 查询订单详情 | code、platform_code | `order_detail` |
| `select_order_list.main(args)` | 查询订单列表 | platform_code、date_type、shop_code、code、has_cancel_data、start_date、end_date | `orders` |
| `select_item_by_sku_code.main(args)` | 按商品条码查询商品 | 商品条码 | `items` |

**参数说明：**
- `app_key`、`session_key`、`secret`：ERP 接口凭证（来自 `package.variables`）
- `code`：商品编码 / 订单编号
- `platform_code`：平台代码
- `start_date`、`end_date`：日期范围
- `max_page_no`：最大页码

不同入口的参数并不通用。例如库存查询有 `item_code` / `item_sku_code` / `warehouse_code`，订单列表有 `date_type` / `shop_code` / `has_cancel_data`。调用时按目标入口的真实参数使用，不要把上面的概括参数列表当成所有函数都支持的公共参数集。

**返回值：** 查询结果列表（items、orders、stocks 等）

**注意事项：**
- `core.py` 提供 API 签名和请求封装：`make_sign()`、`build_payload()`、`gy_call()`
- API 地址：`http://api.guanyierp.com/rest/erp_open`
- 签名规则：`MD5(secret + json_str + secret).upper()`
- 所有业务 `.py` 文件通过 `package.variables` 读取 `APP_KEY`、`SESSION_KEY`、`SECRET`

**典型调用方式：**
```python
from xbot_extensions.guanyi_erp_api import select_stock
from xbot_extensions.guanyi_erp_api.core import build_payload, gy_call

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
from xbot_extensions.guanyi_erp_api.core import build_payload, gy_call

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
