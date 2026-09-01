# ERP 订单详情查询与字段翻译（activity_df0688e4）

> 调用类型：`direct python`
> 证据等级：已从市场指令源码和真实项目调用确认；ERP 接口可用性仍依赖当前账号、网络和服务状态。
> 返回：[市场指令索引](../extension-instructions.md)

---

## 1. 适用场景

根据 ERP 订单号或平台订单号查询订单详情，再把返回字典中的英文字段递归翻译为中文字段，便于后续业务代码直接读取。

## 2. 调用入口

```python
from xbot_extensions.activity_df0688e4 import select_order_dteail, translation
```

查询订单详情：

```python
result = select_order_dteail.main({"platform_code": order_no})
```

翻译字段：

```python
order_data = translation.main({"record": result}) or {}
```

## 3. `select_order_dteail.main(args)`

支持以下查询参数，至少传一个：

| 参数 | 类型 | 说明 |
|---|---|---|
| `platform_code` | `str` | 平台订单号 |
| `code` | `str` | ERP 订单号 |

最小示例：

```python
from xbot_extensions.activity_df0688e4 import select_order_dteail


order_detail = select_order_dteail.main({"platform_code": "平台订单号"})
if not order_detail:
    raise RuntimeError("未查询到 ERP 订单详情")
```

已确认行为：

- `platform_code` 和 `code` 均未提供时抛出 `ValueError`。
- 先查询当前订单；未找到时继续查询历史订单。
- 查询成功返回 ERP 原始订单详情字典；未找到返回 `None`。
- 执行过程中会把结果写入传入字典的 `order_detail` 字段。
- 网络请求或 ERP 接口异常会继续向上抛出，调用方不要静默吞掉。

## 4. `translation.main(args)`

```python
from xbot_extensions.activity_df0688e4 import translation


translated = translation.main({"record": order_detail}) or {}
```

该入口递归翻译字典和列表中的字段名，并把结果写入传入字典的 `new_record` 字段。常见映射包括：

| 原字段 | 中文字段 |
|---|---|
| `details` | `商品明细` |
| `shop_name` | `店铺名称` |
| `item_code` | `商品代码` |
| `item_sku_name` | `规格名称` |

业务字段应以实际返回结果为准，不要假设每笔订单都包含所有字段。

## 5. 推荐完整写法

```python
from xbot_extensions.activity_df0688e4 import select_order_dteail, translation


raw_order = select_order_dteail.main({"platform_code": order_no})
if not raw_order:
    raise RuntimeError(f"未查询到 ERP 订单：{order_no}")

order_data = translation.main({"record": raw_order}) or {}
shop_name = order_data.get("店铺名称")
details = order_data.get("商品明细") or []
```

## 6. 注意事项

- 模块文件名为源码中的 `select_order_dteail`，包含既有拼写，调用时不要自行改成 `detail`。
- 不要把 ERP 凭证、接口密钥或真实订单信息写入知识库。
- 返回空值与接口异常是不同情况：空值表示未查到，异常表示查询过程失败。
