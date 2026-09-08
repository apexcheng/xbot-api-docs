# C-ERP API (guanyi_erp_api)

> 调用类型：`direct python`  
> 主要入口：直接调用 `__init__.py` 已导入的各业务模块 `.main(args)`；`core.py` 属于共享实现，不作为业务代码默认入口。
> 证据边界：本页公开入口已按当前安装版本源码核对；接口凭证和服务可用性仍需按当前项目验证。
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
| `select_stock.main(args)` | 查询库存 | `max_page_no`、`item_code`、`item_sku_code`、`warehouse_code` | 写入 `args['stocks']`；无显式返回值 |
| `select_item.main(args)` | 查询商品 | `max_page_no`、`code`、`combine` | 写入 `args['items']`；无显式返回值 |
| `select_combine_item.main(args)` | 查询组合商品 | `code` | 写入 `args['context']`、`args['items']`；无显式返回值 |
| `translation.main(args)` | 翻译 Dict | `record` | 写入 `args['new_record']`，并返回翻译结果 |
| `select_order_dteail.main(args)` | 查询订单详情 | `code`、`platform_code` | 写入 `args['order_detail']`，并返回订单详情 |
| `select_order_list.main(args)` | 查询订单列表 | `date_type`、`shop_code`、`code`、`has_cancel_data`、`start_date`、`end_date` | 写入 `args['orders']`；无显式返回值 |
| `select_item_by_sku_code.main(args)` | 按商品条码查询商品 | `商品条码` | 写入 `args['items']`；无显式返回值 |

**参数说明：**
- `APP_KEY`、`SESSION_KEY`、`SECRET`：当前扩展业务模块在导入时从自身 `package.variables` 读取，不是上述 `main(args)` 的调用参数。不要把凭证塞进 `args` 期待覆盖模块级配置。
- `code`：商品编码 / 订单编号
- `platform_code`：平台代码
- `start_date`、`end_date`：日期范围
- `max_page_no`：最大页码

不同入口的参数并不通用。例如库存查询有 `item_code` / `item_sku_code` / `warehouse_code`，订单列表有 `date_type` / `shop_code` / `has_cancel_data`。调用时按目标入口的真实参数使用，不要把上面的概括参数列表当成所有函数都支持的公共参数集。

**返回值约定：** 该扩展多数 Code 流通过修改传入的 `args` 写回输出，而不是 `return` 结果。当前已确认 `translation.main(args)` 和 `select_order_dteail.main(args)` 同时有显式返回值；其它上述 `main(args)` 不要按“直接返回列表”使用。

**注意事项：**
- `core.py` 提供共享 API 签名和请求封装，但当前 `__init__.py` 没有把它作为业务入口导出；业务代码默认调用上表模块，不直接绕到 `core.py`。
- `select_item.main(args)` 当前源码虽然读取了 `item_sku_code`，但没有把它传给实际商品查询函数，因此本页不把它列为有效筛选参数；不要因为看到局部变量就假定该筛选已生效。
- `select_order_list` 的底层查询函数支持更多筛选条件，包括 `platform_code`，但当前 `main(args)` 没有向下传递这些额外参数；调用 `main(args)` 时只按上表已确认参数使用。
- 模块文件名 `select_order_dteail` 是扩展现有拼写，调用时不要自行改成 `detail`。

**典型调用方式：**
```text
非执行调用说明（不可直接运行）：

from xbot_extensions.guanyi_erp_api import select_stock

params = {
    "max_page_no": 10,
    "warehouse_code": "WH001",
}
select_stock.main(params)
stocks = params["stocks"]
```

---
