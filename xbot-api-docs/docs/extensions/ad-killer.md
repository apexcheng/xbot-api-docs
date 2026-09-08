# 广告杀手 (ad_killer)

> 调用类型：`Visual / Direct Python`
> 公开入口：`close_ads()` / `close_ads_win()`
> 证据边界：`close_type` 等枚举以当前安装版本为准。
> 返回：[市场指令索引](../extension-instructions.md)

## 用途与入口

- `xbot_extensions.ad_killer.close_ads(网页对象, 广告Xpath, 使用内置广告Xpath, 关闭方式)`：异步处理网页广告。
- `xbot_extensions.ad_killer.close_ads_win(元素选择器列表)`：后台监测 Win32 弹窗。

| 参数 | 说明 |
|---|---|
| `广告Xpath` | 自定义广告元素 XPath |
| `使用内置广告Xpath` | 是否同时使用扩展内置名单，默认 `False` |
| `关闭方式` | `"hidden"` 隐藏元素（默认），或 `"click"` 点击关闭元素 |
| `元素选择器列表` | Win32 弹窗的选择器列表 |

`"hidden"` 不依赖广告存在可点击的关闭按钮；`"click"` 只适用于 XPath 能定位真实关闭元素的情况。网页刷新后需重新调用 `close_ads()`；Win32 监测随主流程结束。

## 最小调用

```text
非执行调用说明（不可直接运行）：

from xbot_extensions.ad_killer import close_ads

close_ads(
    网页对象=web_page,
    广告Xpath="//button[@class='close-btn']",
    使用内置广告Xpath=False,
    关闭方式="click",
)
```

业务代码只使用公开入口，不直接导入扩展的私有实现模块。
